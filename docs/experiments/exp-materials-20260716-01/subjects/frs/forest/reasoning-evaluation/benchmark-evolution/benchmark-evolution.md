---
forest: frs
tree: reasoning-evaluation
branch: benchmark-evolution
leaf_id: frs-eval-bench-001
title: 推理基准的演进路径
type: concept
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
source: "[frs_source] §5.1 | GSM8K [48], MATH [49], MemBench [50]"
refs:
  - "[frs-eval-dynamic-001] 动态Agent评估 | 从静态到动态是基准演进的核心趋势"
---

# 推理基准的演进路径

## 四阶段演进

| 阶段 | 代表基准 | 特点 | 挑战 |
|------|---------|------|------|
| **早期** | GSM8K [48]、MATH [49] | 小学数学应用题、数学竞赛题 | 已被大多数模型接近饱和 |
| **发展** | AIME、AMC | 更高难度数学题集 | 难度上限有限 |
| **扩展** | 多领域专用基准 | 逻辑推理、常识推理、多跳问答 | 碎片化 |
| **前沿** | MemBench [50]、MemoryAgentBench [51]、MemoryArena [52] | 多会话任务，记忆与决策交织 | 评估成本高、复现门槛高 |

## 两大结构性问题

1. **数据污染（Data Contamination）**：部分测试数据可能已出现在训练语料中，导致虚高表现
2. **静态单轮局限**：传统基准无法评估模型在动态多轮环境中的推理和决策能力
