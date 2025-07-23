---
tags:
  - cpp
---

## 基础六大部件

- 容器
- 分配器
- 算法
- 迭代器
- 适配器
- 仿函数

## 容器

- 序列容器
- 关联容器
- 无序关联容器


## array / vector

固定大小 

`array<type, length>`

vector 自动扩容

## List / forward_LIst

双向列表/单向列表

如果容器自己有sort， 最好使用自身的sort

forward_List 只有 push_front  , front 没有 back 等


## deque  

双向容器

![700](https://s2.loli.net/2025/03/25/AeS1fgEGsbZIrmN.png)


分段连续的。

deque和vector的最大差异，一在于deque允许常数时间内对其头端进行元素的插入或移除操作，二在于deque没有所谓的容量概念，因为它是动态地以分段连续空间组合而成，随时可以增加一段新的空间并链接起来。

**deque的迭代器并不是普通指针，其底层实现非常复杂**。因此，除非必要，**应尽可能选用vector而非deque**。对deque进行的排序操作，为了最高效率，可将deque先完整复制到一个vector上，然后vector排序后，再复制到deque。

**deque是由一段一段的定量连续空间构成**。一旦有必要在deque的前端或尾端增加新空间，便配置一段定量连续空间，串接在整个deque的头端或尾端。deque的最大任务，便是在这些分段的定量连续空间上，维护其整体连续的假象，并**提供随机存取的接口**。避开了“重新配置、复制、释放”的轮回，代价则是**复杂的迭代器结构**。

deque采用一块所谓的map（不是STL的map容器）作为主控。

**map是一小块连续空间，其中每个元素(此处称为一个节点，node)都是指针，指向另一段(较大的)连续线性空间，称为缓冲区**。


https://blog.csdn.net/yl_puyu/article/details/103361874

## stack/queue

在 deque 基础上进行构建的。

> 就是容器适配器


