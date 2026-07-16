---
forest: frs
tree: knowledge-governance
branch: fact-verification
leaf_id: frs-fact-001
title: KG-CRAFT知识图谱增强事实核查
type: method
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
source: "[frs_source] §4.1 | Lourenço et al., arXiv:2601.19447, 2026 [20]"
refs:
  - "[frs-kg-llm-003] ToG交互式推理 | KG-CRAFT将ToG的可追溯性思想扩展到事实核查"
---

# KG-CRAFT 知识图谱增强事实核查

## 方法概述

**KG-CRAFT** 利用知识图谱增强LLM的自动事实核查能力 [20]。

## 工作机制

1. **KG构建**：从待核查的声明和相关报告中构建临时KG
2. **对比性问题生成**：基于KG结构制定上下文相关的对比性问题（contrastive questions），引导证据提炼
3. **证据评估**：LLM基于对比性问题和KG证据判断声明真伪

## 性能

在LIAR-RAW和RAWFC两个真实世界数据集上达到**SOTA** [20]。

## 独特优势

对比性问题的设计使KG-CRAFT能捕捉到简单"匹配/不匹配"判断容易遗漏的细微矛盾——例如通过询问"如果声明A为真，那么关系R应该是什么值？"来发现KG中缺失的关键信息。
