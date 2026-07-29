---
forest: flm
tree: 训练方法论
branch: 后训练管线
title: Kimi K3 后训练管线
version: 1.0.0
created: 2026-07-29
updated: 2026-07-29
description: Kimi K3 的三阶段后训练范式——SFT → Multi-Domain RL → MOPD，覆盖三域 × 三推理努力级别的 nine-expert 训练和 Agentic GRM。
keywords:
  - post-training
  - reinforcement learning
  - MOPD
  - multi-teacher distillation
  - reasoning effort
  - Agentic GRM
  - Kimi K3
refs:
  - "[flm] DeepSeek-V4 后训练管线 | 对比性后训练策略"
  - "[flm] 后训练技术路线对比 | 两种范式的交叉分析"
---

# Kimi K3 后训练管线

## 三阶段范式

```
阶段 1: SFT → Cold-start policy（含 agentic trajectories）
阶段 2: Multi-Domain RL × 3 Effort Levels → 9 Expert Models
阶段 3: MOPD → Unified Model
```

## 阶段 1：SFT

- 基于 Kimi 前序模型的 domain-specialized 模型合成数据 trajectories
- 多阶段验证 + human-in-the-loop annotation
- XTML-based chat template 序列化复杂 agentic trajectories
- QAT from SFT stage onward（MXFP4 weights + MXFP8 activations）

## 阶段 2：Multi-Domain RL

### 三域 × 三推理努力 = 9 个专家

| 域 | 子任务 |
|----|--------|
| **General** | experience, vision, reasoning, faithfulness, search, knowledge work |
| **General Agents** | long-horizon assistant, deep research, paragraph writing |
| **Coding Agents** | SWE, coding experience, kernel tasks, web development |

每个域训练 {low, high, max} 三种推理努力级别。

### Partial Rollouts
- 采样 λ 比例完成后即暂停 rollouts，开始 policy 优化
- 暂停的 rollouts 在下一 iteration 被排队恢复
- Per-token regularization 处理跨 iteration 的 data staleness

### Reasoning Effort RL
- Per-problem token budget control：超出 τ·b₀(x) 的 trajectories reward = -1
- Stage-wise curriculum over budget multiplier τ

### Agentic Generative Reward Model (GRM)
- Tournament-style 二元比较 + 强制评估协议（read→rubric→score→scorepad）
- Budget-based verbosity control 防止 reward hacking

### RL 环境
- **Unified White-Box RL Environment**：可组合模块构造多种 harness
- **Knowledge-Graph-Guided Task Synthesis**：自演化层级 KG → 检索 → 合成
- **Verifiable Agentic Problems**：多步搜索、专业工作流、视觉推理
- **Kernel Optimization Tasks**：CUDA/Triton/CuTe/TileLang，correctness+performance reward
- **Personal Assistant Tasks**：Mock Gmail/Notion/Slack/Canvas，数千 tool calls
- **AET (Autonomous Execution Tasks)**：黑盒系统复制、量化因子发现、税务审计
- **Web Development Tasks**：交互游戏、3D/WebGL、data viz、full-stack

## 阶段 3：MOPD

Multi-Teacher On-Policy Distillation 将 9 个专家整合：

```
r^d_OPD(y_t | e, x, y_<t) = clip(sg(log(π_teacher/π_θ)), -R_max, R_max)
```

- 每个 (domain, effort) 对由对应 teacher 引导
- Dense per-token reward + partial rollout 兼容
- Top-k distillation 目标的实验未见明显优势

## 推断效率优化

- **MXFP4 QAT**：MoE expert weights → MXFP4, activations → MXFP8
- **Draft Model Fine-Tuning**：MTP layer 微调为 EAGLE-3 风格 draft model，优化 L_K loss（直接最大化 acceptance rate）
