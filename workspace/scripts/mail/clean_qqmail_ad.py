#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
脚本名称: clean_qqmail_ad.py
脚本功能: 自动清理 QQ 邮箱广告和营销邮件
作者: 小猩 🦧
创建日期: 2026-02-22
版本: 1.0.0

版本记录:
    v1.0.0 (2026-02-22) - 初始版本，基于 Gmail 营销清理脚本改造
"""

"""
清理 QQ 邮箱广告和营销类邮件
- 广告类：全部删除
- 营销类：相同发件人只保留最新一封
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
LOG_FILE = os.path.join(LOGS_DIR, "qqmail_clean_ad.log")

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

def is_ad_email(subject, from_header, sender):
    """判断是否为广告类邮件"""
    # QQ邮箱广告特征
    ad_senders = [
        'qqmail@qq.com', 'service@qq.com', 'qq.com',
        'tmall.com', 'taobao.com', 'jd.com', 'pinduoduo.com',
        'vip.com', 'suning.com', 'gome.com.cn'
    ]
    
    ad_keywords = [
        '广告', '推广', '营销', '优惠券', '限时', '优惠', '促销',
        '折扣', '秒杀', '特价', '抢购', '立减', '满减',
        '代金券', '闪购', '团购', '拼团', '红包', '返现',
        'limited time', 'sale', 'discount', 'promo', 'offer', 'deal',
        'unsubscribe', '退订', '邮件订阅', 'newsletter'
    ]
    
    subject_lower = subject.lower()
    from_lower = from_header.lower()
    sender_lower = sender.lower()
    
    # 检查发件人域名
    for ad_sender in ad_senders:
        if ad_sender in sender_lower:
            return True
    
    # 检查关键词
    return any(keyword in subject_lower or keyword in from_lower for keyword in ad_keywords)

def is_marketing_email(subject, from_header):
    """判断是否为营销类邮件（非广告）"""
    # 营销类特征：电商、品牌推送等
    keywords = [
        '新品', '上架', '热卖', '推荐', '爆款', '爆款',
        '会员', '积分', '等级', '权益',
        '活动', '专场', '盛典', '狂欢',
        'new arrival', 'best seller', 'recommend',
        'member', 'vip', 'exclusive'
    ]
    subject_lower = subject.lower()
    from_lower = from_header.lower()
    return any(keyword in subject_lower or keyword in from_lower for keyword in keywords)

def clean_ad_emails():
    """清理广告和营销类邮件"""
    try:
        # 连接到 QQ 邮箱 IMAP
        imap = imaplib.IMAP4_SSL("imap.qq.com", 993)
        imap.login(QQMAIL_USER, QQMAIL_PASSWORD)
        imap.select("INBOX")

        # 获取所有未读邮件
        status, messages = imap.search(None, "UNSEEN")
        if status != "OK" or not messages[0]:
            imap.close()
            imap.logout()
            print("✅ 没有未读邮件")
            return 0

        email_ids = messages[0].split()

        # 分类邮件
        ad_to_delete = []
        marketing_emails = defaultdict(list)  # {sender: [(msg_id, subject), ...]}
        normal_emails = []

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

                        if is_ad_email(subject, from_header, sender):
                            ad_to_delete.append({
                                'id': msg_id.decode() if isinstance(msg_id, bytes) else msg_id,
                                'from': from_header,
                                'subject': subject,
                                'type': 'ad'
                            })
                        elif is_marketing_email(subject, from_header):
                            marketing_emails[sender].append({
                                'id': msg_id.decode() if isinstance(msg_id, bytes) else msg_id,
                                'from': from_header,
                                'subject': subject,
                                'type': 'marketing'
                            })
                        else:
                            normal_emails.append(msg_id)
            except Exception as e:
                pass  # 跳过处理失败的邮件

        # 执行删除操作
        deleted_count = 0
        kept_marketing = 0
        kept_normal = len(normal_emails)

        # 1. 删除所有广告类邮件
        for email_info in ad_to_delete:
            try:
                imap.store(email_info['id'], '+FLAGS', '\\Seen')
                imap.store(email_info['id'], '+FLAGS', '\\Deleted')
                deleted_count += 1
            except:
                pass

        # 2. 营销类：每个发件人只保留最新一封
        for sender, emails in marketing_emails.items():
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
                    kept_marketing += 1
                except:
                    pass
            else:
                # 只有一封，标记为已读
                try:
                    imap.store(emails[0]['id'], '+FLAGS', '\\Seen')
                    kept_marketing += 1
                except:
                    pass

        # 标记普通邮件为已读
        for msg_id in normal_emails:
            try:
                imap.store(msg_id, '+FLAGS', '\\Seen')
            except:
                pass

        # 永久删除（EXPUNGE）
        imap.expunge()
        imap.close()
        imap.logout()

        # 记录日志
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] QQ邮箱清理完成:\\n")
            f.write(f"  - 🗑️ 删除: {deleted_count} 封（广告+重复营销）\\n")
            f.write(f"  - ✅ 保留: {kept_marketing} 封营销（最新）+ {kept_normal} 封普通\\n")
            if ad_to_delete:
                f.write(f"  - 删除的广告邮件:\\n")
                for item in ad_to_delete[:5]:
                    from_str = item['from'][:50]
                    subject_str = item['subject'][:60]
                    f.write(f"    * {from_str} | {subject_str}\\n")
                if len(ad_to_delete) > 5:
                    f.write(f"    ... 还有 {len(ad_to_delete) - 5} 封\\n")

        print(f"✅ QQ邮箱清理完成！")
        print(f"🗑️ 删除: {deleted_count} 封")
        print(f"✅ 保留: {kept_marketing} 封营销（最新）+ {kept_normal} 封普通")
        print(f"📝 日志: {LOG_FILE}")

        return deleted_count

    except Exception as e:
        error_msg = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 清理失败: {str(e)}\\n"
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(error_msg)
        print(f"❌ 清理失败: {str(e)}")
        return 0

if __name__ == "__main__":
    print("🚀 开始清理 QQ 邮箱广告...")
    count = clean_ad_emails()
    if count > 0:
        print(f"🎉 成功处理 {count} 封邮件")
    else:
        print("📭 没有需要清理的邮件")
