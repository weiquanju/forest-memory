---
forest: flm
tree: 训练方法论
branch: 优化器设计
title: Muon 优化器在 DeepSeek-V4 中的应用
version: 1.0.0
created: 2026-07-29
updated: 2026-07-29
description: DeepSeek-V4 采用的 Muon 优化器——基于 Newton-Schulz 迭代的矩阵正交化优化，含混合迭代策略和 ZeRO 集成方案。
keywords:
  - Muon optimizer
  - Newton-Schulz
  - orthogonalization
  - ZeRO
  - DeepSeek-V4
refs:
  - "[flm] Per-Head Muon 在 Kimi K3 中 | 对比性优化器方案"
---

# Muon 优化器在 DeepSeek-V4 中的应用

## 概述

DeepSeek-V4 系列对大多数模块采用 Muon 优化器（Keller Jordan, 2024 [blog]; Liu et al., 2025 [arXiv:2502.16982]），因其更快的收敛速度和改善的训练稳定性。Muon 最初由 Keller Jordan 在博客文章中提出，后经 Kimi/Moonshot 团队在 "Muon is Scalable for LLM Training" 中验证其大规模可扩展性。Embedding、Prediction Head、mHC 的静态 bias/gating factors 和所有 RMSNorm 权重仍使用 AdamW。

## 算法流程

```
for each weight matrix W ∈ R^(n×m):
    G_t = ∇_W L_t(W_{t-1})                           # 梯度
    M_t = μ·M_{t-1} + G_t                             # 动量累积
    O'_t = HybridNewtonSchulz(μ·M_t + G_t)             # Nesterov + 正交化
    O_t = O'_t · sqrt(max(n,m)) · γ                    # RMS 缩放
    W_t = W_{t-1} · (1 - ηλ) - η·O_t                  # 权重衰减 + 更新
```

## Hybrid Newton-Schulz 迭代

分两阶段执行 10 次迭代：

### 第一阶段（前 8 步）
系数 `(a, b, c) = (3.4445, -4.7750, 2.0315)`，快速将奇异值收敛到接近 1。

### 第二阶段（最后 2 步）
系数 `(a, b, c) = (2, -1.5, 0.5)`，精确将奇异值稳定在 1。

每次迭代：
```
M_k = a·M_{k-1} + b·(M_{k-1}·M_{k-1}^⊤ - I)·M_{k-1} + c·(M_{k-1}·M_{k-1}^⊤ - I)²·M_{k-1}
```

### 避免 QK-Clipping

由于 DeepSeek-V4 的 attention 架构允许直接在 attention queries 和 KV entries 上应用 RMSNorm（有效防止 attention logits 爆炸），因此**不需要** Liu et al. (2025) 中的 QK-Clip 技术。

## ZeRO 混合策略

### 稠密参数
- 限制最大 ZeRO 并行数
- 使用 Knapsack 算法分配参数矩阵到各 rank
- Padding 开销 < 10%（每个 rank 管理不超过 5 个矩阵）
- 超出限制时，在额外 data-parallel groups 上冗余计算

### MoE 参数
- 每个 expert 独立优化
- 按类型（down/gate/up projection）展平并跨 rank 分布
- 不限制 ZeRO 并行数（expert 数量大）
- 连续同形状参数自动合并以批量执行 Newton-Schulz

### BF16 Newton-Schulz + FP8 通信
- MoE 梯度同步使用随机舍入量化为 BF16，通信量减半
- 用 all-to-all + local FP32 sum 替代传统 reduce-scatter，避免低精度累加误差
