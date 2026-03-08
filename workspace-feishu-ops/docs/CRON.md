# CRON.md - 定时任务配置

_章鱼的自动化任务,24/7守护_

## 定时任务列表

### 1. 心跳检查 (每6小时)
```bash
0 */6 * * * /root/.openclaw/workspace-feishu-ops/workspace-feishu-ops/scripts/heartbeat.sh >> /root/.openclaw/workspace-feishu-ops/workspace-feishu-ops/logs/heartbeat.log 2>&1
```

**执行时间:** 02:00, 08:00, 14:00, 20:00 (北京时间)

**检查内容:**
- GitHub 同步状态
- 服务器健康 (飞龙在天)
- Gateway 状态
- 网络状态
- 安全检查
- 自我健康检查
- 飞书文档同步
- 备份状态

---

### 2. 邮件检查 (每天2次)
```bash
0 9,16 * * * /usr/bin/python3 /root/.openclaw/workspace-feishu-ops/workspace-feishu-ops/scripts/email-check.py >> /root/.openclaw/workspace-feishu-ops/workspace-feishu-ops/logs/email-check.log 2>&1
```

**执行时间:** 
- 上午 09:00
- 下午 16:00

**功能:**
- 检查 3 个邮箱未读邮件
- 按重要性分级 (紧急/重要/普通)
- 为需要回复的邮件生成草稿
- 结果保存到 `email-check-result.json`

**汇报方式:**
- 🔴 紧急邮件 → 立即飞书通知
- 🟡 重要邮件 → 飞书通知 + 草稿已生成
- 🟢 普通邮件 → 记录存档

---

### 3. 天气预报推送 (每天早上8点)
```bash
0 8 * * * /root/.openclaw/workspace-feishu-ops/workspace-feishu-ops/scripts/weather.sh >> /root/.openclaw/workspace-feishu-ops/workspace-feishu-ops/logs/weather.log 2>&1
```

**执行时间:** 上午 08:00

**功能:**
- 获取上海天气预报
- 推送到飞书
- 保存日志

---

## 安装定时任务

### 方法 1: 手动添加 crontab
```bash
crontab -e
```

添加以下内容:
```bash
# 胡搞的定时任务
0 */6 * * * /root/.openclaw/workspace-feishu-ops/workspace-feishu-ops/scripts/heartbeat.sh >> /root/.openclaw/workspace-feishu-ops/workspace-feishu-ops/logs/heartbeat.log 2>&1
0 9,16 * * * /usr/bin/python3 /root/.openclaw/workspace-feishu-ops/workspace-feishu-ops/scripts/email-check.py >> /root/.openclaw/workspace-feishu-ops/workspace-feishu-ops/logs/email-check.log 2>&1
0 8 * * * /root/.openclaw/workspace-feishu-ops/workspace-feishu-ops/scripts/weather.sh >> /root/.openclaw/workspace-feishu-ops/workspace-feishu-ops/logs/weather.log 2>&1
```

### 方法 2: 使用脚本安装
```bash
./scripts/install-cron.sh
```

---

## 验证定时任务

### 查看当前 crontab:
```bash
crontab -l
```

### 查看执行日志:
```bash
tail -f logs/heartbeat.log
tail -f logs/email-check.log
tail -f logs/weather.log
```

### 手动测试:
```bash
./scripts/heartbeat.sh
./scripts/email-check.py
./scripts/weather.sh
```

---

## 状态追踪

**日志目录:** `/root/.openclaw/workspace-feishu-ops/workspace-feishu-ops/logs/`

**日志文件:**
- `heartbeat.log` - 心跳检查日志
- `email-check.log` - 邮件检查日志
- `weather.log` - 天气推送日志

**状态文件:**
- `email-check-result.json` - 邮件检查结果
- `heartbeat-state.json` - 心跳状态

---

_创建时间: 2026-03-08_