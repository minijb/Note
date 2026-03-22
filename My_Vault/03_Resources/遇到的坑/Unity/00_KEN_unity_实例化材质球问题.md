---
title: KEN unity 实例化材质球问题
date: 2026-03-16
tags:
  - resource
  - unity
type: knowledge
aliases:
  -
description: https://zhuanlan.zhihu.com/p/22179381
draft: false
---

# KEN unity 实例化材质球问题

https://zhuanlan.zhihu.com/p/22179381
https://blog.csdn.net/thinbug/article/details/103871464
https://keenster.cn/2021/03/25/UnityMemoryLeak-Texture2D/
https://zhuanlan.zhihu.com/p/657727633


`new Material()`  之后需要释放

1. 直接使用 `Destroy`
2. 使用 `Resources.UnloadUnusedAssets();`
3. 使用 `MaterialPropertyBlock` 替换Material属性操作

**注意：这里只能通过**

```c#

```