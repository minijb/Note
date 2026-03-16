---
tags:
  - algo
---
默认可得到大于等于的。


```c++
int left = 1, right = x / 2 + 1;

while(left < right){
	int mid = left + (right - left) / 2;

	long long res = (long long) mid * mid;

	if(res > x){
		right = mid;
	}else{
		left = mid + 1;
	}
}

return left - 1;
```


```txt
>= -- x
> -- >=x+1  
< --  （>=x） -1
<= -- (>x) -1
```


## 常用函数

```c++
lower_bound //第一个大于等于
upper_bound // 第一个 大于 
```