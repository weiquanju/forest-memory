---
forest: agf
tree: 研究方向
branch: 分子层
title: Fact Cluster 分子层设计
version: 1.0.0
created: 2026-07-17
updated: 2026-07-17
description: Fact Cluster 作为 Leaf 和 Assertion 之间的必要中间层——解决检索时的语义撕裂和冲突检测的复杂度爆炸
keywords:
  - Fact Cluster
  - 分子层
  - 检索完整性
  - 语义内聚
  - 冲突检测优化
  - 聚类
refs:
  - "[agf] 知识原子重定义与层级模型 | 分子层在层级中的位置"
  - "[agf] 性能影响与架构张力 | 冲突检测复杂度优化"
  - "[agf] 收益与弊端分析 | 弊端2 碎片化"
---

# Fact Cluster 分子层设计

## 为什么 Fact Cluster 必须存在

引入断言层后，如果没有 Fact Cluster，Assertion 表是一个扁平的三元组集合。这会导致两个严重问题：

### 问题 1：检索时的语义撕裂

```
Leaf "A18 芯片性能分析" → 30 条断言（扁平列表）
  
  {A18, uses_fab, TSMC}
  {A18, process, N3E}
  {A18, transistor_count, 28B}
  {A18, geekbench_score, 3200}
  {A18, perf_gain, 30%}
  ...25 more...

搜索 "A18 的制造工艺":
  → 返回 {A18, uses_fab, TSMC} ✓
  → 返回 {A18, process, N3E} ✓
  → 不返回 {A18, transistor_count, 28B} ✗（语义相关但关键词不匹配）
  
  LLM 收到的是一堆无序的事实碎片，丢失了关联关系
```

### 问题 2：冲突检测复杂度爆炸

```
无 Fact Cluster：O(n²) 全量 pairwise 比较
  5000 万断言 → ~1.25×10¹⁵ 次比较 → 不可行

有 Fact Cluster：O(k²)，k = 簇内断言数（通常 2-10）
  冲突检测在每个簇内独立执行 → 完全可行
```

## Fact Cluster 设计

### 表结构

```sql
CREATE TABLE fact_cluster (
    id          TEXT PRIMARY KEY,
    label       TEXT NOT NULL,       -- "A18 工艺信息"（人类可读）
    description TEXT,                 -- 簇的描述
    leaf_id     TEXT NOT NULL,       -- 所属知识细胞
    created_at  TEXT,
    FOREIGN KEY (leaf_id) REFERENCES leaf(id)
);

-- assertion 表中通过 cluster_id 建立关联
ALTER TABLE assertion ADD COLUMN cluster_id TEXT NOT NULL
    REFERENCES fact_cluster(id);
```

### 工作原理

```
Leaf "A18 芯片性能分析":
  ├── Fact Cluster "A18 工艺信息":
  │     ├── {A18, manufactured_by, TSMC}
  │     ├── {A18, process_node, N3E}
  │     └── {A18, transistor_count, 28B}
  │
  ├── Fact Cluster "A18 性能数据":
  │     ├── {A18, geekbench_score, 3200}
  │     ├── {A18, perf_gain, 30%}
  │     └── {A18, baseline, A17}
  │
  └── Fact Cluster "A18 市场定位":
        ├── {A18, competitor, Snapdragon_8_Gen4}
        └── {A18, market_segment, premium}
```

### Fact Cluster 带来的三项能力

| 能力 | 机制 |
|------|------|
| **检索完整性** | 命中簇内一条断言 → 返回整个簇 + 可选 Leaf 正文。Agent 获得语义完整的知识包 |
| **簇内一致性校验** | 同一簇内不应出现矛盾断言（如 perf_gain 30% 和 perf_gain 25%）。冲突检测 O(k²) << O(n²) |
| **检索上下文理解** | 簇的 label 和 description 提供语义锚点——Agent 知道"我现在在处理工艺信息还是性能数据" |

## 簇的生成方式

| 方式 | 说明 | 成本 |
|------|------|:---:|
| **LLM 语义聚类** | 在断言提取时同步分配 cluster | 低（与提取合并为一次 API 调用） |
| **实体共现** | 共享同一 subject 的断言自动聚合 | 极低（规则驱动） |
| **人工标注** | 对关键知识域手动划分簇 | 高（不适合大规模） |

### 推荐策略

```
Step 1: 实体共现粗聚合（自动）
  → 所有 subject=A18 的断言 → 初始簇

Step 2: LLM 语义细化（自动 + 一次 API 调用）
  → 将初始簇按语义拆分为子簇（工艺/性能/定位）
  → 赋予 label 和 description

Step 3: 人工审核（可选）
  → 仅对核心森林的 10% 的簇进行人工验证
```

> 为什么不往上加 Tissue（组织层）的完整论证参见 [知识原子重定义与层级模型](知识原子重定义与层级模型.md) §"为什么不需要 Tissue"——核心原则：每一层都必须引入新的治理能力，Tissue 不带来任何新能力。
