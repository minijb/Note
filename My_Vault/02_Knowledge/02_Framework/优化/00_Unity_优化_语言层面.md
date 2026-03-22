---
title: Unity 优化 语言层面
date: 2026-03-16
tags:
  - unity
  - optimization
  - performance
type: framework
aliases:
  语言优化
description: Unity语言层面优化：Struct减少装箱、避免匿名函数等
draft: false
---


# Unity 优化 语言层面

1. 使用集合的时候需要提前设置大小
比如 List，Dictionary

2. 引用连续!=内存连续

```c#
class A
{
	public int a;
	public float b;
	public bool c;
}

A[] arrayA = xxxx;

class C
{
	private static C _instance;
	public static C instance
	{
		get xxx
	}
	
	public int[] a = xxx;
	public float[] b = xxx;
	public bool[] c= xxx;
}

C c = C.instance;
```

arrayA 只是引用连续
C存储的地方，内存是连续的可以更好的利用缓存



