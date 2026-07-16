---
forest: memory-systems-ai
tree: t1-brain-memory
branch: b3-retrieval
leaf: l1-pattern-completion
title: 模式分离与模式完成的互补检索机制
version: 1.0.0
created: 2026-07-16
model: DeepSeek V4 Flash
source: "input/bim_source/人脑记忆机制的数据结构与算法分析.md"
refs:
  - "模式分离由齿状回（DG）执行，发生在编码阶段"
  - "模式完成由CA3自联想网络执行（Hopfield, 1982; Rolls, 2013）— 内容寻址存储"
  - "CA3的吸引子网络通过能量函数下降收敛到存储模式"
---

# 模式分离与模式完成的互补检索

模式分离和模式完成是海马体记忆系统的两大互补计算原理。**模式分离**（编码阶段，齿状回）将相似输入映射为差异很大的输出，防止记忆混淆。**模式完成**（检索阶段，CA3区）通过自联想网络（attractor network）从部分线索恢复完整记忆。CA3的循环连接类似于Hopfield网络：输入损坏模式后，网络通过能量函数下降收敛到最近的存储模式。这种互补机制对应内容寻址存储（CAM）的读取过程——通过部分内容直接定位并恢复完整记忆。
