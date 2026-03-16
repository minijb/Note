---
tags:
  - cpp
  - book
---

## 初始化的时候避免窄化

```cpp
double x {2.4};
```

## 如何将一个大任务分割为多个小任务

**基本原则**

- **抽象** ： 不需要了解程序的具体实现细节，细节隐藏在相应的接口中。
- **分治** ： 将一个大问题分割为多个小问题。

**如何进行分割**

- 明确各个子程序之间的关系 -- 按照功能进行划分是最简单的
- 编程之前先进行分析

## 表达式

**常量表达式(constexpr)和常量(const)的区别** 

- 常量表达式 --- 需要在编译之前就可以确定值
- 常量 --- 初始化之后就不会进行改变

```cpp
constexpr double pi = 3.14;
pi+1; // 是一个常量表达式
```

## 类型转换

常见错误： `double a = 9/5` --> 结果为 1

原因: `9/5` 返回的是一个int而不是double --> `9.0/5` 返回一个double值。

## 异常

带异常处理的函数

```cpp
class Bad_area {}

int area(int length, int width){
	if xxx throw Bad_area {};
	return length*width;
}
```

这里 Bad_area 是我么定义的一个新类型，用作 area 中的异常标识。 方便确认异常来之哪里。 `throw Bad_area{}` 就是创建一个异常并抛出他

此时我们可以这样运行

```cpp
try{
	int a1 = area(11,22);
}catch(Bad_area){
	cout << "Bad arguement of area()!" <<endl;
}
```

常见的异常包括 `out_of_range` `runtime_error({string})`

```cpp
try{
	xxx
}catch(runtime_error$ e){
	cout<<e.what() << '\n';
	return 1;
}catch(...){ //用来处理其他所有异常类型  类型 exception 是所有异常的超类
	
}
```