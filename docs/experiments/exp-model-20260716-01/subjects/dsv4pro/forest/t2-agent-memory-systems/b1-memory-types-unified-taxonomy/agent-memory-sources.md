---
forest: memory-systems-ai
tree: t2-agent-memory-systems
branch: b1-memory-types-unified-taxonomy
leaf: agent-memory-sources
title: Agent记忆来源：试内/跨试/外部知识
created: 2026-07-16
model: DeepSeek V4 Pro
source:
  - "arXiv:2404.13501"
refs:
  - "[t2-b1] Agent记忆三维分类 | 来源维度对载体形式和操作的约束"
---

# Agent记忆来源：试内/跨试/外部知识

## 三类记忆来源

基于 Zhang et al.（2024, arXiv:2404.13501）对 LLM Agent 记忆源的系统分类。

### 试内信息（Inside-trial Information）

单次任务中 agent-environment 交互的历史步骤，是最直观、高度相关的记忆来源。

**代表性工作**：
- **Generative Agents**（Park et al., 2023）：从历史行为中派生记忆，模拟人类日常行为
- **MemoChat**（Lu et al., 2023）：基于对话历史构建记忆
- **Voyager**（Wang et al., 2023）：存储基础动作的可执行代码作为记忆

### 跨试信息（Cross-trial Information）

跨多次试验积累的成功/失败动作及其洞察（失败原因、成功模式等）。

**代表性工作**：
- **Reflexion**（Shinn et al., NeurIPS 2023）：以语言形式从过去试验中提炼经验，应用至后续试验——实质是口头强化学习
- **ExpeL**（Zhao et al., 2023）：存储和组织完整轨迹，将成功案例与失败案例对比以识别成功模式
- **Synapse**（Zheng et al., 2023）：通过成功范例记录跨试信息作为相似试验参考

### 外部知识（External Knowledge）

独立于 agent-environment 交互循环的静态信息。

**代表性工作**：
- **ReAct**（Yao et al., 2022）：利用 Wikipedia API 获取外部知识
- **GITM**（Zhu et al., 2023）：引用 Minecraft Wiki 知识
- **ChatDoctor**（Li et al., 2023）：从 Wikipedia 和医学数据库检索

## 来源互补性

仅依赖试内信息可能阻碍 Agent 跨任务积累通用知识。三类来源组合（如 Reflexion、ExpeL、Retroformer 同时使用三者）是实现自我进化的关键。
