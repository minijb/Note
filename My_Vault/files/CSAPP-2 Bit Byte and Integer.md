---
tags:
  - csapp
---

补码 --- int 带符号数的负数。

10 : 0 1 0 1 0  = 0 + 8 + 2 = 10
-10: 1 0 1 1 0  = -16 + 4 + 2 = -10

UMAX  全1
TMAX  011111...
TMIN  100000...
-1    111111...
0     000000...


一些特殊情况

x = 0:
- ~0 = -1
- ~0 + 1 = 0

x = Tmin = -32768
- ~x = 32767
- ~x + 1 = -32768

![400](https://s2.loli.net/2024/06/07/5XgNIAWZfBxGd8m.png)

![400](https://s2.loli.net/2024/06/07/hcisKPpX2flkeG7.png)


relation between signed and unsigned : 

![400](https://s2.loli.net/2024/06/07/JjBqhp2ziXQnCob.png)

当为负数的时候，首地址从 正数变为负数

## unsigned and signed 比较

-1 and 0U  evalueation : unsigned

-1 : 111111111
0U : 000000000

-1 > 0U

一个有符号和无符号的数进行运算都会转化为无符号 

```c++
int i = 100;
for(; i - sizeof(char) >= 0 ; i--){
	//无限循环
}
```

**符号扩展**

task:
- w-bit signed integer x
- convert it wo w+k-bit integer with same value

将符号位左移并用符号位的值进行填充。

正数 不用说 ， 负数:  原本  -8 现在 -16 + 8 = -8 正好抵消。

expand : 

unsigned : zeros added
signed : sign extension

tuncating :

unsigned : mod operation
signed : similar to mod


## 计算

## 加法

### unsigned addtion

- standard addition function : ignores carry output
- implement modular arithmetic 

s = $UAdd_{w}(u,v)=(u+v) mod 2^w$

简单来说就是 加上后，还是原本长度 ，相当于 mod ， 此时就出现了溢出

![400](https://s2.loli.net/2024/06/08/nQdBAg5YctLSqDF.png)


### TAdd

负数 直接使用补码进行运算就可以了

补码计算也会溢出

-3 + -6 = 7 --- 负数变正数

两个较大的正数 

7 + 5 = -4  --- 正数变负数

![600](https://s2.loli.net/2024/06/08/N1bmRe4nZlSozck.png)


## multiplication 乘

### unsigned 

乘需要两倍的空间，但是为了防止内存溢出，我们只取低w位 (结果为 2w)

3 * 5 = 15 --- 没有溢出
5 * 5 = 25 --- 溢出  9

### signed 

对于补码也适用， ---- 只取低w位 同样也会溢出


## 乘/除2

### unsigned

乘 $2^n$ --- 左移n位  同样也需要 在 w 位截断
除法同理


## signed

使用算术右/左移


## Summary

- signed + unsigned  --- 加法和乘法运算是相同的
- 无符号数 ： 1 种 溢出， 有符号数：两种溢出

**什么时候使用 unsigned** 

- 进行模运算
- 使用 bits 表示一个集合

## 机器上中的表示

word size  字长。

`gcc -m64/32 xxx`

![600](https://s2.loli.net/2024/06/09/HInr9RDTbwOGQML.png)


对齐字节：32 --- 4  64 --- 8 字节

**大端，小端**

小端： 第一个字节是最低有效字节

![600](https://s2.loli.net/2024/06/09/n72OXWbEutKIgdv.png)


小端比较常见

使用大端和小端存储 int

![600](https://s2.loli.net/2024/06/09/jteMSuV3pm78cb6.png)

SUM : 大端  其他： 小端

### 无符号数 + 有符号数

$$
\bar{x} = [x_{w-1}, ... , x_0]
$$

$$
B2U_w(\bar{x}) = \sum_{x=0}^{w-1}x_i2^i
$$

$$
UMax_w = \sum_{i=0}^{w-1}2^i = 2^w-1
$$

$$
B2T_w(\bar{x}) = -x_{w-1}2^{w-1} + \sum_{i=0}^{w-2}x_i2^i
$$

$$
TMin_{w} = -2^{w-1} , \quad  TMax_{w} = 2^{w-1} -1
$$
**补码转无符号数**  --- 按位是不变的

$$
T2U_{w}(x) = \begin{cases}
  x + 2^{w-1} &,x <0\\
  x &, x > 0
\end{cases}
$$

注意 当 x = -1 时 结果为 TMax

**当一个有符号数和无符号数一起运算的时候** 两个都会作为无符号数进行运算。

符号位扩展 ：
- 无符号数： 零扩展
- 有符号数： 1扩展  原理 $2^{w} - 2^{w-1} = 2^{w-1}$

注意 ： short 转 unsigned --> 既要变疮毒，也要变类型
(unsigned)short = (unsigned)(int)short 先变长度，然后变类型

**注意：** 左移一定补0，右移看情况 无符号：逻辑， 补码：算数右移

**截断 ：**

1.无符号数 对k进行截断
$$
x' = x mod 2^k
$$
2.有符号

$$
x' = U2T(x mod 2^k)
$$


## 加减法

无符号加分

$$
x+y = \begin{cases}
x + y ,& x+y<2^w &正常 \\
x+y - 2^{w},& 2^w\leq x+y <2^{w+1} & 溢出
\end{cases}
$$

这里移除其实就是 mod $2^w$

**除法**

https://blog.csdn.net/weixin_43844521/article/details/132829932


大端和小端

  

|     | 0x100 | 0x101 | 0x102 | 0x103 |
| --- | ----- | ----- | ----- | ----- |
| ⋯   | 01    | 23    | 45    | 67    |

大端 ： 小对小  最高有效字节在前面 -- （前面： 地址为较小）

|     | 0x100 | 0x101 | 0x102 | 0x103 |
| --- | ----- | ----- | ----- | ----- |
| ⋯   | 67    | 45    | 23    | 01    |
小端 ： 大对小  最低有效字节在前面

有效字节    $\left [ x_{m-1}, x_{m-2} , .... x_1, x_0 \right ]$

最高有效字节 ：$x_{m-1}$ 所在的那个字节
最低有效字节 ： $x_0$  所在的那个字节

`0x1234567` 高位字节 ： 0x01 , 低位字节 ： 0x67

TIPS : 
1. 利用 `^` 的特性可以实现变量交换
2. 对于全1掩码来说,  推荐使用 `~0` 

*****

$$
A \oplus  B = (\bar{A} \cdot B) + (A \cdot \bar{B})
$$

异或具有交换性和结合性

*****

逻辑左移， 算数左移 ： 逻辑补0， 算数补低位(循环)

对于**有符号数** : 算数右移,  对于**无符号数** : 逻辑右移

