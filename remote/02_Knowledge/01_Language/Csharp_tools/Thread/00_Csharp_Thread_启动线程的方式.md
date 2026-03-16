
## 1. 最简单的方式

```c#
Thread t = new Thread(() =>
    {
        Console.WriteLine("开始下载" + Thread.CurrentThread.ManagedThreadId);
        Thread.Sleep(2000);
        Console.WriteLine("下载完成");
    });
t.Start();


public static void Main(string[] args)
{
	Thread t1;
	Thread t2;
	t1 = new Thread(SetInfo1);
	t2 = new Thread(SetInfo2);
	t1.Start();
	//线程睡眠
	//t1.Join(1000);
	//挂起线程
	t1.Suspend();
	//继续执行线程
	t1.Resume();
	//结束线程
	//t1.Abort();

	t2.Start();
	Console.ReadKey();
}

```


## 2. 使用 Task 启动线程

```c#
public class Program
{
	public static void Main(string[] args)
	{
		Task task = new Task(DownLoadFile);
		task.Start();
		Console.ReadKey();
	}
	static void DownLoadFile()
	{
		Console.WriteLine($"开始下载,线程ID:{Thread.CurrentThread.ManagedThreadId}");
		Thread.Sleep(500);
		Console.WriteLine("下载完成!");
	}
}
```

### 3. 使用线程池

```c#
 public class Program
{
	public static void Main(string[] args)
	{
		ThreadPool.QueueUserWorkItem(new WaitCallback(TestThreadPool), new string[] { "test" });
		Console.ReadKey();
	}
	public static void TestThreadPool(object state)
	{
		string[] arry = state as string[];//传过来的参数值
		int workerThreads = 0;
		int CompletionPortThreads = 0;
		ThreadPool.GetMaxThreads(out workerThreads, out CompletionPortThreads);
		Console.WriteLine(DateTime.Now.ToString() + "---" + arry[0] + "--workerThreads=" + workerThreads + "--CompletionPortThreads" + CompletionPortThreads);
	}
}
```