#!/bin/bash
# 清理旧的会话文件
# 定时任务：每天 03:00 执行

WORKSPACE="/root/.openclaw/workspace"
SESSIONS_DIR="/root/.openclaw/agents/main/sessions"
LOG_DIR="$WORKSPACE/scripts/logs"

echo "=== 清理旧会话 ===" | tee -a "$LOG_DIR/cleanup.log"
echo "时间: $(date '+%Y-%m-%d %H:%M:%S')" | tee -a "$LOG_DIR/cleanup.log"

# 检查会话目录
if [ ! -d "$SESSIONS_DIR" ]; then
    echo "会话目录不存在: $SESSIONS_DIR" | tee -a "$LOG_DIR/cleanup.log"
    exit 1
fi

# 统计当前会话数
SESSION_COUNT=$(find "$SESSIONS_DIR" -name "*.jsonl" 2>/dev/null | wc -l)
echo "当前会话数: $SESSION_COUNT" | tee -a "$LOG_DIR/cleanup.log"

# 计算总大小
TOTAL_SIZE=$(du -sh "$SESSIONS_DIR" 2>/dev/null | cut -f1)
echo "会话总大小: $TOTAL_SIZE" | tee -a "$LOG_DIR/cleanup.log"

# 保留最近7天的会话文件
DAYS_TO_KEEP=7
find "$SESSIONS_DIR" -name "*.jsonl" -type f -mtime +$DAYS_TO_KEEP -delete

# 统计清理后数量
AFTER_COUNT=$(find "$SESSIONS_DIR" -name "*.jsonl" 2>/dev/null | wc -l)
echo "清理后会话数: $AFTER_COUNT" | tee -a "$LOG_DIR/cleanup.log"

echo "=== 清理完成 ===" | tee -a "$LOG_DIR/cleanup.log"
echo "" | tee -a "$LOG_DIR/cleanup.log"
