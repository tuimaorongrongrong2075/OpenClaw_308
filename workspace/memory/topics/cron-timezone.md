# Cron 时区问题与修复

> 创建时间: 2026-03-05

## 问题

所有 cron 任务没有添加 `--tz "Asia/Shanghai"` 参数，导致按 UTC 执行。

## 症状

- 设置 9:00 执行，实际 17:00（UTC 9点）才执行
- 任务执行了但用户没收到通知（message failed）
- 重复任务堆积

## 解决方案

### 1. 创建任务时必须加参数
```bash
# ✅ 正确
openclaw cron add --name "任务名" --cron "0 9 * * *" --tz "Asia/Shanghai" ...

# ❌ 错误
openclaw cron add --name "任务名" --cron "0 9 * * *" ...
```

### 2. 删除重复任务
```bash
openclaw cron delete <任务ID>
```

## 验证
```bash
openclaw cron list | grep "Asia/Shanghai"
```

---

## 经验教训

1. 所有 cron 必须加 `--tz "Asia/Shanghai"`
2. 文档记录到 TOOLS.md 和 Memory_Restore_Guide.md

---

*最后更新: 2026-03-05*
