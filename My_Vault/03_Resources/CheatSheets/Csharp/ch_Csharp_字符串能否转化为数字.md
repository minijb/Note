---
title: ch Csharp 字符串能否转化为数字
date: 2026-03-16
tags:
  - resource
  - csharp
type: language
aliases:
  -
description: 使用 Linq 进行快速遍历
draft: false
---

# ch Csharp 字符串能否转化为数字

**方法1 :**

使用 Linq 进行快速遍历

```c#
if(number.All(char.IsDigit))
```

**方法2 :**

使用 tryParse

```c#
bool t = Int32.TryParse(number, out n);
```


