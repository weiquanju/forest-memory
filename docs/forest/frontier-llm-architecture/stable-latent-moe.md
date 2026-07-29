---
forest: flm
tree: 架构设计
branch: MoE架构
title: StableLatentMoE 在 Kimi K3 中的设计
version: 1.0.0
created: 2026-07-29
updated: 2026-07-29
description: Kimi K3 的 StableLatentMoE 架构——896 个路由专家的极稀疏设计，包含 Normalized LatentMoE、SiTU-GLU 激活函数和 QuantileBalancing 负载均衡。
keywords:
  - StableLatentMoE
  - LatentMoE
  - SiTU-GLU
  - QuantileBalancing
  - Kimi K3
  - 896 experts
refs:
  - "[flm] DeepSeekMoE 在 DeepSeek-V4 中的架构演进 | MoE架构对比"
  - "[flm] MoE 路由策略对比 | 路由机制交叉分析"
---

# StableLatentMoE 在 Kimi K3 中的设计

## 概述

Kimi K3（2.8T/104B activated）采用 StableLatentMoE 架构，将路由专家池扩展到 896 个，每 token 激活 16 个，对应 **56 倍稀疏度**。通过 Latent Space 设计将专家宽度与模型全宽度解耦，实现在不显著增加通信开销的情况下扩大专家池。

## 核心组件

### Latent Space 设计

继承自 LatentMoE（Anonymous, 2025; 截至 2026-07 仍处于双盲审稿匿名状态，Kimi K3 报告引用为 [32]），核心思想是：

- **共享专家**：在全宽度路径上运行（每层固定 2 个）
- **路由专家**：在紧凑的 latent space（维度 ℓ = 3584，即 0.5× hidden dim）中运行

路由路径：`x → W↓ → z ∈ R^ℓ → Expert_i(z) → Aggregate → W↑ → y`

### Normalized LatentMoE

在专家聚合与上投影之间插入 **RMSNorm**，解决 routed branch 对 scale variation 的敏感性：

```
u = Σ p_i · E_i^{routed}(W↓x)
y = Σ E_j^{shared}(x) + W↑ · RMSNorm(u)
```

该归一化不仅稳定训练，还持续改善 validation loss 和下游 benchmark。

### SiTU-GLU 激活函数

为解决原始 LatentMoE 中 routed path 的激活爆炸问题，提出 **SigmoidTanhUnit GLU（SiTU-GLU）**：

- Gate branch：`β₁·tanh(W_g·x/β₁) ⊙ Sigmoid(W_g·x)`，β₁=4
- Up branch：`β₂·tanh(W_u·x/β₂)`，β₂=25

SiTU-GLU 在原点附近保持 SwiGLU 的线性响应，而在大值处有界（上界 β₁β₂=100），解决了 SwiGLU 无界导致的激活溢出风险。

### QuantileBalancing (QB)

针对 896 专家池的负载均衡挑战，提出基于分位数的负载均衡方法：

- 目标负载：q = mk/n（m tokens, n experts, Top-k selection）
- 对每个 expert j，计算 margins s_{:,j} - α^(t) 的 (1-k/n)-分位数作为新 bias
- 使用 **histogram estimation** 近似分位数，通过 all-reduce 汇总 bin counts
- 通信成本仅为每个 expert 几百个 bins

QB 使每个 expert 在单个 forward pass 后即可精确匹配目标负载，解决了 auxiliary-loss-based 方法在极稀疏场景下的失效问题。

## 架构规格对比（Kimi K2 vs K3）

| 参数 | Kimi K2 | Kimi K3 |
|------|---------|---------|
| 总参数 | 1.04T | 2.78T |
| 激活参数 | 32.6B | 104.2B |
| 路由专家数 | 384 | 896 |
| 每 token 激活 | 8 | 16 |
| 共享专家 | 1 | 2 |
| 激活函数 | SwiGLU | SiTU-GLU |
| 训练上下文 | 128K | 1M |
| 注意力机制 | MLA | Hybrid KDA-MLA |

## 参考文献

- Anonymous, 2025. LatentMixture-of-Experts.
- DeepSeek-AI, 2024. DeepSeekMoE.
