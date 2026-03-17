# Quartz 4 搭建教程：从 Obsidian 到静态博客

Quartz 4 是完全重写的版本，基于 Node.js，速度极快，原生完美支持 Obsidian 的双向链接、标签、Callouts 等特殊语法。

[元数据](https://blog.csdn.net/gitblog_00228/article/details/151281180)
[配置教程](https://www.lapis.cafe/posts/technicaltutorials/obsidian-quartz-4/)

> **前置条件**：需要 Git 和 Node.js (v18.14+) 环境。

---

## 第一阶段：初始化 Quartz

打开终端（Terminal 或 Git Bash），在你希望存放博客代码的目录（比如 `D:\N\MyBlog`，建议**不要**直接放在 `My_Vault` 里面）执行：

### 1.1 克隆 Quartz 仓库

```bash
git clone https://github.com/jackyzha0/quartz.git
cd quartz
```

### 1.2 安装依赖

```bash
npm install
```

### 1.3 初始化 Quartz

```bash
npx quartz create
```

*终端会问两个问题：*

- **Choose how to initialize the content in `quartz/content`:** 选择 `Empty Quartz`
- **Choose how Quartz should resolve link:** 选择 `Treat link as shortest path`

---

## 第二阶段：连接你的 Obsidian 笔记

让 Quartz 知道你的笔记在哪，有两种方式：

### 方式一：软链接（Symlink）- 推荐

无需每次手动复制，Quartz 直接读取你的 Obsidian 文件。

**Windows (以管理员身份运行终端):**

```cmd
rmdir /S /Q content
mklink /D content "D:\N\My_Vault\02_Knowledge"
```

**macOS / Linux:**

```bash
rm -rf content
ln -s /path/to/your/obsidian/folder content
```

### 方式二：手动复制

直接把要发布的 `.md` 文件和图片复制到 `quartz/content/` 文件夹。

---

## 第三阶段：本地预览

### 3.1 启动本地开发服务器

```bash
npx quartz build --serve
# 或
npx quartz serve
```

### 3.2 查看效果

打开浏览器访问 `http://localhost:8080`

你会看到带有全局搜索、深色/浅色模式切换、节点关系图谱（Graph View）的页面，`[[双链]]` 和图片都已正常显示。

---

## 第四阶段：个性化配置（可选）

配置文件：`quartz.config.ts`

- **`pageTitle`**: 博客名字
- **`theme.color`**: 主题配色
- **`typography`**: 字体设置

修改后保存，网页会自动热更新。

---

## 第五阶段：发布到 GitHub Pages

### 5.1 创建 GitHub 仓库

在 GitHub 创建新仓库（如 `my-digital-garden`），设为 Public。

### 5.2 关联本地仓库到 GitHub

```bash
git remote set-url origin https://github.com/你的用户名/my-digital-garden.git
```

### 5.3 同步推送

```bash
npx quartz sync
```

会自动执行 `git add`, `git commit` 并推送到 GitHub。

### 5.4 启用 GitHub Pages

1. 进入仓库 -> **Settings** -> **Pages**
2. **Source** 选择 `GitHub Actions`
3. 等待几分钟，构建完成后得到博客链接：
   `https://你的用户名.github.io/my-digital-garden/`

---

## 常见问题

| 问题 | 解决方案 |
|------|----------|
| 软链接创建失败 | 以管理员身份运行终端，或使用方式二手动复制 |
| 图片不显示 | 确保图片路径正确，Quartz 支持 `![[嵌入]]` 和相对路径图片 |
| 双链404 | 检查链接目标文件是否存在于 `content` 目录中 |

---

## 相关资源

- Quartz 官方 GitHub: https://github.com/jackyzha0/quartz
- Quartz 官方文档: https://quartz.jzhao.xyz