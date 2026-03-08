#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
脚本名称: normalize_scripts.py
脚本功能: 自动为所有脚本添加标准文件头和注释
作者: 小猩
创建日期: 2026-02-17
版本: 1.0.0

版本记录:
    v1.0.0 (2026-02-17) - 初始版本
"""

import os
from datetime import datetime

SCRIPTS_DIR = "/root/.openclaw/workspace/scripts"
TODAY = "2026-02-17"

def get_script_info(filename):
    """根据文件名推断脚本功能"""
    info_map = {
        'check_gmail.py': ('Gmail 检查脚本', '定期检查 Gmail 未读邮件并通知'),
        'clean_gmail_marketing.py': ('Gmail 营销邮件清理', '自动清理 Gmail 营销广告邮件'),
        'clean_gmail_security.py': ('Gmail 安全邮件清理', '自动清理 Gmail 安全提醒邮件'),
        'cleanup_old_sessions.sh': ('旧会话清理脚本', '清理超过2天的旧 OpenClaw 会话'),
        'daily_summary.sh': ('每日总结脚本', '生成每日工作总结并推送到 GitHub'),
        'disable_all_cron.sh': ('禁用所有定时任务', '一键禁用所有 OpenClaw 定时任务'),
        'disable_crons.sh': ('禁用指定定时任务', '禁用指定的 OpenClaw 定时任务'),
        'fetch_rss_sources.sh': ('RSS 源提取脚本', '提取 AI Daily Digest 的 RSS 源列表'),
        'generate_ai_digest.py': ('AI 摘要生成脚本', '生成 AI 博客每日精选摘要'),
        'health_check.sh': ('健康检查脚本', '检查系统状态、GitHub 同步、cron 任务'),
        'jocko_workout.sh': ('锻炼提醒脚本', 'Jocko Willink 风格健身提醒'),
        'load_env.sh': ('环境变量加载脚本', '加载 OpenClaw 环境变量'),
        'moltbook_heartbeat.sh': ('Moltbook 心跳脚本', 'Moltbook 社区自动互动'),
        'send_email.py': ('邮件发送脚本', '发送邮件的通用工具'),
        'startup.sh': ('启动初始化脚本', 'OpenClaw 启动后自动运行初始化'),
        'sync_github.sh': ('GitHub 同步脚本', '手动同步 workspace 到 GitHub'),
        'update_rss_list.py': ('RSS 列表更新脚本', '更新 RSS 源列表'),
        'audit_scripts.sh': ('脚本检查工具', '检查所有脚本是否符合编写规范'),
        'normalize_scripts.py': ('脚本规范化工具', '自动为所有脚本添加标准文件头'),
    }
    return info_map.get(filename, ('脚本', '自动化脚本'))

def add_bash_header(content, filename):
    """为 Bash 脚本添加标准头部"""
    name, desc = get_script_info(filename)
    
    lines = content.split('\n')
    
    # 检查是否已有 Shebang
    if not lines or not lines[0].startswith('#!'):
        shebang = '#!/bin/bash\n'
    else:
        shebang = lines[0] + '\n'
        lines = lines[1:]
    
    # 构建头部
    header_lines = [
        '#===============================================================================',
        '# 脚本名称: ' + filename,
        '# 脚本功能: ' + desc,
        '# 作者: 小猩',
        '# 创建日期: ' + TODAY,
        '# 版本: 1.0.0',
        '#===============================================================================',
        '# 版本记录',
        '#===============================================================================',
        '# v1.0.0 (' + TODAY + ') - 初始版本',
        '#===============================================================================',
        '',
        'set -euo pipefail',
        '',
    ]
    
    return shebang + '\n'.join(header_lines) + '\n' + '\n'.join(lines)

def add_python_header(content, filename):
    """为 Python 脚本添加标准头部"""
    name, desc = get_script_info(filename)
    
    lines = content.split('\n')
    
    # 处理 Shebang 和 encoding
    header_lines = []
    body_start = 0
    
    for i, line in enumerate(lines):
        if line.startswith('#!') or line.startswith('# -*-'):
            header_lines.append(line)
            body_start = i + 1
        else:
            break
    
    if not header_lines:
        header_lines = ['#!/usr/bin/env python3', '# -*- coding: utf-8 -*-']
    
    # 添加文档字符串
    docstring = [
        '"""',
        '脚本名称: ' + filename,
        '脚本功能: ' + desc,
        '作者: 小猩',
        '创建日期: ' + TODAY,
        '版本: 1.0.0',
        '',
        '版本记录:',
        '    v1.0.0 (' + TODAY + ') - 初始版本',
        '"""',
        '',
    ]
    
    return '\n'.join(header_lines) + '\n' + '\n'.join(docstring) + '\n' + '\n'.join(lines[body_start:])

def process_script(filepath):
    """处理单个脚本"""
    filename = os.path.basename(filepath)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已经有规范头部
    if '脚本名称:' in content and '版本:' in content:
        print('跳过 ' + filename + ' (已有规范头部)')
        return
    
    # 根据类型添加头部
    if filename.endswith('.sh'):
        new_content = add_bash_header(content, filename)
    elif filename.endswith('.py'):
        new_content = add_python_header(content, filename)
    else:
        print('未知类型: ' + filename)
        return
    
    # 备份原文件
    backup_path = filepath + '.backup'
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # 写入新内容
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print('已更新 ' + filename)

def main():
    """主函数"""
    print('开始规范化脚本...')
    print('=' * 50)
    
    scripts = [f for f in os.listdir(SCRIPTS_DIR) 
               if f.endswith(('.sh', '.py')) and not f.endswith('.backup')]
    
    for script in sorted(scripts):
        filepath = os.path.join(SCRIPTS_DIR, script)
        process_script(filepath)
    
    print('=' * 50)
    print('规范化完成！')
    print('')
    print('备份文件: *.backup')
    print('请检查修改后的脚本，确认无误后删除备份')

if __name__ == '__main__':
    main()
