---
title: Claude Code MCP 使用指南
date: 2026-03-23
tags:
  - type/tutorial
  - AI/ClaudeCode
  - MCP
aliases:
  - Claude Code MCP Guide
description: MCP（Model Context Protocol）服务器配置、推荐与故障排除
draft: false
---

# Claude Code MCP 使用指南

> **教程** — MCP 服务器配置与使用

## 前置要求
- Claude Code 已安装
- Node.js / npm 环境（部分 MCP 服务器需要）
- 基础命令行操作能力

---

## MCP 基础概念

MCP（Model Context Protocol）是 Anthropic 推出的开源通信标准，让 Claude Code 可以：

- 📁 访问本地文件系统
- 🌐 连接各种 API 服务
- 🗄️ 操作数据库
- 🛠️ 集成开发工具
- 🔧 自动化任务

---

## 作用域配置

| 作用域 | 配置位置 | 适用场景 | 命令标志 |
|--------|----------|----------|----------|
| Local | 当前目录 `.mcp.json` | 项目特定工具 | 默认（无标记） |
| User | `~/.claude/settings.json` | 全局常用工具 | `-s user` 或 `--scope user` |
| Project | `.mcp.json`（团队共享） | 团队共享工具 | `-s project` 或 `--scope project` |

### 作用域命令详解

```bash
# 查看当前作用域的 MCP 服务器
claude mcp list

# 指定作用域添加 MCP 服务器
claude mcp add <名称> --scope <作用域> -- <命令> [参数]
claude mcp add <名称> -s <作用域> -- <命令> [参数]

# 作用域简写
-s, --scope   # 两者等效

# 示例：添加不同作用域
# 用户级（全局可用）
claude mcp add filesystem -s user -- npx -y @modelcontextprotocol/server-filesystem ~/Documents

# 项目级（仅当前项目可用）
claude mcp add github -s project -- npx -y @modelcontextprotocol/server-github

# 本地级（当前目录可用）
claude mcp add db -s local -- npx -y @modelcontextprotocol/server-postgres
```

### 作用域优先级

当存在多个作用域的配置时，Claude Code 按以下优先级加载：

1. **Local（本地）** > **Project（项目）** > **User（用户）**
2. 相同工具名的本地配置会覆盖全局配置
3. 使用 `/mcp` 命令可查看当前加载的所有 MCP 服务器及所属作用域

---

## 添加 MCP 服务器

### 方法 1：命令行添加（推荐新手）

```bash
# 基本语法
claude mcp add <名称> [选项] -- <命令> [参数...]

# 添加文件系统访问
claude mcp add filesystem -s user -- npx -y @modelcontextprotocol/server-filesystem ~/Documents ~/Projects

# 添加 GitHub 集成
claude mcp add github -s user -e GITHUB_TOKEN=your_token -- npx -y @modelcontextprotocol/server-github
```

### 方法 2：配置文件（推荐高级用户）

编辑 `~/.claude/settings.json`：

```json
{
  "mcpServers": {
    "filesystem": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/username/Documents"],
      "env": {}
    },
    "github": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "your_github_token"
      }
    }
  }
}
```

#### Windows 配置文件格式

在 Windows 下使用 `cmd /c` 的配置格式：

```json
{
  "mcpServers": {
    "filesystem": {
      "type": "stdio",
      "command": "cmd",
      "args": ["/c", "npx -y @modelcontextprotocol/server-filesystem C:/Users/username/Documents"],
      "env": {}
    },
    "context7": {
      "type": "stdio",
      "command": "cmd",
      "args": ["/c", "npx -y @upstash/context7-mcp --api-key=YOUR_API_KEY"],
      "env": {}
    }
  }
}
```

> **注意**：Windows 配置中 `command` 必须是 `"cmd"`，`args` 数组的第一个元素必须是 `"/c`，后续才是实际的命令和参数。

### 3. Windows 下添加 MCP 服务器正确姿势

在 Windows 环境下，直接使用 `npx` 或其他系统命令可能会失败（特别是在使用最新版本的 Claude Code 或特定的 shell 下）。

**关键规则**：必须使用 `cmd /c` 前缀来包裹执行命令。

```bash
# 基本语法
claude mcp add <名称> [选项] -- cmd /c "执行命令及参数"

# 示例 1：添加 Context7
claude mcp add context7 -- cmd /c "npx -y @upstash/context7-mcp --api-key=YOUR_API_KEY"

# 示例 2：添加文件系统（注意路径使用正斜杠或双反斜杠）
claude mcp add filesystem -s user -- cmd /c "npx -y @modelcontextprotocol/server-filesystem C:/Users/username/Documents"

# 示例 3：带环境变量的命令
claude mcp add github -s user -e GITHUB_TOKEN=your_token -- cmd /c "npx -y @modelcontextprotocol/server-github"
```

> **注意**：如果不使用 `cmd /c`，可能会遇到诸如 `ENOENT`（找不到命令）或由于 Windows shell 解析导致的参数错误。
> 在修改 `settings.json` 直接配置时，也需要将 `command` 设为 `cmd`，并在 `args` 中添加 `/c` 及后续命令。

---

## 10 个必备 MCP 服务器

### 1. 文件系统访问（必装）

```bash
claude mcp add filesystem -s user -- npx -y @modelcontextprotocol/server-filesystem ~/Documents ~/Projects ~/Desktop
```

**用途**：让 Claude 直接读写文件，修改代码

### 2. GitHub 集成

```bash
claude mcp add github -s user -e GITHUB_TOKEN=your_token -- npx -y @modelcontextprotocol/server-github
```

**用途**：管理 Issues、PRs、代码审查

### 3. Sequential Thinking（思维链）

```bash
claude mcp add thinking -s user -- npx -y @modelcontextprotocol/server-sequential-thinking
```

**用途**：复杂问题分步骤思考，适合架构设计和问题分析

### 4. Context 7（文档库）

```bash
claude mcp add context7 -s user -- npx -y @context7/mcp-server
```

**用途**：访问大量开源项目文档，代码理解更准确

### 5. Brave Search（AI 增强搜索）

```bash
claude mcp add search -s user -e BRAVE_API_KEY=your_key -- npx -y @modelcontextprotocol/server-brave-search
```

**用途**：搜索最新信息，AI 增强的网络搜索

### 6. Puppeteer（浏览器自动化）

```bash
claude mcp add puppeteer -s user -- npx -y @modelcontextprotocol/server-puppeteer
```

**用途**：自动化网页操作、爬虫、UI 测试

### 7. PostgreSQL 数据库

```bash
claude mcp add postgres -s user -e DATABASE_URL=postgresql://user:pass@localhost/db -- npx -y @modelcontextprotocol/server-postgres
```

**用途**：直接查询和操作数据库

### 8. Fetch（API 调用）

```bash
claude mcp add fetch -s user -- npx -y @kazuph/mcp-fetch
```

**用途**：调用各种 REST API

### 9. Slack 集成

```bash
claude mcp add slack -s user -e SLACK_TOKEN=your_token -- npx -y @modelcontextprotocol/server-slack
```

**用途**：发送消息、管理频道

### 10. Memory（记忆存储）

```bash
claude mcp add memory -s user -- npx -y @modelcontextprotocol/server-memory
```

**用途**：跨对话保存信息

---

## 其他推荐 MCP

| MCP 名称 | 用途 | 场景 |
|----------|------|------|
| `figma` | Figma 设计稿读取 | UI 开发 |
| `playwright` | 浏览器自动化 | Web 测试 |
| `linear` | 任务管理 | 项目管理 |
| `sentry` | 错误监控 | 线上问题追踪 |
| `jira` | 企业任务管理 | 团队协作 |

### 数据流转分析（实用技巧）

使用 MCP 分析数据在代码中的流转路径：

```
帮我梳理一下用户上级 id 的数据流转
```

这可以查看变量或数据所在的层级及使用场景，非常实用。

---

## MCP 管理命令

```bash
# 查看已安装的 MCP 服务器
claude mcp list

# 删除 MCP 服务器
claude mcp remove <server_name>

# 测试 MCP 服务器
claude mcp test <server_name>

# 从 Claude Desktop 导入
claude mcp add-from-claude-desktop

# 查看 MCP 状态
/mcp
```

---

## 故障排除

### 常见错误 1：工具名称验证失败

```text
API Error 400: "tools.11.custom.name: String should match pattern '^[a-zA-Z0-9_-]{1,64}'"
```

**解决方案**：
- 确保服务器名称只包含字母、数字、下划线和连字符
- 名称长度不超过 64 个字符

### 常见错误 2：找不到 MCP 服务器

```text
MCP server 'my-server' not found
```

**解决方案**：
1. 检查作用域设置是否正确
2. 运行 `claude mcp list` 确认服务器已添加
3. 重启 Claude Code

### 常见错误 3：Windows 路径问题

```text
Error: Cannot find module 'C:UsersusernameDocuments'
```

**解决方案**：使用正斜杠或双反斜杠

```bash
# 正确方式
claude mcp add fs -- npx -y @modelcontextprotocol/server-filesystem C:/Users/username/Documents
```

---

## 调试技巧

```bash
# 启用调试模式
claude --mcp-debug

# 查看日志文件
# macOS
tail -f ~/Library/Logs/Claude/mcp*.log
# Windows
type "%APPDATA%\Claude\logs\mcp*.log"

# 手动测试服务器
npx -y @modelcontextprotocol/server-filesystem ~/Documents
```

---

## 参考资源

- [MCP 官方文档](https://zhuanlan.zhihu.com/p/1966486877088506681) — 最重要
- [Claude Code MCP 十大必装](https://help.apiyi.com/claude-code-mcp-top-10-must-install.html)
- [CSDN MCP 配置教程](https://blog.csdn.net/m0_74837192/article/details/150616899)
- [博客园 MCP 详解](https://www.cnblogs.com/wind-xwj/p/19675511)

---

## 相关笔记

- [[00_Claude_Code_速查表]]
- [[Claude Code Agents 与 Commands]]
- [[Claude Code 记忆系统]]
- [[Claude Code 进阶工作流]]
