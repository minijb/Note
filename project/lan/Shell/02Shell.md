# Shell

## Shell的父子关系

在父shell中使用bash命令会生成一个新的shell程序--子Shell运行当前命令

如 `ps -f` 会显示两个进行一个父进程，一个子进程--运行ps，同理运行shell脚本也会创建一个子进程

### 命令列表

简单来说就是先建立一个子进程，然后运行命令

`ls ; xxx; xxx` 不是命令列表
`(ls ; xxx ; xxx)` 是命令列表

### 后台模式

在命令后加 `&`, 返回 后台程序的编号+PID

使用 `jobs` 查看当前终端的后台运行程序 --- 注意其他终端不可见

将进程列表放入后台 --- `(ls; xx; xx)&`， 常用于在后台归档多个文件

### 协程

同时做两件事：在后台生成一个子进程，在子shell内运行命令

`coproc sleep 10` -- `coproc {name} { sleep 10; }`  使用扩展语法，{}在前后两端都是有空格的

## 内建命令

外部命令--文件系统命令，常在/bin 目录

```sh
which ps
/bin/ps
```

外部命令会创建子进程，内部命令不需要子进程

### history

查看历史命令， `![!|num]` 执行历史命令

### 别名

查看别名 `alias -p`
设置别名 `alias li='ls -li'`
