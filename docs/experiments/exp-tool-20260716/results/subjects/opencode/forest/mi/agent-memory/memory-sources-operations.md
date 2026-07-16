---
forest: mi
tree: agent-memory
branch: implementation
title: 记忆来源与操作
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
description: LLM智能体记忆的三个来源类型、两种表示形式及其核心操作流程
keywords:
  - 记忆来源
  - 文本记忆
  - 参数记忆
  - 记忆写入
  - 记忆管理
  - 记忆读取
atom_type: semantic
status: draft
refs:
  - "[mi] Agent记忆定义与分类 | 三维分类确定记忆来源的归属"
  - "[mi] Agent记忆框架 | 具体框架对操作流程的实现"
---

# 记忆来源与操作

**记忆来源**：Inside-trial（同次交互内信息）、Cross-trial（跨次交互信息）、External Knowledge（外部知识库）。

**记忆形式**：文本形式（Textual，显式存储文本描述，可解释性强但占用上下文窗口）和参数形式（Parametric，隐式存储在模型权重中，检索快但不可解释）。两者各具优劣——文本记忆便于编辑和溯源但占用token预算，参数记忆检索高效但难以精确更新。

**核心操作**：写入（Writing，编码和存储新信息）、管理（Management，更新、合并、遗忘过期记忆）、读取（Reading，根据当前上下文检索相关记忆）。这些操作设计直接影响Agent在长对话、多轮交互和复杂任务中的表现。
