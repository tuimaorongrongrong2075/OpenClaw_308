#!/bin/bash
# 天气预报推送脚本
# 作者: 胡搞 🐙
# 用途: 每天8点推送天气预报到飞书

WORKSPACE="/root/.openclaw/workspace-feishu-ops/workspace-feishu-ops"
CITY="Shanghai"  # 可以改成姐姐的城市

# 获取天气 (使用 wttr.in)
WEATHER=$(curl -s "wttr.in/$CITY?format=3" 2>/dev/null)

if [ -z "$WEATHER" ]; then
    WEATHER="天气获取失败"
fi

# 构建飞书消息
MESSAGE="## 🌤️ 早上好,姐姐!

**天气预报** - $(date '+%Y年%m月%d日') $WEATHER

### 今日建议
- 根据天气情况选择合适的出行方式
- 记得带伞/注意防晒 (根据天气)

---

**汇报人:** 胡搞 🐙  
**时间:** $(date '+%H:%M:%S')"

# 保存到日志
echo "=== $(date '+%Y-%m-%d %H:%M:%S') ===" >> "$WORKSPACE/logs/weather.log"
echo "$MESSAGE" >> "$WORKSPACE/logs/weather.log"

# TODO: 发送到飞书 (需要配置飞书机器人)
# curl -X POST "飞书webhook" -d "$MESSAGE"

echo "$MESSAGE"
