# 小猩看板 (Kanban Dashboard)

一个基于 Web 的系统监控与项目追踪仪表盘，采用现代简洁的设计风格，支持动态数据加载。

## 项目结构

```
.
├── kanban.html              # 主页面入口（包含 HTML/CSS/JS）
├── server.py                # Python 简易 HTTP 服务器
├── start.bat                # Windows 一键启动脚本
├── data/                    # 数据目录（JSON 数据源）
│   ├── server-stats.json    # 服务器性能监控数据
│   ├── github-trending.json # GitHub 热门项目排行
│   ├── agent-projects.json  # AI Agent 项目排行
│   ├── ai-news.json         # AI 新闻摘要
│   ├── cron-jobs.json       # 定时任务列表
│   ├── task-schedule.json# 待办事项/优先级
│   ├── project-progress.json# 项目进度追踪
│   └── quick-links.json     # 快速链接
└── README.md                # 本文档
```

## 启动方式

**本项目需要通过 HTTP 服务器访问，不能直接用浏览器打开 HTML 文件。**

### 方式一：Windows 一键启动（推荐）

双击运行 `start.bat`，会自动启动服务器并打开浏览器。

### 方式二：Python 服务器

```bash
# 进入项目目录后执行
python server.py
```

服务器将在 http://localhost:8080 启动，自动打开 kanban.html。

### 方式三：其他 HTTP 服务器

使用任意静态文件服务器，确保根目录指向本项目文件夹：

```bash
# Node.js
npx serve .

# Python 3（内置）
python -m http.server 8080

# PHP
php -S localhost:8080
```

访问地址：`http://localhost:8080/kanban.html`

## 环境要求

- **操作系统**：Windows / macOS / Linux
- **运行时**：Python 3.x（用于启动内置服务器）
- **浏览器**：Chrome 90+ / Firefox 88+ / Edge 90+ / Safari 14+
- **网络**：需要访问 Google Fonts（加载字体）

## 数据文件与页面对应关系

kanban.html 通过 `fetch()` 动态加载 `data/` 目录下的 JSON 文件，对应关系如下：

### 1. 性能监控 (Server Stats)
- **数据文件**：`data/server-stats.json`
- **渲染函数**：`renderServerStats()`
- **目标元素**：`#serverStats`
- **数据结构**：
  ```json
  {
    "title": "板块标题",
    "stats": [
      { "icon": "⏱️", "value": "1d 11h", "label": "在线时长" }
    ]
  }
  ```

### 2. GitHub 热门项目
- **数据文件**：`data/github-trending.json`
- **渲染函数**：`renderGithubTrending()`
- **目标元素**：`#githubTrending`
- **数据结构**：
  ```json
  {
    "projects": [
      {
        "rank": 1,
        "rankClass": "top1",
        "title": "项目名称",
        "description": "项目描述",
        "stars": "240K ⭐"
      }
    ]
  }
  ```

### 3. Agent 项目排行
- **数据文件**：`data/agent-projects.json`
- **渲染函数**：`renderAgentProjects()`
- **目标元素**：`#agentProjects`
- **数据结构**：与 `github-trending.json` 相同

### 4. AI 新闻摘要
- **数据文件**：`data/ai-news.json`
- **渲染函数**：`renderAINews()`
- **目标元素**：`#aiNews`
- **数据结构**：
  ```json
  {
    "title": "板块标题",
    "viewFullLink": "完整摘要链接",
    "itemsPerPage": 10,
    "items": [
      { "icon": "🤖", "text": "新闻内容" }
    ]
  }
  ```

### 5. 定时任务 (Cron Jobs)
- **数据文件**：`data/cron-jobs.json`
- **渲染函数**：`renderCronJobs()`
- **目标元素**：`#cronJobs`
- **分页控制**：`prevCronPage()` / `nextCronPage()`
- **数据结构**：
  ```json
  {
    "title": "板块标题",
    "totalPages": 3,
    "jobs": [
      {
        "id": 1,
        "name": "任务名称",
        "time": "08:00",
        "status": "active|paused",
        "page": 1
      }
    ]
  }
  ```

### 6. 项目日程
- **数据文件**：`data/task-schedule.json`
- **渲染函数**：`renderProjectSchedule()`
- **目标元素**：`#projectSchedule`
- **数据结构**：
  ```json
  {
    "items": [
      {
        "icon": "🔥",
        "title": "任务标题",
        "description": "任务描述",
        "priority": "high|medium|low"
      }
    ]
  }
  ```

### 7. 项目进度
- **数据文件**：`data/project-progress.json`
- **渲染函数**：`renderProjectProgress()`
- **目标元素**：`#projectProgress`
- **数据结构**：
  ```json
  {
    "totalPages": 1,
    "projects": [
      {
        "name": "项目名称",
        "status": "high|medium|low",
        "meta": "进度信息"
      }
    ]
  }
  ```

### 8. 快速链接
- **数据文件**：`data/quick-links.json`
- **渲染函数**：`renderQuickLinks()`
- **目标元素**：`#quickLinks`
- **数据结构**：
  ```json
  {
    "links": [
      { "icon": "🐱", "label": "显示名称", "url": "https://..." }
    ]
  }
  ```

## 样式优先级说明

### Rank 样式（排名徽章）
- `top1`：金色渐变（第1名）
- `top2`：银色渐变（第2名）
- `top3`：铜色渐变（第3名）
- 默认：紫色背景

### Priority/Status 样式（优先级/状态）
- `high`：红色左边框
- `medium`：橙色左边框
- `low`：绿色左边框

### Cron 状态样式
- `active`：绿色圆点 + 发光效果
- `paused`：灰色圆点

## 修改数据

1. 编辑 `data/` 目录下对应的 JSON 文件
2. 保存后刷新浏览器页面即可看到更新
3. **注意**：Cron Jobs 的分页通过 `page` 字段控制，需确保 `totalPages` 与实际页数一致

## 故障排查

| 问题 | 原因 | 解决方法 |
|------|------|----------|
| 页面空白/显示"加载数据失败" | 未通过 HTTP 服务器访问 | 使用 `start.bat` 或 `server.py` 启动 |
| 字体加载失败 | 无法访问 Google Fonts | 检查网络连接，或修改 HTML 中的字体 CDN |
| JSON 数据不显示 | 文件格式错误 | 检查 JSON 语法（可使用在线 JSON 校验工具）|
| Cron 分页异常 | `totalPages` 与实际不符 | 检查 `cron-jobs.json` 中的 `page` 分布 |

## 自定义扩展

如需添加新的数据模块：

1. 在 `data/` 下创建新的 JSON 文件
2. 在 `kanban.html` 的 `loadAllData()` 函数中添加 `fetch()` 调用
3. 添加对应的数据存储变量（如 `let newData = {}`）
4. 编写渲染函数（如 `renderNewSection()`）
5. 在 `renderAll()` 中调用新渲染函数
6. 在 HTML 中添加对应的容器元素

## 许可证

MIT License
