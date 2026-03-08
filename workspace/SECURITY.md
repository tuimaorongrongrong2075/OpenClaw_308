# SECURITY.md - 安全配置说明

**小猩的敏感信息安全存储**

---

## 🔐 环境变量存储位置

所有敏感信息存储在 `~/.bashrc`（**不在workspace中**）：

```bash
# ~/.bashrc (不在git同步范围内）
export GMAIL_USER="your_email@gmail.com"
export GMAIL_APP_PASSWORD="your_app_password"
export MOLTBOOK_API_KEY="your_moltbook_api_key"
export GITHUB_TOKEN="your_github_token"
export FEISHU_USER="your_feishu_user_id"
```

---

## 🚫 不同步的文件

以下文件已在 `.gitignore` 中排除：
- `*.env`, `.env.*` - 环境变量文件
- `*_secret*`, `*_password*`, `*_token*`, `*_key*` - 敏感信息文件
- `*.log` - 日志文件
- `memory/gmail_*.log`, `memory/gmail_state.json` - 邮件状态文件

---

## 🔄 重启后使用

每次OpenClaw重启后，运行：

```bash
bash /root/.openclaw/workspace/scripts/startup.sh
```

该脚本会：
1. 从 `~/.bashrc` 加载环境变量
2. 配置Git认证（使用环境变量中的token）
3. 测试Gmail连接

---

## 📝 敏感信息使用

### Gmail检查
```python
GMAIL_USER = os.environ.get("GMAIL_USER")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")
```

### Moltbook API
```python
MOLTBOOK_API_KEY = os.environ.get("MOLTBOOK_API_KEY")
```

### GitHub Token
```bash
git remote set-url origin "https://${GITHUB_TOKEN}@github.com/user/repo.git"
```

---

## ✅ 安全检查清单

- [x] 敏感信息移至 `~/.bashrc`
- [x] workspace脚本从环境变量读取
- [x] `.gitignore` 排除敏感文件
- [x] 测试启动脚本正常工作
- [x] 已推送到GitHub（无敏感信息）

---

*最后更新：2026-02-13*
*安全配置完成 🦧*
