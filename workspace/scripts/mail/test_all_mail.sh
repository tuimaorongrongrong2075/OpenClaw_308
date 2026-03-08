#!/bin/bash
# 重新加载环境变量并测试邮箱连接

echo "🔄 重新加载环境变量..."
source ~/.bashrc

echo ""
echo "📋 当前环境变量："
env | grep -i qqmail | sort

echo ""
echo "🧪 测试邮箱连接..."

# 测试工作邮箱
echo "1. 工作 QQ 邮箱 (\$QQMAIL_WORK_USER):"
python3 /root/.openclaw/workspace/scripts/mail/check_qqmail.py

echo ""
echo "2. 个人 QQ 邮箱 (\$QQMAIL_PERSONAL_USER):"
python3 /root/.openclaw/workspace/scripts/mail/check_qqmail_personal.py

echo ""
echo "3. Gmail:"
python3 /root/.openclaw/workspace/scripts/mail/check_gmail.py
