#!/bin/bash
#===============================================================================
# 脚本名称: audit_scripts.sh
# 脚本功能: 检查所有脚本是否符合编写规范
# 作者: 小猩 🦧
# 创建日期: 2026-02-17
# 版本: 1.0.0
#===============================================================================
# 版本记录
#===============================================================================
# v1.0.0 (2026-02-17) - 初始版本，实现基础规范检查
#===============================================================================

set -e

SCRIPTS_DIR="/root/.openclaw/workspace/scripts"
REPORT_FILE="/tmp/script_audit_report.txt"

echo "🔍 开始检查脚本规范..." > "$REPORT_FILE"
echo "======================================" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

check_script() {
    local file="$1"
    local filename=$(basename "$file")
    local issues=0
    
    echo "检查: $filename" >> "$REPORT_FILE"
    echo "--------------------------------------" >> "$REPORT_FILE"
    
    # 1. 检查 Shebang
    if ! head -1 "$file" | grep -qE "^#!/bin/(bash|sh)|^#!/usr/bin/env (bash|python|sh)"; then
        echo "❌ 缺少正确的 Shebang" >> "$REPORT_FILE"
        ((issues++))
    else
        echo "✅ Shebang 正确" >> "$REPORT_FILE"
    fi
    
    # 2. 检查文件头注释（脚本名称）
    if ! grep -q "脚本名称:" "$file"; then
        echo "❌ 缺少脚本名称" >> "$REPORT_FILE"
        ((issues++))
    else
        echo "✅ 脚本名称已标注" >> "$REPORT_FILE"
    fi
    
    # 3. 检查作者信息
    if ! grep -q "作者:" "$file"; then
        echo "❌ 缺少作者信息" >> "$REPORT_FILE"
        ((issues++))
    else
        echo "✅ 作者信息已标注" >> "$REPORT_FILE"
    fi
    
    # 4. 检查版本记录
    if ! grep -q "版本记录" "$file"; then
        echo "❌ 缺少版本记录" >> "$REPORT_FILE"
        ((issues++))
    else
        echo "✅ 版本记录已添加" >> "$REPORT_FILE"
    fi
    
    # 5. 检查函数注释（仅检查是否存在函数定义和注释）
    if grep -q "^def \|^function " "$file"; then
        if ! grep -qE "^\s*#.*函数|^\s*\"\"\"|^\s*'\'\'" "$file"; then
            echo "⚠️  有函数但缺少注释" >> "$REPORT_FILE"
        else
            echo "✅ 函数有注释" >> "$REPORT_FILE"
        fi
    fi
    
    # 6. 检查错误处理
    if ! grep -qE "set -e|try:|except" "$file"; then
        echo "⚠️  缺少错误处理 (set -e 或 try-except)" >> "$REPORT_FILE"
    else
        echo "✅ 有错误处理" >> "$REPORT_FILE"
    fi
    
    # 7. 检查日志路径（应该使用 Log/ 而不是 memory/）
    if grep -q "memory/.*\.log" "$file"; then
        echo "❌ 日志路径错误 (应使用 Log/ 目录)" >> "$REPORT_FILE"
        ((issues++))
    else
        echo "✅ 日志路径正确" >> "$REPORT_FILE"
    fi
    
    echo "" >> "$REPORT_FILE"
    
    return $issues
}

# 统计信息
total_files=0
files_with_issues=0

echo "📊 检查结果汇总" >> "$REPORT_FILE"
echo "======================================" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# 遍历所有脚本
for script in "$SCRIPTS_DIR"/*.{sh,py}; do
    [ -f "$script" ] || continue
    ((total_files++))
    
    issues=$(check_script "$script")
    if [ "$issues" -gt 0 ]; then
        ((files_with_issues++))
    fi
done

echo "" >> "$REPORT_FILE"
echo "======================================" >> "$REPORT_FILE"
echo "📈 统计" >> "$REPORT_FILE"
echo "总文件数: $total_files" >> "$REPORT_FILE"
echo "有问题: $files_with_issues" >> "$REPORT_FILE"
echo "通过率: $(( (total_files - files_with_issues) * 100 / total_files ))%" >> "$REPORT_FILE"
echo "======================================" >> "$REPORT_FILE"

cat "$REPORT_FILE"
