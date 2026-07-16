# 对照实验: exp-tool-20260716

## 实验参数

| 项目 | 值 |
|------|-----|
| 维度 | 维度2：不同工具 |
| 被测对象 | opencode, CodeBuddy |
| 固定模型 | DSV4-Flash |
| 固定资料 | bim_source + frs_source + arXiv:2404.13501 |
| 创建时间 | 2026-07-16T09:57:00Z |
| 隔离方式 | git worktree（物理隔离） |

## 目录结构

```
exp-tool-20260716/
├── input/                  # 共享输入资料（锁定版本）
│   ├── bim_source/
│   ├── frs_source/
│   └── papers/
├── subjects/               # git worktree（每个被测对象独立隔离）
│   ├── opencode/           # worktree (branch: experiment/opencode)
│   │   ├── input/          # 输入资料副本（隔离）
│   │   ├── forest/         # 实验输出（待抽取）
│   │   └── .experiment_metadata.yaml
│   └── CodeBuddy/          # worktree (branch: experiment/CodeBuddy)
│       ├── input/
│       ├── forest/
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
终端 1: cd subjects/opencode  → 启动 opencode 会话
终端 2: cd subjects/CodeBuddy → 启动 CodeBuddy 会话
```

每个会话只看到自己 worktree 的文件，物理隔离，无法抄袭。

### 实验流程

1. 进入 worktree → 加载 forest-generation-methodology skill
2. 执行 9 步 SOP（Step 2-3：知识抽取）
3. 执行自评质量门禁（Step 6-7：索引生成 + 迭代修正）
4. 提交产物: `git add -A && git commit -m "experiment: {subject} extraction complete"`
5. 交叉评审 → 数据归集 → 报告输出

## 防抄袭机制

- 每个 subject 在独立 git worktree 中工作
- worktree 间物理隔离，互不可见
- 新会话上下文干净清洁，不继承历史
- 禁止读取其他 worktree 的 forest/ 输出

## 清理 worktree

```bash
git worktree remove subjects/opencode
git worktree remove subjects/CodeBuddy
```
