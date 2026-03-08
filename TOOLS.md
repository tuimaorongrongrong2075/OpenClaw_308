# TOOLS.md - 环境配置笔记

_章鱼的工具箱,一目了然_

## GitHub 仓库

- **仓库地址:** https://github.com/tuimaorongrongrong2075/OpenClaw_308
- **用途:** 同步备份、版本控制

## 服务器 - 飞龙在天 🐉

**基本信息:**
- **主机名:** VM-0-6-ubuntu
- **内网IP:** 10.4.0.6/22
- **公网IP:** 待确认
- **SSH端口:** 22 (默认)
- **用户:** root
- **运行时间:** 启动后自动上报

**硬件配置:**
- **CPU:** AMD EPYC 9754 (128核), 分配 2 核
- **内存:** 3.6Gi 总计, 当前可用 2.6Gi
- **硬盘:** 59Gi 总计, 已用 23Gi (40%)
- **Swap:** 9.9Gi

**系统状态 (实时监控):**
- **CPU 使用率:** [定时检查]
- **内存使用率:** [定时检查]
- **硬盘使用率:** 40% (当前)
- **系统负载:** [定时检查]
- **进程数:** 112 (当前)
- **活跃用户:** 0 (当前)
- **SSH 会话:** [定时检查]
- **开放端口:** 7 个 (当前)
- **运行服务:** 18 个 systemd 服务 (当前)

**网络配置:**
- **网卡:** eth0
- **内网网段:** 10.4.0.0/22
- **广播地址:** 10.4.3.255
- **外网访问:** 待确认

**日志系统:**
- **Journal 大小:** 8.0M
- **系统日志:** rsyslog 运行中

**关键服务:**
- SSH ✅
- Cron ✅
- NTP (chrony) ✅
- tat_agent (腾讯云) ✅
- openclaw-gateway: inactive (需要启动?)

## SSH 密钥 & 环境变量

**检查清单:**
```bash
# 检查 SSH 密钥路径
ls -la ~/.ssh/
cat ~/.ssh/config 2>/dev/null || echo "无 SSH config"

# 检查 GitHub 访问
git config --get user.name
git config --get user.email
gh auth status 2>/dev/null || echo "gh CLI 未认证"

# 检查环境变量
env | grep -i "GITHUB\|SSH\|KEY\|TOKEN" | head -20
```

**待确认:**
- SSH 私钥路径 (默认 ~/.ssh/id_ed25519 或 id_rsa)
- GitHub Token 位置 (环境变量名?)
- 腾讯云 API 密钥 (环境变量名?)

## 监控工具

**待补充:**
- 腾讯云监控访问方式?
- 告警通知渠道?
- 日志路径?

## 文档参考

- **OpenClaw Gateway 文档:** https://docs.openclaw.ai/zh-CN/gateway
- **本地文档路径:** /root/.local/share/pnpm/global/5/.pnpm/openclaw@2026.3.2_@napi-rs+canvas@0.1.95_@types+express@5.0.6_hono@4.12.5_node-llama-cpp@3.16.2/node_modules/openclaw/docs

## 飞书文档

- **运维文件夹:** https://sunsound.feishu.cn/drive/folder/SHWTfJXiilYYM1dVnFPcCcFknwh
- **用途:** 存储运维报告、事故复盘、定期检查记录
- **同步频率:** 每 6 小时(随心跳)

## 邮箱配置

**Gmail (个人):**
- 地址: tuimaorongrong@gmail.com
- IMAP: imap.gmail.com:993 (SSL)
- 认证: 应用专用密码

**QQ 邮箱 (工作):**
- 地址: 1735773453@qq.com
- IMAP: imap.qq.com:993 (SSL)
- 认证: 授权码

**QQ 邮箱 (个人):**
- 地址: 3196736@qq.com
- IMAP: imap.qq.com:993 (SSL)
- 认证: 授权码

**监控优先级:**
1. Gmail (个人) - 最高优先级
2. QQ 工作邮箱 - 高优先级
3. QQ 个人邮箱 - 中等优先级

---

_最后更新: 2026-03-08_
