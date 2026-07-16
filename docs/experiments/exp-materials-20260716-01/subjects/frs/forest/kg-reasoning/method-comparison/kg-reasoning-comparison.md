---
forest: frs
tree: kg-reasoning
branch: method-comparison
leaf_id: frs-kg-compare-001
title: KG推理方法六维横向对比
type: analysis
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
source: "[frs_source] §2.4 方法比较与讨论"
refs:
  - "[frs-kg-llm-003] ToG"
  - "[frs-kg-llm-002] PoG"
  - "[frs-kg-llm-005] KG-RAR"
  - "[frs-path-004] SoG"
  - "[frs-graphrag-004] CS-RAG"
  - "[frs-path-005] MemoTime"
---

# KG推理方法六维横向对比

## 对比矩阵

| 方法 | 推理范式 | 依赖KG完整性？ | 是否需要训练？ | 可追溯性 | 主要局限 |
|------|---------|:---:|:---:|:---:|---------|
| ToG [3] | LLM⊗KG交互探索+beam search | 是 | 否 | **高**（每步可回溯三元组） | 搜索效率受KG规模线性影响 |
| PoG [2] | 三阶段多跳路径融合 | 是 | 否 | 中 | 路径质量依赖预提取完整性 |
| KG-RAR [1] | 过程导向分层检索+奖励模型 | 是 | 部分（PRP-RM） | 中 | 需要构建过程级KG |
| SoG [14] | observe-think-navigate上下文感知导航 | 是 | 否 | **高** | 对LLM自身推理能力要求高 |
| CS-RAG [8] | 原子约束规划+充分性检查 | **否（设计为鲁棒）** | 否 | 中 | 约束规划增加推理开销 |
| MemoTime [15] | 时间树分解+自演化经验记忆 | 部分（时态KG） | 否 | 中 | 仅覆盖时态类问题 |

## 三条关键观察

1. **绝大多数方法假设KG是完整且高质量的**，只有CS-RAG [8] 专门处理不完美KG——这在真实部署场景中是一个重要分化

2. **"无需训练"是当前主流趋势**（ToG/PoG/SoG无需训练），但KG-RAR的PRP-RM提示轻量微调可能显著提升下游任务表现，两类路线的长期优劣尚待观察

3. **缺少统一评测框架**：当前缺少在统一KGQA基准（如GrailQA/WebQSP）上的标准化对比实验，各论文报告的提升数字**不可直接横向比较**，社区亟需统一评测框架
