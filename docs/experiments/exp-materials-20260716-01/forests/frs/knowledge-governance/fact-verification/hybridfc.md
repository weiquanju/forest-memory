---
forest: frs
tree: knowledge-governance
branch: fact-verification
leaf_id: frs-fact-004
title: HybridFC混合事实核查
type: method
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
source: "[frs_source] §4.1 | Qudus et al., arXiv:2409.06692, 2024 [23]"
---

# HybridFC 混合事实核查

## 方法概述

**HybridFC** 提出混合事实核查方法 [23]，在集成学习框架中利用多种核查方法的多样性。

## 四种核查方法

| 方法类型 | 描述 |
|---------|------|
| 文本方法 | 基于文本语义的声明-证据匹配 |
| 路径方法 | 基于KG路径的推理验证 |
| 规则方法 | 基于逻辑规则的推断 |
| 嵌入方法 | 基于嵌入式表示的相似度判断 |

## 性能

在FactBench数据集上AUC提升**0.14-0.27** [23]。

## 设计洞察

不同事实核查方法在不同类型的声明上各有优势——HybridFC通过集成学习让互补的方法相互弥补，这是对"没有单一银弹"原则的实际验证。
