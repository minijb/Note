
##  1. Task

- 内部包含很多状态 
	- 最基本的就是 Status
- 可以得到 result ， 查看是否完成， 是否得到值
- 默认使用线程池

## 2. async await task 几个规则

- async 的作用是  可以使用 await 
- await 的作用是 等待异步任务结束， 并获得结果
- async + await  将方法包装成 一个状态机，  await 就是一个检查点
	- 底层自动帮我们换线程了
- Task.result  --- 同步的获取方法 --- 不推荐
- async  并没有改变返回值！！！！


#TODO  TaskAwaiter


async void  同样会被包装成状态机但是没有返回凭证。  --- 同时外部无法接收报错

### 3. 阻塞

- `Task.Wait()`  `Task.Result` -- result 如果有结果了 则不阻塞直接返回， 没有则阻塞
- `Task.GetAwaiter().GetResult()`  也是阻塞
- Task.Delay()  Thread.Sleep()
- 繁重的任务
- IO操作

## 4. 同步上下文

> Task.ConifgureAwait(True)  --- await 之后的代码  返回原始的线程   --- UI常用！！！！
> false 不返回


TaskScheduler  --
- 控制 Task 的调度方式 和运行线程
- 优先级，上下文， 执行状态


## 5. 异步任务

### 创建异步任务

- Task.Run   --- 函数不需要返回 Task --- 会自己包装
- Task.Factory.StartNew --- 升级版 Task.Run 有很多重载
	- Task.CreationOptions.LongRunning
- Task.Start()  用的少

### 同时开启多个异步任务

- 一个一个 await 
- 同时开启多个，await  Task.Whenall ,  然后 `tasks.select(x=>x.result).ToArray()`

### 取消任务

**最基础的方法**

```c#
var cts = new CanccellationTokenSource();
Task.Delay(1000, cts.Token)



try{
xxx
cts.Cancel()
}catch(TaskCanceledException){

}
finally
{
	cts.Dispoase();
}

```


