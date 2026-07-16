---
forest: frs
tree: knowledge-governance
branch: fact-verification
leaf_id: frs-fact-002
title: GraphCheck多跳推理链事实核查
type: method
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
source: "[frs_source] §4.1 | Chen et al., arXiv:2502.16514, 2025 [21]"
---

# GraphCheck 多跳推理链事实核查

## 方法概述

**GraphCheck** 提出利用提取的知识图谱增强文本表示的事实核查框架 [21]。

## 核心创新

1. **GNN作为桥梁**：通过图神经网络（GNN）将KG处理为**软提示（soft prompt）**，注入LLM
2. **单次推理**：LLM在一次推理调用中完成精确高效的事实核查
3. **多跳推理链捕获**：捕获现有方法常忽略的多跳推理链

## 性能

| 范围 | 效果 |
|------|------|
| 7个基准 | 整体提升最高 **7.1%** |
| 医学等专业领域 | **超越专用事实核查器** |

## 权衡

| 优势 | 代价 |
|------|------|
| 高效（单次推理） | 可解释性降低（GNN黑箱） |
| 捕获多跳推理链 | 依赖KG嵌入质量 |
| 跨领域泛化 | 专业领域训练数据需求 |
