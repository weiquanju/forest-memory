---
forest: mi
tree: neural-micro
branch: synaptic-plasticity
title: 突触可塑性算法
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
description: Hebbian、STDP与BTSP三种突触可塑性规则的多时间尺度分工与算法对应
keywords:
  - Hebbian学习
  - STDP
  - BTSP
  - 突触可塑性
  - 时间尺度分工
  - 钙离子平台电位
atom_type: semantic
status: draft
refs:
  - "[mi] 记忆的时间分层 | 可塑性作为长期记忆基础"
  - "[mi] 模式完成与CA3吸引子网络 | Hebbian学习在CA3自联想网络中的应用"
---

# 突触可塑性算法

突触可塑性是记忆形成的细胞基础，存在三种不同时间尺度的可塑性规则：

**Hebbian学习律**（1949）："一起放电的神经元会加强彼此连接"，对应于相关学习算法。在人工神经网络中用于自联想记忆网络（如Hopfield网络）的权重初始化。

**STDP（脉冲时序依赖可塑性）**：Hebbian原则的时序精细化。突触前神经元在突触后之前数毫秒放电→增强（LTP）；滞后→减弱（LTD）。基于相对时序的学习规则使神经网络能根据输入信号时间相关性调整连接，对应于时序差分学习算法，可用于训练脉冲神经网络（SNN）。

**BTSP（行为时间尺度可塑性）**：Bittner等人（2017, *Science*）发现的海马体CA1区可塑性规则。核心机制是树突钙离子平台电位——当CA1锥体细胞远端树突产生大幅持久钙信号时，会在秒级时间窗口内（约4秒上升+3秒衰减）一次性增强窗口内所有活跃突触输入。BTSP可在**单次经历**中完成持久突触改变，与STDP形成互补：毫秒级STDP负责精细时序调谐，秒级BTSP负责行为关键时刻的快速宏观记忆形成。
