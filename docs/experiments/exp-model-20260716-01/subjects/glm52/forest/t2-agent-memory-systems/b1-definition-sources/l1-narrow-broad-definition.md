---
forest: memory-systems-ai
tree: t2-agent-memory-systems
branch: b1-definition-sources
leaf: l1-narrow-broad-definition
title: 狭义与广义记忆定义
created: 2026-07-16
model: GLM-5.2
source:
  - "arXiv:2404.13501"
refs:
  - "[t1-b1] 记忆的内容模块化分类 | 人脑记忆分类对Agent记忆定义的启发"
  - "[t2-b1] 三类记忆来源 | 广义定义直接引出三类记忆来源分类"
---

# 狭义与广义记忆定义

## 基本概念框架

Zhang et al.（2024, arXiv:2404.13501）从三个层次定义 Agent 记忆：

| 概念 | 定义 |
|------|------|
| Task | Agent 需要实现的最终目标 |
| Environment | Agent 需交互的对象，或影响决策的上下文因素 |
| Trial | 完成任务的一次完整 Agent-环境交互过程 |
| Step | Trial 中的每一轮交互（Agent 行动 + 环境响应） |

一个 T 长度的 Trial 可表示为 ξ = {a₁, o₁, a₂, o₂, ..., oₜ, aₜ}。

## 狭义定义（Narrow Definition）

狭义记忆仅涉及**同一 Trial 内**的历史信息。对于给定任务，Step t 之前的记忆为 ξₜ = {a₁, o₁, ..., aₜ₋₁, oₜ₋₁}。

在玩具示例中，Agent 在 [Step 3] 安排行程时，记忆包含 [Step 1] 和 [Step 2] 中已选定的景点和到达时间信息。

## 广义定义（Broad Definition）

广义记忆来自更广泛来源。给定顺序任务 {T₁, T₂, ..., T_K}，任务 T_k 在 Step t 的记忆来自三个来源：

1. **同一 Trial 内的历史信息**：ξₜᵏ = {a₁ᵏ, o₁ᵏ, ..., aₜ₋₁ᵏ, oₜ₋₁ᵏ}
2. **跨 Trial 的历史信息**：Ξᵏ = {ξ¹, ξ², ..., ξᵏ⁻¹, ξᵏ'}，包括其他任务的 Trial 和当前任务的失败 Trial
3. **外部知识**：Dₜᵏ，来自 Agent-环境交互之外

## 记忆辅助的 Agent-环境交互

记忆模块通过三个操作实现 Agent-环境交互的三阶段：

| 阶段 | 操作 | 形式化 |
|------|------|--------|
| 感知存储 | Memory Writing | mₜ = W({aₜ, oₜ}) |
| 信息处理 | Memory Management | Mₜ = P(Mₜ₋₁, mₜ) |
| 决策支持 | Memory Reading | M̂ₜ = R(Mₜ, cₜ₊₁) |

统一演化函数：aₜ₊₁ = LLM{R(P(Mₜ₋₁, W({aₜ, oₜ})), cₜ₊₁)}

**关键洞察**：不同工作使用不同规格化——Reflexion 中 R 和 P 设为相同函数；Generative Agents 中 R 基于相似性、时间间隔和重要性三准则，P 通过反思过程实现。
