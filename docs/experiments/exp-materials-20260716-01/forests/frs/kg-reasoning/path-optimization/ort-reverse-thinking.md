---
forest: frs
tree: kg-reasoning
branch: path-optimization
leaf_id: frs-path-003
title: ORT本体引导逆向思维推理
type: method
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
source: "[frs_source] §2.3 | Liu et al., arXiv:2502.11491, 2025 [13]"
---

# ORT 本体引导逆向思维推理

## 方法概述

**Ontology-Guided Reverse Thinking (ORT)** 受人类逆向思维启发，从目的反向构建到条件的推理路径 [13]。

## 核心思想

人类在解决复杂问题时，常从"我想要什么样的答案"出发，逆向推导需要什么条件。ORT将这种思维模式形式化：

1. **本体（Ontology）构建标签推理路径**：利用KG本体知识预先标注实体关系
2. **逆向路径生成**：从目标答案类型出发，反向推导需要哪些前置事实
3. **知识检索引导**：使用逆向路径引导在KG中的检索

## 性能

在WebQSP和CWQ数据集上达到**SOTA** [13]。

## 意义

ORT为KG推理路径设计引入了心理学启发的新视角——逆向推理在人类认知中高效，在机器推理中同样有效。
