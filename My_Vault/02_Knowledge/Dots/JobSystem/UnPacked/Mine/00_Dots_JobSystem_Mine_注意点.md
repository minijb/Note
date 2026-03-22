---
title: JobSystem 注意点
date: 2026-03-16
tags:
  - unity
  - dots
  - job-system
type: framework
aliases:
  注意点
description: JobSystem使用注意点
draft: false
---


# Dots JobSystem Mine 注意点

1. Job 不应该访问静态数据
2. 使用 [JobHandle.ScheduleBatchedJobs](https://link.zhihu.com/?target=https%3A//docs.unity3d.com/ScriptReference/Unity.Jobs.JobHandle.ScheduleBatchedJobs.html) 方法立即执行已调度的 Job

Job 在被调度后会被缓存不会立即执行，该方法可立即清空缓存队列中的 Job 并执行，但会影响性能，或调用 [JobHandle.Complete](https://link.zhihu.com/?target=https%3A//docs.unity3d.com/ScriptReference/Unity.Jobs.JobHandle.Complete.html) 执行，ECS 系统已经隐式清空了缓存，以你无需主动调用

3. 不要更新 NativeContainer 内容

由于`ref returns`的缺陷，无法直接修改 NativeContainer 中的内容，需按如下方式

```csharp
MyStruct temp = myNativeArray[i];   
temp.memberVariable = 0;   
myNativeArray[i] = temp;
```


4. 只能在主线程调用 Schedule 和 Complete 方法
5. 使用 [ReadOnly] 标记 NativeContainer

Job 同时用于对 NativeContainer 的读写权限，使用 [ReadOnly] 标记只读 Job 中的 NativeContainer 可提升效率

6. Debugging jobs

可以调用`Run`方法取代`Schedule`在主线程执行 Job
7. 不要在 Job 中分配托管内存

在 Job 中分配托管内存会非常慢，且无法使用 Burst 编译提升效率

8. `[NativeSetThreadIndex]`  得到前thread的编号
9. `[NativeDisableContainerSafetyRestriction]` 不进行竞争检查， 
10. 其他的一些特性 [doc](https://docs.unity.cn/cn/2021.3/ScriptReference/Unity.Collections.LowLevel.Unsafe.NativeContainerAttribute.html)
11. JobWorkerMaximumCount  --- 设置最大 job 个数

https://heerozh.com/post/unity-job-xi-tong-ren-hua-jian-shu/


