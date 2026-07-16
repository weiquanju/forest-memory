---
forest: memory-systems-ai
tree: t3-knowledge-augmentation-reasoning
branch: b2-quality-governance
leaf: l1-fact-checking-traceability
title: 事实核查与知识溯源
created: 2026-07-16
model: GLM-5.2
source:
  - "frs_source/AI与大模型在知识领域、Agent记忆、推理数据及推理关系中的前沿研究综述.md"
refs:
  - "[t3-b1] KG-LLM融合推理 | ToG的可追溯性是事实核查的基础"
  - "[t2-b3] 经验跟随与记忆质量 | 事实核查是记忆质量控制的关键环节"
---

# 事实核查与知识溯源

## 事实一致性检测

### KG-CRAFT（arXiv:2601.19447）
利用知识图谱增强 LLM 自动事实核查：从声明和报告中构建 KG，基于 KG 结构制定上下文相关的对比性问题引导证据提炼。在 LIAR-RAW 和 RAWFC 数据集上达到 SOTA。

### GraphCheck（arXiv:2502.16514）
通过 GNN 将 KG 处理为软提示（soft prompt），使 LLM 在单次推理中完成事实核查。能捕获多跳推理链，在 7 个基准上整体提升最高 7.1%，在医学等领域超越专用事实核查器。

### CommunityKG-RAG（arXiv:2408.08535）
将 KG 中的社区结构集成到 RAG 中，利用多跳特性提高事实核查中信息检索准确性和相关性，无需额外训练即可适应新领域。

### HybridFC（arXiv:2409.06692）
混合事实核查方法，在集成学习框架中利用文本、路径、规则和嵌入等多种方法的多样性，在 FactBench 上 AUC 提升 0.14-0.27。

## 知识溯源与可解释性

### ToG 的可追溯性
推理路径中每一步可追溯到 KG 中的具体事实三元组，人类专家可检查推理链并提供反馈纠正错误——"人在回路中"方法显著提升推理透明度和可信度。

### RL 驱动的可解释事实核查
Nikopensius 等人（arXiv:2310.07613）提出基于 RL 的 KG 推理方法：RL Agent 计算证明或反驳事实声明的路径，路径可呈现给人类读者判断证据是否令人信服——人机协同的可解释事实核查范式。

### 混合事实核查管道
Kolli 等人（arXiv:2511.03217）集成 KG 检索、LLM 分类和 Web 搜索 Agent，在 FEVER 上 F1 达 0.93。设计了"KG 覆盖不足时自动回退到 Web 搜索"的降级策略。

## 方法比较

| 方法 | 核心机制 | 需要 KG | 可解释性 | 最佳表现 |
|------|---------|:---:|:---:|---------|
| KG-CRAFT | KG 增强对比性问题 | 是 | 中 | SOTA on LIAR-RAW, RAWFC |
| GraphCheck | GNN 软提示 + 多跳链 | 是 | 低 | 7 基准提升 7.1% |
| Hybrid Pipeline | KG + LLM + Web Agent | 首选 | 高 | F1=0.93 on FEVER |
| RL-based | RL Agent 证明/反驳路径 | 是 | 高 | — |

**关键观察**：混合管道方法在准确率上领先但工程复杂度高；多数方法依赖 KG 完整性，跨领域泛化性能普遍下降 5-15%，是部署落地的核心瓶颈。
