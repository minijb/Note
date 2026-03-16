
在异步编程模型中，有几个关键概念需要了解：

- 可以对 I/O 绑定和 CPU 绑定代码使用异步代码，但实现不同。
- 异步代码使用 `Task<T>` 和 `Task` 对象作为构造来为在后台运行的工作建模。
- 关键字 `async` 将方法声明为异步方法，这样就可以在方法正文中使用 `await` 关键字。
- 应用 `await` 关键字时，代码将挂起调用的方法，并将控制权交还给其调用者，直到任务完成。
- 只能在异步方法中使用 `await` 表达式。

```c#
static DamageResult CalculateDamageDone()
{
    return new DamageResult()
    {
        // Code omitted:
        //
        // Does an expensive calculation and returns
        // the result of that calculation.
    };
}

s_calculateButton.Clicked += async (o, e) =>
{
    // This line will yield control to the UI while CalculateDamageDone()
    // performs its work. The UI thread is free to perform other work.
    var damageResult = await Task.Run(() => CalculateDamageDone());
    DisplayDamage(damageResult);
};
```


|                          |            |                                                                                                                                                                                                                       |
| ------------------------ | ---------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| _代码是否应等待结果或作，例如数据库中的数据？_ | **I/O 绑定** | 使用 `async` 修饰符和 `await` 表达式_，而不_使用 `Task.Run` 方法。  <br>  <br>避免使用任务并行库。                                                                                                                                               |
| _代码是否应该运行昂贵的计算？_         | **CPU 绑定** | 使用`async`修饰符和`await`表达式，并使用`Task.Run`方法在另一个线程上生成工作。 此方法解决了 CPU 响应能力方面的问题。  <br>  <br>如果该工作同时适用于并发和并行，还应考虑使用[任务并行库](https://learn.microsoft.com/zh-cn/dotnet/standard/parallel-programming/task-parallel-library-tpl)。 |


**Linq 结合  组合**

```c#
private static async Task<User[]> GetUsersAsyncByLINQ(IEnumerable<int> userIds)
{
    var getUserTasks = userIds.Select(id => GetUserAsync(id)).ToArray();
    return await Task.WhenAll(getUserTasks);
}
```


尽管使用 LINQ 编写的代码较少，但在将 LINQ 与异步代码混合时，请谨慎作。 LINQ 使用延迟（或延迟）执行，这意味着在枚举序列之前，不会发生异步调用。

### 审查

使用 `async` 修饰符时，应在方法正文中包含一个或多个 `await` 表达式。 如果编译器未遇到 `await` 表达式，该方法将无法生成。 尽管编译器生成警告，但代码仍会编译，编译器会运行该方法。 由 C# 编译器为异步方法生成的状态机无法完成任何工作，因此整个过程效率很低。

### async void

事件处理程序必须声明 `void` 返回类型，不能像其他方法一样使用或返回 `Task` 对象 `Task<T>` 。 编写异步事件处理程序时，需要对处理程序的返回方法使用 `async` 修饰符 `void` 。 返回方法的其他实现 `async void` 不遵循 TAP 模型，并且可能会带来挑战：


- `async void` 方法中引发的异常无法在该方法外部被捕获
- `async void` 方法难以测试
- `async void` 方法在调用方未期望其为异步时可能会导致负面效果

| 任务方案            | 当前代码                        | 替换为“await”           |
| --------------- | --------------------------- | -------------------- |
| _检索后台任务的结果_     | `Task.Wait` 或 `Task.Result` | `await`              |
| _在任何任务完成时继续_    | `Task.WaitAny`              | `await Task.WhenAny` |
| _**完成所有**任务后继续_ | `Task.WaitAll`              | `await Task.WhenAll` |
| _在一段时间后继续_      | `Thread.Sleep`              | `await Task.Delay`   |

### 考虑使用 ValueTask 类型

当异步方法返回 `Task` 对象时，可能会在某些路径中引入性能瓶颈。 由于 `Task` 是引用类型，因此从堆分配对象 `Task` 。 如果使用 `async` 修饰符声明的方法返回缓存结果或同步完成，那么额外分配可能会在代码的性能关键部分累积显著的时间成本。 当分配在紧密循环中发生时，这种情况可能会变得昂贵。 有关详细信息，请参阅[通用的异步返回类型](https://learn.microsoft.com/zh-cn/dotnet/csharp/language-reference/keywords/async#return-types)。



**如果必须在`Task`上同步阻止，以下是按优先程度从高到低的可用方法：**

- [使用 GetAwaiter().GetResult()](https://learn.microsoft.com/zh-cn/dotnet/csharp/asynchronous-programming/async-scenarios#use-getawaitergetresult)
- [将 Task.Run 用于复杂方案](https://learn.microsoft.com/zh-cn/dotnet/csharp/asynchronous-programming/async-scenarios#use-taskrun-for-complex-scenarios)
- [使用 Wait() 和 Result](https://learn.microsoft.com/zh-cn/dotnet/csharp/asynchronous-programming/async-scenarios#use-wait-and-result)


#### 使用 GetAwaiter（）。GetResult（）

当必须同步阻止时，模式 `GetAwaiter().GetResult()` 通常是首选方法：

C#

```
// When you cannot use await
Task<string> task = GetDataAsync();
string result = task.GetAwaiter().GetResult();
```

此方法：

- 保留原始异常而不将其包装在一个 `AggregateException`中。
- 阻止当前线程，直到任务完成。
- 如果未仔细使用，仍存在死锁风险。