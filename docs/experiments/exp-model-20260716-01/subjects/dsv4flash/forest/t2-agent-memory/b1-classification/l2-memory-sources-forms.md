---
forest: memory-systems-ai
tree: t2-agent-memory
branch: b1-classification
leaf: l2-memory-sources-forms
title: 代理记忆的来源与存储形式
version: 1.0.0
created: 2026-07-16
model: DeepSeek V4 Flash
source: "input/papers/2404.13501.md; input/frs_source/AI与大模型在知识领域、Agent记忆、推理数据及推理关系中的前沿研究综述.md"
refs:
  - "记忆来源：试验内信息（in-trial）、跨试验信息（cross-trial）、外部知识"
  - "记忆形式：文本形式（自然语言，可解释性强）vs 参数形式（嵌入向量，存储高效）"
  - "Zhong et al. — 自然语言形式的可解释记忆"
  - "Modarressi et al. — 参数形式的记忆存储"
---

# 代理记忆的来源与存储形式

Agent 记忆的来源分为三类：**试验内信息**（当前交互中的上下文）、**跨试验信息**（历史交互积累的经验）和**外部知识**（数据库、知识图谱等外部来源）。存储形式分为**文本形式**（自然语言，可解释性强、对用户友好）和**参数形式**（嵌入向量或模型权重，存储高效但黑盒化）。文本记忆的优势在于可解释性和灵活性，参数记忆的优势在于存储效率和无缝集成。实际系统往往结合两者优势采用混合架构。
