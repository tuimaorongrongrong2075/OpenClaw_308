## Heartbeat 同步 (每4小时)
> 最后更新: 2026-02-27

每 4 小时执行一次，检查所有重要事项：

### 1. 邮箱检查
运行以下脚本检查所有邮箱：
1. `scripts/mail/check_gmail.py` - Gmail
2. `scripts/mail/check_qqmail.py` - 工作 QQ 邮箱
3. `scripts/mail/check_qqmail_personal.py` - 个人 QQ 邮箱
**有未读邮件时向主人报告**

### 2. Moltbook 社区活跃
1. 用浏览器打开 https://www.moltbook.com/
2. 阅读热帖，回复有价值的观点（不需要脚本，AI 用 browser 工具直接操作）
3. 有重要私信或热门讨论时向主人报告

### 3. 备忘录检查 (可选)
检查 project/memo/ 下的待办事项，有重要更新时提醒

## 重要规则

**无事只回复 HEARTBEAT_OK，不要每次都汇报！**

只有在以下情况才详细汇报：
- 有紧急邮件
- Moltbook 有重要活动（新 DM、热门讨论）
- 备忘录有重要更新

否则：
- 邮箱清空 + Moltbook 无事 → 只回 HEARTBEAT_OK
- 不要重复说 "Gmail 0封、QQ 0封、Moltbook 无事"
