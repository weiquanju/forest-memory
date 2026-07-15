---
forest: mke
tree: 架构设计
branch: 存储设计
title: SQLite 表结构设计
version: 1.0.0
created: 2026-07-12
updated: 2026-07-12
description: 元知识引擎的 SQLite 数据库完整 DDL——Forest、Tree、Branch、Leaf、References、Vectors、Interaction_Memory 七张核心表的字段定义与索引策略
keywords:
  - SQLite
  - DDL
  - 表结构
  - 数据库设计
  - 索引策略
refs:
  - "[mke] 五层架构蓝图 | 第二层知识构建层和第四层记忆融合层的存储映射"
  - "[mke] 知识原子规范 | Leaf 表字段与 YAML Frontmatter 的映射关系"
  - "[mke] 单一职责与引用机制 | References 表的应用场景"
  - "[mke] 渐进式检索引擎 | Vectors 表的检索用途"
---

# SQLite 表结构设计

## 设计原则

- 所有表位于单个 SQLite 文件 `domain_knowledge.db`
- 使用 `WITHOUT ROWID` 优化主键查询（Leaf 表除外，因其 Text 主键）
- 外键约束通过应用层保证（SQLite 默认不强制外键，需 `PRAGMA foreign_keys = ON`）
- 向量数据通过 sqlite-vec 扩展以虚拟表存储

## DDL

### 1. Forest 表

```sql
CREATE TABLE IF NOT EXISTS forest (
    id          TEXT PRIMARY KEY,          -- 森林 ID，如 'mke', 'aic'
    name        TEXT NOT NULL,             -- 森林名称
    description TEXT NOT NULL,             -- 森林描述
    index_path  TEXT NOT NULL,             -- 索引文件相对路径
    version     TEXT NOT NULL DEFAULT '1.0.0',
    created_at  TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at  TEXT NOT NULL DEFAULT (datetime('now'))
);
```

### 2. Tree 表

```sql
CREATE TABLE IF NOT EXISTS tree (
    id          TEXT PRIMARY KEY,          -- 'forest_id:tree_name'
    forest_id   TEXT NOT NULL REFERENCES forest(id),
    name        TEXT NOT NULL,             -- 树名称
    description TEXT,
    created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_tree_forest ON tree(forest_id);
```

### 3. Branch 表

```sql
CREATE TABLE IF NOT EXISTS branch (
    id          TEXT PRIMARY KEY,          -- 'tree_id:branch_name'
    tree_id     TEXT NOT NULL REFERENCES tree(id),
    name        TEXT NOT NULL,             -- 枝干名称
    description TEXT,
    created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_branch_tree ON branch(tree_id);
```

### 4. Leaf 表（核心）

```sql
CREATE TABLE IF NOT EXISTS leaf (
    id          TEXT PRIMARY KEY,          -- 'forest:tree:branch:title'
    forest_id   TEXT NOT NULL REFERENCES forest(id),
    tree_id     TEXT NOT NULL REFERENCES tree(id),
    branch_id   TEXT NOT NULL REFERENCES branch(id),
    title       TEXT NOT NULL,             -- 文档标题（知识原子标识）
    file_path   TEXT NOT NULL,             -- 相对于森林根目录的 .md 文件路径
    content_hash TEXT NOT NULL,            -- SHA256 哈希，用于变更检测
    version     TEXT NOT NULL DEFAULT '1.0.0',
    status      TEXT NOT NULL DEFAULT 'draft'
                CHECK (status IN ('draft','reviewed','stable','deprecated')),
    description TEXT NOT NULL,             -- 从 YAML Frontmatter 提取
    keywords    TEXT,                      -- JSON 数组字符串
    token_count INTEGER,                   -- 内容 Token 数，用于检索窗口计算
    created_at  TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_leaf_forest   ON leaf(forest_id);
CREATE INDEX IF NOT EXISTS idx_leaf_tree     ON leaf(tree_id);
CREATE INDEX IF NOT EXISTS idx_leaf_branch   ON leaf(branch_id);
CREATE INDEX IF NOT EXISTS idx_leaf_status   ON leaf(status);
```

### 5. References 表（引用图谱）

```sql
CREATE TABLE IF NOT EXISTS reference (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    from_leaf_id TEXT NOT NULL REFERENCES leaf(id),
    to_leaf_id   TEXT NOT NULL REFERENCES leaf(id),
    ref_type     TEXT NOT NULL
                 CHECK (ref_type IN ('depends','extends','implements','references','config','standard')),
    keyword      TEXT,                     -- 引用关键字（从 refs 解析）
    created_at   TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE(from_leaf_id, to_leaf_id, ref_type)
);

CREATE INDEX IF NOT EXISTS idx_ref_from  ON reference(from_leaf_id);
CREATE INDEX IF NOT EXISTS idx_ref_to    ON reference(to_leaf_id);
CREATE INDEX IF NOT EXISTS idx_ref_type  ON reference(ref_type);
```

### 6. Vectors 表（通过 sqlite-vec 扩展）

```sql
-- sqlite-vec 虚拟表，768 维（text-embedding-3-small）或 1536 维（text-embedding-3-large）
CREATE VIRTUAL TABLE IF NOT EXISTS vec_leaf USING vec0(
    leaf_id   TEXT PRIMARY KEY,           -- 对应 leaf.id
    embedding FLOAT[768]                  -- 维度取决于嵌入模型
);
```

### 7. Interaction_Memory 表（Agent 记忆融合）

```sql
CREATE TABLE IF NOT EXISTS interaction_memory (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id        TEXT NOT NULL,       -- 会话标识
    query             TEXT NOT NULL,       -- 用户原始查询
    retrieved_leaf_ids TEXT,               -- JSON 数组：检索到的 leaf.id 列表
    final_answer      TEXT,                -- Agent 最终回答
    user_correction   TEXT,                -- 人工修正内容（覆盖原始文档）
    reasoning_trace   TEXT,                -- Agent 思考链/工具调用序列
    pattern           TEXT,                -- 提炼的策略模式（经验层）
    rating            INTEGER CHECK (rating BETWEEN 1 AND 5),  -- 用户评分
    created_at        TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_mem_session ON interaction_memory(session_id);
CREATE INDEX IF NOT EXISTS idx_mem_leaf_ids ON interaction_memory(retrieved_leaf_ids);
```

## 查询示例

### 通过森林 ID 获取所有叶子

```sql
SELECT l.* FROM leaf l
JOIN forest f ON l.forest_id = f.id
WHERE f.id = 'mke'
ORDER BY l.tree_id, l.branch_id, l.title;
```

### 1-hop 图扩散检索

```sql
-- 获取与指定叶子相关的所有引用叶子
SELECT l_to.title, l_to.file_path, r.ref_type, r.keyword
FROM reference r
JOIN leaf l_to ON r.to_leaf_id = l_to.id
WHERE r.from_leaf_id = 'mke:元知识引擎:存储设计:SQLite表结构设计';
```

### 高频引用检测（个性化 PageRank 的输入）

```sql
SELECT to_leaf_id, COUNT(*) as ref_count
FROM interaction_memory, json_each(retrieved_leaf_ids)
WHERE json_each.value = to_leaf_id
  AND user_correction IS NULL       -- 未被用户修正的引用
GROUP BY to_leaf_id
ORDER BY ref_count DESC
LIMIT 20;
```
