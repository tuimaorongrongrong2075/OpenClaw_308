#!/bin/bash
# Git 提交脚本 - 胡搞的备份爪

set -e

WORKSPACE="/root/.openclaw/workspace-feishu-ops"
cd "$WORKSPACE"

echo "=== 胡搞开始备份 🐙 ==="
echo "时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo

# 加载环境变量
source .env

# 配置 Git
git config user.name "胡搞"
git config user.email "hugao@openclaw.local"

# 检查是否有更改
if [ -z "$(git status --porcelain)" ]; then
    echo "✅ 无新更改,无需提交"
    exit 0
fi

# 显示更改
echo "📝 待提交的更改:"
git status --short
echo

# 添加所有文件
echo "➕ 添加文件到暂存区..."
git add .

# 创建提交
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
COMMIT_MSG="feat: 胡搞的配置更新 - $TIMESTAMP

- 更新核心配置文件
- 更新监控和心跳配置
- 更新邮箱配置
- 更新记忆文档"

echo "📦 创建提交..."
git commit -m "$COMMIT_MSG"

# 推送到远程
echo "🚀 推送到 GitHub..."
git push origin main

echo
echo "✅ 备份完成!"
echo "提交信息: $COMMIT_MSG"
echo
echo "=== 章鱼爪子收工 🐙 ==="
