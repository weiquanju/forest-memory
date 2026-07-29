---
forest: flm
tree: 架构设计
branch: 注意力机制
title: CSA/HCA 混合注意力架构
version: 1.0.0
created: 2026-07-29
updated: 2026-07-29
description: DeepSeek-V4 系列中 CSA 与 HCA 的交错混合部署策略及其效率分析——如何在稀疏精度与全局覆盖之间取得平衡。
keywords:
  - hybrid attention
  - CSA/HCA interleaving
  - long-context efficiency
  - DeepSeek-V4
refs:
  - "[flm] CSA——压缩稀疏注意力 | CSA 核心机制"
  - "[flm] HCA——重度压缩注意力 | HCA 核心机制"
---

# CSA/HCA 混合注意力架构

## 设计动机

CSA 和 HCA 在精度-效率谱系上占据不同位置：
- **CSA**：压缩率低（m=4），通过稀疏 Top-k 选择保持精细的 token 级选择能力，但 KV cache 和 FLOPs 相对较高
- **HCA**：压缩率极高（m'=128），以牺牲精确 token 选择为代价换取极致的 KV cache 和计算效率

混合部署使两者优势互补。

## 层间交错策略

### DeepSeek-V4-Flash (43 层)
- **第 1-2 层**：纯 Sliding Window Attention（不使用压缩）
- **第 3-43 层**：CSA 和 HCA **交错部署**

### DeepSeek-V4-Pro (61 层)
- **第 1-2 层**：HCA（入口层即使用压缩）
- **第 3-61 层**：CSA 和 HCA **交错部署**

交错模式使得相邻层间信息处理方式交替变化，避免单一压缩策略的偏差累积。

## 混合精度存储

KV 条目采用**混合存储格式**：
- **RoPE 维度**：BF16 精度（保持位置编码精度）
- **其余维度**：FP8 精度（节省存储）
- Indexer 注意力计算：**FP4 精度**（进一步加速长上下文场景）

相比纯 BF16 存储，混合精度将 KV cache 大小减少约一半。

## 效率分析

### 1M 上下文场景

| 指标 | DeepSeek-V3.2 | DeepSeek-V4-Pro | 倍数 |
|------|:---:|:---:|:---:|
| Single-token FLOPs | 基准 | 27% | 3.7× lower |
| KV cache size | 基准 | 10% | 9.5× smaller |

Flash 模型效率更高：
- **1M context FLOPs**：仅为 V3.2 的 10%
- **1M context KV cache**：仅为 V3.2 的 7%

### 与标准 GQA8 对比

在 1M 上下文下，CSA/HCA 混合架构的 KV cache 大小约为标准 GQA8（head dim=128）的 **2%**。

## 设计权衡总结

| 维度 | 策略 | 效果 |
|------|------|------|
| 短-中文本效率 | 较小的 attention top-k | 减少不必要的稀疏选择开销 |
| 长文本效率 | CSA+HCA 混合 + 混合精度 | 线性级 KV cache 缩减 |
| 局部依赖 | Sliding Window 分支 | 保持细粒度局部建模 |
| 数值稳定 | RMSNorm Q/K + Attention Sink | 防止 logits 爆炸 |
