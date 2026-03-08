# OpenClaw 工作区使用手册 🦧

> 最后更新: 20202
> 作者6-03-: 小猩

---

## 📁 目录结构总览

```
workspace/
├── analysis/            # 正在调研的项目
│   ├── automation/     # Automaton 项目分析
│   └── openclaw/       # OpenClaw 功能分析
├── daily/               # 定时任务输出（未来）
├── docs/                # 日常文档
│   ├── FAVORITES_EXPORT_GUIDE.md
│   ├── MEMORY_RESTORE_GUIDE.md
│   └── digest/         # AI 每日摘要
├── memory/              # 记忆系统（重点）
│   ├── EverMemOS/      # 长期记忆项目
│   │   ├── ARCHITECTURE.md
│   │   ├── README.md
│   │   ├── facts/
│   │   ├── index/          # 关键词索引
│   │   ├── preferences/
│   │   ├── relationships/
│   │   └── personas/
│   ├── topics/         # Context Sync 专题
│   ├── YYYY-MM-DD.md   # 每日记录（md文件）
│   ├── Feb/            # 归档（2月记忆）
│   ├── raw/            # 原始数据
│   └── structured/     # 结构化数据
├── project/             # 项目文件
│   └── memo/           # 备忘录
│       ├── goal.md
│       ├── project.md
│       ├── task.md
│       ├── unified.md
│       ├── inbox.md
│       ├── idea.md
│       ├── health.md
│       ├── shopping.md
│       ├── todo/
│       └── dashboard/  # KANBAN 项目
├── scripts/             # 自动化脚本
│   ├── mail/           # 邮件管理
│   ├── export/         # 数据导出
│   ├── digest/         # AI 摘要
│   ├── system/         # 系统维护
│   ├── reminder/       # 提醒
│   └── logs/           # 日志
├── shared/              # 共享资源
│   ├── Document_Standards.md
│   ├── Script_Standards.md
│   ├── GITHUB_API_CONFIG.md
│   ├── Openclaw_Config.md
│   ├── Multi-Agent_Guide.md
│   ├── Memory_Restore_Guide.md
│   └── Workspace_Guide.md
├── skills/              # 技能扩展
├── screenshots/         # 截图存储
├── logs/                # 运行日志
└── [核心配置文件]
    ├── AGENTS.md
    ├── SOUL.md
    ├── USER.md
    ├── IDENTITY.md
    ├── MEMORY.md
    ├── HEARTBEAT.md
    ├── TOOLS.md
    ├── MOLTBOOK.md
    ├── ROOT_FILES_SUMMARY.md
    └── SECURITY.md
```

---

## 📂 核心目录说明

### analysis/ - 正在调研的项目
- **automation/** - Automaton 项目深度分析
- **openclaw/** - OpenClaw 功能分析

### memory/ - 记忆系统（重点）
- **EverMemOS/** - 长期记忆项目（正在进行）
  - facts/ - 事实数据库
  - preferences/ - 偏好设置
  - relationships/ - 关系图谱
  - personas/ - 人格设定
- **topics/** - Context Sync 专题记忆
- **YYYY-MM-DD/** - Context Sync 每日记录
- **Feb/** - 归档文件夹（2月记忆）
- **raw/** - 原始数据落盘
- **structured/** - 结构化数据
- **index/** - 关键词索引

### project/ - 项目文件
- **memo/** - 备忘录系统
  - goal.md - 长期目标
  - project.md - 项目管理
  - task.md - 任务管理
  - unified.md - Dashboard
  - inbox.md - 收件箱
  - idea.md - 灵感
  - health.md - 健康
  - shopping.md - 采购
  - todo/ - 分类待办
  - dashboard/ - KANBAN 项目

### docs/ - 日常文档
- FAVORITES_EXPORT_GUIDE.md - 收藏导出指南
- MEMORY_RESTORE_GUIDE.md - 记忆恢复指南
- digest/ - AI 每日摘要

### scripts/ - 自动化脚本
- **mail/** - 邮件管理
- **export/** - 数据导出
- **digest/** - AI 摘要
- **system/** - 系统维护
- **reminder/** - 提醒
- **logs/** - 日志

---

## 🎯 使用规范

### 记忆系统
- Context Sync 触发时记录到 `memory/YYYY-MM-DD.md` 或 `memory/topics/`
- 长期记忆存储到 `memory/EverMemOS/`
- 已归档记忆在 `memory/Feb/`

### 项目管理
- 当前项目存放在 `project/memo/`
- KANBAN 项目在 `project/memo/dashboard/`
- 已完成项目可归档

### 文档管理
- 日常文档放在 `docs/`
- 配置标准放在 `shared/`
- 调研分析放在 `analysis/`

---

*最后更新: 2026-03-02*
*🦧 小猩*
