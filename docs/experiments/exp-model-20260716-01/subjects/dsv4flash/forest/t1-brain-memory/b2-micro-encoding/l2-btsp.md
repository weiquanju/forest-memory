---
forest: memory-systems-ai
tree: t1-brain-memory
branch: b2-micro-encoding
leaf: l2-btsp
title: BTSP行为时间尺度可塑性—单次快速学习机制
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
model: DeepSeek V4 Flash
source: "input/bim_source/人脑记忆机制的数据结构与算法分析.md"
refs:
  - "Bittner et al. (2017, Science, DOI: 10.1126/science.aan3846) — BTSP首次发现，树突钙平台电位驱动的海马CA1位置场快速形成"
  - "Wu & Maass (2025, Nature Communications) — BTSP计算模型，证明其窗口机制可解释位置场一次性形成"
  - "Magee (2026, Nature Neuroscience) — BTSP广泛存在于海马体等脑区的综述"
  - "BTSP窗口：上升时间约4秒，衰减时间约3秒（Bittner实验实测）；后续模型常简化为对称窗口（Wu & Maass, 2025）"
---

# BTSP：行为时间尺度可塑性

BTSP（Behavioral Time Scale Plasticity）是近年发现的一种突触可塑性规则，与STDP有本质区别。BTSP由**树突钙离子平台电位**驱动，在一个秒级时间窗口内（上升约4秒、衰减约3秒），一次性增强窗口内所有活跃的突触输入。与需要毫秒级精确时序匹配且多次重复的STDP不同，BTSP允许**单次经历**即可完成突触强度的持久改变。大脑使用多时间尺度的可塑性规则分工：毫秒级的STDP负责精细调谐（序列学习、因果推理），秒级的BTSP负责在行为关键时刻一次性创建宏观记忆痕迹。
