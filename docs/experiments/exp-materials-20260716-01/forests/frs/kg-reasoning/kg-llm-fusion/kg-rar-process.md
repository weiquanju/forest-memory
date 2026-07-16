---
forest: frs
tree: kg-reasoning
branch: kg-llm-fusion
leaf_id: frs-kg-llm-005
title: KG-RAR过程导向图增强推理
type: method
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
source: "[frs_source] §2.1 | Wu et al., arXiv:2503.01642, 2025 [1]"
refs:
  - "[frs-kg-llm-001] LLM与KG互补关系 | KG-RAR通过过程级KG和奖励模型增强互补效果"
---

# KG-RAR 过程导向图增强推理框架

## 方法概述

**KG-RAR (Graph-Augmented Reasoning)** 通过三个核心机制优化KG增强推理 [1]：

1. **过程导向KG构建**：不仅存储事实，还构建推理过程的图表示
2. **分层检索策略**：按粒度和相关性分层检索知识
3. **后处理与奖励模型 (PRP-RM)**：对候选推理路径进行质量评分和精炼

## 性能指标

| 配置 | 基准 | 相对提升 |
|------|------|:---:|
| Llama-3B + KG-RAR | Math500 | **+20.73%** |
| Llama-3B + KG-RAR | GSM8K | **+20.73%** |

## 独特之处

- **PRP-RM** 提示轻量微调可显著提升下游任务——在"无需训练是主流"的趋势中提供了不同思路
- 过程级KG构建增加了知识表示的丰富度，但也带来了额外成本

## 局限

- 过程级KG构建成本尚未系统评估
- PRP-RM的跨领域迁移效果未知
