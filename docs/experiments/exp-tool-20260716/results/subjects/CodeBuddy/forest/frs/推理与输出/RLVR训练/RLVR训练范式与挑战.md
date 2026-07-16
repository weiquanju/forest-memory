---
forest: frs
tree: 推理与输出
branch: RLVR训练
title: RLVR训练范式与挑战
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
description: RLVR（基于可验证奖励的强化学习）是提升LLM推理能力的主流方法——GRPO/PPO/DCPO三种策略以及校准退化/Reward Hacking等挑战
keywords:
  - RLVR
  - GRPO
  - DCPO
  - 校准退化
  - Reward Hacking
atom_type: semantic
status: draft
refs:
  - "[frs] 推理深度与模型规模 | RLVR的作用机制"
---

# RLVR训练范式与挑战

## 代表方法对比

| 方法 | 训练策略 | 奖励设计 | 代表模型 | 已知局限 |
|------|---------|---------|---------|---------|
| GRPO | 组内相对策略优化 | 规则+格式奖励 | DeepSeek-R1 | 推理链过长时格式崩溃 |
| PPO RLVR | 标准PPO+可验证奖励 | 答案正确性二值 | OpenAI o1 | 推理过程不可见 |
| DCPO | 解耦推理与校准 | 分离正确性和校准梯度 | — | 仅验证于数学领域 |

## 已知挑战

1. **校准退化**：错误答案也给出极高置信度。DCPO通过解耦推理与校准目标缓解
2. **Reward Hacking**：模型利用奖励函数漏洞而非真正推理
3. **推理链质量退化**：长期训练导致格式呆板或崩溃
