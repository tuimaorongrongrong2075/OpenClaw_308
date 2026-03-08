# 多Agents设置研究

> 创建时间: 2026-03-05

## OpenClaw 多Agents架构

### 两种模式

#### 1. 直接调用模式 (Direct Agent Calls)
- 每个 specialized agent 直接调用
- 每个 agent 维护自己的 memory/context
- 手动路由任务到合适的 agent

#### 2. 编排器模式 (Orchestrator Pattern)
- 一个主 "router" agent 分析请求
- 主 agent 委派给 specialized agents
- Agents 之间通过编排器通信
- 可以观察多 agent 对话流程

### 官方支持

OpenClaw 支持通过以下方式实现多 agents：
- `sessions_spawn` - 创建子 agent 会话
- `sessions_send` - Agent 间通信
- `cron` (isolated) - 定时任务

### 参考资源

- OpenClaw 文档: https://docs.openclaw.ai/concepts/multi-agent
- Claude Code Agent Teams: https://code.claude.com/docs/en/agent-teams
- Anthropic 多Agent研究系统: https://www.anthropic.com/engineering/multi-agent-research-system

---

*最后更新: 2026-03-05*
