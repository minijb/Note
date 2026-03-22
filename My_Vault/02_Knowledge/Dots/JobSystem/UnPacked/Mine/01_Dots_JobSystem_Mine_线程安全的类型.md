---
title: JobSystem 线程安全类型
date: 2026-03-16
tags:
  - unity
  - dots
  - job-system
  - thread
type: framework
aliases:
  线程安全
description: JobSystem线程安全类型
draft: false
---


## 内存分配器

创建`NativeContainer`实例时，必须指定所需的内存分配类型。使用的分配类型取决于您希望原生容器保持可用的时长。这样，您就可以根据具体情况定制分配方案，以获得最佳性能。

内存分配和释放有三种[Allocator](https://docs.unity.cn/2023.1/Documentation/ScriptReference/Unity.Collections.Allocator.html)类型`NativeContainer`。实例化实例时必须指定合适的一种`NativeContainer`：

- `Allocator.Temp`：最快的分配方式。适用于生命周期不超过一帧的分配。您不能使用它`Temp`来将分配传递给`NativeContainer`存储在作业成员字段中的实例。
- `Allocator.TempJob`：比 慢`Temp`但比 快的分配方式`Persistent`。使用它来进行四帧生命周期内的线程安全分配。**重要提示**：您必须`Dispose`在四帧内完成此分配类型，否则控制台会打印由本机代码生成的警告。大多数小型作业都使用此分配类型。
- `Allocator.Persistent`：速度最慢的分配方式，但可以根据需要持续很长时间，必要时甚至贯穿整个应用程序的生命周期。它是对 的直接调用的包装器[`malloc`](http://www.cplusplus.com/reference/cstdlib/malloc/)。较长的作业可以使用此 NativeContainer 分配类型。请勿`Persistent`在性能至关重要的情况下使用。

## 安全系统

1. 由于并行运行， 两个独立的调度会同时写入一个 NativeArray ， 这是不安全的。 推荐使用**依赖关系**来安排两个作业。

2. NativeXXX 本质是一个指针 ， 使用 `ref return` 返回结果。 如果需要更改数据，需要先进行复制。修改后保存回去

```c#
MyStruct temp = myNativeArray[i];
temp.memberVariable = 0;
myNativeArray[i] = temp;
```

## 复制 NativeContainer 结构

由于是值类型，每次赋值都是一次复制。其他结构体包含一个指针指向具体数据内容。



### 可动态扩容的容器

如 `NativeList<T>` 大小并不固定。 通过 view 视口来获取内容。**可以设置别名，而无需复制或获取数据所有权！！！** 视图的示例包括枚举器对象（您可以使用它逐个元素地访问原生容器中的数据）以及诸如 之类的方法（[`NativeList<T>.AsArray`](https://docs.unity.cn/Packages/com.unity.collections@latest/index.html?subfolder=/api/Unity.Collections.NativeList-1.html#Unity_Collections_NativeList_1_AsArray)您可以使用`NativeList`它将 视为 ）`NativeArray`。

如果动态原生容器的大小发生变化，视图通常不是线程安全的。这是因为当原生容器的大小发生变化时，Unity 会重新定位数据在内存中的存储位置，这会导致视图存储的所有指针失效。


### 自定义NativeContainer 

https://docs.unity.cn/2023.1/Documentation/Manual/job-system-custom-nativecontainer-example.html