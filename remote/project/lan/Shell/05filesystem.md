# file system

## 分区

查看分区情况： `fdisk -lu [target]` 没有 target 查看多有分区

`sudo fdisk {target:/dev/sdb}` --- 交互式程序

常用命令:

- p : 查看详细信息
- n : 添加一个新的分区
  - e : extended partition 扩展分区-- 逻辑分区
  - o : primary partition 主分区
- w : 保存

## 文件系统

在将数据存储到分区之前，我们必须使用文件系统进行格式化。

`mkefs mke2fs mkfs.xxx`

`sudo mkfs.ext4 {target}` -- `sudo mkfs.ext4 /dev/sdb1`

**挂载** :

```shell
sudo mkdir /mnt/my_file 
sudo mount -t ext4 /dev/sdb1 /mnt/my_file
```

> 这个只能临时挂载，强制linux自动挂载需要，添加到 /etc/fstab 文件中

## 逻辑卷管理

xxxx

