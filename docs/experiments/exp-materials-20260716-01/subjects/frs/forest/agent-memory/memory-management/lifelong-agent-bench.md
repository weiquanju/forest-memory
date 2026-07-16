---
forest: frs
tree: agent-memory
branch: memory-management
leaf_id: frs-mem-mgmt-004
title: LifelongAgentBench终身学习评估基准
type: benchmark
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
source: "[frs_source] §3.3, §5.2 | Zheng et al., arXiv:2505.11942, 2025 [19]"
refs:
  - "[frs-eval-dynamic-004] 动态Agent评估基准 | LifelongAgentBench是终身学习方向的代表"
---

# LifelongAgentBench 终身学习评估基准

## 定位

**LifelongAgentBench** 是首个系统评估LLM Agent终身学习能力的**统一基准** [19]。

## 评估环境

| 环境 | 任务类型 | 考察能力 |
|------|---------|---------|
| 数据库 | SQL查询、数据操作 | 结构化和程序化推理 |
| 操作系统 | 文件操作、命令执行 | 工具使用和长程规划 |
| 知识图谱 | KG查询和推理 | 结构化知识利用 |

三个交互环境中提供基于技能的任务，覆盖不同类型的Agent能力。

## 关键发现

> 传统经验回放对LLM Agent效果有限，原因是**无关信息**和**上下文长度约束** [19]。

这意味着在LLM Agent的终身学习场景中，不能简单复用深度强化学习中的经验回放策略，需要设计专门的Agent记忆和持续学习机制。
