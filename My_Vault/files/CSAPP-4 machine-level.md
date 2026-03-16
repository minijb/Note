---
tags:
  - csapp
---
.c -> .s -> .o -> .a

得到汇编代码

```sh
gcc -Og -S xxx.c
```

和c的区别

inter data of 1,2,3,8 byte

操作：在内存和寄存器中交换数据， 变换控制如(jump, condition branches)

objdump （工具）

常见寄存器

![Ac7sMWnbhpEi8kf.png](https://s2.loli.net/2024/07/10/Ac7sMWnbhpEi8kf.png)


%r -- 64
%e -- 32

![JEtgiwFGPc5Syj2.png](https://s2.loli.net/2024/07/10/JEtgiwFGPc5Syj2.png)


rsp / esp 栈指针

**moving data**

movq Souce,dest;

$ 立即数
% 寄存器 (rsp除外)
(xxx) memory


![gj5HRTSfmYO3xcI.png](https://s2.loli.net/2024/07/10/gj5HRTSfmYO3xcI.png)

一些操作

```txt

(R)  Mem[Reg(R)]
D(R) Mem[Reg(R)+D]

movq 8(%rbp), %rdx
```


![cZBwKeLGvUsgA51.png](https://s2.loli.net/2024/07/10/cZBwKeLGvUsgA51.png)

![w3By8azkgIsHhS6.png](https://s2.loli.net/2024/07/10/w3By8azkgIsHhS6.png)

Memory 操作

```txt

D(Rb, Ri, S)
Mem[Reg(Rb), + S * Reg(Ri) + D]

D :  offset 1,2,4,8
Rb : base rigister
Ri : index regester
S : Scale : 1,2,4,8 --- 默认为1


0x80(,%rdx,2) = 2 * 0xf000 + 0x80 = 0x1e080
```




`leaq src , dst` --- move 的变种

- src : 表达式
- dst ： 目标

leaq a(b, c, d), %rax 先计算地址a + b + c * d，然后把最终地址载到寄存器rax中

使用 ： 不适用 memory 引用， 计算地址

如 `p = &x[i];` `x + k*y` k = 1,2,4 or 8 

**双参数操作**

`addq , subq , imulq(*), salq(<<), sarq(>>), shr(>>), xor(^), and, orq1

`addq src, dst`

`dst = dst + src `

逻辑移位: SHL、SHR 算术移位: CAL、CAR

**单参数操作**

incq Dest  -- dst += 1
decq dest  -- dest -= 1
negq dest  --  dest= - dest
mptq dest  --  dest = ~dest

![e4GiUChHlMX9Q3W.png](https://s2.loli.net/2024/07/11/e4GiUChHlMX9Q3W.png)


## 控制

rsp ： 当前栈的指针
rip ： 当前代码的指针
CF，ZF，SF，OF

CF: Carry Flag
SF：Sign Flag
ZF: zero Flag
OF: Overflow Flag --- 无符号数溢出位

这些状态为还被用来比较 ： 

**cmpq Src2, Src1  -- 和 减法相似  src1 - src2**

> q 结尾： 64位数据进行操作 q：quadward 四字

CF : 用于 unsigned 比较
ZF : if `a == b`
SF : if `a-b < 0` signed
OF if two signed overflow


**testq src2, src1**  和 `a&b` 类似

ZF set when `a&b == 0`
SF set when `a&b < 0`

常用于一个参数使mask的时候

**使用状态码**

**setX** 设置单个寄存器为0/1

![600](https://s2.loli.net/2024/07/21/BJNx8AOEG2QfmFy.png)



> 直接使用最低位 
> ![600](https://s2.loli.net/2024/07/21/vEqRsofMU8Wcwdn.png)



![600](https://s2.loli.net/2024/07/21/JQtR96mK1LxgGXH.png)


mov指令有5中形式
源目的地址:立即数,寄存器,存储器
目的地址:寄存器,存储器
(存储器不能到存储器)
movl 传送双字
movb 传送一个字节
movw 传送两个字节

这里注意:
movsbl movzbl 指令负责拷贝一个字节,并设置目的操作数其余的位
区别在于:
movsbl源操作数是单字节,将24位设置位源字节的最高位,然后拷贝到双字目的中
movzbl 源操作数单字节,前面加24个0扩展到32位.然后拷贝到32位中.


常见寄存器：

1. rax : return value
2. rsp : stack pointer
3. rdi : 1st arg
4. rsi : 2st arg
5. rdx : 3st arg
6. rcx : 4st arg
7. r8  : 5st arg
8. r9  : 6st arg

64  - 32  - 16 - 8
rax - eax - ax - al
rsi - esi - si - sil

setg/l --->  有符号数
seta/b --->  无符号数


MOV :
- 第二个必须是地址
- 两个参数不能全为地址


movq 特殊情况：32位立即数 -> rax 会自动进行 signed extended
movabsq : 可以直接放64位的立即数
movl ： 高 32位会自动变为 全0

内存中，栈是从高到低 (倒立的)， 堆：从低到高
push  = sub + mov
pop = mov + add
栈指针 ： rsp

leaq ： 加载有效地址操作， 用于加法计算

IMM ： 因子只能是 1,2,4,8

**条件码寄存器** (ALU) : 记录一条指令执行后的状态, 每条指令后都会进行**覆盖**

CF : 进位标志位 Carry Flag  --- unsigned
ZF : 零标志位 zero flag
SF : sign flag 
OF : overflow flag 有符号数

一元，二元，移位，比较指令，会更新条件码寄存器

cmp , sub 的区别 ： cmp 不改变 Target ， 只更新条件码
test ， and 同理
test 作用 ： 测试数大于，小于，等于0
sete ： 将条件吗寄存器设置到 target (e : equal)
setl : l less


a < b : 需要使用 `SF^OF` !!! 

**特殊情况**
t  = a - b
a < b , t > 0 此时溢出， SF = 0 ， OF = 1  `SF^OF = 1`
a > b , t < 0  移除  SF = 1 ， OF = 1 `SF ^ OF = 0`

![image.png](https://s2.loli.net/2024/12/13/AEn7VCxoacOfvbM.png)

![N7DS5fmFxXZdTWh.png](https://s2.loli.net/2024/12/13/N7DS5fmFxXZdTWh.png)

cmovege  c: conditinal,  ge : >=， 条件转移指令
分支预测--- cmove 可以避免分支预测提升效率

cmovg， cmovege，cmovl, cmovle

switch: 实现的跳转表，帮助跳转， 只有一次跳转命令。 if else 会存在多次的 cmp 和 jmp


机器码翻译 if

```c
if(t){
	a
}else{
	b
}


if(!t) 
goto b
a : ccc
goto done

b: xxx

done:
```

while 的两种跳转方式 : 

- 跳到中间 -- 先跳到结尾进行判断,再跳到中间进行循环
- gearded-go -- 先判读 !t, 随后进行循环,循环结尾再进行 t的判断跳转

**汇编指令**

**`.data`**，定义data section，保存程序的全局和静态数据，可读可写。
**`.text`**，定义text section，保存代码，只读和可执行。
**`.section .rodata`**，定义只读数据区（必须带上.section前缀）。

**switch** : 存在一个跳转表因此速度较快

**Call** 命令 : 会自动在rsp -- 栈中进行 push 

rsp = rsp -2 , 值指向call的下一条命令

ret 的时候,  PC跳转到 rsp 指向的地方, rsp = rep + 2 

> rsp 中, 调用的函数都有栈帧. 内部存放下一个返回地址, 以及超过6个的参数, 保护的寄存器

栈内 **传递参数的时候** 的最小单位为 : 8B--64bit . 所有大小都会向8取整!!!!

- **局部变量是存放在栈帧中** 
- 同时如果一个运算符需要进行取地址操作,也需要放到栈内.


P172 : **注意对局部变量存储时大小没有要求, 而传递的参数大小需要是8的倍数.**

![dd](https://cdn.acwing.com/media/article/image/2021/09/29/85607_ac8f06b320-3.png)

注意 :  作为参数的部分只有 arg 7,8 ,其他的存储在寄存器中.
因此只有 7,8 进行了对齐,其他没有.

### 调用者保护和被调用者保护

https://blog.csdn.net/Edidaughter/article/details/122334074

- 调用者保护, 在外层函数保护    
- 被调用者保护, 子啊内存函数保护

rbx 就是一个被调用者保护寄存器

### 数组和指针

**定长数组**

一个变量的基本组成方式 ： 1. 地址值 2. 变量值

$$
\&D[i][j] = D_{x} + L(C \cdot i + j)
$$


`int A[5][3]`

```txt
X_a : rdi, i : rsi, j : rdx 
leaq (rsi, rsi, 2), rax   -- rax = 3rsi = 3i
leaq (rdi, rax, 4), rax   -- rax = 4*3i + X_a = 12i + X_a
movl (rax, rdx, 4), rax   -- rax = M(12i+4j+X_a)
```


定长数组可以根据原始 长宽 和 i,j 进行快速定位

每次跨行、列的定位会在编辑阶段转换为常数， 因此速度很快

**变长数组**

`func(int x, int y, int A[x][y])`

注意产犊必须在数组 A 之前。

![UvTjfW4VHuYc2Lg.png](https://s2.loli.net/2024/12/30/UvTjfW4VHuYc2Lg.png)

注意需要进行一次计算。

**两者对比**

![xjimWRdYhz3eDK7.png](https://s2.loli.net/2024/12/30/xjimWRdYhz3eDK7.png)


**struct**

字节对齐规则：

1. 

![rZWkDsfPJCNBLz8.png](https://s2.loli.net/2024/12/30/rZWkDsfPJCNBLz8.png)

`x / k ` 能除的进。

2. 考虑 ： 结构体数组 

结构体之间也需要对齐。 一般是对8字节

> 调整顺序 会改变 struct 类型的大小


**Union**

互斥体 ： 大小为变量中最大的

![wtZaWQixGlURsV4.png](https://s2.loli.net/2024/12/30/wtZaWQixGlURsV4.png)

节约空间。

![kt71KARV6LZa8Mu.png](https://s2.loli.net/2024/12/30/kt71KARV6LZa8Mu.png)

![4nLbYxJKt9wHopS.png](https://s2.loli.net/2024/12/30/4nLbYxJKt9wHopS.png)

可以用于类型转换。

### Buffer Overflow

gets : 根据输入总到 buf (字符数组)中 -- 无法判断buf大小。 

字符数组作为局部变量会多分配一些空间 

![HfyA5vQBhL1F89g.png](https://s2.loli.net/2024/12/30/HfyA5vQBhL1F89g.png)

![AMWHt7zDsO83d4v.png](https://s2.loli.net/2024/12/30/AMWHt7zDsO83d4v.png)

如果超过一定范围， 就会造成返回地址不确定。 本质就是覆盖 返回地址。

Thwarting Buffer Overflow Attacks

1. Stack Randomization
2. Stack Corruption Detection 栈破坏检测 -- use canary（金丝雀/哨兵）
3. Limiting Executable Code Regions


**Stack Corruption Detection**

![wDaX7dI2z8PixsK.png](https://s2.loli.net/2025/01/02/wDaX7dI2z8PixsK.png)


检测到 canary 被修改会报错。

`%fs:40`  指向内存中的特定位置， 其中40为偏移量 --- 只读

![rhfCZcO5u83pgaE.png](https://s2.loli.net/2025/01/02/rhfCZcO5u83pgaE.png)


**Limiting Executable Code Regions**

![olNZW8d1ptKXxcO.png](https://s2.loli.net/2025/01/02/olNZW8d1ptKXxcO.png)




