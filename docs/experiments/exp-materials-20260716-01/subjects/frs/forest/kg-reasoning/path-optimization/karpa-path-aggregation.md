---
forest: frs
tree: kg-reasoning
branch: path-optimization
leaf_id: frs-path-002
title: KARPA知识图谱辅助推理路径聚合
type: method
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
source: "[frs_source] §2.3 | Fang et al., arXiv:2412.20995, 2024 [12]"
refs:
  - "[frs-kg-llm-002] PoG多跳路径融合 | KARPA与PoG均聚焦路径融合但采用不同路线"
---

# KARPA 知识图谱辅助推理路径聚合

## 方法概述

**KARPA (Knowledge graph Assisted Reasoning Path Aggregation)** 利用LLM的全局规划能力预规划关系路径，通过嵌入模型匹配语义相关路径，再在匹配到的路径上进行推理 [12]。

## 工作流程

1. **全局路径规划**：LLM先规划需要经过哪些关系类型
2. **语义路径匹配**：嵌入模型在KG中匹配语义最相关的路径
3. **路径推理**：在匹配到的路径上执行推理

## 关键优势

| 优势 | 说明 |
|------|------|
| 无需遍历 | 避免逐步遍历KG的低效 |
| 无需训练 | 可适配多种LLM架构 |
| 语义对齐 | 嵌入匹配确保路径语义相关性 |

## 局限

- LLM规划的关系路径可能与KG实际结构不匹配
- 路径聚合质量依赖嵌入模型的语义理解能力
