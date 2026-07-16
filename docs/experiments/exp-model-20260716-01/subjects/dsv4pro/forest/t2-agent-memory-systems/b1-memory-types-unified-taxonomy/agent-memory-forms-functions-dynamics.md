---
forest: memory-systems-ai
tree: t2-agent-memory-systems
branch: b1-memory-types-unified-taxonomy
leaf: agent-memory-forms-functions-dynamics
title: Agent记忆的载体-功能-动态三维分类
created: 2026-07-16
model: DeepSeek V4 Pro
source:
  - "arXiv:2404.13501"
  - "frs_source/AI与大模型在知识领域、Agent记忆、推理数据及推理关系中的前沿研究综述.md"
refs:
  - "[t2-b2] 记忆实现架构与前沿 | 分类框架在Mem0等系统中的实例化"
  - "[t1-b1] 人脑模块化记忆分类 | 人脑分类对AI分类的启发"
---

# Agent记忆的载体-功能-动态三维分类

## 框架来源

Hu et al.（2025, arXiv:2512.13564）系统综述提出了统一的 Agent 记忆分类框架，从三个维度系统化梳理 LLM Agent 记忆。

## 维度一：载体形式（Forms）

| 级别 | 特征 | 示例 |
|------|------|------|
| **令牌级（Token-level）** | 显式且离散 | 对话历史 |
| **参数级（Parametric）** | 隐式权重 | 模型参数 |
| **潜在级（Latent）** | 隐状态 | RNN 隐状态 |

## 维度二：功能（Functions）

| 类型 | 内容 |
|------|------|
| **事实性记忆（Factual）** | 知识 |
| **经验性记忆（Experiential）** | 技能和洞察 |
| **工作记忆（Working Memory）** | 主动上下文管理 |

## 维度三：动态过程（Dynamics）

| 阶段 | 描述 |
|------|------|
| **形成（Formation）** | 提取 |
| **演化（Evolution）** | 巩固与遗忘 |
| **检索（Retrieval）** | 访问策略 |

## 关键发现

**经验跟随属性（Experience-Following）**：当当前任务与检索到的记忆高度相似时，Agent 往往输出与记忆中相似的答案。这有助于复用成功经验，但也可能导致错误累积——记忆中的错误输出可能在后续任务中被复制甚至放大。

**错位经验重放**：某些看似正确的记忆在作为示例时可能对当前任务价值有限甚至具有误导性。

## 与相关概念的区别

该三维分类框架有助于区分 Agent 记忆与 RAG 和上下文工程等邻近概念。RAG 更多对应"检索外部知识"的动态过程，而 Agent 记忆还涵盖内部经验积累与演化。
