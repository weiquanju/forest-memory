---
forest: frs
tree: Agent记忆
branch: 管理挑战
title: 前沿Agent记忆管理框架
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
description: Mem0/MemVerse/DYNA三大前沿记忆框架的比较——图结构/层次化KG/时态KG作为持久记忆的事实标准
keywords:
  - Mem0
  - MemVerse
  - DYNA
  - 层次化KG
  - 持久记忆
atom_type: semantic
status: draft
refs:
  - "[frs] Agent记忆统一三维分类框架 | 三大框架对三维分类的实现"
  - "[frs] 记忆对推理与输出质量的影响 | 框架应对经验跟随问题的策略"
---

# 前沿Agent记忆管理框架

## 三大框架比较

| 框架 | 组织方式 | 遗忘机制 | 多模态 | 训练 |
|------|---------|---------|:---:|:---:|
| **Mem0** | 图结构 | 隐式（图更新） | 否 | 否 |
| **MemVerse** | 层次化KG+周期蒸馏 | 显式自适应遗忘 | 是 | 否 |
| **DYNA** | 时态KG+随机游走 | 隐式权重衰减 | 否 | 否 |

## 关键观察

- MemVerse 唯一覆盖多模态+显式遗忘+知识蒸馏
- 三种框架均以 KG 为核心组织方式——图结构正在成为持久记忆的事实标准
- "经验跟随属性"带来的错误累积风险尚未被任何框架系统性解决
