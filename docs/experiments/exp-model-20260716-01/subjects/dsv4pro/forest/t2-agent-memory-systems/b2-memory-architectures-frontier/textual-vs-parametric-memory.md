---
forest: memory-systems-ai
tree: t2-agent-memory-systems
branch: b2-memory-architectures-frontier
leaf: textual-vs-parametric-memory
title: 文本记忆与参数化记忆的权衡
created: 2026-07-16
model: DeepSeek V4 Pro
source:
  - "arXiv:2404.13501"
refs:
  - "[t2-b2] Mem0/MemVerse/DYNA架构 | 各框架在两个范式中的选择"
  - "[t3-b3] 知识编辑与灾难性遗忘 | 参数化记忆更新的工程挑战"
---

# 文本记忆与参数化记忆的权衡

## 两种储存形式

Zhang et al.（2024, arXiv:2404.13501）系统分析了 Agent 记忆的两种表示形式及其优劣。

### 文本形式（Textual Form）

显式以自然语言保留和调用信息，当前主流方法。

**四种子类型**：
1. **完整交互（Complete Interactions）**：串联所有历史信息至 prompt（如 LongChat），但面临计算复杂度平方增长和"Lost in the Middle"位置偏差问题
2. **近期交互（Recent Interactions）**：仅保留最近 t-k 步观测（如 SCM、MemGPT），遵循局部性原理但忽略远期关键信息
3. **检索式交互（Retrieved Interactions）**：基于相关性/重要性/话题的向量检索（如 MemoryBank、Generative Agents），可访问远期关键记忆但依赖检索精度
4. **外部知识**：通过 API 获取的工具调用型记忆（如 ReAct、Toolformer）

### 参数化形式（Parametric Form）

将信息编码进模型参数，隐式影响 Agent 行为。

- **微调方法**：通过 SFT 注入领域知识（如 Character-LLM、Huatuo），适合离线场景但可能引发灾难性遗忘和过拟合
- **记忆编辑方法**：精准修改特定事实而不影响无关知识（如 MEND、KnowledgeEditor），适合在线小规模更新

## 多维权衡

| 维度 | 文本记忆 | 参数化记忆 |
|------|---------|-----------|
| 信息完整性 | 高（原始信息详细完整） | 中（转换可能信息丢失） |
| 读取效率 | 低（占据 prompt token） | 高（无额外上下文开销） |
| 写入效率 | 高（直接追加） | 低（需训练/编辑） |
| 可解释性 | 高（自然语言可读） | 低（隐空间表示） |
| 信息密度 | 低（离散空间） | 高（连续空间） |

**结论**：文本记忆适合需要频繁写入和可解释的场景（对话、近期上下文）；参数化记忆适合大规模、既定知识和高效读取的场景。混合架构是未来方向。
