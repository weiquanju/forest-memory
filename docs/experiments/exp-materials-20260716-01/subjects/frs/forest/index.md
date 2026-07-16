---
forest: frs
title: AI与大模型前沿研究综述知识森林
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
description: 基于2025-2026年AI大模型推理能力前沿综述（v4.0.0, 54篇参考文献）构建的层级化知识森林，覆盖GraphRAG、Agent记忆、知识治理、推理评估、RLVR训练、知识编辑六大核心方向。
source: "[frs_source] AI与大模型在知识领域、Agent记忆、推理数据及推理关系中的前沿研究综述 v4.0.0 | 内部综述文档"
---

# AI与大模型前沿研究综述知识森林 (frs)

## 定位

本森林从"知识可追溯性"与"输出可靠性"的双重视角，系统化组织2023-2026年间AI大模型推理能力前沿研究。森林覆盖六大核心方向——KG增强推理、Agent记忆、知识治理、推理评估、RLVR训练、知识编辑——揭示它们协同作用的"知识闭环"链条。

## 森林内文档

### 树：知识领域与GraphRAG推理增强 (kg-reasoning)

| 文档 | 说明 |
|------|------|
| [KG-LLM融合互补机制](kg-reasoning/kg-llm-fusion/) | LLM与KG的互补关系、PoG/ToG/KG-Agent/KG-RAR方法 |
| [GraphRAG图增强检索与多跳推理](kg-reasoning/graphrag/) | GraphRAG范式、实用级框架、T-GRAG、CS-RAG、RTSoG |
| [推理路径优化](kg-reasoning/path-optimization/) | RRP/KARPA/ORT/SoG/MemoTime路径优化方法 |
| [方法比较](kg-reasoning/method-comparison/) | KG推理方法六维横向对比 |

### 树：Agent记忆机制 (agent-memory)

| 文档 | 说明 |
|------|------|
| [记忆分类体系](agent-memory/memory-taxonomy/) | 三维统一分类框架（载体/功能/动态过程） |
| [记忆对推理质量的影响](agent-memory/memory-impact/) | 经验跟随属性、错位经验重放 |
| [记忆管理前沿](agent-memory/memory-management/) | Mem0/MemVerse/DYNA/LifelongAgentBench |
| [框架比较](agent-memory/framework-comparison/) | 三维度框架横向对比 |

### 树：知识评估与治理 (knowledge-governance)

| 文档 | 说明 |
|------|------|
| [事实一致性检测](knowledge-governance/fact-verification/) | KG-CRAFT/GraphCheck/CommunityKG-RAG/HybridFC/ConflictBank |
| [知识溯源与可解释性](knowledge-governance/knowledge-traceability/) | 可追溯性、RL可解释核查、混合管道、语义三元组 |
| [方法比较](knowledge-governance/method-comparison/) | 五维评估方法对比 |

### 树：推理数据与评估 (reasoning-evaluation)

| 文档 | 说明 |
|------|------|
| [推理基准演进](reasoning-evaluation/benchmark-evolution/) | GSM8K/AIME到MemBench的演进、数据污染问题 |
| [动态智能体评估](reasoning-evaluation/dynamic-evaluation/) | MemBench/MemoryAgentBench/MemoryArena/LifelongAgentBench |
| [评估范式讨论](reasoning-evaluation/paradigm-discussion/) | 评估成本、记忆与推理纠缠、生态碎片风险 |

### 树：推理与输出关系 (reasoning-output)

| 文档 | 说明 |
|------|------|
| [RLVR训练范式](reasoning-output/rlvr-training/) | GRPO/PPO/DCPO、校准退化、Reward Hacking |
| [多模态推理](reasoning-output/multimodal-reasoning/) | STARE空间操作瓶颈、Insight-V长链视觉推理 |
| [模型对比](reasoning-output/model-comparison/) | DeepSeek-R1/o1/DCPO/Insight-V四维对比 |

### 树：知识更新与遗忘 (knowledge-update)

| 文档 | 说明 |
|------|------|
| [KG持续学习](knowledge-update/kg-continual-learning/) | EWC/BAKE/MRCKG/MSPT/KG-GMM |
| [LLM知识编辑](knowledge-update/llm-knowledge-editing/) | WilKE/PRUNE/STABLE/事件级编辑/逻辑规则编辑 |
| [持续学习与编辑比较](knowledge-update/method-comparison/) | 五维横向对比 |

### 树：综述方法论基础 (methodology-foundations)

| 文档 | 说明 |
|------|------|
| [综述方法论](methodology-foundations/review-methodology/) | PRISMA 2020检索策略、筛选流程、局限性声明 |
| [相关综述比较](methodology-foundations/review-comparison/) | 与Peng/Hu/Wu/Li等已有综述的差异化定位 |
| [结论与展望](methodology-foundations/conclusions/) | 六大维度发现总结、五项开放挑战 |
