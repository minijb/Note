---
title: Claude Code 进阶工作流
date: 2026-03-23
tags:
  - type/tutorial
  - AI/ClaudeCode
aliases:
  - Claude Code Advanced Workflow
description: Claude Code 与 WSL2、Tmux、Windows Terminal 的集成使用
draft: false
---

# Claude Code 进阶工作流

> **教程** — 终端配置、多会话管理与高效工作流

## 前置要求
- WSL2 已安装（Windows 用户推荐）
- Tmux 基础了解
- Windows Terminal 或类似终端

---

## WSL2 安装与配置

### 推荐方案

在 WSL2 中安装 Claude Code，通过代理在 Windows 中使用。

### 参考资源

- [WSL2 + Claude Code 配置教程](https://zhuanlan.zhihu.com/p/2009054711144288460)

### 基本步骤

```bash
# 1. 在 WSL2 中安装 Claude Code
curl -sL https://.githubusercontent.com/anthropics/claude-code-cli/releases/latest/download/install.sh | sh

# 2. 配置代理（如果需要）
export http_proxy=http://localhost:7890
export https_proxy=http://localhost:7890

# 3. 创建 Windows 别名方便调用
# 在 Windows 终端中
doskey claude=wsl -e claude $*
```

### WSL2 优势

| 优势 | 说明 |
|------|------|
| 原生 Linux 环境 | 更好的 Shell 体验 |
| 高效文件访问 | `/mnt/c/` 访问 Windows 文件 |
| 开发工具兼容 | 更丰富的命令行工具 |

---

## Tmux 终端复用

Tmux 让你在单个终端中运行多个会话，适合需要同时操作多个项目的场景。

### Windows 上的替代方案

| 方案 | 说明 |
|------|------|
| Windows Terminal | 内置分屏功能 |
| Tmux + WSL2 | 完整 Tmux 体验 |
| Windows Terminal + Tmux | 最佳组合 |

### 基础操作

```bash
# 安装 tmux（WSL2）
sudo apt install tmux

# 启动 tmux
tmux

# 常用快捷键（Ctrl+b 后按）
# --- 会话 ---
new -s mysession    # 创建新会话
d                  # 分离会话
ls                 # 列出会话
attach -t mysession  # 重新连接

# --- 窗口 ---
c                  # 创建新窗口
n / p              # 下/上一个窗口
w                  # 列出所有窗口
,                  # 重命名窗口

# --- 分屏 ---
%                  # 垂直分屏
"                  # 水平分屏
o                  # 切换面板
x                  # 关闭面板
space              # 切换布局
```

### Tmux + Claude Code 工作流

```bash
# 场景：同时开发多个项目

# 1. 启动 tmux
tmux new -s work

# 2. 创建多个窗口
# 窗口 1: 主项目开发
# 窗口 2: 笔记整理
# 窗口 3: 资料查询

# 3. 在每个窗口启动 Claude Code
# 窗口 1
cd ~/projects/my-game
claude

# 窗口 2
cd ~/notes
claude

# 窗口 3（无 Claude Code，仅查询）
```

### Tmux 配置示例

创建 `~/.tmux.conf`：

```bash
# 基础配置
set -g prefix C-a
unbind C-b
bind C-a send-prefix

# 鼠标支持
set -g mouse on

# 更好的配色
set -g default-terminal "screen-256color"

# 状态栏
set -g status-left "#[fg=green]#S #[fg=white]| "
set -g status-right "#[fg=yellow]%Y-%m-%d %H:%M"

# 窗口从 1 开始
set -g base-index 1
setw -g pane-base-index 1
```

---

## Windows Terminal 配置

### 分屏操作

| 快捷键 | 功能 |
|--------|------|
| `Alt + Shift + +` | 垂直分屏 |
| `Alt + Shift + -` | 水平分屏 |
| `Alt + 方向键` | 切换面板 |

### 设置文件

编辑 `settings.json`：

```json
{
  "profiles": {
    "defaults": {
      "colorScheme": "One Dark",
      "font": {
        "face": "Cascadia Code",
        "size": 12
      }
    },
    "list": [
      {
        "name": "WSL",
        "commandline": "wsl.exe -d Ubuntu",
        "startingDirectory": "~"
      }
    ]
  }
}
```

---

## 后台运行

### Bash 后台任务

```bash
# 后台运行
rum python -m http.server 8080 &

# 或使用 Claude Code 的 run_in_background
# 在 Claude Code 中
run python -m http.server 8080

# 查看后台任务
jobs

# 切回前台
fg %1

# 停止任务
kill %1
```

### 持久化后台服务

```bash
# 使用 nohup
nohup python -m http.server 8080 > server.log 2>&1 &

# 使用 systemd（WSL2）
# 创建 ~/.config/systemd/user/python-server.service
[Unit]
Description=Python HTTP Server

[Service]
ExecStart=/usr/bin/python3 -m http.server 8080
WorkingDirectory=/home/user/www
Restart=always

[Install]
WantedBy=default.target

# 启用服务
systemctl --user enable python-server
systemctl --user start python-server
```

---

## 多会话管理

### 场景：同时开发多个项目

```bash
# 方法 1: Tmux 多窗口
tmux new -s dev
# Ctrl+b, c  创建新窗口
# 每个窗口一个项目

# 方法 2: 多个 Claude Code 会话
# 会话 1: 主项目
cd ~/projects/main
claude

# 会话 2: 辅助工具
cd ~/tools
claude

# 方法 3: 使用 Agent 分离任务
# 在单个 Claude Code 会话中使用 Agent 处理不同任务
/agents
```

### 会话切换

```bash
# 查看所有 tmux 会话
tmux list-sessions

# 切换会话
tmux switch -t mysession

# 或使用 tmux 的窗口导航
# Ctrl+b, 数字   跳转到指定窗口
```

---

## 效率提升技巧

### 1. 自定义 Commands

```markdown
# ~/.claude/commands/start-dev.md
# 启动开发环境

请帮我执行以下操作：
1. 启动 Unity 开发服务器
2. 打开 Claude Code 分析项目
3. 启动文件监控
```

### 2. 截图快速分享

Claude Code 支持直接粘贴截图：

```text
# 直接 Ctrl+V 粘贴图片
# Claude 会自动保存并分析
```

### 3. 数据流转分析

```text
# 使用 Claude Code 追踪代码中的数据流转
# 示例问题
帮我梳理一下用户上级 id 的数据流转，查看变量在不同层级的使用情况
```

### 4. 记忆文件自动更新

```bash
# 在 ~/.bashrc 中添加
# 每次 cd 到项目目录时显示项目信息
cd() {
  builtin cd "$@"
  if [ -f .CLAUDE.md ]; then
    echo "📁 项目: $(head -1 .CLAUDE.md | sed 's/# //')"
  fi
}
```

---

## 参考资源

- [B 站 Tmux 教程](https://www.bilibili.com/video/BV1WBbszvE9A)
- [B 站 WSL2 Claude Code 安装](https://www.bilibili.com/video/BV1kv3ez2E2B)
- [Claude Code Workflow](https://catlog22.github.io/Claude-Code-Workflow/zh/)
- [Claude Deck](https://claudedeck.org)

---

## 相关笔记

- [[00_Claude_Code_速查表]]
- [[01_Claude_Code_MCP_使用指南]]
- [[02_Claude_Code_Agents与Commands]]
- [[03_Claude_Code_记忆系统]]
