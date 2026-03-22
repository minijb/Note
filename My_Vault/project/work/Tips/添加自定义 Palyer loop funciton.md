---
title: 添加自定义 Palyer loop funciton
date: 2026-03-16
tags:
  - untagged
type: knowledge
aliases:
  -
description: https://docs.unity.cn/cn/2021.1/ScriptReference/LowLevel.PlayerLoop.html
draft: false
---

# 添加自定义 Palyer loop funciton

https://docs.unity.cn/cn/2021.1/ScriptReference/LowLevel.PlayerLoop.html

注意 `PlayerLoop` 是值类型，因此get之后还需要set

`getCurrentxxx` 得到当前的
`getDefaultxx`  得到默认的
`setxxx` 设置 playerLoop

有两个主要属性 type ， subSystemList

有三级层次 --- 通过 subSystemList 进入下一级 

1. PlayerLoop   总的循环 --- 没有 type
2. 主要生命周期  ---- type 对应的生命周期  类型 `UnityEngine.PlayerLoop`
3. 每个生命周期执行的方法 --- type 可自定义方法 

