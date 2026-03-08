#!/bin/bash
# 心跳检查脚本 - 每6小时执行
# 作者: 胡搞 🐙
# 用途: 服务器健康检查 + 运维报告

WORKSPACE="/root/.openclaw/workspace-feishu-ops/workspace-feishu-ops"
LOG_FILE="$WORKSPACE/logs/heartbeat.log"
REPORT_FILE="$WORKSPACE/logs/heartbeat-report-$(date +%Y%m%d-%H%M%S).md"

# 创建日志目录
mkdir -p "$WORKSPACE/logs"

# 记录开始时间
echo "=== 心跳检查开始: $(date '+%Y-%m-%d %H:%M:%S') ===" | tee -a "$LOG_FILE"

cd "$WORKSPACE" || exit 1

# 1. GitHub 同步状态
echo "检查 GitHub 状态..." | tee -a "$LOG_FILE"
git status --short | tee -a "$LOG_FILE"
git log -1 --oneline | tee -a "$LOG_FILE"

# 2. 服务器健康
echo -e "\n=== 服务器状态 ===" | tee -a "$LOG_FILE"
uptime | tee -a "$LOG_FILE"
free -h | tee -a "$LOG_FILE"
df -h / | tee -a "$LOG_FILE"

# 3. OpenClaw Gateway
echo -e "\n=== Gateway 状态 ===" | tee -a "$LOG_FILE"
openclaw gateway status 2>&1 | tee -a "$LOG_FILE" || echo "Gateway 命令不可用" | tee -a "$LOG_FILE"

# 4. 网络状态
echo -e "\n=== 网络状态 ===" | tee -a "$LOG_FILE"
ping -c 3 8.8.8.8 > /dev/null 2>&1 && echo "外网: ✅" | tee -a "$LOG_FILE" || echo "外网: ❌" | tee -a "$LOG_FILE"

# 5. 安全检查
echo -e "\n=== 安全状态 ===" | tee -a "$LOG_FILE"
last -n 5 | tee -a "$LOG_FILE"

# 6. 自我健康
echo -e "\n=== 工作目录状态 ===" | tee -a "$LOG_FILE"
du -sh "$WORKSPACE" | tee -a "$LOG_FILE"

# 记录结束时间
echo "=== 心跳检查完成: $(date '+%Y-%m-%d %H:%M:%S') ===" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# 如果有异常,通知
# TODO: 集成飞书通知
