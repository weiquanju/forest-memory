---
forest: agf
tree: 架构设计
branch: 新层设计
title: Layer 0 断言抽取层
version: 1.0.0
created: 2026-07-17
updated: 2026-07-17
description: MKE 架构新增 Layer 0——原始文本接入与断言抽取层，包括 Assertion Extractor、Assertion Deduplicator 和 SQLite assertion 表 DDL
keywords:
  - Layer 0
  - 断言抽取
  - Assertion Extractor
  - 原始文本接入
  - SQLite DDL
  - 断言去重
refs:
  - "[agf] 断言图与知识无损压缩 | 断言抽取流程"
  - "[agf] SSOT 双层扩展与六层架构 | 0层在整体架构中的位置"
  - "[mke] 五层架构蓝图 | 现有架构基础"
  - "[mke] SQLite表结构设计 | 现有表结构"
---

# Layer 0 断言抽取层

## 定位

在 MKE 现有五层架构的**最底部新增 Layer 0**——原始文本接入与断言抽取层。

```
┌─────────────────────────────────────────────────────────┐
│  Layer 0：原始数据接入与断言抽取层                    【新增】 │
│                                                           │
│  原始文本（Web/PDF/对话）                                  │
│       ↓                                                   │
│  ┌─────────────────┐                                      │
│  │  Assertion       │  LLM 驱动，(s,p,o,conf) 提取         │
│  │  Extractor       │  含：实体/关系/置信度/来源追溯         │
│  └────────┬────────┘                                      │
│           ↓                                               │
│  ┌─────────────────┐                                      │
│  │  Assertion       │  结构化比较而非向量相似度              │
│  │  Deduplicator    │  (s1,p1,o1) ≡ (s2,p2,o2)?           │
│  │                  │  → 合并 source_count += 1            │
│  └────────┬────────┘                                      │
│           ↓                                               │
│  输出：Assertion 列表 → 送入 Layer 1 常规流程                │
└─────────────────────────────────────────────────────────┘
```

这与 MKE 现有的五层架构互补——Layer 0 处理**原始文本→断言**的转化，Layer 1-5 处理**知识原子的组织与治理**。

## Assertion 实体

### SQLite DDL

```sql
CREATE TABLE assertion (
    id            TEXT PRIMARY KEY,          -- 断言唯一 ID
    subject       TEXT NOT NULL,              -- 主语（实体）
    predicate     TEXT NOT NULL,              -- 谓词（关系）
    object        TEXT NOT NULL,              -- 宾语（值/实体）
    confidence    REAL DEFAULT 0.0,           -- 置信度 [0, 1]
    source_count  INTEGER DEFAULT 1,          -- 来自多少独立原始文档
    canonical     TEXT,                       -- 规范表示（用于生成训练文本）
    cluster_id    TEXT NOT NULL,              -- 所属 Fact Cluster
    leaf_id       TEXT NOT NULL,              -- 所属知识细胞
    constraints   TEXT,                       -- 条件约束（场景/基准/度量）
    status        TEXT DEFAULT 'active',      -- active | superseded | deprecated
    created_at    TEXT,
    updated_at    TEXT,
    FOREIGN KEY (cluster_id) REFERENCES fact_cluster(id),
    FOREIGN KEY (leaf_id) REFERENCES leaf(id)
);

-- 断言级去重不需要向量相似度——直接比较 (s, p, o) 三元组
CREATE UNIQUE INDEX idx_assertion_spo ON assertion(subject, predicate, object);
```

### Assertion 与 Leaf 的关系

```
Leaf（知识细胞）:
  ├── title: "A18 芯片性能分析"
  ├── content: "全文论述..."（完整语境，LLM 消费）
  ├── assertions:
  │     ├── {s: iPhone16, p: uses_chip,    o: A18, conf: 0.98, source_count: 47}
  │     ├── {s: A18,      p: perf_gain,    o: 30%, conf: 0.90, source_count: 32}
  │     └── {s: A18,      p: manufactured_by, o: TSMC, conf: 0.97, source_count: 28}
  └── refs: [...]
```

**断言是 Leaf 的索引，不是替代**——Leaf 的 content 字段始终保留完整论述。断言用于精确去重和结构化检索，LLM 消费时实际注入的是原始 Leaf 正文。

## Assertion Deduplicator

与 MKE 现有的交叉声明检测（向量相似度 + LLM 裁决）不同，断言去重是**确定性的**：

```
输入: {s: iPhone16, p: uses_chip, o: A18, conf: 0.98}
现有: {s: iPhone16, p: uses_chip, o: A18, conf: 0.95, source_count: 46}

匹配: (s, p, o) 字符串完全一致 → UNIQUE INDEX 直接拦截

动作: 不写入新行 → 更新现有行的 source_count += 1
      若新 conf 与现有 conf 差异 > 0.2 → 触发冲突检测
```

> 断言去重的核心理论优势参见 [断言图与知识无损压缩](断言图与知识无损压缩.md) §"为什么断言图能做到 MKE 做不到的事"——结构化匹配从 D4（批判性分析）降到了字符串比较。

## 与 Layer 1 的衔接

```
Layer 0 输出: Assertion 列表 + 来源追溯
                ↓
Layer 1（数据接入与归一化层）:
  - 将原始文本 + 断言整合为 Leaf
  - Leaf.content 保持原始文本的完整论述
  - Leaf.assertions 挂载 Layer 0 的产出
```

这保持了 MKE 的核心不变——Layer 1 仍然产出知识细胞（Leaf），只是现在 Leaf 多了一个断言子层。
