#!/usr/bin/env python3
"""
feishu_doc_full.py - 完整飞书文档创建流程（确保不为空）
"""
import json
import os
import sys

def main():
    if len(sys.argv) < 3:
        print("Usage: feishu_doc_full.py <title> <markdown_file>")
        sys.exit(1)
    
    title = sys.argv[1]
    md_file = sys.argv[2]
    
    # 读取 markdown 内容
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 输出指令，让用户在 OpenClaw 中执行
    print("请在 OpenClaw 中执行以下命令创建飞书文档：")
    print("")
    print("=" * 50)
    print("# Step 1: 创建文档")
    print('feishu_doc action=create title="' + title + '"')
    print("")
    print("# Step 2: 写入内容 (替换 DOC_TOKEN 为上一步返回的token)")
    print('feishu_doc action=write doc_token="DOC_TOKEN" content=\\' + json.dumps(content)[:100] + '..."')
    print("=" * 50)
    
    # 直接输出 content 供后续使用
    print("")
    print("CONTENT_START")
    print(content)
    print("CONTENT_END")

if __name__ == "__main__":
    main()
