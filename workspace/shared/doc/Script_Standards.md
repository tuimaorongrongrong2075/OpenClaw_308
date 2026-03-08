# Script Standards - 脚本编写标准

> **版本**: v2.0 (合并版)
> **最后更新**: 2026-02-25
> **位置**: `shared/standards/Script_Standards.md`

---

## 📝 脚本编写规范

### 1. 文件命名

#### 基本规则
- 使用小写字母和下划线
- 描述性名称，清晰表明功能
- 示例：`check_gmail.py`, `send_notification.sh`

#### 特定前缀
- `check_` - 检查类脚本
- `send_` - 发送类脚本
- `backup_` - 备份类脚本
- `update_` - 更新类脚本

---

### 2. 脚本结构

#### 标准头部
```bash
#!/bin/bash
# 脚本名称 - 简短描述
# 作者: 小猩 🦧
# 创建日期: YYYY-MM-DD
# 最后更新: YYYY-MM-DD
# 用法: ./script_name.sh [参数]

set -euo pipefail  # 严格模式
```

#### Python 脚本头部
```python
#!/usr/bin/env python3
"""
脚本名称 - 简短描述

作者: 小猩 🦧
创建日期: YYYY-MM-DD
最后更新: YYYY-MM-DD

用法: python3 script_name.py [参数]
"""

import sys
import logging
from typing import Optional

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
```

---

### 3. 函数规范

#### 函数命名
- 使用小写字母和下划线
- 动词开头，描述功能
- 示例：`check_email()`, `send_message()`

#### 函数文档
```bash
# 函数功能描述
# 参数:
#   $1 - 参数1说明
#   $2 - 参数2说明
# 返回:
#   0 - 成功
#   1 - 失败
function_name() {
    local param1="$1"
    local param2="$2"

    # 函数体
}
```

---

### 4. 错误处理

#### Bash 错误处理
```bash
set -euo pipefail  # 严格模式

# 捕获错误
trap 'echo "❌ 错误: 命令失败，行号 $LINENO"; exit 1' ERR

# 检查命令是否存在
command -v command_name >/dev/null 2>&1 || {
    echo "❌ 错误: command_name 未安装"
    exit 1
}
```

#### Python 错误处理
```python
try:
    # 代码
except Exception as e:
    logger.error(f"❌ 错误: {e}")
    sys.exit(1)
```

---

### 5. 日志规范

#### 日志级别
- **INFO**: 正常信息
- **WARNING**: 警告信息
- **ERROR**: 错误信息
- **DEBUG**: 调试信息

#### 日志格式
```bash
# Bash
echo "✅ 成功: 操作完成"
echo "⚠️  警告: 需要注意"
echo "❌ 错误: 操作失败"
echo "🔍 调试: 详细信息"
```

```python
# Python
logger.info("✅ 成功: 操作完成")
logger.warning("⚠️  警告: 需要注意")
logger.error("❌ 错误: 操作失败")
logger.debug("🔍 调试: 详细信息")
```

---

### 6. 配置管理

#### 环境变量
```bash
# 从环境变量读取配置
: "${CONFIG_FILE:=/path/to/default/config}"
: "${LOG_LEVEL:=INFO}"

# 检查必需的环境变量
if [ -z "${REQUIRED_VAR:-}" ]; then
    echo "❌ 错误: REQUIRED_VAR 未设置"
    exit 1
fi
```

#### 配置文件
```bash
# 读取配置文件
if [ -f "$CONFIG_FILE" ]; then
    source "$CONFIG_FILE"
else
    echo "⚠️  警告: 配置文件不存在: $CONFIG_FILE"
fi
```

---

### 7. 依赖检查

#### 检查命令
```bash
check_dependencies() {
    local deps=("command1" "command2" "command3")

    for cmd in "${deps[@]}"; do
        if ! command -v "$cmd" >/dev/null 2>&1; then
            echo "❌ 错误: $cmd 未安装"
            return 1
        fi
    done

    echo "✅ 所有依赖已安装"
}
```

#### Python 依赖
```python
def check_dependencies():
    """检查 Python 依赖"""
    required = {
        'requests': 'requests',
        'yaml': 'pyyaml'
    }

    for module, package in required.items():
        try:
            __import__(module)
        except ImportError:
            logger.error(f"❌ 缺少依赖: {package}")
            sys.exit(1)
```

---

### 8. 测试规范

#### 单元测试
```bash
# 测试函数
test_function() {
    local result

    result=$(function_name "test_input")

    if [ "$result" = "expected_output" ]; then
        echo "✅ 测试通过"
        return 0
    else
        echo "❌ 测试失败"
        return 1
    fi
}
```

#### 集成测试
```python
def test_integration():
    """集成测试"""
    result = main_function()
    assert result == expected, f"测试失败: {result} != {expected}"
    logger.info("✅ 测试通过")
```

---

### 9. 文档规范

#### 脚本说明
```bash
# 脚本功能: 检查邮箱未读邮件
# 作者: 小猩 🦧
# 创建日期: 2026-02-25
#
# 用法:
#   ./check_mail.sh [gmail|qqmail|personal]
#
# 示例:
#   ./check_mail.sh gmail
#   ./check_mail.sh qqmail
#
# 依赖:
#   - curl
#   - jq
#   - python3
#
# 环境变量:
#   GMAIL_USER - Gmail 用户名
#   GMAIL_APP_PASSWORD - Gmail 应用密码
#
# 返回:
#   0 - 成功
#   1 - 失败
```

---

### 10. 版本控制

#### Git 提交信息
```bash
# 格式: <type>: <description>
#
# 类型:
#   ✨ feat - 新功能
#   🐛 fix - 修复 bug
#   📝 docs - 文档更新
#   ♻️  refactor - 重构
#   🧹 chore - 清理
#   ✅ test - 测试
#
# 示例:
#   ✨ feat: 添加邮箱检查功能
#   🐛 fix: 修复密码泄露问题
#   📝 docs: 更新使用说明
```

---

## 📋 脚本检查清单

### 发布前检查
- [ ] 脚本有执行权限 (`chmod +x`)
- [ ] 头部信息完整
- [ ] 函数有文档说明
- [ ] 错误处理完善
- [ ] 日志输出规范
- [ ] 依赖检查完整
- [ ] 配置管理合理
- [ ] 测试通过
- [ ] 文档完整

---

## 🎯 最佳实践

1. **保持简单**: 一个脚本做一件事
2. **可读性优先**: 清晰的变量名和函数名
3. **错误处理**: 捕获并处理所有可能的错误
4. **日志记录**: 记录关键操作和错误
5. **文档完整**: 清晰的使用说明和示例
6. **测试充分**: 编写测试用例
7. **版本控制**: 使用 Git 管理版本
8. **定期更新**: 保持依赖和代码更新

---

*脚本编写标准 v2.0 - 合并版*
*小猩 🦧*
*最后更新: 2026-02-25*
