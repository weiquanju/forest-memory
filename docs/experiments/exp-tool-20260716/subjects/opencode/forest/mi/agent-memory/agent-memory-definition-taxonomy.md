---
forest: mi
tree: agent-memory
branch: taxonomy
title: Agent记忆定义与分类
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
description: 从载体形式、功能角色和动态过程三个维度对AI Agent记忆进行统一分类
keywords:
  - Agent记忆
  - 记忆分类
  - 载体形式
  - 功能维度
  - 动态过程
  - 三维分类框架
atom_type: semantic
status: draft
refs:
  - "[mi] 模块化记忆分类 | 人脑记忆分类对Agent分类的启发"
  - "[mi] 键值记忆统一框架 | KV框架对Agent记忆架构设计的理论支撑"
---

# Agent记忆定义与分类

近期综合调查（Hu et al.）提出统一的Agent记忆三维分类框架：

**载体形式（Forms）**：令牌级（Token-level，显式离散，如对话历史）、参数级（Parametric，隐式权重，如模型参数）、潜在级（Latent，隐状态，如RNN隐状态）。

**功能（Functions）**：事实性记忆（Factual，知识存储）、经验性记忆（Experiential，技能和洞察）、工作记忆（Working Memory，主动上下文管理）。

**动态过程（Dynamics）**：涉及记忆的编码、巩固、检索和更新各阶段的动态管理。

Mem0框架证明了结构化持久记忆对长对话一致性的关键作用：相对OpenAI基线在LLM-as-Judge指标上提升26%，p95延迟降低91%，Token成本节省超过90%。这一框架为Agent记忆系统设计提供了系统化的分类学基础。
