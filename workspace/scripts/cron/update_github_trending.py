#!/usr/bin/env python3
"""
update_github_trending.py - GitHub聚合账号最新项目
每个账号选最新5条，转中文，飞书文档

【API说明】使用 GitHub REST API
  用途：获取指定用户/组织的最新仓库
  接口：GET /users/{username}/repos?sort=updated
  区别：REST API = "帮我看看 @karpathy 最近更新了什么项目"
"""
import json
import os
import subprocess
import requests
from datetime import datetime

WORKSPACE = "/root/.openclaw/workspace"
DATA_DIR = f"{WORKSPACE}/project/memo/dashboard/data"
OUTPUT_FILE = f"{DATA_DIR}/github-trending.json"

# 聚合账号列表
ACCOUNTS = [
    "papers-with-code",
    "karpathy",
    "stanfordnlp",
    "microsoft",
    "deepseek",
    "anthropic",
    "openai",
]

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

def get_user_repos(username):
    """获取用户最新项目"""
    try:
        url = f"https://api.github.com/users/{username}/repos?sort=updated&per_page=10"
        headers = {"Accept": "application/vnd.github.v3+json"}
        result = requests.get(url, headers=headers, timeout=10)
        if result.status_code == 200:
            repos = result.json()
            return repos[:5]  # 每账号5条
    except Exception as e:
        print(f"获取 {username} 失败: {e}")
    return []

def main():
    print("🔍 正在获取 GitHub 聚合账号最新项目...")
    
    all_repos = []
    
    for account in ACCOUNTS:
        print(f"  - 获取 @{account}...")
        repos = get_user_repos(account)
        for repo in repos:
            all_repos.append({
                "account": account,
                "name": repo.get("name", ""),
                "description": repo.get("description", ""),
                "stars": repo.get("stargazers_count", 0),
                "url": repo.get("html_url", ""),
                "updated": repo.get("updated_at", "")[:10]
            })
    
    print(f"共获取 {len(all_repos)} 个项目")
    
    # 翻译描述（限制数量避免超时）
    print("翻译成中文...")
    for i, repo in enumerate(all_repos[:15]):  # 只翻译前15条
        if repo["description"]:
            repo["description_cn"] = translate(repo["description"])
        else:
            repo["description_cn"] = "无描述"
        if (i+1) % 5 == 0:
            print(f"  已翻译 {i+1}/15...")
    
    # 保存JSON
    data = {
        "title": "📊 GitHub 聚合账号动态",
        "count": len(all_repos),
        "accounts": ACCOUNTS,
        "repos": all_repos,
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 已更新: {OUTPUT_FILE}")
    
    return data

if __name__ == "__main__":
    main()
