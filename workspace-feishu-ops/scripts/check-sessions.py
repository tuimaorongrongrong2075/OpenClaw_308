#!/usr/bin/env python3
"""
会话状态检查脚本
作者: 胡搞 🐙
用途: 获取所有会话信息,提取关键词,用于心跳报告
"""

import subprocess
import json
from datetime import datetime
import os

def get_sessions():
    """获取会话列表"""
    try:
        # 使用 tool 方式调用
        import sys
        sys.path.insert(0, '/root/.local/share/pnpm/global/5/.pnpm/openclaw@2026.3.2_@napi-rs+canvas@0.1.95_hono@4.12.5_node-llama-cpp@3.16.2/node_modules/openclaw')
        
        # 直接读取会话文件
        session_dir = "/root/.openclaw/agents/feishu-ops/sessions"
        sessions = []
        
        for filename in os.listdir(session_dir):
            if filename.endswith('.jsonl'):
                file_path = os.path.join(session_dir, filename)
                
                # 读取第一行获取会话信息
                with open(file_path, 'r') as f:
                    first_line = f.readline()
                    try:
                        session_data = json.loads(first_line)
                        session_id = session_data.get('id', 'unknown')
                        timestamp = session_data.get('timestamp', '')
                        
                        # 解析时间戳
                        try:
                            start_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                        except:
                            start_time = datetime.fromtimestamp(float(timestamp) / 1000)
                        
                        # 读取最后几条消息
                        messages = []
                        with open(file_path, 'r') as f:
                            lines = f.readlines()
                            for line in lines[-10:]:  # 最后10条
                                try:
                                    msg_data = json.loads(line)
                                    if msg_data.get('type') == 'message':
                                        msg = msg_data.get('message', {})
                                        role = msg.get('role', 'unknown')
                                        content = msg.get('content', [])
                                        
                                        if content and isinstance(content, list):
                                            text = content[0].get('text', '') if isinstance(content[0], dict) else str(content[0])
                                            
                                            messages.append({
                                                'role': role,
                                                'text': text[:200],  # 只保留前200字符
                                                'timestamp': msg.get('timestamp', 0)
                                            })
                                except:
                                    pass
                        
                        sessions.append({
                            'sessionId': session_id,
                            'startTime': start_time.strftime('%Y-%m-%d %H:%M:%S'),
                            'lastMessageTime': datetime.fromtimestamp(messages[-1]['timestamp'] / 1000).strftime('%Y-%m-%d %H:%M:%S') if messages else start_time.strftime('%Y-%m-%d %H:%M:%S'),
                            'messages': messages
                        })
                    except:
                        pass
        
        return sessions
    except Exception as e:
        print(f"获取会话失败: {e}")
        return []

def extract_keywords(text):
    """提取关键词"""
    if not text:
        return []
    
    # 简单分词
    words = text.split()
    
    # 过滤掉短词和常见词
    stop_words = {'的', '是', '了', '在', '有', '和', '我', '你', '他', '她', '它', 'the', 'a', 'an', 'is', 'are', 'was', 'were'}
    
    keywords = []
    for word in words:
        word = word.strip('.,!?;:()[]{}""\'').lower()
        if len(word) > 3 and word not in stop_words:
            keywords.append(word)
    
    return keywords[:5]  # 只返回前5个关键词

def main():
    """主函数"""
    print("=== 会话状态检查 ===")
    print(f"检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    sessions = get_sessions()
    
    if not sessions:
        print("无活动会话")
        return
    
    print(f"总会话数: {len(sessions)}")
    print()
    
    for i, session in enumerate(sessions, 1):
        print(f"### 会话 {i}")
        print(f"**ID:** {session['sessionId'][:20]}...")
        print(f"**开始时间:** {session['startTime']}")
        print(f"**最后更新:** {session['lastMessageTime']}")
        
        # 最近关键词
        messages = session['messages'][-3:]  # 最后3条
        if messages:
            print(f"**最近关键词:**")
            for msg in reversed(messages):  # 从最新到最旧
                keywords = extract_keywords(msg['text'])
                if keywords:
                    print(f"  - [{msg['role']}] {', '.join(keywords)}")
        
        print()
    
    # 保存到 JSON
    output_file = '/root/.openclaw/workspace-feishu-ops/workspace-feishu-ops/session-state.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'checkTime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'totalSessions': len(sessions),
            'sessions': sessions
        }, f, ensure_ascii=False, indent=2)
    
    print(f"💾 会话状态已保存到: {output_file}")

if __name__ == '__main__':
    main()
