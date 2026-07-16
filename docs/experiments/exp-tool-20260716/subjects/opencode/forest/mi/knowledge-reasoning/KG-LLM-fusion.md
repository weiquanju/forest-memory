---
forest: mi
tree: knowledge-reasoning
branch: KG-fusion
title: 知识图谱与LLM融合
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
description: 通过知识图谱补偿LLM知识短板——ToG/PoG/KG-Agent/KG-RAR等方法对比
keywords:
  - 知识图谱
  - LLM推理
  - ToG
  - PoG
  - 多跳推理
  - 知识可追溯性
atom_type: semantic
status: draft
refs:
  - "[mi] GraphRAG范式 | GraphRAG作为KG融合的最新范式"
  - "[mi] Agent记忆定义与分类 | 外部知识作为Agent记忆来源"
---

# 知识图谱与LLM融合

知识图谱（KG）以结构化形式存储大量事实，补偿LLM的内部隐式知识缺陷，增强模型在知识密集型任务中的表现。

**Paths-over-Graph（PoG）**：三阶段动态多跳路径探索，将LLM知识+KG事实知识结合。在GPT-3.5-Turbo上相较ToG准确率提升18.9%，PoG+GPT-3.5-Turbo甚至超过ToG+GPT-4达23.9%。

**Think-on-Graph（ToG）**：提出"LLM⊗KG"深度整合范式，LLM作为Agent在KG上交互式beam search探索推理路径。关键贡献在于证明了知识可追溯性——每一步推理都可回溯到KG中的具体三元组。

**KG-Agent**：自主LLM Agent框架，集成多功能工具箱、KG执行器和知识记忆，仅用10K样本微调LLaMA-7B即可在KGQA任务上超越更大模型的SOTA方法。

**KG-RAR**：过程导向知识图谱+分层检索策略+奖励模型（PRP-RM），在Math500和GSM8K上使用Llama-3B相较基线提升20.73%。关键启示：结构化知识有效补充LLM参数化记忆，在复杂推理任务中表现更佳。
