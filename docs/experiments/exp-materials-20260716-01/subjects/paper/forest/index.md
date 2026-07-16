---
forest: agent-memory-survey
title: LLM-based Agent Memory Mechanism Survey
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
description: >
  A comprehensive knowledge forest extracted from the survey paper "A Survey on the Memory Mechanism 
  of Large Language Model based Agents" (arXiv:2404.13501). Covers the what/why/how of agent memory,
  including definitions, theoretical foundations, implementation architectures (sources/forms/operations),
  evaluation methodologies, real-world applications, and future research directions.
source:
  - "[arXiv:2404.13501] Zhang et al., A Survey on the Memory Mechanism of LLM based Agents, 2024 | 39 pages, 174 references"
refs: []
---

# LLM-based Agent Memory Mechanism Survey

## 定位

本森林基于 Zhang et al. (2024) 的综述论文 arXiv:2404.13501，系统梳理 LLM-based Agent 记忆机制的知识体系。论文从三个核心问题出发——What is the memory? Why do we need it? How to implement and evaluate it?——构建了完整的 Agent 记忆设计空间。森林覆盖记忆定义与理论基础（T1）、实现架构（T2）、评估方法（T3）、应用场景（T4）和前沿挑战（T5）五个维度。

## 森林内文档

### 树：T1 — 记忆基础理论

| Branch | 叶子文档 | 说明 |
|--------|---------|------|
| **B1.1 定义与形式化** | [agent-memory-definitions](t1-memory-foundations/b1-definitions/agent-memory-definitions.md) | 狭义/广义记忆定义、Task/Trial/Step 建模 |
| | [memory-assisted-interaction-model](t1-memory-foundations/b1-definitions/memory-assisted-interaction-model.md) | W/P/R 三操作统一模型与形式化推导 |
| **B1.2 理论必要性** | [cognitive-psychology-basis](t1-memory-foundations/b2-why-memory/cognitive-psychology-basis.md) | 认知心理学视角：从人类记忆到 Agent 设计 |
| | [self-evolution-necessity](t1-memory-foundations/b2-why-memory/self-evolution-necessity.md) | 自我进化视角：经验积累/环境探索/知识抽象 |

### 树：T2 — 记忆实现架构

| Branch | 叶子文档 | 说明 |
|--------|---------|------|
| **B2.1 记忆来源** | [inside-trial-vs-cross-trial](t2-memory-implementation/b1-sources/inside-trial-vs-cross-trial.md) | 试内信息 vs 跨试信息：代表性研究与权衡 |
| | [external-knowledge-integration](t2-memory-implementation/b1-sources/external-knowledge-integration.md) | 外部知识集成：API/工具调用与在线知识获取 |
| **B2.2 记忆形态** | [textual-memory-forms](t2-memory-implementation/b2-forms/textual-memory-forms.md) | 文本记忆：完整交互/最近交互/检索交互/外部知识 |
| | [parametric-memory-forms](t2-memory-implementation/b2-forms/parametric-memory-forms.md) | 参数化记忆：Fine-tuning 方法 vs 知识编辑方法 |
| | [textual-vs-parametric-tradeoffs](t2-memory-implementation/b2-forms/textual-vs-parametric-tradeoffs.md) | 效果/效率/可解释性三维权衡分析 |
| **B2.3 记忆操作** | [memory-writing-strategies](t2-memory-implementation/b3-operations/memory-writing-strategies.md) | 写入策略：信息提取、结构化存储与自主更新 |
| | [memory-management-mechanisms](t2-memory-implementation/b3-operations/memory-management-mechanisms.md) | 管理机制：合并-反思-遗忘三元操作 |
| | [memory-reading-retrieval](t2-memory-implementation/b3-operations/memory-reading-retrieval.md) | 读取检索：相似度匹配/Chain-of-Memory/隐式读取 |

### 树：T3 — 记忆评估方法

| Branch | 叶子文档 | 说明 |
|--------|---------|------|
| **B3.1 直接评估** | [subjective-evaluation-framework](t3-memory-evaluation/b1-direct-eval/subjective-evaluation-framework.md) | 主观评估：Coherence/Rationality + 评估者选择与标注 |
| | [objective-evaluation-metrics](t3-memory-evaluation/b1-direct-eval/objective-evaluation-metrics.md) | 客观评估：Correctness/F1/时间硬件成本 |
| **B3.2 间接评估** | [task-based-evaluation](t3-memory-evaluation/b2-indirect-eval/task-based-evaluation.md) | 任务驱动评估：对话/多源QA/长上下文/成功率 |

### 树：T4 — Agent 应用场景

| Branch | 叶子文档 | 说明 |
|--------|---------|------|
| **B4.1 核心交互应用** | [role-playing-social-simulation](t4-agent-applications/b1-core-apps/role-playing-social-simulation.md) | 角色扮演与社会模拟中的记忆设计 |
| | [personal-assistant-games](t4-agent-applications/b1-core-apps/personal-assistant-games.md) | 个人助理与开放世界游戏 |
| **B4.2 垂直领域应用** | [code-generation-recommendation](t4-agent-applications/b2-domain-apps/code-generation-recommendation.md) | 代码生成与推荐系统中的记忆 |
| | [expert-systems-domain](t4-agent-applications/b2-domain-apps/expert-systems-domain.md) | 医疗/金融/科学专家系统中的领域记忆 |

### 树：T5 — 前沿与挑战

| Branch | 叶子文档 | 说明 |
|--------|---------|------|
| **B5.1 参数化记忆前沿** | [parametric-memory-frontier](t5-frontiers-challenges/b1-parametric-frontier/parametric-memory-frontier.md) | 从文本到参数：信息压缩、Meta-learning、可解释性 |
| **B5.2 新兴方向** | [multi-agent-lifelong-learning](t5-frontiers-challenges/b2-emerging/multi-agent-lifelong-learning.md) | 多智能体记忆同步与终身学习 |
| | [humanoid-agent-memory](t5-frontiers-challenges/b2-emerging/humanoid-agent-memory.md) | 类人Agent记忆：认知对齐与知识边界 |

## 跨树引用关系

```
T1(记忆基础理论) ──定义──▶ T2(记忆实现架构) ──驱动──▶ T3(记忆评估方法)
       │                         │                         │
       ├── W/P/R 模型 → 操作设计  ├── 评估指标 → 应用验证    ├── 评估反馈 → 实现改进
       └── 自我进化 → 跨试记忆   └── 实现架构 → T4(应用场景) └── 直接vs间接 → 评估框架选择

T4(应用场景) ──需求──▶ T5(前沿与挑战)
       │
       ├── 多Agent协作 → 记忆同步
       ├── 长期交互 → 终身学习
       └── 角色一致性 → 类人Agent记忆
```
