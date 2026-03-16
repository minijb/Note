---
tags:
  - csapp
---

物理寻址   --- `[0,M-1]` 直接使用物理地址

![700](https://s2.loli.net/2025/03/22/yboS9sOfKQAeULd.png)


![700](https://s2.loli.net/2025/03/22/sXlzOgpf3MELQ5T.png)


**地址空间**

![700](https://s2.loli.net/2025/03/22/54AkRhsiOca3K6S.png)


![700](https://s2.loli.net/2025/03/22/ne36wBVqCo1fYXb.png)


内存和disk 之间的交换单位 ： 页。


![700](https://s2.loli.net/2025/03/22/QKbcOaw4EV7TsCn.png)


三种状态：
- unallocated
- cached -- 已缓存的
- uncached -- 已分配但 未缓存的

![700](https://s2.loli.net/2025/03/22/HCNbhY7AaOcwQMl.png)


![700](https://s2.loli.net/2025/03/22/cVHx6JBQy1PdwKn.png)


**只写回， 而不是写穿透！！！！！！！**

TLB  页表

![700](https://s2.loli.net/2025/03/22/fK6Ze3JywFpTkWC.png)

![700](https://s2.loli.net/2025/03/22/Gbqsc19SLMTHkzr.png)


缺页故障 ---- 异常处理程序 会到物理内存去找一个对应的页

此时需要看页是否被修改，如果被修改了则写回到硬盘。

![700](https://s2.loli.net/2025/03/22/s2N7rHJjbIXe3cU.png)


**malloc 分配的位置为虚拟页中 -- 应该是内存映射**

![700](https://s2.loli.net/2025/03/22/DcQSuV93827thBR.png)

## 地址翻译

CPU 使用的是 虚拟地址， MMU翻译后寻找的是物理地址。

![700](https://s2.loli.net/2025/03/23/ZdFNh2SquijQD9l.png)

根据页表进行寻找。

**虚拟地址的组成** VA virtual address  4KB -- 一页 



![700](https://s2.loli.net/2025/03/23/PGVjC7sk1qcnoN6.png)


页表的起始地址。

![700](https://s2.loli.net/2025/03/23/DjdJ8vhtFm5BNTk.png)


**注意 ： 页表是在内存中的！！！！！**

**页表命中的情况**
![700](https://s2.loli.net/2025/03/23/RZCVp2tOrvjgUfL.png)



**页表未命中**  --- 缺页

![700](https://s2.loli.net/2025/03/23/SNtE8phWcq6aVLx.png)



**先后顺序的问题**  ： SARM 和  虚实地址转换的问题。

1. 虚实地址转换 --- 使用物理地址去查cache
2. 然后才会去查找  cache


![700](https://s2.loli.net/2025/03/23/lL34IQpigkeyoMA.png)




**同理  MMU 内部也可以缓存页表项的缓存**  TLB -- 快表   缓存的是页表项

![700](https://s2.loli.net/2025/03/23/PF5LS3hlzZiq9xX.png)


虚拟页表号  分为 tag and index


TLB 命中 则地址查找直接在CPU内部得到

![700](https://s2.loli.net/2025/03/23/LNE7vHcBrhU9sDg.png)


没有命中则会写回 TLB

![700](https://s2.loli.net/2025/03/23/t2AZWhDEbfzgd5a.png)




![700](https://s2.loli.net/2025/03/23/f7aCkPoTGmD2Avw.png)



![700](https://s2.loli.net/2025/03/23/ZNrR4ljqDKCypmM.png)


![700](https://s2.loli.net/2025/03/23/smuraPEq4FxYeLO.png)

找到物理地址就会到 cache 中进行查找

![700](https://s2.loli.net/2025/03/23/FlKsQeM1gfU63iL.png)



> 每个进程都有独立的页表，于此同时还有一些标志位

![700](https://s2.loli.net/2025/03/23/hKTe9RkBNqJFpzD.png)


### 多级页表

![700](https://s2.loli.net/2025/03/23/DIBzr1PJaFcGMAU.png)


![700](https://s2.loli.net/2025/03/23/A47B6T3XshfNMUp.png)


### Intel i7 


![700](https://s2.loli.net/2025/03/23/WtcKrRJImG9pa38.png)


![700](https://s2.loli.net/2025/03/23/x5GolIPyKDCapAg.png)


![700](https://s2.loli.net/2025/03/23/C7bGsSNtIXQ3Vzp.png)

注意 ：  L2 cache 连接在 L3 cache 中。

但是 L2 TLB 连接在 memory 中

![700](https://s2.loli.net/2025/03/23/7cEi3TlKNe5Rm61.png)


![700](https://s2.loli.net/2025/03/23/xoIkay8QFrWlbjB.png)


![700](https://s2.loli.net/2025/03/23/yR6qMr9ODYpKicQ.png)


### 虚拟内存区域/段


https://www.cnblogs.com/LoyenWang/p/12037658.html

![700](https://s2.loli.net/2025/03/23/kTALBN6O1Un8Mx4.png)


## 内存映射

将磁盘的东西加载到内存中。


ELF文件。

![700](https://s2.loli.net/2025/03/23/ZLbEkJa6yw5j8TC.png)


**我们并没有把数据/代码加载到物理内存中！！！！！！**

复制的过程是由缺页处理程序做的！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！

访问的时候触发缺页异常，才会加载到内存中。


问题 ： 栈/堆，shared 库 如何进行填充 ？？？？？？？？

data， text 可以直接进行复制。

**匿名文件！！！！！！** 内部是二进制  一开始未 0 ---- 来映射堆和栈  ----- 磁盘和内存直接是没有数据的交互

![700](https://s2.loli.net/2025/03/23/M4bnhDGO9AlQ2y6.png)



**共享对象**

![700](https://s2.loli.net/2025/03/23/E3DS65jABCJfvHM.png)


**私有对象** 写时复制 copy on write  --- 延后写入操作的时间  --- 故障处理程序

此时不会影响其他进程的运行
![700](https://s2.loli.net/2025/03/23/Fug6djwTzbDVxe4.png)


![700](https://s2.loli.net/2025/03/23/eThtO3K7jxXBVbf.png)


fork 会进行写时复制

![700](https://s2.loli.net/2025/03/23/iZA9StEpLC7jbJU.png)


![700](https://s2.loli.net/2025/03/23/3NvjyQrmbUPVo7A.png)


**用户级别的内存映射函数 mmap**


![700](https://s2.loli.net/2025/03/23/gqeV2Z5DIx4vfmB.png)


![700](https://s2.loli.net/2025/03/23/FrZyYs5jwPXg8ak.png)


https://zhuanlan.zhihu.com/p/473643975


## 动态内存分配


malloc  


execve 这种初始化的时候， 初始化为0.

brk 指针

![700](https://s2.loli.net/2025/03/23/AnpckHxUMEgyZq8.png)



![700](https://s2.loli.net/2025/03/23/RbP5vKincIA9X6q.png)


地址时需要对齐的  ---- 32-8  64-16 倍进行对齐

calloc -- 申请并初始化    realloc -- 重新分配（如扩充）

sbrk  brk 函数， 前者是库函数，  后者是系统调用


字 ： 2字节
双字 ： 4字节

![700](https://s2.loli.net/2025/03/23/yYIeKjw3mF8UgTX.png)

![700](https://s2.loli.net/2025/03/23/tsoMwf7vPDQpW9c.png)

注意此处没有对齐  --- 20 字节  需要扩充到 24 字节对齐


![700](https://s2.loli.net/2025/03/23/Ub3BwnHKD8CGgPs.png)

![700](https://s2.loli.net/2025/03/23/8qz9sBclmdWe3jb.png)


![700](https://s2.loli.net/2025/03/23/nNHgR5BZ8e4FKSp.png)


## 分配器

![700](https://s2.loli.net/2025/03/23/B5Ui4XnlAWC6yOL.png)

- 最大化吞吐率
- 最大化内存使用率

- 内部碎片 ： 由于对齐造成的内存浪费
- 外部碎片 ： 分配内存之间的空间内存

![700](https://s2.loli.net/2025/03/23/9hWbsVFkD1cAE5i.png)


## Heap block

分配的数据块 ： 头部信息 ， 有效载荷，  padding

![700](https://s2.loli.net/2025/03/23/tFO7QL3BfPoUbes.png)


a = 1 表示已经被分配， a = 0 表示没有被分配

![700](https://s2.loli.net/2025/03/23/VRHILWljtcCryku.png)


由于 8 字节对齐， 所以最低三位为0 ！！！！！！  所以可以使用低三位可以被使用

### Free List

![700](https://s2.loli.net/2025/03/23/4PtGOB2NEnZ8o19.png)


### 分配策略

- 首次分配  -- 第一次找到就分配
- 下一次分配 -- 从上一次之后找
- 最佳分配



## 合并策略

带边界标记的块。

假碎片 --- 两个碎片连在一起。

- 立即合并
- 推迟合并

添加一个脚步信息。


![700](https://s2.loli.net/2025/03/23/yjqkhI9MY6dUNoS.png)



![700](https://s2.loli.net/2025/03/23/aBIJlbKrpMx5iT2.png)



![700](https://s2.loli.net/2025/03/23/OG1NZjMEp6Ke38F.png)


![700](https://s2.loli.net/2025/03/23/2jSreihn9CMQPfX.png)


![700](https://s2.loli.net/2025/03/23/jo28IDYyWTXa9vB.png)


> 优势 ： 头尾都可以
> 劣势 ： 额外空间


![700](https://s2.loli.net/2025/03/23/za9W3jFApHSBq8L.png)


![700](https://s2.loli.net/2025/03/23/p6kMQZEqILztCFj.png)


![700](https://s2.loli.net/2025/03/23/clAU3ysMYC8bLhp.png)


![700](https://s2.loli.net/2025/03/23/5TkWgjPzKesVah3.png)

规定 ： 开始块8/1

![700](https://s2.loli.net/2025/03/23/gVjhybfxlN45OnM.png)


![700](https://s2.loli.net/2025/03/23/KC4tEX6a5frPUuo.png)


## 垃圾回收

![700](https://s2.loli.net/2025/03/23/LY4GHgxoK1jpSvA.png)


![700](https://s2.loli.net/2025/03/23/ZfcTRAbOoK5Bz7r.png)


### 错误

- 写入一个错误的地址
- 读取一个未初始化的内存  --- 使用一个 calloc 代替 malloc
- 栈缓冲区溢出 --  gets
- 误认为对象和指针相同大小


![700](https://s2.loli.net/2025/03/23/Bv16wNLJTI9hglz.png)


- 运算符优先级问题

`*，--` 优先级相同

![700](https://s2.loli.net/2025/03/23/KsXeQn9aHCZNu4q.png)


- `p++   P+=1`  代表下一个对象指针的位置， +4 则为4个

![700](https://s2.loli.net/2025/03/23/WrfSvDes1xNQbYR.png)

- 引用一个不存在的对象  -- 栈回收

![700](https://s2.loli.net/2025/03/23/3MPSIUZN4emTvhy.png)


- 引用的数据在空闲的块中


![700](https://s2.loli.net/2025/03/23/aB7FLDEJcojAIbO.png)

- 内存泄漏   --- 申请了没有回收

![700](https://s2.loli.net/2025/03/23/6xAoODSzP9sr7QF.png)

