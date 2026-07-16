---
forest: memory-systems-ai
tree: t3-knowledge-augmentation-reasoning
branch: b1-graphrag-structured-knowledge
leaf: kg-llm-fusion-toe-poe-sog
title: KG-LLM融合：ToG/PoG/SoG多跳推理路径
created: 2026-07-16
model: DeepSeek V4 Pro
source:
  - "frs_source/AI与大模型在知识领域、Agent记忆、推理数据及推理关系中的前沿研究综述.md"
refs:
  - "[t3-b1] GraphRAG多跳推理 | 此类方法为GraphRAG的基础形式"
  - "[t1-b3] 模式完成与内容寻址 | KG 推理路径与大脑联想检索的结构类比"
---

# KG-LLM融合：ToG/PoG/SoG多跳推理路径

## 四种范式对比

| 方法 | 推理范式 | KG完整性依赖 | 需训练？ | 可追溯性 |
|------|---------|:---:|:---:|:---:|
| **ToG** | LLM⊗KG 交互探索 + beam search | 是 | 否 | 高 |
| **PoG** | 三阶段多跳路径融合 | 是 | 否 | 中 |
| **SoG** | observe-think-navigate 上下文感知导航 | 是 | 否 | 高 |
| **KG-RAR** | 过程导向分层检索 + 奖励模型 | 是 | 部分 | 中 |

## Think-on-Graph (ToG, Sun et al., 2023, arXiv:2307.07697)

提出"LLM⊗KG"深度整合范式，LLM 作为 Agent 在 KG 上交互式探索相关实体和关系，通过 beam search 发现最有前景的推理路径。**关键贡献**：证明知识可追溯性——推理路径每一步可回溯到 KG 中具体事实三元组，支持人类检查每一步并纠正错误。

## Paths-over-Graph (PoG, Tan et al., 2024, arXiv:2410.14211)

通过三阶段动态多跳路径探索整合 KG 多跳推理路径，将 LLM 自身知识与 KG 事实知识相结合。PoG+GPT-3.5-Turbo 超过 ToG+GPT-4 达 23.9%，在 GPT-3.5-Turbo 上相较 ToG 平均提升 18.9%。

## Search-on-Graph (SoG, Sun et al., 2025, arXiv:2510.08825)

遵循 observe-think-navigate 范式：每一步观察当前实体关系连接 → 推理最佳路径 → 导航至下一实体。完全利用 LLM 自身推理能力，无需独立路径选择模块。

## 其他路径优化方法

- **RRP**（Xiao et al., 2025）：关系嵌入 + 双向分布学习 + 重思考模块评估精炼路径
- **KARPA**（Fang et al., 2024）：LLM 全局预规划关系路径 + 嵌入模型匹配语义路径
- **ORT**（Liu et al., 2025）：受逆向思维启发，从目的反向构建到条件的推理路径，WebQSP/CWQ 达 SOTA

## 开放问题

1. 绝大多数方法假设 KG 完整高质量，仅 CS-RAG 处理不完美 KG——真实部署的核心瓶颈
2. 各论文报告提升数字无法直接横向比较（缺少统一评测框架）
3. 搜索效率随 KG 规模线性下降（10^6 节点级 KG 单次查询延迟可能超 30 秒）
