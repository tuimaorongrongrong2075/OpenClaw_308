# 看板数据更新流程

> 创建时间: 2026-03-05

## 概述

每日自动更新 4 个板块数据并推送到飞书云文档。

## 4个板块

| 板块 | 来源 | 数量 |
|------|------|------|
| AI News | RSS订阅 | 50条 |
| GitHub Trending | 聚合账号 | 25条 |
| Agent Projects | 关键词搜索 | 40条 |
| 服务器状态 | 系统命令 | 12指标 |

## 脚本

- 主脚本: `scripts/cron/update_dashboard_all.sh`
- 子脚本:
  - `scripts/cron/update_server_stats.py`
  - `scripts/cron/update_ai_news.py`
  - `scripts/cron/update_github_trending.py`
  - `scripts/cron/update_agent_projects.py`

## 飞书文档

创建后必须调用 write 写入内容，否则为空！

```python
# 1. 创建文档
feishu_doc(action="create", title="xxx")
# 返回 doc_token

# 2. 写入内容
feishu_doc(action="write", doc_token="xxx", content="xxx")
```

## Cron 配置

- 时间: 每天 11:00 (上海时间)
- 任务: `看板数据更新`

---

*最后更新: 2026-03-05*
