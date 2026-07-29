---
forest: flm
tree: 基础设施
branch: 分布式策略
title: Kimi K3 分布式并行策略
version: 1.0.0
created: 2026-07-29
updated: 2026-07-29
description: Kimi K3 的分布式训练和推理策略——KDA Context Parallelism、Pipeline+Expert+Data 三维并行和 Co-located RL 系统。
keywords:
  - distributed training
  - KCP
  - pipeline parallelism
  - expert parallelism
  - co-located RL
  - Kimi K3
refs:
  - "[flm] DeepSeek-V4 分布式并行策略 | 对比性并行方案"
  - "[flm] Kimi K3 训练基础设施 | 训练框架"
---

# Kimi K3 分布式并行策略

## KDA Context Parallelism (KCP)

### 核心分解

每个 rank i 计算两个本地 fragment：
- **M^{T_i←1}_{[i]}**：前 T_i 个 token 的累积转换矩阵 ∈ R^(dk×dk)
- **S̃^{T_i}_{[i]}**：从 S=0 开始的本地状态 ∈ R^(dk×dv)

任意状态可表示为 fragment 的组合：
```
S^t_{[i+1]} = S̃^t_{[i+1]} + M^{t←1}_{[i+1]} · S^{T_i}_{[i]}
           = S̃^t_{[i+1]} + M^{t←1}_{[i+1]} · Σ_j (Π_l M^{T_l←1}_{[l]}) · S̃^{T_j}_{[j]}
```

### 通信
- 仅需 **all-gather** M 和 S̃（固定大小，与序列长度无关）
- Prefix scan 恢复各 rank 的 incoming state
- 计算缩放：**O(n/P)**，通信固定

## 3T 级预训练三维并行

```
PP (Pipeline Parallelism) + VP (Virtual Stages)
  × EP (Expert Parallelism)
  × DP (Data Parallelism)
```

- MoonEP 保证 896 专家在 3T 参数下的完美均衡
- Memory-efficient training 维持 bounded memory 内的高利用率
- 多模态 encoder 优化

## Co-located RL 系统（1M Token Agentic RL）

| 组件 | 功能 |
|------|------|
| Partial Rollouts | λ 比例完成即暂停，下轮排队恢复 |
| External KV-cache Retention | 跨 iteration 保留长程 trajectory 的模型状态 |
| Adaptive Throttling | 动态调节并发 |
| Resumable microVM Sandboxes | 保持执行环境和模型状态 |

### 稳定性保证
- Per-token regularization：约束 policy update 在局部邻域
- 支持 extreme off-policy（trajectory 跨多个 iteration 的 data staleness）

## KDA 推理并行

### Intra-Device CP（Training/Prefill）
- SM-level 自动序列分区
- Segment 状态转换独立计算 + 精确组合

### Inter-Device KCP
- 跨 rank 固定大小通信

### Decoding
- 专用 decoding kernel 处理小 batch × 单 token 的特殊瓶颈
