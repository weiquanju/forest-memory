---
forest: memory-systems-ai
tree: t1-human-memory-principles
branch: b2-synaptic-plasticity-coding
leaf: synaptic-plasticity-rules
title: Hebbian/STDP/BTSP多时间尺度突触可塑性
created: 2026-07-16
model: DeepSeek V4 Pro
source:
  - "bim_source/人脑记忆机制的数据结构与算法分析.md"
refs:
  - "[t1-b2] 稀疏编码与模式分离 | 可塑性规则的下游编码效应"
---

# Hebbian/STDP/BTSP多时间尺度突触可塑性

## 三种核心可塑性规则

大脑使用多时间尺度的可塑性规则分工，使得既能进行精细的学习调整，又能在必要时快速捕获和存储新经历。

| 规则 | 时间尺度 | 机制 | 功能 |
|------|---------|------|------|
| **Hebbian** | 无严格时序约束 | "一起放电的神经元加强连接" | 联想记忆编码（如 Hopfield 网络权重初始化） |
| **STDP** | 毫秒级 | 突触前先于突触后几毫秒→LTP，反之→LTD | 序列学习、因果推理 |
| **BTSP** | 秒级 | 树突 Ca²⁺ 平台电位一次性增强窗口内所有输入 | 快速经验学习、位置场一次性形成 |

## STDP（脉冲时序依赖可塑性）

STDP 是 Hebbian 原则的时序精细化。关键发现：突触前后放电的毫秒级精确时序匹配，需要多次重复才能产生稳定的突触变化。在算法上对应于时序差分学习，可用于训练脉冲神经网络（SNN）完成模式识别和序列预测。

## BTSP（行为时间尺度可塑性）

Bittner 等人（2017, *Science*）发现海马体 CA1 位置细胞的位置场形成不由传统 Hebbian/STDP 机制驱动，而是由 BTSP 驱动。

**核心机制**：当 CA1 锥体细胞的远端树突产生钙离子平台电位时，该信号在秒级时间窗口内（平台电位前后数秒，约 4s 上升 / 3s 衰减），将窗口内所有活跃突触输入一次性增强。BTSP 可在单次经历中完成突触强度的持久改变，使位置细胞在一次探索中即可快速建立位置偏好放电。

**计算建模**：Wu 和 Maass（2025, *Nature Communications*）构建的 BTSP 计算模型证明，BTSP 的独特窗口机制能解释 CA1 位置场的一次性快速形成，传统可塑性模型无法重现这一现象。Magee（2026, *Nature Neuroscience*）进一步综述指出 BTSP 广泛存在于海马体 CA1 及其他脑区。

## 多时间尺度分工的工程意义

毫秒级 STDP 负责精细时序调谐，秒级 BTSP 负责行为关键时刻一次性创建宏观记忆痕迹。这启示 AI 记忆系统应具备多速率学习能力：快速路径用于捕获重要新事件，慢速路径用于精细模式学习。
