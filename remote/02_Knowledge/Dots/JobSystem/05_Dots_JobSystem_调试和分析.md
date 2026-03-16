
## 1. 查看Burst编译

Jobs > Burst > Open Inspector

在窗口搜索对饮的函数名称 查看是否正确的编译


## 2. 使用 Profiler 分析 Job 执行

Window > Analysis > Profiler > Job Details


## 3. 添加日志

- 使用 UnityEngine.Debug.Log 会报错  
- 使用 Unity.Collections.LowLevel.Unsafe.UnsafeUtility 中的方法  
- Job 中不能抛出异常，否则会导致 Silent Failure（静默失败）。建议：

- 使用 `NativeArray<int>` 或 `NativeQueue<Exception>` 收集错误信息。
- 在 `Complete()` 后检查并处理。

## 4. Job 的依赖关系图可视化

Unity Profiler 中的 Job Dependency Viewer，帮助可视化 Job 之间的依赖关系和执行时间。


## 5. Job 中常用性能分析标记

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