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

