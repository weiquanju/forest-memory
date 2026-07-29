---
forest: flm
tree: 基础设施
branch: 推理框架
title: DeepSeek-V4 推理优化
version: 1.0.0
created: 2026-07-29
updated: 2026-07-29
description: DeepSeek-V4 的推理基础设施——异构 KV Cache 管理（State Cache + 经典 KV Cache）、On-Disk 存储和共享前缀复用策略。
keywords:
  - inference optimization
  - KV cache management
  - on-disk storage
  - prefix caching
  - DeepSeek-V4
refs:
  - "[flm] Kimi K3 推理基础设施 | 对比性推理框架"
  - "[flm] DeepSeek-V4 训练基础设施 | 训练侧基础设施"
---

# DeepSeek-V4 推理优化

## 异构 KV Cache 结构

### 两类 Cache

| Cache 类型 | 内容 | 特点 |
|-----------|------|------|
| **State Cache** | SWA KV + CSA/HCA 未压缩 tail tokens | 固定大小，按请求预分配 |
| **经典 KV Cache** | CSA/HCA 已压缩 KV entries | 多 block per request，可变大小 |

### Block 设计
每 cache block 覆盖 `lcm(m, m')` 个原始 token：
- CSA 压缩 token 数：k₁ = lcm(m, m') / m
- HCA 压缩 token 数：k₂ = lcm(m, m') / m'

### 两大挑战
1. **多样化 Cache 策略**：SWA 的滑动窗口策略与压缩 branch 的块压缩策略不同
2. **高性能 Attention Kernel 约束**：对齐要求限制了 cache 布局灵活性

### 解决方案
- **State Cache**：将 SWA + 未压缩 tail 视为 state-space model → 预分配固定大小池
- **Sparse Attention Kernel Co-Design**：与 kernel 协同设计 cache 布局，支持不同层可变 token per block

## On-Disk KV Cache 存储

### CSA/HCA 存储
- 全部压缩 KV entries 写盘
- 命中前缀时读取直到最后一个完整压缩块
- Tail 不完整块需重计算

### SWA 存储（三种策略）

| 策略 | 存储开销 | 计算开销 | 适用场景 |
|------|:---:|:---:|------|
| **Full SWA Caching** | 高（全量） | 零 | 写密集型 SSD 不平衡 |
| **Periodic Checkpointing** | 可调 | 可调 | 灵活 trade-off |
| **Zero SWA Caching** | 零 | 需重算最后 n_win·L tokens | 存储受限场景 |

## 混合精度存储

- RoPE 维度：BF16
- 其余维度：FP8（相比纯 BF16 减少近一半）
- Indexer attention：FP4
