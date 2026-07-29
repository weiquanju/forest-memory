---
forest: flm
tree: 基础设施
branch: 分布式策略
title: DeepSeek-V4 分布式并行策略
version: 1.0.0
created: 2026-07-29
updated: 2026-07-29
description: DeepSeek-V4 的分布式训练策略——细粒度 Expert Parallelism、Muon 的混合 ZeRO 策略和长上下文 Context Parallelism。
keywords:
  - distributed training
  - expert parallelism
  - ZeRO
  - context parallelism
  - DeepSeek-V4
refs:
  - "[flm] Kimi K3 分布式并行策略 | 对比性并行方案"
  - "[flm] DeepSeek-V4 训练基础设施 | 训练框架"
---

# DeepSeek-V4 分布式并行策略

## Expert Parallelism

### 细粒度 Wave-Based EP
- 将 experts 分组为 waves
- 每个 wave 完成后立即通信→计算流水线
- 融合 Dispatch+Linear1+Linear2+Combine 为单一 kernel
- RL rollout 和高速 agent serving 下最高 1.96× 加速

### 计算-通信比平衡
EP 的关键约束：`C/B ≤ 2d = 6144 FLOPs/Byte`

其中 C=峰值计算吞吐，B=互联带宽，d=hidden dimension。每 GBps 互联带宽可隐藏 6.1 TFLOPs 计算。

## ZeRO 混合策略（Muon）

### Dense Parameters
- 限制 ZeRO 并行数
- Knapsack 分配 → 均衡负载
- Padding < 10%（每个 rank ≤ 5 矩阵）
- 超出 DP 限制时冗余计算 Muon updates

### MoE Parameters
- 每 expert 独立优化
- 按类型展平（down→up→gate）
- 不限制 ZeRO 并行度
- FP8 梯度通信（BF16 随机舍入量化）
- All-to-all + FP32 local sum 替代 reduce-scatter

## Context Parallelism for CSA/HCA

### 挑战
- 不同 rank 的序列经压缩后长度不等
- 压缩操作需要 m 个连续 token，可能跨越 rank 边界

### 两阶段方案
1. **Tail Token Exchange**：rank i → rank i+1 发送最后 m 个未压缩 KV
2. **All-Gather + Fused Select-and-Pad**：收集所有本地压缩 KV，重排去 padding

Padding entries 置于尾部，query 可见范围可通过规则预计算。

## Activation Checkpointing

### Tensor-Level（非 Module-Level）
- TorchFX 图追踪全计算图
- 标注 tensor → 反向遍历确定最小重计算子图
- 自动去重（共享 storage 的 tensor）
- 零 GPU memory copy（复用 storage pointer）
