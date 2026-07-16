---
forest: frs
tree: reasoning-output
branch: model-comparison
leaf_id: frs-output-compare-001
title: 推理模型四维横向对比
type: analysis
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
source: "[frs_source] §6.3 推理能力对比与讨论"
refs:
  - "[frs-rlvr-001] RLVR训练范式"
  - "[frs-multimodal-001] 多模态推理瓶颈"
---

# 推理模型四维横向对比

## 对比矩阵

| 模型/方法 | 推理范式 | 亮点 | 已知局限 |
|------|---------|------|---------|
| DeepSeek-R1 [46] | RLVR (GRPO) | 推理能力可蒸馏至小模型 | 推理链过长时格式崩溃风险 |
| OpenAI o1 [47] | 内置隐式推理链 | 强推理能力开箱即用 | 推理过程不可见、API成本高 |
| DCPO [31] | 解耦推理与校准 | 解决RLVR校准退化 | 仅验证于数学推理领域 |
| Insight-V [53] | 长链视觉推理+多Agent | CVPR 2025，多模态突破 | 空间操作任务仍接近随机 |

## 三项开放问题

1. **Reward Hacking**：DCPO的校准优化是必要但不充分的缓解——reward hacking仍是深层风险
2. **推理深度边际收益递减**：更多推理步骤何时变成有害的冗长？最优推理深度尚未量化
3. **多模态推理的分离评估**：STARE暗示视觉理解和逻辑推理均可能独立构成瓶颈
