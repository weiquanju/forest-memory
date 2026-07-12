---
forest: mke
tree: 元知识引擎
branch: 知识抽取
title: LLM 知识抽取器设计
version: 1.0.0
created: 2026-07-12
updated: 2026-07-12
description: 利用大模型自动从现有文档中抽取实体、关系、层级结构的关键设计——System Prompt 策略、Few-shot 模板、输出 Schema 和交叉声明检测
keywords:
  - LLM抽取器
  - Few-shot
  - 知识抽取
  - System Prompt
  - 交叉声明检测
  - 自动化构建
refs:
  - "[mke] 五层架构蓝图 | 第二层知识构建层"
  - "[mke] 知识原子规范 | 输出的 Schema 定义"
  - "[mke] 单一职责与引用机制 | 交叉声明检测的触发条件"
  - "[mke] SQLite表结构设计 | 抽取结果的存储映射"
---

# LLM 知识抽取器设计

## 定位

利用 LLM 本身做自动化知识抽取——读取文档，自动提取实体、关系和层级结构，人工只做审核和修正。这是元知识引擎在建库阶段最关键的组件，决定了知识图谱的初始质量。

## 抽取流程

```
原始文档 (.md / .py 扫描结果)
        │
        ▼
┌─────────────────────────────┐
│  LLM 知识抽取器               │
│  System Prompt + Few-shot   │
└─────────────────────────────┘
        │
        ▼
   JSON 结构化输出
   { forest, tree, branch, leaves[], references[] }
        │
        ▼
┌─────────────────────────────┐
│  交叉声明检测器               │
│  与已有 Leaf 比较相似度        │
└─────────────────────────────┘
        │
   ┌────┴────┐
   ▼         ▼
 接受写入   拒绝并返回引用建议
```

## System Prompt 策略

```
你是一个领域知识抽取专家。你的任务是从给定的文档中提取结构化的知识原子。

## 提取规则

1. **层级归属**：判断文档应归属的森林（forest）、树（tree）、枝干（branch）
2. **单一职责**：每个知识原子只能声明一个核心概念，如果原文包含多个独立概念，拆分输出
3. **引用而非重复**：如果检测到某个定义/标准在别处已有权威来源，请输出引用关系而非重新声明
4. **元数据提取**：自动生成 title、description、keywords

## 输出 JSON Schema

{
  "atoms": [
    {
      "forest": "mke",
      "tree": "元知识引擎",
      "branch": "存储设计",
      "title": "SQLite表结构设计",
      "description": "...",
      "keywords": ["SQLite", "DDL", ...],
      "content_preview": "文档正文的前 200 字符摘要"
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
  "cross_declaration_warnings": [
    {
      "detected_in": "当前文档第 15-20 行",
      "duplicates": "mke:元知识引擎:数据规范:知识原子规范",
      "suggestion": "请引用 [mke] 知识原子规范 | 字段定义"
    }
  ]
}

## 质量要求
- description 必须是以该知识原子的"核心价值"为中心的一句话
- keywords 至少 3 个，至多 8 个
- 交叉声明检测必须在 JSON 中显式输出，不要只在文本中提示
```

## Few-shot 模板

### 示例输入

```markdown
# 数据存储方案

我们使用 SQLite 作为存储引擎，配合 sqlite-vec 扩展实现向量检索。
数据库文件命名为 domain_knowledge.db。

## 核心表结构

Forest 表存储森林元信息，Leaf 表是核心表，存储每个知识原子的路径和哈希。
```

### 期望输出

```json
{
  "atoms": [{
    "forest": "mke",
    "tree": "元知识引擎",
    "branch": "存储设计",
    "title": "SQLite表结构设计",
    "description": "元知识引擎的 SQLite 数据库完整 DDL...",
    "keywords": ["SQLite", "DDL", "表结构", "数据库设计"],
    "content_preview": "使用 SQLite + sqlite-vec 作为存储引擎，单文件 domain_knowledge.db，核心表包括 Forest、Leaf..."
  }],
  "references": [{
    "from_title": "SQLite表结构设计",
    "to_forest": "mke",
    "to_title": "五层架构蓝图",
    "ref_type": "references",
    "keyword": "第二层存储映射"
  }],
  "cross_declaration_warnings": []
}
```

## 交叉声明检测器

在 LLM 抽取后，与已有 Leaf 表进行二次校验：

```python
def detect_cross_declaration(candidate: dict, existing_leaves: list) -> list[Warning]:
    """
    检测候选知识原子是否与已有叶子重复声明。
    策略：
    1. 向量相似度：candidate.content_preview vs 所有 existing_leaves 的向量
    2. 对相似度 > 0.85 的候选，用 LLM 做精确判断
    3. 返回需要引用而非重复的建议
    """
    pass
```

### 阈值配置

| 阶段 | 阈值 | 动作 |
|------|------|------|
| 向量相似 > 0.95 | 直接拒绝 | 返回引用建议 |
| 向量相似 0.85–0.95 | 标记待审 | 人工/LLM 二次裁决 |
| 向量相似 < 0.85 | 自动通过 | 写入新 Leaf |

## 迭代策略

- **初次构建**：批量抽取所有文档，人工审核核心森林/树的归属
- **增量更新**：新文档加入时，仅抽取增量并检测与已有 Leaf 的交叉声明
- **修订反馈**：人工修正的结果作为 Few-shot 样本，持续优化抽取器 Prompt
