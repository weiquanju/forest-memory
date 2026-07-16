---
forest: frs
tree: 知识更新
branch: 持续学习
title: KG嵌入持续学习方法
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
description: EWC/知情初始化/BAKE/MRCKG/MSPT/KG-GMM六类方法解决KG嵌入持续学习中的灾难性遗忘问题
keywords:
  - 持续学习
  - KG嵌入
  - EWC
  - BAKE
  - 灾难性遗忘
atom_type: semantic
status: draft
refs:
  - "[bim] 灾难性遗忘的键值补充视角 | 持续学习问题的不同解释路径"
---

# KG嵌入持续学习方法

## 代表方法

| 方法 | 核心机制 | 效果 |
|------|---------|------|
| **EWC on KG**[33] | Fisher信息权重保护 | 遗忘从12.62%降至6.85% |
| **知情初始化**[34] | KG Schema引导实体表示初始化 | 加速学习+减少轮次 |
| **BAKE**[35] | 序贯贝叶斯后验更新+聚类 | CKGE基准最优 |
| **MRCKG**[36] | 多模态-结构协同课程调度 | 首次研究CMMKGR |
| **KG-GMM**[38] | 演化KG增强类增量学习 | CIL+SOTA |

## 关键发现

基于关系的任务划分比随机划分高出9.8个百分点的遗忘率——任务划分策略对遗忘程度有重要影响（Jhajj & Lin, 2025）。
