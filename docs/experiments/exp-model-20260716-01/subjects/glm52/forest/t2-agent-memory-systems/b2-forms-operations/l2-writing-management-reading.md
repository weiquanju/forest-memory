---
forest: memory-systems-ai
tree: t2-agent-memory-systems
branch: b2-forms-operations
leaf: l2-writing-management-reading
title: 写入-管理-读取三操作
created: 2026-07-16
model: GLM-5.2
source:
  - "arXiv:2404.13501"
refs:
  - "[t1-b3] 模式完成与内容寻址存储 | 记忆读取的内容寻址对应CAM检索"
  - "[t1-b2] 再巩固与主动遗忘 | 记忆管理的反思与遗忘对应生物再巩固机制"
---

# 写入-管理-读取三操作

## 三操作框架

记忆的完整过程分为三个协作操作：

## Memory Writing（记忆写入）

将原始观测投影为实际存储的记忆内容，使其更具信息量和更简洁。

- **TiM**：将原始信息提取为实体间关系，存入结构化数据库，相似内容归入同一组
- **SCM**：设计记忆控制器决定何时执行操作
- **MemGPT**：完全自主的记忆写入，Agent 根据上下文自动更新记忆
- **MemoChat**：对每段对话摘要抽象主要话题，作为索引记忆片段的键

**关键洞察**：信息提取策略的设计至关重要——原始信息通常冗长且有噪声，不同环境提供不同形式的反馈。

## Memory Management（记忆管理）

处理存储的记忆信息使其更有效，包括三种子操作：

| 子操作 | 功能 | 代表模型 |
|-------|------|---------|
| Merging | 合并相似信息减少冗余 | MemoryBank, ChatDB, TiM |
| Reflection | 反思生成更高层次概念 | MemoryBank, Generative Agents, Reflexion |
| Forgetting | 遗忘不重要/早期记忆 | 几乎所有模型（✓ 25/28） |

- **MemoryBank**：将对话蒸馏为日常事件摘要，持续评估和提炼知识生成个性洞察
- **Generative Agents**：当累积事件足够时触发反思过程生成抽象思想
- **GITM**：从多个计划中提取关键动作建立通用参考计划

大多数记忆管理操作受到人脑工作机制的启发——利用 LLM 模拟人脑能力生成高层次信息。

## Memory Reading（记忆读取）

从记忆中提取相关信息支持推理和决策。

- **ChatDB**：通过 SQL 语句执行读取，Agent 预先生成 Chain-of-Memory
- **MPC**：从记忆池检索相关记忆，提供 CoT 示例以忽略某些记忆
- **ExpeL**：利用 FAISS 向量存储作为记忆池，获取与当前任务相似度最高的 top-K 成功轨迹

**关键洞察**：记忆读取与写入是协作关系——文本记忆通过文本相似性和辅助信息读取；参数化记忆通过更新后的参数隐式读取。
