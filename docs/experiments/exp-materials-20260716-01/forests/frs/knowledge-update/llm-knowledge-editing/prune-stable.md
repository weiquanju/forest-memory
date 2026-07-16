---
forest: frs
tree: knowledge-update
branch: llm-knowledge-editing
leaf_id: frs-kg-edit-002
title: PRUNE与STABLE顺序模型编辑约束
type: method
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
source: "[frs_source] §7.2 | PRUNE [41], STABLE [42]"
refs:
  - "[frs-kg-edit-001] WilKE | PRUNE从数学角度分析编辑退化的条件数根源"
---

# PRUNE与STABLE顺序模型编辑约束

## PRUNE：扰动约束模型编辑 [41]

### 理论分析

Ma等人从理论上分析：顺序模型编辑中影响通用能力的因素在于被编辑矩阵的**条件数（condition number）**。随着编辑次数增加：
- 条件数增大
- 对原始知识关联的扰动加剧
- 通用能力持续退化

### PRUNE方案

对条件数施加约束，降低对编辑模型的**扰动上界**，在保持编辑性能的同时有效保留通用能力。

## STABLE：门控持续自编辑 [42]

### 机制

- 利用LoRA进行参数高效微调
- 通过**三种指标**评估每次候选编辑对稳定性预算的影响：

| 指标 | 测量什么 |
|------|---------|
| 精确匹配下降 | 旧知识的正确性是否下降 |
| bits增加 | 编辑引入的信息量是否过大 |
| KL散度 | 编辑前后的输出分布变化 |

- 超过阈值时对LoRA更新进行**裁剪或拒绝**

## 关键观察

PRUNE提供理论保证（扰动上界），STABLE提供工程约束（门控拒绝），两者互补。
