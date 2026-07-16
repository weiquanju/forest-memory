---
forest: frs
tree: reasoning-evaluation
branch: dynamic-evaluation
leaf_id: frs-eval-dynamic-001
title: 动态Agent评估三大范式
type: concept
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
source: "[frs_source] §5.2 | Scheherazade [55], MemBench [50], MemoryAgentBench [51], MemoryArena [52]"
---

# 动态Agent评估三大范式

## 趋势一：组合式基准

**Scheherazade** [55] 将多个现有基准"链式"连接，生成更复杂、更长的推理链，评估模型处理长链条件推理时的表现。

## 趋势二：过程导向评估

不仅看最终答案正确性，还关注推理过程本身：
- **可重用性**：推理步骤是否可被其他模型理解并复用
- **可验证性**：推理步骤是否可被独立验证

## 趋势三：智能体基准

| 基准 | 核心特点 |
|------|---------|
| **MemBench [50]** | 首个同时覆盖参与/观察两种场景、事实/反思两种记忆层次的综合基准 |
| **MemoryAgentBench [51]** | 基于增量多轮交互，评估准确检索、测试时学习、长程理解、选择性遗忘四能力 |
| **MemoryArena [52]** | 多会话Memory-Agent-Environment循环中的统一评估场 |
| **LifelongAgentBench [19]** | 首个系统评估LLM Agent终身学习能力，覆盖Database/OS/KG三个环境 |
