---
forest: memory-systems-ai
tree: t3-knowledge-reasoning
branch: b1-graphrag
leaf: l1-graphrag-multihop
title: GraphRAG：图增强检索与多跳推理
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
model: DeepSeek V4 Flash
source: "input/frs_source/AI与大模型在知识领域、Agent记忆、推理数据及推理关系中的前沿研究综述.md"
refs:
  - "Edge et al. (arXiv:2404.16130) — GraphRAG学术论文，取代博客版"
  - "ToG（Think-on-Graph）— 基于知识图谱的多跳推理路径优化"
  - "PoG（Path-of-Graph）— 图路径推理增强"
  - "GraphRAG实现从'检索片段'到'检索结构化知识'的范式转变"
---

# GraphRAG：图增强检索与多跳推理

GraphRAG（Graph-enhanced Retrieval-Augmented Generation）实现了从"检索片段"到"检索结构化知识"的范式转变。传统RAG检索扁平文本块，GraphRAG则利用知识图谱的结构化关系进行多跳推理，使模型能够沿着实体关系的路径深入探查，获取更深层的知识关联。核心方法包括**ToG（Think-on-Graph）**和**PoG（Path-of-Graph）**等，通过在图结构上执行多步推理来优化检索路径，提升复杂问题回答的准确性和可解释性。
