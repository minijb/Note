# 环境变量

## 环境变量

### 全局环境变量

查看 `env` `printenv {xxx}` `echo $xxx`

### 局部环境变量

查看 `set`

## 用户定义变量

```sh
echo $one

one=Hello

echo $one
```

注意:

- 如果字符串有空格需要加上单双引号，同时变量，等号，值之间没有空格
- 子bash中设置的局部变量父bash不能使用

### 设置全局变量

```shell
val="hello"
export val
```

子shell可以修改，但是不影响全局变量，无法使用export改变全局变量的值。

### 删除环境变量

`unet {val}` 不加$

全局变量同理，但是在子进程删除不影响父shell

### 默认shell环境变量

...

### PATH环境变量

定义了命令和程序查找目录，使用:分割，我们可以如此添加`PATH=$PATH:/home/sss/sss`, 通常加入 `.` 表示将当前目录设为搜索。

## 非交互式shell

子shell可以继承父shell导出的变量(epxort)，但是不能继承局部变量(设置但是没有导出的变量)

### 数组变量

`mytest=(one two three)`

```shell
echo $mytest
one

echo ${mytest[2]}
three

echo ${mytest[*]}
one two three

#可以直接通过索引改变值
mytest[2]=eleven
```

使用unset可以删除数组，或者索引上的值
