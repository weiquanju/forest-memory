# 森林索引文件模板

> **用途**：直接复制此模板作为新 Forest 的根目录 `index.md` 起始文件。
> **来源**：forest-generation-methodology Step 6 索引生成规范。

---

```markdown
---
forest: <forest_id>
title: <森林中英文名称>
version: 1.0.0
created: YYYY-MM-DD
updated: YYYY-MM-DD
description: >
  一句话概括：本森林的定位、覆盖范围和独特价值。
source: "[来源类型] 来源描述 | URL"
keywords:
  - 关键词1
  - 关键词2
  - 关键词3
refs:
  - "[其他forest] 文档标题 | 引用说明"
---

# <森林中文名称>

## 定位

<3-5 句话说明：(1) 核心研究领域 (2) 在项目中的角色 (3) 独特贡献>

## 森林内文档

### 树：<Tree1>
| 文档 | 说明 |
|------|------|
| [leaf](path) | 描述 |

### 树：<Tree2>
...

## 与其他森林的关系

| 关系 | 目标 | 内容 |
|------|------|------|
| 注入/消费 | [forest_id] | 概要 |
```
