---
title: Window Powershell 升级
date: 2026-03-16
tags:
  - archive
type: knowledge
aliases:
  -
description: **查看是否有新版本**
draft: false
---

# Window Powershell 升级

**查看是否有新版本**

```sh
# 查看当前坂本
$PSVersionTable.PSVersion
# 查看网络上的坂本
winget search Microsoft.PowerShell
```


**安装新版本**

```sh
# 使用 Winget 安装 PowerShell
winget install --id Microsoft.Powershell --source winget
 
# 使用 Winget 安装 PowerShell 预览版
winget install --id Microsoft.Powershell.Preview --source winget
```

**手动安装**

https://learn.microsoft.com/zh-cn/powershell/scripting/install/installing-powershell-on-windows?view=powershell-7.5#msi

**设置终端**

在终端 中的 启动 + 默认配置文件