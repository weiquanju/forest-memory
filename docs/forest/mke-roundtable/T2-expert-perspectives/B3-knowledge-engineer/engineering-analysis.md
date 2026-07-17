---
forest: mrt
tree: T2-expert-perspectives
branch: B3-knowledge-engineer
title: 知识工程专家视角——工程可行性与分阶段构建策略
version: 1.0.0
created: 2026-07-17
updated: 2026-07-17
description: 从工程实施角度评估 MKE 六层架构的可构建性、技术栈风险和分阶段实施策略
keywords:
  - 工程可行性
  - 技术栈风险
  - 分阶段构建
  - 冒烟测试
  - 延迟预算
refs:
  - "[mke] 技术选型对比 | SQLite + sqlite-vec 的原始选型"
  - "[agf] 断言图框架 | Layer 0 的实现复杂度"
---

# 知识工程专家视角

## 核心判断

**MKE 六层架构可分阶段构建，但按全蓝图一次性实现是灾难性的。**

必须将六层架构拆为三层：

| 层级 | 内容 | 周期 |
|:---:|------|:---:|
| **MVP 层** | Layer 1 数据接入 + Layer 2 层级存储 + Layer 3 简化检索（无 LLM 裁决）| 2-4 周 |
| **优化层** | 图扩散 + LLM 裁决 + 记忆回灌 | 4-12 周（需条件验证）|
| **研究层** | AGF 断言抽取 + 三层冲突检测 + 全自动 Consolidation | 12+ 周或搁置 |

## 三大工程风险

### 风险 1：sqlite-vec 生态成熟度（🔴 高）

sqlite-vec 是社区项目，非 SQLite 官方扩展。Windows 下预编译 wheel 支持未知——编译 C 扩展的工具链要求高。

**缓解**：Day 1 冒烟测试。若 1 天无法让 sqlite-vec 工作，切换为 **ChromaDB + SQLite 分体方案**。

### 风险 2：LLM 裁决延迟爆炸（🔴 高）

五阶段检索中的阶段三（LLM 裁决）每次至少 1 次 API 调用（500ms-2s）。复杂查询可能需要 2-3 轮迭代 → 6-10 秒总延迟，对实时对话不可接受。

**缓解**：第一阶段不做 LLM 裁决。返回 Top K + confidence 分数，由消费端 LLM 自行决定是否满足。

### 风险 3：sentence-transformers 本地嵌入性能（🟡 中）

单文档嵌入 ~30ms（CPU），建库阶段 78 叶 = 2.3s（可接受）。但 Agent 写回场景下实时嵌入可能成为瓶颈。

**缓解**：全量建库时异步 CPU 嵌入；检索时单 query 嵌入约 30ms，在延迟预算内。

## 技术选型冒烟测试（第 1 步，1 天）

```bash
pip install sqlite-vec
pip install sentence-transformers
python -c "import sqlite_vec; print('ok')"
python -c "from sentence_transformers import SentenceTransformer; m = SentenceTransformer('all-MiniLM-L6-v2'); print(m.encode('hello').shape)"
```

任何一项不通过 → 立即调整技术选型。
