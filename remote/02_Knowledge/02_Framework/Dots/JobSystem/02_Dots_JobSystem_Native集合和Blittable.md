
Native集合

- 为 struct 是一个值类型
- 本质是一个包装器 --- 还有一个指针。 因此内部的T---需要是定长的。[源码](https://blog.csdn.net/enternalstar/article/details/143299952)
	- 这个指针通过 unity 内部的 allocateor 分配非托管的内存块和一些源数据
	- 赋值，拷贝这些都是**浅拷贝** ，本质是复制指针


JobSystem 需要一个 **非托管集合** -- 一个 struct  同时内部所有字段都必须是 Blittable。 **原因 ： 可以确定长度**

![image.png](https://s2.loli.net/2025/10/15/eQTlvDgJc51KFRP.png)


可以使用 struct 但是 但是需要满足，结构体里只能包含Blittable类型，或**嵌套其他非托管结构体**。 部分类型可以使用 `Unity.Mathematics` 内的类型替代如 float3 等。

> 使用 `[StructLayout(LayoutKind.Sequential, Pack = 4)]` 实现结构内部的字节对齐


**本质原因** ： 多线程拷贝数据的时候内存分布是一致的。

## 其他 Native集合

- `Unity.Collections`  Native开头的集合类型
- `Unity.Collections.LowLevel.Unsafe` 以UnSafe开头的集合类型-- 没有安全检查

引入 Unsafe 集合 ： 因为 Native 集合不能嵌套。 因此您可以使用 `NativeList<UnsafeList>` 或 `UnsafeList<UnsafeList>`，但不能使用 `NativeList<NativeList>`。

**数组**

| 数据结构                  | 描述                                               |
| --------------------- | ------------------------------------------------ |
| `NativeList< T >`     | 一个可调整大小的列表。具有线程和处置安全检查。                          |
| `UnsafeList< T >`     | 一个可调整大小的列表。                                      |
| `UnsafePtrList< T >`  | 一个可调整大小的指针列表。                                    |
| NativeStream          | 一组仅append的、无类型的缓冲区。具有线程和处置安全检查。                  |
| UnsafeStream          | 一组仅append的、无类型的缓冲区。                              |
| UnsafeAppendBuffer    | 仅附加的无类型缓冲区。                                      |
| `NativeQueue<T>`      | 一个可调整大小的队列。具有线程和处置安全检查。                          |
| `UnsafeRingQueue<T>`  | 固定大小的循环缓冲区。                                      |
| `FixedList32Bytes<T>` | 一个 32 字节的列表，包括 2 字节的开销，因此有 30 字节可用于存储。最大容量取决于 T。 |

**map/set**

| 数据结构                             | 描述                                              |
| -------------------------------- | ----------------------------------------------- |
| NativeHashMap<TKey, TValue>      | 键值对的无序关联数组。具有线程和处置安全检查。                         |
| UnsafeHashMap<TKey, TValue>      | 键值对的无序关联数组。                                     |
| NativeHashSet< T >               | 一组独特的值。具有线程和处置安全检查。                             |
| UnsafeHashSet< T >               | 一组独特的值。                                         |
| NativeMultiHashMap<TKey, TValue> | 键值对的无序关联数组。Key不必是唯一的，即两对可以具有相同的Key。具有线程和处置安全检查。 |
| UnsafeMultiHashMap<TKey, TValue> | 键值对的无序关联数组。Key不必是唯一的，即两对可以具有相同的Key。             |
**bitarray**

| 数据结构           | 描述                   |
| -------------- | -------------------- |
| BitField32     | 一个固定大小的 32 位数组。      |
| BitField64     | 一个固定大小的 64 位数组。      |
| NativeBitArray | 任意大小的位数组。具有线程和处置安全检查 |
| UnsafeBitArray | 任意大小的位数组。            |
**字符串**

| 数据结构               | 描述                                              |
| ------------------ | ----------------------------------------------- |
| NativeText         | UTF-8 编码的字符串。可变和可调整大小。具有线程和处置安全检查。              |
| FixedString32Bytes | 一个 32 字节的 UTF-8 编码字符串，包括 3 字节的开销，因此有 29 字节可用于存储 |

**其他**

| 数据结构                  | 描述                                   |
| --------------------- | ------------------------------------ |
| `NativeReference<T>`  | 对单个值的引用。功能上等同于长度为 1 的数组。具有线程和处置安全检查。 |
| UnsafeAtomicCounter32 | 一个 32 位原子计数器                         |
| UnsafeAtomicCounter64 | 一个 64 位原子计数器                         |

## Reference


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

- 所有数值类型（`int`, `float`, `double`, `long`, `byte` 等）
- `char`
- `bool`
- `enum`
- `struct`（但有条件，见下文）

- 特点：赋值操作会进行完整的拷贝。
- 关系中的位置：这是所有后续类型的基础。非托管类型和 Blittable 类型首先必须是值类型

**非托管类型 (Unmanaged Types)**

这是值类型的一个子集，是 C# 7.3 引入的一个正式概念，主要用于 `unsafe` 上下文和与非托管代码的交互。

- 定义：一种类型，如果它满足以下所有条件，则它是非托管类型：

- 它必须是值类型（引用类型永远不是非托管的）。
- 它不包含任何引用类型的字段。
- 它的所有字段递归地也都是非托管类型。

关系中的位置：非托管类型是值类型的子集。它排除了那些包含引用类型的值类型（如某些 `struct`）。

**Blittable 类型 (Blittable Types)**

这是非托管类型中一个更严格的子集，是与非托管代码互操作（P/Invoke）时最关键的概念。

- 定义：一种数据类型，它在托管内存和非托管内存中具有相同的二进制表示形式（相同的内存布局和位模式）。因此，在互操作时，运行时可以直接进行“位拷贝”（blit）来传递数据，而无需进行任何特殊的转换或封送处理（Marshaling）。
- 包括：

- 大多数基础数值类型：`byte`, `sbyte`, `short`, `ushort`, `int`, `uint`, `long`, `ulong`, `single`, `double`。
- 包含“非嵌套”的 Blittable 类型的数组（如 `int[]`）。
- 只包含 Blittable 类型字段的 `struct`，并且其布局是连续的（通常是 `[StructLayout(LayoutKind.Sequential)]` 或默认顺序）。

- 不包括（重要的非 Blittable 类型）：

- `bool`： 在C#中占1字节，但在非托管代码中可能是4字节（如Win32 BOOL）。需要封送处理。
- `char`： 在C#中是2字节Unicode，在非托管代码中可能是1字节ANSI。需要封送处理。
- `string`： 引用类型，且编码不同，必须封送。
- 包含 `bool` 或 `char` 字段的 `struct`：因为这些字段不是 Blittable 的，所以整个结构体也不是 Blittable 的。

```


````ad-note
title: 什么是结构数组（SoA）
结构数组指的是为每种数据创建平行的、等长的 `NativeArray`。这是 Data-Oriented Design（面向数据设计）的核心。

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
如果每个结构体内部都有一个独立的 `NativeArray`，数据会被分散在内存的各个角落，导致大量的缓存未命中，性能会急剧下降。

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
这是一个非常重要的特性，也是它能在 JobSystem 中安全使用的关键原因之一。但是，它的行为与简单的值类型（如 `int`、`float`）有本质区别，理解这一点至关重要。

**为什么 `NativeArray<T>` 是值类型，却又如此特殊？**

简单来说：`NativeArray<T>` 是一个包装器或智能指针。它的结构体内部并不直接存储数据数组，而是包含了一个指向Unity内存管理系统（Allocator）中分配的非托管内存块的指针和一些管理元数据（如长度、版本号等）。  

**这种设计带来的行为特性：**

1.值类型的拷贝语义：

1. 当我们将一个 `NativeArray` 变量赋值给另一个变量，或者作为参数传递给方法时，发生的是值类型的拷贝。这意味着 `m_Buffer`、`m_Length` 等内部字段的值被复制了一份。
2. 关键点：复制的是指针（`m_Buffer`），而不是指针所指向的数据。因此，两个 `NativeArray` 变量（`arrayA` 和 `arrayB`）将指向同一块非托管内存数据。

2.“浅拷贝”而非“深拷贝”：

1. 对 `arrayA[0]` 进行修改，会直接反映在 `arrayB[0]` 上，因为它们操作的是同一片内存。
2. 这种行为类似于引用类型，但其本质是值类型（结构体）包含了一个指针。

**为什么Unity要这样设计？**

1. 性能：避免在Job之间传递数据时进行昂贵的内存拷贝。Job可以高效地读写同一块内存，从而实现线程间通信。
2. 与JobSystem协同工作：作为值类型，`NativeArray` 可以完美地嵌入到 `IJob` 结构体中，满足Job参数必须是Blittable类型的要求。因为它只包含指针和整数等原始类型，整个结构体的内存布局是固定的和明确的。
3. 内存安全：虽然数据是共享的，但Unity的安全系统（通过 `AtomicSafetyHandle`）会跟踪`NativeArray`的生命周期和访问权限。例如，它会在我们尝试在Schedule的Job仍在执行时`Dispose()`数组，或者在一个写入权限不匹配的Job中写入数据时抛出异常，从而防止内存损坏和数据竞争。
   
**总结**

4. `NativeArray<T>` 是一个值类型的struct。
5. 它进行的是浅拷贝，只复制内部的指针和元数据，多个变量共享同一份底层数据。
6. 它的内存布局只包含原生类型（如指针、int），可以被安全地直接拷贝到工作线程。
7. 必须管理它的生命周期。因为它管理着非托管内存，必须在使用完毕后调用 Dispose() 方法来释放内存，否则会导致内存泄漏。
8. 多个 NativeArray 变量可能指向同一块内存，修改一个会影响另一个。这可能导致难以察觉的 Bug，尤其是在多个 Job 中共享数据时。

   
```


## 最大扁平化

```c#
strutc A{
	// ohters
	NativeList<float3> path
}

NativeArray<A> entities;
```

此时 entities 中 path 的分布是离散的。如果需要查找多个的时候，其实会存在大量的缓存未命中。

那么此时 

```c#
strutc A{
	// ohters	
}
NativeArray<A> entites;
NativeArray<NativeList<float3>> paths;


// 如果要跟进一步
NativeArray<int> start;
NativeArray<int> length;
NativeArray<float3> paths;
```

此时为缓存命中的情况就好很多。

## :LiList: Native 注意事项

1. 必须手动释放 ： `Dispose`
2. 多使用只读标记，允许多个作业并行读取 `[ReadOnl]`
3. 不是类，先要修改原始的值，必须通过 复制-修改-赋值
```c#
MyStruct temp = myNativeArray[i]; // 复制
temp.value = temp.value + 1;       // 修改
myNativeArray[i] = temp;          // 赋值

// ❌错误示范
myNativeArray[i].value++
```
4. 避免内部分配托管内存否则会组织Burst编译器优化。
5. 在获取数据的之前必须使用 `Complete()` 等待线程完成工作。
6. Native 嵌套规则

| 集合              | 嵌套规则                                            |
| --------------- | ----------------------------------------------- |
| Native          | 禁止嵌套 Native，但是可以使用unsafe和FixedListNBytes集合，推荐使用 |
| unsafeList      | 几乎所有无指征类型                                       |
| FixedListNBytes | 纯直类型结构，且总大小不超过其字节数N ---- 会自动释放，很方便              |
| 指针              | 手动管理，风险高                                        |
```c#
using Unity.Collections;
using Unity.Collections.LowLevel.Unsafe;
using Unity.Jobs;

public struct DynamicNestedJob : IJobParallelFor
{
    // 核心结构：UnsafeList 的数组
    public NativeArray<UnsafeList<float>> dataBuckets; // !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    // 1. 初始化：创建数组，并为每个元素创建列表
    public void Init(int bucketCount, Allocator allocator)
    {
        dataBuckets = new NativeArray<UnsafeList<float>>(bucketCount, allocator);
        for (int i = 0; i < bucketCount; i++)
        {
            dataBuckets[i] = new UnsafeList<float>(0, allocator);
        }
    }

    // 2. 在Job中并行操作：每个索引只访问自己的列表
    public void Execute(int index)
    {
        dataBuckets[index].Add(index * 1.5f);
    }

    // 3. 关键：必须手动逐层释放内存
    public void Dispose()
    {
        foreach (var list in dataBuckets)
        {
            list.Dispose();
        }
        dataBuckets.Dispose();
    }
}


// 定义：一个数组，每个元素是一个固定大小的列表
NativeArray<FixedList32Bytes<byte>> modifiersPerEntity = new NativeArray<FixedList32Bytes<byte>>(entityCount, Allocator.Persistent);

// 使用：和普通列表API一样，但不会扩容
modifiersPerEntity[entityId].Add((byte)ModifierType.Poisoned);
if (modifiersPerEntity[entityId].Contains((byte)ModifierType.Slowed)) { /* ... */ }

// 释放：只需释放外层数组，内层列表会自动处理
modifiersPerEntity.Dispose();
```


```ad-warning
注意 ： 在并行 Job 中修改嵌套的 `UnsafeList` 时，必须确保**每个并行迭代只访问完全独立的内层列表**，否则需手动加锁
```