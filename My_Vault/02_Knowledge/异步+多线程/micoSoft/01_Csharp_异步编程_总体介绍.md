
.NET 提供了三种用于执行异步作的模式：

- **基于任务的异步模式 （TAP）**  它使用单个方法来表示异步作的启动和完成
- **基于事件的异步模式（EAP）** 这是一个提供异步行为的基于事件的传统模型。 它需要一种具有`Async`后缀的方法，该方法包含一个或多个事件、事件处理程序委托类型和`EventArg`派生类型 
- **异步编程模型 （APM） 模式**  这是使用 [IAsyncResult](https://learn.microsoft.com/zh-cn/dotnet/api/system.iasyncresult) 接口提供异步行为的旧模型。 在此模式中，异步操作需要 `Begin` 和 `End` 方法（例如，使用 `BeginWrite` 和 `EndWrite` 方法来实现异步写入操作）。 对于新开发，不再建议使用此模式


## TAP

返回类型  ： TAP 中的异步方法在返回可等待类型（如 `Async、Task、Task<TResult> 和 ValueTask`）的方法的操作名称后面添加 `ValueTask<TResult>` 后缀.

此外，请考虑添加参数 [CancellationToken](https://learn.microsoft.com/zh-cn/dotnet/api/system.threading.cancellationtoken) ，即使 TAP 方法的同步对应项不提供参数。


**组合器** ： 将多个 task 组合在一起 ， WhenAll  WhenAny

### 任务状态

该 [Task](https://learn.microsoft.com/zh-cn/dotnet/api/system.threading.tasks.task) 类提供异步作的生命周期，该周期由 [TaskStatus](https://learn.microsoft.com/zh-cn/dotnet/api/system.threading.tasks.taskstatus) 枚举表示。 为了支持派生自 [Task](https://learn.microsoft.com/zh-cn/dotnet/api/system.threading.tasks.task) 和 [`Task<TResult>`](https://learn.microsoft.com/zh-cn/dotnet/api/system.threading.tasks.task-1) 的类型的角落案例，并支持构造与计划的分离，[Task](https://learn.microsoft.com/zh-cn/dotnet/api/system.threading.tasks.task) 类公开了 [Start](https://learn.microsoft.com/zh-cn/dotnet/api/system.threading.tasks.task.start) 方法。 由公共 [Task](https://learn.microsoft.com/zh-cn/dotnet/api/system.threading.tasks.task) 构造函数创建的任务称为_冷任务_，因为它们在未调度 [Created](https://learn.microsoft.com/zh-cn/dotnet/api/system.threading.tasks.taskstatus#system-threading-tasks-taskstatus-created) 状态下开始其生命周期，并且仅当对这些实例调用[Start](https://learn.microsoft.com/zh-cn/dotnet/api/system.threading.tasks.task.start)时才进行调度。

所有其他任务都以热状态开始其生命周期，这意味着它们所代表的异步操作已被启动，其任务状态为除 [TaskStatus.Created](https://learn.microsoft.com/zh-cn/dotnet/api/system.threading.tasks.taskstatus#system-threading-tasks-taskstatus-created) 之外的枚举值。 必须激活从 TAP 方法返回的所有任务。 **如果 TAP 方法在内部使用任务的构造函数来实例化要返回的任务，则在返回该任务之前，TAP 方法必须在 [Start](https://learn.microsoft.com/zh-cn/dotnet/api/system.threading.tasks.task.start) 对象上调用 [Task](https://learn.microsoft.com/zh-cn/dotnet/api/system.threading.tasks.task)。** TAP 方法的使用者可以安全地假设返回的任务处于活动状态且不应尝试对从 TAP 方法返回的任何 [Start](https://learn.microsoft.com/zh-cn/dotnet/api/system.threading.tasks.task.start) 调用 [Task](https://learn.microsoft.com/zh-cn/dotnet/api/system.threading.tasks.task)。 对活动的任务调用 [Start](https://learn.microsoft.com/zh-cn/dotnet/api/system.threading.tasks.task.start) 将引发 [InvalidOperationException](https://learn.microsoft.com/zh-cn/dotnet/api/system.invalidoperationexception) 异常。


### 取消任务

`cancellationToken`


该异步操作监视取消请求的此标记。 如果收到取消请求，可以选择接受该请求并取消操作。 如果取消请求导致工作过早结束，TAP 方法将返回一个任务，其结束状态为 [Canceled](https://learn.microsoft.com/zh-cn/dotnet/api/system.threading.tasks.taskstatus#system-threading-tasks-taskstatus-canceled)；没有可用的结果，也不会抛出异常。 状态[Canceled](https://learn.microsoft.com/zh-cn/dotnet/api/system.threading.tasks.taskstatus#system-threading-tasks-taskstatus-canceled)被视为任务的最终（已完成）状态，以及[Faulted](https://learn.microsoft.com/zh-cn/dotnet/api/system.threading.tasks.taskstatus#system-threading-tasks-taskstatus-faulted)[RanToCompletion](https://learn.microsoft.com/zh-cn/dotnet/api/system.threading.tasks.taskstatus#system-threading-tasks-taskstatus-rantocompletion)状态。 因此，如果任务处于 [Canceled](https://learn.microsoft.com/zh-cn/dotnet/api/system.threading.tasks.taskstatus#system-threading-tasks-taskstatus-canceled) 状态，则其 [IsCompleted](https://learn.microsoft.com/zh-cn/dotnet/api/system.threading.tasks.task.iscompleted) 属性返回 `true`。 在 [Canceled](https://learn.microsoft.com/zh-cn/dotnet/api/system.threading.tasks.taskstatus#system-threading-tasks-taskstatus-canceled) 状态下完成任务时，将计划或执行向任务注册的任何延续，除非延续选项（如 [NotOnCanceled](https://learn.microsoft.com/zh-cn/dotnet/api/system.threading.tasks.taskcontinuationoptions#system-threading-tasks-taskcontinuationoptions-notoncanceled)）特定于取消延续。 任何通过使用语言功能异步等待已取消的任务的代码都将继续运行，但不接收 [OperationCanceledException](https://learn.microsoft.com/zh-cn/dotnet/api/system.operationcanceledexception) 或其中派生的异常。 通过诸如 [Wait](https://learn.microsoft.com/zh-cn/dotnet/api/system.threading.tasks.task.wait) 的方法同步阻止的代码等待任务，并且 [WaitAll](https://learn.microsoft.com/zh-cn/dotnet/api/system.threading.tasks.task.waitall) 将继续运行但出现异常。


## 任务进度

[`IProgress<T>`](https://learn.microsoft.com/zh-cn/dotnet/api/system.iprogress-1)

```c#
public Task ReadAsync(byte[] buffer, int offset, int count,
                      IProgress<long> progress)
```

