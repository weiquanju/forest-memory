# 对照实验项目目录结构模板

> 使用 `setup_experiment.sh` 脚本自动创建，基于 git worktree 实现物理隔离。

## 快速创建

```bash
# 在实验项目根目录执行（脚本自动检查/初始化 git 仓库）
bash .codebuddy/skills/forest-generation-methodology/assets/setup_experiment.sh \
    <project_name> <subject1> [subject2] [subject3] ...

# 示例
bash setup_experiment.sh exp-model-20260716 dsv4flash dsv4pro glm52
bash setup_experiment.sh exp-tool-20260716 codebuddy qwen-codex claude-code
bash setup_experiment.sh exp-source-20260716 bim frs paper-2404-13501
```

## 目录结构（git worktree 方案）

```
forest-memory-experiments/                # 独立 Git 仓库（脚本自动 init）
│
├── README.md                              # 实验项目说明（脚本生成）
├── .experiment_metadata_template.yaml      # 环境声明模板
├── .gitignore
│
├── input/                                 # 共享输入资料（锁定版本，主分支管理）
│   ├── bim_source/
│   │   └── 人脑记忆机制的数据结构与算法分析.md
│   ├── frs_source/
│   │   └── AI与大模型...前沿研究综述.md
│   └── papers/
│       └── 2404.13501.pdf
│
├── subjects/                              # git worktree 根目录（物理隔离）
│   │
│   ├── dsv4flash/                         # worktree (branch: experiment/dsv4flash)
│   │   ├── input/                         # 输入资料副本（隔离）
│   │   ├── forest/                        # 该 subject 的实验输出
│   │   │   ├── index.md
│   │   │   └── ...                        # 知识原子 .md 文件
│   │   ├── .experiment_metadata.yaml      # 实验元数据
│   │   └── .gitignore
│   │
│   ├── dsv4pro/                           # worktree (branch: experiment/dsv4pro)
│   │   ├── input/
│   │   ├── forest/
│   │   └── .experiment_metadata.yaml
│   │
│   └── glm52/                             # worktree (branch: experiment/glm52)
│       ├── input/
│       ├── forest/
│       └── .experiment_metadata.yaml
│
├── reviews/                               # 评审报告（主分支管理，交叉评审）
│   ├── review-dsv4flash-by-dsv4pro.md    # 命名规则: review-{被评审}-by-{评审者}
│   ├── review-dsv4flash-by-glm52.md
│   ├── review-dsv4pro-by-dsv4flash.md
│   ├── review-dsv4pro-by-glm52.md
│   └── ...
│
└── results/                               # 汇总结果（主分支管理）
    ├── comparison-matrix-models.md        # 维度1: 不同模型对照矩阵
    ├── comparison-matrix-tools.md         # 维度2: 不同工具对照矩阵
    ├── comparison-matrix-sources.md       # 维度3: 不同资料对照矩阵
    └── capability-quality-mapping.md      # 能力-质量映射表更新
```

## 隔离原理

git worktree 为每个 subject 创建独立的工作目录（物理隔离）：
- 每个 worktree 是独立的文件系统目录
- 新会话 `cd subjects/{subject}/` 后只能看到自己的 `input/` 和 `forest/`
- worktree 间互不可见，天然防止抄袭
- 不同 worktree 可在不同终端并行执行

## 合并流程

实验完成后，各 worktree 的结果需要合并到主分支：

```bash
bash .codebuddy/skills/forest-generation-methodology/assets/merge_experiment.sh
```

合并脚本自动完成：
- 将各 worktree 分支的 `forest/`、`input/`、`.experiment_metadata.yaml` 合并到主分支
- 生成 `results/comparison-matrix-models.md` 和 `REPORT.md` 模板
- 提交合并结果到 main 分支

合并后各 subject 的 `forest/` 内容在主分支可见，评审者可直接读取。

## 命名规则

### 实验 ID

```
exp-{序号:3位}-{模型简称}-{资料简称}
```

| 模型简称 | 对应模型 |
|---------|---------|
| dsv4flash | DeepSeek V4 Flash (AAI 40) |
| dsv4pro | DeepSeek V4 Pro (AAI 44) |
| glm52 | GLM-5.2 (AAI 51) |
| claude-s46 | Claude Sonnet 4.6 (AAI ~55) |
| claude-f5 | Claude Fable 5 (AAI 60) |

| 资料简称 | 对应资料 |
|---------|---------|
| bim | 人脑记忆机制源文档 |
| frs | 前沿研究综述源文档 |
| paper | 顶级期刊论文 |

### 实验目录数计算

```
模型数 × 资料数 = 实验目录数

Phase 1: 3 模型 × 3 资料 = 9 个实验目录
Phase 2: + 顶级模型 × 3 资料 = +3 个实验目录
```

### 评审报告数计算

```
实验数 × (模型数 - 1) = 评审报告数

Phase 1: 9 实验 × 2 评审者 = 18 份评审报告
```

## 项目隔离要求

1. **独立 Git 仓库**：实验项目必须是独立的 Git 仓库，不与 forest-memory 主项目共享
2. **无引用依赖**：实验输出不得引用 forest-memory 主项目的文件路径
3. **输入锁定**：`input/` 目录一旦创建不可修改，确保不同实验使用完全相同的输入
4. **工具锁定**：同一维度内的实验必须使用相同工具版本，记录在 `.experiment_metadata.yaml` 中
5. **会话隔离（强制）**：每个实验（被测对象）必须在全新会话中执行，上下文干净清洁，不得继承之前会话的抽取结果、修正记录或评审数据
6. **防抄袭机制（强制）**：使用 git worktree 实现物理隔离——每个 subject 在独立 worktree 中执行，worktree 间互不可见。新会话进入各自 worktree 目录，无法读取其他 subject 的 `forest/` 输出。由 `setup_experiment.sh` 脚本自动创建 worktree

## 社区贡献流程

1. Fork 实验项目仓库
2. 运行 `setup_experiment.sh` 创建实验环境（自动初始化 git worktree）
3. 选择一个 subject 的 worktree，在新会话中执行
4. 执行 forest-generation-methodology 的 9 步 SOP
5. 执行交叉评审（不能自评）
6. 提交 PR，包含：
   - `subjects/{subject}/forest/` 完整实验输出
   - `subjects/{subject}/.experiment_metadata.yaml` 实验元数据
   - `reviews/review-{subject}-by-{reviewer}.md` 评审报告
   - 更新 `results/` 下的对照矩阵
