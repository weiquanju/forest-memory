---
forest: memory-systems-ai
tree: t3-knowledge-reasoning
branch: b3-reasoning
leaf: l1-reasoning-benchmarks
title: 推理能力评估基准的范式演进
version: 1.0.0
created: 2026-07-16
model: DeepSeek V4 Flash
source: "input/frs_source/AI与大模型在知识领域、Agent记忆、推理数据及推理关系中的前沿研究综述.md"
refs:
  - "GSM8K (Cobbe et al., 2021, arXiv:2110.14168) — 数学推理基准"
  - "MATH (Hendrycks et al., 2021, arXiv:2103.03874) — 数学问题求解"
  - "STARE (Li et al., 2025, arXiv:2506.04633) — 多模态空间推理"
  - "Insight-V (Dong et al., 2024, arXiv:2411.14432, CVPR 2025) — 长链视觉推理"
---

# 推理能力评估基准的范式演进

推理评估从**静态数学基准**（如GSM8K、MATH）向**动态多维度评估**演进。当前基准覆盖：数学推理（GSM8K、MATH）、多模态推理（Insight-V、STARE）、Agent记忆（MemBench、MemoryArena）。**STARE**（Li et al., 2025, arXiv:2506.04633）专门测试多模态模型的空间操作能力，揭示当前模型在此类推理上的瓶颈。范式演进方向是企业应用对推理能力提出更高要求：不仅要准确，还要可解释、可溯源。
