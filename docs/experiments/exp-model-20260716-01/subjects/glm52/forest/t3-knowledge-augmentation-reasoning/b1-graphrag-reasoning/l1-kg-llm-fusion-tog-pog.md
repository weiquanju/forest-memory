---
forest: memory-systems-ai
tree: t3-knowledge-augmentation-reasoning
branch: b1-graphrag-reasoning
leaf: l1-kg-llm-fusion-tog-pog
title: KG-LLM融合推理
created: 2026-07-16
model: GLM-5.2
source:
  - "frs_source/AI与大模型在知识领域、Agent记忆、推理数据及推理关系中的前沿研究综述.md"
refs:
  - "[t2-b1] 三类记忆来源 | KG作为外部知识来源为Agent记忆提供结构化知识"
  - "[t3-b2] 事实核查与知识溯源 | ToG的可追溯性是知识质量治理的基础"
---

# KG-LLM融合推理

## 知识图谱与大模型融合的动机

LLM 内部知识是隐式的，存在幻觉和知识更新不及时等问题。知识图谱（KG）以结构化形式存储大量事实，能提供精确的实体、属性和关系信息，增强模型在知识密集型任务中的表现。

## 代表性方法

### Think-on-Graph（ToG）
- **范式**："LLM⊗KG" 深度整合——LLM 作为 Agent 在 KG 上交互式探索，执行 beam search 发现推理路径
- **关键贡献**：证明了知识可追溯性——推理路径中每一步可追溯到 KG 中的具体事实三元组
- **局限**：搜索效率受 KG 规模线性影响

### Paths-over-Graph（PoG）
- **范式**：三阶段动态多跳路径探索，将 LLM 自身知识与 KG 事实知识结合
- **性能**：在 GPT-3.5-Turbo 上相较此前 SOTA 方法 ToG 平均准确率提升 18.9%；PoG+GPT-3.5-Turbo 超过 ToG+GPT-4 达 23.9%
- **局限**：路径质量依赖预提取的完整性

### KG-Agent
- **范式**：自主 LLM Agent 框架，集成多功能工具箱、KG 执行器和知识记忆
- **性能**：仅用 10K 样本微调 LLaMA-7B 即可在 KGQA 任务上超越使用更大模型的 SOTA 方法

### KG-RAR
- **范式**：过程导向的 KG 构建、分层检索策略和后处理奖励模型（PRP-RM）
- **性能**：在 Math500 和 GSM8K 上使用 Llama-3B 相较基线有 20.73% 相对提升

## 方法比较

| 方法 | 推理范式 | 依赖 KG 完整性 | 需要训练 | 可追溯性 | 主要局限 |
|------|---------|:---:|:---:|:---:|---------|
| ToG | LLM⊗KG + beam search | 是 | 否 | 高 | 搜索效率受 KG 规模线性影响 |
| PoG | 三阶段多跳路径融合 | 是 | 否 | 中 | 路径质量依赖预提取 |
| KG-Agent | 自主 Agent + 工具箱 | 是 | 是（10K微调） | 中 | 微调数据需求 |
| KG-RAR | 过程导向分层检索 + RM | 是 | 部分 | 中 | 需构建过程级 KG |

**关键观察**：绝大多数方法假设 KG 完整且高质量，"无需训练"是当前主流趋势，但当前缺少在统一 KGQA 基准上的标准化对比实验。
