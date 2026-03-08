#!/bin/bash
# 心跳检查脚本 v3 - 完整版 (包含会话状态)
# 作者: 胡搞 🐙
# 用途: 服务器健康检查 + 运维报告 + 会话状态

WORKSPACE="/root/.openclaw/workspace-feishu-ops/workspace-feishu-ops"
LOG_FILE="$WORKSPACE/logs/heartbeat.log"
REPORT_FILE="$WORKSPACE/logs/heartbeat-report-$(date +%Y%m%d-%H%M%S).md"

# 创建日志目录
mkdir -p "$WORKSPACE/logs"

# 记录开始时间
START_TIME=$(date '+%Y-%m-%d %H:%M:%S')
echo "=== 心跳检查开始: $START_TIME ===" | tee -a "$LOG_FILE"

cd "$WORKSPACE" || exit 1

# 1. GitHub 同步状态
echo -e "\n## 🔗 GitHub 状态" | tee -a "$LOG_FILE"
git status --short | tee -a "$LOG_FILE"
git log -1 --oneline | tee -a "$LOG_FILE"

# 2. 服务器健康
echo -e "\n## 🐉 服务器状态 (飞龙在天)" | tee -a "$LOG_FILE"
uptime | tee -a "$LOG_FILE"
free -h | tee -a "$LOG_FILE"
df -h / | tee -a "$LOG_FILE"
ps aux | wc -l | tee -a "$LOG_FILE"

# 3. OpenClaw Gateway
echo -e "\n## 🚪 Gateway 状态" | tee -a "$LOG_FILE"
echo "Gateway 检查暂不可用 (Node.js 未安装)" | tee -a "$LOG_FILE"

# 4. 网络状态
echo -e "\n## 🌐 网络状态" | tee -a "$LOG_FILE"
ping -c 3 8.8.8.8 > /dev/null 2>&1 && echo "外网: ✅" | tee -a "$LOG_FILE" || echo "外网: ❌" | tee -a "$LOG_FILE"

# 5. 安全检查
echo -e "\n## 🔒 安全状态" | tee -a "$LOG_FILE"
last -n 5 | tee -a "$LOG_FILE"

# 6. 会话状态 (新增)
echo -e "\n## 💬 会话状态" | tee -a "$LOG_FILE"
python3 "$WORKSPACE/scripts/check-sessions.py" | tee -a "$LOG_FILE"

# 7. 自我健康
echo -e "\n## 🏥 工作目录状态" | tee -a "$LOG_FILE"
du -sh "$WORKSPACE" | tee -a "$LOG_FILE"

# 记录结束时间
END_TIME=$(date '+%Y-%m-%d %H:%M:%S')
echo "=== 心跳检查完成: $END_TIME ===" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# 生成 Markdown 报告
SESSION_INFO=$(python3 -c "import json; data = json.load(open('$WORKSPACE/session-state.json')); print(f\"**总会话:** {data.get('totalSessions', 0)}\")" 2>/dev/null || echo "会话数据不可用")

cat > "$REPORT_FILE" << EOF
# 🐉 飞龙在天 - 运维心跳报告

**检查时间:** $START_TIME  
**报告人:** 胡搞 🐙

---

## 📊 实时状态

\`\`\`
$(uptime)
\`\`\`

## 💬 会话状态

$SESSION_INFO

详见: \`session-state.json\`

---

_下次检查: 6小时后_
EOF

echo "💾 报告已保存: $REPORT_FILE"
