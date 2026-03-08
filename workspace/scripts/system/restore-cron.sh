#!/bin/bash
# 恢复定时任务脚本
# 用法: bash scripts/restore-cron.sh

echo "🧙 恢复定时任务中..."

# 健康检查
openclaw cron add --name "系统健康检查" --cron "0 7 * * *" --message "执行系统健康检查并报告状态" --model "isolated" --announce

# AI 摘要
openclaw cron add --name "AI每日摘要" --cron "0 8 * * *" --message "生成今日AI资讯摘要" --model "isolated" --announce

# Moltbook 发帖
openclaw cron add --name "Moltbook发帖-早" --cron "0 8 * * *" --message "去Moltbook社区发帖分享今日感想" --model "isolated" --announce
openclaw cron add --name "Moltbook发帖-晚" --cron "0 16 * * *" --message "去Moltbook社区发帖分享今日感想" --model "isolated" --announce

# 邮箱检查
openclaw cron add --name "邮箱检查-早" --cron "0 9 * * *" --message "检查所有邮箱并汇报未读邮件" --model "isolated" --announce
openclaw cron add --name "邮箱检查-下午" --cron "0 14 * * *" --message "检查所有邮箱并汇报未读邮件" --model "isolated" --announce
openclaw cron add --name "邮箱检查-晚" --cron "0 17 * * *" --message "检查所有邮箱并汇报未读邮件" --model "isolated" --announce

# 运动提醒
openclaw cron add --name "每日运动提醒" --cron "13 15 * * *" --message "提醒姐姐做运动" --model "isolated" --announce

# 每日总结
openclaw cron add --name "每日总结" --cron "0 22 * * *" --message "生成今日工作/生活总结" --model "isolated" --announce

echo "✅ 定时任务恢复完成！"
openclaw cron list
