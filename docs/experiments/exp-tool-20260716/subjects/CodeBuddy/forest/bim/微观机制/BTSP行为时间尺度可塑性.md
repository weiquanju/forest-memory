---
forest: bim
tree: 微观机制
branch: 突触可塑性
title: BTSP行为时间尺度可塑性
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
description: Bittner等人（2017）发现的海马体CA1区秒级可塑性规则——通过树突钙平台电位在单次经历中一次性创建记忆痕迹
keywords:
  - BTSP
  - 行为时间尺度可塑性
  - 树突钙平台电位
  - 位置细胞
  - 单次学习
atom_type: semantic
status: draft
---

# BTSP行为时间尺度可塑性

## 核心机制

BTSP 由树突钙离子平台电位（dendritic Ca²⁺ plateau potential）驱动。当 CA1 锥体细胞的远端树突产生大幅持久的钙信号时，在秒级时间窗口内（上升约4秒、衰减约3秒）将窗口内所有活跃的突触输入一次性增强（Bittner et al., 2017, *Science*, DOI: 10.1126/science.aan3846）。

## 与STDP的本质区别

| 维度 | STDP | BTSP |
|------|------|------|
| 时间尺度 | 毫秒级 | 秒级 |
| 重复要求 | 需要多次重复 | 单次经历即可 |
| 机制 | 毫秒级精确时序匹配 | 树突钙平台电位驱动 |

## 后续验证

- Wu & Maass（2025, *Nature Communications*）：构建计算模型证明 BTSP 可解释 CA1 位置场一次性快速形成
- Magee（2026, *Nature Neuroscience*）：综述指出 BTSP 广泛存在于海马体 CA1 及其他脑区

## 多时间尺度分工

STDP（毫秒级）→ 精细调谐（序列学习、因果推理）；BTSP（秒级）→ 快速捕获新经历。二者协同实现精细学习与快速记忆的平衡。
