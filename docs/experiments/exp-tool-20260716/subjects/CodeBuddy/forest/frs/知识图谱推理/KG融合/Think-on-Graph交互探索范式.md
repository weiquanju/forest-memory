---
forest: frs
tree: 知识图谱推理
branch: KG融合
title: Think-on-Graph交互探索范式
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
description: ToG将LLM作为Agent在KG上通过beam search交互式探索实体和关系——首次实现推理路径每步可追溯至KG具体事实三元组
keywords:
  - Think-on-Graph
  - ToG
  - beam search
  - 知识可追溯性
  - LLM⊗KG
atom_type: semantic
status: draft
---

# Think-on-Graph交互探索范式

## 核心创新

ToG（Sun et al., 2023, arXiv:2307.07697）提出"LLM⊗KG"深度整合范式：LLM 作为 Agent 在 KG 上通过 beam search 交互式探索相关实体和关系，发现最有前景的推理路径。

## 关键贡献

证明**知识可追溯性**（knowledge traceability）——推理路径中的每一步都可追溯到 KG 中的具体事实三元组。人类专家可检查推理链中的每一步并提供反馈纠正错误，实现"人在回路中"的推理透明度。
