#!/usr/bin/env python3
"""
实验数据归集脚本 (Step 5)

从用户指定的评审报告文件中自动提取评分数据，
生成对照矩阵和统计量。

用法:
    python collect_experiment_data.py <review_files...> [--output PATH]

示例:
    # 维度1（模型对照）— shell 自动展开通配符
    python collect_experiment_data.py reviews/review-*.md --output results/matrix.md

    # 维度2（工具对照）
    python collect_experiment_data.py reviews/*.md --output results/matrix-tools.md

    # 明确指定文件
    python collect_experiment_data.py review-a-by-b.md review-a-by-c.md

前置条件:
    - 评审报告含 frontmatter（reviewee_model 或 reviewee_tool 或 reviewee_material）
    - 评审报告正文含 D1-D5 评分数据
"""
import os
import sys
import re
import argparse
import yaml
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
        "frontmatter": frontmatter,
        "reviewer": frontmatter.get("reviewer_model") or frontmatter.get("reviewer_tool", "unknown"),
        "reviewer_aai": frontmatter.get("reviewer_aai", "?"),
        "reviewee": frontmatter.get("reviewee_model") or frontmatter.get("reviewee_tool") or frontmatter.get("reviewee_material", "unknown"),
        "reviewee_aai": frontmatter.get("reviewee_aai", "?"),
        "bias_risk": frontmatter.get("bias_risk", "?"),
        "scores": scores,
    }


def collect_reviews(file_list):
    """从用户指定的文件列表中收集评审报告。"""
    reviews = []
    for filepath in file_list:
        if not os.path.exists(filepath):
            print(f"  ✗ {filepath}: 文件不存在")
            continue
        result = parse_review_report(filepath)
        if result and result["scores"]:
            reviews.append(result)
            print(f"  ✓ {result['file']}: {result['reviewer']} -> {result['reviewee']} "
                  f"(D1={result['scores'].get('D1', '?')}, 综合={result['scores'].get('overall', '?')})")
        else:
            print(f"  ✗ {filepath}: 无法提取评分")
    return reviews


def detect_group_key(reviews):
    """自动检测分组键：reviewee_tool > reviewee_material > reviewee_model。"""
    for r in reviews:
        fm = r.get("frontmatter", {})
        if fm.get("reviewee_tool"):
            return "reviewee_tool", "工具"
        if fm.get("reviewee_material"):
            return "reviewee_material", "资料"
    return "reviewee_model", "模型"


def compute_stats(reviews, group_key):
    """按分组键计算均值和评审者间一致性。"""
    # 按分组键分组
    by_group = defaultdict(list)
    for r in reviews:
        group_value = r["frontmatter"].get(group_key, r.get("reviewee", "unknown"))
        by_group[group_value].append(r)

    # 计算每组的均值
    group_stats = {}
    for group_value, revs in by_group.items():
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

        group_stats[group_value] = {
            "reviewers": [r["reviewer"] for r in revs],
            "means": means,
            "agreement": f"{agreement}/{total}" if total > 0 else "N/A",
            "agreement_rate": f"{agreement/total*100:.1f}%" if total > 0 else "N/A",
        }

    return group_stats


def generate_matrix(stats, output_path, dimension_label):
    """生成对照矩阵 markdown。"""
    lines = [
        f"# 对照矩阵：不同{dimension_label}（脚本自动生成）",
        "",
        "> 由 collect_experiment_data.py 自动生成，请人工验证后使用。",
        "",
        f"## 五维度评分（双评审均值）",
        "",
        f"| 维度 | " + " | ".join(stats.keys()) + " |",
        "|------|" + "|".join(["---" for _ in stats]) + "|",
    ]

    for dim in ["D1", "D2", "D3", "D4", "D5", "overall"]:
        row = f"| {dim} |"
        for group_value in stats:
            val = stats[group_value]["means"].get(dim, "?")
            row += f" {val} |"
        lines.append(row)

    lines.extend([
        "",
        "## 评审者间一致性",
        "",
        f"| 被评审{dimension_label} | 评审者 | 一致率 |",
        "|-----------|--------|:---:|",
    ])

    for group_value, s in stats.items():
        lines.append(f"| {group_value} | {', '.join(s['reviewers'])} | {s['agreement_rate']} |")

    lines.extend([
        "",
        "## 评审报告清单",
        "",
        f"| 被评审{dimension_label} | 评审者 | D1 | D2 | D3 | D4 | D5 | 综合 |",
        "|-----------|--------|:---:|:---:|:---:|:---:|:---:|:---:|",
    ])

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"\n对照矩阵已生成: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="实验数据归集 (Step 5)")
    parser.add_argument("review_files", nargs="+", help="评审报告文件路径（可用 shell 通配符）")
    parser.add_argument("--output", default="results/comparison-matrix.md",
                        help="对照矩阵输出路径（默认 results/comparison-matrix.md）")
    args = parser.parse_args()

    print("=" * 60)
    print("实验数据归集 (Step 5)")
    print("=" * 60)
    print(f"\n输入文件: {len(args.review_files)} 个")
    print(f"输出路径: {args.output}\n")

    # 收集评审
    print("提取评审数据:")
    reviews = collect_reviews(args.review_files)

    if not reviews:
        print("\n错误: 未找到有效评审报告")
        sys.exit(1)

    # 自动检测分组维度
    group_key, dimension_label = detect_group_key(reviews)
    print(f"\n分组维度: {dimension_label}（分组键: {group_key}）")

    # 计算统计量
    print(f"\n计算统计量:")
    stats = compute_stats(reviews, group_key)

    for group_value, s in stats.items():
        print(f"  {group_value}: 综合={s['means'].get('overall', '?')}, "
              f"一致性={s['agreement_rate']}")

    # 生成对照矩阵
    output_dir = Path(args.output).parent
    output_dir.mkdir(parents=True, exist_ok=True)
    generate_matrix(stats, args.output, dimension_label)

    # 汇总
    print(f"\n{'=' * 60}")
    print("归集完成")
    print(f"{'=' * 60}")
    print(f"  评审报告数: {len(reviews)}")
    print(f"  {dimension_label}数: {len(stats)}")
    print(f"  对照矩阵: {args.output}")
    print(f"\n下一步:")
    print(f"  1. 人工验证对照矩阵数据")
    print(f"  2. 由非实验参与者（MiniMax-M3）撰写 REPORT.md")


if __name__ == "__main__":
    main()
