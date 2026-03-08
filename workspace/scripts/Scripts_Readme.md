# Scripts 目录说明

> 本目录包含小猩自动化任务的所有脚本
> 最后更新: 2026-03-03

---

## 📁 目录结构

```
scripts/
├── cron/              # 定时任务（Dashboard 数据更新）
│   ├── feishu_doc_full.py
│   ├── feishu_doc_helper.py
│   ├── update_agent_projects.py
│   ├── update_ai_news ├── update_dashboard_all.sh
│   ├── update_github_trending.py
│   ├── update_server_stats.py
│  
├── mail/              # 邮件管理
│   ├── check_gmail.py
│   ├── check_qqmail.py
│   ├── check_qqmail_personal.py
│   ├── list_unread.py
│   ├── send_email.py
│   ├── test_all_mail.sh
│   ├── analyze_invoice_emails.py
│   ├── clean_gmail_marketing.py
│   ├── clean_gmail_security.py
│   ├── clean_gmail_otp.py
│   ├── clean_qqmail_ad.py
│   └── clean_qqmail_otp.py
├── export/           # 收藏导出
│   ├── bilibili/
│   │   └── test_bilibili_api.py
│   ├── bilibili_favorites_export.py
│   └── get/
│       └── parse_getnotes.py
├── system/           # 系统维护
│   ├── health_check.sh
│   ├── check_env.sh
│   ├── load_env.sh
│   ├── daily_summary.sh
│   ├── cleanup_old_sessions.sh
│   ├── restore_xiaoxing.sh
│   ├── restore-cron.sh
│   ├── audit_scripts.sh
│   ├── backup_sessions.sh
│   └── run_with_env_check.sh
├── reminder/         # 提醒
│   └── jocko_workout.sh
├── logs/             # 日志目录（不提交）
├── startup.sh        # 启动脚本
├── normalize_scripts.py
├── normalize_markdown.py
└── Scripts_Readme.md

```

---

## 📋 功能说明

### ⏰ cron/ - 定时任务

| 脚本 | 功能 |
|------|------|
| `update_dashboard_all.sh` | 更新 Dashboard 所有数据 |
| `update_agent_projects.py` | 更新 Agent 项目数据 |
| `update_ai_news.py` | 更新 AI 新闻 |
| `update_github_trending.py` | 更新 GitHub Trending |
| `update_server_stats.py` | 更新服务器状态 |
| `feishu_doc_full.py` | 飞书文档完整操作 |
| `feishu_doc_helper.py` | 飞书文档辅助工具 |

### 📧 mail/ - 邮件管理

| 脚本 | 功能 |
|------|------|
| `check_gmail.py` | 检查 Gmail 未读邮件 |
| `check_qqmail.py` | 检查工作 QQ 邮箱 |
| `check_qqmail_personal.py` | 检查个人 QQ 邮箱 |
| `list_unread.py` | 列出所有邮箱未读邮件 |
| `send_email.py` | 发送邮件 |
| `test_all_mail.sh` | 测试所有邮箱配置 |
| `analyze_invoice_emails.py` | 分析发票邮件 |
| `clean_gmail_marketing.py` | 清理 Gmail 营销邮件 |
| `clean_gmail_security.py` | 清理 Gmail 安全提醒 |
| `clean_gmail_otp.py` | 清理 Gmail 验证码 |
| `clean_qqmail_ad.py` | 清理 QQ 邮箱广告 |
| `clean_qqmail_otp.py` | 清理 QQ 邮箱验证码 |

### 📥 export/ - 收藏导出

| 脚本 | 功能 |
|------|------|
| `bilibili_favorites_export.py` | 导出 B 站收藏到 Obsidian |
| `bilibili/test_bilibili_api.py` | B 站 API 测试 |
| `get/parse_getnotes.py` | 解析 Get 笔记 |


### ⚙️ system/ - 系统维护

| 脚本 | 功能 |
|------|------|
| `health_check.sh` | 系统健康检查 |
| `check_env.sh` | 检查环境变量配置 |
| `load_env.sh` | 加载环境变量 |
| `daily_summary.sh` | 生成每日总结 |
| `cleanup_old_sessions.sh` | 清理旧会话 |
| `restore_xiaoxing.sh` | 一键恢复记忆 |
| `restore-cron.sh` | 恢复定时任务 |
| `audit_scripts.sh` | 脚本审计检查 |
| `backup_sessions.sh` | 备份会话数据 |
| `run_with_env_check.sh` | 带环境检查的脚本执行 |
| `normalize_scripts.py` | 规范化脚本格式 |
| `normalize_markdown.py` | 规范化 Markdown 文档 |

### ⏰ reminder/ - 提醒

| 脚本 | 功能 |
|------|------|
| `jocko_workout.sh` | 健身提醒 |

### 🚀 根目录脚本

| 脚本 | 功能 |
|------|------|
| `startup.sh` | OpenClaw 启动初始化 |

---

## ⚠️ 已删除脚本

以下脚本已被删除（功能已被 Skills 替代或不再需要）：
- ~~`sync_github.sh`~~ → 使用 git 命令行替代
- ~~`screenshot.sh`~~ → 使用 screenshot skill
- ~~`web_screenshot.sh`~~ → 使用 webpage-screenshot skill
- ~~`url_screenshot.sh`~~ → 使用 webpage-screenshot skill
- ~~`generate_screenshot_summaries.sh`~~ → 已过时
- ~~`wechat_favorites_export.py`~~ → 已删除
- ~~`disable_crons.sh`~~ → 已删除
- ~~`disable_all_cron.sh`~~ → 已删除
- ~~`scripts/digest/`~~ → 整个目录已删除（RSS 订阅功能）

---

## 📝 更新日志

- **2026-03-03**: 新增 `cron/` 目录，移除 `disable_crons.sh`/`disable_all_cron.sh`，更新目录结构

---

*最后更新: 2026-03-03*
*🦧 小猩*
