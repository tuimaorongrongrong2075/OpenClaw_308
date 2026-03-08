#!/bin/bash
#===============================================================================
# 脚本名称: health_check.sh
# 脚本功能: 检查系统状态、GitHub 同步、cron 任务
# 作者: 小猩
# 创建日期: 2026-02-17
# 版本: 1.0.0
#===============================================================================
# 版本记录
#===============================================================================
# v1.0.0 (2026-02-17) - 初始版本
#===============================================================================

set -euo pipefail

# 小猩每日健康检查脚本
# 检查系统状态、GitHub同步、cron任务

set -e

WORKSPACE="/root/.openclaw/workspace"
DATE=$(date '+%Y-%m-%d %H:%M')

echo "🦧 小猩健康检查 - $DATE"
echo "=" * 50

# 1. 检查GitHub同步状态
echo ""
echo "📦 GitHub同步检查..."
cd "$WORKSPACE"
if git remote get-url origin &>/dev/null; then
    LAST_COMMIT=$(git log -1 --oneline --format="%h %s" 2>/dev/null || echo "无")
    echo "   ✅ GitHub已关联"
    echo "   📝 最后提交: $LAST_COMMIT"
else
    echo "   ⚠️ GitHub未关联"
fi

# 2. 检查cron任务状态
echo ""
echo "⏰ Cron任务检查..."
CRON_COUNT=$(crontab -l 2>/dev/null | grep -c "小猩" || true)
CRON_COUNT=${CRON_COUNT:-0}
echo "   📊 小猩定时任务: $CRON_COUNT 个"
if [ "$CRON_COUNT" -ge 4 ]; then
    echo "   ✅ 任务齐全"
else
    echo "   ⚠️ 任务可能缺失"
fi

# 3. 检查磁盘空间
echo ""
echo "💾 磁盘检查..."
DISK_USAGE=$(df -h / | tail -1 | awk '{print $5 " 已用"}')
echo "   📊 磁盘: $DISK_USAGE"

# 4. 检查内存
echo ""
echo "🧠 内存检查..."
MEM_USAGE=$(free -h | tail -1 | awk '{print $3 " / " $2}')
echo "   📊 内存: $MEM_USAGE"

# 5. 检查关键文件
echo ""
echo "📁 文件检查..."
FILES=("IDENTITY.md" "USER.md" "HEARTBEAT.md" "scripts/sync_github.sh")
for f in "${FILES[@]}"; do
    if [ -f "$WORKSPACE/$f" ]; then
        echo "   ✅ $f"
    else
        echo "   ❌ $f 缺失!"
    fi
done
# MEMORY.md在memory目录
if [ -f "$WORKSPACE/memory/MEMORY.md" ]; then
    echo "   ✅ memory/MEMORY.md"
else
    echo "   ❌ memory/MEMORY.md 缺失!"
fi

# 6. 检查上次运行时间
echo ""
echo "🕐 运行时检查..."
SCRIPT_COUNT=$(ls "$WORKSPACE/scripts/"*.sh 2>/dev/null | wc -l)
echo "   📊 脚本数量: $SCRIPT_COUNT"

# 生成健康报告
echo ""
echo "=" * 50
echo "✅ 健康检查完成"
echo ""
echo "💡 提示:"
echo "   - 若GitHub同步失败，运行: scripts/sync_github.sh"
echo "   - 若cron异常，检查: cron list"
echo "   - 若磁盘满，清理: memory/ 旧文件"
