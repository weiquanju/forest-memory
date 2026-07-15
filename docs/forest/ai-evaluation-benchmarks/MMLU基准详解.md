---
forest: aeb
tree: MMLU
branch: 基准方法论
title: MMLU基准详解
version: 1.0.0
created: 2026-07-15
updated: 2026-07-15
description: MMLU（Massive Multitask Language Understanding）基准详解——57 学科 15,908 道选择题的零样本/少样本评估范式、三大用途（基线/对比/短板识别）、使用流程与学术引用规范
keywords:
  - MMLU
  - 学术基准
  - 零样本评估
  - Few-shot
  - 语言理解
  - 学术引用
source: "[论文] Hendrycks et al. (2020). Measuring Massive Multitask Language Understanding. arXiv:2009.03300"
refs:
  - "[aeb] GPQA基准详解 | MMLU 测'广度'，GPQA 测'深度'——二者在学术研究中通常互补使用"
  - "[aeb] Artificial Analysis Intelligence Index方法论 | MMLU-Pro 是 Intelligence Index 的历史组成评测（v4.0 后移除），MMLU 是其方法论参照之一"
  - "[frs] 推理评估基准演进 | MMLU 是基准演进'早期'阶段的核心代表，当前正面临饱和困境"
---

# MMLU基准详解

## 一、性质与定位

**MMLU**（Massive Multitask Language Understanding，大规模多任务语言理解）是衡量语言模型在零样本（zero-shot）或少样本（few-shot）场景下对多领域知识理解与掌握能力的**标准学术基准**。

> 原始论文：Hendrycks et al. (2020). *Measuring Massive Multitask Language Understanding*. arXiv:2009.03300.

| 属性 | 说明 |
|------|------|
| **定位** | 学术基准（经同行评审） |
| **评估目标** | 衡量广泛的知识广度（通识理解） |
| **核心指标** | Accuracy（准确率），即模型正确回答选择题的比例 |
| **格式** | 57 学科 × 15,908 道四选一选择题 |
| **当前状态** | 顶尖模型接近饱和（>90%），区分度下降 |

### 核心构成

覆盖 57 个学科，横跨四大领域：

| 领域 | 示例学科 |
|------|----------|
| **人文** | 哲学、历史、法律、道德 |
| **社科** | 经济学、心理学、社会学、政治学 |
| **自然科学** | 物理、化学、生物、医学 |
| **其他** | 计算机科学、数学、工程、商业 |

---

## 二、评估范式

### 2.1 零样本（Zero-Shot）与少样本（Few-Shot）

| 范式 | 说明 | 典型配置 |
|------|------|----------|
| **零样本** | 直接给出问题和选项，不提供示例 | temperature=0，仅给出指令提示 |
| **少样本（Few-Shot）** | 在每个问题前附加 k 个问答示例 | k=0, 1, 5 为最常见配置 |

### 2.2 评估工具

| 工具 | 说明 |
|------|------|
| **EleutherAI LM Evaluation Harness** | 最广泛使用的评估框架，内置 MMLU 支持 |
| **HELM（Holistic Evaluation of Language Models）** | Stanford 开发的综合评估框架 |
| **OpenCompass** | 国内常用的大模型评测框架 |
| **Hugging Face Open LLM Leaderboard** | 社区排行榜，MMLU 为核心指标之一 |

### 2.3 标准使用流程

1. **获取数据**：从官方源或 Hugging Face Datasets 获取 MMLU 数据集
2. **配置评估**：设置 few-shot 数量（0/1/5）、temperature、解码参数
3. **运行评估**：使用 lm-eval 等框架运行模型在 57 个学科上的推理
4. **分析结果**：
   - 报告整体准确率（Accuracy）作为主要指标
   - 按学科领域分组分析，识别模型在不同知识领域的长处和短板
   - 按难度分级（如 MMLU-Pro 提供更细粒度的难度标注）分析

---

## 三、学术研究中的三大用途

### 3.1 模型能力基线（Baseline）

MMLU 是评估模型知识储备的"通用语言"——大多数新模型论文中**必报的指标**。研究者通过报告 MMLU 分数为读者提供模型的"知识广度"基线。

### 3.2 跨模型对比（Cross-Model Comparison）

57 个学科的统一选择题格式提供了标准化"赛场"：
- 公平对比不同模型（如 GPT-4 vs Claude 3 vs Gemini）
- 同一模型不同版本的性能追踪（如 LLaMA 3 → LLaMA 4）
- 不同训练方法（如 SFT vs RLHF vs DPO）的消融对比

### 3.3 识别模型短板（Weakness Identification）

通过分析 57 个细分学科的表现，精准定位模型的特定领域不足：
- 法律学科准确率低 → 法律知识短板
- 道德学科接近随机 → 价值观对齐问题
- 抽象代数学科差 → 数学推理局限

---

## 四、局限与注意事项

### 4.1 饱和问题

当前顶尖模型在 MMLU 上的准确率已超过 90%，区分度显著下降——这直接导致 Artificial Analysis 在 v4.0 中将 MMLU-Pro 从 Intelligence Index 中移除，转向更具挑战性的评测。

### 4.2 数据污染（Data Contamination）

MMLU 的测试题目可能已在模型的训练数据中出现，导致分数虚高。研究者应在论文中讨论此风险。

### 4.3 格式局限

纯选择题格式无法评估模型的生成能力、推理过程质量和多步决策能力。

---

## 五、MMLU-Pro 变体

MMLU-Pro（Wang et al., 2024, arXiv:2406.01574）是 MMLU 的改进版本：
- **10 选项**（相比原版 4 选项），大幅降低随机猜中的概率
- **12,032 题**，在保持学科覆盖的同时提升难度
- 当前仍被 Artificial Analysis 作为额外评测运行（但已从 Intelligence Index 核心指数中移除）

---

## 六、学术引用规范

### 6.1 引用原始论文

> Hendrycks, D., Burns, C., Basart, S., Zou, A., Mazeika, M., Song, D., & Steinhardt, J. (2020). *Measuring Massive Multitask Language Understanding*. arXiv:2009.03300.

### 6.2 需在论文中描述

为确保可复现性，引用 MMLU 时必须在论文中详细描述：
- **数据集版本**：使用的 MMLU 具体版本（原版 / MMLU-Pro）
- **提示策略**：zero-shot 还是 few-shot（及其数量 k）
- **解码参数**：temperature（通常设为 0）、采样方式
- **评估框架**：使用 lm-eval / HELM / 其他框架的版本

### 6.3 结果报告示例

> "We evaluate our model on MMLU (Hendrycks et al., 2020) using the lm-eval harness (v0.4.x) in a 5-shot setting with temperature=0. Our model achieves 85.3% accuracy on average across all 57 subjects."
