---
forest: flm
tree: 基础设施
branch: 训练框架
title: Kimi K3 训练基础设施
version: 1.0.0
created: 2026-07-29
updated: 2026-07-29
description: Kimi K3 的训练基础设施——KDA 系统协同设计（FlashKDA/KCP）、MoonEP 完美均衡专家并行和 memory-efficient 3T 级训练。
keywords:
  - training infrastructure
  - KDA system co-design
  - FlashKDA
  - KCP
  - MoonEP
  - Kimi K3
refs:
  - "[flm] DeepSeek-V4 训练基础设施 | 对比性训练框架"
  - "[flm] Kimi K3 推理基础设施 | 推理侧基础设施"
---

# Kimi K3 训练基础设施

## 1. KDA 算法-系统协同设计

### FlashKDA（Training/Prefill）
- CUTLASS-based chunkwise kernel
- 重叠 intra-chunk 计算与 cross-chunk state 传播
- Token-parallel stages + head-parallel recurrence 独立调度

### Intra-Device Context Parallelism
- 自动 SM-level CP planner
- 每个 segment 的状态转换可独立计算后精确组合
- 纯 intra-device，无跨设备通信

### KDA Context Parallelism (KCP)
- 每个 rank 计算本地 fragment：M^{T_i←1}_{[i]}（累积转换）和 S̃^{T_i}_{[i]}（从零生成的状态）
- 跨 rank 仅需 all-gather 固定大小 tensor
- Prefix scan 组合各 fragment 恢复完整状态
- O(n/P) 计算 + 固定通信量

## 2. MoonEP——完美均衡专家并行

- 静态计算形状（static computation shapes）
- Zero-copy 通信
- 支持 896 个路由专家在 3T 参数规模下的均衡执行
- Memory-efficient training：bounded memory 内维持高利用率

## 3. 3T 级预训练基础设施

- **Pipeline Parallelism (PP)** + Virtual Stages (VP)
- **Expert Parallelism (EP)** + Data Parallelism (DP)
- 多模态 encoder 优化以保持 bounded memory 下的 utilization

## 4. 1M-Token Agentic RL 系统

### Co-located RL System
- **Partial rollouts**：λ 比例完成即暂停
- **External KV-cache retention**：保存长程 rollout 的模型状态
- **Adaptive throttling**：根据系统负载动态调节并发
- **Resumable microVM sandboxes**：保持长程环境和模型状态

### 训练稳定性
- Per-token regularization 约束 policy update 在局部邻域内
- 支持跨 multi-iteration trajectories 的 extreme off-policy regime
