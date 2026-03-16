---
tags:
  - 面试
---
[[C (1).pdf|多线程]]
[[DOTNET.pdf|异步]]

## 线程

```c#
var thread1 = new Thread(Increment);
var thread2 = new Thread(Increment);

thread1.Start();
thread2.Start();

thread1.Join(); // 等待线程结束
thread2.Join();


thread1.Interrupt(); // 中断线程 --- 在 threa的中抛出一个异常
// 如果 while true 循环， 需要添加 time.sleep() 终端一下



// 原子操作

Interlocked.xxx

// 锁/队列等 顶层方法

Parallel.foreach/for/invoke
PLINQ.asParallel asOrdered

```


## 线程安全

```c#
// 原子操作 
Interlocked

// 锁
lock // Monitor
Mutex m = new Mutex();// 可以进程中共享
m.WaitOne();
m.ReleaseMutex();


// 可以进程共享 
// 信号量
Semaphore  sem = new Semaphore(3,3) // 线程同步 --- 可以释放多个资源 (3,3) -- 初始给出的资源，最大的资源数量
int HeavyJob(int input)
{
    semaphore.WaitOne(); // 需求一个
    Thread.Sleep(300);
    semaphore.Release(); // 释放
    return input;
}


WaitHandle //信号量 --- waitall 这种 task 任务
//ManualResetEvent
//AutoResetEvent

ReaderWriterLock // 读写锁


// 轻量型
SemaphoreSlim
ManualResetEventSlim
ReaderWriterLockSlim


// 轮子
线程安全的单例：Lazy
线程安全的集合类型：ConcurrentBag、 ConcurrentStack、ConcurrentQueue、 ConcurrentDictionary
阻塞集合：BlockingCollection
通道：Channe
原子操作：Interlocked
周期任务：PeriodicTimer
```


## 互斥锁 实现 读写锁

```c++
class 下··readwrite_lock
{
public:
    readwrite_lock()
        : read_cnt(0)
    {
    }
 
    void readLock()
    {
        read_mtx.lock();
        if (++read_cnt == 1)
            write_mtx.lock();
 
        read_mtx.unlock();
    }
 
    void readUnlock()
    {
        read_mtx.lock();
        if (--read_cnt == 0)
            write_mtx.unlock();
 
        read_mtx.unlock();
    }
 
    void writeLock()
    {
        write_mtx.lock();
    }
 
    void writeUnlock()
    {
        write_mtx.unlock();
    }
 
private:
    mutex read_mtx;
    mutex write_mtx;
    int read_cnt; // 已加读锁个数
};
```

## 异步编程

异步编程 ： **不阻塞** ， 可以单线程也可以多线程。

**多线程 ： 适合 CPU 密集操作，长期运行的任务**， 创建销毁开销大，不易于传参，返回
**异步 ： 适合 IO 密集操作 ， 适合短小的任务，可以避免线程阻塞，提高响应能力。**

Task基本概念

1. Task对象可以查看他的状态 `task.Status()` 返回一个 TaskStatus 类型的enum
2. `Task.Result` 返回 return 的结果
3. Task 有泛型，就有 result 

异步方法 `async Task`  async 主要的作用 使用来 在方法内部使用  await
- **async Task** 返回值啥都可以， Task xxx() 只能返回 Task
`async void ` 也会弄成状态机, **但是无法处理 异常！！！！！！！**。  **真实作用：对于异步函数对于事件的注册**

```c#
aysnc Task Main(){
	await FooAsync();
}

Task FooAsync(){
	return Task.Delay(200);
	return Task.CompletedTask();
}
```


`await` 的作用 ： 等待异步任务结束，并返回结果。

![Haz3h4fki6dwGXt.png](https://s2.loli.net/2024/08/19/Haz3h4fki6dwGXt.png)


在 Main 中 一开始 是 线程1， 但是结束的时候返回的是 线程8。

使用异步编程 其实就是一个状态机。 使用 MoveNext 切换状态

`task.GetAwaiter().GetResult()`


###  简单总结

- await 会暂时释放当前线程，使得线程可以执行其他工作，而不必阻塞线程知道异步操作完成 **不阻塞**。
- 阻塞分类
	- `Task.Wait Task.Result`  如果任务没有完成，则会阻塞当前线程，容易造成死锁。 `task.GetAwiater().GetResult()`
	- IO等同步操作
	- 耗时的操作
- 同步上下文。
	- configureAwait(false) --- 不同步上下文
	- TaskScheduler --- 可以控制上下文，以及优先级执行状态，调度方式
- 一发即忘 

### 方法

#### 1. 创建异步任务

```c#
Task.Run({同步方法}) // 传入异步匿名方法会被包装成 Task  / 在一个新的线程上执行代码
Task.Factory.StartNew() // 完备的 Run
//提供更多功能，比如 TaskCreationOptions.LongRunning
new Task + Task.Start() // 用的少
```

#### 2. 开启多个异步任务

不要 for 循环中使用 await.
Task.WhenAll()、Task.WhenAny()

```c#

await Task.WhenAll/WhenAny(tasks); // 一个列表
var outputs = tasks.Select(x => x.Result).ToArray();
```

#### 3. 关闭任务

- `CancellationTokenSource + CancellationToken`

这种方法结束 会抛出异常。

```c#
public static async Task GetDataAsync(int a)
{
	var cts = new CancellationTokenSource();

	try
	{

		var task = Task.Delay(10000, cts.Token);

		Thread.Sleep(1000);
		cts.Cancel();

		await task;
	}
	catch (TaskCanceledException)
	{

	}
	finally
	{
		cts.Dispose();
	}

}
```

- `OperationCanceledException & TaskCanceledException`

## 误区

- 可以不使用多线程，可以使用时间片轮转
- 不一定要加 Async ， 只是用来在函数内部使用 await
- `.Result` 不一定会阻塞线程

## 异步中的同步机制

- 所有的锁和信号量 
	- Monitor(lock)
	- Mutex
	- Semaphore
	- EventWaitHandle
- 轻量型的
	- SemaphoreSlim  (可以使用)
	- ManualResetEventSlim (不可以使用)
- 并发集合
	- ConcurrentBag/Stack/Queue
	- BlockingCollection
	- Channel （可以使用）


## 其他的一些技巧


### 1. 取消异步 CancellationTokenSource + CancellationToken

CancellationTokenSource 实现了 IDisposable 接口，需要释放

- **使用一个Task 取消另一个 Task**
- CancellationTokenSource 在创建的时候也可以传入一个参数，传入TimeSpan 就可以直接设置失效时间。 
- `cts.CancelAfter(3000)`
- **所有内置的  aysnc 方法  都可以传入 token 参数 的重载函数**
	- 因此我们自己写的异步函数并传入这个 CancellationTokenSource 参数。
	- 重载函数 可以直接 使用 `cts.None`
	- 也可使用 `xxxx(xxx, CancellationTokenSource? cts = null) { var token = cts ?? CancellationTokenSource.null}`


```c#
using System.Diagnostics;

var cts = new CancellationTokenSource();
var token = cts.Token;

var sw = Stopwatch.StartNew();

try
{

    var cancelTask = Task.Run(async () =>
    {
        await Task.Delay(3000);
        cts.Cancel();
    });

    await Task.WhenAll(Task.Delay(5000, token), cancelTask);
}
catch (TaskCanceledException e)
{
    Console.WriteLine(e);
}finally{
    cts.Cancel(); // !!!!!!!! 需要手动释放， 也可以使用 using 作用域
}

Console.WriteLine($"Task completed in {sw.ElapsedMilliseconds}ms");


// 第二种方法 直接设置 时间
var cts = new CancellationTokenSource(TimeSpan.FromSeconds(3));
ar cts = new CancellationTokenSource(3000);
```


**在同步方法中 实现 cancel 效果。**

```c#
return Task.Run(()=>{

	if(cts.IsCancellationRequested){
		cts.ThrowIfCancellationRequested();
	}

	while(true){
		if(cts.IsCancellationRequested){
			cts.ThrowIfCancellationRequested();
		}
	}


});
```


#### 1.1 取消对策

- 抛出异常
- 提前退出 `Task.FormCanceled<T>(cts)` 不推荐 直接 `return xxx;` 
	- 结合 `Task.IsCanceled` 
- 记得善后工作
	- 使用 委托进行善后

```c#
token.Register(()=> Console.WriteLine("xxxxx")); // 可以多次注册， 有先后顺序 用于善后工作


Task<string> FooAsync(CancellationToken cts){

    var task = new Task(()=>{});


    if(cts.IsCancellationRequested){
        return Task.FromCanceled<string>(cts);
    }

    return Task.FromResult("done");
}
```

#### 1.2 TaskCanceledException / OperationCanceledException

TaskCanceledException 继承自 OperationCanceledException


ThrrowIfCancellationRequested --- 抛出 OperationCanceledException 


ThrrowIfCancellationRequested 不仅仅可以用于异步，也可以用于同步的方法。

**Task.Run**  也可以传入 Token ， 但是使用的不是传入的而是外部的。 (因为传入的是一个回调函数!!!!!!!)，因此不能使用，只用用于提前判断。




https://www.bilibili.com/video/BV1Ya4y1X7WR/?spm_id_from=333.788&vd_source=8beb74be6b19124f110600d2ce0f3957