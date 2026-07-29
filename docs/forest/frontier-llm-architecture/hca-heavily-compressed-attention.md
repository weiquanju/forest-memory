---
forest: flm
tree: 架构设计
branch: 注意力机制
title: HCA——重度压缩注意力
version: 1.0.0
created: 2026-07-29
updated: 2026-07-29
description: DeepSeek-V4 的 Heavily Compressed Attention (HCA) 机制——极高压缩率下的 KV Cache 管理方案，与 CSA 形成"轻量压缩+稀疏选择 vs 重度压缩+稠密注意力"的互补设计。
keywords:
  - HCA
  - Heavily Compressed Attention
  - extreme KV compression
  - MQA
  - DeepSeek-V4
refs:
  - "[flm] CSA——压缩稀疏注意力 | 配合使用的轻量压缩方案"
  - "[flm] CSA/HCA 混合注意力架构 | 在完整架构中的角色"
---

# HCA——重度压缩注意力

## 概述

HCA（Heavily Compressed Attention）采用比 CSA 更激进的压缩策略（m' ≫ m），但不使用稀疏注意力。它将每 m' 个 token 的 KV cache 压缩为 1 个条目，然后对所有压缩条目执行稠密的 Multi-Query Attention。

## 核心流程

### KV 压缩（无重叠）

与 CSA 的双套 KV 不同，HCA 使用更简洁的单套压缩：

```
C = H·W_KV,  Z = H·W_Z    ∈ R^(n×c)
```

压缩时不使用重叠窗口，每 m' 个 token 独立压缩：

```
S_{m'i:m'(i+1)-1} = Softmax_row(Z_{m'i:m'(i+1)-1} + B)
C^Comp_i = Σ_j S_j ⊙ C_j
```

有效压缩率：1/m'（m' = 128，远大于 CSA 的 m = 4）

### Shared Key-Value MQA

HCA 与 CSA 共享相同的 MQA 机制和 Grouped Output Projection 策略：

```
c^Q_t = h_t · W_DQ                      # 低秩压缩
q_{t,1..n_h} = c^Q_t · W_UQ             # 上投影
o_{t,i} = CoreAttn(q_{t,i}, C^Comp, C^Comp)  # MQA
```

### 分组输出投影

与 CSA 相同的 g 组输出投影策略，减少大维度投影的计算开销。

## 补充技术

- **Partial RoPE**：与 CSA 相同
- **Sliding Window**：与 CSA 相同，保留 n_win 个最近 token
- **Attention Sink**：与 CSA 相同

## CSA vs HCA 设计对比

| 维度 | CSA | HCA |
|------|-----|-----|
| **压缩率** | 1/m (= 1/4) | 1/m' (= 1/128) |
| **注意力模式** | 稀疏（Top-k 选择） | 稠密（全量压缩条目） |
| **压缩策略** | 双套 KV + 重叠窗口 | 单套 KV + 无重叠 |
| **Indexer 开销** | 有（Lightning Indexer） | 无 |
| **适用场景** | 需要精细 token 级选择 | 全局上下文聚合 |
| **KV Cache 大小** | 中等 | 极小 |

## 效率收益

在 1M 上下文场景下，HCA 层的 KV cache 大小相比标准 GQA8（head dim=128）可缩减至约 **2%**。配合 FP8/BF16 混合精度存储（RoPE 维度用 BF16，其余用 FP8），KV cache 相比纯 BF16 减少近一半。

## Flash 配置

| 参数 | 值 |
|------|-----|
| 压缩率 m' | 128 |
| Query head 数 n_h | 64 |
| Head dim c | 512 |
| 输出分组数 g | 8 |
