#!/usr/bin/env python3
"""
邮件检查和智能回复助手
作者: 胡搞 🐙
检查时间: 每天 09:00 和 16:00
功能: 检查邮件、按重要性分级、撰写草稿回复
"""

import os
import sys
import imaplib
import email
from email.header import decode_header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from datetime import datetime, timedelta
import re
import json

# 邮箱配置
EMAIL_CONFIGS = {
    'gmail': {
        'name': 'Gmail (个人)',
        'server': 'imap.gmail.com',
        'port': 993,
        'user': os.getenv('GMAIL_USER'),
        'password': os.getenv('GMAIL_APP_PASSWORD'),
        'priority': 1
    },
    'qq_work': {
        'name': 'QQ 邮箱 (工作)',
        'server': 'imap.qq.com',
        'port': 993,
        'user': os.getenv('QQMAIL_WORK_USER'),
        'password': os.getenv('QQMAIL_WORKER_AUTH_CODE'),
        'priority': 2
    },
    'qq_personal': {
        'name': 'QQ 邮箱 (个人)',
        'server': 'imap.qq.com',
        'port': 993,
        'user': os.getenv('QQMAIL_PERSONAL_USER'),
        'password': os.getenv('QQMAIL_PERSONAL_AUTH_CODE'),
        'priority': 3
    }
}

# 紧急关键词
URGENT_KEYWORDS = [
    '紧急', '故障', '告警', '安全', '攻击', '服务器', '异常',
    'urgent', 'alert', 'security', 'attack', 'down', 'error', 'exception'
]

# 需要回复的关键词
REPLY_KEYWORDS = [
    '请回复', '请确认', '需要反馈', '等待答复', '请处理',
    'please reply', 'confirm', 'need feedback'
]

class EmailChecker:
    def __init__(self):
        self.results = {
            'total_unread': 0,
            'urgent': [],
            'important': [],
            'normal': [],
            'need_reply': [],
            'drafts': [],
            'errors': []
        }

    def decode_str(self, s):
        """解码字符串"""
        if isinstance(s, str):
            return s
        decoded = decode_header(s)[0]
        if isinstance(decoded[0], bytes):
            return decoded[0].decode(decoded[1] or 'utf-8', errors='ignore')
        return decoded[0]

    def check_urgency(self, subject, sender, body):
        """检查邮件紧急程度和是否需要回复"""
        subject_lower = subject.lower()
        sender_lower = sender.lower()
        body_lower = body.lower() if body else ""

        # 检查紧急关键词
        for keyword in URGENT_KEYWORDS:
            if keyword.lower() in subject_lower or keyword.lower() in sender_lower:
                return 'urgent', True
        
        # 检查是否需要回复
        need_reply = False
        for keyword in REPLY_KEYWORDS:
            if keyword.lower() in subject_lower or keyword.lower() in body_lower:
                need_reply = True
                break

        if need_reply:
            return 'important', True
        return 'normal', False

    def connect_mailbox(self, config):
        """连接邮箱"""
        try:
            mail = imaplib.IMAP4_SSL(config['server'], config['port'])
            mail.login(config['user'], config['password'])
            mail.select('INBOX')
            return mail
        except Exception as e:
            self.results['errors'].append({
                'mailbox': config['name'],
                'error': str(e)
            })
            return None

    def generate_draft_reply(self, email_info):
        """生成草稿回复"""
        subject = email_info['subject']
        sender = email_info['sender']
        body = email_info.get('body', '')

        # 根据邮件类型生成回复
        if '确认' in subject or 'confirm' in subject.lower():
            draft = f"""你好,

感谢你的邮件关于: {subject}

我的理解是: [需要确认的事项]

建议回复: [草稿内容]

请姐姐审阅后确认发送。

---
胡搞 🐙
运维章鱼
"""
        elif '请处理' in subject or '请回复' in subject:
            draft = f"""你好,

收到你的邮件: {subject}

关于这个问题,我建议:
1. [分析或行动项 1]
2. [分析或行动项 2]

请姐姐审阅后确认发送。

---
胡搞 🐙
运维章鱼
"""
        else:
            draft = f"""你好,

收到你的邮件: {subject}

我会尽快处理此事。

如有需要,请随时联系。

---
胡搞 🐙
运维章鱼
"""

        return draft

    def check_mailbox(self, key, config):
        """检查单个邮箱"""
        print(f"\n📧 {config['name']}")
        print("=" * 50)

        mail = self.connect_mailbox(config)
        if not mail:
            print(f"❌ 连接失败")
            return

        try:
            # 搜索未读邮件
            status, messages = mail.search(None, 'UNSEEN')

            if status != 'OK':
                print(f"⚠️ 搜索失败")
                return

            email_ids = messages[0].split()
            unread_count = len(email_ids)

            print(f"未读邮件: {unread_count} 封")
            self.results['total_unread'] += unread_count

            if unread_count == 0:
                print("✅ 无新邮件")
                return

            # 获取所有未读邮件
            for email_id in email_ids:
                # 获取邮件
                _, msg_data = mail.fetch(email_id, '(RFC822)')
                raw_email = msg_data[0][1]
                msg = email.message_from_bytes(raw_email)

                # 解析邮件头
                subject = self.decode_str(msg['Subject'])
                sender = self.decode_str(msg['From'])
                date = msg['Date']

                # 解析邮件正文
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            try:
                                body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                                break
                            except:
                                pass
                else:
                    try:
                        body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
                    except:
                        body = str(msg.get_payload())

                # 检查紧急程度和是否需要回复
                urgency, need_reply = self.check_urgency(subject, sender, body)

                email_info = {
                    'mailbox': config['name'],
                    'subject': subject,
                    'sender': sender,
                    'date': date,
                    'body': body[:500],  # 只保留前500字符
                    'priority': config['priority'],
                    'need_reply': need_reply
                }

                if urgency == 'urgent':
                    self.results['urgent'].append(email_info)
                    print(f"🔴 [紧急] {subject[:50]}...")
                    print(f"   发件人: {sender}")
                    
                elif urgency == 'important':
                    self.results['important'].append(email_info)
                    print(f"🟡 [重要] {subject[:50]}...")
                    print(f"   发件人: {sender}")
                    if need_reply:
                        self.results['need_reply'].append(email_info)
                        # 生成草稿回复
                        draft = self.generate_draft_reply(email_info)
                        self.results['drafts'].append({
                            'to': sender,
                            'subject': f"Re: {subject}",
                            'draft': draft
                        })
                        print(f"   ✅ 草稿已生成")
                        
                else:
                    self.results['normal'].append(email_info)
                    print(f"🟢 [普通] {subject[:50]}...")

        except Exception as e:
            print(f"❌ 检查出错: {e}")
            self.results['errors'].append({
                'mailbox': config['name'],
                'error': str(e)
            })
        finally:
            try:
                mail.close()
                mail.logout()
            except:
                pass

    def run(self):
        """运行所有邮箱检查"""
        print("=" * 50)
        print("🐙 章鱼邮箱检查 - 开始")
        print(f"检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 50)

        # 按优先级排序检查
        sorted_configs = sorted(EMAIL_CONFIGS.items(), key=lambda x: x[1]['priority'])

        for key, config in sorted_configs:
            self.check_mailbox(key, config)

        # 输出汇总
        self.print_summary()

    def print_summary(self):
        """打印汇总报告"""
        print("\n" + "=" * 50)
        print("📊 检查汇总")
        print("=" * 50)

        print(f"总未读邮件: {self.results['total_unread']} 封")
        print(f"🔴 紧急: {len(self.results['urgent'])} 封")
        print(f"🟡 重要: {len(self.results['important'])} 封")
        print(f"🟢 普通: {len(self.results['normal'])} 封")
        print(f"✉️ 需要回复: {len(self.results['need_reply'])} 封")
        print(f"📝 草稿已生成: {len(self.results['drafts'])} 封")

        if self.results['errors']:
            print(f"\n❌ 错误: {len(self.results['errors'])} 个")
            for error in self.results['errors']:
                print(f"   - {error['mailbox']}: {error['error']}")

        # 如果有紧急邮件,立即通知
        if self.results['urgent']:
            print("\n" + "=" * 50)
            print("🚨 紧急邮件 - 立即处理!")
            print("=" * 50)
            for email in self.results['urgent']:
                print(f"\n主题: {email['subject']}")
                print(f"发件人: {email['sender']}")
                print(f"邮箱: {email['mailbox']}")

        # 显示草稿回复
        if self.results['drafts']:
            print("\n" + "=" * 50)
            print("📝 草稿回复 - 请审阅")
            print("=" * 50)
            for i, draft in enumerate(self.results['drafts'], 1):
                print(f"\n【草稿 {i}】")
                print(f"收件人: {draft['to']}")
                print(f"主题: {draft['subject']}")
                print(f"内容:\n{draft['draft']}")
                print("-" * 50)

        # 保存结果到 JSON
        result_file = '/root/.openclaw/workspace-feishu-ops/workspace-feishu-ops/email-check-result.json'
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        print(f"\n💾 结果已保存到: {result_file}")

if __name__ == '__main__':
    checker = EmailChecker()
    checker.run()
