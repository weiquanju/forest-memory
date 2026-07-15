# 索引文件生成模板（Index Generation Template）

## 概述

Step 6 为森林的每个层级生成标准的 `index.md` 元数据文件。索引文件是森林的"门面"——它们让读者（人类和未来的 AI agent）能够快速理解森林的全貌和导航到具体的 Leaf。

## 层级结构

```
<forest_root>/
├── index.md                    ← Forest 级索引（必填）
├── .experiment_metadata.yaml   ← 实验元数据（必填，见 Step 8）
├── tree-a/
│   ├── index.md                ← Tree 级索引（推荐）
│   ├── branch-a1/
│   │   ├── leaf-a1-1.md        ← 知识原子（YAML Frontmatter + 正文）
│   │   └── leaf-a1-2.md
│   └── branch-a2/
│       └── ...
├── tree-b/
│   ├── index.md
│   └── ...
└── citation_audit_log.md       ← 引用审计日志（如有）
```

## Forest 级索引模板

```markdown
---
forest: <forest_id>
title: <森林中英文名称>
version: 1.0.0
created: YYYY-MM-DD
updated: YYYY-MM-DD
description: >
  一句话概括森林的定位、覆盖范围和独特价值。
  应包含：(1) 领域定位 (2) 覆盖的子领域 (3) 与其他 Forest 的关系。
source: "[来源类型] 来源描述 | URL（如有）"
keywords:
  - 关键词1
  - 关键词2
  - 关键词3
refs:
  - "[其他forest_id] 文档标题 | 跨森林引用说明"
---

# <森林中文名称>

## 定位

一段话（3-5 句）详细说明：
1. 本森林的核心研究领域是什么
2. 本森林在整体项目中的角色是什么
3. 本森林的独特贡献是什么（与其他 Forest 区分开）

## 森林内文档

<!-- 每棵 Tree 用二级标题列出 -->

### 树：<Tree1 中文名>

| 文档 | 说明 |
|------|------|
| [文档1](tree1/branch/leaf1.md) | 一句话说明该 Leaf 的内容 |
| [文档2](tree1/branch/leaf2.md) | ... |
| ... | ... |

### 树：<Tree2 中文名>

...（同上格式）...

### 树：<TreeN 中文名>

...（同上格式）...

## （可选）与其他森林的关系

如果本 Forest 向其他 Forest 注入知识或有消费关系，在此列出：

| 关系 | 目标 Forest | 注入/消费内容概要 |
|------|------------|------------------|
| 注入 | [mke] | 7 项知识：BTSP→P0优先级, CAM→k-hop搜索, ... |
| 消费 | [frs] | 方法论参照和评测基准 |

## （可选）版本历史

| 版本 | 日期 | 变更说明 |
|------|------|---------|
| 1.0.0 | YYYY-MM-DD | 初始版本，N 个文档 |
```

## Tree 级索引模板

```markdown
---
forest: <forest_id>
tree: <tree_id>
title: <树中文名称>
version: 1.0.0
created: YYYY-MM-DD
updated: YYYY-MM-DD
description: >
  这棵 Tree 的定位和覆盖范围。
  说明它在 Forest 中的角色，以及与其他 Tree 的关系。
keywords:
  - 关键词1
  - 关键词2
refs:
  - "[同forest其他tree] 文档标题 | 引用说明（如有）"
  - "[其他forest] 文档标题 | 跨森林引用（如有）"
---

# <树中文名称>

## 定位

一段话说明这棵 Tree 的研究焦点和知识边界。

## 本树枝干与叶子

| 枝干 | 叶子文档 | 核心内容 |
|------|---------|---------|
| <Branch1> | [leaf1](path), [leaf2](path) | Branch 的简要概述 |
| <Branch2> | [leaf3](path) | ... |
| ... | ... | ... |

## （可选）与本 Forest 其他 Tree 的关系

| 关系 | 目标 Tree | 关系说明 |
|------|----------|---------|
| 基础→进阶 | [macro_architecture] | 本 Tree 的机制建立在宏观架构的基础上 |
| 并列 | [other_tree] | 两者分别从不同角度研究同一问题 |
```

## YAML Frontmatter 字段规范

### 所有文件共有的字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|:---:|------|
| `forest` | string | ✅ | 所属 Forest ID（如 `mke`, `bim`, `aic`） |
| `title` | string | ✅ | 文档标题 |
| `version` | semver | ✅ | 版本号（初始为 `1.0.0`）|
| `created` | date | ✅ | 创建日期（YYYY-MM-DD） |
| `updated` | date | ✅ | 最后更新日期 |
| `description` | string | ✅ | 一句话描述 |

### Leaf 特有的字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|:---:|------|
| `tree` | string | ✅ | 所属 Tree ID |
| `branch` | string | ✅ | 所属 Branch ID |
| `keywords` | list[string] | ✅ | 3-8 个关键词 |
| `source` | string | ✅ | 来源文献/URL |
| `refs` | list[string] | 推荐 | 引用列表 `[tree_id] title \| reason` |
| `atom_type` | enum | 推荐 | `conceptual`/`factual`/`procedural`/`reasoning` |
| `confidence` | float | 推荐 | 内容的可信度（0.0-1.0） |
| `status` | enum | 推荐 | `draft`/`reviewed`/`stable`/`deprecated` |

### Index 文件特有的字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|:---:|------|
| `tree` | string | ✅（Tree 级 index）| 所属 Tree ID |
| 无 `branch` | — | — | Index 文件不属于任何 Branch |
| 无 `keywords` | — | — | 可选（index 通常不需要 keywords）|

## 命名约定

| 对象 | 命名格式 | 示例 |
|------|---------|------|
| Forest 目录 | 小写连字符 | `brain-inspired-memory` |
| Tree 目录/ID | 小写连字符 | `micro-mechanisms` |
| Branch（仅在 index 中出现） | 中文或英文短语 | `突触可塑性` |
| Leaf 文件 | 中文.md | `Hebbian学习.md` |
| Leaf ID（用于 refs） | 中文标题 | `Hebbian学习` |
