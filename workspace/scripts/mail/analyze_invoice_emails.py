#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析QQ邮箱1月份发票相关邮件
"""

import imaplib
import email
from email.header import decode_header
from datetime import datetime
import os
import re

# 加载环境变量
def load_env_file():
    env_file = "/root/.openclaw/workspace/.env.qqmail"
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#') and '=' in line:
                    line = line.strip()
                    if line.startswith('export '):
                        line = line[7:]
                    key, value = line.split('=', 1)
                    value = value.strip('"').strip("'")
                    os.environ[key] = value

load_env_file()

# 发票相关关键词
INVOICE_KEYWORDS = ['发票', '电子发票', '增值税', 'invoice', 'receipt', '报销', '开票', 'invoice']

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

def is_invoice_email(subject, from_addr):
    """判断是否为发票相关邮件"""
    text = (subject + ' ' + from_addr).lower()
    return any(kw.lower() in text for kw in INVOICE_KEYWORDS)

def extract_amount(subject):
    """尝试从主题中提取金额"""
    # 匹配 ¥123.45 或 123.45元 或 ￥123.45
    patterns = [
        r'[¥￥]\s*(\d+(?:\.\d+)?)',
        r'(\d+(?:\.\d+)?)\s*元',
        r'金额[:：]?\s*(\d+(?:\.\d+)?)',
    ]
    for pattern in patterns:
        match = re.search(pattern, subject)
        if match:
            return float(match.group(1))
    return None

def analyze_inbox(user, auth_code, label):
    """分析指定邮箱的2月份发票邮件"""
    results = []
    
    try:
        imap = imaplib.IMAP4_SSL("imap.qq.com", 993)
        imap.login(user, auth_code)
        imap.select("INBOX")
        
        # 搜索2026年2月份的邮件 (2月1日至今)
        # IMAP日期格式: SINCE "01-Feb-2026"
        status, messages = imap.search(None, 'SINCE "01-Feb-2026"')
        
        if status != "OK":
            print(f"❌ [{label}] 搜索邮件失败")
            return results
        
        email_ids = messages[0].split()
        print(f"📧 [{label}] 2月份共有 {len(email_ids)} 封邮件")
        
        invoice_count = 0
        for eid in email_ids:
            status, msg_data = imap.fetch(eid, "(RFC822)")
            if status != "OK":
                continue
            
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject = decode_str(msg.get("Subject"))
                    from_addr = decode_str(msg.get("From"))
                    date_str = msg.get("Date")
                    
                    if is_invoice_email(subject, from_addr):
                        invoice_count += 1
                        amount = extract_amount(subject)
                        results.append({
                            'date': date_str,
                            'from': from_addr,
                            'subject': subject,
                            'amount': amount
                        })
        
        imap.close()
        imap.logout()
        
        print(f"📄 [{label}] 找到 {invoice_count} 封发票相关邮件")
        return results
        
    except Exception as e:
        print(f"❌ [{label}] 分析失败: {e}")
        return results

def main():
    print("=" * 60)
    print("📊 QQ邮箱2月份发票邮件统计分析")
    print("=" * 60)
    
    all_invoices = []
    
    # 分析工作QQ邮箱
    work_user = os.environ.get("QQMAIL_USER")
    work_auth = os.environ.get("QQMAIL_AUTH_CODE")
    if work_user and work_auth:
        work_invoices = analyze_inbox(work_user, work_auth, "工作邮箱")
        all_invoices.extend(work_invoices)
    else:
        print("⚠️ 工作邮箱配置缺失")
    
    print()
    
    # 分析个人QQ邮箱
    personal_user = os.environ.get("QQMAIL_PERSONAL_USER")
    personal_auth = os.environ.get("QQMAIL_PERSONAL_AUTH_CODE")
    if personal_user and personal_auth:
        personal_invoices = analyze_inbox(personal_user, personal_auth, "个人邮箱")
        all_invoices.extend(personal_invoices)
    else:
        print("⚠️ 个人邮箱配置缺失")
    
    # 输出统计结果
    print()
    print("=" * 60)
    print("📈 统计结果汇总")
    print("=" * 60)
    print(f"总计发票相关邮件: {len(all_invoices)} 封")
    print()
    
    if all_invoices:
        # 按日期排序
        all_invoices.sort(key=lambda x: x['date'] or '')
        
        print("📋 发票邮件明细:")
        print("-" * 60)
        total_amount = 0
        for i, inv in enumerate(all_invoices, 1):
            amount_str = f"¥{inv['amount']:.2f}" if inv['amount'] else "金额未知"
            print(f"{i}. [{inv['date'][:16] if inv['date'] else '日期未知'}]")
            print(f"   发件人: {inv['from'][:40]}")
            print(f"   主题: {inv['subject'][:50]}")
            print(f"   金额: {amount_str}")
            if inv['amount']:
                total_amount += inv['amount']
            print()
        
        print("-" * 60)
        print(f"💰 可识别金额总计: ¥{total_amount:.2f}")
    else:
        print("📭 未找到2月份的发票相关邮件")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
