---
forest: frs
tree: 知识图谱推理
branch: KG融合
title: Paths-over-Graph多跳路径融合
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
description: PoG通过三阶段动态多跳路径探索将LLM知识与KG事实融合——在GPT-3.5-Turbo上相较ToG平均准确率提升18.9%
keywords:
  - Paths-over-Graph
  - PoG
  - 多跳推理
  - 路径融合
  - 动态探索
atom_type: semantic
status: draft
refs:
  - "[frs] Think-on-Graph交互探索范式 | PoG作为ToG基线的优化改进"
---

# Paths-over-Graph多跳路径融合

## 三阶段过程

PoG（Tan et al., 2024, arXiv:2410.14211）通过三阶段动态多跳路径探索：路径发现、路径融合、推理增强。将 LLM 自身知识与 KG 事实知识相结合，解决多跳推理和多实体问题。

## 性能表现

- PoG+GPT-3.5-Turbo 相较 SOTA 方法 ToG 平均准确率提升 18.9%
- PoG+GPT-3.5-Turbo 超过 ToG+GPT-4 达 23.9%
