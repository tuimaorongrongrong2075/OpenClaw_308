#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
脚本名称: normalize_markdown.py
脚本功能: 自动规范化 Markdown 文档格式
作者: 小猩
创建日期: 2026-02-27
版本: 1.0.0

版本记录:
    v1.0.0 (2026-02-27) - 初始版本
"""

import os
import re
import sys
from datetime import datetime
from pathlib import Path

# 配置
DOCS_DIR = "/root/.openclaw/workspace"
TODAY = datetime.now().strftime("%Y-%m-%d")

# 文档目录
DOC_DIRS = ["docs", "memory", "shared", "skills", "project"]


def check_filename(filename):
    """检查文件名是否符合规范"""
    issues = []
    
    # 检查是否包含中文
    if re.search(r'[\u4e00-\u9fff]', filename):
        issues.append(f"文件名包含中文: {filename}")
    
    # 检查是否使用 kebab-case (应该用 snake_case)
    if '-' in filename and not filename.startswith('.'):
        issues.append(f"使用了中划线: {filename}")
    
    # 检查空格
    if ' ' in filename:
        issues.append(f"文件名包含空格: {filename}")
    
    # 检查大小写 (memory目录除外)
    if filename.islower() and not filename.startswith('20'):
        issues.append(f"建议使用大写: {filename}")
    
    return issues


def check_header(content, filepath):
    """检查文件头是否符合规范"""
    issues = []
    
    # 检查是否有文件头
    if not content.startswith('#'):
        issues.append("缺少标题 (#)")
        return issues
    
    # 检查标题格式
    lines = content.split('\n')
    title = lines[0].strip()
    
    # 应该有英文大写标题
    if '(' not in title or ')' not in title:
        # 可能没有英文标题，给出建议
        pass
    
    # 检查是否有描述 (> 开头)
    has_description = False
    for line in lines[1:10]:
        if line.strip().startswith('>'):
            has_description = True
            break
    
    if not has_description:
        issues.append("缺少文件描述 (> 开头)")
    
    # 检查是否有最后更新
    if '最后更新' not in content and '最后更新' not in content:
        issues.append("缺少'最后更新'日期")
    
    # 检查是否有分隔符 ---
    if '---' not in content[:500]:
        issues.append("缺少章节分隔符 ---")
    
    return issues


def check_code_blocks(content):
    """检查代码块是否符合规范"""
    issues = []
    
    # 查找未指定语言的代码块
    code_blocks = re.findall(r'```(\w*)', content)
    for lang in code_blocks:
        if not lang:  # 空语言
            issues.append("代码块未指定语言")
            break
    
    return issues


def check_tables(content):
    """检查表格格式"""
    issues = []
    
    # 查找表格
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if '|' in line:
            # 检查上一行是否是表头分隔符
            if i > 0 and '---' in lines[i-1]:
                continue  # 这是表头，OK
            if '|' not in lines[i-1] and i > 0:
                issues.append(f"第{i+1}行表格格式可能有问题")
    
    return issues


def check_sensitive_info(content, filepath):
    """检查敏感信息"""
    issues = []
    
    # 检查常见的敏感信息模式
    patterns = [
        (r'password\s*[=:]\s*\S+', "密码"),
        (r'api[_-]?key\s*[=:]\s*\S+', "API Key"),
        (r'token\s*[=:]\s*ghp_', "GitHub Token"),
        (r'sk-[a-zA-Z0-9]{20,}', "OpenAI API Key"),
    ]
    
    for pattern, name in patterns:
        if re.search(pattern, content, re.IGNORECASE):
            issues.append(f"可能包含敏感信息: {name}")
    
    return issues


def normalize_file(filepath):
    """规范化单个文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return {"error": str(e)}
    
    issues = {
        "filename": check_filename(os.path.basename(filepath)),
        "header": check_header(content, filepath),
        "code_blocks": check_code_blocks(content),
        "tables": check_tables(content),
        "sensitive": check_sensitive_info(content, filepath)
    }
    
    # 统计
    total_issues = sum(len(v) for v in issues.values())
    
    return {
        "filepath": filepath,
        "issues": issues,
        "total": total_issues
    }


def main():
    """主函数"""
    print("🔍 Markdown 文档规范化检查")
    print("=" * 50)
    print()
    
    total_files = 0
    total_issues = 0
    
    for doc_dir in DOC_DIRS:
        dir_path = os.path.join(DOCS_DIR, doc_dir)
        if not os.path.exists(dir_path):
            continue
        
        print(f"\n📂 检查 {doc_dir}/")
        print("-" * 30)
        
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                if not file.endswith('.md'):
                    continue
                
                filepath = os.path.join(root, file)
                result = normalize_file(filepath)
                
                if "error" in result:
                    print(f"  ❌ {file}: {result['error']}")
                    continue
                
                total_files += 1
                
                if result["total"] > 0:
                    total_issues += result["total"]
                    rel_path = os.path.relpath(filepath, DOCS_DIR)
                    print(f"  ⚠️  {rel_path}: {result['total']} 个问题")
                    
                    # 打印具体问题
                    for category, problem_list in result["issues"].items():
                        if problem_list:
                            for p in problem_list:
                                print(f"      - [{category}] {p}")
                else:
                    rel_path = os.path.relpath(filepath, DOCS_DIR)
                    print(f"  ✅ {rel_path}")
    
    print()
    print("=" * 50)
    print(f"📊 统计: {total_files} 个文件, {total_issues} 个问题")
    
    if total_issues > 0:
        print("\n⚠️  请修复以上问题")
        sys.exit(1)
    else:
        print("\n✅ 所有文档格式规范!")
        sys.exit(0)


if __name__ == "__main__":
    main()
