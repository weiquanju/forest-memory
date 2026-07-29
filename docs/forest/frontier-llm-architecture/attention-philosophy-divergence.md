---
forest: flm
tree: 技术对比与趋势
branch: 架构哲学分歧
title: 注意力设计哲学分歧——稀疏选择 vs 线性递归
version: 1.0.0
created: 2026-07-29
updated: 2026-07-29
description: DeepSeek-V4（CSA/HCA 压缩+稀疏选择）与 Kimi K3（KDA delta-rule 线性递归）在注意力机制设计上的根本哲学分歧及各自优劣。
keywords:
  - attention philosophy
  - sparse attention
  - linear attention
  - delta-rule
  - KV compression
refs:
  - "[flm] CSA——压缩稀疏注意力 | DSv4 方案"
  - "[flm] KDA——Kimi Delta Attention | K3 方案"
  - "[flm] 长上下文效率对比 | 效率维度"
---

# 注意力设计哲学分歧

## 两种路线

### DeepSeek-V4：保留 Attention 框架，压缩序列

**核心思路**：不改变 attention 的基本范式（Q·K^⊤·V），而是通过压缩输入来降低 O(n²)。

- **CSA**：4× 压缩 + Lightning Indexer Top-k 稀疏选择 → 精细化 token 选择
- **HCA**：128× 压缩 + Dense attention → 全局上下文聚合

**本质**：在 standard softmax attention 的框架内做"降采样"——压缩 KV cache 的序列长度，但仍保留 token-to-token 的精确 attention score 计算。

### Kimi K3：放弃 Token-to-Token Attention，转向 State Space

**核心思路**：用 recurrent state S 替代 KV cache，将 O(n²) 转换为 O(n) ——每一次推理只需要更新一个小型固定矩阵。

- **KDA**：delta-rule recurrence + channel-wise forget gate → 固定大小状态
- **MLA**：仅 27% 层保留全局 token-to-token attention

**本质**：放弃标准 attention，拥抱 state-space model 的线性复杂度范式。

## 对比分析

| 维度 | CSA/HCA（压缩范 paradigm） | KDA（状态范 paradigm） |
|------|--------------------------|----------------------|
| **理论基础** | Softmax Attention | Delta-Rule + Linear Recurrence |
| **复杂度** | O(n·n/m·k) ~ O(n²/m) | O(n·dk·dv) 固定 |
| **信息选择** | 显式 Token-Level（Top-k 选择） | 隐式 State-Level（forget gate 衰减） |
| **可解释性** | 高（可查看每个 query 关注哪些 token） | 低（状态混合了所有历史信息） |
| **硬件兼容** | 高（兼容 standard attention kernel） | 低（需要 FlashKDA/KCP 专用 kernel） |
| **长程依赖** | 受 sparse selection 精度限制 | 受 forget gate 衰减限制 |
| **推理 memory** | 压缩 KV cache（随序列增长） | 固定 recurrent state（序列无关） |

## 根本分歧

### "哪些 token 应该被关注？"

**CSA/HCA**：由 Lightning Indexer 显式计算每个 query 与所有压缩 KV block 的相关性 → Top-k 选择。选择是**稀疏的、显式的**。

**KDA**：由 channel-wise forget gate α_t 控制每个维度的信息保留 → 所有历史信息被混合到 state S 中。选择是**稠密的、隐式的**。

### "遗忘是 bug 还是 feature？"

**CSA/HCA**：遗忘（limited KV cache）是需要用工程手段（滑动窗口分支、sink tokens）弥补的问题。

**KDA**：遗忘（forget gate）是架构的核心设计特征——模型学习自己决定"记住什么、忘记什么"。

## 历史脉络

- CSA/HCA 路线继承自：DSA → GQA → MQA → Sparse Attention（开源社区主导）
- KDA 路线继承自：Linear Attention → Mamba → DeltaNet → Kimi Linear（学术界推动的"alternative to attention"运动）

两条路线代表了当前 LLM 社区在"如何突破 O(n²) attention"问题上的两大阵营。
