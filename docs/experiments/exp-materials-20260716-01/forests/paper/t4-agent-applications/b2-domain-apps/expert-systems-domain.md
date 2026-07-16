---
forest: agent-memory-survey
tree: t4-agent-applications
branch: b2-domain-apps
title: 垂直领域专家系统中的记忆
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
source: "[arXiv:2404.13501] Section 7.6-7.7"
refs:
  - "[t2-b2] 参数化记忆 | 专家系统广泛使用Fine-tuning注入领域知识"
  - "[t2-b1] 外部知识集成 | 专家系统依赖外部领域知识库"
---

# 垂直领域专家系统中的记忆

## 医疗领域（Medicine Domain）

### 主流策略：外部知识注入

| 模型 | 方法 | 知识源 | 基础模型 |
|------|------|--------|---------|
| Huatuo [107] | Fine-tune + 医学知识图谱 CMeKG [165] | QA 形式的医学知识 | LLaMA [127] |
| DoctorGLM [129] | LoRA 高效微调 | 医疗数据 | ChatGLM [130] |
| Radiology-GPT [132] | SFT + 标注放射学数据集 | 放射学专业知识 | — |
| Wang et al. [151] | 文本外部知识获取 | 结构化医学知识库 | — |
| EHRAgent [152] | 成功案例相似度检索 | 过往经验 | — |
| ChatDoctor [115] | Fine-tuned 获取流程 | Wikipedia + 医学数据库 | LLaMA [127] |

## 金融领域（Finance Domain）

| 模型 | 记忆内容 | 策略 |
|------|---------|------|
| InvestLM [113] | 金融投资知识 | SFT + 投资数据集 |
| TradingGPT [154] | 分层结构存储不同类型的市场信息 | Layered Memory |
| QuantAgent [155] | 持续交互记录 + 过往输出（经验检索） | Self-improving |
| FinMem [156] | 分层记忆提供丰富推理信息 | Layered Memory |
| Koa et al. [157] | 过去价格变动+解释 + 历史 trial 反思 | Self-reflective |

## 科学领域（Science Domain）

| 模型 | 领域 | 记忆策略 |
|------|------|---------|
| Chemist-X [158] | 化学合成 | 分子数据库 + 在线文献 → 外部知识检索 |
| ChemDFM [160] | 化学 | Fine-tuning 注入化学领域知识 |
| MatChat [162] | 材料科学 | Fine-tuning 注入结构化材料知识 |

## 专家系统的三个核心挑战

| 挑战 | 描述 | 潜在方向 |
|------|------|---------|
| **高精度要求** | 领域知识专业性强，错误代价高 | 更强的验证机制和不确定性量化 |
| **时效性** | 领域知识随时间过时 | 部分更新机制（Knowledge Editing） |
| **海量知识检索** | 大量领域知识难以基于当前查询准确召回 | 分层索引 + 上下文引导检索 |

## 其他应用

| 模型 | 领域 | 记忆功能 |
|------|------|---------|
| RCAgent [166] | 云根因分析 | 框架规则 + 任务需求 + 工具文档 + Few-shot + 观察 |
| Agent-OM [167] | 本体匹配 | 保存对话对话 + 构建推理数据库 |
| DiLu [168] | 自动驾驶 | 向量数据库存储过往驾驶场景经验 |
| XUAT-Copilot [169] | 用户验收测试 | 自我反思 + 更新记忆池直到达成目标 |

## 通用设计原则

1. **领域知识向 LLM 的对齐**：需要将结构化领域知识（KG/数据库）转化为 LLM 可消费的记忆形式
2. **分层记忆架构**：是多个领域系统（TradingGPT, FinMem, RecAgent）的共同选择——不同层级存储不同粒度的信息
3. **记忆时效管理**：领域知识的时效性要求记忆支持部分更新而非全量重建
