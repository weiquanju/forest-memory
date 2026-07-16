---
forest: memory-systems-ai
tree: t3-knowledge-augmentation-reasoning
branch: b4-reasoning-multimodal
leaf: l1-rlvr-calibration
title: RLVR训练与校准退化
created: 2026-07-16
model: GLM-5.2
source:
  - "frs_source/AI与大模型在知识领域、Agent记忆、推理数据及推理关系中的前沿研究综述.md"
refs:
  - "[t1-b3] 世界模型与RL驱动记忆 | RLVR训练范式与RL驱动记忆管理呼应"
  - "[t2-b3] Agent记忆基准演进 | 推理基准与Agent记忆基准边界日益模糊"
---

# RLVR训练与校准退化

## RLVR 训练范式

RLVR（Reinforcement Learning from Verifiable Rewards）是近年提升 LLM 推理能力的主流方法。通过在训练时获得可验证奖励（如数学题正确答案或代码执行结果），模型学习生成更有效的推理步骤。

## 代表性方法

| 方法 | 训练策略 | 奖励设计 | 代表模型 | 已知局限 |
|------|---------|---------|---------|---------|
| GRPO | 组内相对策略优化 | 规则验证 + 格式奖励 | DeepSeek-R1 | 推理链过长时格式崩溃 |
| PPO-based RLVR | 标准 PPO + 可验证奖励 | 答案正确性二值奖励 | OpenAI o1 | 推理过程不可见、API 成本高 |
| DCPO | 解耦推理优化与置信度校准 | 分离正确性和校准两组梯度 | — | 仅验证于数学推理领域 |

## 三大已知挑战

### 1. 校准退化（Calibration Degeneration）
即使答案错误也给出极高置信度。DCPO（arXiv:2603.09117）通过解耦推理与校准目标缓解该问题——在保持与 GRPO 相当准确率的同时实现最佳校准性能。

### 2. Reward Hacking
模型可能学会利用奖励函数漏洞（如输出特定格式模板）而非真正提升推理能力。GRPO 的组内相对比较机制在一定程度上抑制了该问题，但未根除。

### 3. 推理链质量退化
长期 RLVR 训练可能导致推理格式趋于呆板或崩溃，需要在训练中动态监控推理链质量和多样性。

## 关键洞察

- 推理深度（生成更多中间步骤）通常与输出正确率正相关
- 规模并非万能药：通过 RLVR 训练，较小规模模型也能在推理任务上取得接近大规模模型的表现
- DeepSeek-R1 证明推理能力可蒸馏至小模型

## 开放问题

1. RLVR 的 reward hacking 问题仍是深层风险，DCPO 的校准优化是必要但不充分的缓解
2. 推理深度的"边际收益递减"效应尚未量化——更多推理步骤何时变成有害的冗长？是否存在最优推理深度？
3. RLVR 训练范式如何与 Agent 记忆管理结合——记忆中存储的推理经验能否作为 RLVR 的额外奖励信号？
