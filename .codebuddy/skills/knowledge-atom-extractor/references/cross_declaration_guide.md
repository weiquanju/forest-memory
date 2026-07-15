# 交叉声明检测策略与阈值配置

## 核心问题

知识库中的**交叉声明（Cross-Declaration）** 是指两个或多个文档重复声明同一知识点，
违反单一职责原则（SSOT）。如果不从构建环节就检测并阻止，会导致：

- 一致性危机：修改 A 文档时忘记同步 B 文档中的重复声明
- 检索冗余：同一知识被多次返回，挤占上下文窗口
- 维护成本：知识更新需要多处同步修改

## 检测流程

```
候选知识原子 (candidate)
    │
    ▼
┌──────────────────────────┐
│  第一层：向量相似度粗筛    │
│  candidate 向量 vs       │
│  所有 existing leaves 向量  │
│  → 筛出 top-N 相似项      │
└──────────────┬───────────┘
               │
    ┌──────────┴──────────┐
    ▼                     ▼
 相似度 > 0.95         相似度 0.85-0.95
    │                     │
    ▼                     ▼
 直接拒绝              LLM 二次裁决
 返回引用建议          判断是重复还是互补
                         │
                ┌────────┴────────┐
                ▼                 ▼
             重复→拒绝         互补→通过
             引用建议          保留两个原子
```

## 阈值配置

### 默认阈值

| 阶段 | 相似度范围 | 动作 | 人工介入 |
|------|-----------|------|---------|
| 粗筛 | > 0.95 | 直接拒绝 | 否（自动处理） |
| 待审 | 0.85 – 0.95 | 标记待审，触发 LLM 裁决 | LLM 裁决后可人工复核 |
| 通过 | < 0.85 | 自动通过 | 否 |

### 按知识库规模的阈值建议

| 知识库规模 | 粗筛阈值 | 待审下限 | 说明 |
|-----------|---------|---------|------|
| < 100 个原子 | 0.92 | 0.80 | 小库容错高，多检查 |
| 100 – 1000 | 0.95 | 0.85 | 默认值 |
| 1000 – 10000 | 0.96 | 0.87 | 大库降低待审量，依赖 LLM 质量 |
| > 10000 | 0.97 | 0.88 | 超大库需配合聚类预筛 |

### 按领域的阈值建议

| 领域特性 | 粗筛阈值 | 待审下限 | 原因 |
|---------|---------|---------|------|
| 代码/技术文档 | 0.95 | 0.85 | 术语精确，相似度高时大概率重复 |
| 法律/合规文档 | 0.90 | 0.80 | 条款表述相似但适用场景不同，需更严格检查 |
| 营销/创意文档 | 0.88 | 0.78 | 创意内容相似度天然较低，阈值需降低 |
| 学术/研究文档 | 0.93 | 0.82 | 引用多但需区分原始来源和二手转述 |

### 基于实测数据的校准建议（MKE 自身验证）

以下数据来自对 MKE 项目 51 个知识原子的交叉声明检测自测，使用 `all-MiniLM-L6-v2` 嵌入模型：

| 相似度范围 | 对数 | 占比 | 实测判定 |
|-----------|------|------|---------|
| > 0.80 | 4 | 0.3% | 2 对为 index 与子文档（正常），2 对为语义相关不同概念 |
| 0.70 – 0.80 | 39 | 3.1% | 同领域语义相关，非交叉声明 |
| 0.60 – 0.70 | 192 | 15.1% | 同森林内知识关联，正常 |
| 0.55 – 0.60 | 191 | 15.0% | 弱关联 |
| < 0.55 | 849 | 66.6% | 独立主题 |
| **平均相似度** | — | — | **0.493** |

**关键发现与校准建议**：

1. **0.85 阈值过于严格**——实测中无任何对超过 0.85，但文档确实没有交叉声明。建议粗筛阈值下调至 **0.80**
2. **index 文件需排除**——index.md 与子文档的高相似度是正常的概述关系，非交叉声明。使用 `--exclude-index` 参数排除
3. **多语言模型更准确**——`all-MiniLM-L6-v2` 是英文模型，对中文嵌入区分度不足（平均 0.493 偏高）。建议使用 `paraphrase-multilingual-MiniLM-L12-v2`（默认）
4. **同领域知识库的相似度基线偏高**——51 个文档均在记忆/知识/协作领域，语义天然关联紧密。不同领域需重新校准基线

**校准后的推荐阈值（中文知识库）**：

| 阶段 | 相似度范围 | 动作 | 说明 |
|------|-----------|------|------|
| 粗筛 | > 0.90 | 直接拒绝 | 极高概率完全重复 |
| 待审 | 0.80 – 0.90 | 标记待审，触发 LLM 裁决 | 可能是部分重复或 index 关系 |
| 关注 | 0.70 – 0.80 | 记录但不拦截 | 语义相关，人工抽查 |
| 通过 | < 0.70 | 自动通过 | 正常的领域内关联 |

## LLM 二次裁决 Prompt

当相似度落在 0.85-0.95 区间时，使用以下 Prompt 让 LLM 做精确判断：

```
你是知识库一致性审查专家。判断以下两个知识原子是否构成交叉声明（重复声明同一知识点）。

## 候选知识原子 A
标题：{candidate_title}
描述：{candidate_description}
内容摘要：{candidate_content_preview}

## 已有知识原子 B
标题：{existing_title}
描述：{existing_description}
内容摘要：{existing_content_preview}

## 判定规则

1. duplicate_type = "exact"：A 和 B 声明了完全相同的知识点，只是表述不同
   → 建议拒绝 A，引用 B

2. duplicate_type = "partial"：A 和 B 有部分内容重叠，但 A 包含 B 没有的新信息
   → 建议保留 A，但在 A 中通过 refs 引用 B，去除重复部分

3. duplicate_type = "semantic"：A 和 B 语义相关但声明的是不同知识点
   → 建议保留 A，并在 references 中建立引用关系

## 输出 JSON

{
  "duplicate_type": "exact" | "partial" | "semantic",
  "action": "reject" | "accept_with_ref" | "accept",
  "reason": "判断理由（一句话）",
  "suggestion": "建议操作（如适用）",
  "confidence": 0.0-1.0
}
```

## 检测策略选择

### 策略一：纯向量检测（最简方案）

适用条件：知识库 < 1000 个原子，无 sqlite-vec 环境。

```python
# 使用 sentence-transformers 本地嵌入
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

def detect_cross_declaration(candidate_text, existing_texts, threshold=0.85):
    cand_vec = model.encode([candidate_text])[0]
    exist_vecs = model.encode(existing_texts)
    similarities = np.dot(exist_vecs, cand_vec) / (
        np.linalg.norm(exist_vecs, axis=1) * np.linalg.norm(cand_vec)
    )
    return [(i, sim) for i, sim in enumerate(similarities) if sim > threshold]
```

优点：零依赖、本地运行、无需 API。
缺点：嵌入质量低于 OpenAI text-embedding-3-small；全量计算 O(n) 延迟随库增长。

### 策略二：sqlite-vec 检测（推荐方案）

适用条件：已有 SQLite + sqlite-vec 环境。

```python
import sqlite3
import sqlite_vec

def detect_cross_declaration_vec(candidate_vec, db_path, threshold=0.85, top_k=10):
    conn = sqlite3.connect(db_path)
    conn.enable_load_extension(True)
    sqlite_vec.load(conn)

    # 向量检索 top-k 相似叶子
    results = conn.execute(
        "SELECT leaf_id, distance FROM vec_leaf "
        "WHERE embedding MATCH ? AND k = ? ORDER BY distance",
        [candidate_vec.tolist(), top_k]
    ).fetchall()

    # distance → similarity (cosine distance = 1 - cosine_similarity)
    candidates = [(row[0], 1 - row[1]) for row in results if (1 - row[1]) > threshold]
    conn.close()
    return candidates
```

优点：高效索引检索、与知识库一体化、支持大规模库。
缺点：需要预建向量索引。

### 策略三：两阶段检测（大规模库推荐）

适用条件：知识库 > 10000 个原子。

1. **聚类预筛**：对已有叶子做 K-Means 聚类，候选先找最近簇
2. **簇内向量检索**：仅在最近簇内做精确向量搜索
3. **LLM 裁决**：对 top-N 结果做 LLM 二次判断

```
全库 N 个叶子 → K 个簇 (K = √N)
     │
     ▼
候选向量 → 找最近 1-3 个簇
     │
     ▼
簇内 M 个叶子做向量检索 (M << N)
     │
     ▼
top-K 结果做 LLM 二次裁决
```

## 特殊场景处理

### 场景一：版本更新导致的内容重叠

旧版本和新版本的 description 可能高度相似。检测时应：
- 跳过 `status = 'deprecated'` 的叶子（旧版本已被弃用）
- 对 `status = 'stable'` 的叶子做更严格的检测

### 场景二：跨森林的知识迁移

同一知识点从 A 森林迁移到 B 森林时，A 中的旧原子应标记为 `deprecated`，
B 中的新原子应通过 refs 引用 A 的旧原子（保留追溯链路）。

### 场景三：程序性知识的相似度

Prompt 模板类知识原子的文本相似度天然较高（都包含"你是..."、"请输出..."等模板句式）。
建议：
- 对 `atom_type = 'procedural'` 的原子，阈值提高 0.03
- 在 LLM 二次裁决时，要求判断"操作步骤是否相同"而非"文本是否相似"

## 评估指标

| 指标 | 定义 | 目标 | 测量方法 |
|------|------|------|---------|
| 误拒率 | 被错误拒绝的非重复原子比例 | < 5% | 人工审核被拒绝的候选 |
| 漏检率 | 未被检测到的真实交叉声明比例 | < 10% | 定期全量人工抽查 |
| LLM 裁决准确率 | LLM 二次判断与人工判断一致的比例 | > 85% | 记录 LLM 判断 + 人工复核 |
| 检测延迟 | 从候选输入到检测完成的时间 | < 2s | 计时（含向量检索 + LLM 裁决） |
