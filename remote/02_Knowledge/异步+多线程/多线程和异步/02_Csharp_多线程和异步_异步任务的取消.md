
## 1. 两种取消方法

### 1.1  使用  CancellationTokenSource

```c#
var cts = new CancellationTokenSource();
var token = cts.Token;

cts.Cancel();
```


取消的本质是抛出一个异常。 `TaskCanceledException`   同理  --- Thread.Interupt

**注意** ： 实现了 IDisposable 接口可以被释放

```c#
try{
}catch( exception){
}finally{
	cts.Dispose();
}


// 也可以使用 using

using xxxx {
}
```


### 1.2 使用 TimeSpan 自动取消

有三种方法

```c#
var cts = new CancellationTokenSource(3000);
var cts = new CancellationTokenSource(TimeSpan.FromSeconds(1));
cts.CancelAfter(300);
```


## 2. 查看是否已经取消

```c#
token.IsCancellationRequested
```


```ad-tip
title:注意
推荐 所有异步方法都加入  token 的坂本
```

```ad-note
title:异步的同步等待也可以传入 token
~~~c#
var sem = new SemaphoreSlim();
sem.WaitAsync(token);
~~~
```


经常可以用来作为超时检测。

## 3. 重载 的推荐方式

```c#
async Task Foo(CancellationToken  xxx)

async Task Foo(){
	await Foo(CancelliationToken.None);
}


// 或者可以使用 ？
async Task Foo(int delay, CancellationToken? token = null){
	var cts = token ?? CancellationToken.None;
	await Task.Delay(delay, cts);
}
async Task Foo(int delay, CancellationToken token = default){
	await Task.Delay(delay, token ?? );
}
```


## 4. 使用同步上下文中的 token

```c#
Task FooAysnc(CancellationToken cts)
{
	return Task.Run(() =>
	{
		if (cts.IsCancellationRequested)
		{
			cts.ThrowIfCancellationRequested();
		}

		while (!cts.IsCancellationRequested)
		{
			Thread.Sleep(1999);
		}
	});
}
```


```ad-note
title:主动抛出异常
~~~c#
cts.ThrowIfCancellationRequested
~~~
```


## 5. 取消的对策

- 抛出异常
- 提前返回 `return Task.FormCanceled<string>("")`   --- 一个 Task.IsCancel 的 Task


## 6. 取消的善后

```c#
token.Register(()=> Console.WriteLine("Cancelled"));

// 或者 使用 finally 进行善后
```

后注册  先运用


## 7. Task.Run 中的 token 参数的作用


只有一个 ： 用来在一开始的时候 判断 是否引进取消，  已经取消了就不使用线程了

