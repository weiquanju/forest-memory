---
forest: flm
tree: 基础设施
branch: 推理框架
title: Kimi K3 推理基础设施
version: 1.0.0
created: 2026-07-29
updated: 2026-07-29
description: Kimi K3 的推理基础设施——KDA Prefix Caching、EAGLE-3 Draft Model 推测解码和 Cache/Budget-Aware 调度。
keywords:
  - inference infrastructure
  - KDA prefix caching
  - speculative decoding
  - EAGLE-3
  - draft model
  - Kimi K3
refs:
  - "[flm] DeepSeek-V4 推理优化 | 对比性推理框架"
  - "[flm] Kimi K3 训练基础设施 | 训练侧基础设施"
---

# Kimi K3 推理基础设施

## 1. KDA 推理优化

### State-Aware Prefix Caching
KDA 用固定大小 recurrent state S ∈ R^(dk×dv) 替代增长式 KV cache，天然适合 prefix caching：
- 每个 prefix 的 cumulative state 可直接缓存和复用
- 无需管理分页 KV cache block
- **Inter-block state**（跨 BlockAttnRes block）也可合并

### KDA Decoding Kernel
Decoding 场景的挑战不同于 training/prefill：
- Small batch × single new token → 不同的并行度瓶颈
- 专门设计的 decoding kernel 解决此 regime 的性能问题

## 2. EAGLE-3 Draft Model

Kimi K3 利用预训练的 MTP layer 微调为推测解码 draft model：

### 架构
- Draft 结构匹配 backbone 的 MTP layer（单 decoder layer）
- 输入融合三层次 target model features：
  - **Low-level**：第 1 个 AttnRes block 输出
  - **Mid-level**：第 4 个 AttnRes block 输出
  - **High-level**：最后 AttnRes block 输出 h_h
- 投影初始化为 [0 0 I]，使初始融合 = h_h（MTP 预训练时的输入）

### 训练
- Target model 冻结，仅更新 draft layer + feature fusion projection
- 7 步 unrolling（EAGLE-3 training-time protocol）
- 优化目标：**L_K loss**（直接最大化 acceptance rate）

```
L_K = -log(Σ_x min(p(x), q(x)))
```

而非传统的 KL divergence（KL 最小化不保证最大化 acceptance rate）。

### 量化配置
- MoE expert weights：MXFP4
- Activations：MXFP8
- Non-expert 模块：保持高精度

## 3. Cache/Budget-Aware Fleet Scheduling

- 跨请求感知 KV cache 使用和 token budget
- 将基础设施效率转化为可预测的生产服务
