---
title: JobSystem Job结构体
date: 2026-03-16
tags:
  - unity
  - dots
  - job-system
type: framework
aliases:
  Job结构
description: JobSystem Job结构体写法
draft: false
---


## 1. Job结构体

- 是一个模板，在内存中的长度是确定的，方便复制
- 需要继承接口 `IJob  IJobParallelFor IJobParallelForTransoform  JonFor`

## 2. 接口

#### 2.1 IJob

最基础的接口 job 接口

- 执行模式 ： 单任务模式
- 方法 `void Execute`
- 用途：
	- 执行一个独立的任务
	- 对 `NativeArray/NativeList` 进行整体的读写操作
	- 不适合大量重复的可变性化计算

```c#
public struct MyJob : IJob
{
    public NativeArray<float> InputA;
    public NativeArray<float> InputB;
    public NativeArray<float> Result; // 长度为1

    public void Execute()
    {
        Result[0] = 0;
        for (int i = 0; i < InputA.Length; i++)
        {
            Result[0] += InputA[i] * InputB[i];
        }
    }
}
```

#### 2.2 IJobParallelFor


这是最强大和最常用的并行接口，用于处理可以高度并行化的数据集（如数组、列表）

- 执行模式：数据并行。我们指定一个数量（`count`），`Execute(int index)` 方法会为每个索引（从 `0` 到 `count-1`）并行地执行一次。Unity 会自动将工作分割成多个批次，在多个核心上执行。
- 核心方法：`void Execute(int index)`
- 典型用途：

- 对 `NativeArray`、`NativeSlice` 中的每个元素进行独立的计算。
- 网格顶点处理、粒子系统更新、大批量数学计算等。

**限制**

- 我们必须确保在 `Execute` 方法内，通过 `index` 访问数据时是安全的，即不同 `index` 之间不能有写入竞争。
- 例如，`array[index] = ...` 是安全的，因为每个 `index` 是唯一的。但 `array[0] = ...` 是不安全的，因为所有并行任务都可能尝试写入 `index 0`。

```csharp
public struct AddJob : IJobParallelFor
{
    [ReadOnly] public NativeArray<float> InputA;
    [ReadOnly] public NativeArray<float> InputB;
    [WriteOnly] public NativeArray<float> Result;

    // index 由系统自动提供
    public void Execute(int index)
    {
        Result[index] = InputA[index] + InputB[index];
    }
}

// 调度方式：需要指定数量
var job = new AddJob { ... };
JobHandle handle = job.Schedule(Result.Length, 64); // 64 是每批处理的元素数量
```


```ad-note
title: batch大小如何设置

1. 数量多的小任务 ： batch 可以设置大一些
2. 数量少的大人物 ： batch 可以设置小一些
```


#### 2.3 IJobParallelForTransform

并行处理 大量 Transform 的组件

- 典型用途：高效地更新成千上万个物体的位置、旋转、缩放。它直接操作底层的 `TransformAccess` 结构，避免了从 `Component` 到 `Transform` 的昂贵开销和装箱操作。

**注意事项：**

- 我们需要使用 `TransformAccessArray` 而不是 `NativeArray<Transform>`。  **减少装箱拆箱操作**
- 性能远超在 `IJobParallelFor` 中手动处理 `Transform`。

```csharp
public struct MoveUpJob : IJobParallelForTransform
{
    public float DeltaTime;
    public float Speed;

    public void Execute(int index, TransformAccess transform)
    {
        transform.position += new float3(0, Speed * DeltaTime, 0);
    }
}

// 使用方式
TransformAccessArray transformArray = new TransformAccessArray(transforms);
var job = new MoveUpJob { DeltaTime = Time.deltaTime, Speed = 5f };
JobHandle handle = job.Schedule(transformArray);
```


#### 2.4 IJobFor  串行优化

- 执行模式：串行循环。它的 `Execute(int index)` 方法会在单个线程上按顺序（从 `0` 到 `count-1`）执行。它通常与 `ScheduleParallel` 和 `Run` 方法结合使用。
- 设计目的：主要用于与 Burst Compiler 优化结合。当我们使用 `job.ScheduleParallel(handle)` 时，Burst 可以将整个循环作为一个高效的、编译后的单元来优化，这可能比手写的 `for` 循环性能更高，即使是在单线程上。

```csharp
public struct CumulativeJob : IJobFor
{
    public NativeArray<float> Output;
    public void Execute(int i)
    {
        if (i > 0)
            Output[i] = Output[i-1] + 1; // 依赖前一个元素，必须串行
    }
}

// 调度方式
var job = new CumulativeJob { Output = outputArray };
JobHandle handle = job.Schedule(outputArray.Length, default(JobHandle));
```

#### 2.5 总结

| 接口                       | 执行模式 | 核心方法                                | 用途                  |
| ------------------------ | ---- | ----------------------------------- | ------------------- |
| IJob                     | 单任务  | Execute()                           | 单一独立任务，整体操作数据       |
| IJobParallelFor          | 数据并行 | Execute(int index)                  | 处理大型数组/列表，无数据竞争     |
| IJobParallelForTransform | 数据并行 | Execute(int index, TransformAccess) | 高效并行处理大量Transforms  |
| IJobFor                  | 串行循环 | Execute(int index)                  | 需要Burst优化但存在数据依赖的循环 |

- 只有一个任务要跑 -> `IJob`
- 要处理几万个完全独立的物体或数据点 -> `IJobParallelFor`
- 这几万个物体是 `GameObject` 的 `Transform` -> `IJobParallelForTransform`
- 循环必须按顺序执行，但又想获得Burst极致优化 -> `IJobFor` + `ScheduleParallel`