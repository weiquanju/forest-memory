---
forest: frs
tree: kg-reasoning
branch: kg-llm-fusion
leaf_id: frs-kg-llm-004
title: KG-Agent自主推理框架
type: method
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
source: "[frs_source] §2.1 | Jiang et al., arXiv:2402.11163, 2024 [4]"
refs:
  - "[frs-kg-llm-003] ToG交互式推理 | KG-Agent在微调极小模型方向上另辟蹊径"
---

# KG-Agent 自主推理框架

## 方法概述

**KG-Agent** 提出了一种自主LLM Agent框架 [4]，通过集成多功能工具箱、KG执行器和知识记忆，仅用**10K样本**微调LLaMA-7B即可在KGQA任务上超越使用更大模型的SOTA方法。

## 架构组件

| 组件 | 功能 |
|------|------|
| 多功能工具箱 | 提供关系查询、实体搜索、路径遍历等原子操作 |
| KG执行器 | 在KG上执行Agent的规划动作 |
| 知识记忆 | 存储已探索的路径和已验证的事实 |

## 核心发现

> 10K样本微调的LLaMA-7B超越使用更大模型的SOTA方法。

这表明：**精心设计的Agent框架 + 小模型微调**可以在KGQA任务上达到甚至超越更大泛用模型的性能，为轻量级KG推理系统提供了可行路径。

## 局限

- 需要针对特定KG领域的微调数据
- 10K样本的领域迁移效果未经验证
