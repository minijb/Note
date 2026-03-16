---
tags:
  - OperatingSystemNanjin
---
## 介绍

三个主要线索: 
- 硬件
- 软件
- 操作系统

管道 --- 将一个程序的输出作为另一个程序的输入

## 程序角度的操作系统

helloworld c文件

```shell
gcc --verbose hello.c -static 
```

可以查看很多信息如 include 在哪里。

我们只进行编译 `gcc -c hello.c` -- 得到 `hello.o`

`objdump -d hello.o` 查看汇编 --- 此时的问题就是无法直接链接。

syscall

> busybox toybox

> objdump 更好的翻译汇编

任何程序都是状态机

system call trace (strace) --- 工具 用来跟踪 syscall

**任何程序 == minimal.S == 状态机**

- 总是被操作系统加载开始
	- 通过另一个经常2执行 execve 设置为初始状态
- 经历状态机执行 (计算+syscalls)
	- 进程管理
	- 文件/设备管理
	- 存储管理
- 最终调用 `_exit` 退出

对于 gcc 来说重要的系统调用 -- open 

**应用程序 = 计算 + 操作系统API**

**操作系统的职责： 提供令程序舒适的抽象**

## 高级程序语言

c 也是一个状态机 --- 和汇编的关系

每一个复杂 c 语句 都可以将之改编为 多个单步的 simple c

```c
if(x + y > 0)


int x = 1 , y = 1;

int x + y = cond;

if(cond)
```

**状态机**

状态：
- {stackFrame , stackFra ....} + 全局变量

初始状态
- 仅有一个 stackFrame(main, argc, argv, PC=0)
- 全局递归全部为初始值

状态迁移

- 执行 `frames[-1]`  也就是栈顶的语句 PC位置的简单语句

将 汉诺塔 改写为非递归状态机

```c
#include <stdio.h>
#include <assert.h>

struct Frame {
    // Each frame has a program counter to keep track its next
    // to-be-executed statement.
    int pc;

    // The internal state of the frame. This state includes
    // both arguments and local variables (if any).
    //
    // Arguments:
    int n;
    char from, to, via;

    // Local variables:
    int c1, c2;
};

typedef struct Frame Frame;

int hanoi(int n, char from, char to, char via) {
    Frame stk[64];
    Frame *top = stk - 1;

    // Function call: push a new frame (PC=0) onto the stack
    #define call(...) ({ *(++top) = (Frame){.pc = 0, __VA_ARGS__}; })
    
    // Function return: pop the top-most frame
    #define ret(val) ({ top--; retval = (val); })


    // The last function-return's value. It is not obvious
    // that we only need one retval.
    int retval = 0;

    // The initial call to the recursive function
    call(n, from, to, via);

    while (1) {
        // Fetch the top-most frame.
        Frame *f = top;
        if (top < stk) {
            // No top-most frame any more; we're done.
            break;
        }

        // Jumps may change this default next pc.
        int next_pc = f->pc + 1;

        // Single step execution.

        // Extract the parameters from the current frame. (It's
        // generally a bad idea to reuse variable names in
        // practice; but we did it here for readability.)
        int n = f->n, from = f->from, to = f->to, via = f->via;

        switch (f->pc) {
            case 0:
                if (n == 1) {
                    printf("%c -> %c\n", from, to);
                    ret(1);
                }
                break;
            case 1: call(n - 1, from, via, to); break;
            case 2: f->c1 = retval; break;
            case 3: call(1, from, to, via); break;
            case 4: call(n - 1, via, to, from); break;
            case 5: f->c2 = retval; break;
            case 6: ret(f->c1 + f->c2 + 1); break;
            default: assert(0);
        }

        f->pc = next_pc;
    }

    return retval;
}

```


<span style="background:#fff88f">自己的理解</span>

```c
// 每一个状态机中 PC 记录了当前状态所在的语句 -- 也就是下一步应该运行的语句。

/*
    当前状态A
    每一个递归 都会 入栈 同时更新栈顶 。 -- 状态B
    但是之前的的状态A 中使用pc记录了所运行的语句， 也就是记住了状态。

    那么B执行完成， 就会自动执行A ， 此时A会继续之前的状态继续运行。
*/
```

### 编译器 及其优化

编译器的输入 --- c语言 --- 状态机
编译器的输出 --- 汇编 --- 状态机
编译器 = 状态机之间的翻译器

运算 = 操作数 load 到寄存器，执行运算，store 写回结果
分支/循环 ： 根据条件跳转并分别实现代码
函数调用：留一个寄存器给栈 SP。 --- 函数栈
- stack frame 的信息保存在内存里。
	- 通过SP可以访问访问当前栈帧的变量和返回地址 --- 使用偏移量执行。


### 编译器的优化

三板斧：

- **函数内联**：将函数调用替换为函数体本身的内容
- **常量传播**：在编译时计算常量表达式的值并替换
- **死代码消除**：删除永远不会被执行到的代码

> compiler : https://godbolt.org/

