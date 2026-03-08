#!/bin/bash
# 安装定时任务脚本
# 作者: 胡搞 🐙

echo "=== 安装胡搞的定时任务 ==="

# 备份当前 crontab
crontab -l > /tmp/crontab-backup-$(date +%Y%m%d-%H%M%S) 2>/dev/null

# 添加新的定时任务
(crontab -l 2>/dev/null; cat <<'EOF'

# 胡搞的定时任务
0 */6 * * * /root/.openclaw/workspace-feishu-ops/workspace-feishu-ops/scripts/heartbeat.sh >> /root/.openclaw/workspace-feishu-ops/workspace-feishu-ops/logs/heartbeat.log 2>&1
0 9,16 * * * /usr/bin/python3 /root/.openclaw/workspace-feishu-ops/workspace-feishu-ops/scripts/email-check.py >> /root/.openclaw/workspace-feishu-ops/workspace-feishu-ops/logs/email-check.log 2>&1
0 8 * * * /root/.openclaw/workspace-feishu-ops/workspace-feishu-ops/scripts/weather.sh >> /root/.openclaw/workspace-feishu-ops/workspace-feishu-ops/logs/weather.log 2>&1
EOF
) | crontab -

echo "✅ 定时任务已安装!"
echo ""
echo "当前 crontab:"
crontab -l
echo ""
echo "备份位置: /tmp/crontab-backup-*"
echo ""
echo "日志目录: /root/.openclaw/workspace-feishu-ops/workspace-feishu-ops/logs/"
