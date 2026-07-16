---
forest: frs
tree: kg-reasoning
branch: path-optimization
leaf_id: frs-path-005
title: MemoTime时态记忆增强推理
type: method
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
source: "[frs_source] §2.3 | Tan et al., arXiv:2510.13614, 2025 [15]"
refs:
  - "[frs-graphrag-003] T-GRAG时态GraphRAG | MemoTime与T-GRAG均关注时态KG但侧重记忆复用"
---

# MemoTime 时态记忆增强推理

## 方法概述

**MemoTime** 将记忆增强与时态KG结合 [15]，核心创新点有二：

### 1. 时间树分解（Tree of Time）

将复杂时态问题分解为层次化的"时间树"，每个节点代表一个时间锚点，叶子节点对应具体的时间相关子问题。

### 2. 自演化经验记忆

存储已验证的推理轨迹和子问题嵌入，供跨类型复用。这种机制使得模型在解决新时态问题时可以**复用之前成功的推理模式**。

## 关键性能

> 小模型（Qwen3-4B）达到接近**GPT-4-Turbo**的推理性能 [15]

## 意义

MemoTime证明：通过精巧的记忆和分解机制，小模型可以在特定领域接近大模型的推理水平。
