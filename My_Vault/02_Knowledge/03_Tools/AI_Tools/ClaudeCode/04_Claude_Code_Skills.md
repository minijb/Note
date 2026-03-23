---
title: Claude Code Skills 与插件系统
date: 2026-03-23
tags:
  - type/tutorial
  - AI/ClaudeCode
aliases:
  - Claude Code Skills
  - Claude Code Plugins
description: Claude Code 的 Skills 和 Plugin 系统解析及常用插件推荐
draft: false
---

# Claude Code Skills 与插件系统

> **教程** — 如何通过 Skills 赋予 Claude Code 专业知识和工作流能力。

Claude Code 默认具备强大的通用编程能力，但在特定场景下可能缺乏深度。**Skills（技能）** 让 Claude Code：
- 获得专业领域的深度知识（如 Spring Boot 安全最佳实践）
- 遵循特定规范和模式（如 Go 语言惯用法）
- 执行复杂的工作流（如 TDD 开发流程）
- 记忆项目上下文（跨会话保持一致性）

---

## 核心概念：Plugin 与 Skill 的区别

### Plugin（插件）
插件是 Claude Code **官方包管理体系的最小安装单位**。
- 一个完整插件必须包含根目录的 `plugin.json` 元数据配置文件。
- 可封装 1 个或多个 Skill、自定义命令（Command）、生命周期钩子（Hook）、依赖配置等内容。
- **安装时以插件为单位**，不能只安装插件内的某一个单独的 Skill。

### Skill（技能）
技能是 Claude Code **可直接调用的最小能力单元**。
- 必须包含 `SKILL.md` 元数据文件。
- 可选包含 `skill.json` 额外配置。
- **既可独立存在**（手动安装到特定目录），**也可被封装在 Plugin 插件内**（通过插件市场安装）。

---

## Skill 的目录结构

### 简单架构
最基础的 Skill 只需要一个文件夹和一个 `SKILL.md` 文件。

```txt
~/.claude/skills/          # Unix/macOS 路径，Windows 为 C:\Users\<用户名>\.claude\skills\
└── my-skill/
    └── SKILL.md
```

**核心规则**：
- 文件夹名称：Skill 的唯一标识。
- `SKILL.md`：唯一必需的文件（必须全大写，后缀 `.md` 小写）。

### 复杂架构
适用于功能更丰富的技能，支持配置、脚本和资源。

```txt
~/.claude/skills/
└── my-skill/
    ├── SKILL.md              # 必须：元数据和核心指令
    ├── skill.json            # 可选：额外的元数据配置
    ├── scripts/              # 可选：可执行脚本
    ├── references/           # 可选：参考文档
    └── assets/               # 可选：资源文件
```

**文件说明**：

| 文件 | 必须/可选 | 说明 |
|------|-----------|------|
| `SKILL.md` | **必须** | 包含元数据（name、description）和核心指令，Claude 依靠 description 决定何时激活该 Skill |
| `skill.json` | 可选 | 额外的元数据配置，如版本、作者、分类等 |
| `scripts/` | 可选 | 可执行代码（Python、Shell 等） |
| `references/`| 可选 | 参考文档和示例 |
| `assets/` | 可选 | 图片、模板等资源文件 |

---

## SKILL.md 编写规范

`SKILL.md` 的内容是 Skill 能否正确工作的核心。它分为**元数据（Frontmatter）**和**核心指令**两部分。

**SKILL.md 示例**：
```markdown
---
name: explain-code
description: Explains code with visual diagrams and analogies
---

When explaining code, always include:
1. **Start with an analogy**
2. **Draw a diagram** using ASCII art
3. **Walk through the code** step-by-step
4. **Highlight a gotcha** or common mistake
```

**关键点**：
- 元数据块中 `name` 必须与**文件夹名称一致**。
- `description` 是核心，**Claude 依靠这段描述来决定何时激活该 Skill**。准确、清晰的描述能大幅提高自动触发的准确率。

---

## 触发机制

### 自动触发（绝大多数情况）
大部分 Skills 安装后会**自动根据上下文激活**，不需要手动输入命令。

Claude Code 会实时分析：
1. 当前对话内容
2. 打开的文件类型
3. 项目结构和技术栈

**典型触发场景**：

| 场景 | 触发机制示例 |
|------|--------------|
| 打开一个 Go 项目并询问代码问题 | `go-review`、`golang-patterns` 自动提供 Go 最佳实践 |
| 粘贴一段异常栈问"这是什么问题" | 调试相关 Skills 自动分析根因 |
| 修改代码后说"帮我提交" | Git 集成 Skills 自动生成 commit message |
| 在 Spring Boot 项目中添加新功能 | `springboot-patterns`、`springboot-tdd` 提供架构指导 |
| 上传一个 PDF 并问"帮我提取关键信息" | 文档处理 Skills 自动解析内容 |

### 手动触发（少数情况）
少数 Skills 需要通过 `/` 命令手动触发，通常包括：
1. **自定义命令型 Skills**：你封装的专属工作流命令（如 `/build-java`）。
2. **明确指令型 Skills**：如 `/skill-create`（创建新技能）、`/plan`（规划任务）。

---

## 常用官方基础插件推荐

| 分类       | 插件名称                 | 说明                       | 安装命令                                                           |
| -------- | -------------------- | ------------------------ | -------------------------------------------------------------- |
| **核心基石** | code-simplifier      | 自动识别冗余代码、简化复杂逻辑、补全标准化注释  | `/plugin install code-simplifier@claude-plugins-official`      |
|          | skill-creator        | 根据需求自动生成符合规范的自定义 Skill   | `/plugin install skill-creator@claude-plugins-official`        |
|          | code-review          | 代码审查工具，提供规范检查和改进建议       | `/plugin install code-review@claude-plugins-official`          |
| **开发效率** | frontend-design      | 前端设计辅助，生成 UI 组件和样式       | `/plugin install frontend-design@claude-plugins-official`      |
|          | feature-dev          | 功能开发工作流，从需求到实现的完整流程      | `/plugin install feature-dev@claude-plugins-official`          |
|          | pr-review-toolkit    | PR 审查工具集，集成代码规范和安全性检查    | `/plugin install pr-review-toolkit@claude-plugins-official`    |
| **工程化**  | security-guidance    | 安全指导，提供安全编码最佳实践          | `/plugin install security-guidance@claude-plugins-official`    |
|          | claude-md-management | `CLAUDE.md` 文件管理，维护项目上下文 | `/plugin install claude-md-management@claude-plugins-official` |

---

## 社区高星插件推荐（精选）

这些 GitHub 高星项目经过社区广泛验证，能显著提升 Claude Code 能力。

### ⭐⭐⭐⭐⭐ everything-claude-code（强烈推荐）
> 安装这一个插件后，绝大多数其他插件都不再需要安装。

- **GitHub**: `affaan-m/everything-claude-code` | **星标**: 72k+
- **背景**: Anthropic 黑客松冠军项目，经过 10 个月实战打磨。
- **评价**: "把 Claude Code 从聊天机器人变成资深工程师"，"外挂级插件"。
- **核心能力**:
  - 包含 50+ Skills，覆盖全开发流程。
  - 热门命令：`/tdd`、`/plan`、`/go-review`、`/python-review`、`/security-review`。
  - 框架深度覆盖：Spring Boot、Django、Go、Python、Swift、React/Next.js 等。
  - 工程化支持：部署、数据库迁移、安全扫描、Docker、E2E 测试。

### superpowers（推荐）
- **GitHub**: `obra/superpowers` | **星标**: 78k+
- **背景**: 由 Claude Code 核心贡献者 Jesse Vincent 开发。
- **评价**: "让 AI 像资深工程师一样工作，而不是只会写代码的实习生"，防止"能跑但代码很烂"的问题。
- **核心能力**:
  - 内置 TDD 测试驱动开发工作流。
  - 结构化调试方法论。
  - 自动代码审查（问题按严重程度分类：Minor/Normal/Critical）。
  - 编写实施计划并在完成前验证。

### claude-mem（推荐）
- **GitHub**: `thedotmack/claude-mem` | **星标**: 34k+
- **评价**: "解决了 Claude 的金鱼记忆问题"，"让 Claude 永远不会忘记项目历史"。
- **核心能力**:
  - 跨会话记忆项目上下文、业务规则、历史修改。
  - 智能渐进式披露，按需检索相关记忆。
  - 自动压缩记忆内容，节省 Token 消耗。

### CCPlugins（按需使用）
> ⚠️ **注意**：这是 Commands（命令），不是自动触发的 Skills！必须手动输入 `/命令` 触发。

- **GitHub**: `brennercruvinel/CCPlugins`
- **特点**: 不会自动感知上下文激活，适合需要**精确控制执行时机**的开发场景。
- **核心能力**:
  - 提供 24 个专业开发斜杠命令（安装到 `~/.claude/commands/`）。
  - 开发工作流：`/commit`、`/format`、`/scaffold`、`/test`、`/refactor`。
  - 代码质量：`/review`、`/security-scan`、`/predict-issues`。
  - 会话管理：`/session-start`、`/session-end`、`/undo`。

---

## 相关笔记

- [[00_Claude_Code_MOC]]
- [[01_Claude_Code_MCP_使用指南]]
- [[02_Claude_Code_Agents与Commands]]
- [[03_Claude_Code_记忆系统]]
- [[05_Claude_Code_进阶工作流]]
