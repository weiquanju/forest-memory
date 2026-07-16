---
forest: frs
tree: knowledge-update
branch: kg-continual-learning
leaf_id: frs-kg-cont-002
title: BAKE贝叶斯引导持续KG嵌入
type: method
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
source: "[frs_source] §7.1 | Li et al., arXiv:2508.02426, 2025 [35]"
refs:
  - "[frs-kg-cont-001] EWC在KG持续学习 | BAKE以贝叶斯框架提供比EWC更强的理论保证"
---

# BAKE 贝叶斯引导持续KG嵌入

## 方法概述

**BAKE (Bayesian-guided Continual Knowledge Graph Embedding)** 将持续KG嵌入形式化为**序贯贝叶斯推断问题** [35]。

## 理论优势

| 特性 | 说明 |
|------|------|
| 贝叶斯后验更新 | 作为天然的持续学习策略 |
| 数据顺序不敏感 | 理论上不受任务顺序影响 |
| 理论保证 | 尽可能保留先验知识 |

## 持续聚类方法

BAKE进一步引入**持续聚类方法**维持实体嵌入的紧凑簇结构——类似概念在嵌入空间保持相近，减少新知识对旧知识簇的破坏。

## 性能

在多个CKGE基准上达到**最优** [35]。

## 跨模态扩展

同一团队也提出了**MRCKG**[36]：首次系统研究持续多模态知识图谱推理（CMMKGR），通过多模态-结构协同课程调度和跨模态知识保留机制缓解遗忘。

## 局限

- 真实世界KG漂移场景下贝叶斯框架的充分性尚未验证
- 聚类维护存在额外计算开销
