# 对照实验: exp-model-20260716-01

## 实验维度
**维度1（不同模型）**：固定工具 + 固定资料，变化 LLM 模型。

## 被测对象
| 模型 | AAI | 模型简称 |
|------|:---:|---------|
| DeepSeek V4 Flash | 40 | dsv4flash |
| DeepSeek V4 Pro | 44 | dsv4pro |
| GLM-5.2 | 51 | glm52 |

## 固定变量
- **工具**: CodeBuddy v4.10.2
- **输入资料**: bim_source / frs_source / arXiv:2404.13501（3 份标准资料）
- **方法论**: forest-generation-methodology v1.0.0
- **评审方法**: forest-quality-reviewer v1.0.0

## 目录结构
```
exp-model-20260716-01/
├── input/                            # 共享输入资料（锁定版本）
│   ├── bim_source/
│   ├── frs_source/
│   └── papers/
├── subjects/                         # git worktree（物理隔离）
│   ├── dsv4flash/                    # worktree (branch: experiment/dsv4flash)
│   │   ├── input/                    # 输入资料副本（隔离）
│   │   ├── forest/                   # 实验输出（待抽取）
│   │   └── .experiment_metadata.yaml
│   ├── dsv4pro/                      # worktree (branch: experiment/dsv4pro)
│   │   ├── input/
│   │   ├── forest/
│   │   └── .experiment_metadata.yaml
│   └── glm52/                        # worktree (branch: experiment/glm52)
│       ├── input/
│       ├── forest/
│       └── .experiment_metadata.yaml
├── reviews/                          # 评审报告（交叉评审）
├── .experiment_metadata_template.yaml
└── README.md
```

## 执行方式

### 串行执行
对每个被测对象依次在新会话中执行：
```bash
# 1. 进入 worktree（新会话）
cd exp-model-20260716-01/subjects/dsv4flash

# 2. 在新会话中加载 forest-generation-methodology skill
# 3. 执行 9 步 SOP（Step 2-3: LLM 知识抽取）
# 4. 完成后提交
git add -A && git commit -m "experiment: dsv4flash extraction complete"

# 5. 切换到下一个 subject（新会话）
cd ../dsv4pro
```

### 并行执行（推荐）
为每个被测对象打开独立终端 + 独立会话：
```
终端 1: cd subjects/dsv4flash  →  DeepSeek V4 Flash 会话
终端 2: cd subjects/dsv4pro    →  DeepSeek V4 Pro 会话
终端 3: cd subjects/glm52      →  GLM-5.2 会话
```

## 防抄袭机制
- 每个 subject 在独立 git worktree 中工作，物理隔离
- worktree 间互不可见，无法读取其他 subject 的 forest/ 输出
- 新会话上下文干净清洁，不继承历史

## 交叉评审矩阵
```
被测对象          评审者
                dsv4flash   dsv4pro   glm52
dsv4flash        ✗ 跳过      ✓ (R1+R2)  ✓ (v1+v2)
dsv4pro          ✓ (v1+v2)   ✗ 跳过    ✓ (v2+v3)
glm52            ✓ (R1+R2)   ✓ (R1+R2)  ✗ 跳过
```

两轮评审：首轮（R1）9 份 + 自评质量门禁后重评轮（R2/v2/v3）6 份 = 共 **15 份评审报告**。详见 `REPORT.md`。

## 创建时间
2026-07-16
