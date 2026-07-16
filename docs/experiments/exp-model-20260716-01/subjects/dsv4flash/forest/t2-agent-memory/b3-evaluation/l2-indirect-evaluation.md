---
forest: memory-systems-ai
tree: t2-agent-memory
branch: b3-evaluation
leaf: l2-indirect-evaluation
title: 代理记忆的间接评估与基准
version: 1.0.0
created: 2026-07-16
model: DeepSeek V4 Flash
source: "input/papers/2404.13501.md; input/frs_source/AI与大模型在知识领域、Agent记忆、推理数据及推理关系中的前沿研究综述.md"
refs:
  - "间接评估通过下游任务表现衡量记忆能力：对话、多源问答、长上下文应用"
  - "MemoryArena (arXiv:2602.16313, 2026) — 多会话记忆-环境循环基准"
  - "评估从静态基准向动态多轮交互的范式演进"
---

# 代理记忆的间接评估与基准

间接评估不直接测试记忆模块，而是通过下游任务表现来推断记忆能力。典型任务包括：**长对话**（需要保持跨轮次的一致性）、**多源问答**（需要融合多轮交互积累的信息）、**长上下文应用**（需要在大信息量中精确检索）。**MemoryArena**（arXiv:2602.16313, 2026）提出了多会话记忆-环境循环评估框架，标志着评估从静态基准向动态多轮交互范式的演进。
