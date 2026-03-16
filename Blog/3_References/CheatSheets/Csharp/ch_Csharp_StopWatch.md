
https://learn.microsoft.com/en-us/dotnet/api/system.diagnostics.stopwatch?view=net-9.0

主要用于计时

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


**快速开始一个 stopWatch**

```c#
Stopwatch stopWatch = StopWatch.StartNew();
```


获取时间

|                                                                                                                                                                                    |                                                                                                                                                           |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Elapsed](https://learn.microsoft.com/en-us/dotnet/api/system.diagnostics.stopwatch.elapsed?view=net-9.0#system-diagnostics-stopwatch-elapsed)                                     | Gets the total elapsed time measured by the current instance.                                                                                             |
| [ElapsedMilliseconds](https://learn.microsoft.com/en-us/dotnet/api/system.diagnostics.stopwatch.elapsedmilliseconds?view=net-9.0#system-diagnostics-stopwatch-elapsedmilliseconds) | Gets the total elapsed time measured by the current instance, in milliseconds.                                                                            |
| [ElapsedTicks](https://learn.microsoft.com/en-us/dotnet/api/system.diagnostics.stopwatch.elapsedticks?view=net-9.0#system-diagnostics-stopwatch-elapsedticks)                      | Gets the total elapsed time measured by the current instance, in timer ticks.                                                                             |
| [IsRunning](https://learn.microsoft.com/en-us/dotnet/api/system.diagnostics.stopwatch.isrunning?view=net-9.0#system-diagnostics-stopwatch-isrunning)                               | Gets a value indicating whether the [Stopwatch](https://learn.microsoft.com/en-us/dotnet/api/system.diagnostics.stopwatch?view=net-9.0) timer is running. |

