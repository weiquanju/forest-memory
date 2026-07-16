---
forest: frs
tree: knowledge-governance
branch: fact-verification
leaf_id: frs-fact-003
title: CommunityKG-RAG社区结构增强检索
type: method
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
source: "[frs_source] §4.1 | Chang & Zhang, arXiv:2408.08535, 2024 [22]"
refs:
  - "[frs-graphrag-001] GraphRAG范式 | CommunityKG-RAG是GraphRAG在事实核查领域的特化"
---

# CommunityKG-RAG 社区结构增强检索

## 方法概述

**CommunityKG-RAG** 将KG中的**社区结构**（community structure）集成到RAG中 [22]，利用KG内社区结构的多跳特性显著提高事实核查中信息检索的准确性和相关性。

## 核心思想

KG中的社区结构（紧密连接的子图）天然编码了领域知识的聚类关系。在事实核查时，利用社区结构可以实现：

1. **相关证据聚类**：同一社区内的信息倾向于共同支持或反驳同一声明
2. **多跳关联发掘**：通过社区间的连接桥发现非直接但相关的证据

## 关键特性

- **无需额外训练**：直接利用已有KG的社区结构
- **领域自适应**：无需训练即可适应新领域和查询类型

## 局限

- 依赖于KG社区检测的质量
- 稀疏KG中社区结构不明显时效果受限
