---
forest: frs
tree: reasoning-evaluation
branch: paradigm-discussion
leaf_id: frs-eval-discuss-001
title: 评估范式的结构性问题
type: analysis
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
source: "[frs_source] §5.3 评估范式讨论"
refs:
  - "[frs-eval-bench-001] 推理基准演进"
  - "[frs-eval-dynamic-001] 动态Agent评估"
---

# 评估范式的结构性问题

## 三大结构性挑战

### 1. 评估成本与可复现性

MemBench、MemoryArena等基准需要多轮Agent-环境交互，单次评估的API调用成本和时间开销远高于GSM8K类静态基准，导致**社区复现门槛显著提高**。

### 2. 记忆与推理的纠缠

当前Agent记忆基准同时测量记忆能力和推理能力，难以分离"记错了"和"推理错了":
- 需要更细粒度的归因分析框架
- 理想状态下应能分别报告记忆正确率和推理正确率

### 3. 生态碎片风险

静态基准时代的统一标杆（GSM8K/MATH）正被碎片化的专用Agent基准取代：
- 不同基准间结果不可直接比较
- 跨工作横向对比变得日益困难
- 缺乏类似ImageNet的统一评测平台

## 建议方向

- 建立标准化Agent评估协议，减少环境差异
- 开发记忆-推理分离的归因评估方法
- 降低Agent基准的执行成本以促进复现
