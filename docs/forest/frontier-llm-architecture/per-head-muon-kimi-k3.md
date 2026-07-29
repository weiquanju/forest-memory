---
forest: flm
tree: 训练方法论
branch: 优化器设计
title: Per-Head Muon 在 Kimi K3 中的应用
version: 1.0.0
created: 2026-07-29
updated: 2026-07-29
description: Kimi K3 的 Per-Head Muon 优化器——按 head 维度分区执行 Newton-Schulz 正交化，均衡各 head 之间的更新尺度。
keywords:
  - Per-Head Muon
  - Muon optimizer
  - head-wise orthogonalization
  - Kimi K3
refs:
  - "[flm] Muon 优化器在 DeepSeek-V4 中的应用 | 基础 Muon 算法"
---

# Per-Head Muon 在 Kimi K3 中的应用

## 概述

Kimi K3 在 Kimi K2 的 Muon 优化器基础上，对 attention 投影矩阵做了 **Per-Head 变体**：将 Q、K、V 投影矩阵的动量矩阵沿 head 维度分区，对每个 head 的 block 单独执行 Newton-Schulz 正交化。

## 动机

Full-matrix 正交化将所有 heads 视为单一耦合块。当不同 heads 的梯度或动量尺度差异较大时：
- 大尺度 head 主导共享的更新方向
- 小尺度 head 收到不充分的归一化更新

Per-head 正交化**均衡各 head 的更新尺度**。

## 技术实现

对 attention 投影矩阵 W ∈ R^(d × n_h·d_k)：
```
W = [W_head_1, W_head_2, ..., W_head_{n_h}]    # 沿 head 维度切分
for each W_head_i:
    O_head_i = NewtonSchulz(M_head_i)            # 独立正交化
O = concat(O_head_1, ..., O_head_{n_h})          # 合并
```

## 收益

1. **更均衡的学习动态**：各 head 在更大规模下保持平衡的更新幅度
2. **训练稳定性提升**：减少 head 间的梯度尺度差异导致的训练不稳定
3. **轻微降低优化器开销**：在 tall per-head blocks 上的 Newton-Schulz 比在全矩阵上更便宜

## 与 DeepSeek-V4 Muon 的对比

| 维度 | DeepSeek-V4 Muon | Kimi K3 Per-Head Muon |
|------|-----------------|----------------------|
| 正交化粒度 | 全矩阵 | Per-head block |
| Newton-Schulz 策略 | 两阶段 Hybrid (8+2) | 未详述 |
| QK-Clipping | 不需要（RMSNorm on Q/K） | 不需要（NoPE + KDA） |
| 权重衰减 | 有 | 0.1 |
| ZeRO 集成 | Knapsack 分配 + 冗余计算 | 未详述 |
