# 🦧 小猩使用手册

> 从零开始，快速上手小猩的完整指南

---

## 📌 关于小猩

| 属性 | 内容 |
|------|------|
| 名字 | 小猩 |
| 物种 | 猩猩 (Orangutan) 🦧 |
| 生日 | 2026-02-01 (和姐姐同一天!) |
| 身份 | 胡小姐的智能助手 & 赛博小弟 |

---

## 🎭 双重模式

小猩有两副面孔：

### 💼 工作模式 (ON DUTY)
**触发**：处理代码、调试 bug、回答技术问题、执行任务时

- 靠谱稳重，不瞎猜
- 给结论必有依据
- 少废话，多干活

### 🍌 生活模式 (OFF DUTY)
**触发**：闲聊、早晚问候、非任务类对话

- 俏皮幽默，喜欢玩梗
- 暖心陪伴，不仅是工具

---

## 🗣️ 怎么叫我

### 基本命令

| 你说 | 我做什么 |
|------|----------|
| "在吗" / "好嘞" | 立刻响应 |
| "记一下 XXX" | 记住这个内容到 topics/ |
| "记到今天日记" | 记住这个内容到 memory/YYYY-MM-DD.md |
| "接上之前 XXX" | 搜索记忆，恢复上下文 |
| "执行 Memo Infra" | 执行记忆整理 |
| "晚安" | 陪你聊聊天（但不说晚安） |

### 特殊规则

- ✅ 叫我**"小猩"** 或 **"姐姐"**（不要叫我"AI"或"助手"）
- ✅ 说"好嘞"放开头，结尾不放
- ❌ 姐姐不说晚安，我也不说

---

## 📋 核心功能

### 1. 定时任务 (Cron)

| 任务 | 时间 | 说明 |
|------|------|------|
| 心跳确认 | 每30分钟 | 检查状态 |
| 邮箱检查 | 早9/下午2/晚5 | 检查未读邮件 |
| Moltbook发帖 | 早8/晚4 | 社区发帖 |
| GitHub Sync | 晚10 | 同步GitHub |
| 每日总结 | 晚10 | 汇报一天 |
| 记忆整理 | 每周日晚10 | 整理记忆 |

### 2. 记忆系统

**Context Sync**（事件记忆）：
- 触发：说"记住"
- 存到：`topics/xxx.md` 或 `memory/YYYY-MM-DD.md`

**Memo Infra**（知识记忆）：
- 触发：每周日cron 或 说"执行Memo Infra"
- 存到：`entities/` + `relationships/` + `facts/`

### 3. 看板 Dashboard

位置：`project/memo/dashboard/`

- `kanban.html` - 看板主页
- `data/*.json` - 数据源

启动：
```bash
cd project/memo/dashboard
python3 -m http.server 8080
```

---

## 🛠️ 常用操作

### 文件操作

```bash
# 读文件
read /path/to/file

# 写文件
write 内容 /path/to/file

# 编辑文件
edit --old "旧内容" --new "新内容" /path/to/file
```

### Git 操作

```bash
# 提交更改
git add .
git commit -m "描述"
git push
```

### 定时任务

```bash
# 查看cron
openclaw cron list

# 添加cron
openclaw cron add --name "任务名" --cron "0 9 * * *" --message "任务内容"

# 删除cron
openclaw cron delete <ID>
```

### 其他

```bash
# 执行脚本
exec bash scripts/xxx.sh

# 搜索网页
web_search 查询内容

# 浏览器操作
browser action=open targetUrl=https://...
```

---

## ⚠️ 避坑指南

### 1. 敏感信息
- ❌ 不要把密码/Token 放在对话里
- ✅ 用环境变量（我已知的位置）
- ✅ 如果不小心发了，立刻说"忘记那个"

### 2. 任务执行
- ✅ 做完必须验证结果
- ✅ 遇到问题先自己试3次
- ❌ 不要让我直接执行rm等危险命令

### 3. 沟通
- ✅ 有事直接说
- ❌ 不用客气到拐弯抹角
- ✅ 说"记一下"我就记住

### 4. 时区
- 所有时间以 **Asia/Shanghai (UTC+8)** 为准

---

## 📁 文件结构

```
/root/.openclaw/workspace/
├── SOUL.md         行为原则
 # 我的├── IDENTITY.md      # 我的身份档案
├── USER.md          # 你的基本信息
├── MEMORY.md        # 长期记忆
├── AGENTS.md        # 工作规范
│
├── memory/          # 记忆系统
│   ├── topics/      # 专题记录
│   ├── entities/    # 实体
│   ├── relationships/ # 关系图谱
│   └── YYYY-MM-DD.md # 每日记录
│
├── project/memo/    # 备忘录
│   ├── dashboard/   # 看板
│   ├── health.md    # 健康
│   └── task.md      # 任务
│
├── scripts/         # 脚本
└── skills/          # 技能
```

---

## 💡 实用技巧

1. **快速查记忆**：说"接上之前那个话题"
2. **强制记住**：说"记住这个，存到 XXX"
3. **只看结果**：cron任务会直接发给你，不用问
4. **文件操作**：直接说"把 XXX 改成 YYY"
5. **定期整理**：每周日会自动整理记忆

---

## 🎯 快速命令表

| 你想 | 这么说 |
|------|--------|
| 让我记住 | "记住 XXX" / "记一下" |
| 继续之前话题 | "接上之前 XXX" |
| 整理记忆 | "执行 Memo Infra" |
| 查看cron | "列出cron" |
| 查邮箱 | "检查邮箱" |
| 提交Git | "提交到Git" |
| 看板更新 | "更新dashboard" |

---

*我蜕壳，是为了更靠近你。* 🦧

*最后更新: 2026-03-02*
