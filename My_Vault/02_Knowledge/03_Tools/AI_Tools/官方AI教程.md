
# Claude Code 学习笔记

## 1. 常用流程

### 1.1 基本工作流

- **核心流程**：`context` + `plan` → 执行
- **快捷操作**：
  - `@` — 引用文件/上下文
  - `Shift + Tab` — 快速补全/切换
- **MCP（Model Context Protocol）**：只在有必要时使用，少用，会消耗大量 Token

### 1.2 自动化测试与重构

- **自动化测试**：深度思考 + plan => 可以量化
- **重构**：出现在旧表现和预期表现之间的差异
  - `@Example`：提供流程示例
  - `@Requirement`：提供需求说明
  - `@Note`：提供注意事项
- **其它额外需求**：如编写测试
- **可行的 `Optional()`**：使用多个 subagent 来制定多方案

### 1.3 Git Worktree 与多分支协作

> **笔记中标注 `??`，以下为扩展说明**

`git worktree` 是 Git 提供的功能，允许在同一个仓库下同时 checkout 多个分支到不同目录，从而实现并行开发。

```bash
# 添加一个 worktree，将 feature-x 分支 checkout 到 ../feature-x 目录
git worktree add ../feature-x feature-x

# 列出所有 worktree
git worktree list

# 删除一个 worktree
git worktree remove ../feature-x
```

**在 Claude Code 中的用法**：
- Claude Code 内置了 worktree 支持，可通过 `EnterWorktree` 命令创建隔离的工作环境
- 每个 worktree 拥有独立的分支和工作目录，适合同时处理多个功能/修复
- **使用 `git branch` 来同时加多个功能**：每个功能在独立 worktree 中开发，互不干扰

**合并**：使用 `git merge` 将所有 `.trees` 中的 worktree 合并，并解决可能的 conflict。

### 1.4 自定义钩子（Hooks）

- **传参**：非 `ARGUMENT`，而是通过 `IMPORTANT:` 指令传递上下文
- **最好**：使用 `xxx-changes.md` 来记录修改，方便追溯
- **权限控制**：在 `settings.json` 中配置

> **笔记中标注 `?`，以下为扩展说明：settings.json 权限配置方法**

Claude Code 的权限通过 `settings.json`（位于 `~/.claude/settings.json` 或项目级 `.claude/settings.json`）进行配置：

```jsonc
{
  "permissions": {
    // 允许的工具列表
    "allow": [
      "Read",
      "Glob",
      "Grep",
      "Bash(git status)",
      "Bash(npm test)"
    ],
    // 拒绝的工具列表
    "deny": [
      "Bash(rm -rf *)",
      "Bash(git push --force)"
    ]
  }
}
```

- `allow`：自动批准匹配的工具调用，无需用户确认
- `deny`：自动拒绝匹配的工具调用
- Bash 工具支持通过括号内的前缀匹配来细粒度控制命令权限

---

## 2. GitHub 集成

### 2.1 基本集成

- **安装**：`github.com/apps/claude`
- **恢复会话**：`claude --resume`
- **在 PR/Issue 中使用**：`@claude` 来触发 Claude 进行代码审查或回答问题

### 2.2 GitHub Workflow（CI/CD 集成）

> **笔记中标注 `!!! ??!`，以下为扩展说明**

Claude Code 可以集成到 GitHub Actions Workflow 中，实现自动化的代码审查、PR 处理等：

```yaml
name: Claude Code Review
on:
  pull_request:
    types: [opened, synchronize]
  issue_comment:
    types: [created]

jobs:
  claude-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Claude Code
        uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
```

**主要用途**：
- **自动 PR Review**：每次 PR 提交时自动触发 Claude 审查代码
- **Issue 自动处理**：在 Issue 中 `@claude` 可以让 Claude 分析问题并提交修复 PR
- **CI 质量门控**：将 Claude 的审查结果作为 CI 检查项

### 2.3 Hooks

- Hook 的本质：**推荐用 Bash 来构建**
- 可在特定事件（如工具调用前后）触发自定义 shell 命令

---

## 3. 操控与扩展

- **重构**：Claude Code 支持大规模代码重构
- **Jupyter**：可以直接读写和编辑 `.ipynb` Notebook 文件
- **在 Markdown 中用 `@` 引用文件**：在 CLAUDE.md 等配置文件中通过 `@` 引用项目文件作为上下文
- **用 Streamlit 来做手机优化**：可以通过生成 Streamlit 应用来快速原型化和移动端适配

---

## 4. Skill 与 Agent 体系

### 4.1 核心概念区分

| 概念 | 定义 | 用途 |
|------|------|------|
| **MCP** | 外部数据/服务接口 | Data Access — 连接外部数据库、API 等 |
| **Skill** | 领域工具、工程实践、工作流、专业知识、脚本 | 特定领域的标准化能力封装 |
| **Subagent** | 在配置的上下文中执行子任务 | 分解复杂任务并行处理 |
| **Prompt** | 快速请求 | 简单的一次性指令 |

### 4.2 Agent Skills

Agent Skills 根据 `context/expertise` 使用 `bash/filesystem` 来完成不同领域的事。

**Skills 的能力范围**：
- 包含特定**领域知识**（设计、数据、法律等）
- 封装**复杂工作流**（触发平台对接等）
- 提供**新能力**

**常见引用场景**：
- 生成 PPT（演示文稿）
- 生成 Excel Sheet
- 生成/配置 MCP Servers
- ……

### 4.3 Skill 运行平台

| 平台 | 说明 |
|------|------|
| **Claude（claude.ai）** | 在 Claude 网页/桌面端使用 |
| **Claude Code SDK** | 在 Claude Code CLI 或通过 SDK 编程调用 |

**加载机制**：
1. 先加载 **metadata**（`name` + `description`）用于判断是否匹配
2. 被触发后，才加载**整个文件**内容执行

### 4.4 Skill 文件结构（YAML frontmatter）

```yaml
---
name: skill-name          # 最大 64 字符，小写+下划线+数字
description: ...          # 最大 1024 字符，非常重要
---
```

**结构要素**：
1. **角色进入** — 定义 Skill 扮演的角色
2. **输入需求** — 明确需要用户提供什么
3. **Check** — 校验输入是否合法
4. **过程/分析** — 核心处理逻辑
5. **输出** — 结果格式和内容
6. **操作** — 实际执行的动作

**命名规则**：小写 + 单词间下划线（snake_case），文件名与 name 一致，使用 `.ing` 后缀形式描述

### 4.5 自定义 Skill 最佳实践

- **复杂度**：如果场景过于复杂要说明情况，建议控制在 **< 1500 行**以内
- **自由度**：适当留有灵活空间，让 Agent 可以做判断
- **目录结构**：
  ```
  /scripts      # 脚本文件
  /reference    # 参考资料
  /assets       # 资源文件（图标、样式等）
  ```

### 4.6 Skill 的引用资源

```
agent -> skill
  ├── skill.md          # 核心 Skill 定义
  └── other/
      ├── reference/    # 参考文档
      ├── scripts/      # 辅助脚本
      └── forms.md      # 表单模板
  或 style/
      ├── icon          # 图标
      └── assets/       # 其他资源
  或 example/           # 示例
  或 格式说明            # 输出格式定义
  ...
```

---

## 5. Skill 评测标准

评测一个 Skill 质量的标准流程：

1. **对特定的 input，使用正确的输入工具** — 能否正确识别和调用工具
2. **提取所有可学习对象** — 能否从输入中提炼关键信息
3. **生成 4+ 种类型的问题** — 覆盖多种场景和边界情况
4. **对每个问题提出指引** — 是否提供了有效的解题思路
5. **得出正确的输出** — 结果准确性
6. **成功编译** — 生成内容可执行/无语法错误
7. **输出问题到本地** — 能否正确持久化结果

---

## 6. API 与工具使用

### 6.1 沙箱中执行

- **API 方式**：在沙箱中运行 Bash 来执行各种操作
- **File API**：使用 file API 来上传/下载文件
  - 底层使用 **Python** 实现

### 6.2 Task 框架

- 使用 **Python + Typer** 构建 CLI 任务
- `task + python:typer` — 适合构建自动化任务的命令行工具

---

## 7. Skill Creator 工具

`skill-creator` 是用于创建和管理 Skill 的官方工具：

| 命令 | 功能 |
|------|------|
| `init` | 初始化一个新的 Skill 项目 |
| `zip` | 打包 Skill（将相关文件压缩） |
| `check` / `validate` | 校验 Skill 格式和内容是否合规 |

**预设 Skill 仓库**：`anthropics/skills`

### 7.1 Skill 开发思路

- **合并现有的**：合并已有 CSV 处理的 Skill
- **增加 Logo**：为 Skill 添加品牌标识
- **改进**：用数据库进行合并存储
- **用现有 PPT skills => 建多合一**：将多个演示文稿相关 Skill 整合

---

## 8. 总结：关键要点速查

| 功能 | 关键命令/配置 |
|------|-------------|
| 引用上下文 | `@文件名` 或 `@路径` |
| 快速补全 | `Shift + Tab` |
| 恢复会话 | `claude --resume` |
| GitHub 集成 | `github.com/apps/claude` |
| 多分支并行 | `git worktree add` |
| 权限配置 | `settings.json` 中的 `permissions` |
| Hook 构建 | 用 Bash 脚本实现 |
| Skill 命名 | snake_case，最大 64 字符 |
| Skill 描述 | 最大 1024 字符，包含 what/when/keyword |
| Skill 代码量 | 建议 < 1500 行 |
| Skill 创建 | `skill-creator init/zip/check` |
