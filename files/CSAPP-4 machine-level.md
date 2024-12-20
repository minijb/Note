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

