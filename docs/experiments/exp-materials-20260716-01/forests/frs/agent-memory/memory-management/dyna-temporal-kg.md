---
forest: frs
tree: agent-memory
branch: memory-management
leaf_id: frs-mem-mgmt-003
title: DYNA时态KG情景记忆网络
type: method
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
source: "[frs_source] §3.3 | Sarabadani & Tajvidiyan, arXiv:2606.15778, 2026 [18]"
refs:
  - "[frs-mem-mgmt-002] MemVerse | DYNA与MemVerse均使用KG组织记忆但侧重时态维度"
---

# DYNA 时态KG情景记忆网络

## 方法概述

**DYNA** 将情景记忆建模为**时态知识图谱** [18]：
- 事件 → 节点
- 时态关系 → 带时间戳的有向边

## 检索机制

查询时通过**随机游走**和**中心度度量**检索相关节点，再增强LLM响应。

## 性能指标

| 对比基线 | 改善效果 |
|---------|:---:|
| vs 微调 | 灾难性遗忘减少约 **7%** |
| vs 标准RAG | 时态排序能力改善约 **5%** |

## 关键特性

- 每条记忆天然携带时间戳，支持"在某时间点之后/之前发生了什么"的时态查询
- 随机游走策略使检索既关注局部相关节点，也能探索较远的语义关联

## 局限

- 时态排序仅比RAG基线改善~5%，表明纯时态KG方法在时态理解上还有提升空间
- 仅支持文本模态
