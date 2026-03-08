#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
脚本名称: clean_gmail_security.py
脚本功能: 自动清理 Gmail 安全提醒邮件
作者: 小猩
创建日期: 2026-02-17
版本: 1.0.0

版本记录:
    v1.0.0 (2026-02-17) - 初始版本
"""

"""
清理 Gmail 验证码和登录提醒类邮件
将匹配的邮件标记为已读
"""

import imaplib
import email
from email.header import decode_header
import os
import sys
from datetime import datetime

# 强制使用 UTF-8 编码
if sys.version_info[0] >= 3:
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 配置
GMAIL_USER = os.environ.get("GMAIL_USER")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "")

LOG_FILE = "/root/.openclaw/workspace/Log/gmail_clean.log"

def decode_str(header_value):
    """解码邮件标题"""
    if header_value is None:
        return ""
    try:
        decoded = decode_header(header_value)
        result = ""
        for content, encoding in decoded:
            if isinstance(content, bytes):
                result += content.decode(encoding or "utf-8", errors="ignore")
            else:
                result += content
        return result
    except:
        return str(header_value)

def clean_security_emails():
    """清理验证码和登录提醒类邮件"""
    try:
        # 连接到 Gmail IMAP
        imap = imaplib.IMAP4_SSL("imap.gmail.com")
        imap.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        imap.select("INBOX")

        # 搜索未读的验证码/登录提醒类邮件
        search_queries = [
            '(UNSEEN SUBJECT "验证码")',
            '(UNSEEN SUBJECT "verification code")',
            '(UNSEEN SUBJECT "verify code")',
            '(UNSEEN SUBJECT "login")',
            '(UNSEEN SUBJECT "sign-in")',
            '(UNSEEN FROM "no-reply@accounts.google.com")',
            '(UNSEEN FROM "noreply@github.com" SUBJECT "OAuth")',
        ]

        total_marked = 0
        all_matched = []

        for query in search_queries:
            try:
                status, messages = imap.search(None, query)
                if status == "OK" and messages[0]:
                    email_ids = messages[0].split()
                    for msg_id in email_ids:
                        try:
                            # 获取邮件详情
                            status, msg_data = imap.fetch(msg_id, "(RFC822)")
                            if status == "OK":
                                for response_part in msg_data:
                                    if isinstance(response_part, tuple):
                                        msg = email.message_from_bytes(response_part[1])
                                        from_header = decode_str(msg.get("From"))
                                        subject = decode_str(msg.get("Subject"))

                                        all_matched.append({
                                            'id': msg_id.decode() if isinstance(msg_id, bytes) else msg_id,
                                            'from': from_header,
                                            'subject': subject
                                        })

                                        # 标记为已读
                                        imap.store(msg_id, '+FLAGS', '\\Seen')
                                        total_marked += 1
                        except Exception as e:
                            pass  # 跳过处理失败的邮件
            except Exception as e:
                pass  # 跳过失败的查询

        imap.close()
        imap.logout()

        # 记录日志
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] Cleaned {total_marked} security/verification emails\n"

        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_entry)
            for item in all_matched[:10]:  # 只记录前10个
                from_str = item['from'][:50]
                subject_str = item['subject'][:60]
                f.write(f"  - {from_str} | {subject_str}\n")
            if len(all_matched) > 10:
                f.write(f"  ... and {len(all_matched) - 10} more\n")

        print(f"Cleaned {total_marked} verification/security emails")
        print(f"Log saved to: {LOG_FILE}")

        return total_marked

    except Exception as e:
        error_msg = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Clean failed: {str(e)}\n"
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(error_msg)
        print(f"Clean failed: {str(e)}")
        return 0

if __name__ == "__main__":
    print("Starting Gmail security email cleanup...")
    count = clean_security_emails()
    if count > 0:
        print(f"Successfully processed {count} emails")
    else:
        print("No emails found to clean")
