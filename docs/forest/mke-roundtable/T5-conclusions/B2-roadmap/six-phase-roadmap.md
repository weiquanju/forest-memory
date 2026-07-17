---
forest: mrt
tree: T5-conclusions
branch: B2-roadmap
title: 六阶段实施路线图——Day 1 至 Month 9
version: 1.0.0
created: 2026-07-17
updated: 2026-07-17
description: 经四位专家讨论和 DSV4 Flash 仲裁后的完整可执行六阶段实施路线图
keywords:
  - 路线图
  - 实施计划
  - 六阶段
  - MVP
  - 生产化
refs:
  - "[mrt] T3-B3 改进优先级 | 路线图的前提共识与分歧仲裁"
  - "[mke] 跨森林知识注入与架构细化 | 三阶段 MVP 原始路线图"
---

# 六阶段实施路线图

## 阶段总览

```
Phase 1: Day 1     ← 技术栈冒烟测试（知识工程专家提出）
Phase 2: Week 1-2  ← 文档级最小闭环 Demo（DSV4 Flash 原 P0）
Phase 3: Week 3-4  ← 断言图 MVP（质量评审专家原 P0）
Phase 4: Week 5-6  ← 检索质量基准（全体共识 P0）
Phase 5: Month 3-6  ← 认知机制补齐（认知架构专家原 P0）
Phase 6: Month 6-9  ← 生产化（五阶段检索 + 三层冲突检测）
```

## Phase 1：技术栈冒烟测试（Day 1）

**目标**：1 天内完成技术选型验证。

```bash
pip install sqlite-vec
pip install sentence-transformers

python -c "import sqlite_vec; print('ok')"
python -c "from sentence_transformers import SentenceTransformer; m = SentenceTransformer('all-MiniLM-L6-v2'); print(m.encode('hello').shape)"
python -c "import sqlite3; c=sqlite3.connect(':memory:'); c.execute('CREATE VIRTUAL TABLE t USING fts5(content)'); print('ok')"
```

- 若 sqlite-vec 失败 → 切换为 **ChromaDB + SQLite** 分体方案
- 若 sentence-transformers 失败 → 切换到 **OpenAI text-embedding-3-small** API
- 通过标准：三项测试全部 `print('ok')`

## Phase 2：文档级最小闭环 Demo（Week 1-2）

**目标**：用 mke 森林（15 叶）跑通一条完整检索链路。

| Step | 内容 | 产出 |
|:---:|------|------|
| W1 D1-3 | `build_knowledge.py`：遍历 .md → 解析 YAML → 写入 Forest/Tree/Branch/Leaf 表 | SQLite 库 |
| W1 D4-5 | 用 sentence-transformers 生成嵌入 → 写入 vec_leaf | 向量索引 |
| W2 D1-3 | `retrieve_v1(query, k=5)`：向量 + FTS5 双路粗筛 + RRF 融合 | 可调用的检索函数 |
| W2 D4-5 | 集成到 Agent 对话流：retrieve() → Context 拼接 → System Prompt 注入 | 端到端链路 |

**明确不做**：LLM 裁决、多跳图扩散、AGF 断言抽取、Consolidation Pipeline。

## Phase 3：断言图 MVP（Week 3-4）

**目标**：在已建好的 SQLite 库上叠加 (s,p,o) 断言层。

| Step | 内容 |
|:---:|------|
| W3 | (s,p,o) 提取——用 GLM-5.2（AAI 51）或更强模型做首次断言抽取 |
| W3 | UNIQUE INDEX (s,p,o) 去重——结构化匹配，绕过 D4 瓶颈 |
| W4 | source_count 累积——同一断言被多少 Leaf 确认 |
| W4 | 断言检索接口：`retrieve_assertions(query)` → s,p,o 列表 |

**不做**：实体规范化（先接受"iPhone16" vs "iPhone_16"的碎片化）。

## Phase 4：检索质量基准（Week 5-6）

**目标**：建立 MKE 的第一个检索质量实证基线。

| 指标 | 目标基线 |
|------|:---:|
| Precision@5 | > 0.70 |
| Recall@10 | > 0.60 |
| 多跳完整性 | > 0.50 |
| 端到端准确率 | > 0.85 |

**核心产出**：MKE vs flat-chunk RAG 的 A/B 对比报告——从"理论声明"到"实证声明"的关键一步。

## Phase 5：认知机制补齐（Month 3-6）

**目标**：完成认知架构专家建议的深层机制。

- **M3**：重放优先级算法（预测误差 + 新颖性 + 检索失败信号）
- **M4**：主动遗忘的信号驱动降权（检索但未采纳 → 降权）
- **M5-6**：元认知监控层（知识完备性评分 + 缺口检测）

**前置条件**：需要 3 个月以上的真实交互数据作为输入。

## Phase 6：生产化（Month 6-9）

**目标**：实现 MKE 的完整生产能力。

- LLM 裁决配置（需要 AAI ≥ 51）
- 三层冲突检测（L2 逻辑一致性 + L3 系统一致性）
- 跨森林知识注入（多森林互相关注）
- 规则锚点半自动化生成
