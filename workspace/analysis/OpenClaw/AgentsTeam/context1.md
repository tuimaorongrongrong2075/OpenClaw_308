# context1: agent-team-orchestration 讨论记录

> 日期: 2026-03-05
> 主题: 多 Agent 系统方案设计

---

## 讨论背景

基于已安装的 `agent-team-orchestration` Skill 进行多 Agent 系统设计。

**Skill 来源**: ClawHub
**安装状态**: ✅ 已安装

---

## 讨论内容整理

### 1. 安装 Skill

- ✅ 使用 `clawhub install agent-team-orchestration` 安装
- 安装位置: `/root/.openclaw/workspace/skills/agent-team-orchestration/`

### 2. 研究 Skill 功能

| 功能 | 支持 | 说明 |
|------|------|------|
| 角色定义 | ✅ | Orchestrator/Builder/Reviewer/Ops |
| 任务生命周期 | ✅ | Inbox→Assigned→In Progress→Review→Done/Failed |
| 交接协议 | ✅ | 必须包含5个要素 |
| 审核流程 | ✅ | 每个 artifact 必须有人审核 |
| 不同模型 | ✅ | 每个角色可用不同模型 |
| 不同渠道 | ✅ | 通过 bindings 配置 |

### 3. 架构设计（1主+2子）

| 角色 | 名称 | 职责 |
|------|------|------|
| Orchestrator | 指挥官 | 任务分发、状态跟踪、结果汇总 |
| Builder | 执行者 | 执行具体任务、产出 artifact |
| Reviewer | 审核者 | 质量检查、查漏补缺 |

### 4. 错误处理机制

| 状态 | 处理方式 |
|------|----------|
| Failed | 记录原因，转人工或重试 |
| Blocked | 通知 Orchestrator |
| Timeout | 超时自动回滚 |

**错误升级**:
```
Level 1: Agent 自己处理
    ↓
Level 2: 通知 Orchestrator
    ↓
Level 3: 转人工
```

### 5. 目录结构设计

```
workspace/
├── agents/               # 多 Agent 工作区
│   ├── orchestrator/    # 主 Agent
│   ├── builder/         # 执行者
│   └── reviewer/        # 审核者
├── artifacts/           # 产出物
│   ├── inbox/           # 待处理
│   ├── in-progress/     # 进行中
│   ├── review/          # 待审核
│   ├── done/            # 已完成
│   ├── failed/          # 失败
│   └── decisions/       # 决策记录
└── shared/              # 共享资源
```

### 6. 核心概念细化

#### 角色职责
- **Orchestrator**: 接收任务→分发→跟踪→汇总→返回
- **Builder**: 执行→产出 artifact→报告进度
- **Reviewer**: 检查→指出问题→验证质量

#### 任务状态
| 状态 | 超时 |
|------|------|
| Inbox | 5分钟 |
| Assigned | 10分钟 |
| In Progress | 30分钟 |
| Review | 10分钟 |

#### 交接协议 5 要素
1. 做了什么
2. artifacts 路径
3. 验证方法
4. 已知问题
5. 下一步

### 7. 涉及修改的文件

| 概念 | 文件 |
|------|------|
| 角色 | `workspace/SOUL.md`, `agents/builder/SOUL.md`, `agents/reviewer/SOUL.md` |
| 任务 | `artifacts/inbox/`, `artifacts/review/` 等 |
| 交接 | `shared/prompts/handoff.md` |

### 8. 根目录 Agent

原来的 Agent 变成 Orchestrator（主 Agent），不会消失。

---

## 待确认事项

1. 需要几个 Agent？
2. 每个 Agent 叫什么、做什么？
3. 每个 Agent 用什么模型？
4. 什么渠道对应哪个 Agent？

---

*整理时间: 2026-03-05*
