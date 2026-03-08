#!/bin/bash
#===============================================================================
# 脚本名称: backup_sessions.sh
# 脚本功能: 备份 OpenClaw 会话文件
# 作者: 小猩
# 创建日期: 2026-02-25
# 版本: 1.0.0
#===============================================================================
# 版本记录
#===============================================================================
# v1.0.0 (2026-02-25) - 初始版本
#===============================================================================

set -euo pipefail

SESSIONS_DIR="/root/.openclaw/agents/main/sessions"
BACKUP_DIR="/root/.openclaw/workspace/backups/sessions"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="sessions_backup_${TIMESTAMP}.tar.gz"

# 创建备份目录
mkdir -p "$BACKUP_DIR"

# 备份会话文件
echo "📦 正在备份会话文件..."
tar -czf "${BACKUP_DIR}/${BACKUP_NAME}" \
  -C "$SESSIONS_DIR" \
  *.jsonl \
  sessions.json

# 计算文件大小
SIZE=$(du -h "${BACKUP_DIR}/${BACKUP_NAME}" | cut -f1)

echo "✅ 备份完成: ${BACKUP_DIR}/${BACKUP_NAME} (${SIZE})"

# 保留最近 7 天的备份
echo "🧹 清理旧备份..."
find "$BACKUP_DIR" -name "sessions_backup_*.tar.gz" -mtime +7 -delete

echo "🎉 备份任务完成！"
