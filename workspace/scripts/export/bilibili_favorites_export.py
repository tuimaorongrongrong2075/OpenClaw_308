#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
脚本名称: bilibili_favorites_export.py
脚本功能: 导出B站收藏夹到Obsidian Markdown
作者: 小猩 🦧
创建日期: 2026-02-19
版本: 1.0.0
依赖: Python 3.8+, requests
环境变量: BILIBILI_SESSDATA, BILIBILI_UID

版本记录:
    v1.0.0 (2026-02-19) - 初始版本，支持导出收藏夹为Markdown
"""

import os
import json
import requests
from datetime import datetime
from urllib.parse import urlencode

# B站API基础URL
BILIBILI_API = "https://api.bilibili.com"

# 检查环境变量
def check_env():
    """检查必需的环境变量"""
    required = {
        'BILIBILI_UID': 'B站用户ID',
        'BILIBILI_SESSDATA': 'B站登录凭证(SESSDATA)'
    }
    
    missing = []
    for key, desc in required.items():
        if not os.environ.get(key):
            missing.append(f"{key} ({desc})")
    
    if missing:
        print("❌ 缺少以下环境变量:")
        for item in missing:
            print(f"   - {item}")
        print("\n💡 获取方法见脚本注释或询问姐姐")
        return False
    return True

# 获取收藏夹列表
def get_folders(uid, sessdata):
    """获取用户收藏夹列表"""
    url = f"{BILIBILI_API}/x/v3/fav/folder/list4navigate"
    params = {'up_mid': uid}
    headers = {
        'Cookie': f'SESSDATA={sessdata}',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=30)
        data = response.json()
        
        if data.get('code') == 0:
            # API返回的数据结构: data是列表，每个元素包含mediaListResponse.list
            raw_data = data.get('data', [])
            folders = []
            for item in raw_data:
                # 从mediaListResponse.list中提取收藏夹
                if isinstance(item, dict) and 'mediaListResponse' in item:
                    media_list = item.get('mediaListResponse', {}).get('list')
                    if media_list:  # 检查是否为None
                        folders.extend(media_list)
            return folders
        else:
            print(f"⚠️ 获取收藏夹失败: {data.get('message')}")
            return []
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return []

# 获取收藏夹内容
def get_folder_videos(folder_id, uid, sessdata, page=1, page_size=20):
    """获取收藏夹中的视频列表"""
    url = f"{BILIBILI_API}/x/v3/fav/resource/list"
    params = {
        'media_id': folder_id,
        'pn': page,
        'ps': page_size,
        'platform': 'web'
    }
    headers = {
        'Cookie': f'SESSDATA={sessdata}',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=30)
        data = response.json()
        
        if data.get('code') == 0:
            medias = data.get('data', {}).get('medias', [])
            return medias
        else:
            print(f"⚠️ 获取视频列表失败: {data.get('message')}")
            return []
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return []

# 生成Obsidian Markdown
def generate_markdown(folder_name, videos):
    """生成Obsidian格式的Markdown文件"""
    timestamp = datetime.now().strftime('%Y-%m-%d')
    filename = f"bilibili_favorites_{folder_name}_{timestamp}.md"
    
    content = f"""# B站收藏夹导出 - {folder_name}

> 导出时间: {timestamp}
> 来源: Bilibili
> 视频数量: {len(videos)}

---

"""
    
    for idx, video in enumerate(videos, 1):
        title = video.get('title', '未知标题')
        bvid = video.get('bvid', '')
        link = f"https://www.bilibili.com/video/{bvid}" if bvid else video.get('link', '')
        up_name = video.get('upper', {}).get('name', '未知UP主')
        cover = video.get('cover', '')
        intro = video.get('intro', '')
        
        content += f"""## {idx}. {title}

- **链接**: [{link}]({link})
- **UP主**: {up_name}
- **BV号**: {bvid}
- **封面**: ![封面]({cover})

{intro}

---

"""
    
    return filename, content

# 主函数
def main():
    """主函数"""
    print("🦞 B站收藏夹导出工具")
    print("======================")
    
    # 检查环境变量
    if not check_env():
        return
    
    uid = os.environ.get('BILIBILI_UID')
    sessdata = os.environ.get('BILIBILI_SESSDATA')
    
    print(f"📱 用户ID: {uid}")
    print("🔍 正在获取收藏夹列表...")
    
    # 获取收藏夹列表
    folders = get_folders(uid, sessdata)
    
    if not folders:
        print("❌ 未找到收藏夹，请检查UID和登录状态")
        return
    
    print(f"✅ 找到 {len(folders)} 个收藏夹")
    print("")
    
    # 创建输出目录
    output_dir = "/root/.openclaw/workspace/exports"
    os.makedirs(output_dir, exist_ok=True)
    
    # 遍历每个收藏夹
    for folder in folders:
        folder_id = folder.get('id')  # 使用完整的id（包含后缀）
        folder_name = folder.get('title', f'收藏夹_{folder_id}')
        media_count = folder.get('media_count', 0)
        
        print(f"📁 正在导出: {folder_name} ({media_count}个视频)")
        
        # 获取所有视频
        all_videos = []
        page = 1
        while True:
            videos = get_folder_videos(folder_id, uid, sessdata, page)
            if not videos:
                break
            all_videos.extend(videos)
            
            if len(videos) < 20:  # 不足一页，说明已完
                break
            page += 1
        
        if not all_videos:
            print(f"   ⚠️ 收藏夹为空或获取失败")
            continue
        
        # 生成Markdown
        filename, content = generate_markdown(folder_name, all_videos)
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"   ✅ 已导出: {filename} ({len(all_videos)}个视频)")
    
    print("")
    print("======================")
    print(f"✅ 导出完成！文件保存在: {output_dir}/")
    print("💡 建议: 将导出的Markdown文件复制到Obsidian的收藏夹目录")

if __name__ == '__main__':
    main()
