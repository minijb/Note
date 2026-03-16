---
tags:
  - cpp
  - algo
---
## 接口网站

[cppreference](https://en.cppreference.com/w/)


## set

### unorder_set

```cpp
// unorder_set
unorder_set<T> u_set;

//insert
u_set.insert(T t);

// find and judge
iterator it = u_set.find(T t);
if(u_set.find(t) != it.end()){

}

// 删除
u_set.erase(t);
```


## 技巧

如果想要通过一种数据类型种的值构建另一种数据类型，可以使用迭代器。

使用 push_back 会不断重复分配内存， 直接使用迭代器的复杂度为 $N$

```cpp
return vector<int>(result_temp.begin(), result_temp.end());
```


## stack and queue

栈的底层实现可以是vector，deque，list 都是可以的

指定底层实现: 

```cpp
std::stack<int, std::vector<int> > third;  // 使用vector为底层容器的栈
std::queue<int, std::list<int>> third; 


stack<int> q;	//以int型为例
int x;
q.push(x);		//将x压入栈顶
q.top();		//返回栈顶的元素
q.pop();		//删除栈顶的元素
q.size();		//返回栈中元素的个数
q.empty();		//检查栈是否为空,若为空返回true,否则返回false


//queue
push(x)
pop()
front()
size()
empty()
back()
```


## hash

![[cpp hash]]

## priority_queue



