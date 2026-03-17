## 1. 改变文件属性和权限的方法

chgrp ：改变文件所属群组
chown ：改变文件拥有者
chmod ：改变文件的权限, SUID, SGID, SBIT等等的特性

## 2. chmod 简单使用

```sh
#1. 使用数字
chmod 777 xxx

#2. 使用文字
#user(u) group(g) others(o) all(a)
# 符号可以是 = + -
chmod u=rwx,go=rx xxx
```

## 3. 权限的区别

对于文件：可读，可写，可运行
对于文件夹：可读文件夹内容，可写文件夹，是否为可执行文件目录（是否具有进入该文件的权限）

## 4. 目录配置依据

`/usr` 软件相关, `var` 系统运行过程相关

- `/bin` 运行档目录
- `/boot` 开机用到的文件
- `/dev` 设备
- `/etc` 主要设置档， -- opt 第三方协力软件
- `/lib`
- `/mnt` 挂在的设备
- `/opt`
- `/tmp` 临时目录

### `/usr`

- `/usr/bin` 命令文件 -- lib 
- `/usr/lib`
- `/usr/local/` 自行安装的软件 -- 有下级的 bin lib 等目录
- `/usr/sbin` 非系统正常运行所需要的指令
- `/usr/share`

- `/usr/include` 头文件库
- `/usr/libxxx` 不被一般用户用到的运行文件
- `/usr/src` 源文件

![jpg](https://vbird.org.cn/linux_basic/centos7/0210filepermission//centos7_0210filepermission_4.jpg)
