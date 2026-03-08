# 🧠 三层记忆系统 - 检查指南

> 用于验证系统是否正常运行
> 基于 EverMemOS 理念设计

---

## 快速检查命令

### 查看最近更新
```bash
ls -lt memory/entities/ memory/relationships/ memory/preferences/ memory/facts/
```

### 检查核心文件
```bash
# 胡小姐档案
cat memory/entities/people/胡小姐.md

# 小猩档案  
cat memory/entities/personas/小猩.md

# 关系图谱
cat memory/relationships/graph.json

# 偏好配置
cat memory/preferences/communication.json

# 事实库
cat memory/facts/database.json

# 关键词索引
cat memory/index/keywords.json
```

---

## 文件结构

```
memory/
├── ARCHITECTURE.md      # 架构说明
├── entities/            # 实体
│   ├── people/胡小姐.md
│   └── personas/小猩.md
├── relationships/       # 关系图谱
│   └── graph.json
├── preferences/         # 偏好
│   └── communication.json
├── facts/             # 事实库
│   └── database.json
└── index/             # 索引
    └── keywords.json
```

---

## 触发条件

### 什么时候会更新
1. **发现重要信息**：姐姐告诉我新事实/偏好/关系
2. **任务完成**：重要任务完成，需要记录
3. **Session 结束**：对话结束时做总结
4. **里程碑**：一周小结、满月等特殊时刻

### 手动触发
直接告诉我：
- "记住我喜欢 XXX"
- "记一下 XXX"
- "检查一下你记住的我有哪些信息"

---

## 验证要点

| 检查项 | 预期 |
|--------|------|
| entities/ 有更新 | 时间戳在最近 |
| facts/ 有记录 | 新信息已写入 |
| keywords/ 有索引 | 新关键词已添加 |
| graph.json 有关系 | 新关系已关联 |

---

## 权重说明

| 文件 | 权重 | 说明 |
|------|------|------|
| SOUL.md | 🔴 最高 | 行为原则 |
| IDENTITY.md | 🔴 最高 | 身份档案 |
| USER.md | 🔴 最高 | 用户信息 |
| structured/ | 🟡 中等 | 结构化数据库 |
| MEMORY.md | 🟢 补充 | 长期记忆精选 |

---

## 一周验证点

- [ ] 检查 entities/ 最近更新时间
- [ ] 检查 facts/ 是否有新事实
- [ ] 检查 keywords/ 是否有新关键词
- [ ] 对比与旧系统的同步

---

*小猩 🦧*
*最后更新: 2026-03-01*
