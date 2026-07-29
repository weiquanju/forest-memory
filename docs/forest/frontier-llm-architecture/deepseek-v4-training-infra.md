---
forest: flm
tree: 基础设施
branch: 训练框架
title: DeepSeek-V4 训练基础设施
version: 1.0.0
created: 2026-07-29
updated: 2026-07-29
description: DeepSeek-V4 的训练基础设施创新——细粒度 Expert Parallelism 通信计算重叠、TileLang DSL 和批次不变确定性内核库。
keywords:
  - training infrastructure
  - expert parallelism
  - TileLang
  - batch invariance
  - deterministic kernels
  - DeepSeek-V4
refs:
  - "[flm] Kimi K3 训练基础设施 | 对比性训练框架"
  - "[flm] DeepSeek-V4 推理优化 | 推理侧基础设施"
---

# DeepSeek-V4 训练基础设施

## 1. 细粒度 Expert Parallelism

### 通信-计算重叠
将 MoE 层分解为四个阶段，融合为统一 pipeline：
- **Dispatch**（通信密集）→ **Linear-1**（计算密集）
- **Linear-2**（计算密集）→ **Combine**（通信密集）

关键洞察：MoE 层中通信时间 < 计算时间，融合后计算仍是瓶颈 → 系统可容忍更低互联带宽。

### Wave-Based 调度
将 experts 分组为 waves，每个 wave 完成通信立即开始计算。稳态下：当前 wave 计算 + 下一 wave token 传输 + 已完成 expert 结果发送 → 三者并发。

### MegaMoE
开源 CUDA mega-kernel，NVIDIA GPU 和华为 Ascend NPU 双平台验证：
- 通用推理：1.50–1.73× 加速
- RL rollout / Agent serving：最高 1.96×

### 硬件协同设计建议
- **计算-通信比**：C/B ≤ 2d = 6144 FLOPs/Byte 即可完全隐藏通信
- **功耗预算**：kernel fusion 使计算/内存/网络同时高负载
- **通信原语**：pull-based dispatch 避免细粒度 push 的通知延迟

## 2. TileLang DSL

- 用少量 fused kernels 替代数百个细粒度 Torch ATen operators
- 平衡开发效率与运行时性能

### Host Codegen
- 设备 kernel + 轻量 host launcher 在 IR 层联合生成
- Python 侧的 per-invocation 检查开销从数百微秒降至 <1 微秒

### SMT-Solver-Assisted Formal Analysis
- 集成 Z3 SMT solver (QF_NIA)
- 用于 layout inference、memory hazard detection、bound analysis
- 编译时开销仅数秒

### 数值精度与 Bitwise Reproducibility
- 默认关闭 fast-math
- IEEE-compliant 内置函数
- 与 CUDA baseline 的 bit-identical 输出

## 3. 批次不变 + 确定性内核库

### Batch Invariance
- **Attention**：双 kernel 策略（单 SM 全序列 + 多 SM 最终 wave）
- **Matrix Mul**：DeepGEMM 替代 cuBLAS，未使用 split-k

### Determinism
- **Attention Backward**：每 SM 独立 buffer → 全局确定性求和
- **MoE Backward**：token order pre-processing + buffer isolation
- **mHC Backward**：split-k 结果分离输出 + 后续确定性 reduction

## 4. 训练框架优化

- **Muon + ZeRO**：Knapsack 分配 + 冗余计算（见 Muon 优化器叶）
- **mHC**：fused kernels + selective recomputation + DualPipe 1F1B 调整 → 仅 6.7% 开销
- **Context Parallelism for CSA/HCA**：两阶段通信（tail token 交换 → all-gather → fused select-and-pad）
- **Tensor-Level Activation Checkpointing**：TorchFX 图追踪 + 最小重计算子图
