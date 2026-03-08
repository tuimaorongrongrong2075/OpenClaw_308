#!/bin/bash
# =============================================================================
# 脚本名称: check_env.sh
# 功能描述: 检查并加载所有必需的环境变量
# 作者: 小猩 🦧
# 创建日期: 2026-02-18
# 版本: 1.0.0
#
# 使用方法:
#   source check_env.sh    # 在当前shell加载
#   bash check_env.sh      # 检查并报告状态
#
# 版本记录:
#   v1.0.0 (2026-02-18) - 初始版本
# =============================================================================

set -euo pipefail

# 颜色定义（仅在终端支持时启用）
if [ -t 1 ]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    NC='\033[0m'
else
    RED=''
    GREEN=''
    YELLOW=''
    NC=''
fi

# 必需的环境变量列表
declare -A REQUIRED_ENV=(
    ["GMAIL_USER"]="Gmail邮箱账号"
    ["GMAIL_APP_PASSWORD"]="Gmail应用密码"
    ["QQMAIL_USER"]="工作QQ邮箱账号"
    ["QQMAIL_AUTH_CODE"]="工作QQ邮箱授权码"
    ["QQMAIL_PERSONAL_USER"]="个人QQ邮箱账号"
    ["QQMAIL_PERSONAL_AUTH_CODE"]="个人QQ邮箱授权码"
)

# 可选的环境变量
declare -A OPTIONAL_ENV=(
    ["MOLTBOOK_API_KEY"]="Moltbook API密钥"
    ["GEMINI_API_KEY"]="Gemini API密钥"
    ["GITHUB_TOKEN"]="GitHub Token"
)

# 加载 .env.qqmail 文件
load_qqmail_env() {
    local env_file="/root/.openclaw/workspace/.env.qqmail"
    if [ -f "$env_file" ]; then
        while IFS= read -r line || [[ -n "$line" ]]; do
            # 跳过注释和空行
            [[ "$line" =~ ^#.*$ ]] && continue
            [[ -z "$line" ]] && continue
            # 处理 export KEY=value 格式
            if [[ "$line" == export* ]]; then
                line="${line#export }"
            fi
            # 提取 KEY 和 VALUE
            if [[ "$line" == *"="* ]]; then
                key="${line%%=*}"
                value="${line#*=}"
                # 去除引号
                value="${value%\"}"
                value="${value#\"}"
                value="${value%\'}"
                value="${value#\'}"
                export "$key=$value"
            fi
        done < "$env_file"
        return 0
    fi
    return 1
}

# 检查单个环境变量
check_env_var() {
    local var_name=$1
    local var_desc=$2
    local is_required=$3
    
    if [ -z "${!var_name:-}" ]; then
        if [ "$is_required" = "true" ]; then
            echo -e "${RED}❌ 缺失: $var_name${NC} ($var_desc)"
            return 1
        else
            echo -e "${YELLOW}⚠️  可选: $var_name${NC} ($var_desc)"
            return 0
        fi
    else
        # 隐藏敏感信息
        local display_value="${!var_name}"
        if [ ${#display_value} -gt 8 ]; then
            display_value="${display_value:0:4}****${display_value: -4}"
        fi
        echo -e "${GREEN}✅ 已设置: $var_name${NC} = $display_value"
        return 0
    fi
}

# 主函数
main() {
    echo "🔍 检查环境变量..."
    echo "======================"
    
    # 首先加载 QQ 邮箱配置
    if load_qqmail_env; then
        echo -e "${GREEN}✅ 已加载 .env.qqmail${NC}"
    else
        echo -e "${RED}❌ 未找到 .env.qqmail 文件${NC}"
    fi
    echo ""
    
    local missing_required=0
    local missing_optional=0
    
    # 检查必需变量
    echo "📋 必需环境变量:"
    for key in "${!REQUIRED_ENV[@]}"; do
        if ! check_env_var "$key" "${REQUIRED_ENV[$key]}" "true"; then
            ((missing_required++)) || true
        fi
    done
    
    echo ""
    echo "📋 可选环境变量:"
    for key in "${!OPTIONAL_ENV[@]}"; do
        if ! check_env_var "$key" "${OPTIONAL_ENV[$key]}" "false"; then
            ((missing_optional++)) || true
        fi
    done
    
    echo ""
    echo "======================"
    if [ $missing_required -eq 0 ]; then
        echo -e "${GREEN}✅ 所有必需环境变量已配置！${NC}"
        exit 0
    else
        echo -e "${RED}❌ 缺少 $missing_required 个必需环境变量${NC}"
        echo "请向姐姐索取缺失的配置信息"
        exit 1
    fi
}

# 如果是source执行，只加载环境变量
if [[ "${BASH_SOURCE[0]}" != "${0}" ]]; then
    load_qqmail_env > /dev/null 2>&1
    return 0
fi

# 如果是直接执行，运行检查
main "$@"
