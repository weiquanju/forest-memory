---
forest: memory-systems-ai
tree: t2-agent-memory-systems
branch: b1-definition-sources
leaf: l2-three-memory-sources
title: 三类记忆来源
created: 2026-07-16
model: GLM-5.2
source:
  - "arXiv:2404.13501"
refs:
  - "[t2-b2] 写入-管理-读取三操作 | 来源类型决定写入策略和管理方式"
  - "[t3-b1] KG-LLM融合推理 | 外部知识来源与GraphRAG的结构化检索呼应"
---

# 三类记忆来源

## 来源分类

基于广义记忆定义，Agent 记忆内容来自三个类别。前两者在 Agent-环境交互过程中动态生成，后者是循环之外的静态信息。

| 来源 | 性质 | 时间特征 | 代表模型 |
|------|------|---------|---------|
| Inside-trial Information | 动态 | 短期 | MemoryBank, MemoChat, Voyager, MemGPT |
| Cross-trial Information | 动态 | 长期 | Reflexion, Retroformer, Synapse, ExpeL |
| External Knowledge | 静态 | 外部 | ReAct, GITM, Character-LLM, Huatuo |

## Inside-trial Information（试内信息）

Trial 内的历史步骤是最相关、最具信息量的信号。几乎所有已有工作都使用这类信息作为记忆来源。

- **Generative Agents**：记忆来自实现目标的历次行为
- **MemoChat**：记忆来自对话会话历史
- **Voyager**：记忆包含执行基本动作的可执行代码

局限：仅依赖试内信息可能阻碍 Agent 从不同任务中积累可泛化知识。

## Cross-trial Information（跨试信息）

跨多个 Trial 积累的信息，典型包括成功和失败的动作及其洞察。

- **Reflexion**：提出语言强化学习，从过去 Trial 中以语言形式提取经验并应用于后续 Trial
- **ExpeL**：存储和组织完成的轨迹，召回相似轨迹用于新任务，通过成功与失败案例对比识别成功模式
- **Synapse**：通过成功范例记录跨试信息，用于相似 Trial 的参考

跨试信息可视为**长期记忆**，利用不同 Trial 的反馈支持更广泛的 Agent 试验。

## External Knowledge（外部知识）

LLM-based Agent 可直接以自然语言方式获取文本形式的外部知识。

- **ReAct**：利用 Wikipedia API 获取推理步骤中缺失的外部知识
- **GITM**：从 Minecraft Wiki 和合成配方获取导航知识
- **ChatDoctor**：从 Wikipedia 和医学数据库检索外部知识

外部知识扩展了 Agent 的知识边界，提供无限、最新、有据可依的决策知识。但存在可靠性风险（不准确和偏见）、对齐成本及隐私安全问题。
