---
forest: mi
tree: agent-memory
branch: frameworks
title: Agent记忆框架
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
description: Mem0/MemVerse/DYNA/Mem-α等前沿Agent记忆框架的设计思路与比较
keywords:
  - Mem0
  - MemVerse
  - DYNA
  - Mem-α
  - 结构化记忆
  - RL驱动记忆
atom_type: semantic
status: draft
refs:
  - "[mi] 记忆来源与操作 | 框架对操作流程的具体实现"
  - "[mi] Agent记忆定义与分类 | 框架对应的分类定位"
---

# Agent记忆框架

**Mem0**：结构化持久记忆系统，将记忆组织为结构化表示（实体、关系、重要性评分），支持自动合并和分层检索。在长对话任务中相比OpenAI基线LLM-as-Judge提升26%，延迟降低91%，Token成本节省90%+。

**MemVerse**：多智能体共享记忆平台，为多个Agent提供统一的持久化记忆层，支持Agent间的经验共享和知识传递。

**DYNA**：动态记忆架构，通过自适应遗忘策略和重要性评分动态管理记忆生命周期，解决长对话中的上下文窗口限制问题。

**Mem-α**（Wang et al., 2025）：利用强化学习（RL）训练LLM智能体自主决定何时在核心记忆、情景记忆和语义记忆组件之间存储、更新和检索信息。RL训练本质上优化LLM agent的对话记忆管理策略，体现由价值信号驱动的自适应记忆管理思路。
