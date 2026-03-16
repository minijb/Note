---
tags:
  - csapp
  - cpp
---
## 官方

### Tools

1. printf -- 日志
	- 用于简单程序, 以及条件判断分支
	- 注意, 只输出必要的日志
2. Valgrind -- 处理内存泄漏
	- 用于查看是否存在内存泄漏
3. GDB -- 其他所有
 

### Valgrind

`valgrind -–leak-resolution=high –-leak-check=full –-show-reachable=yes –-track-fds=yes ./myProgram arg1 arg2` 推荐使用的参数 --- 最好看看 man

![BX12d7JCbnoPp56.png](https://s2.loli.net/2024/12/25/BX12d7JCbnoPp56.png)

![Ijv2gYZWSGXQxda.png](https://s2.loli.net/2024/12/25/Ijv2gYZWSGXQxda.png)

![4KCSFGqNhAxRosu.png](https://s2.loli.net/2024/12/25/4KCSFGqNhAxRosu.png)

![5JNbznFEX9PchjW.png](https://s2.loli.net/2024/12/25/5JNbznFEX9PchjW.png)

![SBIse8YcGnXN3vj.png](https://s2.loli.net/2024/12/25/SBIse8YcGnXN3vj.png)


### GDB

功能:

- set breakpoints
- set watchpoints
- print values
- step through execution
- Backtrace see previous function calls

DOC : https://sourceware.org/gdb/current/onlinedocs/gdb.html/

### 启动项

- 在 gdb shell 中启动

```sh
gdb
run xxx(program)
```

- gdb + 二进制文件
- 使用 `gdb --args gcc -O2 -c foo.c` 
- 退出 `(gdb) q`
- `-h`

### 控制

![FciOdo8RGqz3LBK.png](https://s2.loli.net/2024/12/25/FciOdo8RGqz3LBK.png)

![IMiAe6JUY2EnTHB.png](https://s2.loli.net/2024/12/25/IMiAe6JUY2EnTHB.png)
![ktcMzsdfR4rFhom.png](https://s2.loli.net/2024/12/25/ktcMzsdfR4rFhom.png)

![sg1KynWGNqUzf8t.png](https://s2.loli.net/2024/12/25/sg1KynWGNqUzf8t.png)
![jnIaRN2mlT9i6D3.png](https://s2.loli.net/2024/12/25/jnIaRN2mlT9i6D3.png)

![Mkjx4RvQz5sPZTX.png](https://s2.loli.net/2024/12/25/Mkjx4RvQz5sPZTX.png)
![s4Lo5Tt8ueki1Er.png](https://s2.loli.net/2024/12/25/s4Lo5Tt8ueki1Er.png)

- 直接跳入某个位置 `advance xxx`
- 修改变量 : `set variable x = xx`
- 监视 : `watch`  trigger whenever an expression changes
	- 注意不仅仅是变量， 也可以是表达式 如 `*(p+5)` or `a[15]`
- attch pid : 调试已经运行的代码
- 调试异常代码 ： `gdb -tui -c core xxx`

**window function**

- info win
- fs {name/next/prev}
	- Valid window names are "SRC" (source window), "CMD" (command window), "REGS" (registers window), and "ASM" (assembly window).
	- SRC window 可以使用箭头切换文件， 但是在CMD 方向键是切换历史命令

**Display Registers and Assembly**

layout 指令 

|                     |                                                                                                                                                     |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| **layout src**      | Standard layout—source on top, command window on the bottom                                                                                         |
| **layout asm**      | Just like the "src" layout, except it's an assembly window on top                                                                                   |
| **layout split**    | Three windows: source on top, assembly in the middle, and command at the bottom                                                                     |
| **layout reg**      | Opens the register window on top of either source or assembly, whichever was opened last                                                            |
| **tui reg general** | Show the general registers                                                                                                                          |
| **tui reg float**   | Show the floating point registers                                                                                                                   |
| **tui reg system**  | Show the "system" registers                                                                                                                         |
| **tui reg next**    | Show the next page of registers—this is important because there might be pages of registers that aren't in the "general", "float", or "system" sets |

## 速查表

![[Beej's Quick Guide to GDB.pdf]]

## 其他资料

[教程](https://beej.us/guide/bggdb/)
[two page](https://csapp.cs.cmu.edu/3e/docs/gdbnotes-x86-64.pdf)

https://www.tutorialspoint.com/gnu_debugger/gdb_debugging_programs.htm
https://sourceware.org/gdb/current/onlinedocs/gdb.html/

https://web.cecs.pdx.edu/~apt/cs510comp/gdb.pdf