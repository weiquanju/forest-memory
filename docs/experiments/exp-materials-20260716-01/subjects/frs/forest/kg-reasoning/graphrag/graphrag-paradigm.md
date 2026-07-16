---
forest: frs
tree: kg-reasoning
branch: graphrag
leaf_id: frs-graphrag-001
title: GraphRAG范式定义与核心价值
type: concept
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
source: "[frs_source] §2.2 | Edge et al., arXiv:2404.16130, 2024 [5]"
refs:
  - "[frs-kg-llm-001] LLM与KG互补关系 | GraphRAG是LLM-KG互补的工程化实现"
  - "[frs-graphrag-002] 实用级GraphRAG | 解决企业级部署瓶颈"
---

# GraphRAG 范式定义与核心价值

## 范式定义

**GraphRAG (Graph Retrieval-Augmented Generation)** 是将知识图谱与RAG深度融合的前沿范式。与传统基于向量相似度的 Baseline RAG 不同，GraphRAG利用图结构进行**多跳推理**和结构化检索，能够回答需要跨越多个实体和关系的复杂查询 [5]。

## GraphRAG vs Baseline RAG

| 维度 | Baseline RAG | GraphRAG |
|------|-------------|----------|
| 检索方式 | 向量相似度单跳 | 图结构多跳遍历 |
| 知识组织 | 扁平chunk | 图结构（实体-关系） |
| 复杂查询 | 力不从心 | 跨实体关系推理 |
| 可解释性 | 低（黑箱检索） | 高（路径可追溯） |
| 成本 | 低 | 较高 |

## 核心价值

GraphRAG的价值在于使得LLM能够利用**结构化知识图**进行有路径可循的推理，而非仅依赖向量空间的模糊相似性。尤其在需要"以A通过B与C的关系来推断D"这类多跳推理场景中，GraphRAG的优势极其显著。
