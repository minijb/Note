

**基本运行流程**

```c#
public async Task<int> GetUrlContentLengthAsync()
{
    using var client = new HttpClient();

    Task<string> getStringTask =
        client.GetStringAsync("https://learn.microsoft.com/dotnet");

    DoIndependentWork();

    string contents = await getStringTask;

    return contents.Length;
}

void DoIndependentWork()
{
    Console.WriteLine("Working...");
}
```


密切关注 `await` 运算符。 它会暂停 `GetUrlContentLengthAsync`：

- `GetUrlContentLengthAsync` 无法继续，直至 `getStringTask` 完成。
- 同时，控件返回至 `GetUrlContentLengthAsync` 的调用方。
- 当 `getStringTask` 完成时，控件将在此处继续。
- 然后，运算符`await`从`string`中检索`getStringTask`结果。


## 异步编程方法规范

- 方法签名包含`async`修饰符。
    
- 按照约定，异步方法的名称以“Async”后缀结尾。
    
- 返回类型是以下类型之一：
    
    - [`Task<TResult>`](https://learn.microsoft.com/zh-cn/dotnet/api/system.threading.tasks.task-1) 如果方法中有一个返回语句，其中操作数的类型是 `TResult`。
    - [Task](https://learn.microsoft.com/zh-cn/dotnet/api/system.threading.tasks.task) 如果你的方法没有返回语句，或者只有没有操作数的返回语句。
    - `void` 如果您正在编写异步事件处理程序。
    - 具有 `GetAwaiter` 方法的任何其他类型。
    
    有关详细信息，请参阅 [“返回类型和参数](https://learn.microsoft.com/zh-cn/dotnet/csharp/asynchronous-programming/task-asynchronous-programming-model#BKMK_ReturnTypesandParameters) ”部分。
    
- 该方法通常包含至少一个 `await` 表达式，该表达式标记方法在等待的异步操作完成之前无法继续的点。 同时，将方法挂起，并且控件返回到方法的调用方。 本主题的下一节将解释悬挂点发生的情况。

## 异步的返回类型

- `Task, Task<T>`
- 任何具有可访问的 `GetAwaiter` 方法的类型。 `GetAwaiter` 方法返回的对象必须实现 [System.Runtime.CompilerServices.ICriticalNotifyCompletion](https://learn.microsoft.com/zh-cn/dotnet/api/system.runtime.compilerservices.icriticalnotifycompletion) 接口。
- [`IAsyncEnumerable<T>`](https://learn.microsoft.com/zh-cn/dotnet/api/system.collections.generic.iasyncenumerable-1)，对于返回_异步流_的异步方法。
- [`ValueTask<TResult>`](https://learn.microsoft.com/zh-cn/dotnet/api/system.threading.tasks.valuetask-1)
-  void   : 此返回类型主要用于定义事件处理程序，其中返回类型需要是 `void`。 异步事件处理程序通常充当异步程序的起点。



Windows 运行时编程中的异步 API 具有以下返回类型之一，类似于任务：
```
    IAsyncOperation<TResult>，对应于 Task<TResult>
    IAsyncAction，对应于 Task
    IAsyncActionWithProgress<TProgress>
    IAsyncOperationWithProgress<TResult,TProgress>
```


**void** 类型 无法等待， 必须一只执行， 但是此线程内部可以等待其他东西，导致  线程 await


### 通用的异步返回类型和 `ValueTask<TResult>`

```c#
class Program
{
    static readonly Random s_rnd = new Random();

    static async Task Main() =>
        Console.WriteLine($"You rolled {await GetDiceRollAsync()}");

    static async ValueTask<int> GetDiceRollAsync()
    {
        Console.WriteLine("Shaking dice...");

        int roll1 = await RollAsync();
        int roll2 = await RollAsync();

        return roll1 + roll2;
    }

    static async ValueTask<int> RollAsync()
    {
        await Task.Delay(500);

        int diceRoll = s_rnd.Next(1, 7);
        return diceRoll;
    }
}
```


