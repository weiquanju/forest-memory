# 对照实验: exp-materials-20260716-01

## 实验概述

| 参数 | 值 |
|------|-----|
| 实验维度 | 维度3：不同资料对照 |
| 固定模型 | DeepSeek V4 Pro (AAI 44) |
| 固定工具 | CodeBuddy |
| 自变量 | bim 源文档 / frs 源文档 / arXiv:2404.13501 |
| 被测对象 | bim, frs, paper |
| 创建时间 | 2026-07-16 |
| 研究方法论 | forest-generation-methodology v1.0.0 |
| 评审方法论 | forest-quality-reviewer v1.0.0 |

## 实验目的

验证 forest-generation-methodology 在不同类型输入资料上的知识抽取质量差异：
- **bim**: 领域综述型（人脑记忆机制的数据结构与算法分析）
- **frs**: 前沿研究综述型（AI与大模型前沿研究综述）
- **paper**: 单篇学术论文（arXiv:2404.13501, LLM Agent Memory Survey）

## 目录结构

```
exp-materials-20260716-01/
├── input/                  # 共享输入资料（从 assets/input/ 自动复制，锁定版本）
│   ├── bim_source/
│   ├── frs_source/
│   └── papers/
├── subjects/               # git worktree（物理隔离）
│   ├── bim/                # worktree (branch: experiment/bim)
│   │   ├── input/          # 仅 bim_source
│   │   ├── forest/         # 实验输出（待抽取）
│   │   └── .experiment_metadata.yaml
│   ├── frs/                # worktree (branch: experiment/frs)
│   │   ├── input/          # 仅 frs_source
│   │   ├── forest/         # 实验输出（待抽取）
│   │   └── .experiment_metadata.yaml
│   └── paper/              # worktree (branch: experiment/paper)
│       ├── input/          # 仅 papers/2404.13501
│       ├── forest/         # 实验输出（待抽取）
│       └── .experiment_metadata.yaml
├── reviews/                # 评审报告（交叉评审）
├── results/                # 对照矩阵和汇总结果
├── .experiment_metadata_template.yaml
└── README.md
```

## 执行方式

### 并行执行（推荐）

为每个被测对象打开独立终端 + 独立会话：

```
终端 1: cd subjects/bim   → 新会话 → 抽取 bim 森林
终端 2: cd subjects/frs   → 新会话 → 抽取 frs 森林
终端 3: cd subjects/paper → 新会话 → 抽取 paper 森林
```

每个 waytree 只包含对应的一份输入资料,物理隔离,互不可见。

### 执行流程

每个 subject 在新会话中依次完成:
1. 加载 `forest-generation-methodology` skill
2. 对 `input/` 下的资料执行 9 步 SOP（Step 2-3 LLM抽取 + Step 6-7 索引生成+门禁）
3. 输出到 `forest/`
4. 执行自评质量门禁（技术检查：空文件/YAML完整性/index存在性/命名规范）
5. Commit: `git add -A && git commit -m "experiment: {subject} extraction complete"`

## 交叉评审矩阵

| 被评审者 \ 评审者 | bim | frs | paper |
|-------------------|-----|-----|-------|
| bim               | ✗   | ✓   | ✓     |
| frs               | ✓   | ✗   | ✓     |
| paper             | ✓   | ✓   | ✗     |

共 6 组评审数据，每个森林被 2 个外部评审者评估。

## 防抄袭机制

- git worktree 物理隔离,worktree 间互不可见
- 每个 subject 在全新会话中独立执行
- 上下文清洁,不继承历史
- 禁止读取其他 worktree 的 forest/ 输出
