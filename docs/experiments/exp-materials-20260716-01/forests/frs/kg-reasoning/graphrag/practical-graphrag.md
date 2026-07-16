---
forest: frs
tree: kg-reasoning
branch: graphrag
leaf_id: frs-graphrag-002
title: 实用级GraphRAG框架
type: method
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
source: "[frs_source] §2.2 | Min et al., arXiv:2507.03226, 2025 [6]"
refs:
  - "[frs-graphrag-001] GraphRAG范式 | 实用级框架解决企业部署的核心瓶颈"
---

# 实用级GraphRAG框架

## 核心贡献

Min等人提出的实用级GraphRAG框架解决了GraphRAG在企业环境中的**两个核心瓶颈** [6]：

### 瓶颈1：高效KG构建

- 利用**依赖解析（dependency parsing）** 替代LLM进行KG构建
- 达到LLM级别性能的**94%**（61.87% vs 65.83%）
- **大幅降低成本**——无需为每个文档调用昂贵的LLM

### 瓶颈2：混合检索策略

通过**Reciprocal Rank Fusion (RRF)** 融合多种信号：

| 检索维度 | 索引类型 | 作用 |
|---------|---------|------|
| 实体 | 独立嵌入向量 | 实体级匹配 |
| 文档块 | 独立嵌入向量 | 内容级匹配 |
| 关系 | 独立嵌入向量 | 关系级匹配 |

这种**多粒度匹配**在两个企业数据集上相较纯向量检索基线提升最高**15%** [6]。

## 关键意义

这是首个在**成本可控**前提下落地GraphRAG的实用方案，证明GraphRAG从学术概念走向企业部署是可行的。
