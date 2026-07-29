---
forest: flm
tree: 架构设计
branch: 注意力机制
title: Gated MLA 在 Kimi K3 中的演进
version: 1.0.0
created: 2026-07-29
updated: 2026-07-29
description: Kimi K3 对 Multi-head Latent Attention (MLA) 的改进——NoPE 配置、Full-Rank Output Gate 和 FP32 输出精度修正。
keywords:
  - Gated MLA
  - Multi-head Latent Attention
  - NoPE
  - full-rank gate
  - Kimi K3
refs:
  - "[flm] KDA——Kimi Delta Attention | 配合使用的线性注意力层"
  - "[flm] KDA/MLA 混合注意力架构 | 在完整架构中的角色"
---

# Gated MLA 在 Kimi K3 中的演进

## 概述

Multi-head Latent Attention (MLA)，最初由 DeepSeek-V2（DeepSeek-AI, 2024）提出，通过低秩 latent vector c_t = W_c·x_t 压缩 KV 表示，显著减少 KV cache 占用。Kimi K3 在 Kimi K2/2.5 的基础上对 MLA 做了三项关键改进。

## 三项关键改进

### 1. NoPE 配置

不同于 Kimi K2/2.5 在 MLA 中使用位置编码，Kimi K3 在**所有 MLA 层应用 No Position Encoding (NoPE)**：

- KDA 层提供 position-sensitive 和 recency-aware 的序列混合
- MLA 层专注于不受位置约束的全局内容交互
- 避免了扩展上下文时修改 RoPE 频率基或应用 YaRN 的需求

这种 **位置编码关注分离** 设计使 MLA 的角色更纯粹：全局内容检索。

### 2. Full-Rank Output Gate

将低秩输出门改为与 KDA 一致的 full-rank 参数化：

```
y_t = W_o · [Sigmoid(W_g·x_t) ⊙ õ_t]
```

其中 W_g 为 full-rank 投影矩阵，使每个 token 能够以更高的容量调制从全局 attention 读取的通道。

### 3. FP32 Attention 输出修正

为解决 flash attention 中的 **有偏舍入误差**，训练期间将 attention 输出保持为 FP32：

- 这使得 on-chip 输出 tile 内存翻倍
- 通过重新设计 training kernel，将输出 tile 与 KV staging buffers 重叠（而非 query tile）
- 释放 shared memory 用于更深的 KV pipeline，提高训练吞吐

## Gated MLA vs 原始 MLA

| 维度 | 原始 MLA (DeepSeek-V2) | Gated MLA (Kimi K3) |
|------|----------------------|---------------------|
| 位置编码 | 通常有 RoPE | NoPE |
| 输出门 | 低秩或无 | Full-rank input-dependent |
| 训练精度 | BF16/FP8 | FP32 attention 输出 |
| 角色 | 主要注意力层 | 定期全局交互层（每 4 层 1 次） |

## 在混合架构中的角色

Gated MLA 在 Kimi K3 中作为 **定期全局注意力层**：
- 每个 block（3 KDA + 1 Gated MLA）中的第 4 层
- 提供 KDA 线性层无法实现的 token-to-token 全局交互
- 总布局：**69 KDA + 24 MLA + 1 末端 Gated MLA = 94 attention layers**
