
**how to use gdb**

https://sourceware.org/gdb/documentation/
https://www-users.cse.umn.edu/~kauffman/tutorials/gdb

## 计算机系统的状态机模型

**状态** 内存和寄存器的数值
**初始状态** CPU Reset
**状态迁移** 从PC取指令运行

计算机不能直接感知外部世界，同理，系统也不能直接访问 --- 进程只能通过 syscall 访问进程外的信息
于此同时硬件也是一个状态机

**qemu** 计算机仿真器

https://www.usenix.org/legacy/publications/library/proceedings/usenix05/tech/freenix/full_papers/bellard/bellard.pdf

firmwore 用来启动 操作系统，可以自定义。
同理 我们可以自定义启动盘的头 : 以 55 AA结束。

因此我们可以写 446 = 512 -2 - 64(分区表)

