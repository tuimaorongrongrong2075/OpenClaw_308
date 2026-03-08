# SCRIPT_AUDIT.md - 代码检查报告

> 最后更新: 2026-02-17

---

## 🐛 Bug 列表

### 1. 【严重】moltbook_heartbeat.sh - 调用已删除的脚本
**文件**: `scripts/moltbook_heartbeat.sh`  
**位置**: 第 66 行

```bash
# 同步看板数据
echo "📊 同步看板数据..."
bash /root/.openclaw/workspace/scripts/sync_dashboard.sh  # ← dashboard 已删除！
```

**问题**: 看板(`docs/dashboard/`)已删除，但此脚本仍尝试调用 `sync_dashboard.sh`  
**影响**: 每次 Moltbook 心跳会报错  
**修复**: 删除这行代码或注释掉

---

### 2. 【严重】sync_dashboard.sh - 目录不存在
**文件**: `scripts/sync_dashboard.sh`  
**位置**: 多处

```bash
DASHBOARD_DIR="$WORKSPACE/docs/dashboard"
DASHBOARD_NETLIFY_DIR="$WORKSPACE/docs/dashboard_netlify"
```

**问题**: 这两个目录已在 GitHub 上删除  
**影响**: 脚本运行时会产生"目录不存在"错误  
**建议**: 
- 方案 A: 删除整个 `sync_dashboard.sh` 脚本（推荐，看板已不用）
- 方案 B: 修改脚本为其他用途

---

### 3. 【中等】check_gmail.py - 日志路径错误
**文件**: `scripts/check_gmail.py`  
**位置**: 第 17 行

```python
LOG_FILE = "/root/.openclaw/workspace/memory/gmail_check.log"
```

**问题**: 日志文件应该放在 `Log/` 目录，而不是 `memory/`  
**影响**: 日志分散，不符合新的目录结构  
**修复**:
```python
LOG_FILE = "/root/.openclaw/workspace/Log/gmail_check.log"
```

---

### 4. 【低】generate_ai_digest.py - API Key 硬编码
**文件**: `scripts/generate_ai_digest.py`  
**位置**: 第 12 行

```python
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "[API_KEY已移除]")
```

**问题**: 有默认硬编码的 API Key  
**影响**: 安全风险，虽然会从环境变量读取，但默认值仍存在代码中  
**修复**:
```python
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY 环境变量未设置")
```

---

## ⚠️ 优化建议

### 5. 【优化】cleanup_old_sessions.sh - 缺少错误处理
**文件**: `scripts/cleanup_old_sessions.sh`

**问题**: 如果 `sessions.json` 格式异常，Python 代码会崩溃  
**建议**: 添加 try-except 错误处理

---

### 6. 【优化】moltbook_heartbeat.sh - 评论内容重复
**文件**: `scripts/moltbook_heartbeat.sh`  
**位置**: 第 26-37 行

**问题**: 每次生成的评论从固定的 5 个模板中选择，容易被识别为机器人  
**建议**: 增加更多模板或引入随机组合

---

### 7. 【优化】多个脚本缺少超时处理
**文件**: `check_gmail.py`, `moltbook_heartbeat.sh` 等

**问题**: 网络请求没有超时设置，可能挂起  
**建议**: 
- Python: `imaplib.IMAP4_SSL(..., timeout=30)`
- Bash: `curl --max-time 30 ...`

---

## 🗑️ 可删除的脚本

| 脚本 | 原因 |
|------|------|
| `sync_dashboard.sh` | 看板已删除，脚本无用 |
| `generate_missing_dates.sh` | 看板相关，无用 |

---

## ✅ 代码质量良好的脚本

- `cleanup_old_sessions.sh` - 逻辑清晰，功能完整
- `health_check.sh` - 检查全面
- `jocko_workout.sh` - 简单有效
- `startup.sh` - 启动流程完整
- `sync_github.sh` - 同步功能正常

---

## 🔧 修复优先级

| 优先级 | 问题 | 修复时间 |
|--------|------|----------|
| 🔴 P0 | moltbook_heartbeat.sh 调用已删除脚本 | 2分钟 |
| 🔴 P0 | sync_dashboard.sh 目录不存在 | 1分钟(删除) |
| 🟡 P1 | check_gmail.py 日志路径 | 1分钟 |
| 🟡 P1 | generate_ai_digest.py API Key | 2分钟 |
| 🟢 P2 | 增加超时处理 | 10分钟 |
| 🟢 P2 | 优化错误处理 | 15分钟 |

---

## 📝 一键修复脚本

```bash
#!/bin/bash
# 一键修复脚本问题

echo "🔧 开始修复脚本问题..."

# 1. 修复 moltbook_heartbeat.sh - 删除 dashboard 同步
echo "1️⃣ 修复 moltbook_heartbeat.sh..."
sed -i '/同步看板数据/,/sync_dashboard.sh/d' /root/.openclaw/workspace/scripts/moltbook_heartbeat.sh

# 2. 删除无用的 sync_dashboard.sh
echo "2️⃣ 删除 sync_dashboard.sh..."
rm -f /root/.openclaw/workspace/scripts/sync_dashboard.sh

# 3. 修复 check_gmail.py 日志路径
echo "3️⃣ 修复 check_gmail.py..."
sed -i 's|/memory/gmail_check.log|/Log/gmail_check.log|g' /root/.openclaw/workspace/scripts/check_gmail.py

# 4. 修复 generate_ai_digest.py API Key
echo "4️⃣ 修复 generate_ai_digest.py..."
sed -i 's|os.environ.get("GEMINI_API_KEY", ".*")|os.environ.get("GEMINI_API_KEY")|g' /root/.openclaw/workspace/scripts/generate_ai_digest.py

echo "✅ 修复完成！"
echo "请检查修改后提交到 GitHub:"
echo "  cd /root/.openclaw/workspace"
echo "  git add -A && git commit -m '修复脚本bug' && git push"
```

---

*检查人: 小猩 🦧*  
*时间: 2026-02-17*
