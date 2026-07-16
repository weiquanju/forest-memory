---
forest: agent-memory-survey
tree: t2-memory-implementation
branch: b1-sources
title: 记忆来源——试内信息与跨试信息
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
source: "[arXiv:2404.13501] Section 5.1.1-5.1.2"
refs:
  - "[t1-b1] 狭义/广义定义 | 试内→狭义、跨试→广义的直接映射"
  - "[t1-b2] 自我进化视角 | 跨试信息是经验积累的核心载体"
---

# 记忆来源——试内信息与跨试信息

## 分类框架

论文将记忆来源分为三类：
1. **Inside-trial Information**（动态，交互循环内）：同一 trial 内的历史步骤
2. **Cross-trial Information**（动态，交互循环内）：跨不同 trial 的信息积累
3. **External Knowledge**（静态，交互循环外）：Agent-Environment 交互之外的知识

## Inside-trial Information（试内信息）

**定位**：最直接、最相关的信号源。几乎所有已有工作都将其作为记忆的一部分。

### 代表性研究

| 模型 | 试内信息来源 | 记忆形式 |
|------|------------|---------|
| Generative Agents [83] | 为达成目标的日常行为历史 | 自然语言事件记录 |
| MemoChat [94] | 对话会话中的对话历史 | 按主题分段的摘要+检索 |
| TiM [97] | 完成任务后的多个自我生成思考 | 实体关系结构化数据库 |
| Voyager [99] | Minecraft 中基础动作的可执行代码 | 技能库（代码记忆） |

### 关键讨论

- **优势**：与当前任务高度相关，是最直观的记忆源
- **局限**：仅依赖试内信息阻止了 Agent 从多样任务中积累可泛化知识
- **上下文信息**：试内信息不仅包括 Agent-Environment 交互，还包括交互的时空上下文

## Cross-trial Information（跨试信息）

**定位**：Agent 在环境中多次尝试后积累的成功/失败经验，相当于"长期记忆"。

### 代表性研究

| 模型 | 跨试信息策略 | 关键机制 |
|------|------------|---------|
| Reflexion [5] | 语言形式的过往 trial 经验 | Verbal Reinforcement Learning |
| Retroformer [103] | Fine-tune reflection model | 更有效地提取跨试信息 |
| Synapse [91] | 成功 exemplar 作为参考 | 计算机控制任务中的轨迹记忆 |
| ExpeL [82] | 完整轨迹存储+相似轨迹召回 | 成功vs失败对比 → 识别成功模式 |

### 关键讨论

- **经验学习循环**：Agent 基于跨试记忆调整行动→获得反馈→更新记忆→指导未来行动
- **长短期类比**：试内记忆=短期记忆，跨试记忆=长期记忆
- **局限**：仍需 Agent 亲自参与交互，外部经验和知识未被纳入

## 对比总结

| 维度 | Inside-trial | Cross-trial |
|------|-------------|-------------|
| 时间范围 | 单个 trial 内 | 跨多个 trial |
| 信息新鲜度 | 高 | 中-低 |
| 泛化能力 | 低（任务特定） | 高（跨任务模式） |
| 类比 | 短期记忆 | 长期记忆 |
| 代表机制 | 上下文拼接 | 反思/轨迹对比 |
