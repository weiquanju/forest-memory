---
forest: flm
tree: 架构设计
branch: MoE架构
title: MoE 路由策略对比——Hash Routing vs QuantileBalancing
version: 1.0.0
created: 2026-07-29
updated: 2026-07-29
description: 对比 DeepSeek-V4 的 Hash Routing + auxiliary-loss-free 策略与 Kimi K3 的 QuantileBalancing 策略在路由机制设计上的哲学差异。
keywords:
  - MoE路由
  - Hash Routing
  - QuantileBalancing
  - auxiliary-loss-free
  - load balancing
refs:
  - "[flm] DeepSeekMoE 在 DeepSeek-V4 中的架构演进 | 基础架构"
  - "[flm] StableLatentMoE 在 Kimi K3 中的设计 | 对比架构"
---

# MoE 路由策略对比

## 两种路由哲学

### DeepSeek-V4：Hash Routing + Auxiliary-Loss-Free

**底层机制**：auxiliary-loss-free 策略（Wang et al., 2024a）通过动态调整 expert-wise bias 来维持负载均衡，无需辅助损失函数。

**Hash Routing 特化**：前几层采用基于 token ID 的确定性哈希路由，完全跳过学习过程，降低早期层的路由开销。

**关键特征**：
- 移除路由目标节点数约束，增加路由灵活性
- 辅以 sequence-wise balance loss 防止单序列内极端不均衡
- 适合中等稀疏度场景（6/256）

### Kimi K3：QuantileBalancing (QB)

**底层机制**：直接计算使得每个 expert 恰好收到 q 个 token 的 bias 值，通过 margins 的 (1-k/n)-分位数确定。

**关键特征**：
- 单次 forward pass 即可确定 bias，无需迭代调整
- 使用 histogram 近似全局分位数，通信成本极低
- 在极端稀疏场景（16/896 = 1.8% 激活率）下保持稳定

## 设计哲学对比

| 维度 | DeepSeek-V4 | Kimi K3 |
|------|------------|---------|
| **路由粒度** | 6/256 = 2.3% | 16/896 = 1.8% |
| **均衡策略** | 动态 bias + sequence-wise loss | 分位数精确匹配 |
| **计算开销** | 反向传播调整 bias | 单次 forward pass 统计 |
| **稀疏性挑战** | 中等 | 极高（56×） |
| **确定性路由** | 早期层 Hash（确定性）+ 后期学习 | 全部学习路由 |
| **适用场景** | 适度稀疏 + 工程简洁 | 极限稀疏 + 大规模专家池 |

## 核心分歧

1. **Hash Routing 的引入**：DeepSeek-V4 在早期层使用确定性路由，暗示在浅层 MoE 中路由学习可能收益有限
2. **量化均衡的精确性**：Kimi K3 的 QB 追求理论上精确的负载匹配（q = mk/n），而 DeepSeek-V4 更偏向启发式的 balance loss
3. **可扩展性边界**：QB 的设计明确针对 10³ 量级的专家池，其 histogram estimator 在更大规模下可能面临 bin 精度挑战
