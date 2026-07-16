---
forest: frs
tree: 知识图谱推理
branch: GraphRAG
title: 不完美KG鲁棒检索CS-RAG
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
description: Ma等（2026）通过实证识别KG中伪噪声和不完整信息两类问题模式——原子约束规划与充分性检查在受控噪声下保持稳定性能
keywords:
  - CS-RAG
  - 不完美KG
  - 伪噪声
  - 原子约束规划
  - 鲁棒检索
atom_type: semantic
status: draft
---

# 不完美KG鲁棒检索CS-RAG

## 问题识别

Ma 等人（2026, arXiv:2603.14828）通过实证分析识别两类反复出现的 KG 问题模式：
- **伪噪声**（spurious noise）→ 检索漂移
- **不完整信息**（incomplete information）→ 检索幻觉

## 解决方案

CS-RAG 通过原子约束规划（atomic constraint planning）和充分性检查（sufficiency check）缓解这些问题，在 KG 受控噪声注入时保持稳定性能。

## 意义

CS-RAG 是当前极少数专门处理不完美 KG 的 GraphRAG 方法——这在真实部署场景中是关键能力，因为大多数方法假设 KG 完整且高质量。
