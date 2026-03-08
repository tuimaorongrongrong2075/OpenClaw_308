#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
脚本名称: check_qqmail.py
脚本功能: 定期检查工作QQ邮箱未读邮件并通知
作者: 小猩 🦧
创建日期: 2026-02-18
版本: 1.1.0
依赖: Python 3.8+, imaplib, email
环境变量: QQMAIL_WORK_USER, QQMAIL_WORK_PASS
定时任务: 0 * * * * (每小时)

版本记录:
    v1.0.0 (2026-02-18) - 初始版本，实现工作QQ邮箱检查功能
    v1.1.0 (2026-02-21) - 改用系统环境变量，移除 .env.qqmail 文件依赖
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
    user = os.environ.get("QQMAIL_WORK_USER", "")
    # 支持两种环境变量名（向后兼容）
    password = os.environ.get("QQMAIL_WORKER_AUTH_CODE") or os.environ.get("QQMAIL_WORK_PASS", "")
    
    if not user or not password:
        print("❌ 缺少以下环境变量:")
        if not user:
            print("   - QQMAIL_WORK_USER (工作QQ邮箱账号)")
        if not password:
            print("   - QQMAIL_WORKER_AUTH_CODE 或 QQMAIL_WORK_PASS (工作QQ邮箱授权码)")
        print("\n💡 请设置环境变量")
        return False
    return True

# 检查环境变量
if not check_required_env():
    exit(1)

# 配置 - 工作QQ邮箱
QQMAIL_USER = os.environ.get("QQMAIL_WORK_USER", "")
# 支持两种环境变量名（向后兼容）
QQMAIL_PASS = os.environ.get("QQMAIL_WORKER_AUTH_CODE") or os.environ.get("QQMAIL_WORK_PASS", "")
FEISHU_USER = os.environ.get("FEISHU_USER", "ou_0ca9ad88a77fd653f0244807918cab56")

# 状态文件
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

STATE_FILE = os.path.join(LOGS_DIR, "qqmail_work_state.json")
LOG_FILE = os.path.join(LOGS_DIR, "qqmail_work_check.log")
LAST_UNREAD_FILE = os.path.join(LOGS_DIR, "last_qqmail_work_unread.txt")

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

def check_qqmail():
    """
    检查工作QQ邮箱未读邮件
    
    连接到QQ邮箱IMAP服务器，检查收件箱中的未读邮件数量，
    并获取最新一封未读邮件的信息。
    
    Returns:
        tuple: (unread_count, latest_email)
            - unread_count (int): 未读邮件数量，失败返回None
            - latest_email (dict): 最新邮件信息{from, subject, date}，失败返回None
            
    Raises:
        无显式抛出，内部捕获所有异常并返回None
        
    Example:
        >>> count, latest = check_qqmail()
        >>> if count:
        ...     print(f"未读: {count}封，最新: {latest['subject']}")
    """
    if not QQMAIL_USER or not QQMAIL_PASS:
        return None, None

    try:
        # 连接到QQ邮箱IMAP
        imap = imaplib.IMAP4_SSL("imap.qq.com", 993)
        imap.login(QQMAIL_USER, QQMAIL_PASS)
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
        print(f"❌ QQ邮箱检查失败: {e}")
        return None, None

def save_state(unread_count, latest_email):
    """保存状态"""
    state = {
        "last_check": datetime.now().isoformat(),
        "unread_count": unread_count,
        "latest_email": latest_email
    }
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
    
    with open(LAST_UNREAD_FILE, "w") as f:
        f.write(str(unread_count))

def get_last_unread():
    """获取上次未读数量"""
    try:
        if os.path.exists(LAST_UNREAD_FILE):
            with open(LAST_UNREAD_FILE, "r") as f:
                return int(f.read().strip())
    except:
        pass
    return 0

def main():
    """主函数"""
    unread_count, latest_email = check_qqmail()

    if unread_count is None:
        print(f"📧 检查失败")
        return

    # 保存状态
    save_state(unread_count, latest_email)

    # 打印结果
    if unread_count > 0:
        print(f"📧 {unread_count}封未读")
    else:
        print(f"📧 0封未读")

if __name__ == "__main__":
    main()
