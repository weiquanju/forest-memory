---
forest: memory-systems-ai
tree: t3-knowledge-reasoning
branch: b3-reasoning
leaf: l2-rlvr-training
title: RLVR训练范式—强化学习驱动的推理增强
version: 1.0.0
created: 2026-07-16
model: DeepSeek V4 Flash
source: "input/frs_source/AI与大模型在知识领域、Agent记忆、推理数据及推理关系中的前沿研究综述.md"
refs:
  - "DeepSeek-R1 (arXiv:2501.12948, 2025) — RLVR训练范式"
  - "OpenAI o1 (arXiv:2412.16720, 2024) — 推理能力系统卡"
  - "RLVR：Reinforcement Learning with Verifiable Rewards — 通过可验证奖励信号训练推理能力"
---

# RLVR训练范式

RLVR（Reinforcement Learning with Verifiable Rewards，可验证奖励强化学习）是2025年兴起的推理训练范式，以**DeepSeek-R1**（arXiv:2501.12948）和**OpenAI o1**（arXiv:2412.16720）为代表。与传统训练不同，RLVR不依赖人工标注的思维链，而是通过可验证的奖励信号（如数学答案是否正确、代码是否通过测试）来引导模型自主发现有效的推理策略。这一范式使模型能够发展出"思考"能力——在回答前进行内部推理。
