---
forest: frs
tree: kg-reasoning
branch: kg-llm-fusion
leaf_id: frs-kg-llm-002
title: PoG多跳路径融合方法
type: method
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
source: "[frs_source] §2.1 | Tan et al., arXiv:2410.14211, 2024 [2]"
refs:
  - "[frs-kg-llm-001] LLM与KG互补关系 | PoG是互补关系的具体实现"
  - "[frs-kg-llm-003] ToG交互式推理 | PoG在GPT-3.5-Turbo上超越ToG+GPT-4"
---

# Paths-over-Graph (PoG) 多跳路径融合方法

## 方法概述

**Paths-over-Graph (PoG)** 通过整合知识图谱中的多跳推理路径来增强LLM的推理能力 [2]。PoG的核心理念是：将LLM自身的知识与KG的事实知识通过路径融合机制结合，解决多跳推理和多实体问题。

## 三阶段架构

1. **动态多跳路径探索**：在KG中识别从源实体到目标答案的多条候选推理路径
2. **路径融合**：将多条路径的信息整合为统一的推理上下文
3. **增强LLM推理**：将融合后的路径信息注入LLM推理过程

## 关键性能指标

| 基线 | 对比方法 | 准确率提升 |
|------|---------|:---:|
| GPT-3.5-Turbo + PoG | vs ToG (此前SOTA) | **+18.9%** 平均提升 |
| GPT-3.5-Turbo + PoG | vs GPT-4 + ToG | **+23.9%** |

> 关键发现：PoG使得使用较弱基础模型（GPT-3.5-Turbo）的配置超越了使用最强模型（GPT-4）的基线方法。

## 局限

- 路径质量依赖预提取的完整性
- KG质量直接影响多跳路径的可用性
- 对KG的大小和连接度有一定要求
