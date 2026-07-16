---
forest: frs
tree: Agent记忆
branch: 记忆分类
title: Agent记忆统一三维分类框架
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
description: Hu等（2025）从载体形式（Token/Parametric/Latent）、功能（事实/经验/工作）、动态过程（形成/演化/检索）三维度系统分类Agent记忆
keywords:
  - Agent记忆
  - 三维分类
  - 载体形式
  - 功能分类
  - 动态过程
atom_type: semantic
status: draft
refs:
  - "[frs] 记忆对推理与输出质量的影响 | 三维分类的消费方视角"
---

# Agent记忆统一三维分类框架

## 三维度分类体系

### 载体形式（Forms）
| 级别 | 特征 | 示例 |
|------|------|------|
| 令牌级 | 显式且离散 | 对话历史 |
| 参数级 | 隐式权重 | 模型参数 |
| 潜在级 | 隐状态 | RNN隐状态 |

### 功能（Functions）
| 类型 | 内容 |
|------|------|
| 事实性记忆 | 知识 |
| 经验性记忆 | 技能和洞察 |
| 工作记忆 | 主动上下文管理 |

### 动态过程（Dynamics）
| 阶段 | 描述 |
|------|------|
| 形成 | 提取 |
| 演化 | 巩固与遗忘 |
| 检索 | 访问策略 |

该分类有助于区分 Agent 记忆与 RAG、上下文工程等相关概念（Hu et al., 2025, arXiv:2512.13564）。
