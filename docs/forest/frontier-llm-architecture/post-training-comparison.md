---
forest: flm
tree: 训练方法论
branch: 后训练管线
title: 后训练技术路线对比——Specialist-First vs Multi-Domain Unified
version: 1.0.0
created: 2026-07-29
updated: 2026-07-29
description: 对比 DeepSeek-V4 的"先培养专家再蒸馏统一"与 Kimi K3 的"多域同步 RL + 多教师蒸馏"两种后训练范式的设计哲学差异。
keywords:
  - post-training comparison
  - specialist training
  - multi-domain RL
  - on-policy distillation
  - MOPD
refs:
  - "[flm] DeepSeek-V4 后训练管线 | DSv4 方案"
  - "[flm] Kimi K3 后训练管线 | K3 方案"
---

# 后训练技术路线对比

## 两种范式

| 维度 | DeepSeek-V4 | Kimi K3 |
|------|------------|---------|
| **训练范式** | Specialist-First → Unify | Multi-Domain Parallel → Unify |
| **专家数量** | 每域独立训练（未公布具体数） | 9 个专家（3 域 × 3 努力级别） |
| **RL 算法** | GRPO | 继承 Kimi K2.5 RL 算法 |
| **Reward 设计** | 域特定 reward models | GRM（通用域）+ Verifier（Agent/Code） |
| **蒸馏方式** | On-Policy Distillation (Reverse KL) | MOPD (Multi-Teacher OPD, Clip KL) |
| **推理级别** | 未显式区分 | 显式 {low, high, max} |
| **环境多样性** | Agentic sandbox | 7 种环境 + Unified White-Box Harness |
| **Token 效率** | 未详述 | Budget control + Verbosity control |
| **量化感知** | FP4 QAT (expert + indexer QK) | MXFP4 QAT (entire post-training) |

## 核心分歧

### 1. 专家培养顺序

**DSv4** 采用"纵向培养"：每个域独立走完 SFT→RL 全流程，得到各自最优专家后再横向整合。

**K3** 采用"横向并行"：三域同步 RL 训练，共享基础设施和 rollout 系统，最后通过 MOPD 一次性整合。

### 2. 推理努力的显式建模

K3 显式定义 {low, high, max} 三档推理努力，通过 per-problem token budget control 在 RL 阶段直接塑造不同"思考深度"的行为模式。DSv4 未显式区分推理级别（但有 Max 模式用于评估）。

### 3. 合成环境 vs 实际环境

K3 构建了空前多样化的训练环境（7 种环境类型 + 可组合 harness），且大量使用程序化合成任务和 mock 应用。DSv4 的 agentic 训练环境描述相对简略。

### 4. 教师蒸馏的目标函数

DSv4 使用 **Reverse KL**（student 匹配 teacher），K3 使用 **Clipped Per-Token OPD reward**（reward 信号驱动，而非直接概率匹配）。两种策略在优化动力上有本质差异——前者是模仿学习，后者更接近 RL。
