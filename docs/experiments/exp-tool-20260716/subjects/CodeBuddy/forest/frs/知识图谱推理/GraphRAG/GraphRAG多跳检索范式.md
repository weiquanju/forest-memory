---
forest: frs
tree: 知识图谱推理
branch: GraphRAG
title: GraphRAG多跳检索范式
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
description: GraphRAG将知识图谱与RAG深度融合，利用图结构进行多跳推理和结构化检索，解决传统向量RAG无法回答的跨实体复杂查询
keywords:
  - GraphRAG
  - 图增强检索
  - 多跳推理
  - 结构化检索
  - 混合检索
atom_type: semantic
status: draft
refs:
  - "[frs] 知识图谱与大模型融合概述 | GraphRAG作为KG增强推理的前沿范式"
---

# GraphRAG多跳检索范式

## 核心定位

GraphRAG（Edge et al., 2024, arXiv:2404.16130）将知识图谱与 RAG 深度融合。与基于向量相似度的 Baseline RAG 不同，GraphRAG 利用图结构进行多跳推理和结构化检索，能回答需要跨越多个实体和关系的复杂查询。

## 关键进展

| 方法 | 创新点 | 适用场景 |
|------|--------|---------|
| 实用级GraphRAG [6] | 依赖解析高效KG构建+RRF混合检索 | 企业环境 |
| T-GRAG [7] | 时态KG+三层交互检索器 | 时态问答 |
| CS-RAG [8] | 原子约束规划+充分性检查 | 不完美KG |
| RTSoG [9] | MCTS+奖励模型引导的KGQA | 复杂KGQA |
