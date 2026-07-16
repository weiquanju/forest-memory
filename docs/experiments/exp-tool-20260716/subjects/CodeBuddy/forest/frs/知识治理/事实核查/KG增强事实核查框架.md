---
forest: frs
tree: 知识治理
branch: 事实核查
title: KG增强事实核查框架
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
description: KG-CRAFT/GraphCheck/CommunityKG-RAG/HybridFC等方法将知识图谱与事实核查深度融合——从对比性问题生成到GNN多跳推理链
keywords:
  - 事实核查
  - KG-CRAFT
  - GraphCheck
  - CommunityKG-RAG
  - HybridFC
atom_type: semantic
status: draft
---

# KG增强事实核查框架

## 代表方法

| 方法 | 核心机制 | 表现 |
|------|---------|------|
| **KG-CRAFT**[20] | KG引导对比性问题→证据提炼 | SOTA on LIAR-RAW/RAWFC |
| **GraphCheck**[21] | GNN软提示+多跳推理链 | 7基准整体提升7.1% |
| **CommunityKG-RAG**[22] | KG社区结构多跳检索 | 无需训练适应新领域 |
| **HybridFC**[23] | 文本/路径/规则/嵌入集成 | AUC提升0.14-0.27 |

## 关键观察

多数方法依赖 KG 完整性，跨领域泛化性能普遍下降 5-15%，是部署落地的核心瓶颈。
