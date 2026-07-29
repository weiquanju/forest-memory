---
forest: flm
tree: 架构设计
branch: 注意力机制
title: KDA——Kimi Delta Attention
version: 1.0.0
created: 2026-07-29
updated: 2026-07-29
description: Kimi K3 的 Kimi Delta Attention (KDA) 机制——基于 delta-rule 的线性注意力，含 channel-wise forget gate、lower-bounded decay 和 chunkwise parallel 设计。
keywords:
  - KDA
  - Kimi Delta Attention
  - linear attention
  - delta-rule
  - channel-wise decay
  - chunkwise parallel
  - Kimi K3
refs:
  - "[flm] Gated MLA 在 Kimi K3 中 | 配合使用的全局注意力层"
  - "[flm] KDA/MLA 混合注意力架构 | 在完整架构中的角色"
  - "[flm] CSA——压缩稀疏注意力 | 竞争性注意力方案对比"
---

# KDA——Kimi Delta Attention

## 概述

KDA（Kimi Delta Attention）是 Kimi K3 的核心线性注意力机制，首次发表于 Kimi Linear 论文（Kimi Team, 2025, arXiv:2510.26692）。它在 delta-rule recurrence（Schlag et al., 2021, arXiv:2102.11174）和 Gated DeltaNet（Yang et al., 2024）基础上引入 **channel-wise forget gate**，实现了高效的序列混合。Kimi K3 技术报告中将其标为参考 [64]。

## 核心机制

### Recurrent Form

对于单个 attention head：

```
S_t = (I - β_t·k_t·k_t^⊤) · Diag(α_t) · S_{t-1} + β_t·k_t·v_t^⊤
õ_t = S_t^⊤ · q_t
```

其中：
- **α_t ∈ (0,1)^dk**：channel-wise 逐步保留因子（forget gate）
- **β_t ∈ (0,1)**：delta-rule 写入强度
- **S_t ∈ R^(dk×dv)**：固定大小的 recurrent state（替代 KV cache）

### Chunkwise Parallel Form

KDA 采用跨 chunk 串行、chunk 内并行的计算策略：

```
A_[t] = Tril((Q_[t] ⊙ Γ^{1→C}_[t]) · (K_[t] / Γ^{1→C}_[t])^⊤)
O_[t] = (Γ^{1→C}_[t] ⊙ Q_[t]) · S_[t] + A_[t] · Ṽ_[t]
       └── inter-chunk ──┘   └── intra-chunk ──┘
```

其中 Γ^{1→C}_[t] = [γ_1, ..., γ_C] 是 chunk 内累积衰减因子的行向量。

### Lower-Bounded Decay（Kimi K3 改进）

相对于 Kimi Linear 的 negative-Softplus 映射（无下界），Kimi K3 使用 scaled sigmoid：

```
g^h_t = g_min · Sigmoid(e^{A_h} · z^h_t) ∈ (g_min, 0)^dk
α^h_t = exp(g^h_t) ∈ (e^{g_min}, 1)^dk
```

其中 g_min = -5，A_h 为可学习 per-head log-scale。

**关键收益**：
- 每个 retention factor α^h_t > e^{-5} ≈ 6.7×10^{-3}
- 16-token tile 的累积 log-decay ∈ (-80, 0)
- 倒数缩放因子 < e^{80}，在 BF16 动态范围内
- **对角线 tile 也可用 Dense Tensor Core 矩阵乘法**（消除 Kimi Linear 中的 position-pair 对角线路径）

### Full-Rank Output Gate

将 Kimi Linear 的低秩输出门改为输入相关的全秩投影：

```
y_t = W_o · [Sigmoid(W_g·x_t) ⊙ RMSNorm(õ_t)]
```

## 参数化细节

```
q^h_t, k^h_t = L2Norm(Swish(ShortConv(W_{q,k}·x_t)))   # head dim dk
v^h_t = Swish(ShortConv(W_v·x_t))                        # head dim dv
β^h_t = Sigmoid(W_β·x_t)                                  # 写入强度
z^h_t = W_α↑·W_α↓·x_t + b^h_α                              # 低秩 decay logits
```

## 状态大小优势

与传统 softmax attention 的 O(n·d) KV cache 不同，KDA 的 recurrent state S ∈ R^(dk×dv) 大小固定——与序列长度无关。这使得 KDA 在 1M token 上下文下具有天然的内存优势。
