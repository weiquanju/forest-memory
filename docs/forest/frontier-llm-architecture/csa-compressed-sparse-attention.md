---
forest: flm
tree: 架构设计
branch: 注意力机制
title: CSA——压缩稀疏注意力
version: 1.0.0
created: 2026-07-29
updated: 2026-07-29
description: DeepSeek-V4 的 Compressed Sparse Attention (CSA) 机制详解——KV 压缩、Lightning Indexer 稀疏选择与 Shared KV MQA 的组合设计。
keywords:
  - CSA
  - Compressed Sparse Attention
  - KV compression
  - Lightning Indexer
  - sparse attention
  - DeepSeek-V4
refs:
  - "[flm] HCA——重度压缩注意力 | 配合使用的重度压缩方案"
  - "[flm] CSA/HCA 混合注意力架构 | 在完整架构中的角色"
  - "[flm] KDA——Kimi Delta Attention | 竞争性注意力方案对比"
---

# CSA——压缩稀疏注意力

## 概述

CSA（Compressed Sparse Attention）是 DeepSeek-V4 系列设计的两种高效注意力机制之一。它结合了 **KV 压缩**和**稀疏注意力**两种策略：先将每 m 个 token 的 KV cache 压缩为 1 个条目，然后使用 DeepSeekSparseAttention (DSA) 让每个 query 只关注 Top-k 个压缩后的 KV 条目。

## 核心流程

### 1. KV 压缩

对隐藏状态序列 H ∈ R^(n×d)，首先计算两套 KV 条目及其压缩权重：

```
C^a = H·W^a_KV,  C^b = H·W^b_KV   ∈ R^(n×c)
Z^a = H·W^a_Z,   Z^b = H·W^b_Z    ∈ R^(n×c)
```

每 m 个连续 token 的 KV 条目被压缩为一个（带重叠窗口）：

- 对第 i 个压缩块，使用 Softmax 归一化 2m 个压缩权重
- C^Comp_i = Σ_j S^a_j ⊙ C^a_j + Σ_j S^b_{j-m} ⊙ C^b_{j-m}
- 有效压缩率：1/m

### 2. Lightning Indexer 稀疏选择

压缩后，通过低秩 Indexer 选择 Top-k 个最相关的压缩 KV 块：

**低秩 Query 生成**：
```
c^Q_t = h_t · W_DQ                    # 压缩 query (d→d_c)
q^I_{t,1..n^I_h} = c^Q_t · W_I UQ     # 上投影为 indexer queries
```

**Index Score 计算**：
```
I_{t,s} = Σ_h w^I_{t,h} · ReLU(q^I_{t,h} · K^IComp_s)
```
其中 w^I 是各 indexer head 的可学习权重。

**Top-k 选择**: C^SprsComp_t = {C^Comp_s | I_{t,s} ∈ Top-k(I_{t,:})}

### 3. Shared Key-Value MQA

选中的稀疏 KV 条目在 Multi-Query Attention 模式下同时作为 key 和 value：

```
o_{t,i} = CoreAttn(query=q_{t,i}, key=C^SprsComp_t, value=C^SprsComp_t)
```

### 4. Grouped Output Projection

为减少 n_h 个 attention 输出直接投影到 d 维的计算开销，CSA 采用分组输出投影策略：
- 将 n_h 个 head 输出分为 g 组
- 每组先投影到较小维度 d_g（d_g < c·n_h/g）
- 再合并投影到最终 hidden state

## 补充技术

- **Partial RoPE**：仅对 query/KV 的尾部 64 维应用 RoPE，并在输出上施加逆位置 RoPE
- **Sliding Window 分支**：额外保留最近 n_win 个未压缩 KV 条目以增强局部依赖建模
- **Attention Sink**：使用可学习的 sink logits 避免注意力分数强制归一化为 1

## Flash 配置（DeepSeek-V4-Flash）

| 参数 | 值 |
|------|-----|
| 压缩率 m | 4 |
| Indexer head 数 n^I_h | 64 |
| Indexer head dim c_I | 128 |
| Attention top-k | 512 |
| Query head 数 n_h | 64 |
| Head dim c | 512 |
| Query 压缩维度 d_c | 1024 |
| 输出分组数 g | 8 |
| 分组中间维度 d_g | 1024 |
| Sliding Window n_win | 128 |
