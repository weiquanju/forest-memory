---
forest: mi
tree: audit
branch: audit
title: 引用审计报告
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
description: 本森林所有引用的真实性验证状态汇总——带arXiv ID的引用优先使用arxiv-mcp-server验证
keywords:
  - 引用审计
  - 真实性验证
  - arXiv验证
  - 质量指标
atom_type: semantic
status: draft
refs:
  - "[mi] 文献清单 | 完整文献列表"
---

# 引用审计报告

## 审计方法

- 带arXiv ID的引用：通过arxiv-mcp-server逐条检索验证
- 传统期刊引用：通过web搜索确认标题/作者/期刊/年份一致性
- 审计时间：2026-07-16
- 审计工具：arxiv-mcp-server + web search

## 审计结果

| # | 引用 | 来源类型 | 验证状态 | 备注 |
|---|------|---------|---------|------|
| 1 | Gershman et al. (2025) arXiv:2501.02950v2 | arXiv | ✅ 已确认 | KV记忆框架 |
| 2 | Bittner et al. (2017) Science, DOI:10.1126/science.aan3846 | Science | ✅ 已确认 | BTSP原始发现 |
| 3 | Bliss & Lømo (1973) J. Physiol. | 传统期刊 | ✅ 已确认 | LTP经典文献 |
| 4 | Goldmann-Rakic (1995) Neuron | 传统期刊 | ✅ 已确认 | 工作记忆持续活动 |
| 5 | Hopfield (1982) PNAS | 传统期刊 | ✅ 已确认 | 吸引子网络 |
| 6 | Ha & Schmidhuber (2018) arXiv:1803.10122 | arXiv | ✅ 已确认 | 世界模型 |
| 7 | Shuai et al. (2010) Cell | 传统期刊 | ✅ 已确认 | 主动遗忘Rac1 |
| 8 | Ryan et al. (2015) Science | 传统期刊 | ✅ 已确认 | 沉默印迹 |
| 9 | Edge et al. arXiv:2404.16130 | arXiv | ✅ 已确认 | 实用GraphRAG |
| 10 | Wu & Maass (2025) Nature Comms | 传统期刊 | ✅ 已确认 | BTSP计算模型 |
| 11 | Magee (2026) Nature Neuroscience | 传统期刊 | ✅ 已确认 | BTSP综述 |
| 12 | Wang et al. (2025) arXiv:2509.25911 | arXiv | ✅ 已确认 | Mem-α |
| 13 | Peng et al. arXiv:2408.08921 | arXiv | ✅ 已确认 | GraphRAG综述 |

## 质量指标

| 指标 | 当前值 | 目标值 |
|------|:-----:|:-----:|
| 引用真实率 | 13/13 = 100% | ≥ 95% |
| arxiv可查率 | 5/13 = 38% | 记录 |
| 虚构引用数 | 0 | **必须为 0** |

## 待确认引用

以下引用来自frs_source综述（该综述引用54篇文献），本次抽取未全部逐条验证，标记为待审：
- 综述中引用的约40篇论文（未在上表列出）来自frs_source v4.0.0原文
- 需在后续迭代中逐条追加验证
