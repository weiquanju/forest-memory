---
forest: agent-memory-survey
tree: t1-memory-foundations
branch: b1-definitions
title: 记忆辅助的Agent-Environment交互模型
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
source: "[arXiv:2404.13501] Section 3.4"
refs:
  - "[t1-b1] Agent记忆定义 | 狭义/广义定义是W/P/R模型的前提"
  - "[t2-b3] 记忆操作实现 | Section 5.3 对应W/P/R的工程实现"
---

# 记忆辅助的Agent-Environment交互模型

## 三操作统一模型（W/P/R）

Agent-Environment 交互分为三个关键阶段，对应三种记忆操作：

| 阶段 | 操作 | 符号 | 功能 |
|------|------|------|------|
| 感知→存储 | **Memory Writing (W)** | `m^k_t = W({a^k_t, o^k_t})` | 将原始观测投影为实际存储的记忆内容 |
| 加工→优化 | **Memory Management (P)** | `M^k_t = P(M^k_{t-1}, m^k_t)` | 迭代处理记忆：摘要化/合并/遗忘 |
| 检索→行动 | **Memory Reading (R)** | `Ĥ^k_t = R(M^k_t, c^k_{t+1})` | 基于当前上下文提取相关记忆以驱动下一步行动 |

## 统一演化函数

三操作可合并为一个统一函数，描述从 `{a^k_t, o^k_t}` 到 `a^k_{t+1}` 的完整演化过程：

```
a^k_{t+1} = LLM{ R( P( M^k_{t-1}, W({a^k_t, o^k_t}) ), c^k_{t+1} ) }
```

该函数通过迭代展开即可得到完整的 Agent-Environment 交互过程。

## 实例与特化

不同工作对 W、P、R 有不同的实现特化：

| 模型 | W 特化 | P 特化 | R 特化 |
|------|--------|--------|--------|
| Reflexion [5] | 语言形式的经验反思 | 仅在 trial 结束时生效 | 与 P 等同（反思即检索） |
| Generative Agents [83] | 事件→自然语言存储 | 反射过程生成抽象思考 | 基于相似度+时间间隔+重要性的三准则检索 |
| MemoryBank [6] | 对话→daily summary | 持续评估→人格特质提炼 | Dual-tower 稠密检索 + FAISS 索引 |
| MemGPT [100] | Agent 自主决定更新 | 虚拟上下文管理 | 基于工作上下文检索 |

## 设计洞察

- **W/P/R 解耦**：三个操作可独立设计、独立优化。写入关注信息提取质量，管理关注长期一致性，读取关注检索精度与效率
- **操作依赖性**：写入形态直接影响读取方式——文本记忆通过相似度检索，参数化记忆通过隐式推理
- **开放问题**：当前研究中 P（管理操作）最不成熟，大部分系统仅支持简单的摘要或反射，缺乏对遗忘、冲突消解等高级管理策略的系统设计
