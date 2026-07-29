---
forest: flm
tree: 训练方法论
branch: 预训练策略
title: 长上下文扩展策略对比
version: 1.0.0
created: 2026-07-29
updated: 2026-07-29
description: 对比 DeepSeek-V4 与 Kimi K3 在长上下文扩展上的不同策略——Partial RoPE + 文档 packing vs NoPE + 渐进式 curriculum。
keywords:
  - long-context extension
  - position encoding
  - NoPE
  - partial RoPE
  - progressive curriculum
refs:
  - "[flm] DeepSeek-V4 预训练数据与配置 | DeepSeek 预训练策略"
  - "[flm] Kimi K3 预训练与 Scaling Law | Kimi 预训练策略"
---

# 长上下文扩展策略对比

## 位置编码策略

| 维度 | DeepSeek-V4 | Kimi K3 |
|------|------------|---------|
| **位置编码方式** | Partial RoPE（尾部 64 维） | NoPE（无显式位置编码） |
| **扩展时修改** | 无需修改 | 无需修改 |
| **位置信息编码** | RoPE 提供 relative position | KDA 的 recurrent gating + decay 隐式编码 |
| **MLA 层处理** | N/A | NoPE，由 KDA 层提供位置感知 |

## 长上下文数据策略

### DeepSeek-V4
- 特别重视长文档数据策展：科学论文、技术报告
- Document packing 最小化截断
- Sample-level attention masking（区别于 V3）

### Kimi K3
- 自然长文档/视频的清洗 pipeline：精确+模糊去重、感知哈希（视频）、质量过滤
- **上采样**长文档避免被短序列淹没
- **合成长上下文数据**：通过排列和拼接多模态文档/子任务，使嵌入的任务只能通过关注分散在 1M context 中的信息来解决

## 渐进式上下文扩展

### DeepSeek-V4
预训练后即可原生支持 1M context（未详述 curriculum）

### Kimi K3
四阶段 curriculum：
```
8K → 64K → 256K → 1M
```
将昂贵的长序列计算集中在训练预算的小部分（cooldown 阶段）。

## 关键分歧

1. **位置编码哲学**：DeepSeek-V4 仍依赖 RoPE 的显式相对位置，Kimi K3 完全依赖 KDA 的隐式时序编码
2. **数据合成**：Kimi K3 专门合成了"必须关注全 1M context 才能解决"的任务，防止 attention 退化为局部模式
3. **渐进式 vs 一次性**：Kimi K3 的分阶段策略更精细，DeepSeek-V4 在预训练后即具备 1M 能力
