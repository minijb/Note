# 安全

## 用户

### useradd 添加用户

`useradd -D` 查看默认值

创建用户 `useradd -m {name}` , -m 会在HOME中创建目录

常用opt

- -e {time} 以YYYY-MM-DD格式指定一个过期时间
- -g {group} 指定GID或者组名
- -G group ... 除登陆组外多个或一个附加组
- -n 创建一个和登录名一样的新组
- -p passwd
- -u 指定UID
- -s 指定shell

改变默认值--在-D之后再添加其他选项

- -b
- -e 同上
- -g
- -s

### 删除用户

`userdel -r test` 删除用户，-r 会删除用户目录

### 修改用户

#### usermod

- -l 删除登录名
- -L 锁定用户，无法登录
- -p 改密码
- -U 解除锁定

#### passwd/chpasswd 修改面膜

`passwd {user}`

再root用户中使用chpasswd批量修改密码

```shell
chpasswd < user.txt
```

其中格式为 `userid:passwd`

#### chsh chfn chage

chsh 修改登录shell -- 必须使用路径名

`chsh -s /bin/bash test`

`chfn` 没有参数，询问将那些内容加入备注字段

`chage` 管理用户有效期

opt：

- -E 密码过期日期
- -I 密码过期到用户锁定的天数
- -m 修改密码最少要多少田
- -W 过期前多久提示

日期格式:`YYYY-MM-DD`或1970.1.1到该日期的天数

## 组

id：GID

create new group : `groupadd {name}` 默认不添加用户进去

use `usermod` to add user into group.  `usermod -G {groupname} {username}`
> 注意： -g 和 -G 不一样！！！

修改组： `groupmod` -g：GID -n：name  ，`{修改值} {target}`

## 文件权限

`ls -l`

第一个字符：

- - : file
- d : dir
- l : link
- c : 字符型设备
- b : 块设备
- n : 网络设备

`chmod` 改变权限

- `{num}{num}{num}`
- `[ugoa][+-=]{rwx}`

`chown {owner}[.group] {file}` 改变从属关系

`chgrp {group} {file}` 直接改变文件/目录的群组

## 共享文件

文件的三个额外信息位

- SUID 设置用户ID
- SGID 设置组ID
- 粘着位

```shell
chmod u+s filename # 设置SUID位
chmod u-s filename # 去掉SUID设置
chmod g+s filename # 设置SGID位
chmod g-s filename # 去掉SGID设置
```

SGID的作用：可以强制在共享目录下创建的新文件都属于改目录的属组，这个组也就成为了每个用户的属组.
--- 创建的文件都属于目录所属的组故而可以共享。
