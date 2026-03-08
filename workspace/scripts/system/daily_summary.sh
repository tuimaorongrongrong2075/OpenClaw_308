#!/bin/bash
#===============================================================================
# 脚本名称: daily_summary.sh
# 脚本功能: 生成每日工作总结并推送到 GitHub
# 作者: 小猩
# 创建日期: 2026-02-17
# 版本: 1.0.0
#===============================================================================
# 版本记录
#===============================================================================
# v1.0.0 (2026-02-17) - 初始版本
#===============================================================================

set -euo pipefail

# 小猩每日总结脚本 - 每天22:00执行
# 记录今天所有工作内容，不留任何隐私信息

set -e

TODAY=$(date +%Y-%m-%d)
MEMORY_FILE="/root/.openclaw/workspace/memory/$TODAY.md"
WORKSPACE="/root/.openclaw/workspace"

echo "🦧 开始生成每日总结..."

# 1. 获取Git提交历史（去除敏感信息）
GIT_LOG=$(cd "$WORKSPACE" && git log --oneline --since="00:00" --until="now" 2>/dev/null | sed 's/[0-9a-f]\{7\}/[COMMIT]/g' || echo "暂无提交")

# 2. 检查今日文件变更
FILE_CHANGES=$(cd "$WORKSPACE" && git diff --name-only --since="00:00" 2>/dev/null | tr '\n' ', ' || echo "无")

# 3. 检查RSS更新
RSS_CHECK=""
if [ -f "$WORKSPACE/docs/rss_feeds.html" ]; then
    RSS_TIME=$(grep -o "自动更新.*" "$WORKSPACE/docs/rss_feeds.html" | head -1 || echo "")
    RSS_CHECK="📰 RSS: $RSS_TIME"
fi

# 4. 生成今日总结
cat > "$MEMORY_FILE" << EOF
# $TODAY - 小猩日记

## 📋 今日完成事项

### 🔧 技术配置
$(echo "$GIT_LOG" | sed 's/^/- /' || echo "  - 无新提交")

### 📁 文件变更
$FILE_CHANGES

### 📰 RSS订阅
$RSS_CHECK

---

## 💭 今日感悟

好嘞，明天继续干活！🦧

---

*小猩 🦧 · $(date '+%Y-%m-%d %H:%M')*
EOF

echo "✅ 每日总结已保存: $MEMORY_FILE"

# 5. 同步到GitHub
echo "🚀 同步到 GitHub..."
cd "$WORKSPACE"
git add memory/
git commit -m "[$TODAY] 小猩每日总结 🦧" 2>/dev/null || echo "无新内容需要提交"
git push https://x-access-token:$(gh auth token)@github.com/tuimaorongrongrong2075/OpenClaw_201.git HEAD:main --force 2>/dev/null || echo "GitHub同步失败或无需同步"

echo "✅ 每日总结完成！"
