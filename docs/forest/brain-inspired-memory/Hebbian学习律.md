---
forest: bim
tree: 微观机制
branch: 突触可塑性
title: Hebbian 学习律
version: 1.0.0
created: 2026-07-12
updated: 2026-07-12
description: Hebb 在 1949 年提出的经典学习律——"一起放电的神经元会加强彼此连接"，以及其在 Hopfield 网络等自联想记忆模型中的应用
keywords:
  - Hebbian学习
  - 突触可塑性
  - 联想记忆
  - Hopfield网络
  - 相关学习
refs:
  - "[bim] STDP脉冲时序依赖可塑性 | Hebbian 的时序精细化"
  - "[bim] BTSP行为时间尺度可塑性 | 三种可塑性规则的对比"
  - "[bim] 联想记忆与内容寻址 | Hebbian 在自联想网络中的应用"
---

# Hebbian 学习律

## 原始陈述

**"Cells that fire together, wire together."**  
*—— Donald Hebb, The Organization of Behavior (1949)*

## 算法对应

```
如果神经元 A 和 B 在时间上相关地活动
→ A→B 的突触连接增强
→ 实现联想记忆的编码
```

## 在人工神经网络中的应用

### Hopfield 网络（1982）

- 使用 Hebbian 学习做权重初始化
- 存储输入模式的自相关来形成记忆痕迹
- 检索时网络收敛到已存储的最近模式

**公式**：
$$w_{ij} = \sum_{\mu} \xi_i^{\mu} \xi_j^{\mu}$$

其中 $\xi^{\mu}$ 是第 $\mu$ 个存储模式。

## 与后续规则的关系

```
Hebbian (1949)  ← 基础原则："相关即增强"
    ↓
STDP  (1990s)   ← 时序精细化：前后毫秒级精确匹配
    ↓
BTSP  (2017)    ← 行为尺度：秒级窗口一次增强
```

Hebbian 是"定性原则"，STDP 和 BTSP 是"定量机制"。三种规则共同构成了大脑**多时间尺度的可塑性规则分工**。
