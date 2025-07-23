---
tags:
  - algo
---
前缀和 ： 快速定位 区间 sum  --- 可以扩展到可加性上(如乘法，除法，异或)

```txt
sum[1,k] + sum[k+1 , N] = sum[1,N]

sum[l,r] = sum[1,r] - sum[1, l-1]
```

差分数组 ： $d_{i} = a_{i}-a_{i-1}$

性质 ： 1. 从求和还原为 $a_{i}$ , 2. 进行后缀区间的修改！！！！(静态的：先修改再询问)

$$
\sum^{i}_{j=1} = d_{1} + d_{2} + \dots + d_{i} = a_{i}
$$

![dFAX6uijyGCsT35.png](https://s2.loli.net/2025/01/25/dFAX6uijyGCsT35.png)

https://www.starrycoding.com/course/page/1