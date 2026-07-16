---
forest: frs
tree: knowledge-governance
branch: method-comparison
leaf_id: frs-gov-compare-001
title: 知识评估方法五维横向对比
type: analysis
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
source: "[frs_source] §4.3 方法比较与讨论"
refs:
  - "[frs-fact-001] KG-CRAFT"
  - "[frs-fact-002] GraphCheck"
  - "[frs-knowledge-trace-001] 混合管道"
  - "[frs-knowledge-trace-001] RL可解释核查"
  - "[frs-knowledge-trace-001] 语义三元组"
---

# 知识评估方法五维横向对比

## 对比矩阵

| 方法/框架 | 核心机制 | 是否需要KG？ | 证据来源 | 可解释性 | 最佳表现 |
|------|---------|:---:|------|:---:|------|
| KG-CRAFT [20] | KG增强对比性问题生成 | 是 | KG+文本 | 中（对比性问题可读） | SOTA on LIAR-RAW, RAWFC |
| GraphCheck [21] | GNN软提示+多跳推理链 | 是 | KG嵌入 | **低**（GNN黑箱） | 7基准整体提升7.1% |
| Hybrid Pipeline [28] | KG检索+LLM分类+Web Agent | 首选，不足时回退Web | KG+Web | **高**（模块化管道） | F1=0.93 on FEVER |
| RL-based [27] | RL Agent计算证明/反驳路径 | 是 | KG路径 | **高**（路径可呈现给人） | — |
| Semantic Triples [29] | 声明→语义三元组+KG增强 | 是 | KG | 中 | 超越零样本方法 |

## 关键观察

1. **混合管道在准确率上领先**（F1=0.93），但工程复杂度也更高
2. **GraphCheck** 证明GNN可作为LLM与KG之间的桥梁，但以牺牲一定可解释性为代价
3. **跨领域泛化是核心瓶颈**：多数方法依赖KG完整性，从FEVER到Climate-FEVER性能普遍下降5-15%
