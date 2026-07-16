---
forest: agent-memory-survey
tree: t2-memory-implementation
title: 记忆实现架构
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
description: >
  LLM-based Agent 记忆机制的三维实现框架：记忆来源（Sources）、记忆形态（Forms）、
  记忆操作（Operations）。覆盖 26+ 模型的分类对比，文本记忆与参数化记忆的权衡分析，
  以及写入-管理-读取三操作的工程实现策略。
refs:
  - "[t1-b1] W/P/R统一模型 | 三操作直接映射到本树的写入/管理/读取"
  - "[t3] 记忆评估方法 | 评估方法验证本树中各实现选择的效果"
---

# 记忆实现架构

## 本树枝干与叶子

| 枝干 | 叶子文档 |
|------|---------|
| **B2.1 记忆来源** | [inside-trial-vs-cross-trial](b1-sources/inside-trial-vs-cross-trial.md), [external-knowledge-integration](b1-sources/external-knowledge-integration.md) |
| **B2.2 记忆形态** | [textual-memory-forms](b2-forms/textual-memory-forms.md), [parametric-memory-forms](b2-forms/parametric-memory-forms.md), [textual-vs-parametric-tradeoffs](b2-forms/textual-vs-parametric-tradeoffs.md) |
| **B2.3 记忆操作** | [memory-writing-strategies](b3-operations/memory-writing-strategies.md), [memory-management-mechanisms](b3-operations/memory-management-mechanisms.md), [memory-reading-retrieval](b3-operations/memory-reading-retrieval.md) |
