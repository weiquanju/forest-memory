---
forest: flm
tree: 架构设计
branch: MoE架构
title: DeepSeekMoE 在 DeepSeek-V4 中的架构演进
version: 1.0.0
created: 2026-07-29
updated: 2026-07-29
description: DeepSeek-V4 系列沿用的 DeepSeekMoE 架构及其相对于 DeepSeek-V3 的关键调整，包括 Hash Routing、激活函数变更和路由策略。
keywords:
  - DeepSeekMoE
  - Mixture-of-Experts
  - Hash Routing
  - fine-grained experts
  - auxiliary-loss-free
refs:
  - "[flm] StableLatentMoE 在 Kimi K3 中的设计 | MoE架构对比"
  - "[flm] MoE 路由策略对比 | 路由机制交叉分析"
---

# DeepSeekMoE 在 DeepSeek-V4 中的架构演进

## 概述

DeepSeek-V4 系列（Pro: 1.6T/49B activated, Flash: 284B/13B activated）继续采用 DeepSeekMoE 范式（Dai et al., 2024），在 DeepSeek-V3 基础上做了若干关键调整。

## 核心架构

### Fine-Grained Expert 设计

DeepSeekMoE 将 FFN 层设置为 **细粒度路由专家（fine-grained routed experts）** 与 **共享专家（shared experts）** 的组合：

- **DeepSeek-V4-Flash**：每层 1 个共享专家 + 256 个路由专家，每 token 激活 6 个专家
- **DeepSeek-V4-Pro**：更大规模配置，保持相同架构范式

### 激活函数变更

路由亲和度得分的激活函数从 `Sigmoid(·)` 改为 `Sqrt(Softplus(·))`，改善了路由选择的数值特性。

### Hash Routing 策略

DeepSeek-V4 将前几层 Transformer Block 的稠密 FFN 替换为采用 **Hash Routing**（Roller et al., 2021）的 MoE 层。Hash Routing 根据输入 token ID 通过预定义的哈希函数确定性选择目标专家，无需学习路由参数，降低了早期层的路由开销。

### 负载均衡

沿用 **auxiliary-loss-free 策略**（DeepSeek-AI, 2024），辅以轻微的 **sequence-wise balance loss** 防止单序列内的极端不均衡。相比 DeepSeek-V3，移除了路由目标节点数量的约束，并重新设计了并行策略以维持训练效率。

## 相对 DeepSeek-V3 的关键变更

| 组件 | DeepSeek-V3 | DeepSeek-V4 |
|------|------------|------------|
| 激活函数 | Sigmoid | Sqrt(Softplus) |
| 前几层 FFN | Dense FFN | Hash Routing MoE |
| 路由约束 | 有目标节点数限制 | 移除限制 |
| 负载均衡 | auxiliary-loss-free | auxiliary-loss-free + sequence-wise balance |

## Multi-Token Prediction (MTP)

MTP 策略保持不变，深度设为 1，与 DeepSeek-V3 配置相同。

## 参考文献

- Dai et al., 2024. DeepSeekMoE: Towards Ultimate Expert Specialization in Mixture-of-Experts Language Models.
- DeepSeek-AI, 2024. DeepSeek-V3 Technical Report.
- Roller et al., 2021. Hash Layers for Large Sparse Models.
