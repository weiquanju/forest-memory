---
forest: mi
tree: knowledge-reasoning
branch: graphrag
title: GraphRAG范式
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
description: 图增强检索生成的核心范式及T-GRAG/CS-RAG/RTSoG等前沿方法
keywords:
  - GraphRAG
  - 图增强检索
  - 多跳推理
  - 混合检索
  - RRF
  - 知识时态性
atom_type: semantic
status: draft
refs:
  - "[mi] 知识图谱与LLM融合 | GraphRAG作为KG融合的最新发展"
  - "[mi] 推理基准演进 | 动态Agent评估是GraphRAG的关键测试场景"
---

# GraphRAG范式

GraphRAG利用图结构进行多跳推理和结构化检索，与Baseline RAG在检索机制上有本质不同。

**实用级GraphRAG**（Min et al.）：解决企业环境两大瓶颈——(1) 依赖解析实现高效KG构建，达到LLM级别性能的94%同时大幅降低成本；(2) 混合检索策略通过RRF融合向量相似度与图遍历，为实体/文档块/关系维护独立嵌入，实现多粒度匹配。在企业数据集上相较纯向量检索基线提升最高15%。

**T-GRAG**（Temporal GraphRAG）：考虑知识的时态动态性，通过时态KG生成器、时态查询分解、三层交互式检索器解决传统GraphRAG忽视知识时间演化的问题。

**CS-RAG**：处理KG不完美问题——通过原子约束规划和充分性检查缓解伪噪声（检索漂移）和不完整信息（检索幻觉），在KG受控噪声注入时保持稳定性能。

**RTSoG**（Reward-Guided Tree Search on Graph）：将MCTS引入KGQA，通过自批评MCTS在奖励模型引导下检索加权推理路径，在GrailQA上相较SOTA提升8.7%。
