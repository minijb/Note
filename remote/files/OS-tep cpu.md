---
tags:
  - OS
---
fork : 

- 父 : 返回创建的子pid
- 子 : 返回 0

****

`pid_t wait(int *status)` 等待子进程完成 :

如果不考虑结束状态值, 则参数 status 可以设成NULL.

- 成功：返回子pid
- 失败：返回 -1

****

`pid_t waitpid(pid_t pid, int *status, int options);` 类似


****

exec 让进程执行不同的程序

```c
// child (new process)
printf("hello, I am child (pid:%d)\n", (int) getpid());
char *myargs[3];
myargs[0] = strdup("wc");   // program: "wc" (word count)
myargs[1] = strdup("p3.c"); // argument: file to count
myargs[2] = NULL;           // marks end of array
execvp(myargs[0], myargs);  // runs word count
printf("this shouldn't print out");
```

exec 从可执行文件(wc 计数)中加载数据，并用它**覆写**自己的代码段，堆，栈等其他空间。然后操作系统重新执行这个程序，通过 arg 将参数传递给进程。

因此，exec 没有新建进程。而是将程序进行替换

### 重定向的底层 

```c
// child: redirect standard output to a file
close(STDOUT_FILENO); 
open("./p4.output", O_CREAT|O_WRONLY|O_TRUNC, S_IRWXU);

// now exec "wc"...
	char *myargs[3];
	myargs[0] = strdup("wc");   // program: "wc" (word count)
	myargs[1] = strdup("p4.c"); // argument: file to count
	myargs[2] = NULL;           // marks end of array
	execvp(myargs[0], myargs);  // runs word count
```

关闭 STDOUT_FILENO，打开文件描述符 `./p4.output`中 : 此时运行 wc 命令，会寻找文件描述符，此时会将数据写入到文件描述符。

管道 pipe() 类似。

## HOMEWORK 5

vfork -- 当子进程运行结束后再运行父进程

exec族函数， 需要注意的是：只是参数不同，其他相同

**循环创建多个进程的时候**

注意：

![[fork.excalidraw]]



example : 

```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
  int p[2];
  int pids[2];
  char buf[256];
  if (pipe(p) < 0) {
    fprintf(stderr, "pipe create error");
    exit(1);
  }

  int i = 0;
  for ( i = 0; i < 2; i++) {
    pids[i] = fork();

    if (pids[i] < 0) {
      fprintf(stderr, "fork error!");
      exit(1);
    } else if (pids[i] == 0) {
	    printf("i am child %d, %d loop time\n",getpid(), i);
	    // break;
    }
  }

  waitpid(pids[0], NULL, 0);
  waitpid(pids[0], NULL, 0);

  return 0;
}

// OUTPUT no break
i am child 33157, 0 loop time
i am child 33158, 1 loop time
i am child 33159, 1 loop time
// OUTPUT with break
i am child 33648, 0 loop time
i am child 33649, 1 loop time

```


## 进程调度

主要指标： 周转时间(完成时间-到达时间)，响应时间

1. FIFO ， SJF， STCF 最短完成时间有限，RR（IO密集可能抢占CPU）

### **多级反馈队列**

简单思想 ： 在运行过程中学习， 利用工作历史预测它的未来行为。

**旧规则**
规则1 ： 根据优先级大小运行
规则2 ： 如果优先级相同则轮转运行
规则3 ： 工作进入的时候，放在最高优先级队列中
~~规则4a:  工作时间片完整用完之后，**降低优先级**~~  
~~短工作快速完成，长工作会降低优先级~~
~~规则4b： 如果在时间片内主动释放cpu **则优先级不变**~~
~~IO密集任务不会降低优先级~~
规则4 ： 一旦工作用完了某一层中的时间额度(无论放弃几次) 就降低优先级
<span style="background:rgba(136, 49, 204, 0.2)">防止愚弄(每次刚好用完时间片，调用IO)</span>
规则5 : 经过一段时间，将所有工作放入最高优先级
<span style="background:rgba(240, 107, 5, 0.2)">防止饥饿问题</span>

基础设置

60层队列
时间片长度 20ms - 几百ms
每1s所有提升优先级


### 比例份额

- 使用随机数+彩票份额的方式进行调度
- 基于步长的方式 (x/彩票) --- 需要全局状态

P97 -- 内存管理 api 可以看看书。

### api

### 地址转换

MMU ： 内存管理单元  -- 负责地址转换的单元 （物理转换）

动态重定位 ： 两个寄存器 base（基址） bound（界限）

操作系统需要做的

1. 内存管理 ： freeList， 内存空间的分配
2. 基址管理 ： 保存和恢复 base and bound 寄存器
3. 异常处理 ： 越界发生异常(硬件) --- 在开机的时候就处理陷阱表

**进程启动时间表**

![GDvcCFPHitA3dXx.png](https://s2.loli.net/2025/01/06/GDvcCFPHitA3dXx.png)

1. os 分配空间，设置基址，从陷阱返回
2. 硬件： 恢复寄存器，跳转用户模式
3. 用户： 执行命令

**结束**
1. 保存 A的寄存器 (包括基址)
2. 从进程结构恢复 B

**开始B**
