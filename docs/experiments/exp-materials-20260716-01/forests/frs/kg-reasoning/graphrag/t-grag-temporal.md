---
forest: frs
tree: kg-reasoning
branch: graphrag
leaf_id: frs-graphrag-003
title: T-GRAG时态知识增强检索
type: method
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
source: "[frs_source] §2.2 | Li et al., arXiv:2508.01680, 2025 [7]"
refs:
  - "[frs-graphrag-001] GraphRAG范式 | T-GRAG在GraphRAG基础上增加时态维度"
---

# T-GRAG 时态知识增强检索

## 问题背景

传统GraphRAG忽视知识的**时间演化**——例如"某公司CEO"的答案在2023年和2025年可能完全不同，传统方法无法区分不同时间点的知识版本。

## T-GRAG架构

**T-GRAG (Temporal GraphRAG)** 通过四个组件解决时态问题 [7]：

| 组件 | 功能 |
|------|------|
| 时态知识图谱生成器 | 为每个事实关联时间戳，构建时态KG |
| 时态查询分解 | 将复杂时态问题分解为时间锚定的子查询 |
| 三层交互式检索器 | 按时间层、实体层、关系层分层检索 |
| 源文本提取器 | 从原始文本中提取时效性上下文 |

## 评估

在基于真实公司年报的**Time-LongQA**基准上显著超越先前方法。该基准模拟了真实世界的知识时态演化场景。

## 局限

- 仅适用于存在明确时间标签的领域（如金融、法律）
- 时态KG的维护成本高于静态KG
