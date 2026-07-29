---
forest: flm
tree: 技术对比与趋势
branch: 架构哲学分歧
title: MoE 规模化路径对比——细粒度共享路由 vs 潜在空间极限稀疏
version: 1.0.0
created: 2026-07-29
updated: 2026-07-29
description: DeepSeek-V4（fine-grained shared+routed MoE）与 Kimi K3（Latent Space extreme sparsity MoE）两种 MoE 规模化哲学的系统对比。
keywords:
  - MoE scaling
  - fine-grained experts
  - latent space
  - extreme sparsity
  - expert routing
refs:
  - "[flm] DeepSeekMoE 在 DeepSeek-V4 中的架构演进 | DSv4 MoE"
  - "[flm] StableLatentMoE 在 Kimi K3 中的设计 | K3 MoE"
  - "[flm] MoE 路由策略对比 | 路由机制对比"
---

# MoE 规模化路径对比

## 两种路径

### DeepSeek-V4：细粒度共享+路由 MoE

**核心策略**：在 full-width 空间中维持 shared + fine-grained routed experts 组合，通过 Hash Routing 和 auxiliary-loss-free 在适中稀疏度下平衡效率与容量。

- 路由专家数：256/层（Flash）
- 每 token 激活：6 个
- 稀疏度：2.3%
- 专家宽度：full hidden dim（2048 intermediate）

### Kimi K3：潜在空间极限稀疏 MoE

**核心策略**：将 routed expert 压缩到 Latent Space（0.5× hidden dim），以此换取极大的专家池规模和稀疏度。

- 路由专家数：896/层
- 每 token 激活：16 个
- 稀疏度：1.8%（56×）
- 专家宽度：latent dim 3584（0.5× 7168）

## 系统对比

| 维度 | DeepSeek-V4 | Kimi K3 |
|------|------------|---------|
| **专家空间** | Full-width (d) | Latent space (ℓ = d/2) |
| **专家数量** | 256 → 中等 | 896 → 极限 |
| **稀疏比** | 2.3%（中低） | 1.8%（极高，56×） |
| **共享专家** | 1/层 | 2/层（固定） |
| **路由机制** | auxiliary-loss-free + Hash | QuantileBalancing |
| **激活函数** | Sqrt(Softplus) | SiTU-GLU |
| **稳定性策略** | Sequence-wise balance loss | RMSNorm + SiTU boundedness |
| **通信开销** | Full-width dispatching | Half-width dispatching |

## 核心权衡

### 专家容量 vs 专家宽度

**DSv4** 选择**宽专家、少数量**——每个 routed expert 有 2048 维 intermediate FFN，有足够的容量学习复杂的 token 模式。

**K3** 选择**窄专家、多数量**——896 个 latent-space 专家 × 16 路激活 = 更多的专家组合，但每个专家容量减半。

### 扩展性边界

- DSv4 path：增加专家数 → 通信开销线性增长（full-width dispatching）
- K3 path：增加专家数 → 通信更可行（latent space），但 expert 容量瓶颈可能限制个体能力

### 负载均衡

- DSv4：中等稀疏度 + auxiliary-loss-free → 负载均衡相对简单
- K3：56× 稀疏度 → 需要 QuantileBalancing 精确匹配，histogram 近似在更大规模下可能面临精度挑战

## 共享专家角色

两者都用 shared experts 处理通用变换：
- DSv4：1 个共享专家/层
- K3：固定 2 个共享专家/层

K3 的 dual shared expert 设计暗示在极限稀疏下，更多共享容量有助于补充 routed experts 的信息损失。
