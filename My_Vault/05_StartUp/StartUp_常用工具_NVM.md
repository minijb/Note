---
title: 常用工具 - NVM
date: 2026-03-21
tags:
  - type/cheatsheet
  - tool/nvm
  - tool/node
aliases:
  - NVM速查
  - Node版本管理
description: NVM (Node Version Manager) 常用命令速查
draft: false
---

# 常用工具 - NVM

> **速查表** — NVM 常用命令和用法

## 快速导航
- [Windows 安装](#windows-安装)
- [Linux/macOS 安装](#linuxmacos-安装)
- [常用命令](#常用命令)

---

## Windows 安装

**推荐使用 NVM for Windows**

下载地址：[github.com/coreybutler/nvm-windows](https://github.com/coreybutler/nvm-windows)

```powershell
# 以管理员身份运行命令提示符
# 安装完成后验证
nvm version
```

---

## Linux/macOS 安装

```bash
# 安装 NVM
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash

# 加载环境变量
source ~/.bashrc

# 验证安装
nvm --version
```

---

## 常用命令

| 命令 | 说明 |
|------|------|
| `nvm install <version>` | 安装指定版本 |
| `nvm use <version>` | 切换到指定版本 |
| `nvm ls` | 列出已安装版本 |
| `nvm ls-remote` | 列出可安装版本 |
| `nvm alias default <version>` | 设置默认版本 |
| `nvm uninstall <version>` | 卸载指定版本 |
| `nvm current` | 显示当前版本 |

### 常用操作示例

```bash
# 安装最新版 Node
nvm install node

# 安装特定版本
nvm install 20

# 切换版本
nvm use 20

# 设置默认版本
nvm alias default 20
```

---

## 相关链接

- [NVM 官方仓库](https://github.com/nvm-sh/nvm)
- [NVM Windows 仓库](https://github.com/coreybutler/nvm-windows)
