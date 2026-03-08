# Agent Team Orchestration 规划上下文

> 时间: 2026-03-05
> 目标: 基于 agent-team-orchestration skill 搭建多 Agent 工作流

---

## 背景

用户安装了 `agent-team-orchestration` skill，希望基于此搭建知识库 + 看板自动化工作流。

---

## 1. Skill 分析

### 来源
- **Skill**: agent-team-orchestration
- **ClawHub**: https://clawhub.com/skill/agent-team-orchestration
- **作者**: arminnaimi
- **下载量**: 3.615 (最高)

### 核心概念

| 概念 | 说明 |
|------|------|
| **Orchestrator** | 路由、追踪、状态管理 |
| **Builder** | 执行工作、产出产物 |
| **Reviewer** | 质量审核、把关 |
| **Ops** | 定时任务、健康检查 |

### 任务生命周期

```
Inbox → Assigned → In Progress → Review → Done | Failed
```

### Handoff 格式（必须包含5项）

1. 做了什么 + 为什么
2. 产物路径
3. 如何验证
4. 已知问题
5. 下一步找谁

---

## 2. 决策记录

### 2.1 目录结构

**最终决策:**

```
shared/
├── specs/              # 需求规格
├── tasks/              # 任务追踪
└── artifacts/          # 产出物（任务状态流转）
    ├── inbox/          # 待处理任务
    ├── decisions/      # 决策记录
    ├── in-progress/    # 进行中
    ├── reviews/        # 待审核（含 review.md）
    ├── done/           # 已完成
    └── failed/         # 失败（含原因）
```

**讨论过程:**
- 最初: `shared/` 下只有 `specs/` + `artifacts/增加`
- 建议: `tasks/` 任务追踪
- 建议 `decisions/` 放 `agents/` 下
- 最终决策: `decisions/` 合并到 `artifacts/` 下

### 2.2 Agent 数量

**最终决策:** 2 个 Agent（可扩展）

| Agent | 角色 |
|-------|------|
| Builder | 执行者 |
| Reviewer | 审核者 |

**理由:**
- 简化初始复杂度
- 具体角色可以后续随时调整
- 对应知识库 + 看板两个工作流

### 2.3 核心原则

**必须包含错误处理流程:**
- 异常捕获机制
- 降级策略（Fallback）
- 错误通知机制
- 人工介入触发条件

---

## 3. 待讨论问题（未完成）

| # | 问题 | 状态 |
|---|------|------|
| 1 | 任务来源：手动 / 定时？ | ⏳ |
| 2 | 交付物：知识库 / 看板？ | ⏳ |
| 3 | Review 标准：什么算通过？ | ⏳ |
| 4 | 验证方式细化 | ⏳ |

---

## 4. 产出文档

| 文件 | 说明 |
|------|------|
| `agent1-team-orchestration-analysis.md` | Skill 分析 |
| `agent2-team-config-analysis.md` | 配置模板 |
| `workflow/coding-team-setup.md` | 对比 skill |
| `workflow/multi-agent-setup.md` | 规划笔记 |
| `workflow/knowledge-base-prompt.md` | 知识库 prompt |
| `workflow/dashboard-prompt.md` | 看板 prompt |

---

## 5. 下一步

1. 确定任务来源（手动/定时）
2. 确定交付物类型
3. 制定 Review 标准
4. 实际配置 Agent

---

*整理时间: 2026-03-05*
