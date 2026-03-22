---
title: Claude Code Agents 与 Commands
date: 2026-03-23
tags:
  - type/tutorial
  - AI/ClaudeCode
aliases:
  - Claude Code Agents Commands
description: Claude Code Agents 子代理、Commands 自定义命令与 Hook 钩子系统
draft: false
---

# Claude Code Agents 与 Commands

> **教程** — 子代理、自定义命令与钩子配置

## 前置要求
- 了解 Claude Code 基础操作
- 熟悉命令行环境

---

## Commands 自定义命令

Commands 允许你创建可复用的快捷命令，类似 Shell Alias。

### 命令文件位置

```text
~/.claude/commands/xxx.md
```

### 创建自定义 Command

创建文件 `~/.claude/commands/code-review.md`：

```markdown
# 快捷代码审查

请审查当前项目的主要代码文件，关注以下方面：
1. 代码质量和最佳实践
2. 潜在的安全问题
3. 性能优化建议
4. 文档完整性

完成后总结发现的问题和建议。
```

### 使用方式

```text
# 在 Claude Code 中调用
/code-review

# 或带参数
/code-review --scope backend
```

---

## Agents 子代理

Agents 是 Claude Code 的自动化执行单元，可以独立完成复杂任务。

### Agent 文件位置

```text
~/.claude/agents/xxx.md
```

### 创建自定义 Agent

创建文件 `~/.claude/agents/find-txt.md`：

```markdown
# 查找项目中的 TXT 文件

你是文件搜索专家。使用 Glob 工具在项目中搜索所有 .txt 文件。

任务：
1. 搜索项目根目录及所有子目录
2. 列出找到的所有文件路径
3. 统计文件总数

---
type: file-search
capabilities:
  - glob
  - read
---
```

### 使用方式

```text
# 查看可用 Agent
/agents

# 调用 Agent
find-txt
```

### Agent 特点

- 可被 Claude Code 自动调用
- 支持复杂任务分解
- 可指定工具能力

---

## Hook 钩子系统

Hook 允许你在 Claude Code 的关键节点执行自定义操作。

### Hook 类型

| Hook 类型 | 触发时机 | 用途 |
|-----------|----------|------|
| `preTool` | 工具执行前 | 验证参数、日志记录 |
| `postTool` | 工具执行后 | 结果处理、通知 |
| `preTask` | 任务开始前 | 准备工作、环境检查 |
| `postTask` | 任务完成后 | 清理工作、结果汇总 |

### Hook 文件位置

```text
~/.claude/hooks/xxx.json
```

### Hook 配置示例

```json
{
  "hooks": {
    "preTool": [
      {
        "name": "log-tool-use",
        "description": "记录工具使用日志",
        "command": "echo '[$(date)] Tool: {tool_name}, Args: {tool_args}' >> ~/.claude/hooks/log.txt"
      }
    ],
    "postTool": [
      {
        "name": "validate-output",
        "description": "验证输出格式",
        "command": "jq empty {output_path} || echo 'Invalid JSON'"
      }
    ]
  }
}
```

### 常用 Hook 示例

#### 自动生成提交信息

```json
{
  "hooks": {
    "postTask": [
      {
        "name": "git-commit-msg",
        "command": "git log -1 --pretty=%B > ~/.claude/hooks/last_commit.txt"
      }
    ]
  }
}
```

#### 工具执行日志

```json
{
  "hooks": {
    "preTool": [
      {
        "name": "tool-logger",
        "command": "echo '[$(date +%Y-%m-%d\ %H:%M:%S)] Using tool: {tool_name}' >> ~/.claude/hooks/tool_usage.log"
      }
    ]
  }
}
```

### 查看 Hook

```text
/hooks
```

### Hook 调试

```bash
# 安装 jq（Windows WSL 或 macOS）
# Windows: winget install jqlang.jq
# macOS: brew install jq
# Linux: sudo apt install jq

# 测试 Hook 配置
claude --debug-hooks
```

### 简单 Hook 示例

详见官方示例：[Hooks 文档](https://code.claude.com/docs/zh-CN/hooks)

```json
{
  "hooks": {
    "preTool": [
      {
        "name": "echo-tool",
        "command": "echo 'About to use tool: {tool_name}'"
      }
    ]
  }
}
```

---

## Mode Alias

创建命令别名，简化常用命令。

### Windows CMD

```cmd
doskey crazy = claude --dangerously-skip-permissions $*
```

### macOS / Linux (Shell)

```bash
# ~/.bashrc 或 ~/.zshrc
alias cc='claude'
alias cci='claude --init'
alias cch='claude --help'
```

### Claude Code 内部

```text
/mode-alias <名称>=<命令>
```

---

## Output Style 输出风格

### 内置风格

| 风格 | 说明 |
|------|------|
| `default` | 软件工程风格（默认） |
| `explanatory` | 启发性、教育性 |
| `learning` | 学习型 |
| `new` | 创建自定义风格 |

### 使用方式

```text
/output-style explanatory
/output-style learning
/output-style new my-style
```

### 创建自定义风格

```text
/output-style new my-style

# 然后 Claude Code 会引导你配置风格参数
```

---

## 实用技巧

### 结合使用

```
# 使用 Agent 分解任务 + Hook 自动化 + Command 复用
1. 创建 TaskAgent 处理项目分析
2. 用 Hook 自动记录每次操作
3. Command 封装常用操作流程
```

### 任务分解示例

```
使用 Agent + Sequential Thinking MCP 进行复杂任务分解：
1. 创建分析 Agent
2. 配合 thinking MCP 进行多步骤思考
3. Hook 记录中间结果
```

---

## 常见问题

### Q: Commands 和 Agents 有什么区别？

| 特性 | Commands | Agents |
|------|----------|--------|
| 复杂度 | 简单提示模板 | 可包含完整工作流 |
| 执行方式 | 插入到对话 | 独立执行任务 |
| 适用场景 | 快捷操作 | 复杂自动化 |

### Q: Hook 会不会影响性能？

轻微影响，建议只保留必要的 Hook。

### Q: 如何调试 Hook？

使用 `--debug-hooks` 标志启动 Claude Code。

---

## 参考资源

- [Claude Code Hooks 官方文档](https://code.claude.com/docs/zh-CN/hooks)
- [Claude Code Agents 文档](https://docs.claude.ai/claude-code/agents)

---

## 相关笔记

- [[00_Claude_Code_速查表]]
- [[01_Claude_Code_MCP_使用指南]]
- [[Claude Code 记忆系统]]
- [[Claude Code 进阶工作流]]
