# 对照实验项目目录结构模板

> 复制此结构创建独立的实验项目，与 forest-memory 主项目隔离。

```
forest-memory-experiments/
│
├── README.md                              # 实验项目说明
├── .experiment_metadata_template.yaml      # 环境声明模板（复制使用）
│
├── input/                                 # 输入资料（锁定版本，不可修改）
│   ├── bim/
│   │   └── 人脑记忆机制的数据结构与算法分析.md   # bim 源文档
│   ├── frs/
│   │   └── AI与大模型...前沿研究综述.md         # frs 源文档
│   └── paper-2404.13501/
│       ├── paper.md                       # 论文全文（Markdown 格式）
│       └── paper.pdf                      # 论文原始 PDF
│
├── experiments/                           # 实验输出（每次实验一个目录）
│   │
│   ├── exp-001-dsv4flash-bim/            # 命名规则: exp-{序号}-{模型}-{资料}
│   │   ├── .experiment_metadata.yaml      # 实验元数据（必填）
│   │   ├── forest/                        # 生成的知识森林
│   │   │   ├── index.md
│   │   │   └── ...                        # 知识原子 .md 文件
│   │   └── correction-log.md              # 修正日志（Step 7 产出）
│   │
│   ├── exp-002-dsv4pro-bim/
│   ├── exp-003-glm52-bim/
│   ├── exp-004-dsv4flash-frs/
│   ├── exp-005-dsv4pro-frs/
│   ├── exp-006-glm52-frs/
│   ├── exp-007-dsv4flash-paper/
│   ├── exp-008-dsv4pro-paper/
│   ├── exp-009-glm52-paper/
│   └── ...
│
├── reviews/                               # 评审报告（交叉评审）
│   ├── review-exp001-by-dsv4pro.md        # 命名规则: review-{实验ID}-by-{评审者}
│   ├── review-exp001-by-glm52.md
│   ├── review-exp002-by-dsv4flash.md
│   ├── review-exp002-by-glm52.md
│   └── ...
│
└── results/                               # 汇总结果
    ├── comparison-matrix-models.md        # 维度1: 不同模型对照矩阵
    ├── comparison-matrix-tools.md         # 维度2: 不同工具对照矩阵
    ├── comparison-matrix-sources.md       # 维度3: 不同资料对照矩阵
    └── capability-quality-mapping.md      # 能力-质量映射表更新
```

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

## 社区贡献流程

1. Fork 实验项目仓库
2. 选择一个实验组合（模型 × 资料）
3. 复制 `.experiment_metadata_template.yaml`，填写实验环境
4. 执行 forest-generation-methodology 的 9 步 SOP
5. 执行交叉评审（不能自评）
6. 提交 PR，包含：
   - `experiments/exp-XXX-XXX-XXX/` 完整实验目录
   - `reviews/review-exp-XXX-by-XXX.md` 评审报告
   - 更新 `results/` 下的对照矩阵
