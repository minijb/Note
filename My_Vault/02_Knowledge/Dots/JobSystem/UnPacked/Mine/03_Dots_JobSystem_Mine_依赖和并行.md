---
title: JobSystem 依赖和并行
date: 2026-03-16
tags:
  - unity
  - dots
  - job-system
  - parallel
type: framework
aliases:
  依赖并行
description: JobSystem依赖和并行处理
draft: false
---


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