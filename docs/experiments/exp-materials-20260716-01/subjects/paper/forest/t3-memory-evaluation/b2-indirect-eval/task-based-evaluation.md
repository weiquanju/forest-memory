---
forest: agent-memory-survey
tree: t3-memory-evaluation
branch: b2-indirect-eval
title: 任务驱动的间接评估
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
source: "[arXiv:2404.13501] Section 6.2-6.3"
refs:
  - "[t3-b1] 直接评估 | 直接vs间接的两类评估策略"
  - "[t4] Agent应用场景 | 间接评估通过这些应用任务执行"
---

# 任务驱动的间接评估

## 核心逻辑

间接评估的直觉：如果 Agent 能成功完成一个**高度依赖记忆**的任务，则说明记忆模块有效。

## 四类间接评估任务

### 1. Conversation（对话）

**评估维度**：

| 指标 | 定义 | 评估方法 |
|------|------|---------|
| Consistency（一致性） | 响应与上下文的连贯性 | GPT-4 评分 [94] |
| Engagement（参与度） | 用户继续对话的意愿 | SCE-p score [101], CSIM score [100] |

**关键逻辑**：记忆存储上下文信息 → 对话连贯 → 用户体验提升。当 Agent 其他部分确定时，对话表现可直接反映记忆模块效果。

### 2. Multi-source Question-answering（多源问答）

**评估维度**：整合来自试内/跨试/外部三个来源的记忆信息的能力。

**代表研究**：

| 模型 | 记忆来源 | 评估任务 |
|------|---------|---------|
| ReAct [104] | 试内 + Wikipedia 外部知识 | 通用知识推理问答 |
| Reflexion [5], Retroformer [103] | + 跨试信息 | 多步推理任务 |
| MemGPT [100] | 多文档信息 | 长上下文问答 |

**独特价值**：可暴露多源记忆的**矛盾问题**（Memory Contradiction）和知识更新问题。

### 3. Long-context Applications（长上下文应用）

**核心任务**：
- **Passage Retrieval**（段落检索）：在长上下文中找到与问题匹配的正确段落 [139]
- **Summarization**（摘要）：对全局上下文的总结（ROUGE 等匹配分数）

**代表 benchmark**：ZeroSCROLLS [138], LongBench [139]

### 4. Other Tasks（其他任务）

| 指标 | 定义 | 代表场景 |
|------|------|---------|
| Success Rate（成功率） | 成功完成的任务比例 | AlfWorld [141] 空间推理, Minecraft [93] 物品制作 |
| Exploration Degree（探索度） | 探索到的不同物品/状态数量 | Minecraft [99] 技能学习 |

**通用验证方法**：几乎所有配备记忆的 Agent 都可通过 **Ablation Study**（消融实验）——对比有无记忆模块的性能差异——来评估记忆效果。

## 直接评估 vs 间接评估

| 维度 | 直接评估 | 间接评估 |
|------|---------|---------|
| 执行难度 | 高（需定义指标和 ground truth） | 低（利用现有 benchmark） |
| 归因准确性 | 高（独立测量记忆模块） | 低（任务表现可归因于多种因素） |
| 可靠性 | 高 | 中（评估结果可能有偏差） |
| 标准化程度 | **无标准 benchmark** | 有公开 benchmark |

## 关键缺口

> "To our knowledge, there are no open-sourced benchmarks tailored for the memory modules in LLM-based agents." (Section 6.3)

这一缺口意味着记忆模块评估领域迫切需要：
1. 标准化的记忆专用 benchmark
2. 统一的评估协议（包括 direct + indirect 的组合评估框架）
3. 可复现的评估环境（消除模型/环境差异的混杂影响）
