---
forest: frs
tree: 推理评估
branch: 基准演进
title: 推理基准演进与Agent记忆专项基准
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
description: 从GSM8K/MATH到MemBench/MemoryAgentBench/MemoryArena——Agent记忆专项基准的涌现标志着评估范式从静态单轮到动态多轮转型
keywords:
  - 推理基准
  - Agent记忆基准
  - MemBench
  - MemoryArena
  - 动态评估
atom_type: semantic
status: draft
refs:
  - "[frs] 终身学习Agent评估基准LifelongAgentBench | 同一评估范式演进趋势"
---

# 推理基准演进与Agent记忆专项基准

## 基准演进阶段

| 阶段 | 基准 | 特点 |
|------|------|------|
| 早期 | GSM8K, MATH | 数学应用题 |
| 发展 | AIME, AMC | 高难度数学 |
| 扩展 | 多领域专用 | 逻辑推理/常识/多跳问答 |
| 前沿 | MemBench等 | 多会话，记忆与决策交织 |

## 前沿Agent记忆基准

- **MemBench**[50]：同时覆盖参与/观察两种场景、事实/反思两种层次
- **MemoryAgentBench**[51]：增量多轮交互，评估准确检索/测试时学习/长程理解/选择性遗忘
- **MemoryArena**[52]：多会话Memory-Agent-Environment循环统一评估
