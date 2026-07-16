---
forest: mi
tree: retrieval-association
branch: content-addressing
title: 内容寻址联想记忆
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
description: 大脑通过内容寻址存储实现联想回忆——从部分线索恢复完整记忆的机制
keywords:
  - 联想记忆
  - 内容寻址存储
  - CAM
  - 键值分离
  - 海马体索引
  - Transformer KV
atom_type: semantic
status: draft
refs:
  - "[mi] 键值记忆统一框架 | KV框架对CAM的抽象概括"
  - "[mi] 模式完成与CA3吸引子网络 | CAM的神经实现机制"
---

# 内容寻址联想记忆

大脑的记忆检索具有明显的联想特征：一个线索（声音、气味）可触发对整个事件的回忆。这本质上是联想记忆（associative memory）的体现，在算法上通过内容寻址存储（CAM）实现。

CAM是一种特殊存储器，通过内容本身而非预先分配的地址来定位数据。海马体CA3网络是CAM的神经基础——部分输入激活CA3时，网络通过其循环连接的能量景观收敛到存储的记忆，等价于CAM的匹配和读取操作。

键值记忆模型将这一过程抽象为"键"和"值"的分离架构：海马体存储用于检索的"键"（索引），新皮层存储记忆的"值"（内容）。检索时海马体通过匹配键定位记忆，然后从新皮层提取值。这与现代AI中Transformer的KV记忆机制不谋而合——通过Q与K的点积定位信息，从V中读取内容。大脑的联想记忆检索可被看作生物实现的键值存储系统。
