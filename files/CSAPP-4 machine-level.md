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

19.44