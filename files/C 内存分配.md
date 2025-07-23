---
tags:
  - cpp
  - C
---

## 基础的堆分配 brk and sbrk

https://www.cnblogs.com/hanerfan/p/4545370.html

```C
// 成功时返回0，出错时返回-1并设置errno为ENOMEM
int brk(void *addr);

// 成功时返回先前的堆结束位置。出错时，返回(void *)-1并设置errno为ENOMEM
void *sbrk(intptr_t increment);
```

堆分为:


|---| rlimit
  未映射区域
|---| brk
  已映射却与
|---| start_brk
|---| 0


两个函数其实就是使 brk 上升。 不同 ： brk()的addr参数指定了堆在虚拟地址空间中新的结束位置，而sbrk()通过增量increment调节堆的结束位置。

释放的时候 不会返还给系统，而是放在 malloc 内存池中，可以重复使用。

**优势** ： 可以减少缺页异常的发生，提高内存访问效率
**劣势** ： 可能造成内存碎片

## Malloc free

malloc 每次都会多一些空间 ： meta Data
free. 

基础的结构 ： Node 使用单链表

```c++
struct Node{
	next*;
	size_t length;
}
```

## mmap

https://www.cnblogs.com/beilou310/p/17037066.html

mmap 是一种内存映射文件的方法，即将一个文件或者其他对象映射到进程的地址空间，实现文件磁盘地址和进程虚拟地址空间中一段虚拟地址的一一映射关系。
