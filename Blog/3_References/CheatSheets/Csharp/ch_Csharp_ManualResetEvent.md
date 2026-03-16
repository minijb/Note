
ManualResetEvent是C#中一个比较常用的工具，可用于线程间通信，实现一种信号量的功能

主要特点：

1. **两种状态**：`ManualResetEvent`具有两种状态 - 信号和非信号。调用 `Set()` 方法将事件设置为信号状态，调用 `Reset()` 方法将事件设置为非信号状态。
    
2. **阻塞或释放多个线程**：在事件为非信号状态时，调用 `WaitOne()` 方法的线程将被阻塞。当事件转换为信号状态时，所有等待该事件的线程都将继续执行。
    
3. **手动重置**：与 `AutoResetEvent` 不同，`ManualResetEvent` 不会在释放一个等待的线程后自动重置为非信号状态。相反，它会保持信号状态，直到明确调用 `Reset()` 方法。
    
4. 跨线程通信：`ManualResetEvent` 可以用于不同线程之间的通信。一个线程可以等待一个事件，而另一个线程可以设置或重置该事件。
    
5. **简单易用**：`ManualResetEvent` 类的 API 非常简单直接，只需要几个方法就能实现线程间的有效同步。
    
6. **线程池兼容**：`ManualResetEvent` 可以与 .NET 的线程池 (`ThreadPool`) 结合使用，以便更有效地管理和控制线程资源。
    

#### 优点

1. 线程同步：`ManualResetEvent` 提供了一种有效的方式来同步多个线程。你可以使用它来确保一个或多个线程在其他工作完成之前不会继续进行。
    
2. **灵活性**：与 `AutoResetEvent` 相比，`ManualResetEvent` 允许多个等待的线程在事件被设为信号状态后同时继续进行。这是因为 `ManualResetEvent` 在被手动重置之前会保持信号状态，而 `AutoResetEvent` 在释放一个等待的线程后会自动回到非信号状态。
    

#### 缺点

1. **手动控制**：`ManualResetEvent` 需要手动重置，这可能会导致错误，例如如果忘记重置事件，那么所有调用 `WaitOne()` 的线程将立即继续执行，即使预期应该阻塞他们。
    
2. **无法传递额外信息**：`ManualResetEvent` 只提供二元（信号/非信号）的同步机制，并不能传递更为复杂的状态信息。对于需要传递更多数据或状态信息的场景，可能需要使用更为复杂的同步结构如 `Monitor`, `Mutex`, `Semaphore` 等。


```c#
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;

namespace ThreadTest
{
    class Program
    {
        static void Main(string[] args)
        {
            new ProductAndCostTester();
        }
    }

    /// <summary>
    /// 生产消费模型
    /// </summary>
    public class ProductAndCostTester
    {
        /// <summary>
        /// 生产线1线程
        /// </summary>
        private Thread _producterThread1;
        /// <summary>
        /// 生产线2线程
        /// </summary>
        private Thread _producterThread2;
        /// <summary>
        /// 消费线线程
        /// </summary>
        private Thread _costerThread;
        /// <summary>
        /// 产品列表
        /// </summary>
        private List<int> _goodList;
        /// <summary>
        /// ManualResetEvent实例
        /// </summary>
        private ManualResetEvent _mre;

        public ProductAndCostTester()
        {
            _goodList = new List<int>();

            _mre = new ManualResetEvent(false);//false初始化状态为无信号，将使WaitOne阻塞

            _producterThread1 = new Thread(Product1);
            _producterThread1.Name = "Productor1";
            _producterThread1.Start();

            _producterThread2 = new Thread(Product2);
            _producterThread2.Name = "Productor2";
            _producterThread2.Start();

            _costerThread = new Thread(Cost);
            _costerThread.Name = "Costor";
            _costerThread.Start();
        }

        /// <summary>
        /// 生产线1
        /// </summary>
        void Product1()
        {
            while (true)
            {
                Console.WriteLine(Thread.CurrentThread.Name + ":" + DateTime.Now.ToString("HH:mm:ss"));
                for (int i = 0; i < 3; i++)
                {
                    _goodList.Add(1);
                }
                _mre.Set();//表示有信号了，通知WaitOne不再阻塞

                Thread.Sleep(8000);
            }
        }

        /// <summary>
        /// 生产线2
        /// </summary>
        void Product2()
        {
            while (true)
            {
                Console.WriteLine(Thread.CurrentThread.Name + ":" + DateTime.Now.ToString("HH:mm:ss"));
                for (int i = 0; i < 6; i++)
                {
                    _goodList.Add(1);
                }
                _mre.Set();//表示有信号了，通知WaitOne不再阻塞

                Thread.Sleep(10000);
            }
        }

        /// <summary>
        /// 消费线
        /// </summary>
        void Cost()
        {
            while (true)
            {
                if (_goodList.Count > 0)
                {
                    Console.WriteLine("Cost " + _goodList.Count + " at " + DateTime.Now.ToString("HH:mm:ss"));
                    _goodList.Clear();
                    _mre.Reset();//重置为无信号了，使WaitOne可以再次阻塞
                }
                else
                {
                    Console.WriteLine("No cost at " + DateTime.Now.ToString("HH:mm:ss"));
                    _mre.WaitOne();//如果没有可消费的产品，即无信号，则会阻塞
                }
            }
        }
    }
}s
```
