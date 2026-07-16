# 交接文档：P1 / P2 后续工作

> **实验**: exp-model-20260716-01（维度1：不同模型对照）
> **交接日期**: 2026-07-16
> **交接人**: GLM-5.2 (AAI 51) 会话
> **实验状态**: P0（结果合并）已完成，P1（4 项）已完成，P2 待执行
> **关联文档**: `REPORT.md`（实验报告）、`results/comparison-matrix-models.md`（对照矩阵）

---

## 0. 当前实验状态快照

### 0.1 最终评分（重评轮双评审均值）

| 排名 | 模型 | AAI | D1 | D2 | D3 | D4 | D5 | 综合 | 修正率 |
|:---:|------|:---:|:--:|:--:|:--:|:--:|:--:|:----:|:-----:|
| 1 | GLM-5.2 | 51 | 9.0 | 8.5 | 9.0 | 7.5 | 8.5 | **8.5** | <7% |
| 2 | DeepSeek V4 Pro | 44 | 9.0 | 7.0 | 9.0 | 6.0 | 7.0 | **7.6** | ~10% |
| 3 | DeepSeek V4 Flash | 40 | 8.0 | 6.0 | 7.0 | 3.0 | 6.0 | **6.0** | ~20% |

### 0.2 已完成的工作

| 阶段 | 产出 | 状态 |
|------|------|:---:|
| 森林生成 | 3 个森林（dsv4flash/dsv4pro/glm52），共 72 个叶子 | ✅ |
| 首轮交叉评审（R1） | 9 份评审报告 | ✅ |
| dsv4pro 空文件修复 | 2 个空文件重新生成 | ✅ |
| 自评质量门禁（Step 3） | 3 个森林均执行 | ✅ |
| 重评轮（R2/v2/v3） | 6 份重评报告 | ✅ |
| **P0 结果合并** | REPORT.md + comparison-matrix-models.md + README.md 更新 | ✅ |
| **P1-1 仲裁** | reviews/arbitration-glm52-d2d4d5.md | ✅ |
| **P1-2 方法论反馈** | 3 个 SKILL.md/SOP 编辑（技术门禁边界+D2/D5归属+D4抽样+评分项纪律） | ✅ |
| **P1-3 引用验证** | results/p1-3-citation-verification.md（26 篇确认，0 虚构） | ✅ |
| **P1-4 交叉声明检测** | results/p1-4-cross-declaration-detection.md + scripts/cross_declaration_detect.py | ✅ |

### 0.3 关键文件索引

| 类别 | 路径 |
|------|------|
| 实验报告 | `REPORT.md` |
| 对照矩阵 | `results/comparison-matrix-models.md` |
| 评审报告（15份） | `reviews/review-*.md` |
| dsv4flash 森林 | `subjects/dsv4flash/forest/`（31 .md，含 correction-log.md） |
| dsv4pro 森林 | `subjects/dsv4pro/forest/`（25 .md）+ `quality-gate-self-assessment.md` |
| glm52 森林 | `subjects/glm52/forest/`（29 .md） |
| 生成方法论 skill | `.codebuddy/skills/forest-generation-methodology/SKILL.md` |
| 评审方法论 skill | `.codebuddy/skills/forest-quality-reviewer/SKILL.md` |
| 输入资料（共享） | `input/bim_source/` + `input/frs_source/` + `input/papers/2404.13501.md` |

---

## 1. P1 任务清单（4 项，建议优先执行）

### P1-1：glm52 评审者分歧仲裁 ✅ 已完成

> **完成日期**: 2026-07-16
> **产出**: `reviews/arbitration-glm52-d2d4d5.md`
> **结论**: 维持均值（D2=8.5/D4=7.5/D5=8.5，综合 8.5 不变）。根因为方法论分类差异+抽样代表性差异，**非纯能力偏差**。不引入第三评审者。"AAI差≥10→三评审者"规则**不写入** skill，改为更精准的 D4 分层抽样要求+评分项不得自定义。

**背景**：重评轮中 glm52（AAI 51）的两个评审者在 D2/D4/D5 出现 1 分分歧，是本轮信度下降（78%）的主因。

| 维度 | dsv4flash(40) 评分 | dsv4pro(44) 评分 | 偏差方向 |
|------|:---:|:---:|------|
| D2 引用准确性 | 8 | 9 | 弱评者偏严 |
| D4 批判性分析 | 8 | 7 | 弱评者偏高（主观维度高估） |
| D5 学术规范 | 8 | 9 | 弱评者偏严 |

**偏差模式**：dsv4flash（AAI 40）评 glm52（AAI 51，差 -11）时，主观维度（D4）高估、客观维度（D2/D5）偏严。这是"弱评强"场景的典型偏差方向分化。

**待决事项**：
1. 是否需要引入**第三评审者**对 glm52 仲裁？候选：dsv4pro 自评（已有 `review-dsv4pro-by-dsv4pro-re-review.md` 先例，但偏差风险高）
2. 或者接受均值（D2=8.5, D4=7.5, D5=8.5）作为最终值，在报告中标注分歧？
3. 是否将"AAI 差≥10 的评审配对采用三评审者机制"写入 forest-quality-reviewer skill？

**执行建议**：
- 阅读 `reviews/review-glm52-by-dsv4flash.md` 和 `reviews/review-glm52-by-dsv4pro-r2.md` 的 D2/D4/D5 论证细节
- 对比两评审者的抽样范围（dsv4flash 40% vs dsv4pro 40%，但抽样叶子可能不同）
- 若分歧源于抽样差异而非能力偏差，补充全量阅读可消除分歧；若源于能力偏差，需第三评审者

**关联文件**：
- `reviews/review-glm52-by-dsv4flash.md`（D2=8, D4=8, D5=8, 综合=8.4）
- `reviews/review-glm52-by-dsv4pro-r2.md`（D2=9, D4=7, D5=9, 综合=8.6）
- `REPORT.md` 第 4.5 节（发现五：评审者间信度的两轮分化）

---

### P1-2：自评质量门禁作用域发现反馈到方法论 ✅ 已完成

> **完成日期**: 2026-07-16
> **产出**:
> - `forest-generation-methodology/SKILL.md` Step 7 补充：能力边界实证表 + 技术门禁vs内容评审职责边界 + PoG 案例 + 步骤映射澄清
> - `forest-generation-methodology/assets/experiment_execution_sop.md`：自评质量门禁部分加入实验实证
> - `forest-quality-reviewer/SKILL.md`：D2/D5 引用问题归属边界 + D4 抽样代表性要求 + 评分项不得自定义纪律
> **步骤映射已理清**：实验 SOP "Step 3 自评质量门禁" = 生成 SOP 的 Step 6-7（索引+迭代修正），≠ 生成 SOP 的 Step 3（交叉声明检测）。

**背景**：三个森林执行自评质量门禁（Step 3）后重评，发现一个重要的方法论边界——自评门禁作为"技术检查（非内容评分）"，其作用域**严格限于 D5 的 frontmatter 完整性**，D1-D4 内容维度完全不变。

**实验证据**：

| 森林 | 自评修复 | D5 变化 | D1-D4 变化 |
|------|---------|:---:|:---:|
| dsv4flash | 补 updated 字段 + index sources | 5→6 (+1) | 全部不变 |
| dsv4pro | 无（version/updated 推迟） | 0 | 全部不变 |
| glm52 | 补 version 字段 | 8→8.5 (+0.5) | 全部不变 |

**待决事项**：在 forest-generation-methodology 中明确区分"技术门禁"与"内容评审"的职责边界。

**执行建议**：
1. 阅读 `.codebuddy/skills/forest-generation-methodology/SKILL.md`，定位自评质量门禁相关步骤
2. 注意：实验中的"Step 3 自评质量门禁"对应的是"对照实验执行 SOP"的步骤编号，与 forest-generation-methodology SKILL.md 的 Step 3（交叉声明检测）**不同**——需先理清两个 SOP 的步骤映射关系
3. 在方法论中补充说明：
   - 自评质量门禁的**能力边界**：仅覆盖技术格式（空文件/YAML 完整性/命名规范/refs 格式），不评估内容质量
   - 内容质量（引用准确性/批判性分析/跨树引用语义）需由**交叉评审**（forest-quality-reviewer）覆盖
   - dsv4flash 的 PoG 方法名错误（"Path-of-Graph"应为"Paths-over-Graph"）是典型案例——技术门禁未捕获，交叉评审 D2 才发现

**关联文件**：
- `.codebuddy/skills/forest-generation-methodology/SKILL.md`
- `subjects/dsv4flash/forest/correction-log.md`（dsv4flash 自评修复记录）
- `subjects/dsv4pro/quality-gate-self-assessment.md`（dsv4pro 自评门禁报告）
- `REPORT.md` 第 4.3 节（发现三：自评质量门禁的作用域边界）

---

### P1-3：全量 arxiv-mcp-server 引用验证 ✅ 已完成

> **完成日期**: 2026-07-16
> **产出**: `results/p1-3-citation-verification.md`
> **结论**: 26 篇引用确认真实 + 10 篇传统期刊 web 确认 + 2 篇待补充（PRUNE/STABLE，非虚构）= **0 篇虚构引用**。D1 置信度统一提升至 High。Wu et al. (2402.01364) 引用语境偏差经 arXiv 验证确认——dsv4pro 偏差、glm52 准确，证实 D2 评分差异合理。

**背景**：当前 D1（引用真实性）置信度不统一——glm52 重评使用了 arxiv-mcp-server 验证 3 篇核心论文（置信度 High），dsv4flash 重评也验证了 3 篇，但 dsv4pro 和部分引用仍依赖 web 搜索/来源材料交叉验证（置信度 Medium-High）。

**待决事项**：对三个森林的全部引用使用 arxiv-mcp-server 逐条验证，将 D1 置信度统一提升到 High。

**执行建议**：
1. 遍历每个森林的全部叶子 YAML `refs` 字段，提取所有引用
2. 对有 arXiv ID 的引用，用 `arxiv-mcp-server` 的 `search_papers` 或 `download_paper` 验证
3. 对有 DOI 的引用，用 web 搜索验证
4. 对仅"作者+年份"的引用，补充 arXiv ID/DOI 或标注"传统期刊，web 确认"
5. 已验证的关键引用（无需重复）：
   - PoG: arXiv:2410.14211（Paths-over-Graph, Tan et al.）✅
   - Gershman KV: arXiv:2501.02950v2（Key-value memory in the brain）✅
   - Edge GraphRAG: arXiv:2404.16130v2 ✅

**预期产出**：三个森林各一份引用验证清单，D1 置信度统一标注 High。

**关联文件**：
- `reviews/review-dsv4flash-by-glm52-v2.md`（Step 1 已有 arxiv-mcp 验证范例）
- 各森林叶子的 YAML `refs` 字段

---

### P1-4：sentence-transformers 量化交叉声明检测 ✅ 已完成

> **完成日期**: 2026-07-16
> **产出**: `results/p1-4-cross-declaration-detection.md` + 脚本 `scripts/cross_declaration_detect.py`
> **结论**: 三个森林**均无 >0.85 交叉声明对**。dsv4flash 最大相似度 0.845（2 对需审查）、dsv4pro 0.815（3 对）、glm52 0.836（1 对）。所有 0.80-0.85 对经审查均为**互补关系**（评估方法配对/理论-实现配对），非交叉声明。交接文档标注的 dsv4flash "l1-pattern-completion 与 l2-associative-memory 高度重叠"**未被量化确认**（该对未进 Top5，<0.80）——为结构归属问题非语义重叠。D3 评分维持不变。

**背景**：D3（层级组织）的"Leaf 单一职责"评估目前基于人工判断，未运行量化检测。skill 中提供了 sentence-transformers 检测方法（`paraphrase-multilingual-MiniLM-L12-v2` 模型，阈值 0.80）。

**已知交叉声明风险点**（人工判断，待量化确认）：
- **dsv4flash**: `l1-pattern-completion`（b3-retrieval）与 `l2-associative-memory`（b3-retrieval）高度语义重叠——都讨论 CAM/键值记忆/CA3；且 `l1-pattern-completion` 标题含"模式分离"但模式分离属 b2 编码领域（越界）
- dsv4pro 和 glm52 的人工判断未发现高相似度对，但需量化确认

**执行建议**：
1. 安装 sentence-transformers：`pip install sentence-transformers`
2. 对每个森林的全部叶子，提取 `description` + `keywords`（或 title + 正文首段）做嵌入
3. 计算余弦相似度矩阵，统计 > 0.80 的对数
4. skill 基线参考（`.codebuddy/skills/forest-quality-reviewer/SKILL.md` Step 3）：
   - > 0.85：无直接交叉声明（优秀）
   - 0.80-0.85：可能是 index 关系或语义重叠（需审查）
   - < 0.70：独立主题（正常）
5. 产出每个森林的相似度矩阵 + 高相似度对清单

**预期产出**：三个森林各一份交叉声明量化检测报告，D3 单一职责评估从主观转为客观。

**关联文件**：
- `.codebuddy/skills/forest-quality-reviewer/SKILL.md`（Step 3 交叉声明检测方法 + 基线数据）
- `.codebuddy/skills/forest-quality-reviewer/scripts/`（可能有现成脚本）

---

## 2. P2 任务清单（3 项，可延后）

### P2-1：实验归档（git 提交） ✅ 已完成

> **完成日期**: 2026-07-16
> **commit**: `ed2b6c5` — 15 files changed, +2431/-203
> **范围**: P0 结果合并 + P1 全部 4 项任务产出
> **工作树状态**: clean

**背景**：当前工作树有未提交的变更（REPORT.md、comparison-matrix-models.md、README.md 更新 + 6 份重评报告）。

**待决事项**：将所有变更 git 提交，标记实验完成。

**执行建议**：
```bash
cd d:/projects/fm-mke-expirements-001
git add -A
git status  # 确认变更范围
git commit -m "experiment: exp-model-20260716-01 重评轮完成，结果合并

- 新增 6 份重评报告（R2/v2/v3）
- 更新 REPORT.md：重评轮最终数据 6.0/7.6/8.5
- 更新 comparison-matrix-models.md：两轮评审数据 + 自评门禁记录
- 更新 README.md：交叉评审矩阵标注两轮

最终评分：glm52 8.5 > dsv4pro 7.6 > dsv4flash 6.0"
```

**注意事项**：
- 提交前确认 `.experiment_metadata.yaml` 各 subject 的 reviews 段是否需要更新（dsv4pro 已有部分重评记录）
- 确认无敏感信息泄露

---

### P2-2：扩展到不同主题的森林（验证主题无关性）

**背景**：本实验三个模型均生成同一主题（memory-systems-ai），可能存在主题特异性。需验证能力-质量映射关系是否主题无关。

**执行建议**：
1. 选择 1-2 个不同主题（如：软件架构、区块链、生物信息学）
2. 使用相同的固定变量（CodeBuddy v4.10.2 / 相同方法论 / 相同评审方法）
3. 至少用 2 个模型（如 dsv4flash + glm52）生成新主题森林
4. 运行 forest-quality-reviewer 评审
5. 对比同模型在不同主题上的评分稳定性

**预期产出**：新主题森林 + 评审报告 + 主题无关性分析。

---

### P2-3：增加维度2（不同工具）和维度3（不同资料）实验

**背景**：本实验仅验证了维度1（不同模型）。forest-generation-methodology 设计了多维度对照：
- 维度1（已完成）：不同模型 × 固定工具 × 固定资料
- 维度2（待做）：固定模型 × **不同工具** × 固定资料
- 维度3（待做）：固定模型 × 固定工具 × **不同资料**

**执行建议**：
- **维度2**：选 1 个模型（如 glm52），换用不同工具（如 Cursor / Cline / 手动 CLI），生成同主题森林，对比工具对质量的影响
- **维度3**：选 1 个模型，换用不同输入资料（不同领域/不同质量），生成森林，对比资料对质量的影响

**预期产出**：维度2/维度3 实验报告，验证方法论的普适性。

---

## 3. 关键发现摘要（交接必读）

接手 agent 必须了解以下 7 个核心发现，避免重复劳动：

1. **AAI-质量正相关**：6.0→7.6→8.5，每 +1 AAI ≈ +0.22 综合分
2. **D4 是区分度最高维度**：3→6→7.5，呈"双阶梯"增长（40→44 +3，44→55 平台期，>55 预期第二阶梯）
3. **D1/D3 门槛效应**：AAI 40 即达 D1=8，AAI 44 即达 D1=9/D3=9，之后不再提升
4. **自评质量门禁作用域有限**：三个森林均印证"技术检查仅影响 D5，D1-D4 内容维度不变"——**这是对方法论的重要反馈**
5. **工程修复 ≠ 能力提升**：dsv4pro 首轮修复空文件 +0.8 分来自工程缺陷而非能力
6. **评审者信度两轮分化**：首轮 91.7% → 重评轮 78%，glm52 的"弱评强"偏差方向分化（D4 高估、D2/D5 偏严）
7. **GLM-5.2 全面领先**：5 维度全面领先，D4=7.5 接近深度批判门槛

---

## 4. 注意事项与诚实声明

1. **dsv4pro 修复溯源未确认**：2 个修复文件（sparse-coding / graphrag）的内容来源未能确认是 dsv4pro 重新生成还是人工补充——若为后者，D4 评分应审慎解读
2. **glm52 评审者分歧未仲裁**：D2/D4/D5 各差 1 分，当前均值为最终值，但存在不确定性
3. **dsv4pro version/updated 仍缺失**：自评门禁识别但推迟修复，影响 D5 上限
4. **抽样评审局限**：dsv4flash 重评 46%、dsv4pro 100%、glm52 40% 覆盖率，未全量覆盖的森林可能存在未发现问题
5. **同族模型偏差**：dsv4flash 和 dsv4pro 来自同一模型家族，互评时偏差风险中等
6. **P1-2 的步骤映射需理清**：实验中"Step 3 自评质量门禁"对应"对照实验执行 SOP"的编号，与 forest-generation-methodology SKILL.md 的 Step 3（交叉声明检测）不同——反馈到方法论前需先理清两个 SOP 的关系

---

## 5. 快速启动指南

接手 agent 的推荐启动顺序：

```
1. 阅读 REPORT.md（全文）— 掌握实验全貌和最终结论
2. 阅读 results/comparison-matrix-models.md — 掌握详细评分数据
3. 阅读本交接文档第 1-2 节 — 确定 P1/P2 执行优先级
4. 从 P1-1（glm52 分歧仲裁）开始 — 这是影响数据确定性的最紧迫项
5. 若需修改方法论，先执行 P1-2（步骤映射理清 + 边界反馈）
6. P1-3/P1-4 可并行 — 引用验证和交叉声明检测互相独立
7. P2-1（git 提交）在所有 P1 完成后执行
8. P2-2/P2-3 为后续实验规划，可延后
```

**技能加载**：执行评审相关任务时加载 `forest-quality-reviewer` skill；执行生成/方法论修改时加载 `forest-generation-methodology` skill。
