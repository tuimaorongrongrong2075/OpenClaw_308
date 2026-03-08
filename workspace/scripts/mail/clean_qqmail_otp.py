#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
脚本名称: clean_qqmail_otp.py
脚本功能: 自动删除 QQ 邮箱验证码邮件
作者: 小猩 🦧
创建日期: 2026-02-22
版本: 1.0.0

版本记录:
    v1.0.0 (2026-02-22) - 初始版本
"""

"""
删除 QQ 邮箱验证码邮件（OTP）
- 自动识别并删除各类验证码邮件
- 支持中英文验证码关键词
"""

import imaplib
import email
from email.header import decode_header
import os
import sys
from datetime import datetime, timedelta
import re

# 强制使用 UTF-8 编码
if sys.version_info[0] >= 3:
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 检查必需的环境变量
def check_required_env():
    """检查必需的环境变量是否已设置"""
    required = {
        'QQMAIL_USER': 'QQ邮箱账号',
        'QQMAIL_PASSWORD': 'QQ邮箱授权码'
    }
    
    missing = []
    for key, desc in required.items():
        if not os.environ.get(key):
            missing.append(f"{key} ({desc})")
    
    if missing:
        print("❌ 缺少以下环境变量:")
        for item in missing:
            print(f"   - {item}")
        print("\n💡 请设置环境变量 QQMAIL_USER 和 QQMAIL_PASSWORD")
        return False
    return True

# 先检查环境变量
if not check_required_env():
    exit(1)

# 配置（支持工作和个人邮箱）
QQMAIL_USER = os.environ.get("QQMAIL_USER", "")
QQMAIL_PASSWORD = os.environ.get("QQMAIL_PASSWORD", "")

# 脚本目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "logs")
os.makedirs(LOGS_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOGS_DIR, "qqmail_clean_otp.log")

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

def is_otp_email(subject, from_header, body_text):
    """判断是否为验证码邮件"""
    # 验证码关键词（中英文）
    otp_keywords = [
        '验证码', '校验码', '动态码', '安全码', '确认码',
        'code', 'otp', 'verification code', 'verify', 'auth code',
        'verification', 'authenticate', 'passcode', 'pin',
        '一次性密码', '登录码', '注册码', '验证', '确认'
    ]
    
    # 常见验证码发件人
    otp_senders = [
        'noreply', 'no-reply', 'notification', 'verify', 'auth',
        'security', 'account', 'service', 'support', 'code'
    ]
    
    subject_lower = subject.lower()
    from_lower = from_header.lower()
    body_lower = body_text.lower()
    
    # 检查发件人
    for sender in otp_senders:
        if sender in from_lower:
            # 发件人匹配时，还需要检查标题或正文包含验证码关键词
            if any(keyword in subject_lower or keyword in body_lower for keyword in otp_keywords):
                return True
    
    # 检查关键词
    keyword_found = any(keyword in subject_lower or keyword in body_lower for keyword in otp_keywords)
    
    # 验证码邮件通常包含数字代码（4-8位数字）
    has_digit_code = False
    # 查找4-8位连续数字
    digit_patterns = re.findall(r'\b\d{4,8}\b', body_lower)
    if digit_patterns:
        has_digit_code = True
    
    # 同时包含验证码关键词和数字代码
    return keyword_found and has_digit_code

def get_email_body(msg):
    """提取邮件正文内容"""
    body = ""
    try:
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain" or content_type == "text/html":
                    try:
                        payload = part.get_payload(decode=True)
                        if payload:
                            body += payload.decode('utf-8', errors='ignore')
                    except:
                        pass
        else:
            try:
                payload = msg.get_payload(decode=True)
                if payload:
                    body = payload.decode('utf-8', errors='ignore')
            except:
                pass
    except:
        pass
    return body

def clean_otp_emails():
    """删除验证码邮件"""
    try:
        # 连接到 QQ 邮箱 IMAP
        imap = imaplib.IMAP4_SSL("imap.qq.com", 993)
        imap.login(QQMAIL_USER, QQMAIL_PASSWORD)
        imap.select("INBOX")

        # 获取所有邮件（包括已读和未读）
        status, messages = imap.search(None, "ALL")
        if status != "OK" or not messages[0]:
            imap.close()
            imap.logout()
            print("✅ 没有邮件")
            return 0

        email_ids = messages[0].split()

        # 找出验证码邮件
        otp_to_delete = []

        # 只检查最近的500封邮件（避免处理太多）
        recent_emails = email_ids[-500:] if len(email_ids) > 500 else email_ids

        for msg_id in recent_emails:
            try:
                status, msg_data = imap.fetch(msg_id, "(RFC822)")
                if status != "OK":
                    continue

                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        from_header = decode_str(msg.get("From", ""))
                        subject = decode_str(msg.get("Subject", ""))
                        body = get_email_body(msg)

                        if is_otp_email(subject, from_header, body):
                            otp_to_delete.append({
                                'id': msg_id.decode() if isinstance(msg_id, bytes) else msg_id,
                                'from': from_header,
                                'subject': subject
                            })
            except Exception as e:
                pass  # 跳过处理失败的邮件

        # 执行删除操作
        deleted_count = 0

        for email_info in otp_to_delete:
            try:
                # 标记为已读并删除
                imap.store(email_info['id'], '+FLAGS', '\\Seen')
                imap.store(email_info['id'], '+FLAGS', '\\Deleted')
                deleted_count += 1
            except:
                pass

        # 永久删除（EXPUNGE）
        if deleted_count > 0:
            imap.expunge()

        imap.close()
        imap.logout()

        # 记录日志
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] QQ邮箱验证码清理完成:\\n")
            f.write(f"  - 🗑️ 删除: {deleted_count} 封验证码邮件\\n")
            if otp_to_delete:
                f.write(f"  - 删除的验证码邮件:\\n")
                for item in otp_to_delete[:5]:
                    from_str = item['from'][:50]
                    subject_str = item['subject'][:60]
                    f.write(f"    * {from_str} | {subject_str}\\n")
                if len(otp_to_delete) > 5:
                    f.write(f"    ... 还有 {len(otp_to_delete) - 5} 封\\n")

        print(f"✅ QQ邮箱验证码清理完成！")
        print(f"🗑️ 删除: {deleted_count} 封")
        print(f"📝 日志: {LOG_FILE}")

        return deleted_count

    except Exception as e:
        error_msg = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 清理失败: {str(e)}\\n"
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(error_msg)
        print(f"❌ 清理失败: {str(e)}")
        return 0

if __name__ == "__main__":
    print("🚀 开始清理 QQ 邮箱验证码邮件...")
    count = clean_otp_emails()
    if count > 0:
        print(f"🎉 成功删除 {count} 封验证码邮件")
    else:
        print("📭 没有找到验证码邮件")
