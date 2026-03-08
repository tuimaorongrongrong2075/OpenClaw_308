#!/usr/bin/env python3
"""
update_server_stats.py - 获取服务器状态并更新到 data/server-stats.json
"""
import json
import os
import subprocess
import time
import re

WORKSPACE = "/root/.openclaw"
DATA_DIR = f"{WORKSPACE}/workspace/project/memo/dashboard/data"
OUTPUT_FILE = f"{DATA_DIR}/server-stats.json"

def get_uptime():
    """获取在线时长"""
    try:
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
        
        days = int(uptime_seconds // 86400)
        hours = int((uptime_seconds % 86400) // 3600)
        minutes = int((uptime_seconds % 3600) // 60)
        
        if days > 0:
            return f"{days}d {hours}h"
        elif hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m"
    except:
        return "未知"

def get_cpu():
    """获取CPU使用率"""
    try:
        result = subprocess.run(
            ["top", "-bn1"],
            capture_output=True,
            text=True,
            timeout=5
        )
        for line in result.stdout.split('\n'):
            if 'Cpu(s)' in line:
                # 格式: %Cpu(s):  3.1 us,  1.2 sy,  0.0 ni, 95.6 id, ...
                parts = line.split(',')
                for p in parts:
                    if 'id' in p:
                        idle = float(p.split()[0])
                        used = 100 - idle
                        return f"{used:.0f}%"
        return "未知"
    except:
        return "未知"

def get_memory():
    """获取内存使用"""
    try:
        with open('/proc/meminfo', 'r') as f:
            lines = f.readlines()
        
        total = available = 0
        for line in lines:
            if line.startswith('MemTotal:'):
                total = int(line.split()[1]) / 1024 / 1024  # GB
            elif line.startswith('MemAvailable:'):
                available = int(line.split()[1]) / 1024 / 1024  # GB
        
        used = total - available
        percent = (used / total) * 100 if total > 0 else 0
        return f"{percent:.0f}%"
    except:
        return "未知"

def get_disk():
    """获取硬盘使用"""
    try:
        result = subprocess.run(
            ["df", "-h", "/"],
            capture_output=True,
            text=True,
            timeout=5
        )
        line = result.stdout.split('\n')[1]
        parts = line.split()
        # 格式: Filesystem      Size  Used Avail Use% Mounted on
        usage = parts[4]
        return usage
    except:
        return "未知"

def get_network_io():
    """获取网络I/O"""
    try:
        with open('/proc/net/dev', 'r') as f:
            lines = f.readlines()
        
        # 查找 eth0
        for line in lines:
            if 'eth0' in line or 'ens' in line:
                parts = line.split()
                rx_bytes = int(parts[1])
                tx_bytes = int(parts[9])
                
                # 转换为 MB
                rx_mb = rx_bytes / 1024 / 1024
                tx_mb = tx_bytes / 1024 / 1024
                
                return f"↓{rx_mb:.0f}MB ↑{tx_mb:.0f}MB"
        
        return "未知"
    except:
        return "未知"

def get_model():
    """获取当前模型"""
    try:
        session_file = f"{WORKSPACE}/agents/main/sessions/sessions.json"
        if os.path.exists(session_file):
            with open(session_file, 'r') as f:
                data = json.load(f)
                return data.get('defaults', {}).get('model', 'MiniMax-M2.5')
        return "MiniMax-M2.5"
    except:
        return "MiniMax-M2.5"

def get_sessions():
    """获取会话数"""
    try:
        session_dir = f"{WORKSPACE}/agents/main/sessions"
        if os.path.exists(session_dir):
            # 统计 .jsonl 文件数量
            count = len([f for f in os.listdir(session_dir) if f.endswith('.jsonl')])
            return count
        return 0
    except:
        return 0

def get_channels():
    """获取通道"""
    try:
        # 检查配置的通道
        channels = []
        # 飞书
        channels.append("Feishu")
        # QQ
        channels.append("QQ")
        return ", ".join(channels)
    except:
        return "未知"

def get_heartbeat():
    """获取心跳间隔"""
    try:
        with open(f"{WORKSPACE}/openclaw.json", 'r') as f:
            data = json.load(f)
            heartbeat = data.get('heartbeat', {}).get('agents', [{}])[0].get('every', '30m')
            return heartbeat
    except:
        return "30m"

def get_context():
    """获取上下文大小"""
    try:
        session_file = f"{WORKSPACE}/agents/main/sessions/sessions.json"
        if os.path.exists(session_file):
            with open(session_file, 'r') as f:
                data = json.load(f)
                ctx = data.get('defaults', {}).get('contextTokens', 200000)
                return f"{ctx // 1000}k"
        return "200k"
    except:
        return "200k"

def get_load():
    """获取负载"""
    try:
        with open('/proc/loadavg', 'r') as f:
            load = f.read().split()[:3]
            return f"{float(load[0]):.2f}"
    except:
        return "未知"

def get_processes():
    """获取进程数"""
    try:
        result = subprocess.run(
            ["ps", "aux"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return len(result.stdout.split('\n')) - 1
    except:
        return "未知"

def main():
    print("📊 正在获取服务器状态...")
    
    stats = [
        {"icon": "⏱️", "value": get_uptime(), "label": "在线时长"},
        {"icon": "⚡", "value": get_cpu(), "label": "CPU 使用率"},
        {"icon": "💾", "value": get_memory(), "label": "内存使用"},
        {"icon": "💿", "value": get_disk(), "label": "硬盘使用"},
        {"icon": "📡", "value": get_network_io(), "label": "网络 I/O"},
        {"icon": "🦧", "value": get_model(), "label": "模型"},
        {"icon": "📊", "value": str(get_sessions()), "label": "会话"},
        {"icon": "📨", "value": get_channels(), "label": "通道"},
        {"icon": "⏰", "value": get_heartbeat(), "label": "心跳"},
        {"icon": "💾", "value": get_context(), "label": "上下文"},
        {"icon": "📈", "value": get_load(), "label": "负载"},
        {"icon": "🔧", "value": str(get_processes()), "label": "进程"},
    ]
    
    data = {
        "title": "🖥️ 性能监控",
        "stats": stats
    }
    
    # 确保目录存在
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # 写入文件
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 已更新: {OUTPUT_FILE}")
    print(f"   - CPU: {stats[1]['value']}")
    print(f"   - 内存: {stats[2]['value']}")
    print(f"   - 硬盘: {stats[3]['value']}")

if __name__ == "__main__":
    main()
