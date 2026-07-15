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

按 [`experiment_project_template.md`](experiment_project_template.md) 创建独立实验目录：

```
{workspace}/experiments/{project_name}/
├── .experiment_metadata.yaml    # 实验元数据（按 experiment_metadata_template.yaml）
├── input/                       # 输入资料（锁定版本）
│   ├── bim_source/
│   ├── frs_source/
│   └── papers/                  # arXiv 论文 PDF
├── forest/                     # 实验生成的森林（按被测对象分子目录）
│   ├── {subject_1}/
│   ├── {subject_2}/
│   └── {subject_3}/
├── reviews/                    # 评审报告（按 评审者_被评审对象 命名）
│   ├── {reviewer}_{subject}.md
└── REPORT.md                   # 实验总结报告
```

**隔离规则**（强制）：
- 实验目录必须与项目主森林（`docs/forest/`）完全分离
- 实验森林不得引用主森林的任何叶子（避免交叉声明误报）
- 输入资料必须锁定版本（复制到 `input/` 目录，不从主森林读取）

填写 `.experiment_metadata.yaml` 的环境声明部分（`environment` 字段）。

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

对每个被测对象执行 `forest-generation-methodology` 的 **Step 2-3**（LLM 知识抽取）：

```
for subject in subjects:
    1. 切换到该被测对象的执行环境（维度1=切换模型，维度2=切换工具，维度3=切换资料）
    2. 对每份输入资料执行抽取
    3. 输出到 forest/{subject}/
    4. 记录抽取元数据（token 消耗、耗时、人工修正次数）
```

**抽取要求**（与正式生成一致）：
- 必须输出带 YAML frontmatter 的知识原子文档
- 必须执行交叉声明检测（每个 subject 内部）
- 不得引用主森林（隔离原则）

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
| Step 3 抽取阶段 | Step 2-3 LLM 抽取 | 完全复用 |
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
