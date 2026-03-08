#!/bin/bash
# update_dashboard_all.sh - 更新所有看板数据
# 被 cron 调用

echo "🦧 开始更新看板数据..."

cd /root/.openclaw/workspace

# 1. 服务器状态
echo "1/4 更新服务器状态..."
python3 scripts/cron/update_server_stats.py

# 2. AI News
echo "2/4 更新AI News..."
python3 scripts/cron/update_ai_news.py

# 3. GitHub Trending
echo "3/4 更新GitHub Trending..."
python3 scripts/cron/update_github_trending.py

# 4. Agent Projects
echo "4/4 更新Agent Projects..."
python3 scripts/cron/update_agent_projects.py

echo "✅ 看板数据全部更新完成"
