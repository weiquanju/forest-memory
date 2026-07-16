---
forest: mi
tree: knowledge-reasoning
branch: evaluation
title: 推理基准演进
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
description: 从静态数学基准到动态多轮Agent记忆测试的推理评估范式转型
keywords:
  - 推理基准
  - 动态评估
  - Agent记忆测试
  - MemBench
  - MemoryArena
  - 评估范式
atom_type: semantic
status: draft
refs:
  - "[mi] 记忆评估方法 | Agent记忆的专用评估基准"
  - "[mi] RLVR与推理输出关系 | 推理输出质量依赖于评估基准设计"
---

# 推理基准演进

推理评估经历了从静态到动态的范式转型：

**静态阶段**：基于数学和逻辑推理的静态基准（如GSM8K、MATH、MMLU），测试模型在封闭问题上的推理能力。优点是可重复、成本低，缺点是难以反映真实Agent与环境的交互能力。

**动态阶段**：引入多轮交互和工具使用，评估模型在动态环境中的推理连贯性（如AgentBench、SWE-bench）。

**Agent记忆测试阶段**：专用基准如MemBench和MemoryArena构建标准化Agent记忆测试场景，模拟多种交互类型和记忆负载。MemoryArena特别关注长时间交互中记忆保持和检索的准确性，评估记忆系统在实际Agent工作流中的有效性。

这一演进反映了评估理念的根本转变：从"模型知道什么"（静态知识）到"模型如何持续运用知识"（动态记忆管理），再到"模型如何通过记忆自主改进"（自我进化）。
