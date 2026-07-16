---
forest: agent-memory-survey
tree: t1-memory-foundations
branch: b1-definitions
title: Agent记忆的狭义与广义定义
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
source: "[arXiv:2404.13501] Section 3.1-3.4"
refs:
  - "[t1-b2] 认知心理学基础 | 定义受人类记忆理论启发"
  - "[t2-b1] 记忆来源分类 | 狭义/广义定义直接映射到试内/跨试/外部知识三类来源"
---

# Agent记忆的狭义与广义定义

## 背景概念

论文首先定义了四个基础概念，构成 Agent-Environment 交互的完整建模：

| 概念 | 定义 | 粒度 |
|------|------|------|
| **Task (T)** | Agent 需要达成的最终目标（如为 Alice 预订机票） | 最粗 |
| **Environment (E)** | Agent 需要交互以完成任务的对象（狭义：用户反馈；广义：所有上下文因素） | — |
| **Trial (ξ)** | Agent 完成一次任务的完整交互过程 | 中 |
| **Step** | 一次交互回合：Agent action (a_t) → Environment observation (o_t) | 最细 |

形式化表示：长度为 T 的 trial 记为 `ξ_T = {a_1, o_1, a_2, o_2, ..., o_T, a_T}`

## 狭义定义（Narrow Definition）

**核心**：记忆仅包含**同一 trial 内**的历史信息。

形式化：对任务在第 t 步之前，记忆来源于 `ξ_t = {a_1, o_1, ..., a_{t-1}, o_{t-1}}`。

**实例**（Toy Example 任务A）：Agent 在 Step 3 需要为 Alice 安排游览顺序，此时记忆包含 Step 1 的航班安排和 Step 2 的景点决策。记忆范围限定在当前 trip-planning 任务内，不跨任务共享。

**局限**：仅依赖试内信息使 Agent 无法从不同任务中积累可泛化知识。

## 广义定义（Broad Definition）

**核心**：记忆来源于三个维度——(1) 同 trial 内的历史信息，(2) 跨 trial 的历史信息，(3) 外部知识。

形式化表示：对于任务序列 `{T_1, T_2, ..., T_K}`，任务 T_k 在步骤 t 的记忆基于 `(ξ^k_t, Ξ^k, D^k_t)`：
- `ξ^k_t`：同一 trial 内的历史（试内信息）
- `Ξ^k = {ξ^1, ξ^2, ..., ξ^{k-1}, ξ^{k'}}`：所有历史任务的 trial + 当前任务的其他尝试（跨试信息）
- `D^k_t`：外部知识源

**实例**：
- 跨试信息：任务A 中 Alice 的负面反馈被记录，在后续任务中避免类似错误
- 跨任务信息：任务B 中推荐与任务A 中游览景点相关的电影，捕捉用户近期偏好
- 外部知识：Agent 查阅旅游杂志获取北京景点信息

## 学术张力

- **Consistency vs Generality**：狭义记忆确保当前任务一致性，但缺乏泛化能力；广义记忆支持知识迁移，但增加了信息筛选和管理复杂度
- **Source Scope**：三源模型（ξ^k_t, Ξ^k, D^k_t）是通用形式化框架，但实际系统中三者的权重分配尚无统一标准——Reflexion [5] 强调跨试反思，而大多数对话Agent（如 MemoChat [94]）主要依赖试内信息
- **Privacy Boundary**：外部知识源 D^k_t 的引入扩展了 Agent 的能力边界，但同时带来数据安全与合规风险 [18]
