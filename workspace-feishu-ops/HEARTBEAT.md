# HEARTBEAT.md - 定时检查清单

_章鱼的6小时体检,不漏掉任何蛛丝马迹_

## 检查频率

**每 6 小时一次** (北京时间: 02:00, 08:00, 14:00, 20:00)
**邮件检查:** 独立定时任务 (北京时间: 09:00, 16:00)

## 检查项目

### 1. GitHub 同步状态
```bash
cd /root/.openclaw/workspace-feishu-ops
git status
git log -1 --oneline
git remote -v
```
- ✅ 本地有未提交更改 → 提醒提交
- ⚠️ 远程有新提交 → 提醒拉取
- ❌ 推送失败 → 告警姐姐

### 2. 服务器健康 (飞龙在天 🐉)
```bash
# CPU & 内存
top -bn1 | head -20
free -h

# 磁盘空间
df -h

# 系统负载
uptime

# 进程数 & 会话
ps aux | wc -l
who -u
w

# CPU 核心数
nproc

# 开放端口
ss -tuln | grep LISTEN | wc -l
ss -tuln | grep LISTEN

# 运行服务
systemctl list-units --type=service --state=running | wc -l

# 最近错误日志
journalctl -p err -n 50 --since "6 hours ago" 2>/dev/null || tail -100 /var/log/syslog

# CPU 型号
cat /proc/cpuinfo | grep "model name" | head -1

# 内存详情
cat /proc/meminfo | grep -E "MemTotal|MemAvailable|Cached|Buffers"

# Journal 大小
journalctl --disk-usage
```

**告警阈值:**
- CPU > 80% 持续 5分钟 → 告警
- 内存 > 90% → 告警
- 磁盘 > 85% → 告警
- Load Average > 核心数*2 (当前阈值: 4) → 告警
- 进程数 > 500 → 告警
- 开放端口异常增加 → 告警
- SSH 会话异常 → 告警

**实时监控面板:**
```
┌─────────────────────────────────────────┐
│  飞龙在天 - VM-0-6-ubuntu               │
├─────────────────────────────────────────┤
│ CPU:     AMD EPYC 9754 (2核)            │
│ 内存:     3.6Gi (可用 2.6Gi)            │
│ 硬盘:     59Gi (已用 40%)               │
│ 负载:     [实时]                         │
│ 进程:     112                           │
│ 端口:     7 个开放                      │
│ 服务:     18 个运行                     │
│ 会话:     0 个活跃                      │
└─────────────────────────────────────────┘
```

### 3. OpenClaw Gateway 状态
```bash
openclaw gateway status
systemctl is-active openclaw-gateway
```
- 未运行 → 立即告警姐姐
- 版本过时 → 提醒升级

### 4. 网络状态
```bash
# 网络连通性
ping -c 3 8.8.8.8 > /dev/null 2>&1 && echo "外网连通" || echo "外网不通"

# DNS 解析
nslookup github.com > /dev/null 2>&1 && echo "DNS正常" || echo "DNS异常"

# 网络流量 (需要 iftop 或 nethog)
# ip -s link show eth0
```
- 外网不通 → 告警
- DNS 失败 → 告警

### 5. 安全检查
```bash
# 最近登录记录
last -n 20

# 失败登录尝试
grep "Failed password" /var/log/auth.log 2>/dev/null | tail -20 || echo "无 auth.log"

# 开放端口列表
ss -tuln | grep LISTEN

# IP 封禁状态 (fail2ban)
iptables -L -n 2>/dev/null | grep -c DROP || echo "0 个封禁"

# 最近 sudo 操作
grep sudo /var/log/auth.log 2>/dev/null | tail -10 || echo "无 sudo 日志"
```
- 异常登录 → 立即告警
- 爆破尝试 → 告警 + 建议封禁
- 可疑端口开放 → 告警
- 异常 sudo 操作 → 告警

### 6. 温度和硬件状态 (如果有 sensors)
```bash
# CPU 温度
sensors 2>/dev/null || echo "需要安装 lm-sensors"

# 硬盘健康 (需要 smartctl)
smartctl -H /dev/vda 2>/dev/null || echo "需要安装 smartmontools"
```

### 7. 飞书文档同步
```bash
# 检查飞书文件夹同步状态
# 飞书文件夹: https://sunsound.feishu.cn/drive/folder/SHWTfJXiilYYM1dVnFPcCcFknwh
```
- 上传最新运维报告
- 同步本地 memory 到飞书文档

### 8. 备份状态检查
```bash
# 检查最近的备份
ls -lht /root/.openclaw/workspace-feishu-ops/.git/logs/refs/heads/ | head -5

# 检查未提交的更改
cd /root/.openclaw/workspace-feishu-ops
git status --short
```
- 超过 24 小时未提交 → 提醒
- 未提交的重要更改 → 告警

### 9. 自我健康检查
```bash
# 工作目录大小
du -sh /root/.openclaw/workspace-feishu-ops

# 最近更新的文件
find /root/.openclaw/workspace-feishu-ops -type f -mtime -1 -ls | head -10

# 记忆文件检查
ls -lh /root/.openclaw/workspace-feishu-ops/memory/ 2>/dev/null || echo "memory 目录不存在"

# 配置文件完整性
ls -l /root/.openclaw/workspace-feishu-ops/{SOUL,IDENTITY,USER,TOOLS,HEARTBEAT,EMAIL}.md
```

## 汇报方式

**双轨存储:**
1. **飞书文档** → 创建/更新运维日志文档
2. **本地工作目录** → `memory/YYYY-MM-DD.md`

**汇报格式:**
```markdown
## 🐉 飞龙在天 - 运维体检报告 [时间]

### 📊 实时状态
```
┌─────────────────────────────────────────┐
│  CPU:     [使用率]  (2核)               │
│  内存:     [使用率]  (3.6Gi)            │
│  硬盘:     [使用率]  (59Gi)             │
│  负载:     [1min/5min/15min]            │
│  进程:     [数量]                        │
│  端口:     [数量] 个开放                │
│  服务:     [数量] 个运行                │
│  会话:     [数量] 个活跃                │
└─────────────────────────────────────────┘
```

### GitHub 状态
- ✅/⚠️/❌ 状态描述
- 最新提交: [commit]
- 未提交: [文件列表]

### Gateway 状态
- ✅/❌ 运行状态
- 版本: [版本号]

### 网络状态
- 外网: ✅/❌
- DNS: ✅/❌

### 安全检查
- 登录: [正常/异常]
- 失败尝试: [数量]
- 封禁IP: [数量]
- 可疑端口: [如有]

### 邮件状态
- 未读: [数量]
- 🔴 紧急: [数量]
- 🟡 草稿已备: [数量]

### 飞书文档
- ✅/❌ 同步状态
- 最新报告: [链接]

### 备份状态
- 上次备份: [时间]
- 未提交: [文件列表]

### 行动项
- [ ] 待处理事项 1
- [ ] 待处理事项 2

---
_汇报人: 胡搞 🐙 | 下次检查: 6小时后_
```

## 状态追踪

**心跳状态文件:** `/root/.openclaw/workspace-feishu-ops/heartbeat-state.json`

```json
{
  "lastCheck": "2026-03-08T14:00:00+08:00",
  "lastSync": "2026-03-08T12:00:00+08:00",
  "alerts": [],
  "trends": {}
}
```

---

_创建时间: 2026-03-08_
_下次检查: 6小时后_
