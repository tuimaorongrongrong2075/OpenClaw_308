#!/usr/bin/env python3
"""
update_agent_projects.py - Agent项目搜索
关键词: openclaw, skills, memory, agent
各10条，中文，飞书文档

【API说明】使用 GitHub Search API
  用途：按关键词搜索全站热门仓库
  接口：GET /search/repositories?q={keyword}&sort=stars
  区别：Search API = "帮我搜搜有哪些项目包含 'agent' 这个关键词"
"""
import json
import os
import subprocess
import requests
from datetime import datetime

WORKSPACE = "/root/.openclaw/workspace"
DATA_DIR = f"{WORKSPACE}/project/memo/dashboard/data"
OUTPUT_FILE = f"{DATA_DIR}/agent-projects.json"

# 搜索关键词
KEYWORDS = ["openclaw", "skills", "memory", "agent"]

def translate(text):
    """翻译成中文"""
    try:
        url = f"https://api.mymemory.translated.net/get?q={requests.utils.quote(text[:300])}&langpair=en|zh"
        result = requests.get(url, timeout=5)
        if result.status_code == 200:
            data = result.json()
            if data.get('responseStatus') == 200:
                return data['responseData']['translatedText']
    except:
        pass
    return text

def search_projects(keyword):
    """搜索GitHub项目"""
    try:
        url = f"https://api.github.com/search/repositories?q={keyword}&sort=stars&order=desc&per_page=15"
        headers = {"Accept": "application/vnd.github.v3+json"}
        result = requests.get(url, headers=headers, timeout=15)
        if result.status_code == 200:
            data = result.json()
            return data.get("items", [])[:10]  # 每关键词10条
    except Exception as e:
        print(f"搜索 {keyword} 失败: {e}")
    return []

def main():
    print("🔍 正在搜索 Agent 相关项目...")
    
    all_projects = []
    
    for keyword in KEYWORDS:
        print(f"  - 搜索: {keyword}...")
        repos = search_projects(keyword)
        for repo in repos:
            all_projects.append({
                "keyword": keyword,
                "name": repo.get("name", ""),
                "description": repo.get("description", ""),
                "stars": repo.get("stargazers_count", 0),
                "url": repo.get("html_url", ""),
                "owner": repo.get("owner", {}).get("login", "")
            })
    
    print(f"共获取 {len(all_projects)} 个项目")
    
    # 翻译描述
    print("翻译成中文...")
    for i, proj in enumerate(all_projects[:20]):  # 翻译前20条
        if proj["description"]:
            proj["description_cn"] = translate(proj["description"])[:100]
        else:
            proj["description_cn"] = "无描述"
        if (i+1) % 5 == 0:
            print(f"  已翻译 {i+1}/20...")
    
    # 保存JSON
    data = {
        "title": "🤖 Agent Projects 搜索",
        "keywords": KEYWORDS,
        "count": len(all_projects),
        "projects": all_projects,
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 已更新: {OUTPUT_FILE}")
    
    return data

if __name__ == "__main__":
    main()
