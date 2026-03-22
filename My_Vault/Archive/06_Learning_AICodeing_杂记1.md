
使用 `/init` 初始化 claude code 项目 并读取整个库文件 Claude.md 作为全局的上下文

`/resume` 重新使用会话

`/rewind` 切换到之前的会话节点

`/Clear` 清空会话

claude code  可以进行深度思考 `ultrathink` 进行深度思考， 可以连接MCP 进行深度思考

|          |               |                |
| -------- | ------------- | -------------- |
| 命令       | 功能            | 说明             |
| /compact | 压缩对话上下文       | 保留核心信息，节省Token |
| /clear   | 清除对话历史        | 完全重置当前对话       |
| /history | 查看历史对话        | 选择之前的对话继续      |
| /edit    | 编辑记忆文件        | 修改用户或项目记忆      |
| /model   | 切换AI模型        | 选择不同的Claude模型  |
| /help    | 显示帮助          | 查看所有可用命令       |
| /exit    | 退出Claude Code | 返回普通终端         |
### Think模式对比

|              |      |         |            |        |
| ------------ | ---- | ------- | ---------- | ------ |
| 模式           | 思考深度 | Token消耗 | 适用场景       | 响应时间   |
| think        | 基础   | 低       | 简单问题、快速回答  | 2-5秒   |
| think hard   | 深度   | 中       | 复杂逻辑、算法设计  | 5-15秒  |
| think harder | 更深度  | 高       | 架构设计、难题分析  | 15-30秒 |
| ultrathink   | 极深度  | 极高      | 最复杂问题、创新方案 | 30-60秒 |

##  MCP服务器配置详解

### MCP基础概念

MCP（Model Context Protocol）是Anthropic推出的开源通信标准，让Claude Code可以：

- 📁 访问本地文件系统
- 🌐 连接各种API服务
- 🗄️ 操作数据库
- 🛠️ 集成开发工具
- 🔧 自动化任务

### MCP服务器作用域

|   |   |   |   |
|---|---|---|---|
|作用域|配置位置|适用场景|命令标志|
|Local|当前目录|项目特定工具|默认|
|User|~/.claude.json|全局常用工具|-s user|
|Project|.mcp.json|团队共享工具|-s project|

### 添加MCP服务器

**方法1：命令行添加（推荐新手）**

```text
# 基本语法
claude mcp add <名称> [选项] -- <命令> [参数...]

# 添加文件系统访问
claude mcp add filesystem -s user -- npx -y @modelcontextprotocol/server-filesystem ~/Documents ~/Projects

# 添加GitHub集成
claude mcp add github -s user -e GITHUB_TOKEN=your_token -- npx -y @modelcontextprotocol/server-github
```

**方法2：编辑配置文件（推荐高级用户）**

```text
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

## 10个必备MCP服务器

**1. 文件系统访问（必装）**

```text
claude mcp add filesystem -s user -- npx -y @modelcontextprotocol/server-filesystem ~/Documents ~/Projects ~/Desktop
```

用途：让Claude直接读写文件，修改代码

**2. GitHub集成**

```text
claude mcp add github -s user -e GITHUB_TOKEN=your_token -- npx -y @modelcontextprotocol/server-github
```

用途：管理issues、PRs、代码审查

**3. 网页浏览器控制**

```text
claude mcp add puppeteer -s user -- npx -y @modelcontextprotocol/server-puppeteer
```

用途：自动化网页操作、爬虫、测试

**4. 数据库连接（PostgreSQL）**

```text
claude mcp add postgres -s user -e DATABASE_URL=postgresql://user:pass@localhost/db -- npx -y @modelcontextprotocol/server-postgres
```

用途：直接查询和操作数据库

**5. API调用工具**

```text
claude mcp add fetch -s user -- npx -y @kazuph/mcp-fetch
```

用途：调用各种REST API

**6. 搜索引擎**

```text
claude mcp add search -s user -e BRAVE_API_KEY=your_key -- npx -y @modelcontextprotocol/server-brave-search
```

用途：搜索最新信息

**7. Slack集成**

```text
claude mcp add slack -s user -e SLACK_TOKEN=your_token -- npx -y @modelcontextprotocol/server-slack
```

用途：发送消息、管理频道

**8. 时间管理**

```text
claude mcp add time -s user -- npx -y @modelcontextprotocol/server-time
```

用途：时区转换、日期计算

**9. 内存存储**

```text
claude mcp add memory -s user -- npx -y @modelcontextprotocol/server-memory
```

用途：跨对话保存信息

**10. Sequential Thinking（思维链）**

```text
claude mcp add thinking -s user -- npx -y @modelcontextprotocol/server-sequential-thinking
```

用途：复杂问题分步骤思考

### MCP管理命令

```text
# 查看已安装的MCP服务器
claude mcp list

# 删除MCP服务器
claude mcp remove <server_name>

# 测试MCP服务器
claude mcp test <server_name>

# 查看MCP状态
/mcp
```

## MCP故障排除

**常见错误1：工具名称验证失败**

```text
API Error 400: "tools.11.custom.name: String should match pattern '^[a-zA-Z0-9_-]{1,64}'"
```

解决方案：

- 确保服务器名称只包含字母、数字、下划线和连字符
- 名称长度不超过64个字符

**常见错误2：找不到MCP服务器**

```text
MCP server 'my-server' not found
```

解决方案：

1. 检查作用域设置是否正确
2. 运行`claude mcp list`确认服务器已添加
3. 重启Claude Code

**常见错误3：Windows路径问题**

```text
Error: Cannot find module 'C:UsersusernameDocuments'
```

解决方案：使用正斜杠或双反斜杠

```text
# 正确方式
claude mcp add fs -- npx -y @modelcontextprotocol/server-filesystem C:/Users/username/Documents
```

**调试技巧**

```text
# 启用调试模式
claude --mcp-debug

# 查看日志文件
tail -f ~/Library/Logs/Claude/mcp*.log  # macOS
type "%APPDATA%\Claude\logs\mcp*.log"   # Windows

# 手动测试服务器
npx -y @modelcontextprotocol/server-filesystem ~/Documents
```

MCP 相关文档 
- https://zhuanlan.zhihu.com/p/1966486877088506681  --- 最重要 
- https://help.apiyi.com/claude-code-mcp-top-10-must-install.html
- https://blog.csdn.net/m0_74837192/article/details/150616899
- https://www.cnblogs.com/wind-xwj/p/19675511

视频中的  github , Sequential Thinking 任务分解 ， filesystem， context7， Brave search， perplexity search - AI 增强搜索， playwright 浏览器自动化(unity 不需要)  ，Linear 任务管理，  jira 企业任务管理， Sentry 错误监控

## 记忆系统详解

Claude Code的记忆系统让AI能够记住你的偏好和项目信息。

### 记忆文件类型

|      |                     |     |           |
| ---- | ------------------- | --- | --------- |
| 类型   | 位置                  | 作用域 | 用途        |
| 用户记忆 | ~/.claude/CLAUDE.md | 全局  | 个人偏好、编码风格 |
| 项目记忆 | 项目根目录/.CLAUDE.md    | 项目  | 项目特定信息    |


`/mcp` 查看mcp

常用MCP 插件
- context 7  有大量文档
- figma
- playwright
- sequential-thinking

**重要** ： 数据流转 ： 如：帮我梳理一下用户上级id的数据流转， 可以查看变量或者数据所在的层级以及场景 ， 很好用

