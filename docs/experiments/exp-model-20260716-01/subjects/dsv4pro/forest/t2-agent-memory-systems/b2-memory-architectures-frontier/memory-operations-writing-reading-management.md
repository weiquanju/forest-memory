---
forest: memory-systems-ai
tree: t2-agent-memory-systems
branch: b2-memory-architectures-frontier
leaf: memory-operations-writing-reading-management
title: 记忆操作：写入/管理/读取统一模型
created: 2026-07-16
model: DeepSeek V4 Pro
source:
  - "arXiv:2404.13501"
refs:
  - "[t2-b1] Agent记忆三维分类 | 动态过程维度（Formation/Evolution/Retrieval）的操作实现"
  - "[t1-b3] 再巩固与遗忘机制 | 记忆管理的生物启发"
---

# 记忆操作：写入/管理/读取统一模型

## 统一操作框架

Zhang et al.（2024）提出 LLM Agent 记忆的三操作统一模型，对应 agent-environment 交互的三个关键阶段。

## 写入操作（Memory Writing）

将原始观测投影为实际存储的记忆内容（更精炼、更信息丰富）。

**设计要点**：
- 信息提取策略至关重要：原始信息通常冗长含噪
- 需考虑环境反馈形式的多样性

**代表**：
- **TiM**：提取实体间关系存入结构化数据库，相似内容分入同组
- **MemoChat**：摘要每段对话，以讨论主题为键索引记忆片段
- **SCM**：记忆控制器决定何时执行写入

## 管理操作（Memory Management）

迭代处理已存储记忆使之更有效。

**三种管理策略**：
1. **反思（Reflection）**：生成高级抽象（如 Generative Agents 的抽象思维生成）
2. **合并（Merging）**：去除冗余信息（如 RET-LLM 合并相似记忆条目）
3. **遗忘（Forgetting）**：移除不重要或无关信息

大多管理操作受人类大脑工作机制启发，利用 LLM 模拟人类思维的能力。

## 读取操作（Memory Reading）

根据当前上下文从记忆中提取相关信息驱动下一步行动。

**实现方式**：
- **向量检索**：基于相似度+辅助信息计算匹配分数（MemoryBank 使用双塔稠密检索 + FAISS 索引）
- **SQL 查询**：ChatDB 生成 SQL 语句从符号记忆库检索
- **LSH 检索**：RET-LLM 使用局部敏感哈希加速元组检索

## 形式化表示

从 {a_t, o_t} 到 a_{t+1} 的统一演化函数：
```
a_{t+1} = LLM{ R( P( M_{t-1}, W({a_t, o_t}) ), c_{t+1} ) }
```
其中 W=写入, P=管理, R=读取, c_{t+1}=下一动作上下文。
