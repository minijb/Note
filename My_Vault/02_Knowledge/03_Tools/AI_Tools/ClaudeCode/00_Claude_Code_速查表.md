---
title: Claude Code 速查表
date: 2026-03-23
tags:
  - type/cheatsheet
  - AI/ClaudeCode
aliases:
  - Claude Code Cheatsheet
description: Claude Code 常用命令、快捷键与模式速查
draft: false
---

# Claude Code 速查表

> **速查表** — 常用命令和用法

## 快速导航
- [会话管理](#会话管理)
- [思考模式](#思考模式)
- [上下文管理](#上下文管理)
- [MCP](#mcp)
- [快捷操作](#快捷操作)

---

## 会话管理

| 命令 | 功能 | 说明 |
|------|------|------|
| `/init` | 初始化项目 | 读取项目根目录的 CLAUDE.md 作为全局上下文 |
| `/resume` | 重新使用会话 | 恢复之前的对话上下文 |
| `/rewind` | 切换会话节点 | 回退到之前的对话节点继续 |
| `/clear` | 清空会话 | 完全重置当前对话 |
| `/compact` | 压缩对话上下文 | 保留核心信息，节省 Token |
| `/history` | 查看历史对话 | 选择之前的对话继续 |
| `/help` | 显示帮助 | 查看所有可用命令 |
| `/exit` | 退出 | 返回普通终端 |
| `/model` | 切换模型 | 选择不同的 Claude 模型 |
| `/edit` | 编辑记忆文件 | 修改用户或项目记忆 |
| `/mcp` | 查看 MCP 状态 | 查看已安装的 MCP 服务器 |
| `/context` | 查看 Token 占用 | 查看当前上下文 Token 使用情况 |
| `/hooks` | 查看钩子 | 查看已配置的 Hook |
| `/agents` | 查看 Agent | 查看已配置的 Agent |

---

## 思考模式

> 使用 `think` / `think hard` / `think harder` / `ultrathink` 切换思考深度

| 模式 | 思考深度 | Token 消耗 | 适用场景 | 响应时间 |
|------|----------|------------|----------|----------|
| `think` | 基础 | 低 | 简单问题、快速回答 | 2-5秒 |
| `think hard` | 深度 | 中 | 复杂逻辑、算法设计 | 5-15秒 |
| `think harder` | 更深度 | 高 | 架构设计、难题分析 | 15-30秒 |
| `ultrathink` | 极深度 | 极高 | 最复杂问题、创新方案 | 30-60秒 |

---

## 上下文管理

### 三个标准化文档
在复杂任务中保持上下文清晰的必备文档：
- **需求文档** — 明确目标与约束
- **项目状态** — 当前进度与问题
- **代办清单** — 待办事项追踪

### 降低上下文复杂度
```text
# 压缩上下文
/compact

# 清理会话
/clear
```

---

## MCP

```text
# 查看已安装的 MCP 服务器
claude mcp list

# 测试 MCP 服务器
claude mcp test <server_name>

# 添加 MCP 服务器
claude mcp add <名称> [选项] -- <命令> [参数...]

# 删除 MCP 服务器
claude mcp remove <server_name>

# 从 Claude Desktop 导入
claude mcp add-from-claude-desktop
```

### 常用 MCP 命令速查
```text
# 文件系统
claude mcp add filesystem -s user -- npx -y @modelcontextprotocol/server-filesystem ~/Documents

# GitHub
claude mcp add github -s user -e GITHUB_TOKEN=xxx -- npx -y @modelcontextprotocol/server-github

# Sequential Thinking
claude mcp add thinking -s user -- npx -y @modelcontextprotocol/server-sequential-thinking
```

---

## 快捷操作

### 截图粘贴
- 直接 `Ctrl+V` 粘贴图片，自动保存到附件目录

### Output Style 输出风格
```text
# 设置输出风格
/output-style [风格名称]

# 可选风格
- default     # 软件工程风格（默认）
- explanatory # 启发性、教育性
- learning    # 学习型
- 自定义风格  # 可创建新的输出风格
```

### Mode Alias
```text
# Windows CMD 创建别名
doskey crazy = claude --dangerously-skip-permissions $*
```

### Bash 后台运行
```bash
# 后台运行命令
run python -m http.server 8080 &

# 或使用 run_in_background
rum python -m xxx
```

---

## 相关笔记

- [[Claude Code MCP 使用指南]]
- [[Claude Code Agents 与 Commands]]
- [[Claude Code 记忆系统]]
- [[Claude Code 进阶工作流]]

---

> 💡 **提示**：使用 `#AI/ClaudeCode` 标签标记，可快速检索所有 Claude Code 相关笔记。
