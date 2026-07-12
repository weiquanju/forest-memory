---
forest: mke
tree: 元知识引擎
branch: Agent Memory 集成
title: Agent Memory 能力对齐
version: 1.0.0
created: 2026-07-12
updated: 2026-07-12
description: 评估元知识引擎蓝图对 Agent Memory 完整能力框架的覆盖度——架构对齐、记忆类型覆盖、检索能力对照、生命周期管理
keywords:
  - Agent Memory
  - 记忆系统
  - 能力对齐
  - 覆盖度评估
refs:
  - "[mke] 五层架构蓝图 | 第四层记忆融合层"
  - "[mke] 渐进式检索引擎 | 检索策略"
  - "[aic] CEO子公司协作模型 | Agent Memory 的使用场景"
---

# Agent Memory 能力对齐

## 评估结论

元知识引擎蓝图已覆盖 Agent Memory 完整能力的约 **75-80%**。剩余 20-25% 为可迭代补全项（短期缓存、推理记忆、经验模式、BM25 检索），非架构缺陷。

## 一、架构对齐

| 业界 Agent Memory 架构 | 元知识引擎蓝图 |
|----------------------|--------------|
| 五层互补架构（持久化、结构化、搜索、注入、自动压缩） | 五层蓝图完全对应，额外多一层"知识治理"保障数据质量 |
| 短期缓存 + 长期检索双层记忆 | 通过 `Interaction_Memory` 表具备构建短期工作记忆的基础，仅需增加滑动窗口缓存（如保留最近 20 轮对话） |
| 图谱原生记忆（Graph-Native Memory） | 森林→树→枝干→叶 + 图引用是其轻量级实现 |

## 二、记忆类型覆盖

| 记忆类型 | 覆盖情况 | 实现方式 |
|---------|---------|---------|
| 情景记忆（Episodic） | ✅ 已覆盖 | `Interaction_Memory` 表记录对话历史 |
| 语义记忆（Semantic） | ✅ 已覆盖 | Leaf 节点存储领域知识事实 |
| 程序性记忆（Procedural） | ✅ 已覆盖 | 代码域 AST 提取函数/类/依赖关系 |
| 事实记忆（Factual） | ✅ 已覆盖 | 叶子节点存储参数、标准、配置 |
| 推理记忆（Reasoning） | ⚠️ 需补强 | 建议增加 `Reasoning_Trace` 字段记录思考链和工具调用序列 |

## 三、检索能力对照

| 检索能力 | 状态 | 说明 |
|---------|------|------|
| 向量语义搜索 | ✅ | sqlite-vec |
| 图关系遍历 | ✅ | References 表 + 1-hop 扩散 |
| 关键词匹配 | ⚠️ | 建议增加 SQLite FTS5 做 BM25 |
| 时序过滤 | ✅ | Content_Hash + Epoch_ID |
| 渐进式迭代检索 | ✅ | LLM 裁决 + 递归循环 |

## 四、记忆生命周期管理

| 生命周期环节 | 覆盖情况 | 实现 |
|------------|---------|------|
| 写入 | ✅ | 单一职责强制执行 + 引用去重（等于 Write Guard + Conflict Detection） |
| 读取 | ✅ | `retrieve(query)` 三段式检索 |
| 维护 | ✅ | 死链检测 + 版本快照 + 权重更新（个性化 PageRank） |
| 集成 | ✅ | Python API + 拼接至 Agent Prompt |

## 五、经验层补充建议

Agent Memory 框架除记忆层和上下文运行时外，还应有**经验层（Experience）**——从执行过程中提炼策略模式。

建议在 `Interaction_Memory` 表中增加：
- `Pattern` 字段：存储从成功/失败案例中提炼的策略模式（如"类似问题 X 的解决方案 Y 有效"）
- `Reasoning_Trace` 字段：记录 Agent 的思考链和工具调用序列

## 记忆回灌机制

- Agent 下次启动时查询 `Interaction_Memory` 表
- 找出高频引用的 `Leaf_ID`，自动提升该叶子的检索权重（个性化 PageRank）
- 用户修正过的答案挂载到对应叶子节点，优先级高于原始文档（个人经验覆盖标准文档）
