---
tags:
  - linux
---
## 远程连接mysql

```sh
create USER 'Alice'@'%' IDENTIFIED BY '123456';
GRANT ALL on *.* TO 'Alice'@'%' WITH GRANT OPTION;
```

开启 mysql server 的端口
```sh
 vim /etc/mysql/mysql.conf.d/mysqld.cnf
```

