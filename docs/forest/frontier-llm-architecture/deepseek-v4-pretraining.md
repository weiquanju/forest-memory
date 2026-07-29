---
forest: flm
tree: 训练方法论
branch: 预训练策略
title: DeepSeek-V4 预训练数据与配置
version: 1.0.0
created: 2026-07-29
updated: 2026-07-29
description: DeepSeek-V4 系列的预训练数据构建、模型配置和训练超参数——覆盖 32T+ tokens 的多领域语料。
keywords:
  - pre-training
  - data construction
  - training configuration
  - DeepSeek-V4
refs:
  - "[flm] Kimi K3 预训练与 Scaling Law | 对比性预训练策略"
---

# DeepSeek-V4 预训练数据与配置

## 数据构建

在 DeepSeek-V3 数据基础上扩展，预训练语料超 32T tokens，涵盖：
- 数学内容、代码、网页、长文档、多语言数据

### 关键改进
- **Web 数据**：过滤批量化自动生成和模板化内容，降低模型坍塌风险
- **Coding 数据**：mid-training 阶段引入 agentic data
- **多语言**：扩大长尾知识覆盖
- **长文档**：特别重视科学论文和技术报告

### 数据处理
- Tokenizer：DeepSeek-V3 tokenizer + 少量特殊 token，vocab 保持 128K
- 继承 token-splitting 和 Fill-in-Middle (FIM) 策略
- 采用 sample-level attention masking（区别于 V3）
- Document packing 最小化截断

## 模型配置

| 参数 | Flash | Pro |
|------|-------|-----|
| Transformer 层数 | 43 | 61 |
| Hidden dim d | 4096 | 7168 |
| 总参数 | 284B | ~1.6T |
| 激活参数 | 13B | 49B |
| 路由专家/层 | 256 | — |
| 每 token 激活 | 6 | — |
| MTP 深度 | 1 | 1 |
| mHC n_hc | 4 | — |

### 层布局 (Flash)
- Layer 1-2：纯 Sliding Window Attention
- Layer 3-43：CSA/HCA 交错（前 3 MoE 层用 Hash Routing）
- CSA: m=4, HCA: m'=128

### 训练配置
- Flash 预训练：32T tokens
- Pro 预训练：33T tokens
- 预训练后即可原生高效支持 1M context
