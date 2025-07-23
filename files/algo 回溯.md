---
tags:
  - algo
---
> 如果回溯是在尾部 可以使用  recrusion(path + xxx) 来实现 --- 无需使用额外的语句。



三个东西：
- 子集 ： 所有可能的组合
- 组合 ： 非排列
- 排列 ： 顺序不一致，也算一种情况

## 子集

子集问题 ：
两种方法

```c++
dfs(int i){

	dfs(i+1); // 不选

	list.append(xx) // 选
	dfs(i+1);
	list.pop();
}


dfs(int a){
	list.append();

	for(int i = a ; i < n ; i++){
		list.append(i)
		dfs(i+1);
		list.pop();
	}
}
```


## 组合问题

其实就是在子集的基础上进行减枝

推荐倒叙进行枚举。

```python
ans = []
path = []
def dfs(i):
	d = k - len(path)
	if i < d:
		return
	if(len(path)) == k:
		ans.append(path.copy())
		return
	for j in range(i, 0 , -1):
		path.append(j)
		dfs(j-1)
		path.pop()
```

## 排列问题

顺序区别

有`[2,1]` -- 这 `[1,2]` 也是可以的

**写法1**

path 记录已选数字
集合s 记录剩余未选的数字

![700](https://s2.loli.net/2025/03/15/ecQuZBE3H2h7Gf4.png)

**写法2**

哈希表改为bool数组 --- 选择一个值则进行标记

![700](https://s2.loli.net/2025/03/15/ScZUPzQnlaT6Hp1.png)
