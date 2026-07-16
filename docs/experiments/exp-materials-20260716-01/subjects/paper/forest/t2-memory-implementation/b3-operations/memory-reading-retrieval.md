---
forest: agent-memory-survey
tree: t2-memory-implementation
branch: b3-operations
title: 记忆读取与检索
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
source: "[arXiv:2404.13501] Section 5.3.3"
refs:
  - "[t1-b1] W/P/R统一模型 | 读取操作R的工程实现"
  - "[t2-b2] 文本记忆形态 | 文本记忆的检索方式取决于存储形态"
---

# 记忆读取与检索

## 核心问题

记忆读取（Memory Reading）的目标是从海量记忆条目中提取**与当前状态相关**的信息。由于记忆总量巨大且并非所有内容都与当前决策相关，读取策略的设计至关重要。

形式化：`Ĥ^k_t = R(M^k_t, c^k_{t+1})`

其中 R 通常通过计算 `M^k_t` 与 `c^k_{t+1}` 之间的相似度来实现 [82]。

## 代表性读取策略

| 模型 | 读取机制 | 技术方案 |
|------|---------|---------|
| ChatDB [96] | SQL 语句执行 | Agent 先生成 Chain-of-Memory SQL 语句 |
| MPC [101] | Memory Pool 检索 | 从记忆池检索相关记忆 + Chain-of-Thought 忽略无关记忆 |
| ExpeL [82] | Top-K 轨迹召回 | Faiss 向量库 + 最高相似度成功轨迹 |
| Generative Agents [83] | 三准则评分 | 相似度 + 时间间隔 + 重要性的加权组合 |
| MemoryBank [6] | Dual-tower 稠密检索 | 当前 context → embedding → FAISS 索引检索 |
| RET-LLM [7] | LSH 元组检索 | Locality-Sensitive Hashing 检索相关数据库元组 |

## 读取与写入的协作关系

读取和写入操作是**协同设计**的——写入形式直接影响读取方式：

| 写入形态 | 典型读取方式 |
|---------|------------|
| 文本记忆（自然语言） | 文本相似度 + 辅助信息（时效性/重要性） |
| 文本记忆（结构化数据库） | SQL 查询 / 符号化检索 |
| 参数化记忆 | 隐式读取（使用更新后的参数直接推理） |

## 设计维度

### 1. 检索准则

| 准则 | 定义 | 代表实现 |
|------|------|---------|
| 相似度 | 记忆与当前 context 的语义相关性 | 大多数模型使用 |
| 时效性 | 记忆的新鲜程度 | Generative Agents [83] |
| 重要性 | 记忆的事件重要性 | Generative Agents [83] |
| 任务导向 | 与当前任务类型的匹配度 | ExpeL [82] |

### 2. 检索粒度

- **条目级**（Entry-level）：每条记忆独立评分，Top-K 返回
- **轨迹级**（Trajectory-level）：返回完整的成功/失败轨迹（ExpeL [82]）
- **链式**（Chain-level）：Chain-of-Memory 生成多步检索语句（ChatDB [96]）

## 开放问题

- **多准则融合**：如何在相似度/时效性/重要性之间分配权重仍无统一标准
- **负向记忆检索**：大多数系统只检索正向相关记忆，但失败的教训（"什么不该做"）同样有价值
- **检索-推理解耦**：检索结果如何最优地整合进 Agent 的推理 prompt 仍未充分研究
