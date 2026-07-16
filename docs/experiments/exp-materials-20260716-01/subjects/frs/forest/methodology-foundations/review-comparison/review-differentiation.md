---
forest: frs
tree: methodology-foundations
branch: review-comparison
leaf_id: frs-method-002
title: 相关综述差异化定位
type: analysis
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
source: "[frs_source] §一.Y 相关综述比较"
---

# 相关综述差异化定位

## 已有综述对比

| 综述 | 覆盖方向 | 时间截止 | 本文差异 |
|------|---------|---------|---------|
| Peng et al. "GraphRAG: A Survey" (2024) | GraphRAG方法分类 | 2024.08 | 本文延伸至Agent记忆、事实核查、持续学习等交叉地带 |
| Hu et al. "Memory in AI Agents" [16] | Agent记忆统一分类体系 | 2025.12 | 本文以记忆为桥梁连接KG推理与知识编辑，补充知识质量治理 |
| Wu et al. "Continual Learning for LLMs" [39] | 持续预训练、微调、对齐 | 2024.01 | 本文扩展至KG嵌入EWC、BAKE及终身知识编辑 |
| Li et al. "Graph Meets LLM" (IJCAI 2024) | 图学习与LLM双向融合 | 2024.06 | 本文侧重"知识→推理→输出可靠性"的端到端链条 |

## 本文三大独特贡献

1. **跨领域整合视角**：将通常独立讨论的六大领域交叉整合，揭示"结构化知识引入→记忆持久化→质量验证→持续更新"的闭环链条

2. **时效性优势**：覆盖至2026年7月，纳入CS-RAG [8]、DYNA [18]、逻辑规则编辑 [45] 等最新工作

3. **双维度组织**：以"知识可追溯性"和"输出可靠性"为两条主线，而非简单的技术分类罗列
