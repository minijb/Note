---
tags:
  - csapp
---
优化编译

```c++
// 两次读， 两次写内存
*xp += *yp;
*xp += *yp;

// 两次读， 一次写
*xp += 2* *yp;
```

如果 xp ， yp 指向同一个位置， 两个结果会不一样。 因此优化有问题。

**内存别名** --- 会假设两个指针可能指向同一个内存

一个优化, **循环展开**

```c++
for(i = 0; i < n ; i++){
	p[i] = a[i+1];
}



for(i = 1; i < n-1 ; i+=2){
	float mid_val = p[i-1] + a[i];
	p[i] = mid_val;
	p[i+1] = mid_val + a[i+1];
}
```


结构体:

```c++
typedef struct{
	long len;
	data_t *data;
}vec_rec, *vec_ptr;
typedef int datat_t;
typedef float datat_t;
typedef double datat_t;
typedef long datat_t;
typedef long long datat_t;
```

**初始代码**

![700](https://s2.loli.net/2025/02/17/17e9urWgIk8moDt.png)


![700](https://s2.loli.net/2025/02/17/DPlr7gHGKIovNFX.png)

优化 ： 求长度

![700](https://s2.loli.net/2025/02/17/xK98otU4I5FyOG6.png)

![700](https://s2.loli.net/2025/02/17/8yrmYntIS5aleAj.png)

> 函数调用的开销时比较大的


**另一个例子**


![700](https://s2.loli.net/2025/02/17/yBhqwbrtKQ5jkHx.png)


 ![700](https://s2.loli.net/2025/02/17/enwqvZRm1f9UjAx.png)


**combine3**

![700](https://s2.loli.net/2025/02/17/efZG4wUHOpN3CgI.png)

![700](https://s2.loli.net/2025/02/17/734IKcH1NveQ8SO.png)

> 不是关键路径！！！！！

![700](https://s2.loli.net/2025/02/17/LZK8eTGBtxIVjFQ.png)

消除内存引用。

![700](https://s2.loli.net/2025/02/17/ZFXqBbfGQN1jKHp.png)


![700](https://s2.loli.net/2025/02/17/tBPOIAdS1zLvoai.png)


![700](https://s2.loli.net/2025/02/17/wpIRFV8SlQ7vnqo.png)




> 1. 减少函数调用的次数
> 2. 消除没必要的内存引用 --- 如解引用  cache miss


## 数据流图

![700](https://s2.loli.net/2025/03/11/ju7ShEzLfI1Dldi.png)


分支预测 ： 对影响到运行。 会假设运行一个分支。  如果预测成功，则直接拿回数据。否则侧丢弃。


![700](https://s2.loli.net/2025/03/11/Pd2qxYQAS38yrJB.png)


![700](https://s2.loli.net/2025/03/11/ZjkdBnyOvQ1EAzs.png)

latency ： 执行命令的时钟周期
Issue ：  两个相同命令需要的间隔。 -- 发射
latency 3 Issue 1 ： 因此内部也是流水线。
除法运算 时间不是固定的。
Capacity ： 容量 ： 同时可以进行相同的命令个数  --- 由 n 个 ALU 部件。

