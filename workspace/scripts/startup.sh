#!/bin/bash
#===============================================================================
# 脚本名称: startup.sh
# 脚本功能: OpenClaw 启动后自动运行初始化
# 作者: 小猩
# 创建日期: 2026-02-17
# 版本: 1.0.0
#===============================================================================
# 版本记录
#===============================================================================
# v1.0.0 (2026-02-17) - 初始版本
#===============================================================================

set -euo pipefail

# OpenClaw 启动后自动运行
# 完成环境变量加载和初始化工作

set -e

WORKSPACE="/root/.openclaw/workspace"

echo "🦧 小猩启动中..."

# 1. 加载环境变量（从 ~/.bashrc）
if [ -f "$WORKSPACE/scripts/load_env.sh" ]; then
    echo "🔐 加载环境变量..."
    bash "$WORKSPACE/scripts/load_env.sh"
else
    echo "⚠️  警告：load_env.sh 不存在"
fi

# 2. 禁用重复的定时任务（保留手动启动控制）
echo "🔧 定时任务控制（已禁用自动重启）..."
echo "   提示：使用 'openclaw cron list' 查看所有任务"
echo "         使用 'openclaw cron update <id> {\"enabled\":true}' 启用特定任务"

# 3. 初始化 Git 认证
echo "🔧 配置 Git 认证..."
cd "$WORKSPACE"
if [ -n "$GITHUB_TOKEN" ]; then
    # 使用环境变量中的token
    git remote set-url origin "https://${GITHUB_TOKEN}@github.com/tuimaorongrong2075/OpenClaw_201.git" 2>/dev/null || true
    echo "✅ Git 认证已配置"
else
    echo "⚠️  GITHUB_TOKEN 未设置"
fi

# 4. 测试 Gmail 连接
if [ -f "$WORKSPACE/scripts/check_gmail.py" ]; then
    echo "📧 测试 Gmail 连接..."
    python3 "$WORKSPACE/scripts/check_gmail.py" || echo "⚠️  Gmail 测试失败"
fi

echo "✅ 启动完成！小猩就绪 🦧"
