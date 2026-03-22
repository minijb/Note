---
title: C# 匿名函数GC问题
date: 2026-03-16
tags:
  - csharp
  - gc
  - lambda
type: language
aliases:
  匿名函数GC
description: C#匿名函数造成的GC问题及解决方案
draft: false
---


# CSharp 匿名函数GC问题

1. 匿名函数引用外部变量，会形成闭包 --- 实现原理为生成一个 **匿名类来保存外部变量** ， 此时会在堆上进行内存分配

```c#


// cachedTexture --- dic
public void SwitchCharBust(in string texturePath, string partName, bool isFilter = false)
{
	if (partName == "ID") return;
	if (!isFilter)
		filterKey(ref partName);
	if (cachedTextures.TryGetValue(texturePath, out Texture tex)) //已经缓存的直接使用缓存
	{
		charBustComponent.SwitchPart(tex, partName);
	}
	else // 没有则使用 imageManager 进行加载
	{
		ImageManager.Inst.LoadImage(texturePath, ((path, resource) =>
		{
			charBustComponent.SwitchPart(resource.tex, partName);
			cachedTextures.Add(path, resource.tex);
		}));
	}

	isReset = false;
}
```


LoadImage --- 为异步方法

如果同时有两个 load 进行加载， 那么缓存会同时 add --- 报错！！！


- 使用 `[]`
- 应用了自己的缓存那么， 创建一个  loadList + loadedList + Update 这种方式

