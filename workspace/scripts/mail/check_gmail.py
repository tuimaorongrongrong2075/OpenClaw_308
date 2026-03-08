#!/usr/bin/env python3
"""
脚本名称: check_gmail.py
脚本功能: 定期检查 Gmail 未读邮件并通知
作者: 小猩
创建日期: 2026-02-17
版本: 1.0.0

版本记录:
    v1.0.0 (2026-02-17) - 初始版本
"""

"""
Gmail 检查脚本 - 定期检查新邮件并通过飞书通知
"""

import imaplib
import email
from email.header import decode_header
import subprocess
from datetime import datetime
import json
import os

# 检查必需的环境变量
def check_required_env():
    """检查必需的环境变量是否已设置"""
    required = {
        'GMAIL_USER': 'Gmail邮箱账号',
        'GMAIL_APP_PASSWORD': 'Gmail应用密码'
    }
    
    missing = []
    for key, desc in required.items():
        if not os.environ.get(key):
            missing.append(f"{key} ({desc})")
    
    if missing:
        print("❌ 缺少以下环境变量:")
        for item in missing:
            print(f"   - {item}")
        print("\n💡 请向姐姐索取配置信息，我会保存到环境变量后再执行。")
        return False
    return True

# 先检查环境变量
if not check_required_env():
    exit(1)

# 配置
GMAIL_USER = os.environ.get("GMAIL_USER", "")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "")
FEISHU_USER = os.environ.get("FEISHU_USER", "")  # 飞书用户ID（可选）

# 状态文件路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

STATE_FILE = os.path.join(LOGS_DIR, "gmail_state.json")
LOG_FILE = os.path.join(LOGS_DIR, "gmail_check.log")
LAST_UNREAD_FILE = os.path.join(LOGS_DIR, "last_gmail_unread.txt")

def decode_str(header_value):
    """解码邮件标题"""
    if header_value is None:
        return ""
    decoded = decode_header(header_value)
    result = ""
    for content, encoding in decoded:
        if isinstance(content, bytes):
            result += content.decode(encoding or "utf-8", errors="ignore")
        else:
            result += content
    return result

def check_gmail():
    """检查Gmail未读邮件"""
    try:
        # 连接到Gmail IMAP
        imap = imaplib.IMAP4_SSL("imap.gmail.com")
        imap.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        imap.select("INBOX")

        # 搜索未读邮件
        status, messages = imap.search(None, "UNSEEN")
        unread_count = 0
        latest_email = None

        if status == "OK":
            email_ids = messages[0].split()
            unread_count = len(email_ids)

            # 获取最新的邮件
            if email_ids:
                latest_id = email_ids[-1]
                status, msg_data = imap.fetch(latest_id, "(RFC822)")
                if status == "OK":
                    for response_part in msg_data:
                        if isinstance(response_part, tuple):
                            msg = email.message_from_bytes(response_part[1])
                            latest_email = {
                                "from": decode_str(msg.get("From")),
                                "subject": decode_str(msg.get("Subject")),
                                "date": msg.get("Date")
                            }

        imap.close()
        imap.logout()

        return unread_count, latest_email

    except Exception as e:
        log_error(f"Gmail检查失败: {str(e)}")
        return None, None

def log_error(message):
    """记录错误日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] ERROR: {message}\n")

def save_state(unread_count, latest_email):
    """保存状态到文件"""
    state = {
        "last_check": datetime.now().isoformat(),
        "unread_count": unread_count,
        "latest_email": latest_email
    }
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
    
    # 保存未读数量
    with open(LAST_UNREAD_FILE, "w") as f:
        f.write(str(unread_count))

def get_last_unread():
    """获取上次检查的未读数量"""
    try:
        if os.path.exists(LAST_UNREAD_FILE):
            with open(LAST_UNREAD_FILE, "r") as f:
                return int(f.read().strip())
    except:
        pass
    return 0

def send_feishu_notification(unread_count, latest_email):
    """发送飞书通知"""
    try:
        if latest_email:
            message = f"📬 你有 {unread_count} 封未读邮件\n\n最新邮件：\n发件人：{latest_email['from']}\n主题：{latest_email['subject']}"
        else:
            message = f"📬 你有 {unread_count} 封未读邮件"
        
        # 使用OpenClaw的message工具发送飞书通知
        result = subprocess.run([
            "openclaw", "message", "send",
            "--channel", "feishu",
            "--target", FEISHU_USER,
            "--message", message
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            return True
        else:
            log_error(f"飞书通知发送失败: {result.stderr}")
            return False
    except Exception as e:
        log_error(f"飞书通知异常: {str(e)}")
        return False

def main():
    """主函数"""
    unread_count, latest_email = check_gmail()

    if unread_count is None:
        print(f"📧 检查失败")
        return

    # 获取上次未读数量
    last_unread = get_last_unread()
    
    # 如果有新邮件（未读数量增加），发送通知
    new_emails = unread_count - last_unread
    if new_emails > 0:
        if latest_email:
            message = f"📬 你有 {new_emails} 封新邮件（共{unread_count}封未读）\n\n最新：{latest_email['from']}\n{latest_email['subject']}"
        else:
            message = f"📬 你有 {new_emails} 封新邮件（共{unread_count}封未读）"
        send_feishu_notification(unread_count, latest_email)

    if latest_email:
        latest_info = f"{latest_email['from'][:30]} - {latest_email['subject'][:40]}"
    else:
        latest_info = "无新邮件"

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    log_entry = f"[{timestamp}] 未读: {unread_count} | 最新: {latest_info}\n"

    # 追加到日志文件
    with open(LOG_FILE, "a") as f:
        f.write(log_entry)

    # 保存状态
    save_state(unread_count, latest_email)

    # 打印结果
    if unread_count > 0:
        print(f"📧 {unread_count}封未读 | 最新: {latest_info[:60]}")
    else:
        print(f"📧 0封未读")

if __name__ == "__main__":
    main()
