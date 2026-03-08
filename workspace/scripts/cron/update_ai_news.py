#!/usr/bin/env python3
"""
update_ai_news.py - AI新闻摘要，获取RSS并生成飞书云文档
需要中文摘要
"""
import json
import os
import subprocess
import requests
from datetime import datetime

WORKSPACE = "/root/.openclaw/workspace"
DATA_DIR = f"{WORKSPACE}/project/memo/dashboard/data"
OUTPUT_FILE = f"{DATA_DIR}/ai-news.json"

# 翻译函数（免费API）
def translate_to_chinese(text):
    """使用免费API翻译成中文"""
    try:
        # 使用 MyMemory API (免费)
        url = f"https://api.mymemory.translated.net/get?q={requests.utils.quote(text[:500])}&langpair=en|zh"
        result = requests.get(url, timeout=5)
        if result.status_code == 200:
            data = result.json()
            if data.get('responseStatus') == 200:
                return data['responseData']['translatedText']
    except Exception as e:
        print(f"翻译失败: {e}")
    return text  # 失败返回原文

# RSS 源列表
RSS_SOURCES = [
    "https://simonwillison.net/atom/everything/",
    "https://www.jeffgeerling.com/blog.xml",
    "https://krebsonsecurity.com/feed/",
    "https://daringfireball.net/feeds/main",
    "https://lcamtuf.substack.com/feed",
    "https://mitchellh.com/feed.xml",
    "https://garymarcus.substack.com/feed",
    "https://pluralistic.net/feed/",
    "https://dwarkeshpatel.com/feed",
    "https://gwern.substack.com/feed",
]

def fetch_rss():
    """获取RSS内容"""
    items = []
    for url in RSS_SOURCES:
        try:
            result = subprocess.run(
                ["curl", "-s", url],
                capture_output=True,
                text=True,
                timeout=10
            )
            # 简单解析（提取标题和链接）
            lines = result.stdout.split('\n')
            for i, line in enumerate(lines):
                if '<title>' in line.lower():
                    title = line.split('<title>')[-1].split('</title>')[0].strip()
                    if title and title not in ['RSS', 'Atom', '']:
                        items.append({"title": title, "source": url})
                        if len(items) >= 50:
                            break
        except Exception as e:
            print(f"Error fetching {url}: {e}")
        if len(items) >= 50:
            break
    return items[:50]

def generate_summary(news_list):
    """生成中文摘要"""
    summaries = []
    for i, item in enumerate(news_list[:50], 1):
        title = item.get('title', 'Untitled')[:60]
        # 翻译成中文
        chinese_title = translate_to_chinese(title)
        summaries.append(f"{i}. {chinese_title}")
        if i % 10 == 0:
            print(f"已翻译 {i}/50 条...")
    return "\n".join(summaries)

def create_feishu_doc(title, content):
    """创建飞书云文档"""
    try:
        # 先创建文档
        result = subprocess.run(
            ["openclaw", "feishu", "doc", "create",
             "--title", title],
            capture_output=True,
            text=True,
            timeout=30
        )
        print(f"Feishu doc create result: {result.stdout}")
        return True
    except Exception as e:
        print(f"Error creating feishu doc: {e}")
        return False

def main():
    print("📰 正在获取AI新闻...")
    
    # 1. 获取RSS新闻
    news = fetch_rss()
    print(f"获取到 {len(news)} 条新闻")
    
    # 2. 生成摘要
    summary = generate_summary(news)
    
    # 3. 保存JSON
    data = {
        "title": "📰 AI News 摘要",
        "count": len(news),
        "items": news[:50],
        "summary": summary,
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 已更新: {OUTPUT_FILE}")
    
    # 4. 保存markdown内容（50条）
    md_content = f"""# 📰 AI News 资讯

**更新时间**: {datetime.now().strftime("%Y-%m-%d %H:%M")}

## 今日资讯 Top 50

{summary}

---

*来源: RSS订阅，共 {len(news)} 条*
"""
    
    md_file = f"{DATA_DIR}/ai-news.md"
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    # 5. 更新JSON（保存50条）
    data["title"] = "📰 AI News 资讯"
    data["summary"] = summary
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return True

if __name__ == "__main__":
    main()
