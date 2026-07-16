---
forest: frs
tree: knowledge-update
branch: kg-continual-learning
leaf_id: frs-kg-cont-001
title: EWC在知识图谱持续学习中的应用
type: method
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
source: "[frs_source] §7.1 | Jhajj & Lin, arXiv:2512.01890, 2025 [33]"
refs:
  - "[frs-kg-cont-002] BAKE贝叶斯持续KG嵌入 | EWC是KG持续学习的基线方法"
---

# EWC在知识图谱持续学习中的应用

## 问题背景

当KG嵌入（KGE）模型在新数据上增量学习时，往往遭遇**灾难性遗忘（Catastrophic Forgetting）**——先前习得的知识被新知识覆盖 [32]。

## EWC方法

**Elastic Weight Consolidation (EWC)** 通过Fisher信息矩阵保护对旧任务重要的参数权重，在FB15k-237上使用TransE嵌入进行评估 [33]。

## 关键发现

| 指标 | 数值 |
|------|:---:|
| 未使用EWC的遗忘率 | 12.62% |
| 使用EWC后的遗忘率 | **6.85%** |
| 遗忘降低幅度 | **45.7%** |

## 任务划分策略的意外发现

基于关系的任务划分比随机划分高出**9.8个百分点**的遗忘率——这意味着任务划分策略对持续学习效果有显著影响：
- 按关系划分 → 不同任务间的知识重叠度低 → 遗忘更严重
- 随机划分 → 任务间存在知识重叠 → 遗忘更缓和

## 局限

- 遗忘减半但未消除（6.85%残留）
- Fisher信息矩阵假设高斯后验，在非高斯场景下理论保证减弱
