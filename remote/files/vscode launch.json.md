---
tags:
  - vscode
  - settings
---
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "C/C++ Runner: Debug Session",
      "type": "cppdbg",
      "request": "launch",
      "args": [],
      "stopAtEntry": false,
      "externalConsole": true,
      "cwd": "d:/Project/leetcode",
      "program": "d:/Project/leetcode/build/Debug/outDebug",
      "MIMode": "gdb",
      "miDebuggerPath": "gdb",
      "setupCommands": [
        {
          "description": "Enable pretty-printing for gdb",
          "text": "-enable-pretty-printing",
          "ignoreFailures": true
        }
      ]
    }
  ]
}
```

必选属性

- <span style="background:#40a9ff">type</span> : type of debugger --- 每个debug扩展都有一个 type 名称
- <span style="background:#40a9ff">request</span> : 请求类型 -- `launch / attach`
- <span style="background:#40a9ff">name</span> : 自定义名称

可选属性

- presentation : `order, group,hidden` , 用于 debug 侧边栏的展示

```json
  "presentation": {
	"hidden": false,
	"group": "",
	"order": 1
  },
```

- <span style="background:#40a9ff">preLaunchTask</span> : 在 debug 之前执行一个 task， 名称为 task.json 中的任务
- <span style="background:#40a9ff">postDebugTask</span> : 在 debug 结束后执行一个 task
- <span style="background:#40a9ff">internalConsoleOptions</span> : debug 期间的 终端面板控制选项
- <span style="background:#40a9ff">debugServer</span> : **仅对debug扩展** : 此属性允许您连接到指定的端口，而不是启动调试适配器。
- <span style="background:#40a9ff">serverReadyAction</span> : if you want to open a URL in a web browser whenever the program under debugging outputs a specific message to the debug console or integrated terminal. For details see section [Automatically open a URI when debugging a server program](https://code.visualstudio.com/docs/editor/debugging#_automatically-open-a-uri-when-debugging-a-server-program) below.

**常见选项**

- `program` - executable or file to run when launching the debugger
- `args` - arguments passed to the program to debug
- `env` - environment variables (the value `null` can be used to "undefine" a variable)
- `envFile` - path to dotenv file with environment variables
- `cwd` - current working directory for finding dependencies and other files
- `port` - port when attaching to a running process
- `stopOnEntry` - break immediately when the program launches
- `console` - what kind of console to use, for example, `internalConsole`, `integratedTerminal`, or `externalTerminal`

## 变量替换

[[vscode variable substitution]]

## 不同平台指定配置

![[vscode tasks#操作系统特定属性]]

## 断点

**行内断点**

`shift - F9`

一些其他断点

函数断点，数据断点

## 重定向输入或输出

两种方法 : 使用 attach 方法信息调试 ，或者使用管道(如果支持的话)


```json
{
  "name": "launch program that reads a file from stdin",
  "type": "node",
  "request": "launch",
  "program": "program.js",
  "console": "integratedTerminal",
  "args": ["<", "in.txt"]
}
```

## [Multi-target debugging](https://code.visualstudio.com/docs/editor/debugging#_multitarget-debugging)

同时启动多个 debug 程序

### 组合 launch 配置

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "node",
      "request": "launch",
      "name": "Server",
      "program": "${workspaceFolder}/server.js"
    },
    {
      "type": "node",
      "request": "launch",
      "name": "Client",
      "program": "${workspaceFolder}/client.js"
    }
  ],
  "compounds": [
    {
      "name": "Server/Client",
      "configurations": ["Server", "Client"],
      "preLaunchTask": "${defaultBuildTask}",
      "stopAll": true
    }
  ]
}
```


### 自动打开URL -- need more use

```json
{
  "type": "node",
  "request": "launch",
  "name": "Launch Program",
  "program": "${workspaceFolder}/app.js",

  "serverReadyAction": {
    "pattern": "listening on port ([0-9]+)",
    "uriFormat": "http://localhost:%s",
    "action": "openExternally"
  }
}
```

pattern 定义了一个正则，用于捕获终端的输出

uriFormat属性描述如何将端口号转换为URI，The first `%s` is substituted by the first capture group of the matching pattern.

Alternatively, the `action` can be set to `debugWithEdge` or `debugWithChrome`. In this mode, a `webRoot` property can be added that is passed to the Chrome or Edge debug session.

### Triggering an Arbitrary Launch Config

In some cases, you may need to configure additional options for the browser debug session--or use a different debugger entirely. You can do this by setting `action` to `startDebugging` with a `name` property set to the name of the launch configuration to start when the `pattern` is matched.


The named launch configuration must be in the same file or folder as the one with the `serverReadyAction`.