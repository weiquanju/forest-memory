---
forest: flm
tree: 评估与能力
branch: 效率分析
title: 长上下文效率对比——FLOPs 与 KV Cache
version: 1.0.0
created: 2026-07-29
updated: 2026-07-29
description: 定量对比 DeepSeek-V4 和 Kimi K3 在 1M token 上下文下的推理效率——FLOPs、KV Cache 大小和内存占用。
keywords:
  - long-context efficiency
  - FLOPs comparison
  - KV cache comparison
  - 1M token context
refs:
  - "[flm] DeepSeek-V4 评测结果 | DSv4 评测"
  - "[flm] Kimi K3 评测结果 | K3 评测"
  - "[flm] CSA/HCA 混合注意力架构 | DSv4 效率机制"
  - "[flm] KDA/MLA 混合注意力架构 | K3 效率机制"
---

# 长上下文效率对比

## 1M Token 上下文——定量对比

### DeepSeek-V4（相对 V3.2）

| 指标 | Pro | Flash |
|------|:---:|:---:|
| Single-token FLOPs | 27% of V3.2 | 10% of V3.2 |
| KV Cache Size | 10% of V3.2 | 7% of V3.2 |

### 相对标准 GQA8 基线

DeepSeek-V4 的 KV cache ≈ **2%** of BF16 GQA8 (head dim=128) baseline @ 1M context。

### Kimi K3

K3 报告中未提供类似 DSv4 的 FLOPs/KV cache 定量对比，但架构特征暗示不同的效率足迹：

| 维度 | DeepSeek-V4 | Kimi K3 |
|------|------------|---------|
| KV Cache 类型 | 压缩式（reduce length） | 固定大小状态（KDA layers）+ 仅 MLA 层有 KV cache |
| 1M KV Cache 下限 | ~2% of GQA8 baseline | KDA 层 O(1)，MLA 层仍随序列增长 |
| Flash 模型 1M FLOPs | 10% of V3.2 | 未公布 |
| 精度策略 | BF16 + FP8 + FP4 (indexer) | MXFP4 + MXFP8 (post-training) |

## 效率机制的哲学差异

### DeepSeek-V4：压缩长度

通过 CSA（4× 压缩 + Top-k sparse selection）和 HCA（128× 压缩 + dense attention）**减少 KV cache 的序列长度维度**。效率收益直接来自压缩率（m 和 m'）。

优势：与标准 attention 框架兼容，可在现有 sparse attention kernel 上运行。

### Kimi K3：消除长度依赖

KDA 用 **固定大小的 recurrent state** S ∈ R^(dk×dv) 完全替代 KV cache。仅 27% 的 MLA 层仍保留传统 KV cache。

优势：KDA 层的 memory 与序列长度完全解耦——1M context 和 1K context 的 state 大小相同。

劣势：需要全新的 kernel 设计（FlashKDA + KCP），与现有 attention 基础设施兼容性较低。

## 量化效率对比

| 效率维度 | DeepSeek-V4 | Kimi K3 |
|------|------------|---------|
| 单 token FLOPs（长上下文） | 极低（压缩减少计算） | KDA: O(dk·dv) 固定 |
| KV Cache / token | 压缩后 ~2% 基线 | KDA: 0, MLA: 低秩 latent |
| 内存下限 | 约 2% GQA8 | KDA 固定 O(1) + MLA 线性 |
| 硬件兼容 | 标准 attention kernel 可支持 | 需要 FlashKDA 等专用 kernel |
