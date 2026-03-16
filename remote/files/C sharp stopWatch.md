---
tags:
  - Csharp
---
## 最简单的使用

```c#
Stopwatch stopWatch = new Stopwatch();
stopWatch.Start();
Thread.Sleep(10000);
stopWatch.Stop();
// Get the elapsed time as a TimeSpan value.
TimeSpan ts = stopWatch.Elapsed;

// Format and display the TimeSpan value.
string elapsedTime = String.Format("{0:00}:{1:00}:{2:00}.{3:00}",
	ts.Hours, ts.Minutes, ts.Seconds,
	ts.Milliseconds / 10);
Console.WriteLine("RunTime " + elapsedTime);
```

查看运行时间

- `Elapsed`   [TimeSpan](https://learn.microsoft.com/zh-cn/dotnet/api/system.timespan?view=net-8.0)
- `ElapsedMilliseconds`  int64


## 常用方法

- Reset() : 重置0
- Restart()
- StartNew() 初始新的Stopwatch ，置0并运行
- Stop()
