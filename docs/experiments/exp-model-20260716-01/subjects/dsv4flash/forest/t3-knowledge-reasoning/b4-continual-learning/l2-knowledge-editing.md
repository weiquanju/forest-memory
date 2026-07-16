---
forest: memory-systems-ai
tree: t3-knowledge-reasoning
branch: b4-continual-learning
leaf: l2-knowledge-editing
title: 知识编辑—终身知识更新
version: 1.0.0
created: 2026-07-16
model: DeepSeek V4 Flash
source: "input/frs_source/AI与大模型在知识领域、Agent记忆、推理数据及推理关系中的前沿研究综述.md"
refs:
  - "WilKE — 终身知识编辑方法"
  - "PRUNE — 知识剪枝与编辑"
  - "CRAFT & KEDAS (Tang et al., 2025, arXiv:2508.01302) — 实时知识编辑对齐"
  - "Ngoli et al. (2026, arXiv:2606.10554) — 逻辑规则驱动的知识编辑基准"
---

# 知识编辑—终身知识更新

知识编辑（Knowledge Editing）允许在不需要重新训练的情况下对LLM中的特定知识进行精确修改。**WilKE**和**PRUNE**等方法通过定位和修改模型中与特定知识相关的参数来实现精准编辑。**CRAFT & KEDAS**（Tang et al., 2025, arXiv:2508.01302）探索了将知识编辑与模型对齐结合的方案。**Ngoli et al.**（2026, arXiv:2606.10554）提出了逻辑规则驱动的知识编辑基准，系统评估编辑的正确性和副作用。知识编辑是解决知识过时问题的关键技术，与持续学习形成互补。
