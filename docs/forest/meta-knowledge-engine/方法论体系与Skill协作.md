---
forest: mke
tree: 方法论体系
branch: 生成-评审闭环
title: 方法论体系与Skill协作
version: 1.0.0
created: 2026-07-15
updated: 2026-07-15
description: MKE 项目采用的三个 Skill 协作关系——forest-generation-methodology（生成）、forest-quality-reviewer（评审）、knowledge-atom-extractor（抽取）形成"生成-评审"闭环
keywords:
  - 方法论
  - Skill协作
  - 生成-评审闭环
  - 对照实验
  - SOP
  - 质量评审
refs:
  - "[mke] 知识领域森林理论 | 方法论的组织对象"
  - "[mke] LLM知识抽取器设计 | 架构层抽取器"
  - "[mke] 项目定位与边界声明 | 方法论的适用范围"
  - "[aeb] Artificial Analysis Intelligence Index方法论 | 评审标准来源"
---

# 方法论体系与Skill协作

## 定位

MKE 项目的知识构建和质量保障不是"一次性工程"，而是基于三个标准化 Skill 构成的**可复现方法论体系**。三个 Skill 形成"生成→评审"闭环，支持对照实验和多模型量化比较。

## 三个 Skill 的职责

| Skill | 角色 | 核心能力 |
|-------|------|---------|
| `forest-generation-methodology` | **方法论型**——定义从原始资料到知识森林的 9 步 SOP | 输入策展→主题设计→LLM抽取→交叉声明检测→引用建立→引用审计→索引生成→迭代修正→元数据记录 |
| `knowledge-atom-extractor` | **工具型**——LLM 知识抽取的具体执行器 | 标准抽取/代码抽取/经验抽取 + 向量相似度交叉声明检测 + 阈值分级处理 |
| `forest-quality-reviewer` | **评审型**——5 维度质量评审 + Intelligence Index 能力映射 | 引用真实性→引用准确性→层级组织→批判性分析→学术规范→AAI 能力映射 |

## 协作关系

```
┌──────────────────────────────────────────────────────┐
│  forest-generation-methodology                        │
│  (方法论: 定义 9 步 SOP)                               │
│                                                        │
│  Step 2,3 ──→ knowledge-atom-extractor (抽取+检测)     │
│  Step 5  ──→ arxiv-mcp-server (引用审计)              │
└──────────┬───────────────────────────────────────────┘
           │ 产出物: 知识森林
           ▼
┌──────────────────────────────────────────────────────┐
│  forest-quality-reviewer                              │
│  (评审: 5 维度 + AAI 映射)                             │
│                                                        │
│  Step 6  ←─ aeb (AAI/MMLU/GPQA) 能力基准              │
└──────────┬───────────────────────────────────────────┘
           │ 产出物: 5 维度评分 + 能力映射
           ▼
┌──────────────────────────────────────────────────────┐
│  对照实验平台                                           │
│  同资料 × 不同模型 × 相同评审方法 → 可复现量化对照数据    │
└──────────────────────────────────────────────────────┘
```

## 9 步 SOP 概述

`forest-generation-methodology` 定义了从原始资料到完整知识森林的标准化流程：

| Step | 阶段 | 核心动作 | 使用工具 |
|------|------|---------|---------|
| 0 | 输入资料策展 | 选择高质量基础资料 | 质量评估清单 |
| 1 | 森林主题设计 | 划分 Forest/Tree/Branch 层级 | 设计原则 + 粒度控制 |
| 2 | LLM 知识原子抽取 | 将资料拆分为知识原子 | knowledge-atom-extractor |
| 3 | 交叉声明检测 | 检测重复/冲突声明 | knowledge-atom-extractor |
| 4 | 引用关系建立 | 建立 intra/cross-forest refs | refs 格式规范 |
| 5 | 引用真实性审计 | 逐条验证引用存在性 | arxiv-mcp-server |
| 6 | 索引文件生成 | 生成 index.md 元数据 | 模板 |
| 7 | 迭代修正追踪 | 结构化记录修正 | 修正日志 + Few-shot 反馈 |
| 8 | 实验元数据记录 | 记录可复现参数 | .experiment_metadata.yaml |

> 完整 SOP 参见 `.codebuddy/skills/forest-generation-methodology/SKILL.md`

## 5 维度评审体系概述

`forest-quality-reviewer` 定义了标准化的知识森林质量评估体系：

| 维度 | 评估目标 | 评分标准 |
|------|---------|---------|
| D1 引用真实性 | 引用是否真实存在（非虚构） | 0 虚构 + ≥95% 验证 = 9-10 |
| D2 引用准确性 | 元数据和语境是否正确 | 0-5% 问题率 = 9-10 |
| D3 层级组织 | Forest→Tree→Branch→Leaf 结构质量 | 最高相似度 < 0.80 = 9-10 |
| D4 批判性分析 | 内容深度和客观性 | 横向对比+局限性+张力 = 9-10 |
| D5 学术规范 | 格式规范和方法论完整性 | 完整遵循所有规范 = 9-10 |

Step 6 将 5 维度评分映射到 Artificial Analysis Intelligence Index 的能力空间，建立"模型能力→知识质量"的定量关系。

> 完整评审体系参见 `.codebuddy/skills/forest-quality-reviewer/SKILL.md`

## 对照实验框架

三个 Skill 的核心价值在于支持**可复现的对照实验**：

```
固定变量：
  ├── 输入资料（同一份，锁定版本）
  ├── 方法论（9 步 SOP，不变）
  ├── 评测方法（5 维度评审，不变）
  └─ 评审者模型（固定为同一个高能力模型）

自变量：
  └── LLM 模型（Model A vs Model B vs Model C）

因变量：
  ├── 5 维度评分
  ├── 综合评分
  ├── 人工修正率
  └── 生成效率（时间/token 消耗）
```

对照实验数据将记录在 `forest-generation-methodology` 的 Step 8 中，评审结果由 `forest-quality-reviewer` 产出。MKE 自身的知识森林（bim/frs/aic/aeb 四森林）即为首轮实验对象。

## Skill 位置

三个 Skill 均为项目级 Skill，位于：

```
.codebuddy/skills/
├── forest-generation-methodology/   (生成方法论)
├── forest-quality-reviewer/         (质量评审)
└── knowledge-atom-extractor/        (知识原子抽取)
```

## 与 MKE 架构的关系

| MKE 架构层 | 对应 Skill 能力 |
|-----------|----------------|
| 第一层：数据接入 | knowledge-atom-extractor 的抽取模式选择 |
| 第二层：知识构建 | knowledge-atom-extractor 的 LLM 抽取 + 交叉声明检测 |
| 第三层：混合检索 | forest-quality-reviewer D3 层级组织评审的对象 |
| 第四层：记忆融合 | （未来）对照实验的记忆回灌 |
| 第五层：治理校验 | forest-generation-methodology Step 5 引用审计 + forest-quality-reviewer D1/D2 |

> MKE 的 LLM 抽取器架构设计参见 [LLM知识抽取器设计](LLM知识抽取器设计.md)，Skill 层面的抽取方法论（脚本使用、阈值校准、Few-shot 迭代）在 knowledge-atom-extractor 中定义。两者是架构与工具的关系。
