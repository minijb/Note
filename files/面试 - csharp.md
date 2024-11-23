---
tags:
  - 面试
---
## C#基础：简述装箱和拆箱原理

https://www.cnblogs.com/dotnet261010/p/12326344.html

转向步骤 ：
- 在堆力分配一个内存块
- 在内存堆内复制对象地址，这个地址就是指向对象的引用
- 返回堆中新分配对象的地址


- struct 通过重载函数避免装箱 --- 如果 tostring gettype 等方法没有重载，那么会先装箱再调用。
- 通过泛型来避免拆箱，装箱
- 通过同意接口 避免装箱。(struct)
	- A，B 都继承接口， 相当于提前做了装箱操作


## C#多态是如何实现的

- 接口
- 抽象类
- 虚方法

动态继承： 虚函数
静态继承 ： 函数重载


## 构造函数 不能继承，因此不能重写，但是可以重载



## 静态成员

1. 类第一次加载到内存的时候创建，通过类进行访问
2. 不太 static 时 非静态变量，在对象被实例化时创建，通过对象访问
3. 静态方法不能使用非静态成员
4. 静态成员属于类，不属于对象

## const readonly

- const 声明的时候必须赋值， readonly 可以在构造函数的时候赋值
- const 可以修饰类字段，也可以修饰局部变量， readonly 必须时类字段
- const 是 编译常量，readonly 是运行时常量
- const 默认时静态的， readonly 想要静态必须声明
- const 只能修饰 string/null， readonly 都可以

## 不能继承 string 类 ，因为 sealed

## stringBuilder

1. String 字符串常量 ： 线程安全  StringBuilder 字符串变量， 线程不安全
2. String 不可变， StringBuilder 可变

## struct class

struct 是 值类型 class 引用类型

## hashcode  对象相同

1. 对象相同(a.equal(b))，hashcode 必定相同
2. hashcode 相同，两个对象不一定相同

### int? 可空类型

int？ 是通过int装箱为引用实现的

### sleep wait

sleep 当前线程挂起指定时间
wait 释放对象上的锁并阻塞当前线程， 知道重新获得锁

## sealed

1. 用于 class ， 不能被继承，不能和 abstract 同时使用
2. 用于方法和属性， 表示不能被重写， 必须和 override 一起使用


## for foreach

长度固定 ： for
长度不固定 ： foreach --- 循环过程中会释放使用完的资源，会造成额外的GC




## 闭包

通过 Lambda 表达式可以访问 Lambda