# 收藏夹一站式导出工具集

> 将B站、Get笔记、小红书、微信收藏批量导出到Obsidian
> 
> 最后更新: 2026-02-19

---

## 📋 工具清单

| 平台 | 脚本 | 难度 | 推荐方案 |
|------|------|------|---------|
| 📺 **Bilibili** | `bilibili_favorites_export.py` | ⭐⭐ | 自动导出 (需Cookie) |
| 📝 **Get笔记** | `get_notes_export.py` | ⭐⭐⭐ | 手动导出 + 脚本转换 |
| 📕 **小红书** | `xiaohongshu_favorites_export.py` | ⭐⭐⭐ | 手动收集链接 |
| 💬 **微信** | `wechat_favorites_export.py` | ⭐⭐⭐⭐ | Cubox中转 (推荐) |

---

## 🚀 快速开始

### 第一步: 创建目录结构

```bash
# 创建导出目录
mkdir -p /root/.openclaw/workspace/exports
mkdir -p /root/.openclaw/workspace/exports/bilibili_raw
mkdir -p /root/.openclaw/workspace/exports/getnotes_raw
mkdir -p /root/.openclaw/workspace/exports/xiaohongshu_raw
mkdir -p /root/.openclaw/workspace/exports/wechat_raw
```

### 第二步: 按平台导出

选择下面的平台，按照详细步骤操作。

---

## 📺 Bilibili 收藏导出

### 方法: 自动导出 (推荐)

#### 1. 获取B站UID

1. 浏览器登录 [bilibili.com](https://www.bilibili.com)
2. 点击头像 → 进入个人空间
3. 地址栏看到: `https://space.bilibili.com/12345678`
4. **UID = 12345678** (复制这个数字)

#### 2. 获取SESSDATA (登录凭证)

**Chrome/Edge浏览器:**
1. 按 `F12` 打开开发者工具
2. 切换到 **Application** (应用) 标签
3. 左侧选择 **Cookies** → `https://www.bilibili.com`
4. 找到 `SESSDATA` 这一行
5. 复制 **Value** 列的内容 (很长一串)

**快捷方法:**
1. 按 `F12` → 选择 **Console** (控制台)
2. 粘贴代码:
   ```javascript
   document.cookie.match(/SESSDATA=([^;]+)/)[1]
   ```
3. 回车，输出的就是 SESSDATA

#### 3. 配置环境变量

```bash
# 编辑环境变量文件
cat > /root/.openclaw/workspace/.env.bilibili << 'EOF'
export BILIBILI_UID="你的UID"
export BILIBILI_SESSDATA="你的SESSDATA"
EOF
```

#### 4. 执行导出

```bash
cd /root/.openclaw/workspace
python3 scripts/bilibili_favorites_export.py
```

**输出:**
- 文件位置: `exports/bilibili_favorites_收藏夹名_2026-02-19.md`
- 包含: 视频标题、链接、UP主、封面

---

## 📝 Get笔记 导出

### 方法: 手动导出 + 脚本转换

Get笔记暂不支持API自动导出，需要手动导出后转换。

#### 1. 从Get笔记App导出

1. 打开Get笔记App
2. 点击右下角 **"我的"**
3. 选择 **"设置"** → **"数据管理"**
4. 点击 **"导出笔记"**
5. 选择导出格式: **Markdown** (推荐) 或 HTML
6. 选择要导出的笔记范围
7. 导出文件会保存到手机存储

#### 2. 传输到服务器

将导出的文件传输到:
```
/root/.openclaw/workspace/exports/getnotes_raw/
```

#### 3. 执行转换

```bash
cd /root/.openclaw/workspace
python3 scripts/get_notes_export.py
```

**输出:**
- 文件位置: `exports/getnotes_export_2026-02-19.md`
- 包含: 笔记标题、内容、标签、元数据

---

## 📕 小红书 收藏导出

### 方法: 手动收集链接

小红书反爬严格，建议手动收集链接后批量处理。

#### 1. 创建链接列表文件

创建文件: `/root/.openclaw/workspace/exports/xiaohongshu_raw/links.txt`

格式:
```
# 每行一个链接，格式: URL | 标题描述
https://www.xiaohongshu.com/explore/abc123 | 穿搭分享
https://www.xiaohongshu.com/explore/def456 | 美食探店
https://www.xiaohongshu.com/explore/ghi789 | 旅行攻略
```

#### 2. 如何获取链接

**方法一: App内分享**
1. 打开小红书App
2. 进入"我" → "收藏"
3. 打开具体笔记
4. 点击右上角"..."
5. 选择"复制链接"

**方法二: 发送到文件传输助手**
1. 在收藏列表中长按笔记
2. 选择"发送给朋友"
3. 发送到"文件传输助手"
4. 在电脑端微信复制链接

#### 3. 执行导出

```bash
cd /root/.openclaw/workspace
python3 scripts/xiaohongshu_favorites_export.py
```

**输出:**
- 文件位置: `exports/xiaohongshu_favorites_收藏夹_2026-02-19.md`
- 包含: 链接、标题、标签

---

## 💬 微信 收藏导出

### 方法: Cubox中转 (推荐 ⭐⭐⭐)

#### 方案1: Cubox全自动导出

Cubox支持一键导入微信收藏，再导出到Obsidian。

**步骤:**

1. **下载 Cubox**
   - iOS/Android/Mac/Chrome插件
   - 官网: [cubox.pro](https://cubox.pro)

2. **绑定微信收藏**
   - 注册登录 Cubox
   - 设置 → 导入 → 微信收藏
   - 按提示完成授权
   - Cubox会自动同步微信收藏

3. **导出为Markdown**
   - Cubox中: 设置 → 导出
   - 选择 Markdown 格式
   - 下载导出的文件

4. **放入指定目录**
   ```
   /root/.openclaw/workspace/exports/wechat_raw/
   ```

5. **执行转换**
   ```bash
   python3 scripts/wechat_favorites_export.py
   ```

#### 方案2: 微信PC版导出

适合Windows用户。

**步骤:**
1. 电脑安装微信PC版
2. 登录微信，同步收藏
3. 打开"收藏"面板
4. 选中要导出的收藏
5. 右键 → "另存为"
   - 链接保存为 `.url` 文件
   - 笔记保存为 `.txt` 文件
6. 放入 `exports/wechat_raw/`
7. 运行导出脚本

#### 方案3: 手动整理链接

适合少量收藏。

创建文件: `exports/wechat_raw/links.txt`

格式:
```
https://mp.weixin.qq.com/xxx | 公众号文章标题
https://zhuanlan.zhihu.com/yyy | 知乎文章
```

---

## 📂 Obsidian 导入建议

### 推荐文件夹结构

```
📁 收藏夹/
  📁 00-待整理/          # 新导出的文件先放这里
  📁 01-B站收藏/
  📁 02-Get笔记/
  📁 03-小红书/
  📁 04-微信收藏/
  📁 99-归档/            # 已处理/过期
```

### Dataview 自动分类 (可选)

安装 **Dataview** 插件后，创建查询:

```dataview
table title, source, date
from "收藏夹"
where source = "Bilibili"
sort date desc
```

---

## ⚠️ 安全提示

### 敏感信息保护

- **B站SESSDATA**: 是登录凭证，不要泄露
- **各平台Cookie**: 只保存在 `.env.*` 文件中
- **.env文件**: 已添加到 `.gitignore`，不会提交到GitHub

### 账号安全

- 导出完成后可删除环境变量文件
- 定期更换各平台密码
- 不要在公共设备上保存登录状态

---

## 🔧 故障排除

### 问题1: B站导出失败

**症状**: "获取收藏夹失败" 或 "登录失效"

**解决**:
1. 检查SESSDATA是否过期 (有效期通常1个月)
2. 重新登录B站获取新的SESSDATA
3. 更新 `.env.bilibili` 文件

### 问题2: Get笔记无法自动导出

**症状**: 脚本提示需要手动导出

**解决**:
- Get笔记暂不支持API，必须使用App内导出功能
- 按照文档中的手动导出步骤操作

### 问题3: 小红书反爬

**症状**: 账号被限制或需要验证

**解决**:
- 停止自动脚本
- 使用手动收集链接的方式
- 等待24小时后再试

### 问题4: 微信收藏太多

**症状**: 导出文件过大或处理缓慢

**解决**:
1. 分批导出 (按时间段)
2. 先整理收藏，删除不需要的
3. 使用Cubox中转，利用其分类功能

---

## 📞 获取帮助

如果导出遇到问题:

1. 查看各脚本内的详细注释
2. 检查环境变量是否正确配置
3. 确认原始文件已放入正确目录
4. 询问姐姐获取最新的授权码或Cookie

---

## 📝 更新计划

- [ ] 支持更多平台 (知乎、抖音等)
- [ ] 自动同步功能 (定时导出)
- [ ] 增量导出 (只导出新收藏)
- [ ] 智能标签分类 (AI自动打标签)

---

*工具集创建者: 小猩 🦧*
*最后更新: 2026-02-19*
