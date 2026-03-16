
## pstree


**阅读材料**

[POSIX 对命令行参数有一定的约定](http://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap12.html)
https://jyywiki.cn/OS/2024/labs/M1.md
[pid](https://www.gnu.org/software/libc/manual/html_node/Process-Identification.html)



/proc 的介绍

1. `/proc/cpuinfo`：包含有关 CPU 的信息，如型号、速度等。
2. `/proc/meminfo`：提供有关系统内存使用情况的信息。
3. `/proc/version`：显示 Linux 内核的版本。
4. `/proc/uptime`：显示系统启动以来的总时间。
5. `/proc/loadavg`：显示系统在过去 1、5 和 15 分钟的平均负载。
6. `/proc/[pid]`：每个进程都有一个以其进程 ID (`pid`) 命名的目录，其中包含了关于该进程的信息。
    - `/proc/[pid]/status`：进程的状态信息，如进程ID、父进程ID、用户ID等。
    - `/proc/[pid]/cmdline`：启动该进程的完整命令行。
    - `/proc/[pid]/cwd`：当前工作目录的符号链接。
    - `/proc/[pid]/exe`：正在运行的程序的符号链接。
    - `/proc/[pid]/fd`：包含进程打开的文件描述符的符号链接。

`/proc` 文件系统是 Linux 系统中一个非常有用的工具，它允许用户和程序以文件的方式访问系统信息，这对于系统监控、性能分析和故障排除等任务至关重要。

如果你需要更详细的信息或者有特定的问题关于 `/proc` 文件系统，请随时提问。


## C 目录操作

[linux api](https://www.gnu.org/software/libc/manual/html_node/Accessing-Directories.html)

```c
struct dirent *readdir(DIR *dirp);
struct dirent {
 ino_t d_ino; /* inode 编号 */
 off_t d_off; /* not an offset; see NOTES */
 unsigned short d_reclen; /* length of this record */
 unsigned char d_type; /* type of file; not supported by all filesystem types */
 char d_name[256]; /* 文件名 */
};

```


> 问题 编译32位出错 ： sudo apt-get install gcc-multilib