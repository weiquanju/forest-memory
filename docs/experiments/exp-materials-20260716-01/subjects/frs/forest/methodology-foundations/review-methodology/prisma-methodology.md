---
forest: frs
tree: methodology-foundations
branch: review-methodology
leaf_id: frs-method-001
title: PRISMA 2020综述方法论
type: methodology
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
source: "[frs_source] §一.X 综述方法论"
---

# PRISMA 2020综述方法论

## 检索策略

| 维度 | 配置 |
|------|------|
| 数据库 | arXiv、DBLP、Google Scholar、Semantic Scholar |
| 时间范围 | 2023年1月—2026年7月 |
| 语言 | 英文（为主）+ 中文 |
| 文献类型 | 经同行评审的会议/期刊论文，或已发布于arXiv的高影响力预印本 |

## 六大主题关键词

| 主题 | 关键词 |
|------|--------|
| KG增强推理 | `knowledge graph` + `LLM reasoning`、`GraphRAG`、`multi-hop reasoning` |
| Agent记忆 | `agent memory`、`LLM memory`、`memory-augmented LLM` |
| 事实核查 | `fact checking` + `LLM`、`hallucination detection` + `KG` |
| 推理评估 | `reasoning benchmark` + `LLM`、`agent benchmark` |
| 持续学习与编辑 | `knowledge editing` + `LLM`、`continual learning` + `LLM` |
| 多模态推理 | `multimodal reasoning`、`spatial reasoning` + `MLLM` |

## 筛选流程

初始检索 N≈500 → 去重 N≈420 → 标题/摘要筛选 → 全文评估 N≈120 → 最终纳入 **N=54**

## 纳入标准

1. 发表于2023年1月至2026年7月
2. 经同行评审或已发布于arXiv且具备可验证实验数据
3. 主题属于六大覆盖方向之一
4. 提供清晰的方法描述和可引用的实验结论
