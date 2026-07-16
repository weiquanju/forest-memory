---
forest: bim
tree: 微观机制
branch: 突触可塑性
title: Hebbian学习律
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
description: Hebb（1949）提出的"一起放电的神经元加强彼此连接"——相关学习算法，用于自联想记忆网络的权重初始化
keywords:
  - Hebbian学习
  - 相关学习
  - 自联想记忆
  - Hopfield网络
  - 突触增强
atom_type: semantic
status: draft
---

# Hebbian学习律

## 核心原理

Hebb（1949）提出的"一起放电的神经元会加强彼此连接"（fire together, wire together）。在算法上对应于相关学习：两个神经元在时间上相关的活动会增强突触连接。

## 算法对应

- 在人工神经网络中用于自联想记忆网络（如 Hopfield 网络）的权重初始化
- 通过存储输入模式的自相关形成记忆痕迹
- 是更复杂可塑性规则（STDP、BTSP）的奠基性原则
