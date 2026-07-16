---
forest: frs
tree: kg-reasoning
branch: path-optimization
leaf_id: frs-path-004
title: SoG上下文感知图导航推理
type: method
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
source: "[frs_source] §2.3 | Sun et al., arXiv:2510.08825, 2025 [14]"
refs:
  - "[frs-kg-llm-003] ToG交互式推理 | SoG在ToG的交互基础上提出observe-think-navigate范式"
---

# SoG 上下文感知图导航推理

## 方法概述

**Search-on-Graph (SoG)** 遵循 **observe-think-navigate** 范式 [14]，让LLM在每一步完全自主地决策：观察当前环境、推理最佳路径、导航至下一节点。

## 三步循环

```
┌──────────────┐
│   Observe    │  观察当前实体的关系连接
│   Think      │  推理哪条路径最佳
│   Navigate   │  导航至下一实体
└──────┬───────┘
       │ 循环
       ▼
```

## 关键特性

| 特性 | 说明 |
|------|------|
| 纯LLM驱动 | 无需独立的路径选择模块 |
| 上下文感知 | 每一步决策基于当前已探索的上下文 |
| 端到端可追溯 | 导航路径即为推理路径 |

## 与ToG的关系

SoG是ToG交互式推理的自然演进——从beam search变为逐步上下文感知导航，对LLM自身推理能力要求更高。
