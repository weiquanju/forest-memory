---
forest: memory-systems-ai
tree: t2-agent-memory
branch: b3-evaluation
leaf: l1-direct-evaluation
title: 代理记忆的直接评估方法
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
model: DeepSeek V4 Flash
source: "input/papers/2404.13501.md"
refs:
  - "主观评估：人工评分、用户满意度调查"
  - "客观评估：精确率/召回率/F1、记忆容量、检索延迟"
  - "MemBench (Tan et al., 2025, arXiv:2506.21605) — 多维度记忆评估基准"
  - "MemoryAgentBench (Hu et al., 2025, arXiv:2507.05257) — 增量多轮交互评估"
---

# 代理记忆的直接评估方法

直接评估针对记忆模块本身进行测量，分为**主观评估**（人工评分、用户满意度调查）和**客观评估**（精确率/召回率、记忆容量、检索延迟等量化指标）。近年涌现的专项基准如 **MemBench**（Tan et al., 2025, arXiv:2506.21605）提供多维度记忆评估方案，**MemoryAgentBench**（Hu et al., 2025, arXiv:2507.05257）通过增量多轮交互评估 Agent 记忆能力。
