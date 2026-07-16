---
name: forest-generation-methodology
description: 从原始资料到层级化知识森林（Forest → Tree → Branch → Leaf）的端到端生成方法论——涵盖输入策展、主题设计、LLM 抽取、交叉声明检测、跨森林引用建立、引用真实性审计、索引文件生成、迭代修正的全流程 SOP。
metadata: {"version": "1.0.0", "created": "2026-07-15", "updated": "2026-07-15", "author": "Forest Memory Project"}
---

# 知识森林生成方法论（Forest Generation Methodology）

## 定位

本 Skill 是**实验导向的知识森林生成标准操作程序（SOP）**。

它不是"知识抽取工具"（那是 `knowledge-atom-extractor` 的职责），而是定义从原始资料到完整知识森林的**全流程方法论**——确保不同研究者使用相同方法、相同基础资料、切换不同模型时，能够产出可复现、可对照的实验数据。

## 适用场景

| 场景 | 触发方式 |
|------|---------|
| 从论文/综述/技术文档生成新的知识森林 | 加载此 skill 并指定输入资料目录 |
| 复现模型对照实验 | 使用同一份基础资料 × 不同 LLM 执行本 SOP |
| 将现有文档库迁移为森林结构 | 以现有 .docs 目录为输入执行 Step 0-7 |
| 建立领域知识的结构化知识库 | 选择领域综述/教材为输入 |

## 与其他 Skill 的关系

```
┌──────────────────────────────────────────────────────┐
│  forest-generation-methodology (本 skill)             │
│  角色：方法论型 — 定义完整的 9 步 SOP                  │
│                                                        │
│  引用的外部能力：                                       │
│  ├─ knowledge-atom-extractor    (Step 2,3: LLM抽取+检测) │
│  └─ arxiv-mcp-server            (Step 5: 引用审计)      │
│                                                        │
│  配合使用的 skill：                                     │
│  └─ forest-quality-reviewer     (输出物的评审)          │
└──────────────────────────────────────────────────────┘
```

## 核心工作流：9 步 SOP

```
Step 0   输入资料策展        → 选择什么样的原始资料决定了森林质量的上界
Step 1   森林主题设计         → 划分 Forest / Tree / Branch 层级结构
Step 2   LLM 知识原子抽取     → 调用 knowledge-atom-extractor 执行
Step 3   交叉声明检测         → 调用 knowledge-atom-extractor 执行
Step 4   引用关系建立         → 建立跨文档 refs 和跨森林引用网络
Step 5   引用真实性审计       → arxiv-mcp-server 逐条验证
Step 6   索引文件生成         → 生成 index.md 和各层级的元数据文件
Step 7   迭代修正追踪         → 结构化记录修正并反馈到 Few-shot
Step 8   实验元数据记录       → 记录模型版本/参数/时间戳等可复现信息
```

### Step 0：输入资料策展（Input Curation）

**目标**：选择高质量的基础资料作为森林构建的"原材料"。

**决策框架**：

| 策略 | 适用场景 | 资料来源 | 质量要求 |
|------|---------|---------|---------|
| **单源深度** | 针对特定领域的系统梳理 | 一篇高质量综述论文 + 其参考文献 | 综述需有明确的方法论声明（如 PRISMA） |
| **多源聚合** | 跨领域的知识整合 | 多篇综述/教材/技术报告 + 交叉引用验证 | 来源间需要有可追溯的引用关系 |
| **增量迭代** | 已有知识库的扩展 | 现有森林 + 新增文献 | 新增文献需与现有森林的主题边界对齐 |

**质量评估清单**：

- [ ] 资料是否经过同行评审？（学术论文 > 行业白皮书 > 博客文章）
- [ ] 是否包含可追溯的引用链？（每项主张都有 source 引用）
- [ ] 是否覆盖了目标领域的核心子主题？（不遗漏重要方向）
- [ ] 是否有明确的版本标识？（便于复现时的版本锁定）
- [ ] 语言是否为目标语言？（中文森林优先选中文资料）

**参考文档**：`references/input_curation_strategy.md`

---

### Step 1：森林主题设计（Forest Theme Design）

**目标**：将输入资料的内容映射为 `Forest → Tree → Branch` 的三级层级结构。

**设计原则**：

1. **树 = 子领域**：每棵 Tree 对应一个相对独立的子领域或研究方向
2. **枝干 = 话题类别**：每个 Branch 是 Tree 内的一组相关话题
3. **叶子 = 知识原子**：每个 Leaf 是单一职责的最小知识单元
4. **粒度控制**：
   - 单个 Tree 下建议 3-8 个 Branch
   - 单个 Branch 下建议 2-10 个 Leaf
   - 整个 Forest 建议 3-12 棵 Tree（过少则太粗，过多则碎片化）

**设计流程**：

```
1. 通读输入资料，提取所有核心概念/论点/方法
2. 概念聚类：将语义相近的概念归为一组（每组 = 一个候选 Tree）
3. 组内细分：每组内按"机制/应用/评估/局限"维度拆分 Branch
4. 边界审查：确认各组之间无重叠（如有重叠，合并或重新划分）
5. 命名规范：Tree 用领域名称（如"宏观架构"），Branch 用功能描述（如"时间分层"）
```

**MKE 项目实例**（bim 森林，22 文档，6 棵树）：

| Tree | Branch 示例 | Leaf 数 |
|------|------------|--------|
| 宏观架构 | 时间分层/系统分工/内容分类 | 3 |
| 微观机制 | 突触可塑性/编码策略/记忆动态 | 5 |
| 检索算法 | 互补算法/寻址方式/跨模态 | 3 |
| 新兴理论 | 统一框架/协同学习/前沿视角 | 5 |
| 未解之谜 | 睡眠/情感/意识 | 3 |
| 文献审计 | 审计报告/文献清单 | 2 |

**参考文档**：`references/forest_design_principles.md`

---

### Step 2：LLM 知识原子抽取（Knowledge Atom Extraction）

**目标**：调用 `knowledge-atom-extractor` skill，将输入资料拆分为符合规范的知识原子。

**执行方式**：

```bash
# 调用 knowledge-atom-extractor 的 extract_knowledge.py 脚本
python <skill-path>/knowledge-atom-extractor/scripts/extract_knowledge.py \
  --input <输入资料路径> \
  --forest <森林ID> \
  --tree <预设Tree列表> \
  --model <模型名称> \
  --backend openai \
  --output <输出目录> \
  --existing-db <已有知识库SQLite路径> \
  --threshold 0.80 \
  --embedding-model paraphrase-multilingual-MiniLM-L12-v2 \
  --exclude-index
```

**关键参数说明**：

| 参数 | 推荐值 | 说明 |
|------|--------|------|
| `--threshold` | 0.80 | 基于 MKE 51 文档实测校准（详见 cross_declaration_guide.md） |
| `--embedding-model` | paraphrase-multilingual-MiniLM-L12-v2 | 多语言模型对中文友好 |
| `--exclude-index` | 启用 | 避免 index.md 与子文档误报 |

**输出物**：每个知识原子为一个 `.md` 文件，包含 YAML Frontmatter + 正文。

**参考文档**（knowledge-atom-extractor 内置）：
- `knowledge-atom-extractor/references/extraction_schema.md`
- `knowledge-atom-extractor/references/prompt_strategies.md`

---

### Step 3：交叉声明检测（Cross-Declaration Detection）

**目标**：在 Step 2 的抽取过程中同步完成，检测新生成的原子与已有知识库之间的重复/冲突声明。

**执行方式**：由 `extract_knowledge.py` 在 Step 2 中自动执行（`detect_cross_declarations()` 函数）。

**检测结果分级处理**：

| 相似度范围 | duplicate_type | 动作 |
|-----------|---------------|------|
| > 0.90 | exact | 直接拒绝——极大概率完全重复 |
| 0.80 – 0.90 | partial | 标记待审——触发 LLM 二次裁决 |
| 0.70 – 0.80 | semantic | 记录关注——人工抽查 |
| < 0.70 | 通过 | 自动通过——正常领域关联 |

**参考文档**（knowledge-atom-extractor 内置）：
- `knowledge-atom-extractor/references/cross_declaration_guide.md`

---

### Step 4：引用关系建立（Reference Network Construction）

**目标**：建立知识原子之间的 `refs` 引用关系，形成图结构网络。

**两类引用**：

#### 4.1 森林内部引用（intra-forest refs）

知识原子 A 在正文中提及或依赖知识原子 B 时，A 的 YAML Frontmatter 中添加：

```yaml
refs:
  - "[tree_id] B的title | 引用原因"
```

**识别策略**：
- 同一 Tree 内的 Branch 之间：按"基础→进阶""机制→应用""理论→实证"方向建立引用
- 不同 Tree 之间：仅在有明确的跨域依赖时建立（如 bim→mke 的知识注入）
- 避免循环引用：如果 A→B 且 B→A，合并为一个双向引用或提取公共部分为独立原子

#### 4.2 跨森林引用（cross-forest refs）

当前森林的知识被其他森林消费时，使用格式 `[forest_id] 文档标题 | 说明`。

**MKE 项目实例**（bim 向 mke 注入 7 项知识）：

```yaml
# bim 森林的某文档中
refs:
  - "[mke] 五层架构蓝图 | BTSP写入优先级映射为P0-P2"
  - "[mke] 渐进式检索引擎 | CAM寻址算法影响多路粗筛策略"
  - "[mke] SQLite表结构设计 | 四类记忆映射为IM/SM/PM/WM"
```

**参考文档**：`references/cross_forest_reference_guide.md`

---

### Step 5：引用真实性审计（Citation Authenticity Audit）

**目标**：逐条验证森林中所有引用的真实性——确保不存在虚构的论文/书籍/网页。

**执行方式**：

```bash
# 使用 arxiv-mcp-server 逐条检索
# 对每篇带 arXiv ID 的引用：
mcp_call_tool("arxiv-mcp-server", "search_papers", {"query": "<arXiv ID 或标题>"})
# 对非 arXiv 引用（传统期刊/书籍）：
web_search("<作者> <标题> <期刊>")
```

**审计结果记录格式**：

| # | 引用文本 | 来源类型 | 验证状态 | 备注 |
|---|---------|---------|---------|------|
| 1 | Gershman et al. (2025), arXiv:2501.02950v2 | arXiv | ✅ 已确认 | arxiv-mcp-server 直接命中 |
| 2 | Ryan et al. (2015), Science | 传统期刊 | ✅ web 搜索确认 | 67% 未命中 arxiv 的属此类 |
| 3 | Unknown Author (2026) | 不明 | ⚠️ 无法确认 | **需标记为可疑** |

**质量指标**：

| 指标 | 计算 | 目标值 |
|------|------|--------|
| 引用真实率 | 已确认引用数 / 总引用数 | ≥ 95% |
| arxiv 可查率 | arxiv 直接命中数 / 总引用数 | 记录但不设目标（传统期刊不在 arxiv 上）|
| 虚构引用数 | 编造的引用数量 | **必须为 0** |

**参考文档**：`references/citation_audit_protocol.md`

---

### Step 6：索引文件生成（Index File Generation）

**目标**：为森林的每个层级生成标准的 `index.md` 元数据文件。

#### 6.1 森林级索引（Forest Index）

位于森林根目录，模板如下：

```markdown
---
forest: <forest_id>
title: <森林名称>
version: 1.0.0
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
description: <一句话概括森林定位和覆盖范围>
source: "[来源] 来源描述 | URL"
refs:
  - "[其他forest] 文档 | 跨森林引用说明"
---

# <森林名称>

## 定位
<一段话说明森林的核心定位>

## 森林内文档

### 树：<Tree1 名称>
| 文档 | 说明 |
|------|------|
| [文档1](path) | 描述 |
| ... | ... |

### 树：<TreeN 名称>
...（同上）...

## （可选）与其他森林的关系
<描述本森林向哪些森林注入知识，或从哪些森林消费知识>
```

#### 6.2 树级索引（Tree Index）

位于每个 Tree 目录下：

```markdown
---
forest: <forest_id>
tree: <tree_id>
title: <树名称>
version: 1.0.0
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
description: <树的定位>
refs:
  - "[同forest其他tree] 文档 | 引用说明"
  - "[其他forest] 文档 | 跨森林引用"
---

# <树名称>

## 本树枝干与叶子
| 枝干 | 叶子文档 |
|------|---------|
| <branch1> | [leaf1](path), [leaf2](path) |
| ... | ... |
```

**参考文档**：`references/index_generation_template.md`
**资产模板**：`assets/forest_index_template.md`

---

### Step 7：迭代修正追踪（Iteration Correction Tracking）

**目标**：将 Step 3（交叉声明检测）和 Step 5（引用审计）中发现的问题结构化记录，并反馈到后续抽取的 Few-shot 样本中。

**修正记录格式**：

```markdown
## 修正日志

### 修正 #<序号>
- **发现日期**: YYYY-MM-DD
- **发现阶段**: Step 3(交叉声明) / Step 5(引用审计)
- **问题描述**: 具体描述
- **涉及文件**: 文件路径列表
- **修正动作**: 修改了什么
- **修正状态**: pending / in_progress / verified
- **Few-shot 反馈**: 此修正如何转化为 Few-shot 示例
```

**迭代优化策略**：

| 迭代轮次 | 关注点 | 预期效果 |
|---------|--------|---------|
| 第 1 轮（前 10 个文档） | 层级归属准确性 | 校准 Tree/Branch 判断 |
| 第 2 轮（批量处理后） | 交叉声明漏检率 | 调整阈值和 Few-shot |
| 第 3 轮（审计后） | 引用准确性问题 | 补充引用格式的 Few-shot |

**参考文档**：`references/iteration_correction_tracker.md`

#### Step 7 补充：自评质量门禁的能力边界（实验实证）

> **来源**：exp-model-20260716-01 维度1 对照实验，3 个森林（dsv4flash/dsv4pro/glm52）均执行自评质量门禁后重评的实证发现。

**能力边界（实证）**：自评质量门禁作为"技术检查（非内容评分）"，其作用域**严格限于 D5 的 frontmatter 完整性**，D1-D4 内容维度完全不变。

| 森林 | 自评修复内容 | D5 变化 | D1-D4 变化 | 结论 |
|------|------------|:---:|:---:|------|
| dsv4flash | 补 `updated` 字段 + index `sources` 列表 | 5→6 (+1) | 全部不变 | 仅 D5 受影响 |
| dsv4pro | 无（version/updated 推迟修复） | 0 | 全部不变 | 推迟无增益 |
| glm52 | 补 `version` 字段 | 8→8.5 (+0.5) | 全部不变 | 仅 D5 受影响 |

**技术门禁 vs 内容评审的职责边界**：

| 维度 | 自评技术门禁（Step 7） | 交叉内容评审（forest-quality-reviewer） |
|------|---------------------|-------------------|
| 覆盖范围 | 空文件 / YAML 完整性 / 命名规范 / refs 格式 / index 存在性 | D1 引用真实性 / D2 引用准确性 / D3 层级组织 / D4 批判性分析 / D5 学术规范 |
| 能触及的评分维度 | 仅 D5（frontmatter 完整性部分） | D1-D5 全部 |
| 无法触及的短板 | D4 批判性深度、D2 引用语境准确性、D1 虚构引用、D3 跨树引用语义 | — |
| 执行者 | 抽取者自身（可修复技术错误） | 外部模型（只评分不修复） |

**典型案例——技术门禁无法捕获的内容级问题**：

dsv4flash 森林中 `l1-graphrag-multihop` 叶子将 PoG 方法名误写为 "Path-of-Graph"（正确为 "Paths-over-Graph"，arXiv:2410.14211）。该错误：
- **技术门禁未捕获**：文件非空、YAML 完整、命名规范、refs 格式正确——技术检查全部通过
- **交叉评审 D2 才发现**：glm52 重评时通过 arXiv 验证发现方法名错误

> **方法论反馈**：技术门禁有效捕获工程缺陷（空文件/YAML 重复键/缺失字段），但**无法替代内容质量评审**。内容级问题（方法名错误/引用语境偏差/批判深度不足）必须由交叉评审（forest-quality-reviewer）覆盖。两者正交配合，不可互相替代。

**步骤映射澄清**：实验执行 SOP（`assets/experiment_execution_sop.md`）中的"Step 3 自评质量门禁"对应本 SOP 的 **Step 6-7**（索引生成+迭代修正），**不是**本 SOP 的 Step 3（交叉声明检测）。交叉声明检测是语义级去重（sentence-transformers），自评质量门禁是技术级格式检查，两者层级不同。

---

### Step 8：实验元数据记录（Experiment Metadata Recording）

**目标**：记录本次森林生成的所有可复现参数，使实验可被他人复现或用于对照实验。

**必填元数据**：

| 字段 | 说明 | 示例 |
|------|------|------|
| `experiment_id` | 本次实验的唯一标识 | `fgm-20260715-dsv4pro-bim` |
| `model_name` | 用于 LLM 抽取的模型名称和版本 | `DeepSeek V4 Pro` |
| `intelligence_index` | 模型的 Artificial Analysis Intelligence Index 分数 | `44` |
| `model_provider` | API 提供商 | `deepseek-api.com` |
| `tool_name` | 执行抽取的 AI 编程工具名称 | `CodeBuddy` |
| `tool_version` | 工具版本号 | `4.10.2` |
| `ide_name` | IDE 名称 | `VS Code` |
| `ide_version` | IDE 版本号 | `1.106.1` |
| `os` | 操作系统及架构 | `Windows_NT x64 10.0.26200` |
| `input_source` | 输入资料的详细描述 | `综述论文 v4.0, 人脑记忆相关章节` |
| `input_version` | 输入资料的版本/日期 | `v4.0, 2026-03-12` |
| `output_dir` | 输出森林目录 | `docs/forest/bim` |
| `extraction_params` | knowledge-atom-extractor 的关键参数 | `threshold=0.80, embedding_model=paraphrase-multilingual-MiniLM-L12-v2` |
| `timestamp_start` | 开始时间 | `2026-07-15T10:00:00Z` |
| `timestamp_end` | 结束时间 | `2026-07-15T14:30:00Z` |
| `reviewer_model` | 如果做了评审，评审者模型 | `GLM-5.2` |
| `review_score` | 评审综合评分 | `6.5/10` |

**元数据文件位置**：`<output_dir>/.experiment_metadata.yaml`

---

## 对照实验执行指南

对照实验支持**三维对照矩阵**，可在任意一个维度上变化而固定其余两个维度：

### 维度 1：不同模型（固定工具 + 固定资料）

验证 AAI 能力门槛理论——不同能力等级的模型在知识抽取质量上的差异。

```
固定变量：
  ├── 工具（如 CodeBuddy v4.10.2）
  ├── 输入资料（同一份，锁定版本）
  ├── 方法论（本 SOP，9 步不变）
  └── 评测方法（forest-quality-reviewer skill）

自变量：
  └── LLM 模型（Model A vs Model B vs Model C）

因变量：
  ├── 5 维度评分
  ├── 综合评分
  ├── 人工修正率
  └── 生成效率（时间/token 消耗）
```

### 维度 2：不同工具（固定模型 + 固定资料）

验证工具差异对抽取质量的影响——不同 AI 编程工具使用同一模型时的抽取差异。

```
固定变量：
  ├── LLM 模型（同一模型，锁定版本）
  ├── 输入资料（同一份，锁定版本）
  ├── 方法论（本 SOP，9 步不变）
  └── 评测方法（forest-quality-reviewer skill）

自变量：
  └── AI 编程工具（CodeBuddy / qwen code cli / codex / claude code / qoder / opencode）

因变量：同维度 1
```

### 维度 3：不同资料（固定工具 + 固定模型）

验证方法论对不同领域知识的普适性。

```
固定变量：
  ├── 工具（同一工具，锁定版本）
  ├── LLM 模型（同一模型，锁定版本）
  ├── 方法论（本 SOP，9 步不变）
  └── 评测方法（forest-quality-reviewer skill）

自变量：
  └── 输入资料（bim 源文档 / frs 源文档 / 顶级期刊论文）

因变量：同维度 1
```

### 评审者偏差处理：交叉评审

评审者不能评审自己的输出。采用交叉评审矩阵：

```
被测模型（抽取者）     评审者
                    Model A    Model B    Model C
Model A              ✗ 跳过     ✓          ✓
Model B              ✓          ✗ 跳过     ✓
Model C              ✓          ✓          ✗ 跳过

✓ = 可评审   ✗ = 评审者偏差，跳过
```

每个模型被 2 个评审者评审，产生 6 组评审数据。

### 对照数据收集表格模板

**维度 1：不同模型对照**

| 实验 ID | 模型 | AAI | D1:引用真实 | D2:引用准确 | D3:层级组织 | D4:批判分析 | D5:学术规范 | 综合 | 修正率 | 评审者 |
|---------|------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|------|
| exp-001 | DeepSeek V4 Flash | 40 | ? | ? | ? | ? | ? | ? | ? | DSV4-Pro |
| exp-002 | DeepSeek V4 Pro | 44 | 9/10 | 7/10 | 8/10 | 4/10 | 5/10 | 6.5/10 | ~14% | DSV4-Flash |
| exp-003 | GLM-5.2 | 51 | ? | ? | ? | ? | ? | ? | ? | DSV4-Flash |
| exp-004 | [顶级模型] | 55+ | ? | ? | ? | ? | ? | ? | ? | ? |

**维度 2：不同工具对照**（固定模型 + 固定资料）

| 实验 ID | 工具 | 工具版本 | 模型 | D1 | D2 | D3 | D4 | D5 | 综合 | 修正率 | 评审者 |
|---------|------|---------|------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|------|
| exp-101 | CodeBuddy | 4.10.2 | DSV4-Pro (44) | ? | ? | ? | ? | ? | ? | ? | ? |
| exp-102 | qwen code cli | ? | DSV4-Pro (44) | ? | ? | ? | ? | ? | ? | ? | ? |
| exp-103 | codex | ? | DSV4-Pro (44) | ? | ? | ? | ? | ? | ? | ? | ? |
| exp-104 | claude code | ? | DSV4-Pro (44) | ? | ? | ? | ? | ? | ? | ? | ? |

### 开放贡献

项目发布后，社区贡献者可选择任意维度的实验组合提交 PR：
- 提交数据须包含完整的 `.experiment_metadata.yaml`（含实验环境声明）
- 评审须按交叉评审矩阵执行，不得自评
- 实验环境须与现有实验隔离（独立项目或独立目录）

---

## 参考资源

| 资源 | 路径 | 内容 |
|------|------|------|
| 输入资料策展策略 | `references/input_curation_strategy.md` | 质量评估清单、策展策略选择指南 |
| 森林主题设计原则 | `references/forest_design_principles.md` | 层级划分原则、命名规范、实例 |
| 跨森林引用建立指南 | `references/cross_forest_reference_guide.md` | refs 格式、引用方向规则、MKE 实例 |
| 引用审计协议 | `references/citation_audit_protocol.md` | 审计步骤、arxiv-mcp-server 使用、质量指标 |
| 索引文件生成模板 | `references/index_generation_template.md` | Forest/Tree 级 index.md 完整模板 |
| 迭代修正追踪策略 | `references/iteration_correction_tracker.md` | 修正日志格式、Few-shot 反馈循环 |
| 森林索引文件模板 | `assets/forest_index_template.md` | 可直接复制的 index.md 模板 |
| 实验项目目录结构模板 | `assets/experiment_project_template.md` | 对照实验项目的目录结构、命名规则和社区贡献流程 |
| 实验元数据模板 | `assets/experiment_metadata_template.yaml` | 实验环境声明和完整元数据的 YAML 模板 |
| 对照实验执行 SOP | `assets/experiment_execution_sop.md` | 实验场景变体：启动协议（询问用户维度）+ 三维度分支 + 交叉评审调度 |
| 实验环境初始化脚本 | `assets/setup_experiment.sh` | 基于 git worktree 创建物理隔离的实验环境，支持并行实验 |
| 实验结果合并脚本 | `assets/merge_experiment.sh` | 合并各 worktree 分支结果到主分支，生成对照矩阵和报告模板 |
| 实验数据归集脚本 | `assets/collect_experiment_data.py` | 从评审报告自动提取评分，计算均值和一致性，生成对照矩阵 |
| 知识抽取执行器 | `knowledge-atom-extractor/` (独立 skill) | Step 2-3 的具体实现 |
