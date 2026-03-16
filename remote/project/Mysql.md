
https://blog.csdn.net/HappyLearnerL/article/details/128064092

## 连接

`mysql -u xxx -p`

## 重启，关闭

`service mysql restart`

## 修改密码

```sql
use mysql; 
 
update user set authentication_string='' where user='root';      --将字段置为空
 
alter user 'root'@'localhost' identified with mysql_native_password by '123456';     
--修改密码为123456
```


## 授权

```sql
grant all privileges on *.* to 'yangxin'@'%' identified by 'yangxin123456' with grant option;

#可以在本地登录
grant all privileges on *.* to 'yangxin'@'localhost' identified by 'yangxin123456' with grant option;


#刷新
flush privileges;
```

1. all privileges : 所有权限
	1. 也可以是 select create drop
2. on 后面跟哪些数据库.表  如： test.user -- test数据库中的 user 表 ,`*` 表示任意
3. to 后面加目标用户  格式 ： `'用户名'@'登录IP'`  `%` 表示没有i西安至
4. identified by 指定用户名和密码 (可以不加)

在 mysql.db 中查看
## 创建用户

```mysql
create user zhang3 identified by '123_qwerQWER'; # 默认hosts是 % 
flush privileges; #立即生效
---------------------------------------------------------
create user 'kangshifu'@'localhost' identified by '123_qwerQWER'; # 创建指定host的用户
```

可以在 mysql.user中查看


## 删除用户

`drop user zhangsan@'%';`



