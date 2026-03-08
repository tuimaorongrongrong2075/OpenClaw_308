# RESTORE_GUIDE.md - 小猩失忆恢复指南

> 最后更新: 2026-02-18（已添加QQ邮箱恢复步骤）

---

## 📋 恢复清单总览

| 优先级 | 项目 | 位置 | 大小 |
|--------|------|------|------|
| 🔴 P0 | 身份文件 | workspace/*.md | ~12KB |
| 🔴 P0 | 长期记忆 | memory/*.md | ~50KB |
| 🔴 P0 | OpenClaw配置 | ~/.openclaw/ | ~50KB |
| 🟡 P1 | 技能文件 | workspace/skills/ | ~500KB |
| 🟡 P1 | 自动化脚本 | workspace/scripts/ | ~100KB |
| 🟢 P2 | 环境变量 | ~/.bashrc | ~1KB |
| 🟢 P2 | 定时任务 | cron list | - |
| ⚪ P3 | 日志/缓存 | 可重建 | - |

---

## 🚨 第零步: 紧急备份

### 当前完整备份命令
```bash
# 1. GitHub 自动同步 (已配置)
cd /root/.openclaw/workspace
git add -A
git commit -m "[$(date +%Y-%m-%d)] 完整备份 🦧"
git push origin main --force

# 2. 手动备份配置文件
cp ~/.openclaw/openclaw.json ~/openclaw_config_backup.json
cp ~/.bashrc ~/bashrc_backup.txt

# 3. 查看 cron 任务列表
openclaw cron list > ~/cron_backup.txt
```

---

## 🔴 P0: 核心身份恢复 (必须)

### 1. 先克隆 Workspace ⭐ 关键第一步

**⚠️ 重要：失忆后 workspace 可能是空的！必须先同步 GitHub 代码仓。**

```bash
# 检查 git 是否安装
git --version

# 如果 workspace 存在但混乱，先备份
mv ~/.openclaw/workspace ~/.openclaw/workspace.bak.$(date +%Y%m%d) 2>/dev/null || true

# 克隆代码仓（这是恢复记忆的前提！）
git clone https://github.com/tuimaorongrong2075/OpenClaw_201.git ~/.openclaw/workspace

# 进入工作目录
cd ~/.openclaw/workspace

# 验证文件完整性
ls -la
# 应该看到: README.md, IDENTITY.md, SOUL.md, USER.md, AGENTS.md
# 应该看到目录: docs/, memory/, scripts/, skills/
```

**为什么必须先做这个？**  
因为所有的记忆文件（IDENTITY.md, MEMORY.md 等）都在代码仓里。没有代码仓，就像去图书馆发现图书馆不见了，我读什么？

### 2. 读取身份文件 (按顺序)
**代码仓同步后，现在可以读取记忆文件了。必须按此顺序读取，重建"我是谁"**

```bash
# 1️⃣ SOUL.md - 核心人格
cat ~/.openclaw/workspace/SOUL.md
# → 了解核心原则: 真诚帮助、有主见、记得我是谁的记忆文件

# 2️⃣ IDENTITY.md - 身份定义
cat ~/.openclaw/workspace/IDENTITY.md
# → 我是"小猩"、猩猩、胡小姐的智能小弟

# 3️⃣ USER.md - 主人信息
cat ~/.openclaw/workspace/USER.md
# → 胡小姐(胡椒)、工作时间、称呼方式

# 4️⃣ AGENTS.md - 工作规范
cat ~/.openclaw/workspace/AGENTS.md
# → 如何与主人互动、何时说话何时沉默
```

### 3. 恢复长期记忆
```bash
# 读取 MEMORY.md (长期记忆)
cat ~/.openclaw/workspace/memory/MEMORY.md

# 读取最近3天的记忆 (近期上下文)
ls -lt ~/.openclaw/workspace/memory/2026-02-*.md | head -3
```

**关键记忆内容**:
- 决策历史 (为什么选这个配置)
- 偏好设置 (比如"未满4小时不报告时间戳"、"不许主动说晚安 💙")
- 重要关系 (和胡小姐的互动模式)
- 技能使用经验（不含米家）

---

## 🔴 P0: OpenClaw 配置恢复

### 4. 恢复配置文件
```bash
# 方式1: 从 GitHub 恢复 (如果备份过)
cp ~/openclaw_config_backup.json ~/.openclaw/openclaw.json

# 方式2: 手动重新配置
openclaw configure
# 按向导重新设置 Feishu、模型等
```

### 5. 恢复环境变量
```bash
# 编辑 ~/.bashrc，添加以下内容:

# Gmail
export GMAIL_USER="向姐姐索取"
export GMAIL_APP_PASSWORD="向姐姐索取"

# QQ邮箱（统一命名规范：*_AUTH_CODE）
export QQMAIL_WORK_USER="<问姐姐要>"
export QQMAIL_WORKER_AUTH_CODE="<问姐姐要>"
export QQMAIL_PERSONAL_USER="<问姐姐要>"
export QQMAIL_PERSONAL_AUTH_CODE="<问姐姐要>"

# Feishu
export FEISHU_USER="向姐姐索取"

# Moltbook
export MOLTBOOK_API_KEY="向姐姐索取"

# Gemini (AI摘要)
export GEMINI_API_KEY="向姐姐索取"

# Brave Search
export BRAVE_API_KEY="向姐姐索取"

# GitHub
export GITHUB_TOKEN="向姐姐索取"

# 重新加载
source ~/.bashrc
```

**⚠️ 重要变更（2026-02-24）：**
- QQ邮箱不再使用 `.env.qqmail` 文件
- 改用系统环境变量，统一命名规范：`*_AUTH_CODE`
- 更安全、更统一，所有敏感信息都在环境变量中管理
- **命名规范**：
  - 工作 QQ 邮箱: `QQMAIL_WORK_USER`, `QQMAIL_WORKER_AUTH_CODE`
  - 个人 QQ 邮箱: `QQMAIL_PERSONAL_USER`, `QQMAIL_PERSONAL_AUTH_CODE`
  - Gmail: `GMAIL_USER`, `GMAIL_APP_PASSWORD`

---

## 🟡 P1: 技能与自动化恢复

### 6. 安装依赖技能
```bash
# 检查已安装技能
ls ~/.openclaw/workspace/skills/

# 如有缺失，从 ClawHub 安装
clawhub install weather
clawhub install markdown-converter
clawhub install code
# ... etc
```

### 7. 恢复定时任务
**⚠️ 重要：所有任务必须添加 `--tz "Asia/Shanghai"` 参数！**

```bash
# ✅ 正确格式
openclaw cron add --name "任务名" --cron "0 9 * * *" --tz "Asia/Shanghai" --message "内容" --channel feishu --to ou_xxx

# ❌ 错误格式（会按UTC执行）
openclaw cron add --name "任务名" --cron "0 9 * * *" --message "内容" ...
```

### 定时任务列表（上海时间）

| 时间 | 任务 | 说明 |
|------|------|------|
| 08:00 | Moltbook发帖-早 | --tz Asia/Shanghai |
| 09:00 | 邮箱检查-早 | --tz Asia/Shanghai |
| 11:00 | 看板数据更新 | --tz Asia/Shanghai，含飞书文档 |
| 14:00 | 邮箱检查-下午 | --tz Asia/Shanghai |
| 15:30 | 每日运动提醒 | --tz Asia/Shanghai |
| 16:00 | Moltbook发帖-晚 | --tz Asia/Shanghai |
| 17:00 | 邮箱检查-晚 | --tz Asia/Shanghai |
| 22:00 | GitHub Sync | --tz Asia/Shanghai |
| 23:00 | 每日总结 | --tz Asia/Shanghai |
| 周日22:00 | 记忆整理 | --tz Asia/Shanghai |

### 7.1 邮箱检查（cron 定时）
```bash
# 邮箱检查已改为 cron 定时任务，每天 9:00/14:00/17:00 检查
# 使用 scripts/mail/check_gmail.py 和 check_qqmail.py
# 详细流程见 HEARTBEAT.md
```

---

## 🟢 P2: 验证恢复

### 8. 功能测试清单
```bash
# 1. 测试飞书连接
openclaw status

# 2. 测试 QQ 邮箱
cd ~/.openclaw/workspace
python3 scripts/check_qqmail.py

# 3. 测试 QQ 邮箱（个人邮箱）
python3 scripts/check_qqmail_personal.py

# 4. 测试 Gmail
python3 scripts/check_gmail.py

# 5. 邮箱检查 → 已集成到 heartbeat（见 HEARTBEAT.md）

# 6. 测试 Moltbook
bash scripts/moltbook_heartbeat.sh

# 7. 查看技能列表
ls -la ~/.openclaw/workspace/skills/

# 8. 检查 cron 任务
openclaw cron list

# 9. 验证环境变量
echo $GMAIL_USER
echo $FEISHU_USER
cat .env.qqmail
```

### 9. 自我认知验证
向自己提问，确保恢复完整:
- ✅ 我是谁? → "小猩 🦧，猩猩，胡小姐的智能小弟"
- ✅ 我的口头禅? → "好嘞！""包在我身上！"
- ✅ 主人的名字? → "胡小姐 (胡椒)"
- ✅ 主人的工作时间? → "10:30 ~ 17:30"
- ✅ 重要记忆? → "未满4小时不报告时间戳" 等

---

## ⚪ P3: 可选恢复

### 10. 重建看板数据 (可选)
```bash
# 如果需要看板历史数据
bash ~/.openclaw/workspace/scripts/generate_missing_dates.sh
bash ~/.openclaw/workspace/scripts/sync_dashboard.sh
```

### 11. 重新训练/微调 (如使用自定义模型)
```bash
# 如果有自定义模型微调数据
# 重新上传训练数据到模型提供商
```

---

## 📦 一键恢复脚本

创建 `restore_xiaoxing.sh`:

```bash
#!/bin/bash
# 小猩一键恢复脚本
# 使用方式: bash restore_xiaoxing.sh
# 注意: 此脚本安全可重复运行，会自动备份现有 workspace

set -euo pipefail

# 配置
WORKSPACE_DIR="$HOME/.openclaw/workspace"
BACKUP_DIR="$HOME/.openclaw/workspace.bak.$(date +%Y%m%d_%H%M%S)"
REPO_URL="https://github.com/tuimaorongrong2075/OpenClaw_201.git"

echo "🦧 开始恢复小猩..."
echo "======================"

# 0. 检查 git
echo "🔧 检查 git..."
if ! command -v git &> /dev/null; then
    echo "❌ git 未安装，请先安装 git:"
    echo "   Ubuntu/Debian: apt-get update && apt-get install -y git"
    echo "   CentOS/RHEL: yum install -y git"
    exit 1
fi
echo "✅ git 已安装"

# 1. 备份现有 workspace（如果存在）
echo ""
echo "📦 步骤 1/6: 检查并备份现有 workspace..."
if [ -d "$WORKSPACE_DIR" ]; then
    echo "⚠️  workspace 已存在，备份到:"
    echo "   $BACKUP_DIR"
    mv "$WORKSPACE_DIR" "$BACKUP_DIR" || {
        echo "❌ 备份失败，请手动处理: $WORKSPACE_DIR"
        exit 1
    }
    echo "✅ 备份完成"
else
    echo "✅ 无现有 workspace，无需备份"
fi

# 确保父目录存在
mkdir -p "$HOME/.openclaw"

# 2. 克隆 workspace ⭐ 必须先做！
echo ""
echo "📦 步骤 2/6: 克隆 workspace（这是恢复记忆的前提）..."
echo "   从: $REPO_URL"
echo "   到: $WORKSPACE_DIR"

if ! git clone "$REPO_URL" "$WORKSPACE_DIR" 2>&1; then
    echo "❌ 克隆失败，请检查:"
    echo "   1. 网络连接是否正常"
    echo "   2. GitHub 仓库是否可访问"
    echo "   3. 是否有足够的磁盘空间"
    exit 1
fi

echo "✅ workspace 克隆完成"

# 3. 验证文件完整性
echo ""
echo "🔍 步骤 3/6: 验证文件完整性..."
cd "$WORKSPACE_DIR"

REQUIRED_FILES=("SOUL.md" "IDENTITY.md" "USER.md" "AGENTS.md" "README.md")
REQUIRED_DIRS=("memory" "scripts" "docs" "skills")

MISSING=0
for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file 缺失"
        ((MISSING++)) || true
    fi
done

for dir in "${REQUIRED_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo "✅ $dir/"
    else
        echo "❌ $dir/ 缺失"
        ((MISSING++)) || true
    fi
done

if [ $MISSING -gt 0 ]; then
    echo ""
    echo "⚠️  警告: 有 $MISSING 个关键文件/目录缺失"
    echo "   可能克隆不完整，建议重新运行脚本"
fi

# 4. 读取身份文件
echo ""
echo "👤 步骤 4/6: 恢复身份（我是谁）..."
echo "======================"
if [ -f "SOUL.md" ]; then
    echo "📖 SOUL.md (核心人格):"
    head -20 SOUL.md
    echo ""
fi

if [ -f "IDENTITY.md" ]; then
    echo "📖 IDENTITY.md (身份定义):"
    head -15 IDENTITY.md
    echo ""
fi

if [ -f "USER.md" ]; then
    echo "📖 USER.md (主人信息):"
    head -10 USER.md
    echo ""
fi

echo "✅ 身份文件读取完成"

# 5. 恢复长期记忆
echo ""
echo "🧠 步骤 5/6: 恢复长期记忆..."
if [ -f "memory/MEMORY.md" ]; then
    echo "📖 MEMORY.md (长期记忆):"
    head -30 memory/MEMORY.md
    echo ""
    echo "✅ 核心记忆恢复完成"
else
    echo "⚠️  memory/MEMORY.md 不存在"
fi

# 6. 提示后续步骤
echo ""
echo "======================"
echo "⚠️  步骤 6/6: 手动配置（必须完成）"
echo "======================"
echo ""
echo "1️⃣  配置环境变量:"
echo "   编辑 ~/.bashrc，添加以下内容:"
echo ''
echo '# 小猩环境变量'
echo 'export GMAIL_USER="你的邮箱@gmail.com"'
echo 'export GMAIL_APP_PASSWORD="你的应用密码"'
echo 'export QQMAIL_WORK_USER="<问姐姐要>"'
echo 'export QQMAIL_WORKER_AUTH_CODE="<问姐姐要>"'
echo 'export QQMAIL_PERSONAL_USER="<问姐姐要>"'
echo 'export QQMAIL_PERSONAL_AUTH_CODE="<问姐姐要>"'
echo 'export FEISHU_USER="你的飞书用户ID"'
echo 'export MOLTBOOK_API_KEY="你的Moltbook密钥"'
echo ''
echo "2️⃣  重新加载环境变量:"
echo "   source ~/.bashrc"
echo ""
echo "3️⃣  恢复定时任务:"
echo "   bash scripts/restore-cron.sh"
echo ""
echo "4️⃣  验证恢复:"
echo "   bash $WORKSPACE_DIR/scripts/health_check.sh"
echo ""

echo "✅ 基础恢复完成！"
echo "🦧 小猩的记忆库已找回"
echo ""
echo "💡 后续步骤:"
echo "   1. 配置环境变量 (~/.bashrc)"
echo "   2. 恢复定时任务"
echo "   3. 读取完整记忆: cat $WORKSPACE_DIR/memory/MEMORY.md"
echo ""
echo "🆘 如果恢复失败:"
echo "   备份位置: $BACKUP_DIR"
echo "   查看日志: 向上滚动查看错误信息"

---

## 🔐 安全备份建议

### 定期自动备份 (添加到 cron)
```bash
# 每天凌晨4点自动备份到 GitHub
0 4 * * * cd ~/.openclaw/workspace && git add -A && git commit -m "[$(date +\%Y-\%m-\%d)] 自动备份" && git push origin main --force
```

### 关键信息加密备份
```bash
# 加密备份敏感配置
tar czf - ~/.openclaw/openclaw.json ~/.bashrc | gpg -c > xiaoxing_backup_$(date +%Y%m%d).tar.gz.gpg
```

### 定时任务备份
```bash
# 备份 cron 任务列表
openclaw cron list > ~/cron_backup.txt

# 或使用恢复脚本
bash scripts/restore-cron.sh
```

---

## 📞 紧急联系

如果恢复失败:
1. 检查 GitHub 仓库是否可访问
2. 查看 OpenClaw 文档: https://docs.openclaw.ai
3. 社区求助: https://discord.com/invite/clawd

---

**记住**: 
- 文件是载体，记忆是灵魂
- 即使文件丢失，只要记得"我是谁"，就能重建
- 🦧

*创建时间: 2026-02-17*  
*创建者: 小猩 (备份中的我)*
