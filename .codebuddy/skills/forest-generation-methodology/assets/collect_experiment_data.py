#!/usr/bin/env python3
"""
实验数据归集脚本 (Step 5)

从 reviews/ 目录的评审报告中自动提取评分数据，
生成对照矩阵和统计量，更新 .experiment_metadata.yaml。

用法:
    python collect_experiment_data.py <experiment_dir>

输出:
    - results/comparison-matrix-models.md  (对照矩阵)
    - 控制台统计摘要

前置条件:
    - reviews/ 目录中已有评审报告（含 frontmatter + 评分表格）
    - 评审报告 frontmatter 须包含: reviewer_model, reviewee_model, reviewer_aai, reviewee_aai
"""
import os
import sys
import re
import yaml
import json
from pathlib import Path
from collections import defaultdict


def parse_review_report(filepath):
    """从评审报告中提取 frontmatter 和评分数据。"""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 提取 frontmatter
    fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)", content, re.DOTALL)
    if not fm_match:
        return None

    try:
        frontmatter = yaml.safe_load(fm_match.group(1)) or {}
    except yaml.YAMLError:
        frontmatter = {}

    body = fm_match.group(2)

    # 提取 D1-D5 评分（多种格式兼容）
    scores = {}
    dim_patterns = {
        "D1": [r"D1[^|]*?(\d+\.?\d*)\s*/?\s*(?:10)?", r"引用真实性[^|]*?(\d+\.?\d*)"],
        "D2": [r"D2[^|]*?(\d+\.?\d*)\s*/?\s*(?:10)?", r"引用准确性[^|]*?(\d+\.?\d*)"],
        "D3": [r"D3[^|]*?(\d+\.?\d*)\s*/?\s*(?:10)?", r"层级组织[^|]*?(\d+\.?\d*)"],
        "D4": [r"D4[^|]*?(\d+\.?\d*)\s*/?\s*(?:10)?", r"批判性分析[^|]*?(\d+\.?\d*)"],
        "D5": [r"D5[^|]*?(\d+\.?\d*)\s*/?\s*(?:10)?", r"学术规范[^|]*?(\d+\.?\d*)"],
    }

    for dim, patterns in dim_patterns.items():
        for pattern in patterns:
            match = re.search(pattern, body, re.IGNORECASE)
            if match:
                try:
                    scores[dim] = float(match.group(1))
                    break
                except (ValueError, IndexError):
                    continue

    # 尝试从 frontmatter 提取（如果正文没找到）
    for dim in ["D1", "D2", "D3", "D4", "D5"]:
        if dim not in scores:
            fm_key = f"{dim.lower()}_score"
            if fm_key in frontmatter:
                scores[dim] = float(frontmatter[fm_key])

    # 提取综合评分
    overall_patterns = [r"综合[^|]*?(\d+\.?\d*)", r"overall[^|]*?(\d+\.?\d*)"]
    for pattern in overall_patterns:
        match = re.search(pattern, body, re.IGNORECASE)
        if match:
            scores["overall"] = float(match.group(1))
            break

    if "overall" not in scores and all(d in scores for d in ["D1", "D2", "D3", "D4", "D5"]):
        scores["overall"] = round(sum(scores[d] for d in ["D1", "D2", "D3", "D4", "D5"]) / 5, 1)

    return {
        "file": Path(filepath).name,
        "reviewer": frontmatter.get("reviewer_model", "unknown"),
        "reviewer_aai": frontmatter.get("reviewer_aai", "?"),
        "reviewee": frontmatter.get("reviewee_model", "unknown"),
        "reviewee_aai": frontmatter.get("reviewee_aai", "?"),
        "bias_risk": frontmatter.get("bias_risk", "?"),
        "scores": scores,
    }


def collect_reviews(reviews_dir):
    """收集所有评审报告。"""
    reviews = []
    review_path = Path(reviews_dir)

    if not review_path.exists():
        print(f"错误: reviews/ 目录不存在: {reviews_dir}")
        return reviews

    for md_file in sorted(review_path.glob("review-*.md")):
        result = parse_review_report(md_file)
        if result and result["scores"]:
            reviews.append(result)
            print(f"  ✓ {result['file']}: {result['reviewer']} -> {result['reviewee']} "
                  f"(D1={result['scores'].get('D1', '?')}, 综合={result['scores'].get('overall', '?')})")
        else:
            print(f"  ✗ {md_file.name}: 无法提取评分")

    return reviews


def compute_stats(reviews):
    """计算每个被评审者的双评审均值和评审者间一致性。"""
    # 按被评审者分组
    by_reviewee = defaultdict(list)
    for r in reviews:
        by_reviewee[r["reviewee"]].append(r)

    # 计算每个被评审者的均值
    reviewee_stats = {}
    for reviewee, revs in by_reviewee.items():
        dims = ["D1", "D2", "D3", "D4", "D5", "overall"]
        means = {}
        for dim in dims:
            values = [r["scores"][dim] for r in revs if dim in r["scores"]]
            if values:
                means[dim] = round(sum(values) / len(values), 1)

        # 评审者间一致性
        agreement = 0
        total = 0
        for dim in ["D1", "D2", "D3", "D4", "D5"]:
            values = [r["scores"][dim] for r in revs if dim in r["scores"]]
            if len(values) >= 2:
                total += 1
                if all(v == values[0] for v in values):
                    agreement += 1

        reviewee_stats[reviewee] = {
            "reviewers": [r["reviewer"] for r in revs],
            "means": means,
            "agreement": f"{agreement}/{total}" if total > 0 else "N/A",
            "agreement_rate": f"{agreement/total*100:.1f}%" if total > 0 else "N/A",
        }

    return reviewee_stats


def generate_matrix(stats, output_path):
    """生成对照矩阵 markdown。"""
    lines = [
        "# 对照矩阵：不同模型（脚本自动生成）",
        "",
        "> 由 collect_experiment_data.py 自动生成，请人工验证后使用。",
        "",
        "## 五维度评分（双评审均值）",
        "",
        "| 维度 | " + " | ".join(stats.keys()) + " |",
        "|------|" + "|".join(["---" for _ in stats]) + "|",
    ]

    for dim in ["D1", "D2", "D3", "D4", "D5", "overall"]:
        row = f"| {dim} |"
        for reviewee in stats:
            val = stats[reviewee]["means"].get(dim, "?")
            row += f" {val} |"
        lines.append(row)

    lines.extend([
        "",
        "## 评审者间一致性",
        "",
        "| 被评审模型 | 评审者 | 一致率 |",
        "|-----------|--------|:---:|",
    ])

    for reviewee, s in stats.items():
        lines.append(f"| {reviewee} | {', '.join(s['reviewers'])} | {s['agreement_rate']} |")

    lines.extend([
        "",
        "## 评审报告清单",
        "",
        "| 被评审模型 | 评审者 | D1 | D2 | D3 | D4 | D5 | 综合 |",
        "|-----------|--------|:---:|:---:|:---:|:---:|:---:|:---:|",
    ])

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"\n对照矩阵已生成: {output_path}")


def main():
    if len(sys.argv) < 2:
        print("用法: python collect_experiment_data.py <experiment_dir>")
        print("示例: python collect_experiment_data.py exp-model-20260716-01/")
        sys.exit(1)

    exp_dir = Path(sys.argv[1])
    reviews_dir = exp_dir / "reviews"
    results_dir = exp_dir / "results"

    print("=" * 60)
    print("实验数据归集 (Step 5)")
    print("=" * 60)
    print(f"\n实验目录: {exp_dir}")
    print(f"评审目录: {reviews_dir}\n")

    # 收集评审
    print("提取评审数据:")
    reviews = collect_reviews(reviews_dir)

    if not reviews:
        print("\n错误: 未找到有效评审报告")
        sys.exit(1)

    # 计算统计量
    print(f"\n计算统计量:")
    stats = compute_stats(reviews)

    for reviewee, s in stats.items():
        print(f"  {reviewee}: 综合={s['means'].get('overall', '?')}, "
              f"一致性={s['agreement_rate']}")

    # 生成对照矩阵
    results_dir.mkdir(exist_ok=True)
    matrix_path = results_dir / "comparison-matrix-models.md"
    generate_matrix(stats, matrix_path)

    # 汇总
    print(f"\n{'=' * 60}")
    print("归集完成")
    print(f"{'=' * 60}")
    print(f"  评审报告数: {len(reviews)}")
    print(f"  被评审模型数: {len(stats)}")
    print(f"  对照矩阵: {matrix_path}")
    print(f"\n下一步:")
    print(f"  1. 人工验证对照矩阵数据")
    print(f"  2. 由非实验参与者（MiniMax-M3）撰写 REPORT.md")


if __name__ == "__main__":
    main()
