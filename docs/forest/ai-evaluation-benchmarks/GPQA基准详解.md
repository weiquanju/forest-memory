---
forest: aeb
tree: GPQA
branch: 基准方法论
title: GPQA基准详解
version: 1.0.0
created: 2026-07-15
updated: 2026-07-15
description: GPQA（Graduate-Level Google-Proof Q&A）基准详解——448 道博士专家编写的防谷歌科学推理题，Diamond 子集 198 题，GPT-4 基线 39% 准确率；可扩展监督研究与学术引用规范
keywords:
  - GPQA
  - 科学推理
  - 防谷歌
  - 可扩展监督
  - Diamond
  - 学术引用
source: "[论文] Rein et al. (2023). GPQA: A Graduate-Level Google-Proof Q&A Benchmark. arXiv:2311.12022"
refs:
  - "[aeb] MMLU基准详解 | MMLU 测'广度'，GPQA 测'深度'——二者在学术研究中通常互补使用"
  - "[aeb] Artificial Analysis Intelligence Index方法论 | GPQA Diamond 是 Intelligence Index v4.1 Scientific Reasoning 类别的组成评测之一"
  - "[frs] 推理评估基准演进 | GPQA 代表基准演进的'发展'阶段，为前沿模型的推理深度提供量化标尺"
---

# GPQA基准详解

## 一、性质与定位

**GPQA**（Graduate-Level Google-Proof Q&A，研究生级"防谷歌"问答基准）是一个**高难度的科学推理评测集**，专门设计用于衡量模型在研究生级科学问题上的深度推理能力。其核心特点是：这些题目即使专家借助网络搜索也难以轻易回答。

> 原始论文：Rein et al. (2023). *GPQA: A Graduate-Level Google-Proof Q&A Benchmark*. arXiv:2311.12022.

| 属性 | 说明 |
|------|------|
| **定位** | 学术基准（经同行评审） |
| **评估目标** | 衡量深度的科学推理和问题解决能力（非知识回忆） |
| **核心指标** | Accuracy（准确率） |
| **格式** | 448 道四选一选择题（Diamond 子集 198 题） |
| **学科** | 生物学、物理学、化学 |
| **当前状态** | 顶尖模型区分度仍高，GPT-4 基线 39%，是前沿模型的"试金石" |

### "防谷歌"（Google-Proof）含义

题目由对应学科博士专家编写，其设计确保：
- **领域专家**（有博士学位或在读博士）达到 **65% 准确率**（剔除事后发现的错误后为 74%）
- **高技能非专家验证者**尽管平均花费 **30 分钟以上**无限制上网搜索，准确率也仅为 **34%**
- 即：搜索引擎对解题的帮助有限，题目真正测试的是**科学推理**而非信息检索

---

## 二、数据集构成

### 2.1 全集与子集

| 子集 | 题数 | 说明 |
|------|------|------|
| **GPQA 全集** | 448 题 | 博士专家编写的完整评测集 |
| **GPQA Diamond** | 198 题 | 最高质量子集——由原作者定义为"两个专家均答对且多数非专家答错"的题目，具有最大的区分力和准确性 |

### 2.2 学科分布

| 学科 | 说明 |
|------|------|
| **生物学** | 分子生物学、遗传学、细胞生物学等研究生级问题 |
| **物理学** | 量子力学、固体物理、粒子物理等 |
| **化学** | 有机化学、无机化学、物理化学等 |

### 2.3 难度验证

| 群体 | 准确率 | 备注 |
|------|--------|------|
| 领域博士专家 | 65%（修正后 74%） | 设计目标群体 |
| 高技能非专家（30+分钟上网搜索） | 34% | 验证"防谷歌"特性 |
| GPT-4（最强基线） | 39% | 当前 AI 系统仍远低于专家水平 |

---

## 三、评估方法

### 3.1 提示策略

研究者可根据研究目的选择不同的提示策略：

| 策略 | 说明 | 适用场景 |
|------|------|----------|
| **零样本（Zero-Shot）** | 直接给出问题，不提供示例 | 测试模型的原始推理能力 |
| **少样本（Few-Shot）** | 提供少量问答示例 | 验证模型在示范下的推理能力 |
| **思维链（Chain-of-Thought, CoT）** | 要求模型展示逐步推理过程后才给出答案 | 研究推理过程质量和可解释性 |

### 3.2 数据获取

与 MMLU 不同，GPQA 数据集受管控：
- 需在 **Hugging Face** 上同意其使用条款后方可获取
- 这一管控机制旨在防止评测数据泄露到模型训练集中

### 3.3 评估工具

| 工具 | 说明 |
|------|------|
| **lm-eval（EleutherAI）** | 内置 GPQA 支持 |
| **OpenCompass** | 国内常用框架，支持 GPQA |
| **Artificial Analysis** | 商业平台运行 GPQA Diamond（5 次重复）作为 Intelligence Index 组成评测 |

---

## 四、学术研究中的两大用途

### 4.1 评估高级推理能力

GPQA 是测试模型在**最前沿、最困难科学问题上推理极限**的工具——它需要的是真正的推理而非简单的知识回忆。对于声称具有强推理能力的模型，GPQA 分数是不可或缺的验证指标。

### 4.2 可扩展监督研究（Scalable Oversight）

GPQA 的核心设计动机是研究**可扩展监督**：

> 原文："If we are to use future AI systems to help us answer very hard questions, for example, when developing new scientific knowledge, we need to develop scalable oversight methods that enable humans to supervise their outputs, which may be difficult even if the supervisors are themselves skilled and knowledgeable."

即：当 AI 系统超越人类能力时，人类如何有效监督其输出？GPQA 为这类"可扩展监督实验"提供了真实、困难的测试场景——题目对非专家极难（34%），而专家可以验证答案的正确性（65-74%）。

| 监督层级 | GPQA 准确率 | 含义 |
|----------|-------------|------|
| AI 生成答案 | GPT-4: 39% | AI 无法可靠回答 |
| 人类非专家监督 | 34% | 无法有效判断 AI 答案正确性 |
| 人类专家监督 | 65-74% | 可作为最终的"金标准"判断者 |

---

## 五、在学术研究中与其他基准的组合使用

### 5.1 广度 × 深度 组合

| 场景 | MMLU 角色 | GPQA 角色 |
|------|-----------|-----------|
| **新模型评估** | 通识知识基线（必报） | 推理深度验证（推荐报） |
| **新方法验证** | 检验泛化能力 | 检验推理深度提升 |
| **消融实验** | 快速迭代，验证基础能力无损 | 确认方法带来了真正的推理增益 |

### 5.2 GPQA Diamond 在商业评测中的角色

Artificial Analysis Intelligence Index v4.1 中，GPQA Diamond 作为 **Scientific Reasoning** 类别的组成评测（权重 6%），与 HLE（12%）和 CritPt（6%）共同构成科学推理维度。商业平台运行 GPQA 时使用 5 次重复、正则提取、pass@1 评分。

---

## 六、局限与注意事项

### 6.1 数据集规模

448 题（Diamond 198 题）的规模远小于 MMLU（15,908 题），统计显著性有限，尤其在进行学科细分分析时。

### 6.2 选择题格式

与 MMLU 类似，GPQA 也是四选一选择题格式，无法评估生成式能力。

### 6.3 受管控的数据集

由于需要同意使用条款才能获取，GPQA 的可访问性低于 MMLU，可能限制社区复现。

---

## 七、学术引用规范

### 7.1 引用原始论文

> Rein, D., Hou, B. L., Stickland, A. C., Petty, J., Pang, R. Y., Dirani, J., Michael, J., & Bowman, S. R. (2023). *GPQA: A Graduate-Level Google-Proof Q&A Benchmark*. arXiv:2311.12022.

### 7.2 需在论文中描述

- **使用的子集**：GPQA 全集还是 GPQA Diamond
- **提示策略**：zero-shot / few-shot / CoT
- **解码参数**：temperature（通常 0）、采样方式
- **评估框架**：lm-eval / OpenCompass 版本

### 7.3 结果报告示例

> "We evaluate on GPQA Diamond (Rein et al., 2023) using lm-eval in a 0-shot Chain-of-Thought setting with temperature=0. Our model achieves 52.1% accuracy, significantly outperforming the GPT-4 baseline of 39%."
