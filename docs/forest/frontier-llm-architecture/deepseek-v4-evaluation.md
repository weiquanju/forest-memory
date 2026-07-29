---
forest: flm
tree: 评估与能力
branch: 基准评测
title: DeepSeek-V4 评测结果
version: 1.0.0
created: 2026-07-29
updated: 2026-07-29
description: DeepSeek-V4 系列在知识、推理、Agent 和长上下文四个维度的基准评测结果——Pro-Max 模式对标 GPT-5.4、Gemini-3.1-Pro。
keywords:
  - benchmark evaluation
  - DeepSeek-V4
  - knowledge benchmark
  - reasoning benchmark
  - agent benchmark
  - long-context benchmark
refs:
  - "[flm] Kimi K3 评测结果 | 对比性评测"
  - "[flm] 长上下文效率对比 | 效率维度分析"
---

# DeepSeek-V4 评测结果

## 知识（Knowledge）

| 基准 | DeepSeek-V4-Pro-Max 表现 |
|------|------------------------|
| SimpleQA | 显著领先 open-source 模型 |
| Chinese-SimpleQA | 显著领先 open-source |
| MMLU-Pro | 与 open-source 持平 |
| HLE | 边际领先 open-source |
| GPQA | 边际领先 open-source |

整体：**缩小与 Gemini-3.1-Pro 的差距**，但仍略微落后。

## 推理（Reasoning）

- **优于** GPT-5.2 和 Gemini-3.0-Pro
- **略微落后** GPT-5.4 和 Gemini-3.1-Pro
- 估计落后前沿约 **3-6 个月**

### Flash 模型
DeepSeek-V4-Flash-Max 在 Complex Reasoning 上达到 GPT-5.2/Gemini-3.0-Pro 相当水平——以更少的参数（13B activated）实现高性价比推理架构。

## Agent

| 基准 | Pro-Max 表现 |
|------|------------|
| 公开基准 (SWE-Bench, Terminal-Bench 等) | 与 Kimi-K2.6, GLM-5.1 持平 |
| 内部评估 | 超越 Claude Sonnet 4.5，接近 Opus 4.5 |

## 长上下文

在 1M token context 窗口下：
- 合成和实际用例的 strong results
- 学术基准上**超越 Gemini-3.1-Pro**

## DeepSeek-V4-Flash-Base 亮点

预训练后（Base model）即：
- 在多数 benchmark 上超越 DeepSeek-V3.2-Base
- 以更高效的参数设计实现（284B total / 13B activated）

## 内部评估基准集

- Apex Shortlist (Pass@1)
- Codeforces (Rating)
- SWE Verified (Resolved)
- Terminal Bench 2.0 (Acc)
- Toolathlon (Pass@1)
