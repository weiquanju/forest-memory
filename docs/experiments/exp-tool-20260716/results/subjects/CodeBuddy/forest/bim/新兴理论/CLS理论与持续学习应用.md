---
forest: bim
tree: 新兴理论
branch: 互补学习
title: CLS理论与持续学习应用
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
description: McClelland等（1995）提出互补学习系统理论——海马体快速学习（特化）与新皮层慢速学习（泛化）协同实现记忆平衡
keywords:
  - 互补学习系统
  - CLS
  - VAE-MHN
  - 持续学习
  - 抗灾难性遗忘
atom_type: semantic
status: draft
refs:
  - "[bim] 海马体与新皮层互补系统 | CLS的神经科学基础"
  - "[bim] 模式分离与模式完成互补算法 | VAE负责模式完成、MHN负责模式分离"
---

# CLS理论与持续学习应用

## 核心主张

CLS 理论（McClelland et al., 1995）认为大脑存在两个学习速率不同的系统：海马体快速学习细节（特化），新皮层慢速学习规律（泛化），在特化与泛化之间取得平衡。

## AI实现

Jun 等人（2025）提出 CLS 神经网络模型，将变分自编码器（VAE，模拟新模式完成/泛化）与现代 Hopfield 网络（MHN，模拟模式分离/快速编码）相结合。在 Split-MNIST 持续学习基准上达到接近 SOTA 的 ~90% 准确率，显著减少灾难性遗忘。

## 意义

CLS 理论不仅是大脑机制描述，也可指导 AI 模型设计——快速学习（海马体）与慢速整合（新皮层）的双系统架构是解决持续学习中稳定性-可塑性困境的生物启发方案。
