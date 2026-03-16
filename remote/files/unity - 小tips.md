---
tags:
  - unity
---
## UniTask --- 如果跑的东西不需要用到原生的Unity组件，可以使用 Task.RunOnThreadPool

当需要利用到多线程处理东西，同时对象和原生Unity组件交叉不大，可以使用
`RunOnThreadPool` . 

如果想要切回原始线程操作一些东西 可以使用 

```c#
  UniTask.SwitchToMainThread().GetAwaiter().OnCompleted(()=>{
	try
	{
		action();
	}
	finally
	{
		mutex.Set();
	}
});
mutex.WaitOne();
#endif
```


