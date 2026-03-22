---
title: Unity 安卓交互 出现的一些问题
date: 2026-03-16
tags:
  - knowledge
  - unity
type: knowledge
aliases:
  -
description: porject setting / other setting / target api level 中不实用 hightest level api 而是降低一些。
draft: false
---

# Unity 安卓交互 出现的一些问题

## 1. build 过程中，出现 gradle 版本不对的问题

porject setting / other setting / target api level 中不实用 hightest level api 而是降低一些。

## 2. 使用 AndroidJavaClass/AndroidJavaObject 这种类型

必须在 Start 中进行初始化， 默认的 new 无法获取Java Object

