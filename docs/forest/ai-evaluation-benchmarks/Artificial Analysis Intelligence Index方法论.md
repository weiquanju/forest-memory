---
forest: aeb
tree: Artificial Analysis Intelligence Index
branch: 指数方法论
title: Artificial Analysis Intelligence Index 方法论详解
version: 1.0.0
created: 2026-07-15
updated: 2026-07-15
description: Artificial Analysis Intelligence Index v4.1 完整方法论——9 项评测 × 四大能力维度（Agent/Coding/Scientific/General）的加权评分体系、测试参数规范、版本演进历史与学术引用指南
keywords:
  - Artificial Analysis
  - 评测基准
  - 第三方评测
  - Agent 评估
  - 复合基准
  - 学术引用
source: "[页面] Artificial Analysis Intelligence Benchmarking Methodology v4.1 | https://artificialanalysis.ai/methodology/intelligence-benchmarking"
refs:
  - "[aeb] MMLU基准详解 | 与 MMLU 形成'商业评测 vs 学术基准'对比参照"
  - "[aeb] GPQA基准详解 | GPQA Diamond 是 Intelligence Index 的九个组成评测之一"
  - "[frs] 推理评估基准演进 | Intelligence Index 的动态版本演进是基准演进第四阶段的实践案例"
---

# Artificial Analysis Intelligence Index 方法论详解

## 一、性质与定位

Artificial Analysis Intelligence Index 是由第三方商业评测机构 **Artificial Analysis** 发布的**复合型模型能力评分**，旨在为语言模型在推理、知识、数学和编程方面的整体智能提供综合性衡量指标。

| 属性 | 说明 |
|------|------|
| **定位** | 行业第三方评测平台（非学术基准） |
| **性质** | 复合加权指数，聚合多项独立评测 |
| **适用场景** | 跨模型综合能力对比、行业趋势跟踪 |
| **局限性** | 非同行评审、动态变化影响可复现性、具有商业背景 |
| **当前版本** | v4.1（2026 年 6 月发布，9 项评测） |

平台自我定位："它比其他任何现有指标都更有用的跨模型综合对比"，但明确承认"像所有评估指标一样，它有局限性，可能不直接适用于每个用例。"

---

## 二、v4.1 指数构成

Intelligence Index v4.1 通过加权平均 9 项评测来计算，覆盖四大能力维度，**Agent 权重最高（34%）**以强调对 Agentic 任务的倾斜。

### 2.1 四大能力维度与评测项目

| 类别 (权重) | 评测 | 题数 | 重复 | 题型 | 评分 | 权重 | 工具 |
|-------------|------|------|------|------|------|------|------|
| **Agents (34%)** | GDPval-AA v2 | 220 任务 | 1 | Agent 任务完成（文件输出） | Elo（锚定人类专家 1000） | 20% | ✓ |
| | τ³-Banking | 97 | 5 | 双控 Agent-用户模拟（知识检索） | 后端数据库状态验证 pass@1 | 14% | ✓ |
| **Coding (24%)** | Terminal-Bench v2.1 | 89 | 3 | 终端任务执行 | 测试套件 pass/fail, pass@1 | 16% | ✗ |
| | SciCode | 288 子问题 | 3 | Python 代码（须通过所有单元测试） | 代码执行 pass@1，科学家标注背景 | 8% | ✗ |
| **General (18%)** | AA-LCR | 100 | 3 | 开放式问答 | 等价判断 LLM, pass@1 | 6% | ✗ |
| | AA-Omniscience | 6,000 | 1 | 开放式问答 | 正确率 (8%) + 非幻觉率 (4%) | 12% | ✗ |
| **Scientific Reasoning (24%)** | HLE（人类最后的考试） | 2,158 | 1 | 开放式问答 | 等价判断 LLM, pass@1 | 12% | ✗ |
| | GPQA Diamond | 198 | 5 | 四选一选择题 | 正则提取, pass@1 | 6% | ✗ |
| | CritPt | 70 | 5 | Python 函数/符号表达式/数值 | 官方评分服务器, pass@1 | 6% | ✗ |

### 2.2 额外评测（不计入指数）

平台在核心指数之外还运行一系列单独报告的评测，包括：
- **AA-Briefcase**：多周知识工作 Agent 评测（4 场景）
- **Harvey LAB-AA**：法律 Agent 评测（120 任务，24 法律领域）
- **APEX-Agents-AA**：专业服务 Agent 评测（452 任务）
- **AutomationBench-AA**：SaaS 工作流自动化（657 任务）
- **EnterpriseOps-Gym-AA**：企业运维 Agent 评测（1,117 任务，8 领域）
- **ITBench-AA**：Kubernetes 事故根因分析 Agent 评测（59 任务）
- **LiveCodeBench**：代码生成（315 题）
- **IFBench**（已从指数中移除但继续运行）：指令遵循
- **MMLU-Pro**：多任务语言理解 Pro 版（12,032 题）
- **Global-MMLU-Lite**：多语言评测（~6,000 题，15 语言）
- **MMMU Pro**：多模态推理（1,730 题）

---

## 三、评测原则

平台遵循四项核心评测原则：

| 原则 | 说明 |
|------|------|
| **标准化（Standardized）** | 所有模型在相同条件下评估：一致的提示策略、温度设置、评分标准 |
| **无偏（Unbiased）** | 采用避免不公平惩罚的评估技术，包括清晰提示、鲁棒的答案提取、灵活的答案验证 |
| **零样本指令提示（Zero-Shot Instruction Prompted）** | 使用清晰指令，不提供示例或演示，测试模型的指令遵循能力 |
| **透明（Transparent）** | 完全公开方法论，包括提示模板、评分标准和局限性 |

---

## 四、测试参数规范

### 4.1 通用参数

| 参数 | 设置 |
|------|------|
| **温度** | 非推理模型 0，推理模型 0.6（除非模型实验室推荐其他温度） |
| **最大输出 Token** | 非推理模型 16,384（受上下文窗口限制时向下调整）；推理模型使用模型创建者公开允许的最大输出 |
| **代码评估环境** | Ubuntu 22.04 LTS + Python 3.12 |
| **错误处理** | API 失败自动重试（最多 30 次）；持续失败的手动审查 |

### 4.2 评分方法：pass@1

平台普遍使用 **pass@1** 评分：模型必须在**首次尝试**时产出正确答案。多次重复评测时，pass@1 通过聚合所有重复的结果计算：

$$\text{pass@1} = \frac{1}{k}\sum_{i=1}^{k} p_i$$

其中 $p_i = 1$ 表示第 $i$ 次尝试正确，$k$ 为所有重复的总测试实例数。

### 4.3 统计可靠性

平台估计 Intelligence Index 的 **95% 置信区间小于 ±1%**，基于对部分模型进行超过 10 次重复实验得出。单次评测的置信区间可能更宽。

### 4.4 多项选择题处理

GPQA（4 选项 A-D）、MMLU-Pro（10 选项 A-J）使用统一指令提示：

> Answer the following multiple choice question. The last line of your response should be in the following format: 'Answer: A/B/C/D' (e.g. 'Answer: A').

题目提取使用多阶段正则匹配，主模式为 `答案提取正则`，失败时依次尝试 LaTeX boxed、自然语言、括号等多种备选模式。

---

## 五、版本演进历史

| 版本 | 时间 | 主要变更 |
|------|------|----------|
| **v1.0–v1.3** | 2024.01–2025.02 | 初始版本 |
| **v2.0** | 2025.02–2025.08 | 评测体系扩展 |
| **v2.1** | 2025.08 | 新增 IFBench、AIME 2025；移除 MATH-500、AIME 2024 |
| **v2.2** | 2025.08–2025.09 | 新增 AA-LCR（长上下文推理） |
| **v3.0** | 2025.09–2025.12 | 新增 Terminal-Bench Hard、τ²-Bench Telecom；首次纳入 Agent 评测 |
| **v4.0** | 2026.01 | **重大改版**：新增 GDPval-AA、AA-Omniscience、CritPt；移除 MMLU-Pro、LiveCodeBench、AIME 2025；四类均权 25% |
| **v4.0.1–v4.0.4** | 2026.01–2026.06 | 小幅修正：更新评分模型、重锚定 Elo 分数等 |
| **v4.1** | 2026.06（当前） | **Agent 倾斜升级**：升级 Terminal-Bench Hard→v2.1、τ²-Bench Telecom→τ³-Banking、GDPval-AA→v2；移除 IFBench；调整权重为 Agent 34% / Coding 24% / Scientific 24% / General 18% |

关键趋势：从最初的纯知识/数学评测，逐步转向**以 Agentic 任务为核心的评测体系**，同时持续移除模型已"饱和"的评测。

---

## 六、学术引用指南

### 6.1 适用场景

| 推荐场景 | 不推荐场景 |
|----------|------------|
| 论文中模型能力的行业对标佐证 | 作为唯一的模型能力证明 |
| 追踪模型能力随时间变化的趋势 | 替代 MMLU/GPQA 等经同行评审的标准基准 |
| 展示模型在 Agentic 任务上的综合表现 | 用于严谨的消融实验基准 |

### 6.2 引用要点

1. **明确版本**：务必注明具体版本（如 "Artificial Analysis Intelligence Index v4.1"）及发布日期
2. **提供详细来源**：同时引用方法论页面以证明对计算方式的充分了解
3. **说明数据性质**：正文中说明该数据来自第三方行业评测平台，非传统学术基准
4. **注明局限**：说明该基准动态变化的特性及商业背景（知名 AI 学者 Andrew Ng 投资了该平台）

### 6.3 建议引用格式（APA）

> Artificial Analysis. (2026). *Artificial Analysis Intelligence Index v4.1*. Retrieved July 15, 2026, from https://artificialanalysis.ai/methodology/intelligence-benchmarking

### 6.4 版本查看方法

- 访问官方方法论页面 `https://artificialanalysis.ai/methodology/intelligence-benchmarking`，页面顶部标注当前版本
- 搜索官方公告文章（如 "Announcing Artificial Analysis Intelligence Index v4.1"）
- 在模型对比页面查看当前使用的指数版本
