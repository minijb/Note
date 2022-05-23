## 1. 线程queue

线程抢占资源，只能让其串行

1. 互斥锁
2. 队列

```python
q = queue.Queue(3)
q.put(1)
q.put(1)
q.put(1)
print(q.get(timeout=2))#阻塞两秒  如果还是没有值那么就报错
```

栈

```python
q= queue.LifoQueue(3)
q.put(x)
print(q.get())
```

优先级队列

```python
q= queue.PriorityQueue(3)
q.put((5,'xxx'))#前者为优先级
print(q.get())#先取出优先级高的
```

## 2. 时间event

开启两个线程，一个线程运行到中间的某一个阶段触发另一个线程执行

- 增加了两个线程的耦合性



没有event

```python
from  threading import Thread,current_thread
flag = false
def check():
    time.sleep(3)
    global flag
    flag = True

def connnect():
    while :
        print('wait')
        time.sleep(0.5)
        if flag:
            print('connected')
            break
            
t1 = Thread(target=check)
t2= Thread(target=connect)
t1.start()
t2.start()
```

使用event

```python
from  threading import Thread,current_thread,Event

import time

event = Event()

def check():
    time.sleep(3)
    event.set()

def connect():
    print('wait')
    event.wait()#会阻塞
    print('connected')

t1 = Thread(target=check)
t2= Thread(target=connect)
t1.start()
t2.start()

```

- wait(n) 会沉睡n秒如果没有遇到set ， 那么就会直接运行

- 其他方法
- `event.is_set()`查看是否set过

## 3. 协程

一个线程并发的处理任务，把控cpu，线程不由操作系统切换，而是自己来切换

- 优势：
  - 开销小
  - 速度快
  - 长期霸占cpu

- 缺点
  - 只是单线程
  - 如果阻塞会阻塞整个线程

```python
from greenlet import greenlet

def eat(name):
    print(f"{name} eat1")
    g2.switch('two')
    print(f"{name} eat")
    g2.switch()

def play(name):
    print(f"{name} play1")
    g1.switch()
    print(f"{name} play2")


g1=greenlet(eat)
g2=greenlet(play)

g1.switch('one')

```

### gevent

```python
import gevent
from gevent import monkey
monkey.patch_all()#阻塞的打赏标记

def eat(name):
    print(f"{name} eat1")
    gevent.sleep(2)
    print(f"{name} eat")

def play(name):
    print(f"{name} play1")
    gevent.sleep(1)
    print(f"{name} play2")


g1=gevent.spawn(eat,'one')
g2=gevent.spawn(play,'two')

g1.join()
g2.join()

```

