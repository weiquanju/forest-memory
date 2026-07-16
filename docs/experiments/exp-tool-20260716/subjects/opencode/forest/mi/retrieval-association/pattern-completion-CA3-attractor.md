---
forest: mi
tree: retrieval-association
branch: pattern-completion
title: 模式完成与CA3吸引子网络
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
description: 海马体CA3区域作为自联想吸引子网络实现模式完成的计算原理
keywords:
  - 模式完成
  - CA3
  - 吸引子网络
  - Hopfield网络
  - 自联想记忆
  - 能量函数
atom_type: semantic
status: draft
refs:
  - "[mi] 稀疏编码与模式分离 | 模式完成的互补编码机制"
  - "[mi] 内容寻址联想记忆 | CA3模式完成实现CAM读取"
---

# 模式完成与CA3吸引子网络

模式完成（pattern completion）与模式分离是海马体两大互补计算原理。模式分离发生在编码阶段（齿状回），模式完成发生在检索阶段（CA3区域）。

CA3是一个自联想网络（auto-associative network），其 recurrent collateral 突触连接形成吸引子网络（Hopfield, 1982; Rolls, 2013）。当部分记忆线索输入CA3时，循环连接将活动模式收敛到存储的完整记忆模式上，完成对整个记忆的检索。这类似于在Hopfield网络中，输入损坏的模式通过能量函数下降收敛到最近的存储模式。

在算法上，CA3的模式完成对应于内容寻址存储（CAM）的读取过程：通过部分内容（线索）直接定位并恢复完整内容。模式分离和模式完成的互补作用使记忆系统既能区分相似记忆（编码阶段），又能重建部分丢失的记忆（检索阶段），保证记忆检索的高效性和鲁棒性。
