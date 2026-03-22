---
title: JobSystem 内存分配
date: 2026-03-16
tags:
  - unity
  - dots
  - job-system
  - memory
type: framework
aliases:
  内存
description: JobSystem内存分配
draft: false
---


## 1 分配内存

`var data = new NativeArray<float>(1000, Allocator.TempJob);`  
为我们需要参与计算的数据划分一块内存，需要使用正确的Allocator（分配器）。  
Unity 主要提供了三种我们需要关心的 `Allocator`，它们都在 `Unity.Collections` 命名空间下：

1. `Allocator.Temp` (临时分配器)。仅在当前帧的、调用它的函数范围内有效。**绝对不能在主线程分配给 Job 使用**， 如果在 Job 中他的生命周期和 job 相同
2. `Allocator.TempJob` (临时任务分配器)Job最常用分配器。必须在主线程显式调用 `Dispose`。 一般4帧左右，如果没有释放会警告
3. `Allocator.Persistent` (持久化分配器)分配的内存会一直存在，直到你显式调用 `.Dispose()`。
4. (`Allocator.None` 用于特殊场景，通常不主动使用)


**总结**

- 默认选择 `TempJob`：凡是需要给 Job 传递数据的，无脑先选 `Allocator.TempJob`。
- 牢记 `Dispose`：对于 `TempJob` 和 `Persistent`，必须有清晰的分配和释放配对逻辑。通常使用 `using` 块或在 `MonoBehaviour` 的 `OnDestroy` 或自定义的 `Dispose` 方法中释放。
- `Temp` 仅用于主线程瞬时操作：把它想象成 `stackalloc`，绝不跨帧、绝不给Job。
- 慎用 `Persistent`：把它当作最后的手段，而不是首选。问问自己：“这个数据真的需要存活那么久吗？用 `TempJob` 每帧分配一次是否可行？”
- 依赖检查器：在 Unity Editor 中开启 Jobs > Safety Check 选项，它可以帮助你捕获许多分配和访问错误（如忘记 Dispose、竞态条件等）。

| 特性           | Allocator.Temp | Allocator.TempJob    | Allocator.Persistent |
| ------------ | -------------- | -------------------- | -------------------- |
| 生命周期         | 极短（当前函数/帧）     | 较短（至少4帧或Job完成后）      | 永久（直到手动释放）           |
| 性能           | 最快             | 快                    | 最慢                   |
| 线程安全         | 仅主线程           | 可用于Job（多线程）          | 可用于Job（多线程）          |
| 需要手动 Dispose | 是              | 是                    | 是                    |
| 主要使用场景       | 同一函数块内的临时计算    | JobSystem 数据传递（默认选择） | 跨场景/模式的长期缓存          |
| 内存泄漏风险       | 低（但错误使用会导致崩溃）  | 中（忘记Dispose会报错）      | 极高（忘记就真泄漏了）          |
| 错误使用后果       | 崩溃（Job中使用）     | 内存泄漏报错               | 严重内存泄漏               |


```ad-tip
title: TransformAccessArray

每帧new TransformAccessArray是一个非常消耗性能的事情，特别是长度高的时候。  1ms 左右 new 一次
最佳实践是写一个EntityMoveSystem，持有一个私有字段，创建一个固定长度的数组，**动态扩容**。
```
