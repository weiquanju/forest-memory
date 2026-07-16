---
forest: agent-memory-survey
tree: t4-agent-applications
branch: b1-core-apps
title: 角色扮演与社会模拟中的记忆设计
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
source: "[arXiv:2404.13501] Section 7.1"
refs:
  - "[t1-b2] 认知心理学基础 | 角色记忆应与认知心理学理论对齐"
  - "[t2-b2] 参数化记忆 | Character-LLM使用SFT注入角色记忆"
  - "[t5-b2] 类人Agent记忆 | 人形Agent的记忆设计延伸"
---

# 角色扮演与社会模拟中的记忆设计

## 角色扮演（Role-playing）

记忆在角色扮演中的核心功能：**赋予角色独特的特征，使其区别于其他角色**。

### 代表性实现

| 模型 | 记忆构建方法 | 记忆形态 |
|------|------------|---------|
| Character-LLM [105] | Experience Uploading → SFT 注入参数 | 参数化（Fine-tuning） |
| ChatHaruhi [143] | 从剧本提取角色记忆 + 对话拼接 | 文本（Concatenation） |
| RoleLLM [145] | 角色特定知识 + 情景记忆（Context QA pairs） | 文本 |
| NarrativePlay [146] | 从叙事中提取人格特征，按相关性和重要性存储和检索 | 文本（Retrieval-based） |
| CharacterGLM [147] | 生成角色对话 → SFT 赋予对应风格 | 参数化（Fine-tuning） |

### 设计洞察

1. **一致性与辨识度**：记忆必须与角色特征一致——这是提升角色扮演真实感和社会模拟多样性的关键
2. **行为影响**：记忆应恰当地影响后续行为，确保角色行为的一致性和合理性
3. **认知对齐**：对于人形 Agent，记忆机制应与人类记忆特征对齐（遗忘、长短期记忆等）

## 社会模拟（Social Simulation）

社会模拟实质上是角色扮演的多 Agent 扩展，更关注多角色建模。

### 代表性实现

| 模型 | 记忆机制 | 模拟场景 |
|------|---------|---------|
| LyfeAgents [148] | Summarize-and-Forget | 社会场景中的自我监控 |
| S3 [2] | 每个 Agent 有独立 Memory Pool（在线平台用户消息） | 社交网络模拟 |
| Li et al. [163] | 对话上下文 + 经济环境 + 前几个月决策 | 宏观经济趋势模拟 |
| MetaAgents [109] | Profiles + Goals → 对话 + 个人反思 → 持续更新 | 求职场景模拟 |
| WarAgent [150] | 持续维护参与国对话记忆 | 战争决策模拟 |

## 跨应用设计模式

| 设计原则 | 角色扮演 | 社会模拟 |
|---------|---------|---------|
| 记忆一致性 | 与角色档案对齐 | 与全球经济/政治环境对齐 |
| 多源融合 | 剧本+对话+人格 | 环境+决策+对话 |
| 认知模拟 | 体现角色性格特征 | 模拟人类动态行为 |
