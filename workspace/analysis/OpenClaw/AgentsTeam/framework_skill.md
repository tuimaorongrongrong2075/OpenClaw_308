# 多 Agent 系统设置方案设计

> 日期: 2026-03-05
> 状态: 方案设计中

---

## 1. 需求分析

### 1.1 目标
为 OpenClaw 设置多 Agent 协作系统，实现：
- 任务分发与协调
- 子 Agent 管理
- 跨 Agent 记忆共享

### 1.2 场景
- 复杂任务分解多个子任务
- 不同 Agent 处理不同专业领域
- 并行处理提高效率

---

## 2. 方案设计

### 2.1 方案对比：自建 vs ClawHub Skill

| 对比项 | 自建方案（CrewAI/LangGraph） | ClawHub Skill |
|--------|------------------------------|---------------|
| **部署速度** | 需编写代码和配置 | 即装即用 |
| **定制程度** | 完全可控 | 受限于 skill 功能 |
| **维护成本** | 需自行更新维护 | skill 作者维护 |
| **灵活性** | 高 | 中 |
| **集成难度** | 中（需写适配器） | 低（开箱即用） |
| **成本** | 需要额外 API 调用 | skill 免费/付费 |
| **适用场景** | 特殊需求、深度定制 | 标准场景、快速原型 |

### 2.2 推荐方案

**初期**：使用 ClawHub Skill（快速验证）
**长期**：自建 CrewAI（深度定制）

### 2.3 ClawHub Skill 功能对比详解

#### ClawHub Skill 能完成的工作流

以 **agent-team-orchestration** 为例：

| 功能 | 说明 | 示例 |
|------|------|------|
| ✅ 定义角色 | 预设 Agent 角色 | "你是 Researcher" |
| ✅ 任务生命周期 | 固定流程 | inbox→spec→build→review→done |
| ✅ 交接协议 | 简单的任务传递 | Agent A 完成后交给 Agent B |
| ✅ 审核流程 | 固定审核节点 | build 后自动进入 review |

#### 无法完成的深度工作流

| 场景 | ClawHub Skill | 自建 CrewAI |
|------|---------------|-------------|
| **条件分支** | ❌ 固定流程 | ✅ if/else 根据结果跳转 |
| **动态任务拆分** | ❌ 预设任务数 | ✅ 根据输入动态创建子任务 |
| **循环处理** | ❌ 单次执行 | ✅ while/for 循环直到成功 |
| **外部API集成** | ❌ 只能调用内置工具 | ✅ 任意 REST/GraphQL API |
| **状态机复杂逻辑** | ❌ 线性流程 | ✅ 任意状态机 |
| **自定义工具** | ❌ 无 | ✅ 自己编写 Python 工具 |
| **混合模型调用** | ❌ 单一模型 | ✅ 不同任务用不同模型 |

#### 代码对比示例

**ClawHub Skill (固定流程)**：
```
# 只能是预设的流程
inbox → spec → build → review → done
# 无法改成: inbox → (build OR research) → review → if fail → build
```

**CrewAI (自定义流程)**：
```python
from crewai import Crew, Agent, Task, Process

# 动态创建任务
research = Task(description=f"研究 {topic}", agent=researcher)
if need_code:
    coding = Task(description=f"写 {topic} 代码", agent=coder)
    crew.add_task(coding)

# 条件执行
if result.quality < threshold:
    crew.add_task(improvement)
```

#### 结论

| 需求 | 推荐方案 |
|------|----------|
| 简单协作、角色固定 | ClawHub Skill |
| 需要条件/循环/自定义 | 自建 CrewAI |

搜索 "coding-team-setup" 无结果，最高评分：

| Skill | 评分 |
|-------|------|
| agent-team-orchestration | 1.143 |
| teamwork | 1.004 |
| claude-code-mastery | 1.001 |
| agent-team-kit | 0.991 |

### 2.4 架构选择

| 方案 | 复杂度 | 适用场景 |
|------|--------|----------|
| OpenAI Agents SDK | 低 | 简单任务 |
| CrewAI | 中 | 协作任务 |
| LangGraph | 高 | 复杂流程 |

### 2.2 推荐架构：CrewAI

**核心组件**：
- **Crew**: Agent 团队容器
- **Agent**: 单个智能体（角色、目标、背景）
- **Task**: 具体任务定义
- **Process**: 协作模式（sequential/parallel/hierarchical）

### 2.3 实现步骤

1. **定义 Agent 角色**
   - 研究 Agent
   - 执行 Agent
   - 验证 Agent

2. **定义 Task**
   - 输入解析
   - 子任务拆分
   - 结果汇总

3. **配置 Process**
   - 串行：按顺序执行
   - 并行：同时执行
   - 分层：Manager 管理子Agent

---

## 3. OpenClaw 集成

### 3.1 使用 sessions_spawn
```python
# 创建子 Agent
sessions_spawn(
    agentId="default",
    task="具体任务描述",
    mode="run"
)
```

### 3.2 使用 sessions_send
```python
# Agent 间通信
sessions_send(
    sessionKey="agent-1",
    message="任务结果"
)
```

---

## 4. 参考资料

### 4.1 搜索结果来源

1. **How to Build Multi-Agent Systems: Complete 2026 Guide**
   - DEV Community
   - https://dev.to/eira-wexford/how-to-build-multi-agent-systems-complete-2026-guide-1io6

2. **How to Build A Multi Agent AI System in 2026**
   - Intuz
   - https://www.intuz.com/blog/how-to-build-multi-ai-agent-systems

3. **Guide to Multi-Agent Systems in 2026**
   - Botpress
   - https://botpress.com/blog/multi-agent-systems

4. **Multi-Agent Systems: Complete Guide**
   - Medium - Fraidoon Omarzai
   - https://medium.com/@fraidoonomarzai99/multi-agent-systems-complete-guide-689f241b65c8

5. **Multi-agent system: Frameworks & step-by-step tutorial**
   - n8n Blog
   - https://blog.n8n.io/multi-agent-systems/

6. **Tutorial: Creating a Multi-Agent System with Haystack**
   - Haystack
   - https://haystack.deepset.ai/tutorials/45_creating_a_multi_agent_system

7. **Building Your First Multi-Agent System: A Beginner's Guide**
   - MachineLearningMastery
   - https://machinelearningmastery.com/building-first-multi-agent-system-beginner-guide/

8. **Build a Multi-Agent System (from Scratch)**
   - Manning
   - https://www.manning.com/books/build-a-multi-agent-system-from-scratch

9. **How to Build and Deploy a Multi-Agent AI System with Python and Docker**
   - FreeCodeCamp
   - https://www.freecodecamp.org/news/build-and-deploy-multi-agent-ai-with-python-and-docker

### 4.2 CrewAI 相关

10. **CrewAI - Framework for orchestrating role-playing, autonomous AI agents**
    - GitHub
    - https://github.com/crewAIInc/crewAI

11. **Agent orchestration - OpenAI Agents SDK**
    - OpenAI
    - https://openai.github.io/openai-agents-python/multi_agent/

12. **CrewAI + Groq: High-Speed Agent Orchestration**
    - GroqDocs
    - https://console.groq.com/docs/crewai

13. **The Open Source Multi-Agent Orchestration Framework**
    - CrewAI
    - https://crewai.com/open-source

14. **The Leading Multi-Agent Platform**
    - CrewAI
    - https://crewai.com/

15. **AI agent orchestration with OpenAI Agents SDK**
    - Apify
    - https://blog.apify.com/ai-agent-orchestration/

16. **Building Multi-Agent Systems With CrewAI - A Comprehensive Tutorial**
    - Firecrawl
    - https://www.firecrawl.dev/blog/crewai-multi-agent-systems-tutorial

17. **Mastering AI Agent Orchestration- Comparing CrewAI, LangGraph, and OpenAI Swarm**
    - Medium - Arul
    - https://medium.com/@arulprasathpackirisamy/mastering-ai-agent-orchestration-comparing-crewai-langgraph-and-openai-swarm-8164739555ff

18. **CrewAI: A Practical Guide to Role-Based Agent Orchestration**
    - DigitalOcean
    - https://www.digitalocean.com/community/tutorials/crewai-crash-course-role-based-agent-orchestration

19. **Build your First CrewAI Agents**
    - CrewAI Blog
    - https://blog.crewai.com/getting-started-with-crewai-build-your-first-crew/

---

## 3. CrewAI 详解

### 3.1 什么是 CrewAI

CrewAI 是目前最流行的多 Agent 框架之一，专门用于构建"团队协作"类型的 AI 系统。

**核心思想**：让多个 AI Agent 像真实团队一样工作，每个 Agent 有特定角色和职责。

### 3.2 需要哪些操作

#### 安装
```bash
pip install crewai
```

#### 定义组件

| 组件 | 说明 | 代码示例 |
|------|------|----------|
| **Agent** | 智能体（角色+目标+工具） | `Agent(role="研究员", goal="xxx", tools=[search])` |
| **Task** | 具体任务 | `Task(description="写报告", agent=researcher)` |
| **Crew** | 团队容器 | `Crew(agents=[r1,r2], tasks=[t1,t2])` |
| **Process** | 执行模式 | `Process.sequential` / `Process.hierarchical` |

#### 执行
```python
crew = Crew(agents=agents, tasks=tasks, process=Process.sequential)
result = crew.kickoff()
```

### 3.3 需要哪些文档

| 文档 | 说明 |
|------|------|
| Agent 定义 | 每个 Agent 的角色、目标、背景故事 |
| Task 定义 | 任务描述、预期输出 |
| 工具配置 | Agent 使用的工具（搜索、代码等） |
| 流程配置 | sequential / parallel / hierarchical |

---

## 4. 主流框架对比

### 4.1 框架一览

| 框架 | 特点 | 适用场景 |
|------|------|----------|
| **CrewAI** | 角色-based团队协作 | 快速构建多 Agent 团队 |
| **LangGraph** | 状态管理、图结构 | 复杂有状态工作流 |
| **AutoGen** | 多 Agent 对话 | 对话式多 Agent（⚠️ 已并入 Microsoft Agent Framework） |
| **Microsoft Semantic Kernel** | 企业级集成 | 企业应用、API 集成 |
| **OpenAI Agents SDK** | OpenAI 原生 | 简单任务、OpenAI 生态 |
| **MetaGPT** | 软件开发 | 多 Agent 软件开发 |
| **LlamaIndex** | 数据索引 | RAG + Agent |

### 4.2 推荐选择

| 需求 | 推荐框架 |
|------|----------|
| 快速原型 | CrewAI |
| 复杂状态流 | LangGraph |
| 企业应用 | Semantic Kernel |
| 对话式 | AutoGen / OpenAI Agents SDK |

### 4.3 参考资料

1. **Top 5 Open-Source Agentic AI Frameworks in 2026**
   - AIMultiple
   - https://aimultiple.com/agentic-frameworks

2. **A Detailed Comparison of Top 6 AI Agent Frameworks in 2026**
   - Turing
   - https://www.turing.com/resources/ai-agent-frameworks

3. **15 Best AI Agent Frameworks for Enterprise: Open-Source to Managed (2026)**
   - Prem AI
   - https://blog.premai.io/15-best-ai-agent-frameworks-for-enterprise-open-source-to-managed-2026/

4. **Top 5 Agentic AI Frameworks to Watch in 2026**
   - Future AGI
   - https://futureagi.substack.com/p/top-5-agentic-ai-frameworks-to-watch

5. **Multi-Agent Frameworks Explained for Enterprise AI Systems**
   - Adopt AI
   - https://www.adopt.ai/blog/multi-agent-frameworks

6. **CrewAI vs LangGraph vs AutoGen vs OpenAgents (2026)**
   - OpenAgents
   - https://openagents.org/blog/posts/2026-02-23-open-source-ai-agent-frameworks-compared

7. **Top 5 AI Agent Frameworks In 2026**
   - Intuz
   - https://www.intuz.com/blog/top-5-ai-agent-frameworks-2025

8. **The Best Open Source Frameworks For Building AI Agents in 2026**
   - Firecrawl
   - https://www.firecrawl.dev/blog/best-open-source-agent-frameworks

9. **Comparing Open-Source AI Agent Frameworks**
   - Langfuse
   - https://langfuse.com/blog/2025-03-19-ai-agent-comparison

---

*最后更新: 2026-03-05*

搜索结果（未安装）：

| # | Skill | 评分 |
|---|-------|------|
| 1 | multi-agent-dev-team | 3.387 |
| 2 | agent-team | 3.234 |
| 3 | claude-agent-team-workflows | 3.209 |
| 4 | ai-agent-team-manager | 3.150 |
| 5 | agent-team-builder | 2.856 |
| 6 | ai-agent-helper | 0.985 |
| 7 | unitask-agent | 0.866 |
| 8 | team-builder | 0.861 |
| 9 | agent-training | 0.855 |
| 10 | afrexai-agent-engineering | 0.843 |

---

*最后更新: 2026-03-05*

---

## 6. agent-team-orchestration Skill 研究

### 6.1 安装状态
- ✅ 已安装：`skills/agent-team-orchestration`
- 评分：1.143
- 功能：多Agent团队编排、角色定义、任务生命周期、交接协议、审核流程

### 6.2 核心功能

| 功能 | 支持 | 说明 |
|------|------|------|
| **角色定义** | ✅ | Orchestrator/Builder/Reviewer/Ops |
| **任务生命周期** | ✅ | Inbox→Assigned→In Progress→Review→Done/Failed |
| **交接协议** | ✅ | 必须包含：做了什么+文件路径+验证方法+已知问题+下一步 |
| **审核流程** | ✅ | 每个 artifact 必须有人审核 |
| **异步通信** | ✅ | 共享 artifacts 目录 |
| **不同模型** | ✅ | 每个角色可用不同模型 |
| **不同渠道** | ✅ | 通过 bindings 配置 |

### 6.3 角色与模型选择

| 角色 | 推荐模型 | 说明 |
|------|----------|------|
| Orchestrator | 高级模型 | 判断力、优先级 |
| Builder | 中高级模型 | 代码生成 |
| Reviewer | 高级模型 | 审查质量 |
| Ops | 便宜模型 | 机械工作 |

### 6.4 部署步骤

| 步骤 | 任务 | 动作 | 你需要做 |
|------|------|------|----------|
| 1 | 定义角色 | 对话 | ✅ 告诉我几个Agent、各叫什么 |
| 2 | 选择模型 | 对话 | ✅ 告诉每个用什么模型 |
| 3 | 配置workspace | write | 创建各Agent目录 |
| 4 | 定义任务流 | write | inbox→spec→build→review→done |
| 5 | 配置binding | write | 什么渠道对应什么Agent |
| 6 | 测试 | exec | 重启网关后测试 |

### 6.5 重启时机
- 配置修改后：`openclaw gateway restart`

### 6.6 验证方法
- 看日志：每个 agent 有独立 workspace
- 看 artifacts：不同 agent 产出在不同目录

### 6.7 需要你参与的步骤
- 步骤1：定义角色
- 步骤2：选择模型
- 步骤5：定义 binding
- 步骤6：测试验证

---

## 7. 当前待确认

1. 需要几个 Agent？
2. 每个 Agent 叫什么、做什么？
3. 每个 Agent 用什么模型？
4. 什么渠道/账号对应哪个 Agent？

---

*最后更新: 2026-03-05*

---

## 8. Agent 角色设计（1主+2子）

### 8.1 Orchestrator（主 Agent）

| 项目 | 内容 |
|------|-------|
| **角色** | 指挥官 |
| **职责** | 任务分发、状态跟踪、结果汇总 |
| **模型** | 高级模型（判断力） |
| **工具** | 任务管理、消息发送 |

### 8.2 Builder（子 Agent 1）

| 项目 | 内容 |
|------|-------|
| **角色** | 执行者 |
| **职责** | 执行具体任务、产出 artifact |
| **模型** | 中高级模型 |
| **工具** | 代码、搜索、文件操作 |

### 8.3 Reviewer（子 Agent 2）

| 项目 | 内容 |
|------|-------|
| **角色** | 审核者 |
| **职责** | 质量检查、查漏补缺 |
| **模型** | 高级模型 |
| **工具** | 代码审查、测试验证 |

---

## 9. 错误处理机制

### 9.1 任务失败处理

| 状态 | 处理方式 |
|------|----------|
| **Failed** | 记录原因，转人工或重试 |
| **Blocked** | 通知 Orchestrator，求助 |
| **Timeout** | 超时自动回滚 |

### 9.2 Agent 无响应

| 检测 | 处理 |
|------|------|
| 沉默超时 | 假设卡住，触发提醒 |
| 3次重试失败 | 升级到人工 |

### 9.3 错误升级

```
Level 1: Agent 自己处理
    ↓ 无法解决
Level 2: 通知 Orchestrator
    ↓ 无法解决  
Level 3: 转人工（你）
```

### 9.4 重试策略

| 失败次数 | 动作 |
|----------|------|
| 1 | 重试一次 |
| 2 | 换模型重试 |
| 3 | 升级处理 |

---

## 10. 工作流程图

```
用户消息
    ↓
Orchestrator（主）
    ↓
    ├→ [成功] → Builder 执行
    │           ├→ [成功] → Reviewer 审核
    │           │             ├→ [通过] → 汇总结果
    │           │             └→ [失败] → 返回修改
    │           └→ [失败] → 重试/升级
    ↓
返回结果
```

---

*最后更新: 2026-03-05*
