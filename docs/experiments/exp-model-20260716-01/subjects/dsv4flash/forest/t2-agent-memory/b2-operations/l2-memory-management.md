---
forest: memory-systems-ai
tree: t2-agent-memory
branch: b2-operations
leaf: l2-memory-management
title: 代理记忆的管理与遗忘策略
version: 1.0.0
created: 2026-07-16
model: DeepSeek V4 Flash
source: "input/papers/2404.13501.md; input/frs_source/AI与大模型在知识领域、Agent记忆、推理数据及推理关系中的前沿研究综述.md"
refs:
  - "记忆管理涉及记忆的更新、合并、优先级排序和遗忘"
  - "遗忘机制：基于时间衰减、重要性评分、容量阈值等策略"
  - "EWC（Elastic Weight Consolidation）— Kirkpatrick et al. (2017) — 持续学习防止灾难性遗忘"
---

# 代理记忆的管理与遗忘策略

记忆管理（Memory Management）负责控制记忆系统的增长和质量，包括：**更新**（新信息如何修正旧记忆）、**合并**（相似记忆如何整合）、**优先级排序**（哪些记忆更重要）和**遗忘**（何时删除不重要记忆）。遗忘策略包括固定时间衰减、基于重要性评分的选择性保留、容量阈值触发式清理等。在持续学习场景中，EWC（Elastic Weight Consolidation）等方法通过约束重要权重的变动来防止灾难性遗忘。
