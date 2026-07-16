# 对照矩阵：exp-tool-20260716

## 实验参数

| 项目 | 值 |
|------|-----|
| 维度 | 维度2：不同工具 |
| 固定模型 | DSV4-Flash |
| 固定资料 | bim_source + frs_source + arXiv:2404.13501 |
| 被测工具 | opencode, CodeBuddy |

## 森林结构对比

| 指标 | opencode | CodeBuddy |
|------|:--------:|:---------:|
| 森林数 | 1 (mi) | 3 (bim, frs, llm-agent-memory) |
| 树(Tree)数 | 6 | 11 |
| 叶子(Leaf)数 | 22 | 64 |
| 总文档数 | 31 | 71 |
| 组织策略 | 统一森林 | 按资料源分森林 |
| 语言 | 中文为主 | 中文 |
| 空文件 | 0 | 2（已修复） |
| 修正日志 | 无 | 3条（大文档分块、跨森林引用、branch index） |
| 引用审计 | 13条 ✅ | 有引用审计报告 |

## 森林设计差异

| 维度 | opencode | CodeBuddy |
|------|----------|-----------|
| bim_source 处理 | 拆分到 mi 的 neural-macro/micro/retrieval | 独立 bim 森林（4 trees, 21 leaves） |
| frs_source 处理 | 拆分到 mi 的 knowledge-reasoning/agent-memory | 独立 frs 森林（6 trees, 23 leaves） |
| 2404.13501 处理 | 拆分到 mi 的 agent-memory | 独立 llm-agent-memory 森林（5 trees, 11 leaves） |
| 跨森林引用 | ✅ refs 链接 | ✅ refs 链接 |
| 审计文档 | ✅ 引用审计 + 文献清单 | ✅ 引用审计报告 + 修正日志 |

## 交叉评审归集（Step 5，手动归集）

> 归集方式：脚本 `collect_experiment_data.py` 因文件名/分组键不兼容维度2（详见文末说明）无法提取，改按 SOP 回退路径手动归集。
> 评审方法：加载 forest-quality-reviewer skill，按 5 维度评分（D1 引用真实性 / D2 引用准确性 / D3 层级组织 / D4 批判性分析 / D5 学术规范）。

### 评审清单

| 报告文件 | 评审者 | 被评审工具 | D1 | D2 | D3 | D4 | D5 | 综合 | 类型 |
|---------|--------|-----------|:--:|:--:|:--:|:--:|:--:|:--:|------|
| `reviews/CodeBuddy_opencode.md` | CodeBuddy (DSV4-Flash, AAI 40) | opencode | 7 | 7 | 8 | 5 | 6 | 6.6 | 主交叉评审 |
| `reviews/opencode_CodeBuddy.md` | opencode (DSV4-Flash, AAI 40) | CodeBuddy | 7 | 6 | 7 | 5 | 6 | 6.2 | 主交叉评审 |
| `reviews/opencode_CodeBuddy_Hy3.md` | Hy3 (opencode, 不同家族) | CodeBuddy | 8 | 7 | 8 | 4 | 7 | 6.8 | 补充重评 |

### 五维度评分（按被评审工具汇总）

| 维度 | opencode (n=1) | CodeBuddy 主评 (n=1) | CodeBuddy 含Hy3均值 (n=2) |
|------|:--:|:--:|:--:|
| D1 引用真实性 | 7 | 7 | 7.5 |
| D2 引用准确性 | 7 | 6 | 6.5 |
| D3 层级组织 | 8 | 7 | 7.5 |
| D4 批判性分析 | 5 | 5 | 4.5 |
| D5 学术规范 | 6 | 6 | 6.5 |
| **综合** | **6.6** | **6.2** | **6.5** |

### 评审者间一致性

| 被评审工具 | 评审者 | 一致性 | 说明 |
|-----------|--------|:--:|------|
| opencode | CodeBuddy | N/A | 仅 1 位评审者（维度2 双 subject，opencode 只被 CodeBuddy 评审） |
| CodeBuddy | opencode + Hy3 | 精确一致 0/5；全部落于 ±1 | 5 维度评分两两相差恰为 1 分，属合理评审者间方差 |

### 归集要点（诚实声明）

- **样本量极小**：维度2 仅 2 个被测对象。按标准交叉评审矩阵只产生 2 组主数据；opencode 侧仅 1 位评审者，无一致性可算。
- **Hy3 为补充重评**：Hy3（不同模型家族）对 CodeBuddy 的重评是主矩阵之外的补充，用于降低同源偏差，但不改变"仅 2 subject"的样本量本质。含 Hy3 的 CodeBuddy 均值（6.5）与主评（6.2）方向一致。
- **同源偏差**：两个主评审者共用底层模型 DSV4-Flash（AAI 40），主交叉评审的 `bias_risk` 均标注为 low，但同源偏差客观存在（尤其 D4/D5 主观维度）。
- **两工具综合分接近**（opencode 6.6 vs CodeBuddy 主评 6.2，差 0.4），在如此小样本 + 同源评审下，不足以断言工具间存在显著质量差异；差异主要来自组织策略（统一森林 vs 按源分森林）与叶子规模（22 vs 64）。

## 附：数据归集脚本不兼容说明（待决定是否修脚本）

`collect_experiment_data.py` 为维度1（不同模型）设计，运行于本维度2 实验时有两处不兼容：

1. **文件名 glob**：脚本只扫 `review-*.md`，本实验报告命名为 `{评审者}_{被评审者}.md`，匹配 0 份。
2. **分组键**：脚本按 `reviewee_model` 分组，维度2 两工具模型同为 `DSV4-Flash`，会被错误合并；正确应按 `reviewee_tool` 分组。

> 是否修改该共享 skill 脚本以支持维度2/3，需另行讨论——本次采用手动归集，未改动脚本。
