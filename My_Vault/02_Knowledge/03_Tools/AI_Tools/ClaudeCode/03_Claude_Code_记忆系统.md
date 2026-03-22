---
title: Claude Code 记忆系统
date: 2026-03-23
tags:
  - type/concept
  - AI/ClaudeCode
aliases:
  - Claude Code Memory System
description: Claude Code 六层记忆架构与上下文管理策略
draft: false
---

# Claude Code 记忆系统

> **概念解释** — Claude Code 如何记住你的偏好和项目信息

## 核心概念

Claude Code 的记忆系统让 AI 能够跨会话记住：
- 个人编码偏好和风格
- 项目特定配置和约定
- 常用工具和命令
- 工作流程和习惯

---

## 六层记忆架构

| 层级 | 记忆类型 | 位置 | 作用域 | 用途 |
|------|----------|------|--------|------|
| 1 | 用户记忆 | `~/.claude/CLAUDE.md` | 全局 | 个人偏好、编码风格 |
| 2 | 项目记忆 | 项目根目录 `.CLAUDE.md` | 项目 | 项目特定信息 |
| 3 | 对话记忆 | 当前会话 | 会话 | 当前任务上下文 |
| 4 | 工具记忆 | `/memory` | 会话 | 跨对话的信息 |
| 5 | MCP 记忆 | MCP 服务器 | 扩展 | 外部服务数据 |
| 6 | 记忆文件 | `~/.claude/memory/` | 可配置 | 持久化知识库 |

---

## 第一层：用户记忆

### 文件位置

```text
~/.claude/CLAUDE.md
```

### 用途

全局级别的个人偏好设置，影响所有项目。

### 示例内容

```markdown
# 用户偏好

## 编码风格
- 使用 4 空格缩进
- 始终在 if 语句使用大括号
- 变量命名使用 camelCase

## 常用语言
- 主要使用 C#
- 也会使用 Lua 和 Python

## 偏好工具
- 使用 Unity 作为游戏引擎
- 使用 Obsidian 做笔记
- VSCode 作为代码编辑器

## 工作流程
- 每次修改前先阅读相关代码
- 大改动先做备份
- 完成后简要总结改动
```

### 编辑方式

```text
/edit memory
# 或
~/.claude/CLAUDE.md  # 直接编辑文件
```

---

## 第二层：项目记忆

### 文件位置

```text
<项目根目录>/.CLAUDE.md
```

### 用途

项目级别的配置，只影响当前项目。

### 示例内容

```markdown
# 项目配置

## 项目名称
MyGame

## 技术栈
- Unity 2022.3 LTS
- C# 10
- Addressables 资源管理

## 代码规范
- 命名空间: CompanyName.GameName
- UI 脚本放在 Scripts/UI/
- 使用 [RequireComponent] 确保依赖

## 特殊要求
- 所有 MonoBehaviour 需要 EditorWindow 配置
- 资源路径使用 Path.Combine
```

### 编辑方式

```text
/edit project
```

---

## 第三层：对话记忆

### 生命周期

仅在当前会话有效，会话结束后自动清除。

### 有效管理技巧

```text
# 压缩上下文，保留核心信息
/compact

# 清空并重新开始
/clear

# 查看 Token 使用
/context
```

### 优化策略

1. **使用分段任务**：将大任务拆分为小步骤
2. **及时压缩**：Token 接近上限时使用 `/compact`
3. **总结输出**：每个阶段完成后要求总结

---

## 第四层：MCP 记忆服务器

### 安装

```bash
claude mcp add memory -s user -- npx -y @modelcontextprotocol/server-memory
```

### 用途

跨对话保存重要信息，适合：
- 项目进展记录
- 会议纪要
- 决策历史
- 知识沉淀

### 使用方式

```text
# 在对话中自然使用
Claude，请记住这个接口的 URL：https://api.example.com

# 后续对话可以直接引用
Claude，这个接口的 URL 是多少？
```

---

## 第五层：MCP 外部服务

### Context 7

```bash
claude mcp add context7 -s user -- npx -y @context7/mcp-server
```

**用途**：访问开源项目的大量文档，让 AI 更准确地理解代码。

### 其他记忆相关 MCP

| MCP | 用途 |
|-----|------|
| `filesystem` | 读取项目文档和笔记 |
| `github` | 读取 README 和项目文档 |
| `database` | 访问项目数据库 |

---

## 第六层：记忆文件目录

### 目录位置

```text
~/.claude/memory/
```

### 组织方式

```
~/.claude/memory/
├── projects/          # 项目相关信息
│   ├── mygame.md
│   └── website.md
├── concepts/          # 概念和知识
│   ├── design-patterns.md
│   └── algorithms.md
├── decisions/         # 重要决策记录
│   └── 2026-03-architecture.md
└── daily/            # 日常记录
    └── 2026-03-23.md
```

### 使用场景

```
场景：数据流转分析

问题：帮我梳理一下用户上级 id 的数据流转

效果：AI 可以追踪变量在不同层级的使用，理解数据流转路径
```

---

## 上下文管理策略

### 三个标准化文档

在复杂任务中保持清晰的必备文档：

| 文档 | 内容 | 用途 |
|------|------|------|
| 需求文档 | 目标、功能、约束 | 明确方向 |
| 项目状态 | 当前进度、问题 | 了解现状 |
| 代办清单 | 待办事项 | 追踪进度 |

### 视频笔记

> 低优先级参考：[AI 上下文管理视频](https://mp.weixin.qq.com/s/rs0ECent60Z-msREQx4jFQ)

> 重要参考：[B 站上下文管理教程](https://www.bilibili.com/video/BV1rnBKB2EME)

---

## 记忆系统进阶

### Workflow 工作流

结合记忆系统的推荐工作流：

```text
1. 项目初始化
   ↓
2. 读取 .CLAUDE.md（项目记忆）
   ↓
3. 读取用户 CLAUDE.md（个人偏好）
   ↓
4. 执行任务（对话记忆）
   ↓
5. 使用 MCP（外部知识）
   ↓
6. 必要时压缩上下文
   ↓
7. 任务完成，总结记录
```

### 参考资源

- [Claude Code 六层记忆架构](https://zhuanlan.zhihu.com/p/2012328012918596090)
- [Claude Code Workflow](https://catlog22.github.io/Claude-Code-Workflow/zh/)
- [Claude Deck](https://claudedeck.org)

---

## 相关笔记

- [[00_Claude_Code_速查表]]
- [[01_Claude_Code_MCP_使用指南]]
- [[02_Claude_Code_Agents与Commands]]
- [[Claude Code 进阶工作流]]
