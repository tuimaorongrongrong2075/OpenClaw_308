# OPENCLAW_CONFIG.md - OpenClaw 配置详解

> 最后更新: 2026-02-17

---

## 📋 配置总览

```
openclaw.json
├── meta              # 元数据
├── wizard            # 安装向导记录
├── models            # AI 模型配置 ⭐关键
├── agents            # Agent 默认配置 ⭐关键
├── messages          # 消息行为
├── commands          # 命令设置
├── gateway           # 网关配置 ⭐关键
├── skills            # 技能安装
├── plugins           # 插件配置
└── channels          # 通讯频道配置 ⭐关键
```

---

## 🔐 敏感信息说明

⚠️ **此文件包含以下敏感信息，请妥善保管**:
- API Keys (MiniMax, Moonshot, GLM)
- Feishu App Secret
- Gateway Auth Token

**备份建议**: 
```bash
# 加密备份
gpg -c ~/.openclaw/openclaw.json
```

---

## 🤖 1. Models - AI 模型配置

### 当前配置的模型提供商

| 提供商 | 状态 | 用途 |
|--------|------|------|
| **MiniMax** | ✅ 配置 | 备用模型 |
| **Moonshot** | ✅ 配置 | **当前主模型** (Kimi K2.5) |
| **GLMCode** | ✅ 配置 | 备用模型 (智谱) |

### 配置结构
```json
{
  "models": {
    "mode": "merge",           // 合并模式
    "providers": {
      "minimax": {
        "baseUrl": "https://api.minimaxi.com/anthropic",
        "apiKey": "sk-xxx",     // MiniMax API Key
        "api": "anthropic-messages",
        "models": ["MiniMax-M2.1", "MiniMax-M2.1-lightning", "MiniMax-M2"]
      },
      "moonshot": {
        "baseUrl": "https://api.moonshot.cn/v1",
        "apiKey": "sk-xxx",     // Moonshot API Key
        "api": "openai-completions",
        "models": ["kimi-k2.5", "kimi-k2-thinking", ...]
      },
      "glmcode": {
        "baseUrl": "https://open.bigmodel.cn/api/anthropic",
        "apiKey": "xxx",        // 智谱 API Key
        "api": "anthropic-messages",
        "models": ["glm-4.7", "glm-5", "glm-4.5", ...]
      }
    }
  }
}
```

### 模型参数说明
| 参数 | 说明 | 示例值 |
|------|------|--------|
| `contextWindow` | 上下文窗口大小 | 200000 (200K tokens) |
| `maxTokens` | 单次回复最大 tokens | 8192 |
| `reasoning` | 是否启用推理模式 | false |

---

## 👤 2. Agents - Agent 默认配置

### 当前配置
```json
{
  "agents": {
    "defaults": {
      "workspace": "/root/.openclaw/workspace",  // 工作目录 ⭐关键
      "compaction": {
        "mode": "safeguard"                      // 内存压缩模式
      },
      "maxConcurrent": 4,                         // 最大并发会话数
      "subagents": {
        "maxConcurrent": 8                        // 子代理最大并发
      },
      "model": {
        "primary": "moonshot/kimi-k2.5"          // 主模型设置 ⭐关键
      }
    }
  }
}
```

### 关键参数
| 参数 | 说明 | 当前值 |
|------|------|--------|
| `workspace` | 技能、记忆、脚本存放目录 | `/root/.openclaw/workspace` |
| `compaction.mode` | 内存压缩策略 | `safeguard` (安全模式) |
| `maxConcurrent` | 同时处理的会话数 | 4 |
| `primary` | 默认使用的模型 | `moonshot/kimi-k2.5` |

---

## 🌐 3. Gateway - 网关配置

### 当前配置
```json
{
  "gateway": {
    "port": 18789,                    // 网关端口
    "mode": "local",                  // 运行模式
    "bind": "loopback",               // 绑定地址
    "controlUi": {
      "allowInsecureAuth": false      // 是否允许不安全认证
    },
    "auth": {
      "mode": "token",
      "token": "903085a1cc..."        // 网关认证令牌 ⭐关键
    },
    "tailscale": {
      "mode": "off",                  // Tailscale VPN
      "resetOnExit": false
    }
  }
}
```

### 访问地址
- **本地**: http://127.0.0.1:18789/
- **远程**: 需配置 Tailscale 或反向代理

---

## 💬 4. Channels - 通讯频道配置

### 当前启用的频道

| 频道 | 状态 | 配置 |
|------|------|------|
| **Feishu** | ✅ 启用 | AppId + AppSecret |
| QQ Bot | ✅ 启用 | 未配置详情 |
| DingTalk | ✅ 启用 | 未配置详情 |
| WeCom | ✅ 启用 | 未配置详情 |
| ADP | ✅ 启用 | 未配置详情 |

### Feishu 详细配置
```json
{
  "channels": {
    "feishu": {
      "enabled": true,
      "appId": "cli_a9f45496dd789bd6",      // 飞书应用 ID
      "appSecret": "XETGvwKa9Iom8brj...",   // 飞书应用密钥 ⭐关键
      "domain": "feishu",
      "groupPolicy": "open"                  // 群组策略
    }
  }
}
```

### 群组策略说明
| 策略 | 说明 |
|------|------|
| `open` | 任何群组成员可触发 |
| `allowlist` | 仅白名单用户可触发 |
| `mention` | 需要 @ 提及才响应 |

---

## 🔌 5. Plugins - 插件配置

### 已安装的插件

| 插件 | 版本 | 安装路径 |
|------|------|----------|
| qqbot | 1.4.4 | `~/.openclaw/extensions/qqbot` |
| ddingtalk | 1.2.0 | `~/.openclaw/extensions/ddingtalk` |
| wecom | 2026.2.5 | `~/.openclaw/extensions/wecom` |
| adp-openclaw | 0.0.24 | `~/.openclaw/extensions/adp-openclaw` |

### 配置结构
```json
{
  "plugins": {
    "entries": {
      "feishu": { "enabled": true },
      "qqbot": { "enabled": true },
      "ddingtalk": { "enabled": true },
      "wecom": { "enabled": true },
      "adp-openclaw": { "enabled": true }
    },
    "installs": {
      "qqbot": {
        "source": "npm",
        "spec": "@sliverp/qqbot@latest",
        "installPath": "/root/.openclaw/extensions/qqbot",
        "version": "1.4.4"
      }
      // ... 其他插件
    }
  }
}
```

---

## ⚙️ 6. 其他配置

### Messages - 消息行为
```json
{
  "messages": {
    "ackReactionScope": "group-mentions"  // 只在被@时响应群消息
  }
}
```

### Commands - 命令设置
```json
{
  "commands": {
    "native": "auto",        // 原生命令模式
    "nativeSkills": "auto"   // 技能命令模式
  }
}
```

### Skills - 技能安装
```json
{
  "skills": {
    "install": {
      "nodeManager": "npm"   // 使用 npm 安装技能
    }
  }
}
```

### Meta - 元数据
```json
{
  "meta": {
    "lastTouchedVersion": "2026.2.9",       // 最后修改版本
    "lastTouchedAt": "2026-02-13T09:12:06.851Z"  // 最后修改时间
  },
  "wizard": {
    "lastRunAt": "2026-02-11T09:47:49.711Z", // 向导最后运行
    "lastRunVersion": "2026.2.9",
    "lastRunCommand": "onboard",             // onboard = 首次安装
    "lastRunMode": "local"
  }
}
```

---

## 📝 常用配置命令

### 查看完整配置
```bash
openclaw config.get
```

### 修改配置 (安全方式)
```bash
# 修改主模型
openclaw config.patch '{"agents":{"defaults":{"model":{"primary":"moonshot/kimi-k2.5"}}}}'

# 重启生效
openclaw gateway restart
```

### 查看模型列表
```bash
openclaw models list
```

### 查看频道状态
```bash
openclaw status
```

---

## 🔄 配置变更历史

| 时间 | 变更 | 说明 |
|------|------|------|
| 2026-02-11 | 初始配置 | onboard 安装完成 |
| 2026-02-13 | 模型切换 | GLM-4.7 → MiniMax → Kimi K2.5 |
| 2026-02-17 | 添加会话清理 | cleanup_old_sessions 定时任务 |

---

## 🚨 恢复配置

如果配置丢失:

```bash
# 方式1: 从备份恢复
cp ~/openclaw_config_backup.json ~/.openclaw/openclaw.json

# 方式2: 重新配置
openclaw configure

# 重启网关
openclaw gateway restart
```

---

## 📁 相关文件

| 文件 | 说明 |
|------|------|
| `~/.openclaw/openclaw.json` | 主配置文件 (本文件) |
| `~/.bashrc` | 环境变量 (API Keys) |
| `~/.openclaw/workspace/` | 工作目录 (技能、脚本、记忆) |

---

*创建: 2026-02-17*  
*维护: 小猩 🦧*
