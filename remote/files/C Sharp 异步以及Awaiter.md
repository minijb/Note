---
tags:
  - Csharp
---


链式操作  : 

```c#
//无返回值转换前
public async void Example()
{
    Task t = Task.Run(() =>
    {
        Thread.Sleep(1000);
    });
    await t;
    //做一些工作
}
//无返回值转换后
public void Example()
{
    Task t = Task.Run(() =>
    {
        Thread.Sleep(1000);
    });
    t.ContinueWith(task => 
    {
        //做一些工作
    });
}

//有返回值转换前
public async void Example()
{
    Task<int> t = Task.Run<int>(() =>
    {
        Thread.Sleep(1000);
        return 1;
    });
    int res = await t;
    //使用res做一些工作
}
//有返回值转换后
public void Example()
{
    Task<int> t = Task.Run<int>(() =>
    {
        Thread.Sleep(1000);
        return 1;
    });
    t.ContinueWith(task => 
    {
        //使用task.Result做一些工作
    });
}
```

简单来说就是不适用 awaiter 而是使用 **链式操作**。 

异步的底层其实就是一个状态机

```c#
public static Task WorkAsync()
{
    return Task.Run(() => 
    {
        Thread.Sleep(1000);
        Console.WriteLine("Done!");
    });
}
public static async void Test()
{
    Console.WriteLine("步骤1");
    await WorkAsync();
    Console.WriteLine("步骤2");
    await WorkAsync();
    Console.WriteLine("步骤3");
}

public class TestAsyncStateMachine
    {
        public int _state = 0;
        public void Start() => MoveNext();
        public void MoveNext()
        {
            switch(_state)
            {
                case 0:
                    {
                        goto Step0;
                    }
                case 1:
                    {
                        goto Step1;
                    }
                default:
                    {
                        Console.WriteLine("步骤3");
                        return;
                    }
            }

        Step0:
            {
                Console.WriteLine("步骤1");
                _state = 1;
                WorkAsync().ContinueWith(t => this.MoveNext());
                return;
            }
        Step1:
            {
                _state = -1;
                Console.WriteLine("步骤2");
                WorkAsync().ContinueWith(t => this.MoveNext());
                return;
            }

        }
    }


public static void Test()
{
    new TestAsyncStateMachine().Start();
}



```


注意Test()方法返回的是void，这意味这调用方将不能await Test()。如果返回Task，这个状态机类是不能正确处理的，如果要正确处理，那么状态机在Start()启动后，必须返回一个Task，而这个Task在整个状态机流转完毕后要变成完成状态，以便调用方在该Task上调用的ContinueWith得以继续执行，而就Task这个类而言，它是没有提供这种方法（内部有，但没有对外暴露）来主动控制Task的状态的

从状态机中可以看到，主要使用到了Task中的ContinueWith这个函数，它的语义是在任务完成后，执行回调函数，通过回调函数拿到结果

语言开发者当然想到了，它被抽象成了一个Awaiter因此编译器要求await的类型必须要有GetAwaiter方法

- 必须继承INotifyCompletion接口，并实现其中的OnCompleted(Action continuation)方法
- 必须包含IsCompleted属性
- 必须包含GetResult()方法

改造后的状态机 

```c#
public class TestAsyncStateMachine
{
    public int _state = 0;
    public void Start() => MoveNext();
    public void MoveNext()
    {
        switch(_state)
        {
            case 0:
                {
                    goto Step0;
                }
            case 1:
                {
                    goto Step1;
                }
            default:
                {
                    Console.WriteLine("步骤3");
                    return;
                }
        }

    Step0:
        {
            Console.WriteLine("步骤1");
            _state = 1;
            TaskAwaiter taskAwaiter;
            taskAwaiter = WorkAsync().GetAwaiter();
            if (taskAwaiter.IsCompleted) goto Step1;
            taskAwaiter.OnCompleted(() => this.MoveNext());
            return;
        }
    Step1:
        {
            _state = -1;
            Console.WriteLine("步骤2");
            TaskAwaiter taskAwaiter;
            taskAwaiter = WorkAsync().GetAwaiter();
            if (taskAwaiter.IsCompleted) MoveNext();
            taskAwaiter.OnCompleted(() => this.MoveNext());
            return;
        }

    }
}
```


**简单总结**

- async/await只是表示这个方法需要编译器进行特殊处理，并不代表它本身一定是异步的。
- Task类中的GetAwaiter主要是给编译器用的

## Awaiter

```c#
namespace System.Runtime.CompilerServices
{
    /// <summary>
    /// Represents an operation that will schedule continuations when the operation completes.
    /// </summary>
    public interface INotifyCompletion
    {
        /// <summary>Schedules the continuation action to be invoked when the instance completes.</summary>
        /// <param name="continuation">The action to invoke when the operation completes.</param>
        /// <exception cref="System.ArgumentNullException">The <paramref name="continuation"/> argument is null (Nothing in Visual Basic).</exception>
        void OnCompleted(Action continuation);
    }
}
```


除此之外还必须包含IsCompleted属性和包含GetResult()方法。

注意OnCompleted的参数是一个Action委托，并且不出意外的话，委托里面总会有一个地方调用一个MoveNext()方法，它推动状态机到达下一个状态，然后执行下一个状态需要执行的代码。

，OnCompleted中的contination的主要目的是推动状态机的执行，也就是推动异步方法中await后面部分的代码执行。从这里看出，continuation的执行是受我们控制的，因此我们可以直接执行它，或是等待某个条件成熟然后执行它，我们可以把它放到线程池执行，也可以单独起一个线程执行。譬如，我们可以让await后面部分的代码直接在线程池上执行。


```c#
public static async Task AwaiterTest()
{
    Console.WriteLine($"是否是线程池线程？{Thread.CurrentThread.IsThreadPoolThread}");
    await default (SkipToThreadPoolAwaiter);
    Console.WriteLine($"是否是线程池线程？{Thread.CurrentThread.IsThreadPoolThread}");
}

static void Main(string[] args)
{
    _ = AwaiterTest();
    Console.ReadLine();
}

public struct SkipToThreadPoolAwaiter : INotifyCompletion
{
    public bool IsCompleted => false;
    public void GetResult() 
    {
        Console.WriteLine("调用GetResult以获取结果");
    }
    public void OnCompleted(Action continuation)
    {
        Console.WriteLine("调用OnCompleted，把Await后面部分要执行的代码传递过来（传递MoveNext，以推动状态机流转）");
        ThreadPool.QueueUserWorkItem(state =>
        {
            Console.WriteLine("开始执行Await后面部分的代码");
            continuation();
            Console.WriteLine("后面部分的代码执行完毕");
        });
        Console.WriteLine("返回调用线程");
    }

    public SkipToThreadPoolAwaiter GetAwaiter()
    {
        Console.WriteLine("获得Awaiter");
        return this;
    }
}
```

特别注意一下，第五步说明可能有点疑惑，怎么第六步不是打印是否是线程池线程？原因是部分awaiter是有返回值的，在执行await后面部分的代码时，会首先调用GetResult()以获取结果。这对编译器改造异步方法来说是一个固定的模式（上篇文章没有体现这一步）。  
  把Awaiter改成有返回值尝试。

```c#
public static async Task AwaiterTest()
{
    Console.WriteLine($"是否是线程池线程？{Thread.CurrentThread.IsThreadPoolThread}");
    var res = await default (SkipToThreadPoolAwaiter);
    Console.WriteLine($"结果是{res}");
    Console.WriteLine($"是否是线程池线程？{Thread.CurrentThread.IsThreadPoolThread}");
}

static void Main(string[] args)
{
    _ = AwaiterTest();
    Console.ReadLine();
}

public struct SkipToThreadPoolAwaiter : INotifyCompletion
{
    public bool IsCompleted => false;
    public int GetResult() 
    {
        Console.WriteLine("调用GetResult以获取结果");
        return 1;
    }
    public void OnCompleted(Action continuation)
    {
        Console.WriteLine("调用OnCompleted，把Await后面部分要执行的代码传递过来（传递MoveNext，以推动状态机流转）");
        ThreadPool.QueueUserWorkItem(state =>
        {
            Console.WriteLine("开始执行Await后面部分的代码");
            continuation();
            Console.WriteLine("后面部分的代码执行完毕");
        });
        Console.WriteLine("返回调用线程");
    }

    public SkipToThreadPoolAwaiter GetAwaiter()
    {
        Console.WriteLine("获得Awaiter");
        return this;
    }
}
```


前面说到，我们可以控制continuation的执行，那如果当前线程有同步上下文（SychronizationContext），我们是不是可以放到同步上下文中执行？TaskAwaiter是会这么做的，如果你不想它使用同步上下文，你可以在Task实例上调用ConfigureAwait(false)，它表面后面部分的代码将不会使用同步上下文执行。  

另外说一下Task.Yield()这个Awaiter，他的行为是捕捉同步上下文，如果有，则会放到同步上下文中执行，如果没有，则会放到线程池中执行。在窗体程序中，有时候你打开一个模态对话框，会导致主窗体部分的动画没有反应，在模态对话框关闭之后，才会反应。原因是模态对话框阻塞了主窗体的消息循环，也就是阻塞了主线程，如果想让动画先完成，然后再打开模态对话框，则可以在打开模态对话框之前，Await Task.Yield()，这也对应了它的意思，让渡之意。  

后面文章还会说明同步上下文具体是什么、异步代码中使用同步代码会导致死锁的本质原因、如何实现类似Task的类，并且怎么与Async/await这套机制搭配使用等知识。


https://www.cnblogs.com/walterlv/p/10236529.html
https://www.cnblogs.com/hkfyf/p/15949528.html