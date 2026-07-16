---
forest: frs
tree: knowledge-update
branch: kg-continual-learning
leaf_id: frs-kg-cont-003
title: MSPT与KG-GMM多模态持续KG构建
type: method
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
source: "[frs_source] §7.1 | MSPT [37], KG-GMM [38], Informed Init [34]"
refs:
  - "[frs-kg-cont-002] BAKE | MSPT与KG-GMM是多模态和生成式场景的扩展"
---

# MSPT与KG-GMM多模态持续KG构建

## MSPT [37]

为持续多模态KG构建（MKGC）领域引入基准，协调**知识保留（稳定性）**和**新数据整合（可塑性）**的平衡。

## KG-GMM [38]

利用构建的演化知识图谱增强类增量学习：
- 通过KG中的关系增强类别标签
- 为相似类别分配不同关系以增强模型区分能力
- 在常规CIL和少样本CIL设置中均达到**SOTA**

## 知情初始化策略 [34]

利用KG Schema和先前学习到的嵌入初始化新实体表示：
- 基于实体所属的类别获取初始嵌入
- 提升预测性能同时加速知识获取
- 可无缝集成到现有持续学习方法中

## 关键进展

| 方向 | 代表工作 | 进展 |
|------|---------|------|
| 持续KG嵌入 | EWC [33], BAKE [35] | EWC降低遗忘45.7%，BAKE提供理论保证 |
| 多模态持续KG | MRCKG [36], MSPT [37] | 首次系统化研究多模态遗忘 |
| 生成式持续学习 | KG-GMM [38] | KG关系增强类别区分 |
