---
forest: memory-systems-ai
tree: t2-agent-memory-systems
branch: b3-evaluation-applications
leaf: l2-agent-memory-benchmarks
title: Agent记忆基准演进
created: 2026-07-16
model: GLM-5.2
source:
  - "frs_source/AI与大模型在知识领域、Agent记忆、推理数据及推理关系中的前沿研究综述.md"
refs:
  - "[t2-b3] 直接与间接评估方法 | 基准演进体现从静态到动态的评估范式转变"
  - "[t3-b4] RLVR训练与校准退化 | Agent记忆基准与推理基准的边界日益模糊"
---

# Agent记忆基准演进

## 从静态到动态的范式演进

| 阶段 | 基准 | 特点 |
|------|------|------|
| 早期 | GSM8K, MATH | 小学数学应用题、数学竞赛题 |
| 发展 | AIME, AMC | 更高难度数学题集 |
| 扩展 | 多领域专用基准 | 逻辑推理、常识推理、多跳问答 |
| 前沿 | MemBench, MemoryAgentBench, MemoryArena | 多会话任务，记忆与决策交织 |

## 前沿 Agent 记忆基准

### MemBench（arXiv:2506.21605）
首个同时覆盖**参与**和**观察**两种场景、**事实**和**反思**两种记忆层次的综合基准。

### MemoryAgentBench（arXiv:2507.05257）
基于增量多轮交互，评估四种能力：
- 准确检索
- 测试时学习
- 长程理解
- 选择性遗忘

### MemoryArena（arXiv:2602.16313）
多会话 Memory-Agent-Environment 循环中的统一评估场。

### LifelongAgentBench（arXiv:2505.11942）
首个系统评估 LLM Agent 终身学习能力的基准，覆盖 Database/OS/KG 三个环境。实验揭示传统经验回放对 LLM Agent 效果有限——原因是无关信息和上下文长度约束。

## 评估范式三大趋势

1. **组合式基准**：将多个基准"链式"连接生成更长推理链（如 Scheherazade 技术评估长链条件推理）
2. **过程导向评估**：不仅看最终答案正确性，还关注推理过程质量（可重用性 Reusability、可验证性 Verifiability）
3. **智能体评估**：要求多轮交互中的规划、执行和反思

## 结构性挑战

1. **评估成本与可复现性**：多轮 Agent-环境交互的 API 调用成本和时间开销远高于静态基准，社区复现门槛显著提高
2. **记忆与推理的纠缠**：当前基准同时测量记忆能力和推理能力，难以分离"记错了"还是"推理错了"——需要更细粒度归因分析
3. **生态碎片风险**：统一标杆（GSM8K/MATH）正被碎片化专用 Agent 基准取代，跨工作比较日益困难
