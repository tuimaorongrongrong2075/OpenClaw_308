# SCRIPTS.md - 脚本工具清单

_章鱼的触手工具箱,一览无余_

## 📧 邮件检查脚本

### email-checker.py (Python)
**路径:** `/root/.openclaw/workspace-feishu-ops/email-checker.py`  
**权限:** `rwxr-xr-x (755)`  
**大小:** 7.5 KB  
**用途:** 智能邮件检查器

**功能:**
- 连接 3 个邮箱 (Gmail + 2个QQ邮箱)
- 未读邮件统计
- 自动分类 (紧急/重要/普通)
- 关键词识别
- 优先级排序
- 结果 JSON 导出

**运行方式:**
```bash
cd /root/.openclaw/workspace-feishu-ops
python3 email-checker.py
```

**输出文件:** `email-check-result.json`

### check-email.sh (Shell)
**路径:** `/root/.openclaw/workspace-feishu-ops/check-email.sh`  
**权限:** `rwxr-xr-x (755)`  
**大小:** 990 B  
**用途:** Shell 邮箱检查脚本 (占位符)

**运行方式:**
```bash
cd /root/.openclaw/workspace-feishu-ops
./check-email.sh
```

---

## 🚀 Git 备份脚本

### commit.sh
**路径:** `/root/.openclaw/workspace-feishu-ops/commit.sh`  
**权限:** `rwxr-xr-x (755)`  
**大小:** 1 KB  
**用途:** 自动提交和推送到 GitHub

**功能:**
- 检查更改
- 自动添加文件
- 创建带时间戳的提交
- 推送到远程仓库

**运行方式:**
```bash
cd /root/.openclaw/workspace-feishu-ops
./commit.sh
```

**提交信息格式:**
```
feat: 胡搞的配置更新 - YYYYMMDD_HHMMSS

- 更新核心配置文件
- 更新监控和心跳配置
- 更新邮箱配置
- 更新记忆文档
```

---

## 📋 脚本清单

| 脚本 | 类型 | 大小 | 权限 | 用途 |
|------|------|------|------|------|
| email-checker.py | Python | 7.5 KB | 755 | 智能邮件检查 |
| check-email.sh | Shell | 990 B | 755 | 邮箱检查占位符 |
| commit.sh | Shell | 1 KB | 755 | Git 自动备份 |

---

_最后更新: 2026-03-08 20:50_
