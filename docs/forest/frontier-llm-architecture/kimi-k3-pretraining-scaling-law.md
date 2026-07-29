---
forest: flm
tree: 训练方法论
branch: 预训练策略
title: Kimi K3 预训练与 Scaling Law
version: 1.0.0
created: 2026-07-29
updated: 2026-07-29
description: Kimi K3 的预训练数据、Scaling Law 研究和训练配置——2.5× 整体缩放效率提升与 Cosine Decay 策略选择。
keywords:
  - pre-training
  - scaling law
  - cosine decay
  - Kimi K3
  - multimodal training
refs:
  - "[flm] DeepSeek-V4 预训练数据与配置 | 对比性预训练策略"
  - "[flm] 长上下文扩展策略对比 | 上下文扩展方法交叉分析"
---

# Kimi K3 预训练与 Scaling Law

## 预训练数据

四类文本域 + 大规模视觉语料：

- **Web Text**：规则+分类器质量评分+去重，域特定采样率经小模型消融确定
- **Code** 和 **Mathematics**：沿袭 Kimi K2 的 rephrasing recipe（风格/视角多样的 prompt → chunk-wise autoregressive generation → fidelity verification）
- **Knowledge**：同上 rephrasing
- **Vision**：captions、interleaved image-text、OCR、perception、video、visual coding；programmatic multimodal data 大规模扩展（SVG/3D/Webpage/Game/CAD）

## Scaling Law 研究

### 关键发现

相比 Kimi K2，Kimi K3 的架构/数据/训练综合改进产生 **约 2.5× 的 scaling efficiency 提升**——即在相同 FLOPs 下达到更低 validation loss。

### Cosine Decay vs WSD

- 对两种学习率调度分别做独立 scaling law search
- **Cosine Decay 在各自最优超参数下始终优于 WSD**（Warmup Stable Decay）
- 此前 WSD 被报告可匹敌 cosine decay 可能是由于共用非最优超参数导致的不公平比较

### 训练配置

- **优化器**：Per-Head Muon + weight clipping
- **学习率调度**：Cosine decay with 1% linear warmup
- **Weight decay**：0.1
- **MoE 负载均衡**：QuantileBalancing (QB)
- **训练策略**：原生多模态联合训练（视觉和文本 token 从一开始就交错）

## 长上下文扩展

四阶段渐进式 curriculum：
- Pre-training：8K → 64K
- Cooldown：256K → 1M

将昂贵的长序列计算集中在训练预算的小部分，既经济又保证模型逐步适应长程依赖。
