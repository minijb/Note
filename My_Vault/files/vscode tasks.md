---
tags:
  - vscode
  - settings
---
# vscode custom task

task 模板

```json
{
  // See https://go.microsoft.com/fwlink/?LinkId=733558
  // for the documentation about the tasks.json format
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Run tests",
      "type": "shell",
      "command": "./scripts/test.sh",
      "windows": {
        "command": ".\\scripts\\test.cmd"
      },
      "group": "test",
      "presentation": {
        "reveal": "always",
        "panel": "new"
      }
    }
  ]
}
```

解释： 

- <span style="background:#fff88f">type</span> : shell / process -- shell 命令被解释为shell命令行， process 该命令被解释为要执行的进程。
- <span style="background:#fff88f">command</span> : 确切的命令
- windows : 任何Windows特定的属性。将在Windows操作系统上执行该命令时使用，而不是使用默认属性。
- <span style="background:#fff88f">group</span> : 定义task所属的组，注：任意被因为 test 的组会被 `run test task` 运行
- presentation : 定义如何在用户界面中处理任务输出。In this example, the Integrated Terminal showing the output is `always` revealed and a `new` terminal is created on every task run.
- <span style="background:#fff88f">options</span> : 覆盖默认的值 如 <span style="background:#40a9ff">cwd-当前工作目录</span> ，<span style="background:#40a9ff">env-环境变量</span>，<span style="background:#40a9ff">shell-默认shell</span>
- runOptions ： 定义何时以及如何运行一个task

> 自动补全 -- `ctrl+space`
> 完整文档 ： [docs](https://code.visualstudio.com/docs/editor/tasks-appendix)

## shell command

对于 shell 命令需要特别对待

### 默认支持方式 

#### 单一命令

注意：如果命令内部有引号只能使用 **单引号**

```json
{
  "label": "dir",
  "type": "shell",
  "command": "dir 'folder with spaces'"
}
```

单双引号 `dir 'folder with spaces'`

```json
{
  "label": "dir",
  "type": "shell",
  "command": "dir",
  "args": ["folder with spaces"]
}
```

自己控制 quote

```json
{
  "label": "dir",
  "type": "shell",
  "command": "dir",
  "args": [
    {
      "value": "folder with spaces",
      "quoting": "escape"
    }
  ]
}
```

支持的值: 

- strong : linux,macos: `'` , cmd : `"`
- weak : 都是 `"`

## compound task

使用 `dependsOn` 将任务组合

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Client Build",
      "command": "gulp",
      "args": ["build"],
      "options": {
        "cwd": "${workspaceFolder}/client"
      }
    },
    {
      "label": "Server Build",
      "command": "gulp",
      "args": ["build"],
      "options": {
        "cwd": "${workspaceFolder}/server"
      }
    },
    {
      "label": "Build",
      "dependsOn": ["Client Build", "Server Build"]
    }
  ]
}
```

如果使用了 `"dependsOrder": "sequence"` 那么任务就会按照顺序进行。

```json
{
  "label": "One",
  "type": "shell",
  "command": "echo Hello ",
  "dependsOrder": "sequence",
  "dependsOn": ["Two", "Three"]
}
```

> `Tasks: Open User Tasks` : 打开全局task 

## output and run behavior

[vscode-output](https://code.visualstudio.com/docs/editor/tasks#_output-behavior)
[vscode-input](https://code.visualstudio.com/docs/editor/tasks#_run-behavior)

## [Variable substitution](https://code.visualstudio.com/docs/editor/tasks#_variable-substitution)

默认变量替换 [vscode-docs](https://code.visualstudio.com/docs/editor/variables-reference)

注意： `command, args, options` 这三个属性的值可以使用变量替换

> [[vscode variable substitution]]

## 操作系统特定属性

```json
{
  "label": "Run Node",
  "type": "process",
  "windows": {
    "command": "C:\\Program Files\\nodejs\\node.exe"
  },
  "linux": {
    "command": "/usr/bin/node"
  }
}
```

- window : windows
- linux : linux
- macos : osx

## global task

[vscode-global task](https://code.visualstudio.com/docs/editor/tasks#_global-tasks)

## 部分案例 -- scss typescript

[vsocde - examples](https://code.visualstudio.com/docs/editor/tasks#_examples-of-tasks-in-action)

## problem matcher, multiline problem matacher

[vscode - problem matcher](https://code.visualstudio.com/docs/editor/tasks#_defining-a-problem-matcher)

## background/watching tasks

Some tools support running in the background while watching the file system for changes and then triggering an action when a file changes on disk.

- `tsc --watch`
- `npm dev`

[vscode](https://code.visualstudio.com/docs/editor/tasks#_background-watching-tasks)

## 创建问题

### 选择 terminal

```json
options.shell.executable
```

见文档

