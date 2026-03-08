#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
脚本名称: clean_gmail_marketing.py
脚本功能: 自动清理 Gmail 营销广告邮件
作者: 小猩
创建日期: 2026-02-17
版本: 1.0.0

版本记录:
    v1.0.0 (2026-02-17) - 初始版本
"""

"""
清理 Gmail 营销类和订阅类邮件
- 营销类：全部删除
- 订阅类：相同发件人只保留最新一封
"""

import imaplib
import email
from email.header import decode_header
import os
import sys
from collections import defaultdict
from datetime import datetime

# 强制使用 UTF-8 编码
if sys.version_info[0] >= 3:
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 配置
GMAIL_USER = os.environ.get("GMAIL_USER")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "")

LOG_FILE = "/root/.openclaw/workspace/Log/gmail_clean_marketing.log"

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

def extract_sender(from_header):
    """提取发件人邮箱"""
    """从 'Name <email@example.com>' 或 'email@example.com' 提取邮箱"""
    if '<' in from_header:
        # 提取 < > 之间的邮箱
        start = from_header.find('<') + 1
        end = from_header.find('>')
        if start > 0 and end > start:
            return from_header[start:end].strip().lower()
    # 如果没有 < >，直接返回（去除前后空格）
    return from_header.strip().lower()

def is_marketing_email(subject, from_header):
    """判断是否为营销类邮件"""
    keywords = [
        '限时', '优惠', '促销', '折扣', '秒杀', '特价',
        'limited time', 'sale', 'discount', 'promo', 'offer', 'deal',
        '抢购', '立减', '满减', '优惠券', '代金券',
        '闪购', '团购', '拼团',
        'unsubscribe', '退订', '邮件订阅', 'newsletter'
    ]
    subject_lower = subject.lower()
    from_lower = from_header.lower()
    return any(keyword in subject_lower or keyword in from_lower for keyword in keywords)

def is_subscription_email(subject, from_header):
    """判断是否为订阅类邮件（非营销）"""
    # 订阅类特征：定期发送的内容更新
    keywords = [
        'daily', 'weekly', 'newsletter', 'digest', 'update',
        '早报', '日报', '周刊', '更新', '推送',
        'substack', 'medium', 'mirror', 'blog'
    ]
    subject_lower = subject.lower()
    from_lower = from_header.lower()
    return any(keyword in subject_lower or keyword in from_lower for keyword in keywords)

def clean_marketing_emails():
    """清理营销类和订阅类邮件"""
    try:
        # 连接到 Gmail IMAP
        imap = imaplib.IMAP4_SSL("imap.gmail.com")
        imap.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        imap.select("INBOX")

        # 获取所有未读邮件
        status, messages = imap.search(None, "UNSEEN")
        if status != "OK" or not messages[0]:
            imap.close()
            imap.logout()
            print("No unread emails found")
            return 0

        email_ids = messages[0].split()

        # 分类邮件
        marketing_to_delete = []
        subscription_emails = defaultdict(list)  # {sender: [(msg_id, subject), ...]}

        for msg_id in email_ids:
            try:
                status, msg_data = imap.fetch(msg_id, "(RFC822)")
                if status != "OK":
                    continue

                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        from_header = decode_str(msg.get("From", ""))
                        subject = decode_str(msg.get("Subject", ""))

                        sender = extract_sender(from_header)

                        if is_marketing_email(subject, from_header):
                            marketing_to_delete.append({
                                'id': msg_id.decode() if isinstance(msg_id, bytes) else msg_id,
                                'from': from_header,
                                'subject': subject
                            })
                        elif is_subscription_email(subject, from_header):
                            subscription_emails[sender].append({
                                'id': msg_id.decode() if isinstance(msg_id, bytes) else msg_id,
                                'from': from_header,
                                'subject': subject
                            })
            except Exception as e:
                pass  # 跳过处理失败的邮件

        # 执行删除操作
        deleted_count = 0
        kept_count = 0

        # 1. 删除所有营销类邮件
        for email_info in marketing_to_delete:
            try:
                imap.store(email_info['id'], '+FLAGS', '\\Seen')
                imap.store(email_info['id'], '+FLAGS', '\\Deleted')
                deleted_count += 1
            except:
                pass

        # 2. 订阅类：每个发件人只保留最新一封（假设邮件ID越大越新）
        for sender, emails in subscription_emails.items():
            if len(emails) > 1:
                # 按ID排序，保留最大的（最新的）
                emails_sorted = sorted(emails, key=lambda x: int(x['id']) if x['id'].isdigit() else 0)
                # 删除除了最后一封的所有邮件
                for email_info in emails_sorted[:-1]:
                    try:
                        imap.store(email_info['id'], '+FLAGS', '\\Seen')
                        imap.store(email_info['id'], '+FLAGS', '\\Deleted')
                        deleted_count += 1
                    except:
                        pass
                # 标记保留的为已读
                try:
                    imap.store(emails_sorted[-1]['id'], '+FLAGS', '\\Seen')
                    kept_count += 1
                except:
                    pass
            else:
                # 只有一封，标记为已读
                try:
                    imap.store(emails[0]['id'], '+FLAGS', '\\Seen')
                    kept_count += 1
                except:
                    pass

        # 永久删除（EXPUNGE）
        imap.expunge()
        imap.close()
        imap.logout()

        # 记录日志
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] Marketing/Subscription cleanup:\\n")
            f.write(f"  - Deleted: {deleted_count} emails\\n")
            f.write(f"  - Kept (latest): {kept_count} emails\\n")
            if marketing_to_delete:
                f.write(f"  - Marketing emails deleted:\\n")
                for item in marketing_to_delete[:5]:
                    from_str = item['from'][:50]
                    subject_str = item['subject'][:60]
                    f.write(f"    * {from_str} | {subject_str}\\n")
                if len(marketing_to_delete) > 5:
                    f.write(f"    ... and {len(marketing_to_delete) - 5} more\\n")

        print(f"Deleted {deleted_count} marketing/subscription emails")
        print(f"Kept {kept_count} latest subscription emails")
        print(f"Log saved to: {LOG_FILE}")

        return deleted_count

    except Exception as e:
        error_msg = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Cleanup failed: {str(e)}\\n"
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(error_msg)
        print(f"Cleanup failed: {str(e)}")
        return 0

if __name__ == "__main__":
    print("Starting Gmail marketing/subscription cleanup...")
    count = clean_marketing_emails()
    if count > 0:
        print(f"Successfully processed {count} emails")
    else:
        print("No emails found to clean")
