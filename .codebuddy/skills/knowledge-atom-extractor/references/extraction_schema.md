# 抽取输出 JSON Schema 完整规范

## 顶层结构

```json
{
  "extraction_meta": { ... },
  "atoms": [ ... ],
  "references": [ ... ],
  "cross_declaration_warnings": [ ... ]
}
```

## extraction_meta

抽取过程的元信息，用于审计和追溯。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `source_file` | string | 是 | 输入文件路径或标识 |
| `source_hash` | string | 是 | 输入内容 SHA256 哈希 |
| `extraction_model` | string | 是 | 使用的 LLM 模型标识 |
| `extraction_timestamp` | string | 是 | ISO 8601 时间戳 |
| `forest_hint` | string | 否 | 调用方提供的森林 ID 提示（减少 LLM 判断偏差） |
| `tree_hint` | string | 否 | 调用方提供的树名称提示 |

示例：
```json
{
  "extraction_meta": {
    "source_file": "docs/architecture.md",
    "source_hash": "a1b2c3d4...",
    "extraction_model": "gpt-4o",
    "extraction_timestamp": "2026-07-15T10:30:00Z",
    "forest_hint": "mke",
    "tree_hint": "架构设计"
  }
}
```

## atoms[]

提取出的知识原子数组。一个输入文档可能拆分为多个原子（当原文包含多个独立概念时）。

### Atom 字段定义

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `forest` | string | 是 | 森林 ID，小写短标识符（如 `mke`、`backend`） |
| `tree` | string | 是 | 所属树名称 |
| `branch` | string | 是 | 所属枝干名称 |
| `title` | string | 是 | 知识原子标题，同时也是 Leaf 主键的一部分 |
| `description` | string | 是 | 一句话说明该知识原子的内容与用途（以核心价值为中心） |
| `keywords` | string[] | 是 | 检索关键字，3-8 个 |
| `atom_type` | enum | 否 | `semantic`（默认）/ `procedural` / `episodic` |
| `content_preview` | string | 是 | 正文摘要，前 200 字符 |
| `content_full` | string | 否 | 完整正文内容（可选，若直接生成 .md 文件时需要） |
| `depends_on` | string[] | 否 | 硬性前置依赖（必须先理解的知识原子标题列表） |
| `split_reason` | string | 否 | 若从文档中拆分出，说明拆分理由 |

### 约束规则

- `forest` + `tree` + `branch` + `title` 四元组在全局唯一
- `description` 不超过 120 字符
- `keywords` 至少 3 个，至多 8 个
- `content_preview` 恰好 200 字符（不足则取全文，超出则截断并加 `...`）
- `atom_type` 为 `episodic` 时，`content_preview` 应包含交互上下文摘要

示例：
```json
{
  "atoms": [
    {
      "forest": "mke",
      "tree": "元知识引擎",
      "branch": "存储设计",
      "title": "SQLite表结构设计",
      "description": "元知识引擎的 SQLite 数据库完整 DDL——七张核心表的字段定义与索引策略",
      "keywords": ["SQLite", "DDL", "表结构", "数据库设计", "索引策略"],
      "atom_type": "semantic",
      "content_preview": "使用 SQLite + sqlite-vec 作为存储引擎，单文件 domain_knowledge.db，核心表包括 Forest、Tree、Branch、Leaf、References、Vectors、Interaction_Memory...",
      "depends_on": ["五层架构蓝图", "知识领域森林理论"],
      "split_reason": null
    }
  ]
}
```

## references[]

文档间的引用关系，构成图网络的边。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `from_title` | string | 是 | 引用方知识原子的标题 |
| `to_forest` | string | 是 | 被引用方的森林 ID |
| `to_title` | string | 是 | 被引用方的标题 |
| `ref_type` | enum | 是 | 引用类型（见下方枚举） |
| `keyword` | string | 否 | 引用关键字（说明引用的具体内容） |

### ref_type 枚举值

| 值 | 说明 | 使用场景 |
|------|------|---------|
| `depends` | 硬性依赖 | B 必须理解 A 才能正确使用 |
| `extends` | 扩展 | B 是 A 的扩展或特化 |
| `implements` | 实现 | B 是 A 定义接口的实现 |
| `references` | 引用 | B 引用了 A 中的概念或参数 |
| `config` | 配置引用 | B 使用了 A 中定义的配置项 |
| `standard` | 标准引用 | B 遵循 A 中定义的标准 |

示例：
```json
{
  "references": [
    {
      "from_title": "SQLite表结构设计",
      "to_forest": "mke",
      "to_title": "五层架构蓝图",
      "ref_type": "references",
      "keyword": "第二层存储映射"
    },
    {
      "from_title": "SQLite表结构设计",
      "to_forest": "mke",
      "to_title": "知识原子规范",
      "ref_type": "standard",
      "keyword": "Leaf表字段定义"
    }
  ]
}
```

## cross_declaration_warnings[]

检测到的潜在交叉声明。LLM 在抽取时若发现候选原子与已有知识可能重复，必须在此字段显式输出。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `detected_in` | string | 是 | 重复内容在输入文档中的位置（行号或段落标识） |
| `duplicates` | string | 是 | 已有知识原子的 `forest:tree:branch:title` 标识 |
| `duplicate_type` | enum | 是 | `exact`（完全重复）/ `partial`（部分重复）/ `semantic`（语义重复） |
| `suggestion` | string | 是 | 建议操作（引用而非重新声明） |
| `confidence` | float | 是 | 置信度 0-1 |

示例：
```json
{
  "cross_declaration_warnings": [
    {
      "detected_in": "第 15-20 行",
      "duplicates": "mke:元知识引擎:数据规范:知识原子规范",
      "duplicate_type": "partial",
      "suggestion": "请引用 [mke] 知识原子规范 | 字段定义，而非重复声明 Frontmatter 规范",
      "confidence": 0.89
    }
  ]
}
```

## 完整输出示例

```json
{
  "extraction_meta": {
    "source_file": "docs/storage_design.md",
    "source_hash": "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08",
    "extraction_model": "gpt-4o",
    "extraction_timestamp": "2026-07-15T10:30:00Z",
    "forest_hint": "mke",
    "tree_hint": "存储设计"
  },
  "atoms": [
    {
      "forest": "mke",
      "tree": "元知识引擎",
      "branch": "存储设计",
      "title": "SQLite表结构设计",
      "description": "元知识引擎的 SQLite 数据库完整 DDL——七张核心表的字段定义与索引策略",
      "keywords": ["SQLite", "DDL", "表结构", "数据库设计", "索引策略"],
      "atom_type": "semantic",
      "content_preview": "使用 SQLite + sqlite-vec 作为存储引擎...",
      "depends_on": ["五层架构蓝图"],
      "split_reason": null
    }
  ],
  "references": [
    {
      "from_title": "SQLite表结构设计",
      "to_forest": "mke",
      "to_title": "五层架构蓝图",
      "ref_type": "references",
      "keyword": "第二层存储映射"
    }
  ],
  "cross_declaration_warnings": []
}
```
