# GitHub API 配置说明

> 最后更新: 2026-02-24
> 用途: GitHub API 和 CLI 认证配置

---

## 🔑 获取 GitHub Personal Access Token (PAT)

### 步骤：

1. **登录 GitHub**
   - 访问：https://github.com
   - 使用你的账号登录

2. **生成 Token**
   - 访问：https://github.com/settings/tokens
   - 点击 "Generate new token" (classic)
   - 或访问：https://github.com/settings/tokens/new

3. **配置 Token**
   - **Note（名称）**: OpenClaw-GitHub-CLI
   - **Expiration（过期时间）: No expiration（永不过期）或选择合适的时间
   - **Scopes（权限）**: 勾选以下权限：
     - ✅ `repo` - 完整的仓库访问权限
     - ✅ `public_repo` - 访问公共仓库
     - ✅ `read:org` - 读取组织信息（如果需要）
     - ✅ `user` - 读取用户信息
     - ✅ `workflow` - GitHub Actions 权限（如果需要）

4. **生成并复制**
   - 点击 "Generate token"
   - **重要**: 立即复制 token（只显示一次！）

---

## 🔧 配置方式

### 方式 1: 使用 gh CLI（推荐）

```bash
# 登录认证
gh auth login

# 按提示选择：
# 1. GitHub.com
# 2. HTTPS
# 3. Login with a browser (推荐) 或 Paste an authentication token
```

**使用浏览器登录:**
- 会自动打开浏览器
- 在浏览器中授权即可

**使用 Token:**
- 粘贴刚才生成的 token

### 方式 2: 手动设置环境变量

```bash
# 编辑 ~/.bashrc
cat >> ~/.bashrc << 'EOF'

# GitHub API Token
export GITHUB_TOKEN="<你的 GitHub Token>"
export GH_TOKEN="<你的 GitHub Token>"  # gh CLI 使用

EOF

# 重新加载
source ~/.bashrc
```

### 方式 3: 设置 Git Credential

```bash
# 使用 gh CLI 存储 token
gh auth login --with-token

# 粘贴 token
```

---

## 🧪 验证配置

### 测试 gh CLI
```bash
# 查看认证状态
gh auth status

# 查看当前用户
gh api user

# 列出仓库
gh repo list
```

### 测试 API 访问
```bash
# 使用 curl 测试
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/user
```

---

## 📝 使用场景

配置完成后，你可以：

1. **搜索仓库**
   ```bash
   gh search repos automaton
   ```

2. **查看 README**
   ```bash
   gh repo view 用户名/automaton
   ```

3. **克隆仓库**
   ```bash
   gh repo clone 用户名/automaton
   ```

4. **API 调用**
   ```bash
   gh api repos/用户名/automaton/readme
   ```

---

## 🔒 安全提醒

- ⚠️ **Token 就像密码一样重要**，妥善保管
- ⚠️ **不要**将 Token 提交到 Git
- ⚠️ **定期**更新 Token（建议每 6 个月）
- ✅ 使用后**立即删除**本地临时文件
- ✅ 如果 Token 泄露，立即到 GitHub 撤销并重新生成

---

## 📚 相关文档

- [GitHub Personal Access Tokens 文档](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
- [gh CLI 文档](https://cli.github.com/)
- [GitHub API 文档](https://docs.github.com/en/rest)

---

*配置完成后，即可使用 GitHub API 和 CLI*
*🦧 小猩*
