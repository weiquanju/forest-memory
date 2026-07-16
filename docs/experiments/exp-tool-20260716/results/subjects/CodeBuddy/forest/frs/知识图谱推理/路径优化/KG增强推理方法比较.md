---
forest: frs
tree: 知识图谱推理
branch: 路径优化
title: KG增强推理方法比较
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
description: ToG/PoG/KG-RAR/SoG/CS-RAG/MemoTime六类KG增强推理方法在推理范式、KG依赖、可追溯性等维度的横向比较
keywords:
  - 方法比较
  - 推理范式
  - KG依赖
  - 可追溯性
  - 标准化评测
atom_type: semantic
status: draft
---

# KG增强推理方法比较

## 横向对比

| 方法 | 推理范式 | 依赖KG完整？ | 训练需求 | 可追溯性 | 主要局限 |
|------|---------|:---:|:---:|:---:|---------|
| ToG | LLM⊗KG+beam search | 是 | 否 | 高 | 搜索效率受KG规模线性影响 |
| PoG | 三阶段多跳路径融合 | 是 | 否 | 中 | 路径质量依赖预提取完整性 |
| KG-RAR | 过程导向分层+奖励模型 | 是 | 部分 | 中 | 需构建过程级KG |
| SoG | observe-think-navigate | 是 | 否 | 高 | 对LLM推理能力要求高 |
| CS-RAG | 原子约束+充分性检查 | 否 | 否 | 中 | 约束规划增加推理开销 |
| MemoTime | 时间树+经验记忆 | 部分 | 否 | 中 | 仅覆盖时态问题 |

## 关键发现

1. 仅CS-RAG专门处理不完美KG——真实部署的分化点
2. "无需训练"是主流但KG-RAR提示轻量微调可能提升下游表现
3. 缺少统一KGQA基准上的标准化对比实验
