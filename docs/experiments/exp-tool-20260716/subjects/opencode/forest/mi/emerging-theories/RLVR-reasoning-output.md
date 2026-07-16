---
forest: mi
tree: emerging-theories
branch: rlvr
title: RLVR与推理输出关系
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
description: RLVR训练范式对推理深度与输出质量的协同影响及多模态推理瓶颈
keywords:
  - RLVR
  - 推理深度
  - 校准退化
  - 多模态推理
  - 空间操作
  - 输出可靠性
atom_type: semantic
status: draft
refs:
  - "[mi] 推理基准演进 | 动态基准支撑RLVR评估"
  - "[mi] 知识图谱与LLM融合 | 知识增强弥补RLVR纯参数化推理的局限"
---

# RLVR与推理输出关系

RLVR（Reinforcement Learning from Verifiable Rewards）是提升LLM推理深度的关键训练范式。模型规模、推理深度（chain-of-thought长度）与RLVR训练三者之间存在协同效应——更大的模型通过更长的推理链获得更大的RLVR增益。

**校准退化问题**：虽然RLVR显著提升推理准确率，但过度RLVR训练可能导致模型的置信度校准退化——模型在错误答案上表现出过高置信度。这与人类"自信但错误"的认知偏差有相似性。

**多模态推理瓶颈**：当前MLLM在多模态推理中面临空间操作瓶颈——模型在空间关系理解、视觉推理和结构操作任务中表现显著弱于纯文本推理。这表明多模态推理需要新的记忆和表示机制来支持空间信息的结构化编码和检索。RLVR与结构化知识（KG/GraphRAG）的结合是克服这一瓶颈的有前景方向。
