---
tags:
  - thread
---
## 创建

```cpp
// 函数

void xxx(){

}

int main(){
	std::thread thread1(xxx, {参数});
	bool canJoin = thread1.joinable();
	// thread1.detach(); // 线程分离 主线程结束，子进程继续运行
	
	if(canJoin){
		thread1.join();//阻塞
	}
	
	
	return 0;
}
```

主程序如果没有 join 不会等待子程序，而是照常运行。

> 四种创建 函数的方式
> 1. 普通函数
> 2. lambda
> 3. 成员函数
> 4. 函数对象 --- 类重载 ()
## 常见错误

- 通过 `std::ref(x)` 传递参数，但是x为临时变量，报错
- 局部变量/线程使用的变量已经被释放，但是线程没有结束
- 传递指针，我们释放了，但是 thread 不知道。可能出错。 --- 类同理
- 类成员函数作为入口函数，类对象被提前释放。 --- 推荐使用智能指针。
- 入口函数 是 类的私有函数。 --- 将 线程启动封装到函数并 使用 友元

## 互斥量

```cpp
std::mutex mtx;

int a = 0;

void func(){
	mtx.lock();
	a += 1;
	mtx.unlock();
}

```

## lock_guard  unique_lock


lock_guard -- 互斥量封装

- 构建函数被调用的时候，自动锁定
- 析构函数被调用的时候，自动解锁
- `std::lock_gurad` 对象不能复制或者移动，智能在局部作用域中使用

```cpp
std::mutex mtx;

void func(){
	std::lock_guard<std::mutex> lg(mtx);
	// .....
}
```


`std::unique_lock`

具有更多的操作：延迟加锁，条件变量，超时。

方法

- `lock`  尝试对互斥量进行加锁操作，**如果当前互斥量已经被其他线程持有，当前就会被阻塞**
- `try_lock`  相同，不阻塞，但是返回 try/false
- `try_lock_for({chrono} -- real time)` 尝试加锁，如果被持有，则阻塞 --- 直到互斥量被成功加锁，或者超过指定时间。
- `try_lock_until({chrono} -- real time)` .....。。。 超过指定时间点
- `unlock` 解除所

构造函数

默认自动加锁

```cpp
std::timed_mutex mtx;

unique_lock(mtx, std::defer_lock) // 不加锁
```

## call_once

用于单例类在多线程中的使用。

在 饿汉模式 中，如果两个线程同时 getInstance 此时，会被new 多次，违反了 单例模式的定义

```cpp
static Log* log = nullptr;
static std::once_flag = once;


class Log{
public:
...
...

	static Log& GetInstance(){
		std::call_once(once, init);
		return *log;
	}
	static void init(){
		if(!log) log = new Log();
	}
	
}
```

`call_once ` 只能在多线程中使用，不能直接使用


## condition_variable

通常和线程池结合使用

使用步骤

- 创建一个  std::condition_variable 对象
- 创建 std::mutex 对象
- 在需要等待条件变量的地方
	- `std::unique_lock<std::mutex>` 
	- 并调用 `std::condition_variaable::wait()/wait_for()/wait_until()`
- 在其他线程中需要通知线程的时候， 调用 `std::condition_varibale::notify_one()/notify_all()`


基本的生产者消费者模型

```cpp
#include <chrono>
#include <condition_variable>
#include <iostream>
#include <mutex>
#include <ostream>
#include <queue>
#include <string>
#include <thread>

std::queue<int> g_queue;
std::condition_variable g_cv;

std::mutex mtx;

void Producer() {
  for (int i = 0; i < 10000; i++) {
    std::unique_lock<std::mutex> lock(mtx);
    g_queue.push(i);
    g_cv.notify_one(); // 通知取
    std::cout << "task : " << i << " in -" << std::endl;
  }

  std::this_thread::sleep_for(std::chrono::microseconds(100));
}

void Consumer() {
  while (1) {
    std::unique_lock<std::mutex> lock(mtx);

    // 队列空， 则等待
    g_cv.wait(lock, []() { return !g_queue.empty(); });

    int value = g_queue.front();
    g_queue.pop();

    std::cout << "task : " << value << " out +" << std::endl;
    std::this_thread::sleep_for(std::chrono::microseconds(200));
  }
}

int main() {
  std::thread t1(Producer);
  std::thread t2(Consumer);
  std::thread t3(Consumer);
  std::thread t4(Consumer);
  std::thread t5(Consumer);

  t1.join();
  t2.join();
  t3.join();
  t4.join();
  t5.join();

  std::cout << "task end!" << std::endl;

  return 0;
}

```


## 线程池

```cpp

#include <chrono>
#include <condition_variable>
#include <functional>
#include <iostream>
#include <mutex>
#include <queue>
#include <string>
#include <thread>
#include <utility>
#include <vector>

class ThreadPool {
public:
  ThreadPool(int numThreads) : stop(false) {
    for (int i = 0; i < numThreads; i++) {

      thread_list.emplace_back([this] {
        while (1) {
          std::unique_lock<std::mutex> lock(mtx);
          c_var.wait(lock, [this] { return !tasks.empty() || stop; });
          if (stop && tasks.empty())
            return;

          // get and run task from queue
          std::function<void()> task(std::move(tasks.front()));
          tasks.pop();
          lock.unlock();
          task();
        }
      });
    }
  }

  ~ThreadPool() {
    {
      std::unique_lock<std::mutex> lock(mtx);
      stop = true;
    }

    c_var.notify_all();

    for (auto &t : thread_list) {
      t.join();
    }
  }

  template <class F, class... Args> void add_task(F &&f, Args &&...args) {
    std::function<void()> task =
        std::bind(std::forward<F>(f), std::forward<Args>(args)...);
    {
      std::unique_lock<std::mutex> lock(mtx);
      tasks.emplace(std::move(task));
    }
    c_var.notify_one();
  }

private:
  std::vector<std::thread> thread_list;
  std::queue<std::function<void()>> tasks;

  std::mutex mtx;
  std::condition_variable c_var;

  bool stop;
};

int main() {
  ThreadPool pool(4);

  for (int i = 0; i < 10; i++) {
    pool.add_task([i] {
      std::cout << "task : " << i << std::endl;
      std::this_thread::sleep_for(std::chrono::seconds(1));
    });
  }
}

```


https://www.bilibili.com/video/BV1d841117SH?p=10&vd_source=8beb74be6b19124f110600d2ce0f3957