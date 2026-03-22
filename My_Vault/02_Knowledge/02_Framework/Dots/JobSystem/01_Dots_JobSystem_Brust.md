---
title: Dots JobSystem Burst编译
date: 2026-03-16
tags:
  - unity
  - dots
  - job-system
  - burst
type: framework
aliases:
  Burst
description: Unity Dots JobSystem Burst编译器使用
draft: false
---


## 1. 如何使用


```c#
[BurstCompile]
public static int Add(int a, int b)
{
    return a + b;
}
```

直接使用 `[BurstCompile]` 标记类或者方法即可

### 2. 限制

只支持 **值类型** 的数据编译

### 3. 向量化问题

向量化就是把多个计算打包成1个指令，比如float3的计算天然就是向量化的。向量化最好使用`Unity.Mathematics`库的类型和方法，不然可能失败。

如果你没有进行向量化计算，还可以对循环向量化，之前的性能测试可因此再提升到0.09ms，见之前关于二维数组的章节。循环向量化就是让一些可以并行的For loop计算，在一个指令集中完成，Burst会自动判断优化。

**如何判断**

打开Burst Inspector工具（在Jobs菜单里）
## 4. 数据类型转换

Vector3 -> float3

```c#
var floats = new NativeArray<float3>(100, Allocator.TempJob);
NativeArray<Vector3> vertices = floats.Reinterpret<Vector3>();
Vector3[] verticesArray = vertices.ToArray();
floats.Dispose();

var floats = new NativeArray<float>(new float[] {1,2,3}, Allocator.TempJob);
NativeArray<Vector3> aaa = floats.Reinterpret<Vector3>(sizeof(float));
Debug.Log(string.Join("\n", aaa.Select(v => v.ToString())));
floats.Dispose();

```


### 5. 可以在 jobsystem 外部使用 `[BurstCompile]` 

注意点：

- 返回值不能是 NativeArray -- 容易资源泄露
- 参数中不能使用 NatvieArray -- 值类型， 直接复制，容易资源泄露

````ad-note
title: 推荐方法

1. **使用 ref 修饰 NativeArray**

```c#
[BurstCompile]
// 使用 BurstCompile 属性允许Burst编译
public static void GenerateGaussianFilter(int size, float deviationSquare, ref NativeArray<float> outputFilter)
{
    // 你的算法逻辑，直接操作 outputFilter
    for (int i = 0; i < size; i++)
    {
        // 示例计算，请替换为你的实际算法
        outputFilter[i] = Mathf.Exp(-(i * i) / (2.0f * deviationSquare));
    }
}
```

2. **使用 unsafe 的 指针操作**

```c#
[BurstCompile]
// 使用 unsafe 关键字和 BurstCompile 属性
public static unsafe float* GenerateGaussianFilter(int size, float deviationSquare, Allocator allocator)
{
    // 创建 NativeArray
    var array = new NativeArray<float>(size, allocator);
    // 获取指向其数据的指针并返回
    return (float*)array.GetUnsafePtr();
}
```

````

| 方案              | 优点                  | 缺点               | 适用场景            |
| --------------- | ------------------- | ---------------- | --------------- |
| **使用 `ref` 参数** | ✅ 安全、直观、符合Burst最佳实践 | 调用方需预先分配内存       | **绝大多数情况，推荐使用** |
| **返回指针**        | 灵活，可直接操作内存          | ❌ 危险，需手动管理内存，易泄漏 | 高级性能优化场景，需谨慎使用  |
