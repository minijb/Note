---
title: Now 当前任务
date: 2026-03-16
tags:
  - inbox
  - todo
  - unity
  - editor
type: inbox
aliases:
  - 当前任务
  - Now任务
description: 记录当前待办事项：编辑器扩展开发、EventDispatcher事件分发器实现
draft: false
---

# Now 当前任务


use skill-creator， 我希望创建一个 编写lua时使用emmylua 格式的skill， 请参考
  https://github.com/EmmyLuaLs/emmylua-analyzer-rust，  https://github.com/EmmyLuaLs/emmylua-analyzer-rust/blob/main/d
  ocs/emmylua_doc/annotations_CN/README.md，以及之前写过的lua格式： @Client\Assets\Script\Lua\ 。

  同时 需要一些注意点：
  1. 可以将格式分为：原生格式，项目格式风格。
  2. 创建一个 example 文件夹， 内部存放对应的例子， SKILL中的例子可以少一点，但是需要链接到对应的example文件。
  3. 添加一个提示语句，仅当使用到对应的格式时才加载对应的例子，以减少 token的使用
