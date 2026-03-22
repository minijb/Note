---
title: Unity 销毁方法区别
date: 2026-03-16
tags:
  - unity
  - destory
  - lifecycle
type: framework
aliases:
  销毁方法
description: Unity Destory、DestoryImmediate、DestoryObjectImmediate区别
draft: false
---


## 销毁物体相关函数

**Destroy** 将删除的物体放在缓存里，缓存满了，才会完全删除，**如果没有运行，就没有片缓存**
**DestoryImmediate**  立即销毁
`Undo.DestoryObjectImmediate` 销毁对象并**记录销毁操作**