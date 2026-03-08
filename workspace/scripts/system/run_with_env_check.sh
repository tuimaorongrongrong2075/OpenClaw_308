#!/bin/bash
# =============================================================================
# 脚本名称: run_with_env_check.sh
# 功能描述: 带环境变量检查的脚本执行器
# 作者: 小猩 🦧
# 创建日期: 2026-02-18
# 版本: 1.0.0
#
# 使用方法:
#   bash run_with_env_check.sh <脚本路径> [脚本参数...]
#
# 示例:
#   bash run_with_env_check.sh scripts/check_gmail.py
#   bash run_with_env_check.sh scripts/check_qqmail.py
#
# 版本记录:
#   v1.0.0 (2026-02-18) - 初始版本
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="$(dirname "$SCRIPT_DIR")"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 显示帮助
show_help() {
    echo "用法: bash run_with_env_check.sh <脚本路径> [参数...]"
    echo ""
    echo "示例:"
    echo "  bash run_with_env_check.sh scripts/check_gmail.py"
    echo "  bash run_with_env_check.sh scripts/check_qqmail.py"
    echo ""
    echo "功能:"
    echo "  1. 检查必需的环境变量"
    echo "  2. 如果缺失，提示向姐姐索取"
    echo "  3. 环境变量齐全后执行目标脚本"
}

# 检查环境变量
check_environment() {
    echo -e "${BLUE}🔍 检查环境变量...${NC}"
    
    # 加载 QQ 邮箱配置
    local env_file="$WORKSPACE_DIR/.env.qqmail"
    if [ -f "$env_file" ]; then
        while IFS= read -r line || [[ -n "$line" ]]; do
            [[ "$line" =~ ^#.*$ ]] && continue
            [[ -z "$line" ]] && continue
            if [[ "$line" == export* ]]; then
                line="${line#export }"
            fi
            if [[ "$line" == *"="* ]]; then
                key="${line%%=*}"
                value="${line#*=}"
                value="${value%\"}"; value="${value#\"}"
                value="${value%\'}"; value="${value#\'}"
                export "$key=$value"
            fi
        done < "$env_file"
    fi
    
    # 检查必需变量
    local missing_vars=()
    
    declare -a REQUIRED_VARS=(
        "GMAIL_USER:Gmail邮箱"
        "GMAIL_APP_PASSWORD:Gmail应用密码"
        "QQMAIL_USER:工作QQ邮箱"
        "QQMAIL_AUTH_CODE:工作QQ邮箱授权码"
        "QQMAIL_PERSONAL_USER:个人QQ邮箱"
        "QQMAIL_PERSONAL_AUTH_CODE:个人QQ邮箱授权码"
    )
    
    for var_info in "${REQUIRED_VARS[@]}"; do
        IFS=':' read -r var_name var_desc <<< "$var_info"
        if [ -z "${!var_name:-}" ]; then
            missing_vars+=("$var_name:$var_desc")
        fi
    done
    
    if [ ${#missing_vars[@]} -eq 0 ]; then
        echo -e "${GREEN}✅ 所有环境变量已配置${NC}"
        return 0
    else
        echo -e "${RED}❌ 缺少以下环境变量:${NC}"
        for var_info in "${missing_vars[@]}"; do
            IFS=':' read -r var_name var_desc <<< "$var_info"
            echo "   - $var_name ($var_desc)"
        done
        return 1
    fi
}

# 主函数
main() {
    if [ $# -eq 0 ] || [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
        show_help
        exit 0
    fi
    
    local target_script="$1"
    shift
    
    # 如果不是绝对路径，转换为绝对路径
    if [[ ! "$target_script" = /* ]]; then
        target_script="$WORKSPACE_DIR/$target_script"
    fi
    
    # 检查目标脚本是否存在
    if [ ! -f "$target_script" ]; then
        echo -e "${RED}❌ 脚本不存在: $target_script${NC}"
        exit 1
    fi
    
    echo "======================"
    echo "🎯 目标脚本: $(basename "$target_script")"
    echo "======================"
    echo ""
    
    # 检查环境变量
    if ! check_environment; then
        echo ""
        echo -e "${YELLOW}⚠️  环境变量不完整，无法执行脚本${NC}"
        echo ""
        echo "💡 请向姐姐索取缺失的配置信息，"
        echo "   我会保存到环境变量后再执行。"
        echo ""
        exit 1
    fi
    
    echo ""
    echo -e "${GREEN}🚀 环境变量检查通过，开始执行脚本...${NC}"
    echo "======================"
    echo ""
    
    # 执行目标脚本
    if [[ "$target_script" == *.py ]]; then
        python3 "$target_script" "$@"
    else
        bash "$target_script" "$@"
    fi
}

main "$@"
