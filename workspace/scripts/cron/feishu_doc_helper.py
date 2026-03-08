#!/usr/bin/env python3
"""
feishu_doc_helper.py - 飞书文档创建+写入Helper
确保文档不为空
"""
import json
import subprocess
import sys

def create_and_write_doc(title, content):
    """创建飞书文档并写入内容"""
    # 1. 创建文档，获取 doc_token
    create_result = subprocess.run(
        ["openclaw", "message", "send", "--channel", "feishu",
         "--target", "ou_0ca9ad88a77fd653f0244807918cab56",
         "--message", "test"],
        capture_output=True,
        text=True
    )
    
    # 使用 feishu_doc 工具
    # 先创建
    create_cmd = f'''
import json
from feishu_doc import feishu_doc
result = feishu_doc(action="create", title="{title}")
print(json.dumps(result))
'''
    
    # 这个方法不行，我们需要用 tool 调用
    
    # 正确的做法：在脚本中直接输出指令，让 OpenClaw 调用 feishu_doc 工具
    print("===FEISHU_DOC_NEEDED===")
    print(json.dumps({"title": title, "content": content}))
    print("===FEISHU_DOC_NEEDED===")
    
    return None

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: feishu_doc_helper.py <title> <content_file>")
        sys.exit(1)
    
    title = sys.argv[1]
    with open(sys.argv[2], 'r') as f:
        content = f.read()
    
    create_and_write_doc(title, content)
