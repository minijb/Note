---
tags:
  - cpp
---
## 什么是移动

c++ 中 ` = ` 的默认操作是拷贝 每次操作内存的时候都会进行拷贝操作。移动操作相当于数据的转移，原来存放数据的地方没有这个值了。

## 左值引用，右值引用

```cpp
int val{ 0 };
int&& rRef0{ getTempValue() };  // OK，引用临时对象
int&& rRef1{ val };  // Error，不能引用左值
int&& rRef2{ std::move(val) };  // OK，引用使用std::move标记的对象
```

移动操作需要使用一个右值引用， `std::move` 就是用来提供右值引用的。

编译器匹配右值引用的方式
1. **一个在语句执行完毕后就会被自动销毁的临时对象**、
2. **由std::move标记的非const对象**

## 重载类的移动构造函数


```cpp
class vector
{
public:
    void push_back(const MyClass& value)  // const MyClass& 左值引用
    {
        // 执行拷贝操作
    }

```cpp
    MyClass(MyClass&& rValue) noexcept  // 关于noexcept我们稍后会介绍
        : str{ std::move(rValue.str) }  // 看这里，调用std::string类型的移动构造函数
    {}
};
```

实现自己的移动构造类

```cpp
class MyClass
{
public:
    MyClass()
        : val{ 998 }
    {
        name = new char[] { "Peter" };
    }

    // 实现移动构造函数
    MyClass(MyClass&& rValue) noexcept
        : val{ std::move(rValue.val) }  // 转移数据
    {
        rValue.val = 0;  // 清除被转移对象的数据

        name = rValue.name;  // 转移数据
        rValue.name = nullptr;  // 清除被转移对象的数据
    }
 // 移动赋值运算符
    MyClass& operator=(MyClass&& myClass) noexcept
    {
        val = myClass.val;
        myClass.val = 0;

        name = myClass.name;
        myClass.name = nullptr;

        return *this;
    }

    ~MyClass()
    {
        if (nullptr != name)
        {
            delete[] name;
            name = nullptr;
        }
    }

private:
    int val;
    char* name;
};

MyClass A{};
MyClass B{ std::move(A) };  // 通过移动构造函数创建新对象B
```


## noexcept 的作用

太多了 ，记得写上就好