---
tags:
  - Csharp
---
https://learn.microsoft.com/zh-cn/dotnet/standard/garbage-collection/weak-references

如果不存在强引用，则弱引用的有限期只限于收集对象前的一个不确定的时间段。 使用弱引用时，应用程序仍可对该对象进行强引用，这样做可防止该对象被收集.

使用 `IsAlive` 来确定弱引用是否存在