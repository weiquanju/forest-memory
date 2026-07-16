---
forest: memory-systems-ai
tree: t1-brain-memory
branch: b2-micro-encoding
leaf: l3-sparse-coding
title: 稀疏编码与模式分离
version: 1.0.0
created: 2026-07-16
model: DeepSeek V4 Flash
source: "input/bim_source/人脑记忆机制的数据结构与算法分析.md"
refs:
  - "齿状回（DG）颗粒细胞实现稀疏编码 — 约9%激活率（GoodSmith et al., 2017, Neuron）"
  - "计算模型常假设2–5%激活率以突出模式分离效应（Hainmueller & Bartos, 2020, Nature Reviews Neuroscience）"
  - "模式分离：将相似输入映射为差异很大的神经活动模式，防止记忆混淆"
  - "Karbowski (2019) — 代谢约束模型：突触可塑性消耗总能量预算4-11%"
  - "Shuai et al. (2010, Cell) — 主动遗忘的Rac1分子通路"
  - "Akers et al. (2014, Science) — 成年神经发生导致旧记忆痕迹稀释"
---

# 稀疏编码与模式分离

大脑在编码记忆时采用**稀疏分布式编码**策略：每个记忆事件中仅一小部分神经元被激活。在海马体齿状回（DG），颗粒细胞的发放极其稀疏（约9%激活率），这种稀疏性通过**模式分离**机制将相似输入映射为差异很大的输出，防止相似记忆间的混淆。在算法上，这类似于哈希函数或正交编码。大脑还通过**再巩固**机制在记忆提取时进行在线更新，并通过**主动遗忘**——包括突触资源竞争、Rac1分子通路、成年神经发生等机制——防止记忆系统过载。
