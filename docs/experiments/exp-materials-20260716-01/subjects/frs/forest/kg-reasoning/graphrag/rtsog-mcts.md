---
forest: frs
tree: kg-reasoning
branch: graphrag
leaf_id: frs-graphrag-005
title: RTSoG蒙特卡洛树搜索增强KGQA
type: method
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
source: "[frs_source] §2.2 | Long et al., arXiv:2505.12476, 2025 [9]"
refs:
  - "[frs-graphrag-001] GraphRAG范式 | RTSoG将MCTS引入图增强推理"
---

# RTSoG 蒙特卡洛树搜索增强KGQA

## 方法概述

**Reward-Guided Tree Search on Graph (RTSoG)** 将蒙特卡洛树搜索（MCTS）引入知识图谱问答（KGQA）[9]。核心创新是通过**自批评MCTS（SC-MCTS）** 在奖励模型引导下迭代检索加权推理路径。

## 工作机制

1. 在KG上构建搜索树，每个节点代表一个实体
2. 奖励模型评估每个候选路径的推理质量
3. SC-MCTS通过自我批评机制动态调整搜索策略
4. 选择累积奖励最高的路径作为推理结果

## 性能

| 基准 | 相对SOTA提升 |
|------|:---:|
| GrailQA | **+8.7%** |
| WebQSP | **+7.0%** |

## 意义

RTSoG将AlphaGo式的MCTS搜索策略引入KG推理，为提升推理路径选择质量提供了新思路。
