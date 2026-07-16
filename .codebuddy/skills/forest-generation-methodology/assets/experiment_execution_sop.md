---
title: 对照实验执行 SOP
type: methodology-asset
parent_skill: forest-generation-methodology
version: 1.0.0
created: 2026-07-16
status: active
---

# 对照实验执行 SOP

> 本文档是 `forest-generation-methodology` 9 步生成 SOP 的**实验场景变体**。
> 它不重复 9 步方法论本身，只定义实验场景特有的：启动协议、环境隔离、三维度分支、交叉评审调度。
> 执行实验时，9 步 SOP 仍按原步骤推进，本文档负责"在什么变量上变化、如何对照、如何评审"。

---

## Step 0：启动协议（强制）

**LLM 在开始任何对照实验前必须执行此步骤，不得跳过。**

LLM 必须使用 `ask_followup_question` 工具一次性向用户提出以下 4 个问题（不可分多次询问，避免打断用户）：

| 问题 ID | 问题 | 选项 |
|---------|------|------|
| `dimension` | 本次实验在哪个维度上变化？ | 维度1：不同模型 / 维度2：不同工具 / 维度3：不同资料 |
| `fixed_vars` | 固定变量的具体值（根据维度自动确定哪些需要固定） | 由用户填写 |
| `subjects` | 被测对象列表（自变量取值，至少 2 个） | 由用户填写 |
| `project_name` | 实验项目名称（用于目录命名） | 由用户填写 |

### 询问模板

LLM 应使用如下结构构造 `ask_followup_question` 的 `questions` 参数（JSON 数组）：

```json
[
  {
    "id": "dimension",
    "header": "实验维度",
    "question": "本次对照实验在哪个维度上变化？其余两个维度将作为固定变量。",
    "multiSelect": false,
    "options": [
      {"label": "维度1：不同模型", "description": "固定工具+资料，变化 LLM 模型。验证 AAI 能力门槛。"},
      {"label": "维度2：不同工具", "description": "固定模型+资料，变化 AI 编程工具。验证工具差异。"},
      {"label": "维度3：不同资料", "description": "固定工具+模型，变化输入资料。验证方法论普适性。"}
    ]
  },
  {
    "id": "subjects",
    "header": "被测对象",
    "question": "请列出本次实验的被测对象（自变量取值，至少 2 个，用逗号分隔）。例如维度1：'GLM-5.2, DSV4-Pro, DSV4-Flash'。",
    "multiSelect": false,
    "options": [
      {"label": "（由用户填写）", "description": "在回复中直接写出被测对象列表"}
    ]
  },
  {
    "id": "project_name",
    "header": "实验项目名",
    "question": "实验项目名称（用于创建独立实验目录，建议格式：exp-{维度简写}-{日期}，如 exp-model-20260716）。",
    "multiSelect": false,
    "options": [
      {"label": "（由用户填写）", "description": "在回复中直接写出项目名称"}
    ]
  }
]
```

### 用户回答后的处理

1. 根据维度自动推导固定变量：
   - 维度1（模型）：固定工具 = 当前工具，固定资料 = `bim源文档 + frs源文档 + arXiv:2404.13501`
   - 维度2（工具）：固定模型 = 用户指定，固定资料 = 同上
   - 维度3（资料）：固定工具 = 当前工具，固定模型 = 用户指定
2. 若用户未指定固定模型/工具，LLM 应再次询问（不得假设）。
3. 启动协议完成后，进入 Step 1。

---

## Step 1：实验环境隔离

使用 [`setup_experiment.sh`](setup_experiment.sh) 脚本基于 **git worktree** 创建物理隔离的实验环境：

```bash
# 在实验项目根目录执行（脚本会自动检查/初始化 git 仓库）
bash .codebuddy/skills/forest-generation-methodology/assets/setup_experiment.sh \
    exp-model-20260716 dsv4flash dsv4pro glm52
```

脚本自动完成：检查/初始化 git 仓库 → 创建目录结构 → 为每个 subject 创建独立 worktree → 复制 input/ 副本 → 生成元数据文件。

**目录结构（git worktree 方案）**：

```
{experiment_repo}/                          # 独立 Git 仓库（脚本自动 init）
├── input/                                   # 共享输入资料（锁定版本，主分支管理）
│   ├── bim_source/
│   ├── frs_source/
│   └── papers/
├── subjects/                                # git worktree 根目录
│   ├── {subject_1}/                         # worktree (branch: experiment/{subject_1})
│   │   ├── input/                           # 输入资料副本（隔离）
│   │   ├── forest/                          # 该 subject 的实验输出
│   │   └── .experiment_metadata.yaml        # 实验元数据
│   ├── {subject_2}/                         # worktree (branch: experiment/{subject_2})
│   └── {subject_3}/                         # worktree (branch: experiment/{subject_3})
├── reviews/                                 # 评审报告（主分支管理）
│   └── {reviewer}_{subject}.md
├── .experiment_metadata_template.yaml
└── README.md
```

**隔离规则**（强制）：
- 实验项目必须是独立 Git 仓库，与项目主森林（`docs/forest/`）完全分离
- 实验森林不得引用主森林的任何叶子（避免交叉声明误报）
- 输入资料必须锁定版本（脚本复制到各 worktree 的 `input/`，不从主森林读取）
- **每个 subject 在独立 git worktree 中执行**——worktree 间物理隔离，互不可见，无需额外 ignore 配置
- **支持并行实验**：不同 worktree 可在不同终端 + 不同会话中同时执行

填写各 worktree 的 `.experiment_metadata.yaml` 的环境声明部分（`environment` 字段）。

---

## Step 2：资料准备

根据维度进入对应分支：

### 维度1（不同模型）/ 维度2（不同工具）

固定资料 = 3 份：
- `input/bim_source/`：人脑记忆机制的数据结构与算法分析（bim 森林源文档）
- `input/frs_source/`：AI 与大模型前沿研究综述（frs 森林源文档）
- `input/papers/2404.13501.pdf`：A Survey on the Memory Mechanism of Large Language Model based Agents

> 这 3 份资料已有审计基线（bim 35 篇引用 + frs 54 篇引用），可直接对比。

### 维度3（不同资料）

被测资料由用户在 Step 0 提供。LLM 应验证每份资料满足：
- 有明确版本或 arXiv ID
- 不是已有森林的子集（避免污染）
- 引用密度足以测试 D1/D2

---

## Step 3：抽取阶段

对每个被测对象执行 `forest-generation-methodology` 的 **Step 2-3**（LLM 知识抽取）。

### 会话隔离与防抄袭（强制）

**核心原则**：每个 subject 必须在全新会话中独立抽取，且工作区中不得存在其他 subject 的实验产物。

| 要求 | 说明 | 违反后果 |
|------|------|---------|
| 新会话 | 每个 subject 必须在全新会话中执行，上下文干净清洁 | 实验数据作废 |
| 上下文清空 | 不得继承之前会话的抽取结果、修正记录、评审数据 | 实验数据作废 |
| 工作区隔离 | 当前 subject 工作区中不得存在其他 subject 的 forest/ 输出 | 实验数据作废 |
| 禁止抄袭 | 新会话+新模型不得直接复制/参考其他模型的实验产物 | 实验数据作废，标记为作弊 |

**为什么需要物理隔离**：

防抄袭不能依赖"禁止读取"的口头约束——模型可能读取工作区中存在的任何文件。若 exp-001 的 `forest/` 输出仍在工作区中，启动 exp-002 的新会话时，模型可能：
- 读取 exp-001 的输出并"参考"其结构 → 抽取质量虚高
- 直接复制 exp-001 的知识原子 → 完全抄袭
- 受 exp-001 的组织方式影响 → 失去独立性

最可靠的机制是**物理隔离**：当前 subject 工作时，工作区中不存在其他 subject 的产物。本项目通过 **git worktree** 实现物理隔离——每个 subject 在独立 worktree 中执行，worktree 间互不可见。

### 执行流程

```
for subject in subjects:
    1. 【开启新会话】确保上下文干净清洁（不得继承之前会话的任何上下文）
    2. 【进入 worktree】cd subjects/{subject}/
       - worktree 是独立物理目录，天然看不到其他 subject 的产物
       - 确认 forest/ 目录为空（worktree 初始化时已创建）
    3. 切换到该被测对象的执行环境
       - 维度1：切换 LLM 模型
       - 维度2：切换 AI 编程工具
       - 维度3：切换输入资料
    4. 对每份输入资料执行抽取（复用 9 步 SOP Step 2-3）
    5. 输出到 forest/
    6. 记录抽取元数据（token 消耗、耗时、人工修正次数）
    7. 【自评质量门禁】执行 9 步 SOP Step 6-7（索引生成 + 迭代修正）：
       a. 生成 index.md（森林级 + 树级）
       b. 执行技术检查清单（不涉及内容质量）：
          - 空文件检测（0 字节 .md）
          - YAML frontmatter 完整性（title/version/created/updated/refs）
          - index.md 存在性（森林级 + 树级）
          - 文件命名规范（无特殊字符、无空格）
          - 跨树引用格式检查（仅检查已有引用的格式，不检查是否应该有跨树引用）
       c. 发现技术错误 → 修复 → 记录修正日志（见下方"自评质量门禁"说明）
       d. 无技术错误 → 通过门禁
    8. 【提交产出】git add -A && git commit -m "experiment: {subject} extraction complete"

并行模式（推荐）：为每个 subject 打开独立终端 + 独立会话，同时执行步骤 1-8。
```

### 抽取要求（与正式生成一致）

- 必须输出带 YAML frontmatter 的知识原子文档
- 必须执行交叉声明检测（每个 subject 内部）
- 不得引用主森林（隔离原则）

### 自评质量门禁（Step 7 详解）

**目的**：在抽取后、交叉评审前，排除技术错误（空文件、格式问题）对评审公平性的影响。

**背景**：首轮对照实验中 DSV4 Pro 出现 2 个空文件（0 字节），到交叉评审时才发现，导致评分偏低。空文件是技术错误（如 API 超时、文件写入失败），不代表模型能力差异。自评质量门禁确保技术错误在提交前被修复。

**自评 vs 交叉评审的边界**：

| 维度 | 自评（Step 7 门禁） | 交叉评审（Step 4） |
|------|---------------------|-------------------|
| 执行者 | 抽取者自己 | 其他模型 |
| 检查范围 | 技术性检查（空文件/格式/YAML） | 5 维度内容质量评分 |
| 可否修复 | 可修复技术错误 | 不可修复，只评分 |
| 记录 | 修正日志 | 评审报告（5 维度评分） |
| 目的 | 质量门禁——排除技术噪音 | 对照比较——评估内容质量 |

**为什么自评不使用 forest-quality-reviewer 的 5 维度评分**：

1. **自评偏差**——抽取者评自己的 D4 批判性分析会有美化倾向
2. **预知弱点**——若自评发现 D4 低，抽取者可能"补写"批判性内容，影响交叉评审公平性
3. **角色冲突**——抽取者同时是"运动员"和"裁判"，降低评审可信度

**自评只做技术门禁，不做内容评分**——这是公平性的关键保障。

**修正日志要求**（强制）：

修复技术错误后，必须在 commit message 中记录修复内容：

```
experiment: dsv4pro extraction complete

fix: 2 empty files detected and regenerated
  - graphrag-multi-hop-reasoning.md (was 0 bytes, regenerated)
  - sparse-coding-pattern-separation.md (was 0 bytes, regenerated)
```

交叉评审者在 Step 4 可查看修正日志，了解哪些文件被技术性修复。这保证实验的透明性和可追溯性。

**技术检查清单细则**：

| 检查项 | 判定标准 | 修复方式 |
|--------|---------|---------|
| 空文件 | 文件大小 = 0 字节 | 重新抽取该知识原子 |
| YAML 缺失 | frontmatter 缺少必填字段 | 补充缺失字段 |
| index.md 缺失 | 森林级或树级 index.md 不存在 | 按 forest_index_template 生成 |
| 命名不规范 | 文件名含空格或特殊字符 | 重命名（kebab-case） |
| 跨树引用格式 | 三级判定（见下方说明） | 修复格式错误的跨树引用 |

**跨树引用格式三级判定**：

| 情况 | 判定 | 处理 |
|------|------|------|
| 有跨树引用，格式正确（`[forest_id] 文档名 \| 原因`） | ✅ 通过 | — |
| 有跨树引用，格式错误（缺少 `[forest_id]` 前缀） | ❌ 技术错误 | 自评门禁修复格式 |
| 无跨树引用（refs 仅用于文献引用） | ➖ 不适用 | 记录数量，供交叉评审参考 |

> **关键原则**：自评门禁只检查已有跨树引用的格式是否正确，不检查是否应该有跨树引用。后者是内容质量问题，属于交叉评审 D3/D5 的评分范围。

---

## Step 3b：合并 worktree 结果

各 subject 的抽取在独立 worktree 中完成后，需要将结果合并到主分支，便于后续评审和汇总。

### 执行方式

```bash
bash .codebuddy/skills/forest-generation-methodology/assets/merge_experiment.sh
```

合并脚本自动完成：
1. 切换到主分支
2. 发现所有 `experiment/*` 分支
3. 更新 `.gitignore`（允许追踪元数据文件）
4. 将各 worktree 的 `forest/`、`input/`、`.experiment_metadata.yaml` 添加到主分支
5. 提交合并
6. 生成 `results/comparison-matrix-models.md` 和 `REPORT.md` 模板

### 合并后的目录结构

```
{experiment_repo}/
├── input/                           # 共享输入资料
├── subjects/
│   ├── {subject_1}/
│   │   ├── forest/                  # 已合并的实验产出
│   │   ├── input/                   # 输入资料副本
│   │   └── .experiment_metadata.yaml
│   ├── {subject_2}/
│   └── {subject_3}/
├── reviews/                         # 评审报告（待填写）
├── results/                         # 对照矩阵和汇总结果
│   └── comparison-matrix-models.md
├── REPORT.md                        # 实验总结报告
├── .experiment_metadata_template.yaml
└── README.md
```

> 合并完成后，各 subject 的 `forest/` 内容在主分支可见，评审者可直接读取。

---

## Step 4：评审阶段（交叉评审矩阵）

按交叉评审矩阵调度评审者。**评审者不能评审自己的输出**。

### 矩阵构造

对于 N 个被测对象（互为评审者），构造 N×(N-1) 组评审：

```
被测对象          评审者
                subject_1   subject_2   ...   subject_N
subject_1        ✗ 跳过       ✓           ...   ✓
subject_2        ✓           ✗ 跳过      ...   ✓
...              ...         ...         ...   ...
subject_N        ✓           ✓           ...   ✗ 跳过
```

### 评审执行

对每个有效评审单元（subject_i 被 subject_j 评审）：

1. 评审者调用 `forest-quality-reviewer` skill
2. 评审者读取 `forest/{subject_i}/` 的输出
3. 评审者按 5 维度评分（D1 引用真实性 / D2 引用准确性 / D3 层级组织 / D4 批判性分析 / D5 学术规范）
4. 评审者声明自身能力等级（AAI 分数）
5. 输出到 `reviews/{subject_j}_{subject_i}.md`

### 评审者偏差声明（强制）

每份评审报告必须在 frontmatter 声明：
- `reviewer_model`: 评审者模型
- `reviewer_aai`: 评审者 AAI 分数
- `reviewee_model`: 被评审对象
- `reviewee_aai`: 被评审对象 AAI 分数
- `bias_risk`: 偏差风险评估（低/中/高）

---

## Step 5：数据归集

### 5.1 填写评审结果

将所有评审数据填入 `.experiment_metadata.yaml` 的 `results` 字段：

```yaml
results:
  - experiment_id: exp-001
    subject: {subject_1}
    reviewer: {subject_2}
    d1_citation_authenticity: 9/10
    d2_citation_accuracy: 7/10
    d3_hierarchy: 8/10
    d4_critical_analysis: 4/10
    d5_academic_norm: 5/10
    overall: 6.5/10
    human_correction_rate: 0.14
    tokens_consumed: 125000
    duration_minutes: 45
  - experiment_id: exp-002
    # ...
```

### 5.2 生成对照数据表格

按实验维度生成对照表格（参见 `SKILL.md` 中的表格模板）：
- 维度1：模型对照表
- 维度2：工具对照表
- 维度3：资料对照表

### 5.3 计算统计量

- 各维度的均值与标准差
- 被测对象间的差异显著性（样本量足够时）
- 评审者间的一致性（inter-rater agreement）

---

## Step 6：实验报告输出

生成 `REPORT.md`，包含：

1. **实验概述**：维度、被测对象、固定变量、实验环境
2. **对照数据表格**：5 维度评分 + 综合分 + 修正率
3. **关键发现**：
   - 是否验证了预期假设（如 AAI 门槛效应）
   - 异常数据点的解释
   - 评审者偏差的影响评估
4. **与历史数据对比**：
   - 维度1：与 DSV4 评审基线（exp-002, 44 分模型）对比
   - 维度2/3：与维度1 数据对比
5. **结论与局限**：
   - 可推广的结论
   - 样本量局限
   - 待补充的实验（如顶级模型数据）

---

## 附录：与 9 步 SOP 的对应关系

| 本 SOP 步骤 | 对应 9 步 SOP 步骤 | 说明 |
|------------|------------------|------|
| Step 0 启动协议 | （新增） | 实验场景特有 |
| Step 1 环境隔离 | Step 1 输入策展 | 实验版增加隔离要求 |
| Step 2 资料准备 | Step 1 输入策展 | 实验版固定资料版本 |
| Step 3 抽取阶段 | Step 2-3 LLM 抽取 + Step 6-7 索引生成+迭代修正 | 复用 + 增加自评质量门禁（技术检查，不含内容评分） |
| Step 4 评审阶段 | Step 4-7 评审+修正 | 实验版改为交叉评审 |
| Step 5 数据归集 | Step 8 元数据 | 实验版扩展元数据 |
| Step 6 报告输出 | Step 9 索引生成 | 实验版改为报告生成 |

**不重复的内容**：9 步 SOP 中的"主题设计规则""交叉声明检测算法""引用真实性审计流程"等在实验中完全适用，本文档不重复定义。

---

## 附录：常见问题

**Q1：用户在 Step 0 未指定固定模型/工具怎么办？**
A：LLM 必须再次询问，不得假设。若用户明确表示"使用当前默认值"，则记录默认值并继续。

**Q2：被测对象只有 1 个怎么办？**
A：对照实验至少需要 2 个被测对象才能产生对照数据。LLM 应提示用户补充。

**Q3：评审者能力远低于被评审对象怎么办？**
A：在评审报告中标注 `bias_risk: 高`，并在 REPORT.md 中说明该组评审数据的可信度限制。低能力评审者可能"评不出"高能力输出的差距。

**Q4：实验过程中主森林更新了怎么办？**
A：实验森林与主森林隔离，主森林更新不影响进行中的实验。但实验报告中应记录实验期间主森林的版本快照。

**Q5：社区贡献者提交的实验数据如何验证？**
A：贡献者须提交完整的 `.experiment_metadata.yaml` + `forest/` + `reviews/` 目录。维护者按本 SOP 检查：环境声明完整性、交叉评审矩阵正确性、隔离原则遵守情况。
