---
name: forest-quality-reviewer
description: 知识森林质量评审方法论——基于 5 维度评审体系（引用真实性/引用准确性/层级组织/批判性分析/学术规范），集成 Artificial Analysis Intelligence Index 能力映射，支持标准化评分、对照实验和模型能力-质量校准。与 forest-generation-methodology 正交配合，形成"生成-评审"闭环。
metadata: {"version": "1.0.0", "created": "2026-07-15", "updated": "2026-07-15", "author": "Forest Memory Project"}
---

# 知识森林质量评审方法论（Forest Quality Reviewer）

## 定位

本 Skill 是**标准化的知识森林质量评估方法论**。

它与 `forest-generation-methodology` 形成正交配合关系：

```
┌──────────────────────────┐      ┌──────────────────────────┐
│ forest-generation-      │      │ forest-quality-reviewer   │
│ methodology              │ ──→ │                          │
│ (生成)                   │ 输出物 │ (评审)                    │
│                          │      │                          │
│ 输入: 原始资料 + 模型     │      │ 输入: 已生成的知识森林      │
│ 输出: 层级化知识森林       │      │ 输出: 5维度评分 + 改进建议  │
└──────────────────────────┘      └──────────────────────────┘
                                          │
                                          ▼
                              ┌──────────────────────────┐
                              │   对照实验平台              │
                              │  同资料 × 不同模型          │
                              │  × 相同评审方法             │
                              │  → 可复现量化对照数据        │
                              └──────────────────────────┘
```

## 适用场景

| 场景 | 触发方式 |
|------|---------|
| 评审单个知识森林的质量 | 加载此 skill 并指向森林目录 |
| 模型对照实验中的统一评分 | 为 forest-generation-methodology 的每次输出运行此 skill |
| 校准"大模型能力-知识质量"映射 | 收集多个模型的评审数据，拟合能力-质量曲线 |
| 迭代改进知识抽取 Prompt | 利用评审发现的系统性弱点调整抽取策略 |

## 核心工作流：6 步评审 SOP

```
Step 0   评审准备              → 确认评审对象、获取元数据、确定评审者
Step 1   维度一：引用真实性      → 逐条验证引用是否存在（非虚构）
Step 2   维度二：引用准确性      → 验证引用的元数据和语境是否正确
Step 3   维度三：层级组织质量    → 评估森林结构和单一职责执行
Step 4   维度四：内容深度与批判性分析 → 评估内容的深度和客观性
Step 5   维度五：学术规范性      → 评估格式规范和方法论完整性
Step 6   Intelligence Index 映射 → 将 5 维度评分映射到模型能力空间
```

---

### Step 0：评审准备（Review Preparation）

**目标**：收集评审所需的所有上下文信息。

**必填信息收集**：

| 信息 | 来源 | 说明 |
|------|------|------|
| 森林目录路径 | 用户指定 | 如 `docs/forest/bim` |
| 森林元数据 | 目录下的 `.experiment_metadata.yaml` 或 index.md | 包含模型名称、Intelligence Index 等 |
| 生成该森林所用的模型名称 | experiment_metadata | 用于能力映射 |
| 该模型的 Intelligence Index 分数 | Artificial Analysis 官网或用户提供 | 能力校准的核心变量 |
| 评审者模型名称 | 当前会话模型 | 记录以评估评审者偏差 |
| 已有的审计报告（如有） | `archive/` 目录或森林内的审计文档 | 作为二次评审的依据 |

**评审者偏差声明**：

> 所有评审都受评审者自身能力水平的影响。必须在报告中声明评审者模型及其大致能力等级。例如："评审者：GLM-5.2，估计 Intelligence Index 约 50-55"。

**参考文档**：`references/report_template.md`

---

### Step 1：维度一——引用真实性（Citation Authenticity）

**目标**：验证森林中所有引用的文献/资料是否真实存在，无虚构。

**评分标准**：

| 评分 | 标准 | 含义 |
|------|------|------|
| 9-10 | 0 篇虚构引用，≥95% 已通过验证 | 优秀 |
| 7-8 | 0 篇虚构引用，80-94% 已验证 | 良好（未验证的多为传统期刊，合理） |
| 5-6 | 0-1 篇疑似虚构引用，70-79% 验证 | 及格但需注意 |
| 0-4 | ≥2 篇虚构引用或验证率 < 70% | 不合格 |

**审计方法**：

```python
# 伪代码：引用真实性审计流程
for citation in all_citations(forest):
    if citation.has_arxiv_id():
        result = arxiv_mcp_search(citation.arxiv_id)
        status = "CONFIRMED" if result.found else "NOT_FOUND"
    elif citation.has_doi():
        result = web_search(f"{citation.title} {citation.doi}")
        status = "CONFIRMED" if doi_resolves else "NEEDS_MANUAL_CHECK"
    else:
        result = web_search(f"{citation.authors} {citation.title}")
        status = "CONFIRMED" if found_elsewhere else "SUSPICIOUS"

    record(citation, status, verification_method)
```

**能力门槛发现**（基于 DeepSeek V4 Pro 实测）：

> Intelligence Index ~40 分的模型即可达到引用真实性 9/10（89 篇引用 0 虚构）。这表明**引用真实性存在能力门槛效应**——低于门槛会编造，达到门槛后不再线性提升。

**参考文档**：`references/review_dimensions.md`（维度一详述）

---

### Step 2：维度二——引用准确性（Citation Accuracy）

**目标**：验证引用的元数据（作者/年份/标题/期刊）和引用语境是否准确。

**检查项目**：

| 检查项 | 权重 | 常见错误 |
|--------|:---:|---------|
| 作者名单完整性 | 25% | 缺少作者列表 |
| 年份准确性 | 20% | 年份错误或使用了预印本而非正式版 |
| 标题准确性 | 20% | 标题与实际论文不一致 |
| 期刊/会议准确性 | 15% | 将书籍章节误标为期刊论文 |
| 引用语境恰当性 | 20% | 将文献归入不直接相关的方向 |

**评分标准**：

| 评分 | 问题率 | 含义 |
|------|--------|------|
| 9-10 | 0-5% | 优秀——几乎无需人工修正 |
| 7-8 | 6-12% | 良好——少量问题可快速修复 |
| 5-6 | 13-20% | 及格——需系统性审核修复 |
| 0-4 | >20% | 不合格——引用质量问题严重 |

**能力门槛发现**：

> Intelligence Index ~45 分模型可达 7/10（11% 问题率）。精确引用需要中等偏上的指令遵循能力。

**参考文档**：`references/review_dimensions.md`（维度二详述）

---

### Step 3：维度三——层级组织质量（Hierarchical Organization Quality）

**目标**：评估森林的 Forest → Tree → Branch → Leaf 结构是否逻辑清晰、单一职责执行良好。

**评估项目**：

| 评估项 | 权重 | 方法 |
|--------|:---:|------|
| Tree 划分合理性 | 25% | 专家判断：每棵 Tree 是否对应独立子领域 |
| Branch 覆盖完整性 | 20% | 每个 Tree 的 Branch 是否覆盖了该子领域的核心话题 |
| Leaf 单一职责执行 | 30% | 交叉声明检测（sentence-transformers 向量嵌入相似度） |
| 命名规范一致性 | 15% | 检查命名是否符合 `forest/tree/branch` 的层级约定 |
| refs 引用网络连通性 | 10% | 检查是否有孤立节点（无入边也无出边的 Leaf）|

**交叉声明检测方法**（量化 Leaf 单一职责执行）：

```python
# 使用 sentence-transformers 做向量嵌入
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
# 对所有 Leaf 的 description+keywords 做嵌入
vecs = model.encode(all_leaf_texts, convert_to_numpy=True)
# 计算余弦相似度矩阵
sims = normalize(vecs) @ normalize(vecs).T
# 统计超过阈值的对数
high_sim_pairs = np.where(sims > 0.80)
```

**基于 MKE 51 文档实测的基线数据**：

| 相似度范围 | 对数占比 | 判定 |
|-----------|---------|------|
| > 0.85 | 0% | 无直接交叉声明（优秀） |
| 0.80-0.85 | 0.3% | 可能是 index 关系或语义重叠（需审查） |
| < 0.70 | 82% | 独立主题（正常） |

**评分标准**：

| 评分 | 标准 | 含义 |
|------|------|------|
| 9-10 | 最高相似度 < 0.80，Tree 划分逻辑清晰 | 优秀 |
| 7-8 | 最高相似度 0.80-0.85，划分基本合理 | 良好 |
| 5-6 | 有少量明显交叉声明（0.85-0.90），需重组 | 一般 |
| 0-4 | 大量交叉声明（> 0.90），结构混乱 | 不合格 |

**能力门槛发现**：

> Intelligence Index ~40 分模型即可达到 8/10（优秀的层级组织）。**知识结构化组织的能力门槛较低**，可能在 ~40 分就达到瓶颈。

**参考文档**：`references/review_dimensions.md`（维度三详述）

---

### Step 4：维度四——内容深度与批判性分析（Critical Analysis Depth）

**目标**：评估知识原子的内容是否超越表面总结，包含批判性思考、横向对比和局限性讨论。

这是**区分中等能力和强能力的核心维度**。

**评估项目**：

| 评估项 | 权重 | 检查方法 |
|--------|:---:|---------|
| 论述深度（超越总结） | 30% | 是否仅有"方法简介+性能数据"，还是有深入分析 |
| 方法间横向对比 | 25% | 是否比较了不同方法的优劣、适用场景 |
| 局限性讨论 | 20% | 是否讨论了已知失败案例或方法局限性 |
| 张力与争议呈现 | 15% | 是否呈现了学术界的不一致观点 |
| 可操作的洞见 | 10% | 是否提供了超越文献摘要的新见解 |

**典型表现分级**：

| 表现 | 评分范围 | 示例 |
|------|---------|------|
| 仅做总结，无任何批判 | 0-4 | "方法 X 取得了 Y% 的准确率"（无更多） |
| 有简单对比但缺乏深度 | 5-6 | "方法 X 比 Y 好，因为 Z"（但无反面证据） |
| 有横向对比和部分局限讨论 | 7-8 | "X 在任务 A 上优于 Y，但在 B 上不足；X 的局限是..." |
| 深度批判性分析，呈现张力 | 9-10 | "X 与 Y 的整合仍是开放问题；Z 指出的反例表明..." |

**能力门槛发现**（基于 DeepSeek V4 Pro 实测）：

> Intelligence Index 44 分模型在此维度仅得 **4/10**——这是最明显的短板。推断 Intelligence Index **> 55 分**才可能达到 7/10 以上。**批判性分析与 Scientific Reasoning 维度高度正相关**。

**参考文档**：`references/review_dimensions.md`（维度四详述）

---

### Step 5：维度五——学术规范性（Academic Norm Compliance）

**目标**：评估森林的文档是否遵循学术写作规范（即使不是严格意义上的学术论文）。

**评估项目**：

| 评估项 | 权重 | 检查方法 |
|--------|:---:|---------|
| 方法论声明 | 25% | 是否说明了知识抽取/筛选/组织的具体方法 |
| 引用格式一致性 | 20% | 所有引用是否遵循统一的 YAML 格式 |
| 版本标识 | 15% | 文档是否都有 version/created/updated 字段 |
| 元数据完整性 | 20% | Frontmatter 是否包含 title/description/keywords/source/refs |
| 内部标签隔离 | 10% | 项目内部标签（如 [mke]）是否混入学术引用 |
| 图表与可视化 | 10% | 是否有必要的图表辅助理解 |

**评分标准**：

| 评分 | 标准 | 含义 |
|------|------|------|
| 9-10 | 完整遵循所有规范 | 优秀 |
| 7-8 | 小瑕疵（1-2 项不规范） | 良好 |
| 5-6 | 明显缺陷（3-4 项不规范） | 一般 |
| 0-4 | 系统性缺陷（>4 项不规范） | 不合格 |

**能力门槛发现**：

> Intelligence Index 44 分模型得 **5/10**——存在系统性缺陷。推断 **~55 分**以上才有显著改善。学术规范性与**指令遵循能力**高度相关。

**参考文档**：`references/review_dimensions.md`（维度五详述）

---

### Step 6：Intelligence Index 能力映射（Capability-Quality Mapping）

**目标**：将 5 维度评分映射到 Artificial Analysis Intelligence Index 的能力空间，建立"模型能力 → 知识质量"的定量关系。

#### 6.1 映射方法论

本步骤的核心思想来自 **aeb（AI Evaluation Benchmarks）森林** 中的 **Artificial Analysis Intelligence Index** 方法论：

> Intelligence Index v4.1 通过加权平均 **9 项评测**来计算，覆盖 **四大能力维度**：
> - **Agents (34%)**：Agent 任务完成能力
> - **Coding (24%)**：代码生成能力
> - **Scientific Reasoning (24%)**：科学推理能力
> - **General Capability (18%)**：通用能力

我们将这四大能力维度映射到知识森林质量的 5 个评审维度：

```
Intelligence Index 四大能力维度          →  知识森林 5 评审维度
═══════════════════════════════════════════════════════════

General Capability (18%, AA-Omniscience + AA-LCR)
  → 引用真实性（基础事实能力：能否正确回忆论文是否存在）
  → 引用准确性（精确引用能力：能否准确记住论文的元数据）

Scientific Reasoning (24%, HLE + GPQA Diamond + CritPt)
  → 批判性分析（深层推理：能否进行方法间的横向对比和局限性分析）

Agents (34%, GDPval-AA + τ³-Banking)
  → 层级组织（结构化规划：能否将复杂内容组织为清晰的层级结构）
  → 学术规范（指令遵循：能否按照规定的格式输出内容）

Coding (16%, Terminal-Bench + SciCode)
  → （间接支撑）代码/形式化知识的抽取质量
```

#### 6.2 能力-质量映射表（基于 DeepSeek V4 Pro 实测校准）

| Intelligence Index | D1:引用真实 | D2:引用准确 | D3:层级组织 | D4:批判分析 | D5:学术规范 | **综合** | 人工修正率 | 实证状态 |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| < 40 | ? | ? | ? | ? | ? | **差** | > 40% | 无实测（推断） |
| **44** | **9/10** | **7/10** | **8/10** | **4/10** | **5/10** | **6.5/10** | **~14%** | **DeepSeek V4 Pro 实测** |
| ~50 | 预期 9-10 | 预期 8 | 预期 8-9 | 预期 5-6 | 预期 6-7 | **~7.5/10** | < 10% | 推断 |
| ~55 | 预期 9-10 | 预期 8-9 | 预期 8-9 | 预期 7 | 预期 7-8 | **~8.5/10** | < 8% | 推断 |
| **60** (Claude Fable 5) | 预期 9-10 | 预期 9-10 | 预期 9 | 预期 8-9 | 预期 8-9 | **~9+/10** | < 5% | 推断 |

#### 6.3 能力门槛效应（关键发现）

基于 44 分实测数据，识别出三类不同的能力响应模式：

```
模式 A：门槛效应（非线性）
────────────────────────
引用真实性：  ____|¯¯¯¯¯
                ↑
              门槛 ~40
达到后不再显著提升

层级组织：   ____|¯¯¯¯¯
               ↑
             门槛 ~40
结构化能力在中低水平就饱和


模式 B：近似线性增长
────────────────────────
引用准确性：  /¯¯¯
              ↑
            持续改善

学术规范：   /¯¯¯
             ↑
           持续改善（与指令遵循正相关）


模式 C：陡峭增长（高能力区差异最大）
────────────────────────
批判性分析：    ___/¯¯¯¯¯¯
                   ↑
              ~55 后才开始显著分化
这是区分"能用"和"优秀"的分水岭
```

#### 6.4 对模型路由的实践指导

基于能力-质量映射，推荐分层模型路由策略：

| 知识抽取阶段 | 所需能力维度 | 推荐 Intelligence Index | 性价比之选 |
|------------|------------|:---:|----------|
| **建库阶段**（引用真实+层级组织） | General + Agents | ~40-50 | DeepSeek V4 Flash ($0.10/M) |
| **校验阶段**（引用准确+学术规范） | General + Agents | ~45-55 | Claude Sonnet 4.6 ($3/$15 per M) |
| **深化阶段**（批判性分析+横评） | Scientific Reasoning | **> 55** | Claude Opus 4.7 / Claude Fable 5 ($5/$25 per M) |

**参考文档**：
- `references/intelligence_index_mapping.md` —— 完整映射方法论和 aeb 评测基准参照
- `references/scoring_standardization.md` —— 评分标准化与统计显著性检验
- `docs/forest/ai-evaluation-benchmarks/Artificial Analysis Intelligence Index方法论.md` —— AAI 方法论原文

---

## 评审报告输出规范

### 必填章节

一份完整的评审报告应包含以下章节：

```markdown
# <森林名称> 知识森林质量评审报告

> **评审日期**: YYYY-MM-DD
> **评审者**: <模型名称及估计能力等级>
> **评审对象**: <森林目录路径及文档数量>
> **评审方法**: 基于 forest-quality-reviewer skill 的 5 维度评审体系
> **置信度**: High/Medium/Low（基于验证数据的可信程度）

## 1. 评审概述
## 2. 评审维度与结果（5 个维度逐一展开）
## 3. 综合评分与能力映射
## 4. 改进建议（按优先级排序）
## 5. 信息来源与可信度声明
## 6. 局限性声明
```

### 评分汇总表示例

| 维度 | 评分 | 与 Intelligence Index <N> 分的对应 | 主要发现 |
|------|:---:|:---:|------|
| 引用真实性 | X/10 | ... | ... |
| 引用准确性 | X/10 | ... | ... |
| 层级组织 | X/10 | ... | ... |
| 批判性分析 | X/10 | ... | ... |
| 学术规范 | X/10 | ... | ... |
| **综合** | **X.X/10** | **...** | **...** |

### 可信度分级

| 等级 | 条件 |
|------|------|
| **High** | 有 arxiv-mcp-server 逐条验证 / paper-review skill 结构化审稿 / 实测脚本运行结果 |
| **Medium** | 有间接来源（web 搜索确认）但未经一手工具验证 |
| **Low** | 基于推断或主观判断，无直接验证数据 |

**参考文档**：`references/report_template.md`
**资产模板**：`assets/review_scorecard_template.md`

---

## 与 aeb 评测基准的联动

本 Skill 的 Intelligence Index 映射直接依赖于 `aeb`（AI Evaluation Benchmarks）森林提供的方法论基础：

| aeb 资源 | 在本 Skill 中的角色 |
|----------|-------------------|
| Artificial Analysis Intelligence Index 方法论 | 能力空间的定义和评分计算方式 |
| MMLU 基准详解 | 通用知识能力的参照基准（广度） |
| GPQA 基准详解 | 科学推理能力的参照基准（深度） |
| AAI 四大能力维度权重 | 映射到 5 评审维度的理论基础 |

**重要声明**：Artificial Analysis Intelligence Index 是第三方商业评测平台的数据，其动态更新特性意味着：
- 每次评审时应注明使用的 AAI **版本号**
- 不同版本的权重变化可能影响映射关系的稳定性
- AAI 数据不应作为唯一的模型能力证明（应与 MMLU/GPQA 等学术基准互补使用）

---

## 参考资源

| 资源 | 路径 | 内容 |
|------|------|------|
| 5 维度评审体系详解 | `references/review_dimensions.md` | 每个维度的评分标准、检查清单、实测基线 |
| Intelligence Index 能力映射 | `references/intelligence_index_mapping.md` | 映射方法论、aeb 联动、能力门槛效应分析 |
| 评分标准化与对照实验 | `references/scoring_standardization.md` | 统计显著性检验、对照组设计、p-value 计算 |
| aeb 评测基准集成指南 | `references/aeb_benchmark_integration.md` | 如何使用 AAI/MMLU/GPQA 数据辅助评审 |
| 评审报告模板 | `references/report_template.md` | 完整的报告 Markdown 模板 |
| 评审评分卡模板 | `assets/review_scorecard_template.md` | 可直接复制的评分汇总表 |
