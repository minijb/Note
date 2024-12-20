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

