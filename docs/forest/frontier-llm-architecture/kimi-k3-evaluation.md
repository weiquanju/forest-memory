---
forest: flm
tree: 评估与能力
branch: 基准评测
title: Kimi K3 评测结果
version: 1.0.0
created: 2026-07-29
updated: 2026-07-29
description: Kimi K3 在编程、Agent、知识和视觉四个维度的基准评测结果——开源前沿模型定位，超越其他开源和商业模型但落后于 Claude Fable 5 和 GPT-5.6 Sol。
keywords:
  - benchmark evaluation
  - Kimi K3
  - coding benchmark
  - agent benchmark
  - knowledge benchmark
  - vision benchmark
refs:
  - "[flm] DeepSeek-V4 评测结果 | 对比性评测"
  - "[flm] 长上下文效率对比 | 效率维度分析"
---

# Kimi K3 评测结果

## 总体定位

> "Consistently outperforms other open and proprietary models evaluated in our suite, while overall performance still trails the most powerful proprietary models — Claude Fable 5 and GPT-5.6 Sol."

## 编程（Coding）

| 基准 | Kimi K3 得分 | 对比 |
|------|:---:|------|
| DeepSWE | 67.5 | 低于 GPT-5.6 Sol (73.0), Fable 5 (70.0) |
| Terminal-Bench 2.1 | 88.3 | 仅低于 GPT-5.6 Sol (88.8) |
| FrontierSWE | 81.2 | 仅低于 Fable 5 (86.6) |
| Kimi Code Bench 2.0 | 72.9 | 仅低于 Fable 5 (76.9) |
| ProgramBench | 77.8 | 最高 |
| SWE-Marathon | 42.0 | 最高 |

## 通用 Agent 与视觉 Agent

| 基准 | Kimi K3 得分 | 排名 |
|------|:---:|:---:|
| GDPval-AA v2 (Elo) | 1686 | 第三（后 Fable 5, GPT-5.6 Sol） |
| BrowseComp | 91.2 | 最高 |
| AutomationBench | 30.8 | 最高 |
| JobBench | 54.3 | 第二（后 Fable 5） |
| CharXiv (RQ) w/ tool | 91.3 | 第二（后 Fable 5） |
| Zerobench w/ tool | 41.0 | 与 GPT-5.5 并列第二 |

## 评估特点

### 专用内部基准
- Kimi Code Bench 2.0（内部编程基准）
- 多域 RL 环境中的可验证问题（search, professional workflows, visual reasoning）

### 推理努力 All-Max
所有对比评估使用最大推理努力（max/xhigh thinking effort）

### 模型发布
**Full model weights** 在 HuggingFace 公开发布（https://huggingface.co/moonshotai/Kimi-K3）

## 效率维度

RL 阶段 scaling FLOPs 持续改善所有能力域（knowledge, reasoning, vision, general agent, coding），tool-call steps 同步增长。
