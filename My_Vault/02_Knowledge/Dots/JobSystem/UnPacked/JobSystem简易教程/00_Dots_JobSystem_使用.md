---
title: JobSystem 使用
date: 2026-03-16
tags:
  - unity
  - dots
  - job-system
type: framework
aliases:
  JobSystem使用
description: Unity JobSystem使用方法
draft: false
---


## 1. 如何使用

### 1.1 限制1 ： 必须继承接口

#### 1.1 创建Job结构体

相当于建立一个模板， 只有在调用知心的时候才会被实例化。 定义了 **那些输入输出数据及执行方法**


需要集成接口 `IJob  IJobParallelFor IJobParallelForTransoform  JonFor` ,  都来自命名空间 `Unity.Jobs.IJob`  



#### 1.2 IJob


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


#### 1.3 IJobParallelFor

这是最强大和最常用的并行接口，用于处理可以高度并行化的数据集（如数组、列表）

- 执行模式：数据并行。我们指定一个数量（`count`），`Execute(int index)` 方法会为每个索引（从 `0` 到 `count-1`）并行地执行一次。Unity 会自动将工作分割成多个批次，在多个核心上执行。
- 核心方法：`void Execute(int index)`
- 典型用途：

- 对 `NativeArray`、`NativeSlice` 中的每个元素进行独立的计算。
- 网格顶点处理、粒子系统更新、大批量数学计算等。

- 关键限制：

- 我们必须确保在 `Execute` 方法内，通过 `index` 访问数据时是安全的，即不同 `index` 之间不能有写入竞争。
- 例如，`array[index] = ...` 是安全的，因为每个 `index` 是唯一的。但 `array[0] = ...` 是不安全的，因为所有并行任务都可能尝试写入 `index 0`。

> 简单的例子 ： 这里如果将 `array[1-99]`的 和放入 `array[0]` 中 这个就会出现数据竞争 ！！！！  --- 也就是说 在处理 index 的时候， 不能使用 i != index 的 数据

- 示例：并行计算两个数组的对应元素之和。

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



#### 1.4 IJobParallelForTransform

并行处理 大量 Transform 的组件

- 执行模式：与 `IJobParallelFor` 相同，是数据并行的。
- 核心方法：`void Execute(int index, TransformAccess transform)`
- 典型用途：高效地更新成千上万个物体的位置、旋转、缩放。它直接操作底层的 `TransformAccess` 结构，避免了从 `Component` 到 `Transform` 的昂贵开销和装箱操作。
- 注意事项：

- 我们需要使用 `TransformAccessArray` 而不是 `NativeArray<Transform>`。  **减少装箱拆箱操作**
- 性能远超在 `IJobParallelFor` 中手动处理 `Transform`。

- 示例：让一堆物体并行地向上移动。

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


#### 1.4 IJobFor  串行优化

这个接口的行为与 `IJobParallelFor` 完全不同，它不是并行的。

- 执行模式：串行循环。它的 `Execute(int index)` 方法会在单个线程上按顺序（从 `0` 到 `count-1`）执行。它通常与 `ScheduleParallel` 和 `Run` 方法结合使用。
- 核心方法：`void Execute(int index)`
- 设计目的：主要用于与 Burst Compiler 优化结合。当我们使用 `job.ScheduleParallel(handle)` 时，Burst 可以将整个循环作为一个高效的、编译后的单元来优化，这可能比手写的 `for` 循环性能更高，即使是在单线程上。
- 典型用途：需要 Burst 优化但循环迭代间存在数据依赖，无法并行化的计算。
- 示例：**一个累积计算，每次迭代依赖于前一次的结果**（这种场景无法用 `IJobParallelFor`）。

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

#### 1.5 总结

| 接口                       | 执行模式 | 核心方法                                | 用途                  | 关键点                                          |
| ------------------------ | ---- | ----------------------------------- | ------------------- | -------------------------------------------- |
| IJob                     | 单任务  | Execute()                           | 单一独立任务，整体操作数据       | 最简单，一次执行                                     |
| IJobParallelFor          | 数据并行 | Execute(int index)                  | 处理大型数组/列表，无数据竞争     | 最常用，高性能，需注意线程安全                              |
| IJobParallelForTransform | 数据并行 | Execute(int index, TransformAccess) | 高效并行处理大量Transforms  | IJobParallelFor 的特化版，需用 TransformAccessArray |
| IJobFor                  | 串行循环 | Execute(int index)                  | 需要Burst优化但存在数据依赖的循环 | 不是并行的，用于Burst优化单线程循环                         |

- 只有一个任务要跑 -> `IJob`
- 要处理几万个完全独立的物体或数据点 -> `IJobParallelFor`
- 这几万个物体是 `GameObject` 的 `Transform` -> `IJobParallelForTransform`
- 循环必须按顺序执行，但又想获得Burst极致优化 -> `IJobFor` + `ScheduleParallel`

### 2.1 必须使用非托管集合


字段必须是 Blittable 类型

![image.png](https://s2.loli.net/2025/10/15/eQTlvDgJc51KFRP.png)

字段必须是Blittable类型，或者是只包含Blittable类型的struct。Blittable类型意味着在托管和原生代码中,内存的表现是一致的。这是一个硬性规定，违反它会导致编译错误或运行时异常。

常见定义字段的方式

```csharp
 [ReadOnly] public NativeArray<float> Input;
 [ReadOnly] public float Ratio;
 public NativeArray<MyEntityStruct> InputOutput;
```


- 数据集合的**容器**推荐使用Unity提供的**NativeArray, NativeList, NativeQueue, NativeHashMap**等等。<font color="#ffc000">直接使用List 会编译报错</font>
- 可以直接不用数据容器定义Blittable类型的字段。
- 可以加上标签提高性能。 [ReadOnly] [WriteOnly]。
- 可以使用**自定义的结构体。但是需要满足，结构体里只能包含Blittable类型**，或**嵌套其他非托管结构体**。嵌套结构体也必须是非托管的。结构体**也不能包含Native容器的字段（可以理解成结构体的<font color="#00b050">长度需要是确定</font>的）**。
- 常用类型中Vector3并不满足Bilttable，可以使用**Unity.Mathematics的float3**替代。旋转参数推荐使用**quaternion。`math.mul()`、`math.rotate()` 等函数代替 `Vector3` 操作。**
- **使用结构数组的设计模式（SoA）是最佳实践**
- 在 Unity.Mathematics **中提供了 `bool4`、`char` 等替代类型**，它们是 Blittable 的。
- 如果一定要用 **`bool`，可以使用 `byte` 或 `int` 代替**。

> 使用 `[StructLayout(LayoutKind.Sequential, Pack = 4)]` 实现结构内部的字节对齐

```ad-note
title: **JobSystem为什么会限制只能使用Blittable类型？**

根本原因在于 JobSystem的工作方式和 内存安全。

1. 跨线程内存访问：JobSystem的目的是在多线程（通常是工作线程）上安全地执行任务。这意味着Job结构体的数据需要被完整地拷贝到另一个线程的内存上下文中去执行。
2. 无封送处理（No Marshaling）：与非托管代码交互（P/Invoke）时，.NET运行时可以进行“封送处理”（Marshaling）来转换非Blittable类型（如`string`）。但JobSystem在跨线程传递数据时，没有这种复杂的封送处理机制。它依赖的是最原始、最快的内存块拷贝（memcpy）。
3. Blittable类型保证内存布局一致：只有Blittable类型在内存中的二进制表示是明确、固定且连续的。这使得Unity引擎可以简单地将整个Job结构体对应的内存块直接复制到工作线程，工作线程也能用完全相同的布局来解读这块内存，从而安全地访问每一个字段。
4. 非Blittable类型的危险：如果一个Job包含了非Blittable类型（如`string`），会发生什么？  
    

5. `string`是引用类型。它的实例存储在托管堆上，而字段本身只是一个指向堆内存的指针（引用）。
6. 当我们将Job调度到工作线程时，Unity会拷贝这个结构体，也就是拷贝了这个指针值，但不会拷贝指针所指向的堆上的字符串数据。
7. 工作线程现在拿到了一个指向主线程托管堆内存的指针。一旦工作线程尝试通过这个指针去访问字符串，就会导致竞态条件（Race Condition），因为主线程可能同时在操作或甚至垃圾回收器（GC）已经移动/释放了那块内存。这会导致无法预测的行为、数据损坏或程序崩溃。

为了彻底杜绝这种危险，Unity在编译期（Burst编译）和调度期（`Job.Schedule`）都会进行严格的检查。
```


```ad-note
title: 类型之间的关系
它们的关系是一个逐渐缩小的子集关系：  
值类型 (Value Types) ⊃ 非托管类型 (Unmanaged Types) ⊃ Blittable 类型 (Blittable Types)

**值类型 (Value Types)**

这是最广的范畴。

- 定义：值类型是其实例直接包含其数据的类型。它们通常分配在栈上（但也可以是类的字段而被间接分配在堆上）。
- 包括：

- 所有数值类型（`int`, `float`, `double`, `long`, `byte` 等）
- `char`
- `bool`
- `enum`
- `struct`（但有条件，见下文）

- 特点：赋值操作会进行完整的拷贝。
- 关系中的位置：这是所有后续类型的基础。非托管类型和 Blittable 类型首先必须是值类型

**非托管类型 (Unmanaged Types)**

这是值类型的一个子集，是 C# 7.3 引入的一个正式概念，主要用于 `unsafe` 上下文和与非托管代码的交互。

- 定义：一种类型，如果它满足以下所有条件，则它是非托管类型：

- 它必须是值类型（引用类型永远不是非托管的）。
- 它不包含任何引用类型的字段。
- 它的所有字段递归地也都是非托管类型。

关系中的位置：非托管类型是值类型的子集。它排除了那些包含引用类型的值类型（如某些 `struct`）。

**Blittable 类型 (Blittable Types)**

这是非托管类型中一个更严格的子集，是与非托管代码互操作（P/Invoke）时最关键的概念。

- 定义：一种数据类型，它在托管内存和非托管内存中具有相同的二进制表示形式（相同的内存布局和位模式）。因此，在互操作时，运行时可以直接进行“位拷贝”（blit）来传递数据，而无需进行任何特殊的转换或封送处理（Marshaling）。
- 包括：

- 大多数基础数值类型：`byte`, `sbyte`, `short`, `ushort`, `int`, `uint`, `long`, `ulong`, `single`, `double`。
- 包含“非嵌套”的 Blittable 类型的数组（如 `int[]`）。
- 只包含 Blittable 类型字段的 `struct`，并且其布局是连续的（通常是 `[StructLayout(LayoutKind.Sequential)]` 或默认顺序）。

- 不包括（重要的非 Blittable 类型）：

- `bool`： 在C#中占1字节，但在非托管代码中可能是4字节（如Win32 BOOL）。需要封送处理。
- `char`： 在C#中是2字节Unicode，在非托管代码中可能是1字节ANSI。需要封送处理。
- `string`： 引用类型，且编码不同，必须封送。
- 包含 `bool` 或 `char` 字段的 `struct`：因为这些字段不是 Blittable 的，所以整个结构体也不是 Blittable 的。

```


````ad-note
title: 什么是结构数组（SoA）
结构数组指的是为每种数据创建平行的、等长的 `NativeArray`。这是 [Data-Oriented Design](https://zhida.zhihu.com/search?content_id=262348453&content_type=Article&match_order=1&q=Data-Oriented+Design&zhida_source=entity)（面向数据设计）的核心。

- **错误设计 (❌ AoS - Array of Structures)：内存布局分散，难以管理_。_**

```csharp
public struct BadEntityStruct
{
    public int Health;
    public NativeArray<Vector3> PathPoints; // ❌ 非常糟糕
}
public NativeArray<BadEntityStruct> BadEntities;
```

JobSystem 和 Burst 的性能优势来自于连续内存块的线性遍历。  
如果每个结构体内部都有一个独立的 `NativeArray`，数据会被分散在内存的各个角落，导致大量的缓存未命中，性能会急剧下降。

- **正确设计 (✅ SoA - Structure of Arrays)：内存布局连续，易于批量处理，缓存友好。**

```csharp
public NativeArray<int> EntityHealths; 
public NativeArray<Vector3> EntityPositions; 
NativeArray<NativeList<Vector3>> EntityPaths; 
```

- **如果需要包含动态数量的数据，正确的做法是：**
- 使用平行的数组或列表：

```csharp
public NativeArray<MyEntityStruct> Entities; // 核心数据
public NativeArray<NativeList<Vector3>> EntityPathLists; // 每个实体的路径点列表
// 确保Entities和EntityPathLists长度一致，索引对应同一个实体
```

- 使用一个大的扁平化数组 + 偏移量：

```csharp
public NativeArray<Vector3> AllPathPoints; // 所有实体的所有路径点都塞进这里
public NativeArray<int> EntityPathStartIndex; // 每个实体的路径点在AllPathPoints中的起始索引
public NativeArray<int> EntityPathLength; // 每个实体的路径点数量 
```
````


```ad-note
title: NativeArray<T> 是值类型吗？

NativeArray<T> 是一个结构体（struct），因此它属于值类型。  
这是一个非常重要的特性，也是它能在 JobSystem 中安全使用的关键原因之一。但是，它的行为与简单的值类型（如 `int`、`float`）有本质区别，理解这一点至关重要。

**为什么 `NativeArray<T>` 是值类型，却又如此特殊？**

简单来说：`NativeArray<T>` 是一个包装器或智能指针。它的结构体内部并不直接存储数据数组，而是包含了一个指向Unity内存管理系统（Allocator）中分配的非托管内存块的指针和一些管理元数据（如长度、版本号等）。  

**这种设计带来的行为特性：**

1.值类型的拷贝语义：

1. 当我们将一个 `NativeArray` 变量赋值给另一个变量，或者作为参数传递给方法时，发生的是值类型的拷贝。这意味着 `m_Buffer`、`m_Length` 等内部字段的值被复制了一份。
2. 关键点：复制的是指针（`m_Buffer`），而不是指针所指向的数据。因此，两个 `NativeArray` 变量（`arrayA` 和 `arrayB`）将指向同一块非托管内存数据。

2.“浅拷贝”而非“深拷贝”：

1. 对 `arrayA[0]` 进行修改，会直接反映在 `arrayB[0]` 上，因为它们操作的是同一片内存。
2. 这种行为类似于引用类型，但其本质是值类型（结构体）包含了一个指针。

**为什么Unity要这样设计？**

1. 性能：避免在Job之间传递数据时进行昂贵的内存拷贝。Job可以高效地读写同一块内存，从而实现线程间通信。
2. 与JobSystem协同工作：作为值类型，`NativeArray` 可以完美地嵌入到 `IJob` 结构体中，满足Job参数必须是Blittable类型的要求。因为它只包含指针和整数等原始类型，整个结构体的内存布局是固定的和明确的。
3. 内存安全：虽然数据是共享的，但Unity的安全系统（通过 `AtomicSafetyHandle`）会跟踪`NativeArray`的生命周期和访问权限。例如，它会在我们尝试在Schedule的Job仍在执行时`Dispose()`数组，或者在一个写入权限不匹配的Job中写入数据时抛出异常，从而防止内存损坏和数据竞争。
   
**总结**

1. `NativeArray<T>` 是一个值类型的struct。
2. 它进行的是浅拷贝，只复制内部的指针和元数据，多个变量共享同一份底层数据。
3. 它的内存布局只包含原生类型（如指针、int），可以被安全地直接拷贝到工作线程。
4. 必须管理它的生命周期。因为它管理着非托管内存，必须在使用完毕后调用 Dispose() 方法来释放内存，否则会导致内存泄漏。
5. 多个 NativeArray 变量可能指向同一块内存，修改一个会影响另一个。这可能导致难以察觉的 Bug，尤其是在多个 Job 中共享数据时。

   
```



https://docs.unity3d.com/Packages/com.unity.mathematics@1.3/api/Unity.Mathematics.math.html --- Burst.Math



### 3. 例子

```csharp
// 简单任务：为数组中的每个元素加一
public struct AddOneJob : IJob
{
    public NativeArray<float> InputOutput;
    
    public void Execute()
    {
        for (int i = 0; i < InputOutput.Length; i++)
        {
            InputOutput[i] = InputOutput[i] + 1;
        }
    }
}
```


想要它真正执行，还需要以下几个步骤。

```csharp
void Start()
{
    var data = new NativeArray<float>(1000, Allocator.TempJob);
    for (int i = 0; i < data.Length; i++)
        data[i] = i;
    var job = new AddOneJob { InputOutput = data };
    JobHandle handle = job.Schedule();
    DoOtherWork();
    handle.Complete();
    Debug.Log($"Result: {data[0]}");
    data.Dispose();
}
```


## 4. 基本流程


#### 4.1 分配内存

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

#### 4.2 初始化数据

为上一步分配的内存，填充工作数据。

```csharp
for (int i = 0; i < data.Length; i++)
        data[i] = i;
```

#### 4.3 创建并设置 Job

实例化Job结构体出来，并且将之前分配好的数据赋值给Job的字段。

```csharp
var job = new AddOneJob { InputOutput = data };
```

#### 4.4 调度Job

**简单调用IJob**

如果只有一个IJob的话，可以简单的写  
`JobHandle handle = job.Schedule();`  
这段代码并没有立刻阻塞主线程，你仍然可以执行其他操作  
`DoOtherWork();`  
直到这段代码`handle.Complete();`，主线程才会开始阻塞，直到所有Job完成。 

**调用并行的IJobParallelFor**

不太一样的地方是，job.Schedule的时候，需要传递数据长度，和批处理大小  
`JobHandle handle = job.Schedule(vectors.Length, 64);`  
依然等待完成即可  
`handle.Complete();`

**依赖关系与链式调度**

Job 之间可以建立依赖关系，确保执行顺序：

```csharp
public struct JobA : IJob { /* ... */ }
public struct JobB : IJob { /* ... */ }
public struct JobC : IJobParallelFor { /* ... */ }

void ScheduleJobChain()
{
    var jobA = new JobA();
    var jobB = new JobB();
    var jobC = new JobC();
    
    // JobB 依赖 JobA
    JobHandle handleA = jobA.Schedule();
    JobHandle handleB = jobB.Schedule(handleA); // 传入依赖句柄
    
    // JobC 依赖 JobB，并行处理1000个元素，每批32个
    JobHandle handleC = jobC.Schedule(1000, 32, handleB);
    
    // 只需等待最后一个 Job
    handleC.Complete();
}
```

**Transform相关的调用**

```c#
TransformAccessArray transformArray = new TransformAccessArray(transforms);
var job = new MoveUpJob { DeltaTime = Time.deltaTime, Speed = 5f };
JobHandle handle = job.Schedule(transformArray);
```

请注意，每帧new TransformAccessArray是一个非常消耗性能的事情，特别是长度高的时候。  1ms 左右 new 一次
最佳实践是写一个EntityMoveSystem，持有一个私有字段，创建一个固定长度的数组，**动态扩容**。  
`_transformAccessArray = new TransformAccessArray(transforms);`  
这里的transform作为了移动的载具，可以作为父节点分配给需要被移动的物体，然后物体被回收时也同时被回收。

测试结论是当物体数量1000以下时，基本不需要考虑用Job优化。当物体数量在2000以上时，仅消耗传统方法1/5的时间。

```ad-note
非常有趣的情况是，如果我们设置了  
Physics.autoSimulation = false;  
Physics.autoSyncTransforms = false;  
并且在FixedUpdate里Physics.Simulate(fixedDeltaTime);  **帧同步的时候常用**
在LateUpdate里Physics.SyncTransforms();  
unity内部其实也是自动使用了IJobParallelForTransform来并行处理
```

**使用处理后的数据**

将Job处理好后的数据传给感兴趣的其他模块。

**手动释放内存**

必须为第1步分配的非托管集合手动释放内存。  
`data.Dispose();`

### 5. Burst 编译

`[BurstCompile]` 是一个属性标记，用于触发 Burst 编译器。  
把它放在一个结构体（如 IJob 结构体）或一个静态方法上，就是在告诉 Unity 的 Burst 编译器：“请把这个代码编译成极度优化的、平台特定的本地机器码。”  
使用Burst编译的好处

**极高的性能：**

- 向量化（SIMD）：这是最大的亮点。Burst 能将我们的循环操作编译成 SSE/AVX 等 CPU 指令，使得一条指令可以同时对多个数据（如4个float）进行操作，而不是一次一个。这对于数学计算密集型任务（如动画、物理、粒子模拟）是效率极高的。
- 低级优化：Burst 编译器比标准的 .NET JIT（即时编译器）激进得多，它会进行循环展开、常量传播、内联等各种底层优化，生成堪比手动编写 C++ 代码效率的机器码。

**避免托管代码开销：**

- 生成的代码直接是本地码，运行时不经过 .NET 虚拟机的 JIT 编译和垃圾回收（GC）管理，避免了相关的性能开销。

**跨平台优化：**

- Burst 会为我们的目标平台（Windows, macOS, Android, iOS等）生成特定的指令集，确保在每个平台上都能获得最佳性能。

需注意代码必须符合 Burst 的安全子集（避免使用托管类型、异常等）。

```csharp
using Unity.Burst;

[BurstCompile] // 添加此特性让 Burst 编译器优化
public struct OptimizedJob : IJobParallelFor
{
    public NativeArray<float> Data;
    
    public void Execute(int index)
    {
        Data[index] = math.abs(Data[index]);
    }
}
```

请尽量使用Burst.Compatible的数学库以便Brust编译出高效的机器码


### 5. 调试和诊断

#### 5.1 使用 Profiler 分析 Job 执行

Window > Analysis > Profiler > Job Details

#### 5.2 增加日志

使用 UnityEngine.Debug.Log 会报错  
使用 Unity.Collections.LowLevel.Unsafe.UnsafeUtility 中的方法  
Job 中不能抛出异常，否则会导致 Silent Failure（静默失败）。建议：

- 使用 `NativeArray<int>` 或 `NativeQueue<Exception>` 收集错误信息。
- 在 `Complete()` 后检查并处理。

#### 5.3 使用 Safety Checks

在 Player Settings 中启用/禁用安全检测，开发阶段启用，发布时禁用以提升性能。

#### 5.4 Job 的依赖关系图可视化

Unity Profiler 中的 Job Dependency Viewer，帮助可视化 Job 之间的依赖关系和执行时间。  

#### 5.5 Job 中常用性能分析标记

```csharp
using Unity.Profiling;

var marker = new ProfilerMarker("MyJob.Execute");
public void Execute(int index)
{
    using (marker.Auto())
    {
        // job code
    }
}
```


### 推荐使用场景

- 大规模数学运算（矩阵、向量、物理）
- 网格/顶点数据处理
- 动画骨骼计算
- 大规模状态更新（如1000+实体位置更新）
- 寻路、视野、碰撞、挤压等算法

### 不推荐场景

- 简单、轻量级的计算（开销可能大于收益）
- 需要频繁访问 Unity API 的操作
- 逻辑复杂、分支众多的算法
- 需要每帧分配内存的操作