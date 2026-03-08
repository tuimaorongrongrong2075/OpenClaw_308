#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Get笔记HTML转换脚本
手动解析HTML并转换为Obsidian Markdown
"""

import re
import os
from datetime import datetime

def parse_getnotes_html(html_file):
    """解析Get笔记导出的HTML文件"""
    
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    notes = []
    
    # 提取表格中的每一行笔记
    # 匹配 <tr class="date-list-item" data-date-str="..." data-tags="...">
    pattern = r'<tr class="date-list-item"[^>]*data-date-str="([^"]+)"[^>]*data-tags="([^"]*)"[^>]*>.*?<a href="([^"]+)"[^>]*>([^<]+)</a>'
    
    matches = re.findall(pattern, html_content, re.DOTALL)
    
    for match in matches:
        date_str = match[0]
        tags = match[1] if match[1] else ''
        link = match[2]
        title = match[3]
        
        # 清理标签
        tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()] if tags else []
        
        notes.append({
            'title': title,
            'date': date_str,
            'tags': tag_list,
            'link': link,
            'source': 'Get笔记'
        })
    
    return notes

def generate_markdown(notes, output_file):
    """生成Obsidian格式的Markdown文件"""
    
    content = f"""# Get笔记导出

> 导出时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
> 总计: {len(notes)} 条笔记

---

## 📝 笔记列表

"""
    
    # 按日期排序（最新的在前）
    notes_sorted = sorted(notes, key=lambda x: x['date'], reverse=True)
    
    for i, note in enumerate(notes_sorted, 1):
        tags_str = ' '.join([f"#{tag}" for tag in note['tags']]) if note['tags'] else ''
        
        note_entry = f"""
### {i}. {note['title']}

**日期**: {note['date']}
**标签**: {tags_str if tags_str else '无'}
**来源**: {note['source']}
**链接**: [查看原文]({note['link']})

---

"""
        content += note_entry
    
    # 保存文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    """主函数"""
    
    html_file = '/root/.openclaw/workspace/OpenClaw_201/scripts/export/get_raw/voicenotes_202602192358_getnotes_archive_1a65cccfc0024a60kdPo3ZxB/index.html'
    output_dir = '/root/.openclaw/workspace/OpenClaw_201/scripts/export/get'
    
    os.makedirs(output_dir, exist_ok=True)
    
    print("🦞 Get笔记导出工具")
    print("======================")
    print("🔍 正在解析HTML文件...")
    
    notes = parse_getnotes_html(html_file)
    
    if not notes:
        print("❌ 未找到笔记，请检查HTML文件格式")
        return
    
    print(f"✅ 找到 {len(notes)} 条笔记")
    print()
    
    timestamp = datetime.now().strftime('%Y-%m-%d')
    output_file = os.path.join(output_dir, f'getnotes_export_{timestamp}.md')
    
    generate_markdown(notes, output_file)
    
    print(f"✅ 导出完成！")
    print(f"📄 文件: {output_file}")
    print(f"📊 共 {len(notes)} 条笔记")

if __name__ == '__main__':
    main()
