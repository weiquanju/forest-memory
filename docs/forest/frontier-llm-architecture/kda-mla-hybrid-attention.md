---
forest: flm
tree: 架构设计
branch: 注意力机制
title: KDA/MLA 混合注意力架构
version: 1.0.0
created: 2026-07-29
updated: 2026-07-29
description: Kimi K3 的 Hybrid KDA-MLA 注意力架构——3:1 交错的线性-全局注意力混合策略及其设计理由。
keywords:
  - hybrid attention
  - KDA/MLA interleaving
  - linear attention
  - global attention
  - Kimi K3
refs:
  - "[flm] KDA——Kimi Delta Attention | KDA 核心机制"
  - "[flm] Gated MLA 在 Kimi K3 中 | MLA 核心机制"
  - "[flm] CSA/HCA 混合注意力架构 | 竞争性混合策略对比"
---

# KDA/MLA 混合注意力架构

## 设计理念

Kimi K3 的注意力架构围绕**三个维度的信息流缩放**设计：
- **序列维度**：KDA 提供高效的 long-sequence mixing（线性复杂度）
- **深度维度**：Attention Residuals 提供跨层信息访问
- **宽度维度**：Stable LatentMoE 提供稀疏 channel mixing

其中，Hybrid KDA-MLA 负责序列维度的信息流。

## 3:1 混合比例

每个 Transformer block 包含 **3 个 KDA 层 + 1 个 Gated MLA 层**：

```
Block_n:
  KDA Layer 1  ← linear attention (position-sensitive, recency-aware)
  KDA Layer 2  ← linear attention
  KDA Layer 3  ← linear attention
  Gated MLA    ← global attention (unrestricted token-to-token interaction)
```

骨架末端额外增加 1 个 Gated MLA 层，确保最终输出始终经过全局 attention。

**总布局**：69 KDA + 24 MLA + 1 末端 MLA = 94 attention layers

## 两种注意力的分工

| 维度 | KDA（线性注意力） | Gated MLA（全局注意力） |
|------|-----------------|---------------------|
| **复杂度** | O(n) | O(n²) |
| **状态** | 固定大小 recurrent state S | 增长式 KV cache c_t |
| **位置信息** | 隐式（通过 decay gating） | NoPE（无显式位置编码） |
| **核心能力** | 高效长序列处理、recency bias | 不受限制的 token 间全局交互 |
| **瓶颈** | 遗忘旧信息的风险 | 长序列下 KV cache 膨胀 |
| **占比** | 73%（69/94 层） | 27%（25/94 层） |

## 位置编码关注分离

KDA 使用 NoPE——位置信息隐式地通过 recurrent gating 和 decay 机制编码。KDA 的 channel-wise α_t 决定了 token 在序列中的"持久性"。

MLA 也使用 NoPE——让 KDA 层负责序列位置感知，MLA 专注于内容驱动的全局交互。这种分离避免了：
- 调整 RoPE 频率基
- 应用 YaRN 插值
- 修改位置编码参数以适应上下文扩展

## 与 CSA/HCA 混合架构的对比

| 维度 | DeepSeek-V4 (CSA/HCA) | Kimi K3 (KDA/MLA) |
|------|---------------------|-------------------|
| **线性+全局混合** | CSA(压缩+稀疏) + HCA(压缩+稠密) | KDA(delta-rule线性) + MLA(latent全局) |
| **压缩比例** | 4× / 128× | N/A（固定 state size） |
| **KV cache 下限** | 约 2% of GQA8 baseline | 仅 MLA 层有 KV cache |
| **稀疏选择** | Lightning Indexer Top-k | N/A（KDA 无 sparsity） |
| **混合策略** | 层间交错（未公布具体比例） | 3:1 block 内交错 |
