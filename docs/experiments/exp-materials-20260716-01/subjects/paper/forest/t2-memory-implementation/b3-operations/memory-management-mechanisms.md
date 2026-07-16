---
forest: agent-memory-survey
tree: t2-memory-implementation
branch: b3-operations
title: 记忆管理机制
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
source: "[arXiv:2404.13501] Section 5.3.2"
refs:
  - "[t1-b1] W/P/R统一模型 | 管理操作P的工程实现"
  - "[t1-b2] 认知心理学基础 | 管理操作受人类记忆机制启发"
  - "[t5-b2] 终身学习 | 管理操作是终身学习的关键挑战"
---

# 记忆管理机制

## 三元操作框架

记忆管理（Memory Management）由三个子操作组成，灵感来源于人类大脑的记忆工作机制：

| 操作 | 目标 | 人类类比 |
|------|------|---------|
| **Merging（合并）** | 合并冗余记忆条目，减少重复 | 人类将相似经历整合为概括性记忆 |
| **Reflection（反思）** | 从累积事件中生成更高层抽象 | 人类对经历的反思和总结 |
| **Forgetting（遗忘）** | 移除不重要或无关的信息 | 人类自然遗忘不重要的信息 |

形式化：`M^k_t = P(M^k_{t-1}, m^k_t)`

## 代表性实现

### Merging（合并）

| 模型 | 合并策略 |
|------|---------|
| MemoryBank [6] | 对话→每日高层摘要→长期人格洞察提炼 |
| GITM [93] | 多个 plan 中的关键 action 被总结为标准参考 plan |

### Reflection（反思）

| 模型 | 反思策略 | 触发条件 |
|------|---------|---------|
| Generative Agents [83] | 从累积事件生成抽象思考 | 当累积事件足够多时激活 |
| Voyager [99] | 基于环境反馈精炼记忆 | 任务完成后 |
| ChatDev [1] | 多 Agent 角色记忆中的对话反思 | 持续 |
| S3 [2] | 社交网络模拟中的记忆更新 | 持续 |

### Forgetting（遗忘）

| 模型 | 遗忘策略 |
|------|---------|
| MemoryBank [6] | 通过持续评估自然淘汰不重要信息 |
| TiM [97] | 相似内容分组合并，隐式遗忘冗余 |
| Agent 知识编辑 [137] | 通过 Knowledge Editing 改变"不良记忆"，可视为一种遗忘机制 |

## 管理操作对比（Table 3 摘要）

| 模型 | Merging | Reflection | Forgetting |
|------|:---:|:---:|:---:|
| MemoryBank [6] | ✓ | ✓ | ✓ |
| Generative Agents [83] | ✓ | ✓ | ✓ |
| RecAgent [95] | ✓ | ✓ | ✓ |
| S3 [2] | ✓ | ✓ | ✓ |
| Voyager [99] | × | ✓ | × |
| MemGPT [100] | × | ✓ | × |
| RET-LLM [7] | × | × | × |

> 注：大多数模型的 Forgetting 列为 ×，说明遗忘机制是当前研究中最被忽视的操作。

## 关键讨论

- 大多数管理操作受**人脑工作机制启发**，利用 LLM 模拟人类思维的能力
- **遗忘是被最忽视的操作**——Table 3 中仅 3 个模型（MemoryBank/Generative Agents/RecAgent）明确实现了遗忘，这与人类记忆的核心特征（Ebbinghaus 遗忘曲线）形成对比
- 管理操作的**LLM 自主性**是一个重要趋势：不设计手工规则，而是让 Agent 自主判断何时合并/反思/遗忘
