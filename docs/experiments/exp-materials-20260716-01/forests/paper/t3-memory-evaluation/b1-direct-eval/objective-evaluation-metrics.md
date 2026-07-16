---
forest: agent-memory-survey
tree: t3-memory-evaluation
branch: b1-direct-eval
title: 客观评估指标
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
source: "[arXiv:2404.13501] Section 6.1.2"
refs:
  - "[t3-b1] 主观评估框架 | 客观评估的互补方法"
---

# 客观评估指标

## 概述

客观评估通过数值指标量化记忆模块的效果和效率，使不同模块可以直接比较。

## 效果评估（Effectiveness）

### 1. Result Correctness（结果正确性）

**定义**：Agent 是否能基于记忆模块成功回答预定义问题。

**计算**：
```
Correctness = (1/N) Σ I[a_i = â_i]

其中：a_i = ground truth, â_i = agent 回答
I[a_i = â_i] = 1 if 匹配，否则 0
```

**代表实现**：
- Hu et al. [96]：从历史记录构建带标注 ground truth 的问题，计算记忆是否能匹配正确答案
- Packer et al. [100]：生成只能从过去会话中推导的问题和答案，与 ground truth 比较

### 2. Reference Accuracy（参考准确性）

**定义**：评估 Agent 是否能发现**相关**的记忆内容来回答问题（关注中间推理过程而非最终结果）。

**计算（F1-score）**：
```
F1 = 2 × (Precision × Recall) / (Precision + Recall)

Precision = TP / (TP + FP)
Recall = TP / (TP + FN)

其中：TP = 真阳性记忆内容数, FP = 假阳性, FN = 假阴性
```

**Result Correctness vs Reference Accuracy**：

| 维度 | Result Correctness | Reference Accuracy |
|------|-------------------|-------------------|
| 关注点 | 最终答案 | 中间参考信息 |
| 指标 | Accuracy | F1-score |
| 评估目标 | "答对了吗？" | "找对参考了吗？" |

**代表实现**：
- Lu et al. [94]：F1-score 评估记忆检索过程
- Zhong et al. [6]：评估相关记忆是否能被成功检索

## 效率评估（Efficiency）

### Time & Hardware Cost（时间与硬件成本）

| 指标 | 定义 | 计算 |
|------|------|------|
| Adaptation Time | 记忆写入+管理的时间 | Δt = (1/M) Σ (t^end_i - t^start_i) |
| Inference Time | 记忆读取的时间延迟 | 同上 |
| Peak GPU Memory | 内存操作的峰值 GPU 占用 | — |

**代表实现**：
- Tack et al. [106]：使用峰值内存分配和适应时间来评估记忆操作效率

## 客观 vs 主观评估对比

| 维度 | 主观评估 | 客观评估 |
|------|---------|---------|
| 可量化性 | 低（依赖人类判断） | 高（数值指标） |
| 可复现性 | 低 | 高 |
| 适用场景 | 无 ground truth 的场景 | 可定义 ground truth 的场景 |
| 成本 | 高（需人类标注者） | 低（自动计算） |
| 可解释性 | 高（标注者提供理由） | 低（纯数值） |

## 开放问题

论文明确指出一个重要缺口：**目前不存在针对 LLM-based Agent 记忆模块的开源标准化 benchmark**（Section 6.3）。这导致不同研究的评估结果难以直接比较。
