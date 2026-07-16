---
forest: frs
tree: reasoning-output
branch: multimodal-reasoning
leaf_id: frs-multimodal-001
title: 多模态推理的机遇与空间操作瓶颈
type: observation
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
source: "[frs_source] §6.2 | STARE [54], Insight-V [53]"
---

# 多模态推理的机遇与空间操作瓶颈

## 当前能力基本面

多模态大模型（MLLM）推理需要理解图像、视频、音频等信息后进行推理，复杂性远高于纯文本推理。

## 关键瓶颈：空间操作

**STARE基准**评估表明 [54]：

| 任务类型 | MLLM表现 |
|---------|---------|
| 静态任务（计数） | 较好 |
| 2D基础变换 | 尚可 |
| 3D立方体展开折叠 | **接近随机猜测水平** |
| 七巧板拼图等多步视觉模拟 | **接近随机猜测水平** |

## 前沿方案：Insight-V

发表在CVPR 2025的**Insight-V**[53]：
- 生成长而稳健的多模态推理链
- 采用多智能体训练管道
- 在多个视觉推理基准上显著提升

**但**：即使Insight-V，在STARE的3D空间操作任务上增益也有限。

## 开放问题

- 视觉推理链的自动验证机制如何设计（类比RLVR的数学答案验证）？
- "视觉理解"和"逻辑推理"的质量能否分离评估？
