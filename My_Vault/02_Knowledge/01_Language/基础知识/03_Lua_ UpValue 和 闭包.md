---
title: Lua UpValue 和闭包
date: 2026-03-16
tags:
  - lua
  - closure
  - upvalue
type: language
aliases:
  UpValue
  - 闭包
description: Lua UpValue和闭包概念
draft: false
---


### 1. 共享

多个闭包引用一个外部局部变量，实际为共享同一个 UpValue

### 2. 关闭和开启

一个闭包被创建的时候开启，没有任何必报引用的时候关闭--资源回收。 

### 3. 存储

lua 会正常一个全局栈，  所有upvalue 会指向该栈中的值。如果对应的参数离开作用域，栈中的值也会被释放。