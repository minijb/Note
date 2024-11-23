
允许自己添加规则。 默认是大根堆 -- < 表示队列后面的元素要小于前面的元素。

```cpp
template<
    class T,
    class Container = std::vector<T>,
    class Compare = std::less<typename Container::value_type>
> class priority_queue;
```

同理建立小根堆

```cpp
priority_queue<int, vector<int>, greater<int>> test; 
```

## 使用方法

支持的顺序容器 `vector queue`

建立自己的规则

```cpp
auto cmp = [](int left, int right) { return (left ^ 1) < (right ^ 1); };
std::priority_queue<int, std::vector<int>, decltype(cmp)> q5(cmp);
```