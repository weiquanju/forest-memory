---
forest: agent-memory-survey
tree: t2-memory-implementation
branch: b2-forms
title: 文本记忆形态
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
source: "[arXiv:2404.13501] Section 5.2.1"
refs:
  - "[t2-b2] 参数化记忆 | 文本记忆与参数化记忆的对比分析"
  - "[t2-b2] 文本vs参数权衡 | 效果/效率/可解释性三维对比"
  - "[t2-b3] 记忆读取 | 文本记忆的检索方式取决于存储形态"
---

# 文本记忆形态

## 定位

文本形式是当前 Agent 记忆的**主流表示方法**，具有可解释性强、实现简单、读写效率高的特点。

## 四种文本记忆类型

文本记忆按存储策略分为四类，前三类记录交互循环内的信息，第四类记录循环外的信息：

### 1. Complete Interactions（完整交互）

**策略**：利用长上下文策略 [116] 存储所有 Agent-Environment 交互历史。

**代表工作**：
- LongChat [116]：Fine-tune 基础模型以更好地适应完整交互记忆
- MemorySandbox [117]：透明的交互式管理，在拼接前移除无关记忆
- Giraffe [118]、Focused Transformer [119]：增强 LLM 处理更长上下文的能力

**关键局限**：
| 问题 | 原因 |
|------|------|
| 计算成本高 | Attention 计算复杂度随序列长度二次增长 |
| 长度溢出 | 记忆长度可能超过预训练时的序列长度上限 |
| 位置偏差 | "Lost in the Middle" [120]：长上下文中的不同位置文本利用率不均 |

### 2. Recent Interactions（最近交互）

**策略**：基于局部性原理（Principle of Locality [121]），存储和维护最近获取的记忆。

**代表工作**：

| 模型 | 机制 | 特点 |
|------|------|------|
| SCM [98] | 基于 Cache 的 Flash Memory | 保留最近 t-1 步的观测 |
| MemGPT [100] | Working Context | 虚拟上下文管理的一部分 |
| RecAgent [95] | 短期记忆中间缓存 | 模拟人脑记忆机制 [122, 123] |

**关键权衡**：
- ✅ 高效聚焦近期信息
- ❌ 在长期任务中丢失关键历史信息——重视时效性本质上是忽视更早但可能关键的信息

### 3. Retrieved Interactions（检索交互）

**策略**：基于相关性、重要性和主题选择记忆内容，而非基于时间。

**代表工作**：

| 模型 | 检索策略 | 索引方式 |
|------|---------|---------|
| Generative Agents [83] | 余弦相似度 + 重要性 + 时效性三准则 | 嵌入向量 + 辅助信息 |
| MemoryBank [6] | Dual-tower 稠密检索 | FAISS [124] 索引 |
| RET-LLM [7] | Locality-Sensitive Hashing (LSH) | 元组数据库 |
| ChatDB [96] | SQL 语句生成 | 符号化记忆数据库 |

**关键权衡**：
- ✅ 包含远距离但关键的记忆
- ❌ 检索不准确可能获取无用信息；大规模检索计算成本高
- ❌ 仅处理同构信息（交互循环内），外部异构信息难以用同一方法

### 4. External Knowledge（外部知识）

通过工具调用将外部知识转化为记忆。详见 `external-knowledge-integration.md`。

## 四类文本记忆对比

| 类型 | 选择准则 | 信息完整性 | 计算效率 | 适用场景 |
|------|---------|:---:|:---:|------|
| Complete | 时间顺序 | 高 | 低 | 短对话/简单任务 |
| Recent | 时间窗口 | 中 | 高 | 实时交互 |
| Retrieved | 语义相关性 | 中 | 中 | 需要远距离信息 |
| External | 工具可用性 | 按需 | 中 | 需要专业知识 |
