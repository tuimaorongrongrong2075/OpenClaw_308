# TOOLS.md - Local Notes
> 最后更新: 2026-02-27

## 账号与平台（环境变量）

### 邮箱
| 类型 | 环境变量 | 检查脚本 |
|------|----------|----------|
| 工作 QQ | `QQMAIL_WORK_USER`, `QQMAIL_WORKER_AUTH_CODE` | `scripts/mail/check_qqmail.py` |
| 个人 QQ | `QQMAIL_PERSONAL_USER`, `QQMAIL_PERSONAL_AUTH_CODE` | `scripts/mail/check_qqmail_personal.py` |

### 平台
| 平台 | 环境变量 | 说明 |
|------|----------|------|
| GitHub | `GITHUB_USERNAME`, `GITHUB_TOKEN` | 仓库: tuimaorongrongrong2075/OpenClaw_201 |
| Feishu | `FEISHU_OPEN_ID` | 用户 ID |
| Moltbook | `MOLTBOOK_API_KEY` | XiaoXingBot |
| Brave Search | `BRAVE_API_KEY` | 网页搜索 |

---

## 技能 Skills

| 技能 | 功能 | 位置 |
|------|------|------|
| frontend | 前端设计 | skills/frontend/ |
| webpage-screenshot | 网页截图 | skills/webpage-screenshot/ |
| code | 代码开发 | skills/code/ |
| test-runner | 测试运行 | skills/test-runner/ |
| markdown-converter | 文档转换 | skills/markdown-converter/ |
| feishu-doc | 飞书文档 | skills/feishu-doc/ |
| screenshot | 屏幕截图 | skills/screenshot/ |
| obsidian-git-sync | Obsidian 同步 | skills/obsidian-git-sync/ |

---

## 截图工具

| 工具 | 命令 | 用途 |
|------|------|------|
| Puppeteer | `node scripts/screenshot.js <URL> <输出文件>` | 网页截图（首选） |

---

## 脚本位置

### 常用脚本
| 脚本 | 功能 |
|------|------|
| `scripts/system/health_check.sh` | 系统健康检查 |
| `scripts/system/check_env.sh` | 检查环境变量 |
| `scripts/system/daily_summary.sh` | 每日总结 |
| `scripts/system/cleanup_old_sessions.sh` | 清理旧会话 |
| `scripts/system/normalize_markdown.py` | 文档规范化 |

### 邮件脚本
| 脚本 | 功能 |
|------|------|
| `scripts/mail/check_gmail.py` | 检查 Gmail |
| `scripts/mail/check_qqmail.py` | 检查工作 QQ 邮箱 |
| `scripts/mail/check_qqmail_personal.py` | 检查个人 QQ 邮箱 |

---

## 项目路径

| 项目 | 路径 |
|------|------|
| 备忘录 | project/memo/ |
| 记忆系统 | memory/ |
| 日常文档 | docs/ |
| 正在调研 | analysis/ |
| 定时任务输出 | daily/ |

---

## Cron 定时任务配置

**重要**：所有 cron 任务必须使用 `--tz "Asia/Shanghai"` 参数！

### 正确格式
```bash
# ✅ 正确：添加时区参数
openclaw cron add \
  --name "任务名" \
  --cron "0 9 * * *" \
  --tz "Asia/Shanghai" \
  --message "任务内容" \
  --channel feishu \
  --to ou_xxx

# ❌ 错误：没有时区参数（会使用UTC）
openclaw cron add --name "任务名" --cron "0 9 * * *" ...
```

### 当前任务列表（上海时间）

| 任务 | 时间 | 备注 |
|------|------|------|
| 心跳确认 | 每30分钟 | 自动 |
| Moltbook发帖-早 | 08:00 | --tz Asia/Shanghai |
| 邮箱检查-早 | 09:00 | --tz Asia/Shanghai |
| 看板数据更新 | 11:00 | --tz Asia/Shanghai |
| 邮箱检查-下午 | 14:00 | --tz Asia/Shanghai |
| 每日运动提醒 | 15:30 | --tz Asia/Shanghai |
| Moltbook发帖-晚 | 16:00 | --tz Asia/Shanghai |
| 邮箱检查-晚 | 17:00 | --tz Asia/Shanghai |
| GitHub Sync | 22:00 | --tz Asia/Shanghai |
| 每日总结 | 23:00 | --tz Asia/Shanghai |
| 记忆整理(周日) | 22:00 | --tz Asia/Shanghai |

### 常见错误
1. 忘记加 `--tz "Asia/Shanghai"` → 按 UTC 执行
2. 删除旧任务时任务正在运行 → 等待完成后自动失效

---

*此文件记录当前配置的环境变量、脚本和技能位置*
