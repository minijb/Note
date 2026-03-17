# Quartz + GitHub Pages 部署教程

本文详细介绍如何将 Quartz 制作的博客发布到 GitHub Pages。

[参考](https://www.lapis.cafe/posts/technicaltutorials/obsidian-quartz-4/)

---

## 准备工作

### 检查 Git 配置

在终端执行以下命令配置 Git（如果已经配置过可跳过）：

```bash
# 配置用户名（与 GitHub 用户名一致）
git config --global user.name "你的GitHub用户名"

# 配置邮箱
git config --global user.email "你的邮箱@example.com"
```

### 检查 SSH 密钥（推荐）

为了避免每次推送时输入密码，推荐配置 SSH 密钥：

```bash
# 检查是否已有 SSH 密钥
ls -la ~/.ssh
```

如果没有密钥，生成一个新的：

```bash
# 生成 SSH 密钥（直接回车使用默认路径，设置密码）
ssh-keygen -t ed25519 -C "你的邮箱@example.com"
```

然后将 `~/.ssh/id_ed25519.pub` 的内容添加到 GitHub：
- 进入 GitHub -> **Settings** -> **SSH and GPG keys** -> **New SSH key**
- 粘贴公钥内容，保存

---

## 第一步：创建 GitHub 仓库

1. 登录 [GitHub](https://github.com)
2. 点击右上角 **+** -> **New repository**
3. 填写仓库信息：
   - **Repository name**: `my-digital-garden`（也可以用其他名字）
   - **Description**: 可选描述
   - **Visibility**: 选择 **Public**（必须 Public 才能用 GitHub Pages）
4. 点击 **Create repository**

---

## 第二步：克隆 Quartz 并关联远程仓库

### 2.1 克隆 Quartz（如果还没做）

```bash
git clone https://github.com/jackyzha0/quartz.git
cd quartz
npm install
npx quartz create
# 选择 Empty Quartz
# 选择 Treat link as shortest path
```

### 2.2 关联远程仓库

进入 Quartz 项目目录，关联你刚创建的 GitHub 仓库：

```bash
# 查看当前远程仓库
git remote -v

# 如果是指向官方仓库，修改 origin 为你的仓库
git remote set-url origin https://github.com/你的用户名/my-digital-garden.git

# 验证修改结果
git remote -v
```

---

## 第三步：配置 GitHub Actions

Quartz 项目已自带 `.github/workflows/deploy.yml`，但需要确认配置正确。

### 检查 workflow 文件

打开 `.github/workflow/deploy.yml`，确保关键配置如下：

```yaml
on:
  push:
    branches: [hugo]

jobs:
  deployment:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '18'

      - name: Install dependencies
        run: npm ci

      - name: Build Quartz
        run: npx quartz build

      - name: Deploy
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./public
```

> **注意**：Quartz 4 默认使用 `hugo` 分支进行部署，而非 `main`。

---

## 第四步：同步到 GitHub

### 方式一：使用 quartz sync 命令（推荐）

```bash
npx quartz sync
```

这个命令会：
1. 自动执行 `git add .`
2. 自动提交（生成提交信息）
3. 推送到远程仓库的 `hugo` 分支

### 方式二：手动推送

如果 `quartz sync` 有问题，可以手动执行：

```bash
# 添加所有文件
git add .

# 提交（带描述信息）
git commit -m "Deploy my digital garden"

# 推送到 hugo 分支
git push origin hugo
```

---

## 第五步：启用 GitHub Pages

1. 进入 GitHub 仓库页面
2. 点击 **Settings** -> 左侧 **Pages**
3. 在 **Build and deployment** 部分：
   - **Source**: 选择 **GitHub Actions**
4. 等待几分钟，页面会显示：
   - Your GitHub Pages site is taking the time to deploy!

### 获取博客链接

部署成功后，刷新页面，**Pages** 部分会显示你的博客地址：

```
https://你的用户名.github.io/my-digital-garden/
```

---

## 第六步：自动部署（每次更新后自动发布）

上述流程配置好后，以后的工作流程非常简单：

1. **在 Obsidian 中编辑笔记**
2. **在 Quartz 目录执行同步**
   ```bash
   cd quartz
   npx quartz sync
   ```
3. **等待 1-2 分钟**，GitHub Action 会自动构建并发布

无需手动操作，GitHub 会自动检测到 `hugo` 分支的推送并触发部署。

---

## 常见问题排查

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| `quartz sync` 失败 | 可能没有关联正确的远程仓库 | 检查 `git remote -v`，确认 origin 指向你的仓库 |
| GitHub Page 显示 404 | 仓库是 Private 或还没构建完成 | 确认仓库是 Public，等待 3-5 分钟 |
| 构建失败 | Node 版本不对 | 检查 `.github/workflow/deploy.yml` 中 node-version 是否为 18 |
| 双链无法跳转 | content 目录中没有目标文件 | 确认软链接或复制已正确设置 |
| 图片不显示 | 图片路径问题 | 使用 `![[图片名.png]]` 嵌入语法 |

---

## 自定义域名（可选）

如果你有自定义域名，可以配置：

1. 进入仓库 **Settings** -> **Pages**
2. 在 **Custom domain** 输入你的域名（如 `blog.example.com`）
3. 按提示配置 DNS 记录
4. 勾选 **Enforce HTTPS**（推荐）

---

## 相关资源

- Quartz GitHub: https://github.com/jackyzha0/quartz
- GitHub Pages 文档: https://docs.github.com/en/pages
- Peaceiris Actions: https://github.com/peaceiris/actions-gh-pages