---
forest: memory-systems-ai
tree: t3-knowledge-augmentation-reasoning
branch: b2-knowledge-quality-governance
leaf: knowledge-traceability-explainability
title: 知识溯源与可解释推理
created: 2026-07-16
model: DeepSeek V4 Pro
source:
  - "frs_source/AI与大模型在知识领域、Agent记忆、推理数据及推理关系中的前沿研究综述.md"
refs:
  - "[t3-b2] 事实一致性检测 | 溯源是可解释事实核查的基础"
  - "[t3-b1] KG-LLM融合 | ToG 是知识溯源的代表性实践"
---

# 知识溯源与可解释推理

## 可追溯性的关键地位

知识的可追溯性（traceability）和可解释性（explainability）是将 AI 从"黑箱"推向可信系统的关键。

## ToG 的知识可追溯性

Think-on-Graph（Sun et al., 2023）明确证明了知识可追溯性和可纠正性：推理路径中的每一步都可以回溯到 KG 中的具体事实三元组。人类专家可以检查推理链中的每一步并提供反馈纠正错误——这种"人在回路中"方法显著提升推理透明度和可信度。

## 基于 RL 的可解释事实核查

Nikopensius 等人（2023, arXiv:2310.07613）：RL 推理 Agent 计算出证明或反驳事实声明的路径，这些路径可呈现给人类读者，让读者自行判断证据是否令人信服——人机协同的可解释事实核查范式。

## 混合事实核查管道

Kolli 等人（2025, arXiv:2511.03217）：集成 KG 检索、LLM 分类和 Web 搜索 Agent。关键设计：**"KG 覆盖不足时自动回退到 Web 搜索"的降级策略**。在 FEVER 基准上 F1 达 0.93，展示了模块化、开源架构。

## WKGFC 多源多 Agent 证据检索

Gong 等人（2026, arXiv:2603.00267）：利用权威开放 KG 作为核心证据来源，通过 MDP 建模让推理 LLM Agent 根据当前证据和声明自主决定采取什么行动，实现 KG + Web 搜索的协同证据检索。

## 溯源工程的挑战

1. **人在回路成本**：从"每条路径审核"降低到"异常检测+抽样审核"
2. **统一框架缺失**：声明、数值、时态三类事实需要统一的事实一致性评估框架
3. **可追溯性与效率的权衡**：神经方法可加速但牺牲可追溯性，符号方法可追溯但效率低
