
## 依赖

```c#
JobHandle firstJobHandle = firstJob.Schedule();
secondJob.Schedule(firstJobHandle);

// 合并依赖项

NativeArray<JobHandle> handles = new NativeArray<JobHandle>(numJobs, Allocator.TempJob);

// Populate `handles` with `JobHandles` from multiple scheduled jobs...

JobHandle jh = JobHandle.CombineDependencies(handles);
```



## 并行

https://docs.unity.cn/2023.1/Documentation/Manual/JobSystemParallelForJobs.html