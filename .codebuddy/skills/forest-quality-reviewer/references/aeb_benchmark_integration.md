# aeb 评测基准集成指南（AEB Benchmark Integration Guide）

## 概述

本文档说明如何将 `aeb`（AI Evaluation Benchmarks）森林中的三大评测基准集成到知识森林质量评审流程中，为 Intelligence Index 能力映射提供标准化的能力参照。

## 三大基准的角色分配

| aeb 基准 | 在 forest-quality-reviewer 中的角色 | 映射的评审维度 |
|----------|-------------------------------------|---------------|
| **Artificial Analysis Intelligence Index** | 核心能力标尺——定义模型的综合能力分数 | 全部 5 维度的能力空间定位 |
| **MMLU** | 广域知识能力的参照基准——补充 AAI General 维度的学术对标 | D1 引用真实性（基础事实广度）、D2 引用准确性 |
| **GPQA Diamond** | 深度推理能力的参照基准——补充 AAI Scientific Reasoning 的学术对标 | **D4 批判性分析**（核心关联维度）|

## AAI 集成方式

### 获取模型分数

```python
# 方法 1：从 Artificial Analysis 官网获取
# 访问 https://artificialanalysis.ai/text/leaderboards
# 找到目标模型的 Intelligence Index 分数

# 方法 2：使用 web_fetch 抓取特定模型页面
from web_fetch import fetch
result = fetch(
    url="https://artificialanalysis.ai/text/leaders",
    fetch_info="Extract the Intelligence Index score for <model_name>"
)
```

### 版本锁定

每次评审必须注明使用的 AAI 版本：

```yaml
# 在评审报告的元数据中：
aai_version: "v4.1"
aai_retrieval_date: "2026-07-15"
aai_url: "https://artificialanalysis.ai/methodology/intelligence-benchmarking"
```

**版本注意事项**：
- AAI 的权重会随版本变化（如 v4.0 四类均权 25% → v4.1 Agent 升至 34%）
- 不同版本的分数不可直接比较
- 如果评审跨越多个 AAI 版本，需在报告中注明并分别列出

## MMLU 集成方式

### 用途

MMLU（57 学科 15908 题）作为**广域知识能力的独立验证**：

| 场景 | MMLU 的作用 |
|------|------------|
| 模型 A 的 II 分数未知 | 用 MMLU 分数推断大致的 General 能力水平 |
| D1/D2 评分异常 | 对照 MMLU 分数判断是"该领域特异"还是"普遍能力不足" |
| 学术报告引用 | MMLU 是论文中"必报指标"，增加评审报告的学术可信度 |

### MMLU → D1/D2 的参照表

| MMLU 分数范围 | 推断的 General 能力 | 对 D1/D2 的预期影响 |
|-------------|-------------------|-------------------|
| > 90% | 极强 | D1 预期 9-10，D2 预期 8-10 |
| 80-90% | 强 | D1 预期 9，D2 预期 7-9 |
| 70-79% | 中上 | D1 预期 8-9，D2 预期 7-8 |
| 60-69% | 中 | D1 预期 8，D2 预期 6-7 |
| < 60% | 弱 | D1 可能 < 8，D2 可能 < 6 |

**注意**：这是粗略参照，非精确映射。MMLU 测的是选择题准确率，D1/D2 测的是引用质量——两者相关但不等价。

## GPQA 集成方式

### 用途

GPQA Diamond（198 题，博士级难度）作为**深度推理能力的核心验证**——与 D4（批判性分析）高度相关：

| GPQA Diamond 分数 | 推断的 Scientific Reasoning 能力 | 对 D4 的预期影响 |
|-------------------|----------------------------------|-----------------|
| > 70% | 顶尖（超越 GPT-4 基线 39% 的近 2 倍）| D4 预期 **8-10** |
| 55-70% | 强（显著超越基线） | D4 预期 **6-8** |
| 40-54% | 中（接近或略超 GPT-4 基线） | D4 预期 **4-6** |
| 30-39% | 一般（GPT-4 基线水平） | D4 预期 **3-5** |
| < 30% | 弱 | D4 预期 **< 4** |

**DeepSeek V4 Pro 的对照**：
- 如果 DS-V4-Pro 的 GPQA Diamond 分数可获取，可直接验证 D4=4/10 是否与其推理能力一致
- 这将为"能力-质量映射"提供第二个独立的数据点（除 AAI 外）

## 多基准交叉验证策略

当多个基准的数据都可获取时，进行交叉验证以提高映射的可信度：

```
                    ┌─ AAI II = 44
                    │
模型能力评估 ───────┼─ MMLU = ?%
                    │
                    └─ GPQA = ?%
                          │
                          ▼
              ┌──────────────────────┐
              │   三角验证            │
              │                      │
              │  AAI ↔ MMLU 一致性？   │ ← 检查 General 能力是否自洽
              │  AAI ↔ GPQA 一致性？   │ ← 检查 Scientific Reasoning 是否自洽
              │  MMLU ↔ GPQA 一致性？  │ ← 检查整体能力画像是否合理
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │   修正后的能力画像      │
              │   → 输入到 D1-D5 映射    │
              └──────────────────────┘
```

### 不一致时的处理

| 不一致模式 | 可能原因 | 处理方式 |
|-----------|---------|---------|
| AAI 高但 MMLU 低 | AAI 权重偏向 Agent/Coding，该模型通用知识偏弱 | 以 AAI 为主，MMLU 作为辅助警示 |
| GPQA 显著高于 AAI Scientific 推断 | 该模型在科学推理上有特长 | D4 评分可能高于 AAI 映射预期 |
| 三个基准互相矛盾 | 数据来源时间不同、模型版本差异 | 报告所有数据，标注不一致，不做强行统一 |

## 引用规范

在评审报告中引用 aeb 基准时：

```markdown
### 模型能力参照

- **Artificial Analysis Intelligence Index**: v4.1, score=XX [来源]
- **MMLU**: XX% (Hendrycks et al., 2020, arXiv:2009.03300) [如有]
- **GPQA Diamond**: XX% (Rein et al., 2023, arXiv:2311.12022) [如有]
```
