---
forest: memory-systems-ai
tree: t1-brain-memory
branch: b3-retrieval
leaf: l2-associative-memory
title: 联想记忆与内容寻址存储（CAM）
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
model: DeepSeek V4 Flash
source: "input/bim_source/人脑记忆机制的数据结构与算法分析.md"
refs:
  - "海马体CA3网络是生物实现的内容寻址存储器（CAM）的神经基础"
  - "键值记忆模型（Gershman et al., 2025）— 海马体编码键（索引）、新皮层存储值（内容）"
  - "Transformer的KV机制与大脑键值框架在结构上的相似性"
---

# 联想记忆与内容寻址存储

大脑的记忆检索具有明显的联想特征：一个线索可触发对整个事件的回忆。这本质上是**内容寻址存储（CAM）**的体现——通过内容的一部分来检索完整内容，而非通过预先分配的地址。海马体-皮层系统正是一种生物实现的CAM。**键值记忆模型**将这一过程进一步抽象为"键"和"值"的分离架构：海马体存储用于检索的"键"（索引），新皮层存储记忆的"值"（内容）。这种键值分离使得检索更高效——海马体只需处理轻量索引信息，新皮层作为大型数据库存储具体内容。这与现代AI中Transformer的键值对（KV）记忆机制高度呼应。
