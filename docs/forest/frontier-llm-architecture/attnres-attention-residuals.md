---
forest: flm
tree: 架构设计
branch: 残差连接创新
title: AttnRes——注意力残差
version: 1.0.0
created: 2026-07-29
updated: 2026-07-29
description: Kimi K3 的 Attention Residuals (AttnRes)——将注意力机制应用于网络深度维度，使每层能选择性检索所有前驱层的表示。
keywords:
  - AttnRes
  - Attention Residuals
  - depth attention
  - pseudo-query
  - BlockAttnRes
  - Kimi K3
refs:
  - "[flm] mHC——流形约束超连接 | 竞争性残差连接方案对比"
---

# AttnRes——注意力残差

## 概述

Attention Residuals (AttnRes, Anonymous, 2026b; 截至 2026-07 仍处于双盲审稿匿名状态，Kimi K3 报告引用为 [58]，尚无独立公开论文完整披露机制细节）将 Transformer 的核心思想——通过注意力选择性访问序列位置——应用于**网络深度维度**：每层使用可学习的 pseudo-query 从所有前驱层检索表示，而非均匀累积它们。

## 核心动机

标准残差连接 h_{l+1} = h_l + F_l(h_l) 将所有先前信息压缩到单一状态 h_l 中，形成深度上的信息瓶颈——类似于 RNN 在时间上的瓶颈。Transformer 用 attention 替换了 RNN 的 recurrence，AttnRes 用同样的方法论替换深度上的"recurrence"。

## Full Attention Residuals

对每层 l，定义层特定的可学习 **pseudo-query** q_l = w_l ∈ R^d：

```
k_i = v_i = f_i(h_i)    # i ∈ {0, 1, ..., l-1}，h_0 = token embedding
α_{i→l} = softmax_i( q_l^⊤ · RMSNorm(k_i) )
h_l = Σ_{i=0}^{l-1} α_{i→l} · v_i
```

RMSNorm 应用于 keys 防止大模长的层输出主导注意力权重。

## Block Attention Residuals

为降低 Full AttnRes 的 O(L·d) 内存开销（保存所有层输出），引入 Block 结构：

- 将 L 层划分为 N 个 block，每 block S = L/N 层
- Block 内输出通过求和归约为单一表示 b_n = Σ_{j∈B_n} f_j(h_j)
- 跨 Block 执行 Full Attention（N 个 block 级表示）
- Block 内层仍可访问本 block 的部分和 b^i_n

**内存从 O(L·d) 降至 O(N·d)**，推理时通过 online softmax 合并并行 block 间结果与串行 block 内部分和。

**Kimi K3 配置**：N ≈ 8 个 blocks, 每 block 12 层, 加上 embedding 共 9 个总 blocks。

## AttnRes vs mHC 对比

| 维度 | AttnRes (Kimi K3) | mHC (DeepSeek-V4) |
|------|------------------|-------------------|
| **机制** | 注意力 over 层 | 流形约束的线性变换 |
| **选择性** | 每层动态学习权重 | 每层动态参数化 + 静态 bias |
| **信息访问** | 任意前驱层（skip 所有中间层） | 逐层传递（宽度扩展 n_hc 倍） |
| **计算复杂度** | O(L²d) Full / O(N²d) Block | O(n_hc²·d) per layer |
| **理论基础** | Transformer 注意力 → 深度 | Birkhoff 多面体 → 非扩展性保证 |
| **稳定性保证** | RMSNorm on keys | Sinkhorn-Knopp 谱范数 ≤1 |
| **开销** | O(Nd) 内存 | 6.7% wall-time |
