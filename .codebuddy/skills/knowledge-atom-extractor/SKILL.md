---
name: knowledge-atom-extractor
description: >-
  通用知识原子抽取技能。当用户需要从文档（Markdown/Word/代码 AST 扫描结果等）中提取结构化知识、
  构建层级化知识库、进行知识原子化拆分、检测交叉声明/重复声明、或生成带 YAML Frontmatter 的
  知识原子文档时触发此技能。适用场景包括：为 RAG/Agent 知识库整理文档、将杂乱笔记转化为
  结构化知识体系、代码文档的知识图谱构建、多文档一致性治理等。不适用于纯翻译、摘要或格式转换任务。
---

# Knowledge Atom Extractor（知识原子抽取器）

## Overview

从非结构化或半结构化文档中，利用 LLM 自动提取结构化的知识原子（Knowledge Atom）——
每个知识原子是一个单一职责的最小知识单元，携带 YAML Frontmatter 元数据头，通过引用
声明（refs）与其他知识原子构成图网络。该技能将"知识抽取 + 交叉声明检测 + 引用去重"
合为一体，从构建环节就保障知识库的质量。

核心设计理念：
- **单一职责（SSOT）**：每个知识原子只声明一个核心概念，杜绝交叉声明
- **引用非复制**：已有权威来源的知识点通过 `refs` 引用，不重新声明
- **层级定位**：知识原子归属 森林→树→枝干→叶 的层级结构，便于精准检索
- **元数据先行**：YAML Frontmatter 携带完整的检索与治理元数据

## 核心概念

| 概念 | 说明 |
|------|------|
| 知识原子（Knowledge Atom） | 不可再分的最小知识单元，一个 `.md` 文件 = 一个知识原子 |
| 森林（Forest） | 顶层知识领域，如 `mke`、`backend`、`marketing` |
| 树（Tree） | 森林内的大主题，如 `存储层`、`检索层` |
| 枝干（Branch） | 主题下的子模块，如 `向量检索`、`图扩散` |
| 叶（Leaf） | 具体知识原子文档 |
| atom_type | 知识原子类型：`semantic`（事实）/ `procedural`（规则/模板）/ `episodic`（交互经验） |
| refs | 引用声明，格式 `[森林ID] 文档标题 \| 引用关键字` |
| 交叉声明 | 两个文档重复声明同一知识点，违反 SSOT 原则 |

## 工作流

### Step 1: 判断输入类型与抽取模式

根据输入来源选择抽取模式：

| 输入类型 | 抽取模式 | atom_type 默认值 | 说明 |
|---------|---------|-----------------|------|
| Markdown 文档 | 标准抽取 | `semantic` | 领域知识、设计文档、技术方案 |
| 代码 AST 扫描结果 | 代码抽取 | `procedural` | 函数签名、类依赖、配置项 |
| Word/PDF 转换文本 | 标准抽取 | `semantic` | 策划案、需求文档 |
| 交互记录/对话日志 | 经验抽取 | `episodic` | Interaction_Memory 巩固 |

若输入为多个文档，逐个处理但共享同一批已有 Leaf 列表用于交叉声明检测。

### Step 2: 执行 LLM 知识抽取

使用 `references/prompt_strategies.md` 中的 System Prompt 策略和 Few-shot 模板，
对输入文档执行抽取。抽取器输出 JSON 结构化结果，包含：

- `atoms[]`：提取出的知识原子（可能一个文档拆分为多个原子）
- `references[]`：文档间的引用关系
- `cross_declaration_warnings[]`：检测到的潜在交叉声明

输出 Schema 的完整定义参见 `references/extraction_schema.md`。

### Step 3: 交叉声明检测

抽取后，将候选知识原子与已有知识库中的 Leaf 进行二次校验：

1. **向量相似度粗筛**：candidate 的 content_preview 向量 vs 所有 existing leaves 的向量
2. **阈值判定**：
   - 相似度 > 0.95 → 直接拒绝，返回引用建议
   - 相似度 0.85–0.95 → 标记待审，触发 LLM 二次裁决
   - 相似度 < 0.85 → 自动通过
3. **LLM 精确判断**（仅对待审项）：判断是否真正重复，还是互补关系

详细策略参见 `references/cross_declaration_guide.md`。

### Step 4: 生成知识原子文档

通过检测的知识原子，使用 `assets/knowledge_atom_template.md` 模板生成最终的 `.md` 文件：

1. 填充 YAML Frontmatter（forest/tree/branch/title/version/created/updated/description/keywords/refs）
2. 写入正文内容（单一职责，不超过 200 行）
3. 设置 `status: draft`（初始状态，待人工审核）
4. 确保四元组 `forest:tree:branch:title` 全局唯一

### Step 5: 人工审核与迭代

- 初次构建：批量抽取后人工审核核心森林/树的归属是否正确
- 增量更新：新文档加入时仅抽取增量，与已有 Leaf 做交叉声明检测
- 修订反馈：人工修正结果作为 Few-shot 样本，持续优化抽取器 Prompt

## 脚本资源

### scripts/extract_knowledge.py

可直接执行的知识抽取脚本，支持：
- 单文件/批量目录模式
- OpenAI / Anthropic API 后端切换
- 交叉声明检测（基于 sqlite-vec 或纯 Python 余弦相似度）
- JSON 结构化输出 + 知识原子 `.md` 文件生成

使用方式：
```bash
python scripts/extract_knowledge.py --input <file_or_dir> --forest <forest_id> --output <output_dir>
```

关键参数：
- `--model`：LLM 模型选择（默认 `gpt-4o`）
- `--existing-db`：已有知识库 SQLite 文件路径（用于交叉声明检测）
- `--threshold`：交叉声明检测阈值（默认 0.85）
- `--dry-run`：仅输出 JSON，不生成 .md 文件

## 参考文档

以下文档包含详细规范，在需要时加载到上下文中参考：

- **`references/extraction_schema.md`**：JSON 输出 Schema 的完整字段定义、类型约束、示例值
- **`references/prompt_strategies.md`**：System Prompt 完整文本、Few-shot 模板（含示例输入和期望输出）、抽取质量要求
- **`references/cross_declaration_guide.md`**：交叉声明检测的完整策略、阈值配置表、LLM 二次裁决 Prompt、不同领域的阈值建议

## 定制指南

此 skill 是通用模板，建议根据自身知识体系进行以下定制：

1. **领域标签**：在 `references/extraction_schema.md` 中补充 `keywords` 的领域标签预设（如 `backend/config`、`marketing/campaign`）
2. **Few-shot 样本**：在 `references/prompt_strategies.md` 中替换为符合自身知识库风格的 Few-shot 示例
3. **阈值调整**：在 `references/cross_declaration_guide.md` 中根据知识库规模和领域特性调整相似度阈值
4. **atom_type 扩展**：根据需要扩展知识原子类型（如增加 `factual`、`reasoning` 等）
5. **森林/树预设**：在 System Prompt 中预定义常见的森林/树/枝干归属，减少 LLM 的层级判断偏差
