# Basic of Shell

## ls 的过滤器

- ?: 匹配一个字符
- *: 匹配多个字符
- []: 匹配某个范围如: `[a-i] [1-9]`
- [!]: 排除某个范围如: `[!a]`

## 常用的选项

- -i: prompt before overwrite
- -r -R: recursice

## 链接

软链接/符号链接 : `ln -s {des} {name}`
硬链接: `ln {des} {name}`

## 监控

### 进程

`ps` : 当前控制台下，当前用户的进程

最有用的参数

- -e : 显示所有进程
- -f : 以完整格式输出
- -l : 长格式输出

长格式的输出列：

- S: 进程状态
- PRI: 进程的优先级

### 实时进程监控

`top`

- PR: 进程优先级
- VIRT：虚拟内存占用量
- RES: 物理内存占用量
- S: 进程状态
- SHR: 共享的内存总量

### 结束进程

进程之间通过进程信号进行通信，先识别信号再决定是否接收。

常用*进程信号*:

- 1 -- HUP -- 挂起
- 2 -- INT -- 中断
- 3 -- QUIT -- 结束运行
- 9 -- KILL -- 无条件中止
- 11 -- SEGV -- 段错误
- 15 -- TERM -- 尽可能中止
- 17 -- STOP -- 无条件停止，但是不中止
- 18 -- TSTP -- 停止或暂停，但是继续再后台运行
- 19 -- CONT -- 再STOP或TSTP之后恢复运行

两个可以发送进程信号的命令

#### kill

`kill {options} {PID}`, 默认情况下发送TERM信号。

使用 `-s` 指定i型号 : `kill -s {xxx} {PID}`

#### killall

不使用PID，而是进程名，可以使用通配符

`killall http*`

## 磁盘和存储

### mount 管理设备

`mount` 查看挂载的设备

- 媒体文件名
- 虚拟目录挂载点
- 文件类型
- 访问状态

手动挂载: `mount -t {type} {device} {directory}`

- type : 文件类型

例子：`mount -t vfat /dev/sdb1 /media/disk`

`-o` 指定挂载类型： ro 只读， rw 读写，user, check=none, loop ...

卸载设备：`umount {directory | device}` , 如果正在使用则卸载设备失败

### df 磁盘查看

`df` ：查看设备的磁盘空间

常用选项：

- -h: 使用易读形式

### du 文件的大小

`du {options} {aug_list}`

没有aug则默认当前文件下所有文件

常用参数

- -c: 显示列出的文件总大小
- -h：易读格式
- -s: 每个输出参数的总计

## 处理数据

### sort

默认从小到大

常用选项：

- -k: 指定排序字段
- -t：指定分隔符
- -n: 按字符串数值进行排序
- -r: 反向排序


可以按字段进行分割并排序, 联合使用 `-k -t`

`sort -t ':' -k 3 -n /etc/passwd`

### grep

按行搜索 `grep {opt} pattern {file}`

常用opt:

- -v : 反向搜索
- -n : 显示所在行号
- -c : 匹配个数
- -e : 多个匹配 `grep -e t -e f file`

可以受用unix的通配符

衍生：egrep 可以受用正则，fgrep

### 压缩

gzip

### 归档 tar

`tar function {option} obj1 obj2 ...`

一个function 对应多个 opt

常用function:

- -A 将一个tar文件追加在另一个tar
- -c 创建一个新的tar文件
- -x 从归档文件中提取文件
- -t 列出归档文件的内容

常用opt：

- -C dir 切换到指定目录
- -v 处理文件时列出文件
- -f file 输出结果到文件或file
- -j 重定向给bzip2用来压缩
- -z 重定向给gzip用来压缩

常用：`-cvf` 归档文件 `-xvf` 提取文件(如果从一个文件夹归档，则恢复成一个文件夹，否则为多个文件)

注意：`-z -j` 放在最前面
