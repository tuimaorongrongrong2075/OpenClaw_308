# Coding Team Setup v2.0 - 子代理开发团队

> 来源: 微信文章 - 四十学蒙
> 日期: 2026-03-05

## 简介

用于搭建 2-10 人子代理开发团队的 skill，支持多团队命名、自定义协作流程。

## 安装

```bash
clawhub install coding-team-setup
```

## 快速开始

```bash
# 默认团队
node wizard/setup.js

# 命名团队（支持多个团队并存）
node wizard/setup.js --team alpha
node wizard/setup.js --team beta
```

## 预设角色（10 个）

| 角色 ID | Emoji | 类别 | 默认模型类型 | 职责 |
|---------|-------|------|-------------|------|
| pm | 📋 | 管理 | Balanced | 需求分析、PRD、用户故事 |
| architect | 🏗️ | 工程 | Strongest | 系统架构设计、API 规范 |
| frontend | 🎨 | 工程 | Code | UI 组件开发、页面交互 |
| backend | ⚙️ | 工程 | Code | API 开发、数据库设计 |
| qa | 🔍 | 质量 | Balanced | 测试用例、自动化测试 |
| devops | 🚀 | 运维 | Strongest | CI/CD、容器化部署 |
| code-artisan | 🛠️ | 质量 | Code | 代码审查、重构优化 |
| data-engineer | 📊 | 工程 | Code | 数据管道、ETL |
| security | 🔒 | 质量 | Strongest | 安全审计、渗透测试 |
| tech-writer | 📝 | 管理 | Balanced | API 文档、用户手册 |

## 协作流程模板（4 种）

1. **标准 9 步** - 完整项目开发
2. **快速 3 步** - 小型功能、hotfix
3. **全栈独角兽** - 2-3 人精简团队
4. **完全自定义** - 自由定义步骤

## 实战经验

1. `allowAgents` 必须在 main agent 的 subagents 下
2. 模型 ID 必须包含完整 provider 前缀
3. 修改 openclaw.json 后必须重启 Gateway
4. 并发控制 - 同时 spawn 太多会触发 Rate Limit

---

*最后更新: 2026-03-05*
