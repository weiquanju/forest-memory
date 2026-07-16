---
forest: memory-systems-ai
tree: t1-brain-memory
branch: b2-micro-encoding
leaf: l1-hebbian-stdp
title: 突触可塑性—Hebbian学习律与STDP
version: 1.0.0
created: 2026-07-16
model: DeepSeek V4 Flash
source: "input/bim_source/人脑记忆机制的数据结构与算法分析.md"
refs:
  - "Hebbian学习律：一起放电的神经元会加强彼此连接 — 对应于相关学习算法"
  - "STDP：突触增强/减弱取决于突触前后放电的相对时序 — 对应时序差分学习"
  - "Bittner et al. (2017, Science) — BTSP的发现"
  - "Wu & Maass (2025, Nature Communications) — BTSP计算模型"
  - "Magee (2026, Nature Neuroscience) — BTSP广泛存在于海马体的综述"
---

# 突触可塑性规则：Hebbian与STDP

突触可塑性是记忆形成的细胞基础。**Hebbian学习律**（1949）提出"一起放电的神经元会加强彼此连接"，在算法上对应相关学习，常用于Hopfield网络等自联想记忆模型。**STDP（脉冲时序依赖可塑性）**是Hebbian原则的时序精细化：突触前神经元在突触后之前数毫秒放电则增强（LTP），反之则减弱（LTD）。STDP在算法上对应时序差分学习，可用于训练脉冲神经网络完成模式识别和序列预测。
