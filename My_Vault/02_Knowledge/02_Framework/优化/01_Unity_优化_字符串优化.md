---
title: Unity 优化 字符串优化
date: 2026-03-16
tags:
  - unity
  - optimization
  - string
type: framework
aliases:
  字符串优化
description: Unity字符串String优化技巧
draft: false
---


## 字符串优化

- Csharp 对字符串没有任何优化。推荐自己缓存 比如使用 Dictonary。用的时候先查询
- 使用 native --- 非安全的方式。使用类似 C++的方式来处理身体乳那个类。

```c#
string strA = "aaa";
string strB = "bbb" + "b";

fixed(char* strA_ptr = strA)
{
	fixed(char* strB_ptr = strB)
	{
		memcopy((byte*)strB_ptr, (byte*)strA_ptr, 3*sizeof(char));
	}
}

strB; // "aaab"
```

> `fixed` 关键字用于防止垃圾回收器移动内存中的一个或多个对象。它通常与非安全代码（即包含指针操作的代码）一起使用，允许开发者对内存进行更底层的操作。

## 将两种方式混合起来使用

```c#
Dictionary<int, string> cacheStr;

public unsafe string Concat(string strA, string strB)
{
	int a_length = a.Length;
	int b_length = b.Length;
	
	int sum_length = a_Length + b_length;
	string result = null;
	
	if(!cacheStr.TryGetValue(sum_length, out strResult))
	{
		strResult = strA + strB;
		cacheStr.Add(sum_length, strResult);
		return strResult;
	}
	
	fixed(char* strA_ptr = strA)
	{
		fixed(char* strB_ptr = strB)
		{
			fixed(char* strResult_ptr = strResult)
			{
				memcopy((byte*)strResult_ptr, (byte*)strA_ptr, a_length * sizeof(char));
				memcopy((byte*)strResult_ptr + a_length, (byte*)strB_ptr, b_length * sizeof(char));
			}
		}
	}
	return strResult_ptr;
}
```


```c#
public unsafe void memcopy(byte* dest, byte* src, int len)
{
	while((--len) >= 0)
	{
		dest[len] = src[len];
	}
}
```