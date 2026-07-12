---
forest: aic
tree: AI 人机协作
branch: Agent 设计
title: Agent 角色与职责定义
version: 1.0.0
created: 2026-07-12
updated: 2026-07-12
description: 通用 Agent 系统中各角色的精确定义——Manager Agent、Worker Agent、Reviewer Agent 的职责边界、通信协议和调度规则
keywords:
  - Agent角色
  - Manager Agent
  - Worker Agent
  - Reviewer Agent
  - 调度协议
refs:
  - "[aic] CEO-子公司协作模型 | 组织类比中的角色对应"
  - "[aic] 胶水提示词设计 | Agent 间通信的提示词模板"
  - "[mke] Agent Memory 能力对齐 | Agent 的记忆基础设施"
---

# Agent 角色与职责定义

## 角色体系

```
          ┌──────────────────┐
          │   Human (CEO)    │
          │   设定方向/决策    │
          └────────┬─────────┘
                   │ 目标 + 验收标准
                   ▼
          ┌──────────────────┐
          │  Manager Agent   │
          │   (CTO)          │
          │   任务拆解/调度    │
          └────────┬─────────┘
                   │ 子任务分配
       ┌───────────┼───────────┐
       ▼           ▼           ▼
┌──────────┐ ┌──────────┐ ┌──────────┐
│ Worker A │ │ Worker B │ │ Worker C │
│ 代码实现  │ │ 测试编写  │ │ 文档更新  │
└──────────┘ └──────────┘ └──────────┘
       │           │           │
       └───────────┼───────────┘
                   │ 产出汇总
                   ▼
          ┌──────────────────┐
          │  Reviewer Agent  │
          │   代码审查/合并    │
          └──────────────────┘
```

## Manager Agent（CTO）

### 职责边界
- **负责**：接收人类的高层目标，拆解为可执行的子任务
- **负责**：按 Worker 能力将子任务分配给最合适的 Worker Agent
- **负责**：监控 Worker 进度，处理超时和异常
- **负责**：汇总 Worker 产出，在需要跨模块决策时上报人类
- **不负责**：写代码、Review 代码、修改文档（这些是 Worker 的职责）
- **不负责**：自行决定上线或改变架构方向

### 调度协议
```
输入: { goal: string, acceptance_criteria: string[], constraints: string[] }
处理:
  1. 解析目标 → 拆解为 Epic
  2. Epic → 子任务列表 [{ id, type, description, estimated_complexity }]
  3. 按 type 匹配 Worker 池 → 分配任务
  4. 等待所有 Worker 完成 → 汇总产出
  5. 判断是否需要人工决策 → 是: 上报 / 否: 交给 Reviewer
输出: { summary: string, pr_list: [...], decisions_needed: [...] }
```

## Worker Agent（开发小组）

### 类型分类

| Worker 类型 | 擅长 | 触发条件 | 模型建议 |
|------------|------|---------|---------|
| `code-writer` | 代码实现、重构 | 任务 type = `implementation` | GPT-5.5/Claude（复杂）或 GPT-5.6 Sol（简单） |
| `test-writer` | 单元测试、集成测试 | 任务 type = `testing` | GPT-5.6 Sol（模式化任务） |
| `doc-writer` | 文档生成、同步更新 | 任务 type = `documentation` | GPT-5.6 Sol |
| `debugger` | 问题排查、日志分析 | 任务 type = `debugging` | GPT-5.5/Claude（需要深度推理） |
| `researcher` | 技术调研、方案对比 | 任务 type = `research` | GPT-5.5 + Web Search |

### 工作契约
- 接收子任务时，附带：任务描述 + 验收标准 + 上下文（由元知识引擎注入）
- 执行环境：隔离沙盒（Docker/虚拟环境）
- 完成条件：自测通过 → 提交 PR → 通知 Manager
- 失败处理：重试 2 次 → 标注失败原因 → 上报 Manager

## Reviewer Agent

### 职责
- 自动检查：编译、Lint、测试覆盖率
- 检查：开放协议合规（是否有高危开源协议引入）
- 比较：本次变更与历史类似变更的模式一致性
- 生成 PR 摘要（变更模块、覆盖率变化、风险提示）
- **不负责**：架构决策、业务逻辑正确性判断（交给人类）

### Review 门禁矩阵

| 检查项 | 通过条件 | 失败动作 |
|--------|---------|---------|
| 编译 | 0 error | 退回 Worker |
| Lint | 0 warning（可配置） | 退回 Worker |
| 测试 | 覆盖率不下降 + 新增用例通过 | 退回 Worker |
| 协议 | 无 GPL/AGPL 等强传染协议 | 上报人类 |
| 安全 | 无硬编码密钥/密码 | 上报人类 |

## 通信协议

Agent 之间通过结构化 JSON 通信：

```json
{
  "from": "manager-001",
  "to": "worker-code-003",
  "type": "task_assignment",
  "payload": {
    "task_id": "task-042",
    "description": "实现用户登录模块的 JWT 刷新逻辑",
    "acceptance_criteria": [
      "token 过期前 5 分钟自动刷新",
      "刷新失败返回 401"
    ],
    "context": { "retrieved_from_mke": [...] },
    "deadline": "2026-07-12T18:00:00Z"
  }
}
```

Manager Agent 和人类之间使用自然语言（聊天），仅在需要结构化决策时使用交互式 UI 弹窗。
