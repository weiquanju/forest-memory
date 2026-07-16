---
forest: memory-systems-ai
tree: t2-agent-memory
branch: b2-operations
leaf: l3-memory-reading
title: 代理记忆的读取与检索机制
version: 1.0.0
created: 2026-07-16
model: DeepSeek V4 Flash
source: "input/papers/2404.13501.md"
refs:
  - "记忆读取：从存储中检索相关记忆支持当前决策"
  - "检索策略：精确匹配、语义相似度搜索、注意力机制"
  - "读取时机：主动检索（根据需求触发）vs 被动检索（自动激活相关记忆）"
---

# 代理记忆的读取与检索机制

记忆读取（Memory Reading）是从存储中检索相关信息以支持当前决策的过程。检索策略包括：**精确匹配**（基于标识符）、**语义相似度搜索**（基于嵌入向量的最近邻查找）、**注意力机制**（基于查询与存储内容的匹配评分）。读取时机分为**主动检索**（Agent根据当前需求触发查询）和**被动检索**（系统自动激活与当前上下文相关的记忆）。有效的读取机制需要在检索精度、召回率和响应速度之间取得平衡。
