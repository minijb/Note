

## 1. Thread 线程


```c#
int count = 0;
var thread1 = new Thread(ThreadMethod);
var thread2 = new Thread(ThreadMethod);


thread1.Start();
thread2.Start();

thread1.Join();
thread2.Join();

Console.WriteLine(count);

void ThreadMethod()
{
    for (int i = 0; i < 10000; i++)
    {
        count++;
    }
}
```


**使用同步**

```c#
lock (obj)
{
	count++;
}
```


需要注意的是 部分集合操作 也不是原子操作， 需要在锁的范围内进行操作


## 2. 线程的创建,中止,挂起,IsBackGround

**创建**

- 函数
- lambda 表达式
- 创建对象， 传入对象的方法 ---  好处是线程可以使用对象的所有属性

```c#
class Program
{
    public class Download
    {
        private int Id;
        private string Name;
        public Download(int id, string name)
        {
            Id = id;
            Name = name;
        }
        public void DownloadFile()
        {
            Console.WriteLine("DownLoad Begin " + "ID: " + Id + " Name: " + Name);
            Thread.Sleep(1000);
            Console.WriteLine("DownLoad End");              
        }
    }
    static void Main(string[] args)
    {
        Download download = new Download(1, "人民日报");
        Thread thread = new Thread(download.DownloadFile);
        thread.Start();
        Console.WriteLine("Main");
        Console.ReadKey();
    }
}
```

- 使用匿名方法  --- 好处是可以捕获变量
- Task
- Parallel

> `Thread.Start`  可以传参

**创建的时候添加一些参数**

```c#
var thread1 = new Thread(xxx){
	IsBackground = true,
	Priority = ThreadProxxx
}
```

**中止**

`Thread.Interrupt`   --- 中断线程   --- 抛出异常， 只要函数内部拿到 ThreadInterruptedException  就会离开线程

```c#
   public void ThreadMethod()
    {
        Console.WriteLine("newThread is executing ThreadMethod.");
        while(!sleepSwitch)
        {
            // Use SpinWait instead of Sleep to demonstrate the 
            // effect of calling Interrupt on a running thread.
            Thread.SpinWait(10000000);
        }
        try
        {
            Console.WriteLine("newThread going to sleep.");

            // When newThread goes to sleep, it is immediately 
            // woken up by a ThreadInterruptedException.
            Thread.Sleep(Timeout.Infinite);
        }
        catch(ThreadInterruptedException e)
        {
            Console.WriteLine("newThread cannot go to sleep - " +
                "interrupted by main thread.");
        }
    }
```

**等待**

`Thread.Join`  等待

**挂起和恢复**

不推荐使用，  推荐使用锁

## 3. 使用csharp 自带方法实现并行操作


- Parallel  
- PLINQ

**Parallel**
1.1、Parallel.For 使用  
1.2、Parallel.ForEach 使用  
1.3、Parallel.Invoke 使用  
1.4、ParallelOptions 选项配置  
1.5、ParallelLoopResult 执行结果  
1.6、ParallelLoopState 提前结束  
1.7、Parallel的使用场景分析

**PLINQ**

AsParallel， AsSequential
AsOrdered

## 4. 异步竞争

#TODO 

### 原子操作

Interlocked  --- 针对基础类型  

### 锁和信号量

- lock   Monitor （lock 底层使用  Monitor）
- Mutex  -- 互斥锁  可进程之间共享
- Semaphore  信号量  --- 主要用于控制同时进行的数量
- WaitHandle  同信号量   --- 用于生产者和消费者
	- ManualResetEvent 
	- AutoResetEvent  
	- **区别** ： **1**. 如果有多个线程都在用WaitOne等待信号量，那么每次Set()，auto只会释放一个WaitOne，而manual会全部释放 **2**. 调用WaitOne后，auto会自动调用Reset()方法，而manual则会保持开放
	- 相当于进入后自动关门
- ReaderWriterLock

### 轻量型

- SemaphoreSlim
- ManualResetEventSlim
- AutoResetEventSlim
- ReaderWriterLockSlim

轻量型 +  适用于异步版本

### Csharp  提供的轮子

- 线程安全的单例  ： Lazy
- 线程安全的集合 ： Concurrentxxx
- 阻塞集合 BlockingCollection
- 通道 Channel
- 原子操作  Interlocked
- 周期任务  PeriodicTimer

