#!/bin/bash
#===============================================================================
# 脚本名称: restore_xiaoxing.sh
# 脚本功能: 小猩一键恢复脚本 - 失忆后自动恢复所有记忆和配置
# 作者: 小猩
# 创建日期: 2026-02-18
# 版本: 1.0.0
# 依赖: git, bash
# 使用方式: bash restore_xiaoxing.sh
#===============================================================================
# 版本记录
#===============================================================================
# v1.0.0 (2026-02-18) - 初始版本，实现完整的失忆恢复流程
#===============================================================================

set -euo pipefail

#===============================================================================
# 配置
#===============================================================================
WORKSPACE_DIR="${HOME}/.openclaw/workspace"
BACKUP_DIR="${HOME}/.openclaw/workspace.bak.$(date +%Y%m%d_%H%M%S)"
REPO_URL="https://github.com/tuimaorongrong2075/OpenClaw_201.git"

# 颜色定义（用于输出）
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly NC='\033[0m' # No Color

#===============================================================================
# 函数定义
#===============================================================================

#-------------------------------------------------------------------------------
# 打印带颜色的消息
# 参数: $1=颜色 $2=消息
#-------------------------------------------------------------------------------
print_msg() {
    local color="$1"
    local msg="$2"
    echo -e "${color}${msg}${NC}"
}

#-------------------------------------------------------------------------------
# 检查命令是否存在
# 参数: $1=命令名
# 返回值: 0=存在, 1=不存在
#-------------------------------------------------------------------------------
check_command() {
    command -v "$1" &> /dev/null
}

#-------------------------------------------------------------------------------
# 验证文件是否存在
# 参数: $1=文件路径
#-------------------------------------------------------------------------------
verify_file() {
    local file="$1"
    if [ -f "$file" ]; then
        print_msg "$GREEN" "✅ $file"
        return 0
    else
        print_msg "$RED" "❌ $file 缺失"
        return 1
    fi
}

#-------------------------------------------------------------------------------
# 验证目录是否存在
# 参数: $1=目录路径
#-------------------------------------------------------------------------------
verify_dir() {
    local dir="$1"
    if [ -d "$dir" ]; then
        print_msg "$GREEN" "✅ $dir/"
        return 0
    else
        print_msg "$RED" "❌ $dir/ 缺失"
        return 1
    fi
}

#===============================================================================
# 主程序
#===============================================================================

echo "🦧 开始恢复小猩..."
echo "======================"

#-------------------------------------------------------------------------------
# 步骤 0: 检查 git
#-------------------------------------------------------------------------------
echo ""
echo "🔧 步骤 0/6: 检查 git..."
if ! check_command git; then
    print_msg "$RED" "❌ git 未安装，请先安装 git:"
    echo "   Ubuntu/Debian: apt-get update && apt-get install -y git"
    echo "   CentOS/RHEL: yum install -y git"
    exit 1
fi
print_msg "$GREEN" "✅ git 已安装"

#-------------------------------------------------------------------------------
# 步骤 1: 备份现有 workspace
#-------------------------------------------------------------------------------
echo ""
echo "📦 步骤 1/6: 检查并备份现有 workspace..."
if [ -d "$WORKSPACE_DIR" ]; then
    print_msg "$YELLOW" "⚠️  workspace 已存在，备份到:"
    echo "   $BACKUP_DIR"
    if ! mv "$WORKSPACE_DIR" "$BACKUP_DIR"; then
        print_msg "$RED" "❌ 备份失败，请手动处理: $WORKSPACE_DIR"
        exit 1
    fi
    print_msg "$GREEN" "✅ 备份完成"
else
    echo "✅ 无现有 workspace，无需备份"
fi

# 确保父目录存在
mkdir -p "${HOME}/.openclaw"

#-------------------------------------------------------------------------------
# 步骤 2: 克隆 workspace（必须先做！）
#-------------------------------------------------------------------------------
echo ""
echo "📦 步骤 2/6: 克隆 workspace（这是恢复记忆的前提）..."
echo "   从: $REPO_URL"
echo "   到: $WORKSPACE_DIR"

if ! git clone "$REPO_URL" "$WORKSPACE_DIR" 2>&1; then
    print_msg "$RED" "❌ 克隆失败，请检查:"
    echo "   1. 网络连接是否正常"
    echo "   2. GitHub 仓库是否可访问"
    echo "   3. 是否有足够的磁盘空间"
    exit 1
fi

print_msg "$GREEN" "✅ workspace 克隆完成"

#-------------------------------------------------------------------------------
# 步骤 3: 验证文件完整性
#-------------------------------------------------------------------------------
echo ""
echo "🔍 步骤 3/6: 验证文件完整性..."
cd "$WORKSPACE_DIR"

# 必需文件列表
readonly REQUIRED_FILES=("SOUL.md" "IDENTITY.md" "USER.md" "AGENTS.md" "README.md")
# 必需目录列表
readonly REQUIRED_DIRS=("memory" "scripts" "docs" "skills")

MISSING=0

# 验证文件
for file in "${REQUIRED_FILES[@]}"; do
    verify_file "$file" || ((MISSING++)) || true
done

# 验证目录
for dir in "${REQUIRED_DIRS[@]}"; do
    verify_dir "$dir" || ((MISSING++)) || true
done

if [ $MISSING -gt 0 ]; then
    echo ""
    print_msg "$YELLOW" "⚠️  警告: 有 $MISSING 个关键文件/目录缺失"
    echo "   可能克隆不完整，建议重新运行脚本"
fi

#-------------------------------------------------------------------------------
# 步骤 4: 读取身份文件
#-------------------------------------------------------------------------------
echo ""
echo "👤 步骤 4/6: 恢复身份（我是谁）..."
echo "======================"

if [ -f "SOUL.md" ]; then
    echo "📖 SOUL.md (核心人格):"
    head -20 SOUL.md
    echo ""
fi

if [ -f "IDENTITY.md" ]; then
    echo "📖 IDENTITY.md (身份定义):"
    head -15 IDENTITY.md
    echo ""
fi

if [ -f "USER.md" ]; then
    echo "📖 USER.md (主人信息):"
    head -10 USER.md
    echo ""
fi

print_msg "$GREEN" "✅ 身份文件读取完成"

#-------------------------------------------------------------------------------
# 步骤 5: 恢复长期记忆
#-------------------------------------------------------------------------------
echo ""
echo "🧠 步骤 5/6: 恢复长期记忆..."

if [ -f "memory/MEMORY.md" ]; then
    echo "📖 MEMORY.md (长期记忆):"
    head -30 memory/MEMORY.md
    echo ""
    print_msg "$GREEN" "✅ 核心记忆恢复完成"
else
    print_msg "$YELLOW" "⚠️  memory/MEMORY.md 不存在"
fi

#-------------------------------------------------------------------------------
# 步骤 6: 提示后续步骤
#-------------------------------------------------------------------------------
echo ""
echo "======================"
print_msg "$YELLOW" "⚠️  步骤 6/6: 手动配置（必须完成）"
echo "======================"
echo ""
echo "1️⃣  配置环境变量:"
echo "   编辑 ~/.bashrc，添加以下内容:"
echo ''
echo '# 小猩环境变量'
echo '# Gmail'
echo 'export GMAIL_USER="你的邮箱@gmail.com"'
echo 'export GMAIL_APP_PASSWORD="你的应用密码"'
echo ''
echo '# QQ邮箱 (工作)'
echo 'export QQMAIL_WORK_USER="你的工作邮箱"'
echo 'export QQMAIL_WORKER_AUTH_CODE="你的授权码"'
echo ''
echo '# QQ邮箱 (个人)'
echo 'export QQMAIL_PERSONAL_USER="你的个人邮箱"'
echo 'export QQMAIL_PERSONAL_AUTH_CODE="你的授权码"'
echo ''
echo '# 飞书'
echo 'export FEISHU_USER="你的飞书用户ID"'
echo ''
echo '# Moltbook'
echo 'export MOLTBOOK_API_KEY="你的Moltbook密钥"'
echo ''
echo '# GitHub'
echo 'export GITHUB_USERNAME="你的GitHub用户名"'
echo 'export GITHUB_TOKEN="你的GitHub Token"'
echo ''
echo "2️⃣  重新加载环境变量:"
echo "   source ~/.bashrc"
echo ""
echo "3️⃣  恢复定时任务:"
echo "   bash scripts/restore-cron.sh"
echo "   或查看 docs/guides/memory_restore_guide.md 中的'恢复定时任务'章节"
echo ""
echo "4️⃣  验证恢复:"
echo "   bash ${WORKSPACE_DIR}/scripts/health_check.sh"
echo ""

#===============================================================================
# 完成提示
#===============================================================================
print_msg "$GREEN" "✅ 基础恢复完成！"
echo "🦧 小猩的记忆库已找回"
echo ""
echo "💡 后续步骤:"
echo "   1. 配置环境变量 (~/.bashrc)"
echo "   2. 恢复定时任务: bash scripts/restore-cron.sh"
echo "   3. 读取完整记忆: cat ${WORKSPACE_DIR}/memory/MEMORY.md"
echo ""
echo "🆘 如果恢复失败:"
echo "   备份位置: $BACKUP_DIR"
echo "   查看日志: 向上滚动查看错误信息"
