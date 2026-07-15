---
forest: aeb
title: AI评测基准（AI Evaluation Benchmarks）
version: 1.0.0
created: 2026-07-15
updated: 2026-07-15
description: AI 模型能力评测基准的知识森林——覆盖行业第三方评测平台（Artificial Analysis Intelligence Index）与学术标准基准（MMLU、GPQA）三大评测体系，涵盖方法论、构成、定位与学术引用规范
source: "[对话] DeepSeek 学术研究专家对话 (2026-07-15) | https://chat.deepseek.com/share/pixeyu4dh1pg2ckfpy"
refs:
  - "[frs] 推理评估基准演进 | MMLU、GPQA 是基准演进中'早期→发展'阶段的代表性静态基准，aeb 补充其性质、方法与引用规范"
---

# AI评测基准（AI Evaluation Benchmarks）

## 定位

本森林收纳 **AI 模型能力评测基准的方法论知识**——覆盖三类主流评测体系：

| 类型 | 代表 | 属性 |
|------|------|------|
| 行业第三方评测平台 | Artificial Analysis Intelligence Index | 商业评测机构、动态版本演进、复合加权评分 |
| 通识知识学术基准 | MMLU | 学术论文、静态数据集、57 学科广度覆盖 |
| 深度推理学术基准 | GPQA | 学术论文、静态数据集、博士级难度 |

区别于 frs 森林的"基准演进趋势"，本森林聚焦于**单个基准的深度方法论**，包括：评测构成、评分方法、定位特点、优势局限、以及学术引用规范。

## 森林内文档

### 树：Artificial Analysis Intelligence Index

| 文档 | 说明 |
|------|------|
| [指数方法论详解](Artificial%20Analysis%20Intelligence%20Index方法论.md) | v4.1 方法论：9 项评测 × 四大能力维度（Agent/Coding/Scientific/General）加权体系 + 学术引用规范 |

### 树：MMLU

| 文档 | 说明 |
|------|------|
| [MMLU基准详解](MMLU基准详解.md) | 57 学科 15,908 题：零样本评估范式 + 三大用途（基线/对比/短板） + 使用流程与引用规范 |

### 树：GPQA

| 文档 | 说明 |
|------|------|
| [GPQA基准详解](GPQA基准详解.md) | 448 题 Diamond 子集：研究生级"防谷歌"科学推理评测 + 可扩展监督研究 + 引用规范 |

## 三基准对比

| 维度 | Artificial Analysis | MMLU | GPQA |
|------|---------------------|------|------|
| **类型** | 第三方行业评测平台 | 学术基准 | 学术基准 |
| **核心目标** | 综合模型能力排名 | 知识广度（通识理解） | 知识深度（科学推理） |
| **规模** | 9 项评测，动态更新 | 57 学科，15,908 题 | 448 题（Diamond: 198 题） |
| **格式** | 多种（Agent/Coding/QA） | 四选一选择题 | 四选一选择题 |
| **评分** | 加权平均，pass@1 | Accuracy（准确率） | Accuracy（准确率） |
| **版本** | 动态（当前 v4.1，2026-06） | 静态（arXiv:2009.03300） | 静态（arXiv:2311.12022） |
| **同行评审** | 否（商业平台） | 是 | 是 |
| **区分度** | 中 | 低（接近饱和） | 高 |
| **引用层级** | 补充性行业数据 | 标准学术引用（必报指标） | 标准学术引用（推理试金石） |

## 引用规范

- 本森林的叶子通过 `refs` 向 frs 发出跨森林引用，形成"frs 覆盖演进趋势 + aeb 覆盖单基准方法论"的互补关系
- 引用格式：`[aeb] 文档标题 | 引用说明`
- 学术基准（MMLU/GPQA）需引用原始论文，并用 ArXiv 永久链接确保可复现性
- 第三方评测平台（Artificial Analysis）需标注具体版本号和访问日期
