---
forest: frs
tree: knowledge-governance
branch: knowledge-traceability
leaf_id: frs-knowledge-trace-001
title: 知识可追溯性与可解释性
type: concept
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
source: "[frs_source] §4.2 | ToG [3], RL-based [27], Hybrid Pipeline [28], Semantic Triples [29], WKGFC [30]"
refs:
  - "[frs-kg-llm-003] ToG交互式推理 | 可追溯性是ToG的核心贡献"
---

# 知识可追溯性与可解释性

## 核心概念

知识的**可追溯性（traceability）**和**可解释性（explainability）**是将AI从"黑箱"推向可信系统的关键。

## 五种溯源方法

| 方法 | 溯源机制 | 人类参与方式 |
|------|---------|------------|
| **ToG [3]** | 推理路径每步回溯至KG三元组 | 人类专家检查并纠正每步推理 |
| **RL可解释核查 [27]** | RL Agent计算证明/反驳路径 | 将路径呈现给人类读者自行判断 |
| **混合管道 [28]** | KG检索→LLM分类→Web回退 | 模块化管道每步结果可查看 |
| **语义三元组 [29]** | 声明分解为三元组+KG增强 | 三元组天然可读 |
| **WKGFC [30]** | 多源多Agent MDP建模 | Agent决策过程可审计 |

## 混合管道最佳实践 [28]

- F1=**0.93** on FEVER
- "KG覆盖不足时自动回退到Web搜索"的降级策略确保鲁棒性
- 模块化开源架构适合部署

## 当前挑战

跨领域泛化时（如从FEVER到Climate-FEVER），性能普遍下降**5-15%**——这是知识溯源在真实场景中落地的核心瓶颈。
