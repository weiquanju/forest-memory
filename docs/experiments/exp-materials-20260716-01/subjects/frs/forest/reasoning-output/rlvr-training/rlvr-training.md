---
forest: frs
tree: reasoning-output
branch: rlvr-training
leaf_id: frs-rlvr-001
title: RLVR训练范式与三大方法
type: method
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
source: "[frs_source] §6.1 | DeepSeek-R1 [46], o1 [47], DCPO [31]"
---

# RLVR 训练范式与三大方法

## RLVR定义

**RLVR (Reinforcement Learning from Verifiable Rewards)** 是近年提升LLM推理能力的主流方法。在训练时获得可验证的奖励（如数学题正确答案或代码执行结果），模型学习生成更有效的推理步骤。

## 三大方法对比

| 方法 | 训练策略 | 奖励设计 | 代表模型 | 已知局限 |
|------|---------|---------|---------|---------|
| **GRPO [46]** | 组内相对策略优化 | 规则验证+格式奖励 | DeepSeek-R1 | 推理链过长时格式崩溃 |
| **PPO-RLVR [47]** | 标准PPO+可验证奖励 | 答案正确性二值奖励 | OpenAI o1 | 推理过程不可见、API成本高 |
| **DCPO [31]** | 解耦推理优化与置信度校准 | 分离正确性和校准两组梯度 | — | 仅验证于数学推理领域 |

## 三大已知挑战

1. **校准退化（Calibration Degeneration）**：即使答案错误也给出极高置信度——DCPO通过解耦优化缓解
2. **Reward Hacking**：模型利用奖励函数漏洞而非真正提升推理能力——GRPO组内比较部分抑制但未根除
3. **推理链质量退化**：长期RLVR训练导致推理格式呆板或崩溃
