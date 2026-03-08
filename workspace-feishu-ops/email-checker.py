#!/usr/bin/env python3
"""
邮箱检查器 - 胡搞的智能邮件助手
支持多个 IMAP 邮箱,自动分类和优先级判断
"""

import os
import imaplib
import email
from email.header import decode_header
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
        'priority': 1  # 最高优先级
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
    '紧急', '故障', '告警', '安全', '攻击',
    'urgent', 'alert', 'security', 'attack', 'down',
    '服务器', '异常', 'error', 'exception'
]

# 重要发件人 (可配置)
IMPORTANT_SENDERS = [
    'github.com',
    'noreply',
    'alert'
]

class EmailChecker:
    def __init__(self):
        self.results = {
            'total_unread': 0,
            'urgent': [],
            'important': [],
            'normal': [],
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

    def check_urgency(self, subject, sender):
        """检查邮件紧急程度"""
        subject_lower = subject.lower()
        sender_lower = sender.lower()

        # 检查紧急关键词
        for keyword in URGENT_KEYWORDS:
            if keyword.lower() in subject_lower or keyword.lower() in sender_lower:
                return 'urgent'

        # 检查重要发件人
        for important_sender in IMPORTANT_SENDERS:
            if important_sender.lower() in sender_lower:
                return 'important'

        return 'normal'

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

            # 获取最近5封未读邮件
            recent_emails = email_ids[-5:] if unread_count > 5 else email_ids

            for email_id in recent_emails:
                # 获取邮件
                _, msg_data = mail.fetch(email_id, '(RFC822)')
                raw_email = msg_data[0][1]
                msg = email.message_from_bytes(raw_email)

                # 解析邮件头
                subject = self.decode_str(msg['Subject'])
                sender = self.decode_str(msg['From'])
                date = msg['Date']

                # 检查紧急程度
                urgency = self.check_urgency(subject, sender)

                email_info = {
                    'mailbox': config['name'],
                    'subject': subject,
                    'sender': sender,
                    'date': date,
                    'priority': config['priority']
                }

                if urgency == 'urgent':
                    self.results['urgent'].append(email_info)
                    print(f"🔴 [紧急] {subject[:50]}...")
                    print(f"   发件人: {sender}")
                elif urgency == 'important':
                    self.results['important'].append(email_info)
                    print(f"🟡 [重要] {subject[:50]}...")
                    print(f"   发件人: {sender}")
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

        # 保存结果到 JSON
        self.save_results()

    def save_results(self):
        """保存检查结果"""
        result_file = '/root/.openclaw/workspace-feishu-ops/email-check-result.json'
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        print(f"\n💾 结果已保存到: {result_file}")

if __name__ == '__main__':
    checker = EmailChecker()
    checker.run()
