---
title: JobSystem 例子
date: 2026-03-16
tags:
  - unity
  - dots
  - job-system
  - example
type: framework
aliases:
  例子
description: JobSystem使用例子
draft: false
---


## 避免长时间作业

将长时间作业分拆成多个小作业。

特别是，长时间运行的[`IJobParallelFor`](https://docs.unity.cn/2023.1/Documentation/ScriptReference/Unity.Jobs.IJobParallelFor.html)作业会对作业系统产生负面影响，因为这些作业类型会刻意尝试在作业批次大小内尽可能多地运行工作线程。如果您无法拆分长时间并行作业，请考虑在调度作业时增加作业的批次大小，以限制有多少工作线程负责处理长时间运行的作业。


```c#
MyParallelJob jobData = new MyParallelJob();
jobData.Data = someData;  
jobData.Result = someArray;  
// Use half the available worker threads, clamped to a minimum of 1 worker thread
const int numBatches = Math.Max(1, JobsUtility.JobWorkerCount / 2); 
const int totalItems = someArray.Length;
const int batchSize = totalItems / numBatches;
// Schedule the job with one Execute per index in the results array and batchSize items per processing batch
JobHandle handle = jobData.Schedule(result.Length, totalItems, batchSize);
```

## IJobFor

作业允许您选择多种方式来安排工作执行。Run  
  
将在主线程上运行作业并立即完成。Schedule  
  
会安排作业在工作线程（也可能是主线程）上运行，但会指示工作应在单线程中执行。此选项允许工作在主线程之外完成，但由于工作将按顺序执行，因此更容易理解。ScheduleParallel  
  
会安排作业在多个工作线程上并发运行。此调度选项可以提供最佳性能，但需要用户了解从多个工作线程同时访问相同数据时可能发生的冲突。Execute  
  
(int index) 将针对从 0 到指定长度的每个索引执行一次。Run  
  
和 Schedule 将保证作业的 Execute(int index) 方法按顺序调用。ScheduleParallel


```c#
using UnityEngine;
using Unity.Collections;
using Unity.Jobs;

class ApplyVelocityParallelForSample : MonoBehaviour
{
    struct VelocityJob : IJobFor
    {
        // Jobs declare all data that will be accessed in the job
        // By declaring it as read only, multiple jobs are allowed to access the data in parallel
        [ReadOnly]
        public NativeArray<Vector3> velocity;

        // By default containers are assumed to be read & write
        public NativeArray<Vector3> position;

        // Delta time must be copied to the job since jobs generally don't have concept of a frame.
        // The main thread waits for the job same frame or next frame, but the job should do work deterministically
        // independent on when the job happens to run on the worker threads.
        public float deltaTime;

        // The code actually running on the job
        public void Execute(int i)
        {
            // Move the positions based on delta time and velocity
            position[i] = position[i] + velocity[i] * deltaTime;
        }
    }

    public void Update()
    {
        var position = new NativeArray<Vector3>(500, Allocator.Persistent);

        var velocity = new NativeArray<Vector3>(500, Allocator.Persistent);
        for (var i = 0; i < velocity.Length; i++)
            velocity[i] = new Vector3(0, 10, 0);

        // Initialize the job data
        var job = new VelocityJob()
        {
            deltaTime = Time.deltaTime,
            position = position,
            velocity = velocity
        };

        // Schedule job to run immediately on main thread. First parameter is how many for-each iterations to perform.
        job.Run(position.Length);

        // Schedule job to run at a later point on a single worker thread.
        // First parameter is how many for-each iterations to perform.
        // The second parameter is a JobHandle to use for this job's dependencies.
        //   Dependencies are used to ensure that a job executes on worker threads after the dependency has completed execution.
        //   In this case we don't need our job to depend on anything so we can use a default one.
        JobHandle sheduleJobDependency = new JobHandle();
        JobHandle sheduleJobHandle = job.Schedule(position.Length, sheduleJobDependency);

        // Schedule job to run on parallel worker threads.
        // First parameter is how many for-each iterations to perform.
        // The second parameter is the batch size,
        //   essentially the no-overhead innerloop that just invokes Execute(i) in a loop.
        //   When there is a lot of work in each iteration then a value of 1 can be sensible.
        //   When there is very little work values of 32 or 64 can make sense.
        // The third parameter is a JobHandle to use for this job's dependencies.
        //   Dependencies are used to ensure that a job executes on worker threads after the dependency has completed execution.
        JobHandle sheduleParralelJobHandle = job.ScheduleParallel(position.Length, 64, sheduleJobHandle);

        // Ensure the job has completed.
        // It is not recommended to Complete a job immediately,
        // since that reduces the chance of having other jobs run in parallel with this one.
        // You optimally want to schedule a job early in a frame and then wait for it later in the frame.
        sheduleParralelJobHandle.Complete();

        Debug.Log(job.position[0]);

        // Native arrays must be disposed manually.
        position.Dispose();
        velocity.Dispose();
    }
}
```

ScheduleParallel
batch分配原则：
- 任务重 ： 使用小的数 如1 ， 多分配几个线程
- 任务轻 ： 使用较大的数， 一个线程多执行几次

注意：由于 index 是无序的需要注意数据安全

https://www.bilibili.com/video/BV1Gd4y1B7ob?spm_id_from=333.788.videopod.sections&vd_source=8beb74be6b19124f110600d2ce0f3957

[定点动画的例子](https://www.bilibili.com/video/BV1314y1V7mF?spm_id_from=333.788.videopod.sections&vd_source=8beb74be6b19124f110600d2ce0f3957)