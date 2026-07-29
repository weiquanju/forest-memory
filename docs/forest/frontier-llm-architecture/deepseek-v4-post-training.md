---
forest: flm
tree: 训练方法论
branch: 后训练管线
title: DeepSeek-V4 后训练管线
version: 1.0.0
created: 2026-07-29
updated: 2026-07-29
description: DeepSeek-V4 的两阶段后训练范式——Specialist Training（独立领域专家培养）+ On-Policy Distillation（统一模型整合），含 GRPO 和 FP4 QAT。
keywords:
  - post-training
  - specialist training
  - on-policy distillation
  - GRPO
  - FP4 QAT
  - DeepSeek-V4
refs:
  - "[flm] Kimi K3 后训练管线 | 对比性后训练策略"
  - "[flm] 后训练技术路线对比 | 两种范式的交叉分析"
---

# DeepSeek-V4 后训练管线

## 两阶段范式

```
阶段 1: Specialist Training
  Base Model → SFT → RL (GRPO) → Domain Expert_i
  重复 N 次得到 N 个领域专家

阶段 2: On-Policy Distillation
  N 个专家 → 统一模型（最小化 Reverse KL）
```

## 阶段 1：Specialist Training

### 目标领域
- 数学、编程、Agent、指令遵循

### 流程
1. **SFT**：在高质量、领域特定的数据上进行监督微调，建立基础能力
2. **RL (GRPO)**：使用 Group Relative Policy Optimization，由针对特定成功标准的 reward models 引导

## 阶段 2：On-Policy Distillation

将独立的领域专家能力整合到单一统一模型：
- 统一模型作为 student
- 各领域专家作为 teacher
- 优化目标：**Reverse KL Loss**

## 后训练基础设施创新

### FP4 Quantization-Aware Training
- MoE expert weights 和 indexer QK path 使用 FP4 QAT
- 减少内存和计算开销

### Full-Vocabulary OPD 的 Teacher 调度
- 高效的 teacher scheduling 以支持全词表 on-policy distillation

### Preemptible Rollout Service
- 可抢占、容错的 rollout 服务

### 1M-Token RL Framework
- 将 RL 框架扩展到百万 token 上下文
- Sandbox infrastructure for agentic AI

## 核心评估结果

| 能力域 | DeepSeek-V4-Pro-Max 表现 |
|--------|------------------------|
| Knowledge | 显著领先 open-source，缩小与 Gemini-3.1-Pro 差距 |
| Reasoning | 优于 GPT-5.2，落后前沿约 3-6 个月 |
| Agent | 与 Kimi-K2.6/GLM-5.1 持平，接近 Opus 4.5 |
| Long-Context | 1M context 下超越 Gemini-3.1-Pro（学术基准） |
