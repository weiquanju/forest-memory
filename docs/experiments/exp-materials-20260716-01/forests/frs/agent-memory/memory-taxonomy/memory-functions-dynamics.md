---
forest: frs
tree: agent-memory
branch: memory-taxonomy
leaf_id: frs-mem-tax-003
title: 记忆功能分类与动态过程
type: concept
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
source: "[frs_source] §3.1 功能(Functions)与动态过程(Dynamics) | Hu et al., arXiv:2512.13564, 2025 [16]"
refs:
  - "[frs-mem-tax-001] 三维统一分类框架 | 功能与动态是另外两个维度"
---

# 记忆功能分类与动态过程

## 功能维度（Functions）

| 类型 | 内容 | 典型场景 |
|------|------|---------|
| **事实性记忆 (Factual)** | 知识 | 存储世界知识、领域事实 |
| **经验性记忆 (Experiential)** | 技能和洞察 | 记录任务执行的经验轨迹 |
| **工作记忆 (Working Memory)** | 主动上下文管理 | 维护当前任务的上下文状态 |

## 动态过程维度（Dynamics）

| 阶段 | 描述 | 对应生物记忆类比 |
|------|------|----------------|
| **形成 (Formation)** | 提取和编码新记忆 | 编码/巩固 |
| **演化 (Evolution)** | 记忆的巩固与遗忘 | 突触可塑性/记忆衰减 |
| **检索 (Retrieval)** | 访问已存储的记忆 | 回忆/线索提取 |

## 三维交叉分析

任一Agent记忆实例可在三个维度上交叉定位。例如：
- **Mem0的对话摘要** = 令牌级载体 × 经验性功能 × 检索阶段
- **模型微调知识** = 参数级载体 × 事实性功能 × 形成阶段
- **KV cache** = 潜在级载体 × 工作记忆功能 × 形成+检索阶段

这种交叉定位有助于系统化地分析记忆系统的设计空间和权衡。
