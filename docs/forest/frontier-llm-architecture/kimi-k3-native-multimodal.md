---
forest: flm
tree: 架构设计
branch: 多模态能力
title: Kimi K3 原生多模态架构
version: 1.0.0
created: 2026-07-29
updated: 2026-07-29
description: Kimi K3 的 MoonViT-V2 视觉编码器及其原生多模态训练策略——从零开始训练、pixel shuffle 压缩和视觉-语言联合优化。
keywords:
  - MoonViT-V2
  - native multimodal
  - vision encoder
  - pixel shuffle
  - from-scratch training
  - Kimi K3
refs:
  - "[flm] DeepSeek-V4 文本专精定位 | 对比性纯文本策略"
---

# Kimi K3 原生多模态架构

## 概述

Kimi K3 采用**原生多模态**设计——文本、图像和视频由单一共享 backbone 在同一上下文中处理，无需后置模态对齐阶段。这为长程 vision-in-the-loop 行为提供了架构基础。

## MoonViT-V2

### 架构规格

- 27 层 Vision Transformer
- 约 0.4B 参数
- 采用 RMSNorm，移除所有 linear 和 attention 投影中的 bias 项
- 图像和视频共享全部参数（类似 MoonViT-3D）

### 注意力分解

- **Intra-frame spatial attention**：帧内空间注意力
- **Inter-frame temporal attention**：帧间时序注意力
- **Temporal pooling**：沿时间维度进一步压缩 token

### Pixel Shuffle 压缩

在投影到 LLM 之前，使用 2×2 downsampling 的 **pixel shuffle 操作**将视觉 token 数量减少 4 倍。这使得最高 3584×3584 像素的输入在 1M token 上下文内可行。

## 从零开始训练的关键发现

与 Kimi K2.5（使用 SigLIP 初始化的 MoonViT-3D）不同，Kimi K3 的 MoonViT-V2 完全从零开始训练：

| 策略 | 梯度稳定性 | 训练效率 | 最终性能 |
|------|:---:|:---:|:---:|
| SigLIP 初始化 (MoonViT-3D) | 频繁 spike | 不稳定 | 基准 |
| From-scratch (MoonViT-V2) | 稳定低 norm | 稳定 | 匹配基线 |

**结论**：在大规模多模态语言模型中，对比预训练（contrastive pre-training）作为视觉编码器初始化不是必需的——next-token prediction 从零训练即可匹配对比预训练的性能，且训练更稳定。

## 原生多模态训练

视觉和文本 token 在单一 next-token prediction 目标下交错训练，共享 backbone 从一开始就学习统一的多模态表示。
