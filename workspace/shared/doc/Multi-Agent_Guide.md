# 多 Agent 协同配置指南

> 最后更新: 2026-02-20  
> 作者: 小猩 🦧

---

## 📖 概述

OpenClaw 支持多 Agent 协同工作，通过以下方式实现：
1. **sessions_spawn** - 创建子 Agent 会话
2. **消息传递** - Agent 间通信（sessions_send）
3. **Cron 定时任务** - 独立的 Agent 任务
4. **并行处理** - 多个 Agent 同时工作

---

## 🚀 方式 1: 使用 sessions_spawn 创建子 Agent

### 基本用法

```python
# 通过工具调用创建子 Agent
sessions_spawn(
    task="研究这个主题并给我报告",
    agentId="main",              # 使用哪个 agent
    model="moonshot/kimi-k2.5",  # 可选：指定模型
    thinking="on",               # 可选：启用推理模式
    timeoutSeconds=300           # 可选：超时时间
)
```

### 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `task` | 子 Agent 的任务描述 | 必填 |
| `agentId` | 使用的 agent ID | main |
| `label` | 子会话标签（方便识别） | 自动生成 |
| `model` | 指定模型 | 继承主会话 |
| `thinking` | 推理模式（on/off/stream） | off |
| `runTimeoutSeconds` | 子 agent 运行超时 | 600 |
| `cleanup` | 完成后是否删除会话 | delete |

### 实际示例

```python
# 示例 1: 简单任务
sessions_spawn(
    task="分析这份文档的要点，生成摘要",
    label="文档分析"
)

# 示例 2: 复杂任务（指定模型）
sessions_spawn(
    task="深入研究这个技术话题，写一篇详细教程",
    model="glmcode/glm-4.7",
    thinking="on",
    label="技术研究"
)

# 示例 3: 保留会话（用于后续参考）
sessions_spawn(
    task="监控这个指标，每小时报告一次",
    cleanup="keep",
    label="监控任务"
)
```

---

## 💬 方式 2: Agent 间通信（sessions_send）

### 发送消息到另一个会话

```python
sessions_send(
    sessionKey="agent:main:sub:abc123",  # 目标会话
    message="这是从主会话发来的消息"
)
```

### 使用标签发送

```python
sessions_send(
    label="文档分析",
    message="继续之前的分析工作"
)
```

---

## ⏰ 方式 3: Cron 定时任务

### 创建独立 Agent 任务

```python
cron(
    action="add",
    job={
        "sessionTarget": "isolated",  # 隔离会话
        "schedule": {
            "kind": "cron",
            "expr": "0 9 * * *",      # 每天早上 9 点
            "tz": "Asia/Shanghai"
        },
        "payload": {
            "kind": "agentTurn",
            "message": "早上好！请执行每日检查任务",
            "thinking": "on"
        }
    }
)
```

### 一次性提醒

```python
cron(
    action="add",
    job={
        "sessionTarget": "isolated",
        "schedule": {
            "kind": "at",
            "at": "2026-02-21T09:00:00+08:00"
        },
        "payload": {
            "kind": "agentTurn",
            "message": "提醒：修改 QQ 邮箱授权码"
        }
    }
)
```

### 周期性任务

```python
# 每 4 小时执行一次
cron(
    action="add",
    job={
        "sessionTarget": "isolated",
        "schedule": {
            "kind": "every",
            "everyMs": 14400000  # 4 * 60 * 60 * 1000
        },
        "payload": {
            "kind": "agentTurn",
            "message": "执行周期性健康检查"
        }
    }
)
```

---

## 🔄 方式 4: 并行处理

### 同时创建多个子 Agent

```python
# 任务 1
sessions_spawn(
    task="研究技术方案 A",
    label="方案A研究"
)

# 任务 2
sessions_spawn(
    task="研究技术方案 B",
    label="方案B研究"
)

# 任务 3
sessions_spawn(
    task="研究技术方案 C",
    label="方案C研究"
)

# 主 Agent 等待所有子 Agent 完成后汇总
```

### 限制并发数

在 `openclaw.json` 中配置：

```json
{
  "agents": {
    "defaults": {
      "maxConcurrent": 4,        # 主 Agent 最大并发
      "subagents": {
        "maxConcurrent": 8       # 子 Agent 最大并发
      }
    }
  }
}
```

---

## 📋 管理子 Agent 会话

### 查看所有会话

```python
sessions_list(
    kinds=["subagent"],          # 只显示子 Agent
    activeMinutes=60,            # 最近 60 分钟活跃的
    limit=10
)
```

### 获取会话历史

```python
sessions_history(
    sessionKey="agent:main:sub:abc123",
    limit=50,
    includeTools=true
)
```

### 删除会话

```python
# 通过 sessionKey 删除
process(
    action="remove",
    sessionId="abc123"
)
```

---

## 🎯 实战案例

### 案例 1: 研究型任务（并行研究）

**场景**: 需要研究多个技术方案并汇总

```python
# 主 Agent 分配任务
sessions_spawn(task="研究方案 A 的优缺点", label="方案A")
sessions_spawn(task="研究方案 B 的优缺点", label="方案B")
sessions_spawn(task="研究方案 C 的优缺点", label="方案C")

# 等待所有子 Agent 完成...
# 然后汇总所有研究结果，生成对比报告
```

### 案例 2: 监控型任务（定时检查）

**场景**: 每小时检查邮件并报告

```python
cron(
    action="add",
    job={
        "sessionTarget": "isolated",
        "schedule": {"kind": "every", "everyMs": 3600000},
        "payload": {
            "kind": "agentTurn",
            "message": "检查所有邮箱，有重要邮件立即报告"
        }
    }
)
```

### 案例 3: 协作型任务（流水线）

**场景**: 多个 Agent 协作完成复杂任务

```python
# 步骤 1: Agent A 收集数据
result_a = sessions_spawn(
    task="收集相关数据",
    label="数据收集"
)

# 步骤 2: Agent B 分析数据
result_b = sessions_spawn(
    task=f"分析这些数据：{result_a}",
    label="数据分析"
)

# 步骤 3: Agent C 生成报告
result_c = sessions_spawn(
    task=f"基于分析结果生成报告：{result_b}",
    label="报告生成"
)
```

---

## ⚙️ 配置优化

### 提高子 Agent 性能

```json
{
  "agents": {
    "defaults": {
      "subagents": {
        "maxConcurrent": 16,          # 增加并发数
        "model": {
          "primary": "glmcode/glm-4.7"  # 使用更快的模型
        }
      }
    }
  }
}
```

### 内存管理

```json
{
  "agents": {
    "defaults": {
      "compaction": {
        "mode": "safeguard",          # 安全模式
        "maxTokens": 100000           # 最多保留 10 万 tokens
      }
    }
  }
}
```

---

## 🚨 注意事项

### 1. 资源限制
- 子 Agent 会消耗 API 配额
- 注意 `maxConcurrent` 限制，避免过载

### 2. 会话清理
- 默认 `cleanup="delete"`，任务完成后自动删除
- 需要保留结果的，设置 `cleanup="keep"`

### 3. 错误处理
- 子 Agent 失败不会影响主会话
- 使用 `timeoutSeconds` 防止任务挂起

### 4. 安全性
- 子 Agent 继承主会话的权限
- 隔离会话（isolated）更安全，但无法访问主会话上下文

---

## 📊 监控与调试

### 查看运行中的子 Agent

```python
sessions_list(
    kinds=["subagent"],
    activeMinutes=5
)
```

### 检查子 Agent 状态

```python
process(
    action="list"
)
```

### 获取子 Agent 输出

```python
sessions_history(
    sessionKey="agent:main:sub:abc123",
    includeTools=true
)
```

---

## 🔗 相关工具

| 工具 | 用途 |
|------|------|
| `sessions_spawn` | 创建子 Agent |
| `sessions_send` | 发送消息到其他会话 |
| `sessions_list` | 列出所有会话 |
| `sessions_history` | 获取会话历史 |
| `process` | 管理运行中的会话 |
| `cron` | 定时任务调度 |

---

## 📚 参考文档

- [OpenClaw 配置详解](./Openclaw_Config.md)
- [恢复指南](./Restore_Guide.md)
- [官方文档](https://docs.openclaw.ai)

---

*创建: 2026-02-20*  
*维护: 小猩 🦧*
