---
forest: frs
tree: kg-reasoning
branch: path-optimization
leaf_id: frs-path-001
title: RRP可靠推理路径框架
type: method
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
source: "[frs_source] §2.3 | Xiao et al., arXiv:2506.10508, 2025 [11]"
refs:
  - "[frs-kg-llm-003] ToG交互式推理 | RRP在ToG基础上增加路径精炼"
---

# RRP 可靠推理路径框架

## 核心主张

**Reliable Reasoning Path (RRP)** 提出：精炼事实间的关系并将它们组织成逻辑一致的推理路径，与事实性知识本身**同等重要** [11]。

## 工作机制

| 组件 | 功能 |
|------|------|
| 关系嵌入 | 提取图结构信息，编码关系语义 |
| 双向分布学习 | 从正反两个方向学习关系分布 |
| 重思考模块（Rethinking） | 评估和精炼推理路径质量 |

## 关键特性

- **即插即用**：可集成到各种LLM中，无需修改模型架构
- **路径精炼**：不是简单检索而是主动评估和优化推理路径

## 局限

- 重思考模块增加了额外的推理开销
- 关系嵌入质量依赖KG的预处理
