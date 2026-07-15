# 引用真实性审计协议（Citation Audit Protocol）

## 概述

Step 5 是知识森林生成流程中的**质量控制关卡**——逐条验证所有引用的真实性，确保森林中不存在虚构的论文、书籍或网页。这是区分"严肃的知识工程"和"AI 幻觉产物"的核心环节。

## 审计工具链

| 工具 | 用途 | 适用范围 |
|------|------|---------|
| **arxiv-mcp-server** | 通过标题/arXiv ID 搜索 arXiv 数据库 | 所有带 arXiv ID 的引用 |
| **Web Search** | 搜索非 arXiv 论文（传统期刊/书籍） | Science/Nature/Cell/Neuron 等顶刊论文 |
| **DOI 解析器** | 通过 DOI 精确定位论文 | 所有带 DOI 的引用 |
| **人工审核** | 无法自动验证时的最终手段 | 特殊文献（技术报告/内部文档）|

## 审计流程

### Phase 1：自动批处理（arxiv-mcp-server）

```python
# 伪代码：arxiv 批量审计
from arxiv_mcp_server import search_papers

citations = extract_all_citations(forest_dir)  # 提取所有引用
results = []

for cit in citations:
    if cit.arxiv_id:
        paper = search_papers(query=cit.arxiv_id, max_results=1)
        if paper.found and match_title(paper.title, cit.title):
            results.append({
                "citation": str(cit),
                "status": "CONFIRMED_ARXIV",
                "method": "arxiv-mcp-server",
                "evidence": f"arXiv:{paper.arxiv_id}"
            })
        else:
            results.append({"status": "NOT_FOUND_ARXIV", ...})
    
log_results(results)  # 写入审计日志
```

### Phase 2：补充验证（Web Search）

对 arxiv 未命中的引用（通常是因为论文发表于传统期刊），使用 Web Search 补充验证：

```python
# 伪代码：web 搜索补充验证
import web_search

for result in results:
    if result["status"] == "NOT_FOUND_ARXIV":
        query = f"{cit.authors} {cit.title} {cit.year}"
        web_results = web_search.search(query, max_results=5)
        
        if any(match_institution(r, cit.institution) for r in web_results):
            results[i]["status"] = "CONFIRMED_WEB"
            results[i]["method"] = f"web_search: {web_results[0].url}"
        else:
            results[i]["status"] = "SUSPICIOUS"  # 标记为可疑
```

### Phase 3：可疑项人工复核

对标记为 `SUSPICIOUS` 的引用进行人工决策：

| 选项 | 操作 | 条件 |
|------|------|------|
| ✅ 确认真实 | 更新状态为 `CONFIRMED_MANUAL` | 通过其他途径（Google Scholar/ResearchGate）找到证据 |
| ❌ 确认虚构 | **删除该引用并修正引用它的 Leaf** | 经过充分搜索仍找不到任何证据 |
| ⚠️ 标记存疑 | 保留但标注置信度低 | 有间接证据但无法完全确认 |

## 质量指标计算

### 指标定义

| 指标 | 公式 | 目标值 | 含义 |
|------|------|--------|------|
| **引用真实率** | `confirmed / total × 100%` | **≥ 95%** | 核心质量指标 |
| **arxiv 可查率** | `arxiv_confirmed / total_arxiv_citations × 100%` | 记录 | 反映资料来源的开放程度（传统期刊不在 arxiv 上，此值自然偏低）|
| **虚构引用数** | `count(status == FABRICATED)` | **必须为 0** | 一票否决指标 |
| **可疑引用数** | `count(status == SUSPICIOUS)` | **< 3%** | 需后续跟进 |

### 分级标准

| 引用真实率 | 等级 | 行动 |
|-----------|------|------|
| 98-100% | **A+** | 优秀——无需进一步行动 |
| 95-97% | **A** | 良好——记录可疑项待后续确认 |
| 90-94% | **B** | 及格——需补充验证遗漏的 5-10% |
| < 90% | **C** | 不合格——需大规模重审 |

## 审计输出格式

### 审计日志文件

审计结果应写入森林目录下的 `citation_audit_log.md`：

```markdown
# 引用真实性审计日志

> **审计日期**: YYYY-MM-DD
> **审计工具**: arxiv-mcp-server + Web Search
> **审计范围**: <Forest名称>, 共 N 篇引用

## 汇总统计

| 指标 | 数值 |
|------|------|
| 总引用数 | N |
| arxiv 确认数 | n1 (%) |
| Web 搜索确认数 | n2 (%) |
| 人工确认数 | n3 (%) |
| 存疑数 | n_sus (%) |
| **虚构数** | **n_fab (** 必须为 0 **)** |
| **引用真实率** | **(N - n_fab - n_sus) / N × 100%** |

## 逐条审计结果

### Tree: <tree_name>

| # | 引用文本 | 来源类型 | 验证状态 | 验证方式 | 备注 |
|---|---------|---------|---------|---------|------|
| 1 | Author (Year), Title | arXiv | ✅ CONFIRMED | arxiv-mcp-server | 直接命中 |
| 2 | Author (Year), Title | 传统期刊 | ✅ CONFIRMED | web_search | Science/Nature 等 |
| 3 | Unknown (Year), Title | 不明 | ⚠️ SUSPICIOUS | — | 需人工复核 |

## 修正记录

### 修正 #1
- **发现**: 引用 #X 为虚构
- **涉及**: leaf_name.md 第 Y 行
- **动作**: 删除该引用，替换为正确的引用 Z
- **状态**: verified
```

## 能力门槛观察

基于 DeepSeek V4 Pro（Intelligence Index = 44）的实测数据：

| 模型能力 | 引用真实率 | 虚构率 | 解读 |
|---------|:---:|:---:|------|
| **44 分（DeepSeek V4 Pro）** | **100%（89篇全真实）** | **0%** | 基础事实能力的"能力门槛"可能在 ~35-40 分 |
| < 40（推断） | 可能 < 95% | 可能 > 0% | 低能力模型倾向于编造引用以满足"看起来专业"的需求 |
| > 50（推断） | 预期 99-100% | 0% | 高能力模型的引用真实率不会显著优于 44 分（门槛效应）|

**结论**：引用真实性存在**非线性门槛效应**——低于某条线会编造，达到后不再线性提升。44 分已经越过这个门槛。
