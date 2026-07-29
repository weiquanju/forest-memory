---
forest: flm
title: 前沿大模型技术架构
version: 1.0.0
created: 2026-07-29
updated: 2026-07-29
description: 基于 DeepSeek-V4 与 Kimi K3 技术报告的前沿 LLM 架构知识森林——覆盖 MoE 架构、注意力机制、训练方法论、基础设施和评估体系的系统性对比分析。
source: "[DSv4] DeepSeek-V4: Towards Highly Efficient Million-Token Context Intelligence (arXiv:2606.19348v1) | [K3] Kimi K3: Open Frontier Intelligence Technical Report"
refs:
  - "[mke] 知识领域森林理论 | 森林组织方法论"
  - "[mke] 知识原子规范 | Leaf 格式规范"
  - "[mke] 单一职责与引用机制 | 跨森林引用格式"
---

# 前沿大模型技术架构

## 定位

本森林从两份 2025-2026 年的前沿 LLM 技术报告中系统性提取、组织和对比关键架构知识——**DeepSeek-V4**（DeepSeek-AI）和 **Kimi K3**（Moonshot AI）——覆盖模型架构设计、注意力机制创新、训练方法论、基础设施和评估体系五大维度，并提供跨模型的技术路线对比分析。

两份报告代表了当前 LLM 前沿的两条不同技术路线：
- **压缩范式**（DeepSeek-V4）：通过 CSA/HCA 压缩 KV cache 序列长度，在标准 attention 框架内突破 O(n²) 瓶颈
- **状态范式**（Kimi K3）：通过 KDA delta-rule recurrence 用固定大小 state 替代 KV cache，拥抱线性 attention

## 森林结构概览

```
flm (前沿大模型技术架构)
├── 树1: 架构设计 (Architecture Design)          [13 叶]
│   ├── MoE架构 (3 叶): DeepSeekMoE / StableLatentMoE / 路由对比
│   ├── 注意力机制 (6 叶): CSA / HCA / CSA-HCA混合 / KDA / Gated MLA / KDA-MLA混合
│   ├── 残差连接创新 (2 叶): mHC / AttnRes
│   └── 多模态能力 (2 叶): K3原生多模态 / DSv4文本专精
├── 树2: 训练方法论 (Training Methodology)       [8 叶]
│   ├── 优化器设计 (2 叶): Muon / Per-Head Muon
│   ├── 预训练策略 (3 叶): DSv4预训练 / K3预训练+ScalingLaw / 长上下文扩展对比
│   └── 后训练管线 (3 叶): DSv4后训练 / K3后训练 / 技术路线对比
├── 树3: 基础设施 (Infrastructure)               [6 叶]
│   ├── 训练框架 (2 叶): DSv4训练 / K3训练
│   ├── 推理框架 (2 叶): DSv4推理 / K3推理
│   └── 分布式策略 (2 叶): DSv4并行 / K3并行
├── 树4: 评估与能力 (Evaluation & Capabilities)  [3 叶]
│   ├── 基准评测 (2 叶): DSv4评测 / K3评测
│   └── 效率分析 (1 叶): 长上下文效率对比
└── 树5: 技术对比与趋势 (Comparison & Trends)    [4 叶]
    ├── 架构哲学分歧 (2 叶): 注意力哲学 / MoE路径
    ├── 技术趋势 (1 叶): 2025-2026趋势总结
    └── 迭代修正 (1 叶): 引用审计报告
```

**总计：5 棵树，34 片叶子（含 1 片审计叶子）**

## 森林内文档

### 树 1：架构设计

#### MoE 架构

| 文档 | 说明 |
|------|------|
| [DeepSeekMoE 在 DeepSeek-V4 中的架构演进](deepseek-moe-architecture.md) | DSv4 的 DeepSeekMoE 架构调整——Hash Routing、Sqrt(Softplus) 激活、auxiliary-loss-free |
| [StableLatentMoE 在 Kimi K3 中的设计](stable-latent-moe.md) | K3 的 896 专家极稀疏 MoE——Normalized LatentMoE、SiTU-GLU、QuantileBalancing |
| [MoE 路由策略对比](moe-routing-comparison.md) | Hash Routing + auxiliary-loss-free vs QuantileBalancing——两种路由哲学 |

#### 注意力机制

| 文档 | 说明 |
|------|------|
| [CSA——压缩稀疏注意力](csa-compressed-sparse-attention.md) | DSv4 CSA 机制详解——KV 压缩、Lightning Indexer、Shared KV MQA |
| [HCA——重度压缩注意力](hca-heavily-compressed-attention.md) | DSv4 HCA 机制——128× 极压缩率、稠密 MQA |
| [CSA/HCA 混合注意力架构](csa-hca-hybrid-attention.md) | DSv4 的 CSA/HCA 交错混合策略与效率分析 |
| [KDA——Kimi Delta Attention](kda-kimi-delta-attention.md) | K3 的 delta-rule 线性注意力——channel-wise forget gate、lower-bounded decay |
| [Gated MLA 在 Kimi K3 中](gated-mla-kimi-k3.md) | K3 对 MLA 的改进——NoPE、Full-Rank Gate、FP32 精度修正 |
| [KDA/MLA 混合注意力架构](kda-mla-hybrid-attention.md) | K3 的 3:1 KDA/MLA 混合策略——线性+全局注意力的分工设计 |

#### 残差连接创新

| 文档 | 说明 |
|------|------|
| [mHC——流形约束超连接](mhc-manifold-hyper-connections.md) | DSv4 的 Birkhoff 多面体约束残差——Sinkhorn-Knopp 投影、非扩展性保证 |
| [AttnRes——注意力残差](attnres-attention-residuals.md) | K3 的深度注意力残差——pseudo-query 选择性检索前驱层 |

#### 多模态能力

| 文档 | 说明 |
|------|------|
| [Kimi K3 原生多模态架构](kimi-k3-native-multimodal.md) | K3 的 MoonViT-V2 从零训练、pixel shuffle 压缩、原生多模态 |
| [DeepSeek-V4 的文本专精定位](deepseek-v4-text-only-positioning.md) | DSv4 的纯文本架构定位及其与多模态路线的对比 |

### 树 2：训练方法论

#### 优化器设计

| 文档 | 说明 |
|------|------|
| [Muon 优化器在 DeepSeek-V4 中](muon-optimizer-deepseek-v4.md) | DSv4 的 Hybrid Newton-Schulz Muon + ZeRO 混合策略 |
| [Per-Head Muon 在 Kimi K3 中](per-head-muon-kimi-k3.md) | K3 的 head-wise 正交化 Muon——均衡各 head 更新尺度 |

#### 预训练策略

| 文档 | 说明 |
|------|------|
| [DeepSeek-V4 预训练数据与配置](deepseek-v4-pretraining.md) | DSv4 的 32T+ tokens 数据构建与 Flash/Pro 模型配置 |
| [Kimi K3 预训练与 Scaling Law](kimi-k3-pretraining-scaling-law.md) | K3 的 2.5× scaling efficiency 提升与 Cosine Decay 选择 |
| [长上下文扩展策略对比](long-context-extension-comparison.md) | Partial RoPE vs NoPE + 渐进式 curriculum——两种位置编码哲学 |

#### 后训练管线

| 文档 | 说明 |
|------|------|
| [DeepSeek-V4 后训练管线](deepseek-v4-post-training.md) | DSv4 的 Specialist Training + On-Policy Distillation + FP4 QAT |
| [Kimi K3 后训练管线](kimi-k3-post-training.md) | K3 的 3 域 × 3 努力 RL + MOPD + 7 种 RL 环境 |
| [后训练技术路线对比](post-training-comparison.md) | Specialist-First vs Multi-Domain Unified——两种后训练范式 |

### 树 3：基础设施

#### 训练框架

| 文档 | 说明 |
|------|------|
| [DeepSeek-V4 训练基础设施](deepseek-v4-training-infra.md) | DSv4 的细粒度 EP、TileLang DSL、批次不变内核库 |
| [Kimi K3 训练基础设施](kimi-k3-training-infra.md) | K3 的 FlashKDA、KCP、MoonEP、Co-located RL 系统 |

#### 推理框架

| 文档 | 说明 |
|------|------|
| [DeepSeek-V4 推理优化](deepseek-v4-inference-infra.md) | DSv4 的异构 KV Cache 管理、On-Disk 存储、Prefix Caching |
| [Kimi K3 推理基础设施](kimi-k3-inference-infra.md) | K3 的 KDA Prefix Caching、EAGLE-3 Draft Model、推测解码 |

#### 分布式策略

| 文档 | 说明 |
|------|------|
| [DeepSeek-V4 分布式并行策略](deepseek-v4-distributed-strategy.md) | DSv4 的 Wave-Based EP、Muon ZeRO、CP for CSA/HCA |
| [Kimi K3 分布式并行策略](kimi-k3-distributed-strategy.md) | K3 的 KCP、PP×EP×DP 三维并行、1M RL 系统 |

### 树 4：评估与能力

#### 基准评测

| 文档 | 说明 |
|------|------|
| [DeepSeek-V4 评测结果](deepseek-v4-evaluation.md) | DSv4 的 Knowledge/Reasoning/Agent/Long-Context 评测 |
| [Kimi K3 评测结果](kimi-k3-evaluation.md) | K3 的 Coding/Agent/Knowledge/Vision 评测——开源前沿 |

#### 效率分析

| 文档 | 说明 |
|------|------|
| [长上下文效率对比](long-context-efficiency-comparison.md) | 1M 上下文下 FLOPs、KV Cache 和 Memory 定量对比 |

### 树 5：技术对比与趋势

#### 架构哲学分歧

| 文档 | 说明 |
|------|------|
| [注意力设计哲学分歧](attention-philosophy-divergence.md) | 稀疏选择（CSA/HCA）vs 线性递归（KDA）——两大阵营 |
| [MoE 规模化路径对比](moe-scaling-path-comparison.md) | Full-width fine-grained vs Latent Space extreme sparsity |

#### 技术趋势

| 文档 | 说明 |
|------|------|
| [前沿 LLM 技术趋势总结](frontier-llm-technical-trends.md) | 2025-2026 七大技术趋势——1M 上下文、MoE 极限稀疏、RL 后训练等 |

#### 迭代修正

| 文档 | 说明 |
|------|------|
| [引用真实性审计报告](citation-audit-report.md) | Step 5 引用审计——13 篇外部引用验证、4 处修正、0 虚构引用，引用真实率 100% |

## 核心原则

### 单一职责
每片叶子只阐述一个核心概念。跨模型的知识被组织在"对比"叶子中（如 `attention-philosophy-divergence.md`），而非在同一叶子中混述两个模型。

### 交叉声明检测
合并为同一森林的核心价值——两份报告在相同问题上提出不同方案（CSA vs KDA、mHC vs AttnRes、GRPO vs MOPD），森林内的 cross-reference 机制使这些"竞争性声明"可被系统对比。

### 引用真实性
所有技术主张均来自原始技术报告，标注了原始论文引用。已完成 Step 5 引用审计（详见 [citation-audit-report.md](citation-audit-report.md)）：13 篇外部引用中 8 篇经 arxiv-mcp-server 直接验证，0 篇虚构引用。4 处引用已做元数据修正（Jordan 2024 标注为博客源、KDA 关联到 Kimi Linear arXiv:2510.26692、LatentMoE/AttnRes 标注匿名审稿状态）。
