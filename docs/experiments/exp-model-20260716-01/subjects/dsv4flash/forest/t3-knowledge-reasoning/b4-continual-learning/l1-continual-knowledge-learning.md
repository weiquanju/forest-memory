---
forest: memory-systems-ai
tree: t3-knowledge-reasoning
branch: b4-continual-learning
leaf: l1-continual-knowledge-learning
title: 持续知识学习与灾难性遗忘
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
model: DeepSeek V4 Flash
source: "input/frs_source/AI与大模型在知识领域、Agent记忆、推理数据及推理关系中的前沿研究综述.md"
refs:
  - "EWC (Kirkpatrick et al., 2017) — 弹性权重巩固，持续KG嵌入学习"
  - "灾难性遗忘：新知识覆盖旧知识，是持续学习的核心挑战"
  - "持续学习策略：正则化（EWC）、回放（replay）、动态架构"
---

# 持续知识学习与灾难性遗忘

持续学习（Continual Learning）解决AI系统在学习新知识时如何不遗忘旧知识的问题。**灾难性遗忘**（catastrophic forgetting）是核心挑战：新任务的梯度更新覆盖了旧任务学到的权重表示。应对策略包括：**正则化方法**（如EWC约束重要权重变动）、**回放方法**（存储少量旧样本与新数据混合训练）、**动态架构方法**（为每个新任务分配新参数）。从键值记忆框架视角看，遗忘也可以理解为旧任务键值对被新任务检索路径"遮蔽"——信息仍在但无法访问。
