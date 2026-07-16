---
forest: frs
tree: 知识图谱推理
branch: GraphRAG
title: 实用级GraphRAG混合检索
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
description: Min等（2025）提出企业级GraphRAG——依赖解析实现LLM级别94%性能的低成本KG构建，RRF融合向量与图遍历实现多粒度匹配
keywords:
  - 实用级GraphRAG
  - 依赖解析
  - RRF融合
  - 多粒度匹配
  - 企业部署
atom_type: semantic
status: draft
refs:
  - "[frs] GraphRAG多跳检索范式 | 实用级方案作为GraphRAG的工程化实现"
---

# 实用级GraphRAG混合检索

## 两个核心瓶颈解决方案

1. **高效KG构建**：利用依赖解析（dependency parsing）达到 LLM 级别性能的 94%（61.87% vs 65.83%），大幅降低成本
2. **混合检索策略**：通过 Reciprocal Rank Fusion（RRF）融合向量相似度与图遍历，为实体、文档块和关系分别维护独立嵌入向量

## 效果

在两个企业数据集上，相较纯向量检索基线提升最高 15%（Min et al., 2025, arXiv:2507.03226）。
