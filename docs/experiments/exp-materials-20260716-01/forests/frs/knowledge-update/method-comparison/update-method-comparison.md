---
forest: frs
tree: knowledge-update
branch: method-comparison
leaf_id: frs-update-compare-001
title: 持续学习与知识编辑方法横向对比
type: analysis
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
source: "[frs_source] §7.3 持续学习与知识编辑比较"
refs:
  - "[frs-kg-cont-001] EWC"
  - "[frs-kg-cont-002] BAKE"
  - "[frs-kg-edit-001] WilKE"
  - "[frs-kg-edit-002] PRUNE"
  - "[frs-kg-edit-002] STABLE"
---

# 持续学习与知识编辑方法横向对比

## 对比矩阵

| 方法 | 类型 | 遗忘缓解机制 | 理论保证 | 规模已验证 | 核心瓶颈 |
|------|------|------------|:---:|:---:|------|
| EWC on KG [33] | 持续KG嵌入 | Fisher信息矩阵权重保护 | 局限（假设高斯后验） | FB15k-237 | 遗忘减半但未消除（6.85%残留） |
| BAKE [35] | 持续KG嵌入 | 序贯贝叶斯后验更新 | **是** | 多个CKGE基准 | 聚类维护开销 |
| WilKE [40] | LLM知识编辑 | 基于模式匹配的层选择 | 否 | GPT2-XL, GPT-J | 顺序编辑毒性累积 |
| PRUNE [41] | LLM知识编辑 | 条件数约束 | **是**（扰动上界） | 多步顺序编辑 | 约束可能限制编辑灵活性 |
| STABLE [42] | LLM知识编辑 | 门控LoRA更新裁剪 | 否 | 多步顺序编辑 | 阈值调参敏感 |

## 三条关键观察

1. **BAKE和PRUNE提供了理论保证**，但理论保证的充分性在真实世界知识漂移场景下尚待检验

2. **KG持续嵌入和LLM知识编辑独立发展**——将KG的结构化约束引入LLM编辑过程可能是一个高潜力的交叉方向

3. **"毒性累积"揭示的深层矛盾**：当前编辑方法设计为独立操作，但真实知识更新是相互关联的网络效应——事件级编辑 [43] 和逻辑规则编辑 [45] 是对此的直接回应
