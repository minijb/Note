---
title: C# 集合接口
date: 2026-03-16
tags:
  - csharp
  - collection
  - interface
type: language
aliases:
  集合接口
description: C#常用集合接口IList、ICollection等
draft: false
---


## IList

表示可由索引单独访问的对象的非泛型集合。

[Doc](https://learn.microsoft.com/zh-cn/dotnet/api/system.collections.ilist?view=net-9.0)

常用方法：

- Add
- Clear
- Indexof
- Insert
- Remove
- RemoveAt


## IReadOnlyList

[doc](https://learn.microsoft.com/zh-cn/dotnet/api/system.collections.generic.ireadonlylist-1?view=net-9.0)


- GetEnumerator()  循环的访问集合的枚举器
- Count
- Item



## IDisposable

释放接口， 描述类需要释放一些东西  可以搭配 `using` 使用

作用
- 释放非托管接口
- 主动释放一些东西, 如内存，释放设备，句柄等
- 一些需要自动结束的类

**可以级联调用** : class 内部还有一个 实现了 IDisposable 的接口

**Dispose(bool) 方法重载**

在重载中，`disposing` 参数是一个 [Boolean](https://learn.microsoft.com/zh-cn/dotnet/api/system.boolean)，用于指示方法调用是来自 [Dispose](https://learn.microsoft.com/zh-cn/dotnet/api/system.idisposable.dispose) 方法（其值是 `true`），还是来自析构函数（其值是 `false`）。

```C#
protected virtual void Dispose(bool disposing)
{
    if (_disposed)
    {
        return;
    }

    if (disposing)
    {
        // Dispose managed state (managed objects).
        // ...
    }

    // Free unmanaged resources.
    // ...

    _disposed = true;
}



using System;
using System.IO;

public class DisposableBase : IDisposable
{
    // Detect redundant Dispose() calls.
    private bool _isDisposed;

    // Instantiate a disposable object owned by this class.
    private Stream? _managedResource = new MemoryStream();

    // Public implementation of Dispose pattern callable by consumers.
    public void Dispose()
    {
        Dispose(true);
        GC.SuppressFinalize(this);
    }

    // Protected implementation of Dispose pattern.
    protected virtual void Dispose(bool disposing)
    {
        if (!_isDisposed)
        {
            _isDisposed = true;

            if (disposing)
            {
                // Dispose managed state.
                _managedResource?.Dispose();
                _managedResource = null;
            }
        }
    }
}
```