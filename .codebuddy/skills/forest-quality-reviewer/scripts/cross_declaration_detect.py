#!/usr/bin/env python3
"""
交叉声明量化检测脚本 (P1-4)
基于 sentence-transformers 计算森林叶子间的语义相似度，识别潜在交叉声明。

用法:
    python cross_declaration_detect.py <forest_dir> [--threshold 0.80]

输出:
    - 相似度矩阵统计
    - 高相似度对清单 (> threshold)
    - 每个森林的 D3 单一职责量化评估
"""

import os
import sys
import re
import argparse
import yaml
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer


def extract_leaf_text(md_path: str) -> dict:
    """从 markdown 叶子文件提取 title + description + 正文首段作为嵌入文本。"""
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 分离 YAML frontmatter 和正文
    frontmatter = {}
    body = content
    fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)", content, re.DOTALL)
    if fm_match:
        try:
            frontmatter = yaml.safe_load(fm_match.group(1)) or {}
        except yaml.YAMLError:
            frontmatter = {}
        body = fm_match.group(2)

    title = frontmatter.get("title", Path(md_path).stem)
    description = frontmatter.get("description", "")
    leaf_id = frontmatter.get("leaf", Path(md_path).stem)
    tree = frontmatter.get("tree", "")
    branch = frontmatter.get("branch", "")

    # 提取正文首段（跳过标题行和空行）
    first_para = ""
    lines = body.strip().split("\n")
    para_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        if stripped == "":
            if para_lines:
                break
            continue
        para_lines.append(stripped)
    first_para = " ".join(para_lines)

    # 组合文本：title + description + 首段
    text_parts = [str(title)]
    if description:
        text_parts.append(str(description))
    if first_para:
        text_parts.append(first_para[:500])  # 限制首段长度

    return {
        "path": md_path,
        "leaf_id": leaf_id,
        "tree": tree,
        "branch": branch,
        "title": title,
        "text": " ".join(text_parts),
    }


def collect_leaves(forest_dir: str) -> list:
    """收集森林中所有叶子文件（排除 index.md）。"""
    forest_path = Path(forest_dir)
    leaves = []
    for md_file in sorted(forest_path.rglob("*.md")):
        if md_file.name == "index.md":
            continue
        if md_file.name.startswith("correction-log") or md_file.name.startswith("quality-gate"):
            continue
        leaf_info = extract_leaf_text(str(md_file))
        if leaf_info["text"].strip():
            leaves.append(leaf_info)
    return leaves


def compute_similarity(leaves: list, model: SentenceTransformer) -> np.ndarray:
    """计算所有叶子文本间的余弦相似度矩阵。"""
    texts = [leaf["text"] for leaf in leaves]
    embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
    # 归一化后点积 = 余弦相似度
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    norms[norms == 0] = 1
    normalized = embeddings / norms
    sim_matrix = normalized @ normalized.T
    return sim_matrix


def analyze_forest(forest_dir: str, threshold: float, model: SentenceTransformer) -> dict:
    """分析单个森林的交叉声明。"""
    forest_name = Path(forest_dir).name
    leaves = collect_leaves(forest_dir)

    if len(leaves) < 2:
        return {"forest": forest_name, "error": "叶子数不足"}

    sim_matrix = compute_similarity(leaves, model)

    # 收集高相似度对（排除自身对角线和重复对）
    high_pairs = []
    for i in range(len(leaves)):
        for j in range(i + 1, len(leaves)):
            sim = sim_matrix[i][j]
            if sim >= threshold:
                high_pairs.append({
                    "leaf_a": leaves[i]["leaf_id"],
                    "leaf_b": leaves[j]["leaf_id"],
                    "tree_a": leaves[i]["tree"],
                    "tree_b": leaves[j]["tree"],
                    "title_a": leaves[i]["title"],
                    "title_b": leaves[j]["title"],
                    "similarity": round(float(sim), 4),
                })

    # 统计
    upper_tri = sim_matrix[np.triu_indices_from(sim_matrix, k=1)]
    stats = {
        "forest": forest_name,
        "leaf_count": len(leaves),
        "threshold": threshold,
        "max_similarity": round(float(upper_tri.max()), 4),
        "mean_similarity": round(float(upper_tri.mean()), 4),
        "pairs_above_threshold": len(high_pairs),
        "pairs_085_plus": int((upper_tri >= 0.85).sum()),
        "pairs_080_085": int(((upper_tri >= 0.80) & (upper_tri < 0.85)).sum()),
        "pairs_070_080": int(((upper_tri >= 0.70) & (upper_tri < 0.80)).sum()),
        "pairs_below_070": int((upper_tri < 0.70).sum()),
        "high_pairs": sorted(high_pairs, key=lambda x: -x["similarity"]),
    }

    # 最高相似度 Top 5（无论是否超阈值）
    top5 = []
    pair_sims = []
    for i in range(len(leaves)):
        for j in range(i + 1, len(leaves)):
            pair_sims.append((sim_matrix[i][j], leaves[i], leaves[j]))
    pair_sims.sort(key=lambda x: -x[0])
    for sim, la, lb in pair_sims[:5]:
        top5.append({
            "leaf_a": la["leaf_id"],
            "leaf_b": lb["leaf_id"],
            "title_a": la["title"],
            "title_b": lb["title"],
            "similarity": round(float(sim), 4),
        })
    stats["top5_pairs"] = top5

    return stats


def main():
    parser = argparse.ArgumentParser(description="交叉声明量化检测 (P1-4)")
    parser.add_argument("forest_dirs", nargs="+", help="森林目录路径（可多个）")
    parser.add_argument("--threshold", type=float, default=0.80, help="相似度阈值（默认 0.80）")
    parser.add_argument("--model", default="paraphrase-multilingual-MiniLM-L12-v2", help="嵌入模型")
    args = parser.parse_args()

    print(f"加载模型: {args.model}")
    model = SentenceTransformer(args.model)

    all_stats = []
    for forest_dir in args.forest_dirs:
        print(f"\n{'='*60}")
        print(f"分析森林: {forest_dir}")
        print(f"{'='*60}")
        stats = analyze_forest(forest_dir, args.threshold, model)
        all_stats.append(stats)

        if "error" in stats:
            print(f"  错误: {stats['error']}")
            continue

        print(f"  叶子数: {stats['leaf_count']}")
        print(f"  最大相似度: {stats['max_similarity']}")
        print(f"  平均相似度: {stats['mean_similarity']}")
        print(f"  > 0.85 (交叉声明): {stats['pairs_085_plus']} 对")
        print(f"  0.80-0.85 (需审查): {stats['pairs_080_085']} 对")
        print(f"  0.70-0.80 (语义关联): {stats['pairs_070_080']} 对")
        print(f"  < 0.70 (独立主题): {stats['pairs_below_070']} 对")
        print(f"  超阈值对数 (>={args.threshold}): {stats['pairs_above_threshold']}")

        if stats["high_pairs"]:
            print(f"\n  高相似度对清单:")
            for p in stats["high_pairs"]:
                print(f"    [{p['similarity']}] {p['leaf_a']} <-> {p['leaf_b']}")
                print(f"           {p['title_a']}  <->  {p['title_b']}")

        print(f"\n  Top 5 相似度对:")
        for p in stats["top5_pairs"]:
            print(f"    [{p['similarity']}] {p['leaf_a']} <-> {p['leaf_b']}")

    # 汇总
    print(f"\n{'='*60}")
    print("汇总")
    print(f"{'='*60}")
    print(f"{'森林':<20} {'叶子数':<8} {'最大相似':<10} {'>0.85':<8} {'0.80-0.85':<10} {'超阈值':<8}")
    for s in all_stats:
        if "error" in s:
            print(f"{s['forest']:<20} ERROR")
            continue
        print(f"{s['forest']:<20} {s['leaf_count']:<8} {s['max_similarity']:<10} "
              f"{s['pairs_085_plus']:<8} {s['pairs_080_085']:<10} {s['pairs_above_threshold']:<8}")


if __name__ == "__main__":
    main()
