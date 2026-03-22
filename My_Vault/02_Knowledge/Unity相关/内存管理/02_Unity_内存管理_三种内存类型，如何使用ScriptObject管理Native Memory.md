---
title: Unity 内存管理 三种内存类型，如何使用ScriptObject管理Native Memory
date: 2026-03-16
tags:
  - knowledge
  - unity
type: knowledge
aliases:
  -
description: 1. Managed Memory -- C# Object + Value type (int, float ,struct)
draft: false
---

# Unity 内存管理 三种内存类型，如何使用ScriptObject管理Native Memory

## 1. 三种内存类型

1. Managed Memory -- C# Object + Value type (int, float ,struct)
	- 第一种是会被C# GC的
	- 第二种是会被自动释放的
2. Native Memory 
	- Unity 管理的 (C++)
	- 包含 ： Asset + Resource： Texture Mesh ....
	- Engine SubSystem ：  Renderer， Physics
3. UnManaged Menory ： 需要手动释放的内存， 不会被GC
	- `NativeArray, NativeList`

## 2. ScriptObject

如果在ScriptObjec 中存储一些资源如  ： 
- Texture ， mesh ， 以及**自身**  --- Native Memory 会使用指针 ： **`m_CachedPtr`** 链接到 C++ 管理的 Native 层
- 基础类型如 int float 会在托管堆上


**Pollution（污染）：直接引用同一个实例，所有修改都会污染原始资源**

- 直接  tempSO = originSO
- 直接修改原资源

**Shallow Clone（浅拷贝）：SO 对象被复制，但资源依然共享**

- `tempSO = Instantiate(originSO)`
- So的Instance ID 不一样, 但是 内部的资源 Instance ID 是一样的
- 修改 tempSO 的资源也会被复制到 Native 层

**Deep Clone（深拷贝）：SO 和资源都被完全复制，互不影响**

```c#
tempSO = Instantiate(originSO)
tempSO.tex = Instantiate(originSO.tex)
```

- tempSO 不会修改 originSO的资源，同时也不会修改本机资源
- 资源+自身的 Instance ID 不一样。
