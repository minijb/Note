---
tags:
  - csapp
---
## 指令系统结构


Y86 -- 精简的 X86


程序员的可见状态  -- 少一个 r15 寄存器
少了一个条件位
PC -- 执行的地址
Stat 
Memory


mov -- reg -> reg , $ -> reg , reg -> mem , mem -> reg  （mem to mem is error）

Y86 : rrmovq , irmovq, rmmovq , mrmovq


![700](https://s2.loli.net/2025/02/02/jbWiICao1ZsMV4T.png)


为什么少 r15 --> 8bit 表示两个寄存器 一个就是 4 bit F 表示 没有寄存器， 因此必须少一个

![700](https://s2.loli.net/2025/02/02/RZyX4sfOPMmAKDz.png)


![700](https://s2.loli.net/2025/02/02/V7K2vhrgnXZ4elN.png)

![700](https://s2.loli.net/2025/02/02/l2ucSKWsG5DTALN.png)

![700](https://s2.loli.net/2025/02/02/jncfpS5T6kOEJBd.png)

![700](https://s2.loli.net/2025/02/02/jWymgA3OzcraNnY.png)

![700](https://s2.loli.net/2025/02/02/2pfynbxLMXqt3PF.png)

![700](https://s2.loli.net/2025/02/02/jBJPuMtFrZy4xDg.png)


**Stat**

![700](https://s2.loli.net/2025/02/02/Tlb7P3x8Ohzk6pr.png)


## 数字电路

![700](https://s2.loli.net/2025/02/02/PtEbSTXGM8RAhuz.png)


![700](https://s2.loli.net/2025/02/02/yn128gsPVImfxOd.png)


PN  可以做成逻辑电路 --- CMOS


![700](https://s2.loli.net/2025/02/02/hYAuDKwvbdnW1Ic.png)



![700](https://s2.loli.net/2025/02/02/BCcxydTutSqIoaD.png)


使用硬件描述语言进行表示 ：

![700](https://s2.loli.net/2025/02/02/v84qQoyxweZj5YT.png)


![400](https://s2.loli.net/2025/02/02/9EMfPYawTjGqKpZ.png)


组合逻辑 vs 时序逻辑(有时序)

![500](https://s2.loli.net/2025/02/03/poTySsVtIO1Km5v.png)

![500](https://s2.loli.net/2025/02/03/lSLe4DPovhtpjOH.png)


硬件描述文件。

总结：

USTC Verlog OJ

![500](https://s2.loli.net/2025/02/03/Dod6tNWLsvUQuz1.png)

## Y86 顺序实现


![700](https://s2.loli.net/2025/02/03/Sz37PNOgy2HQFxi.png)


![700](https://s2.loli.net/2025/02/04/ZidOFpIPWawvkez.png)



**CPU处理汇编代码基本过程**

一条指令

- Fetch ： 取指令阶段
- Decode : 译码阶段
- Execute ： 执行阶段
- Memory ： 访存阶段
- wrtie back ： 写回阶段
- 更新PC


**Fetch state**

获取指令 ： 变长 --> 指令长度不一致


![700](https://s2.loli.net/2025/02/04/3PyldtrqzjfpJSe.png)


I-cache -- Instruction memory 存储指令的地方

**Decode Stage**

读寄存器

![700](https://s2.loli.net/2025/02/04/3lURaOQy6zc8PI7.png)


**Execute Stage**

ALU  算术逻辑单元

![700](https://s2.loli.net/2025/02/04/TFzUqMkRsZrEbg2.png)


算术 ， 计算地址 ， push/pop -- rsp指针的计算

CC 条件吗寄存器

**Memory Stage**

内存写和读

**write back**

写回寄存器



![700](https://s2.loli.net/2025/02/04/xHaUoZL9GOmewEY.png)

![700](https://s2.loli.net/2025/02/04/tCayBPQ1MoRciJX.png)

![700](https://s2.loli.net/2025/02/04/itRmO5DfKTJC4yM.png)

![700](https://s2.loli.net/2025/02/04/uqdoH8hAbvk72sD.png)


**Push**

![700](https://s2.loli.net/2025/02/04/2OdYqUG7jPiuFKr.png)


**cmp**

![700](https://s2.loli.net/2025/02/04/XCGQUcPel6FYdRN.png)


跳转有两种形式。


## 硬件实现

**Fetch  阶段**

Instruction Memory --- 指令的存储部件

根据 PC 的值 取指令。

- Y86 -- 变长 ， 一次取10个字节。
- 进行切分 ： split + Align
	- 根据 icode  0-B 指令是否有效 并判断 是否有常数位，寄存器位。 (依据此来判断命令长度)
- 剩下9个字节。
	- 有常数/寄存器，则进行解析
	- 没有则继续下一条命令

![700](https://s2.loli.net/2025/02/07/1lmwjvcoUh73I4r.png)



**Decode stage**

还需要 icode 指令。  因为需要 push 这种指令，还需要rsp (指令没有 rsp 指令)。 其他还有 call 等


![700](https://s2.loli.net/2025/02/07/rRu7dD9GW5y2MEL.png)


**Execute Stage**

ALU : 算术逻辑单元 ： 计算地址

add， sub， push， pop


![700](https://s2.loli.net/2025/02/07/sk91n7ZmRJD8P4z.png)


valC : IRMOVQ，RMMOVQ  -- 需要使用 ValC

call , push : -8
IRET , IPOP : 8

icode 根据 CC 选择是否执行

jmp 根据 CC 和 icode 选择是否执行

![700](https://s2.loli.net/2025/02/07/gLDI9naWuAdFoSG.png)


**Memory Stage**

读写内存

- 根据 icode 判断是读还是写， 读只要 地址， 写还需要 数据
- valP ： call 指令 ： --- 返回地址压栈 因此需要一个 valP 返回地址
- valE ： 地址
- valA ： 数据
- Stat ： 状态 

![700](https://s2.loli.net/2025/02/07/ZLpKmhUdi8HrVtA.png)


**PC Update Stage**


![700](https://s2.loli.net/2025/02/07/qFuxOBRp19EXsng.png)


- 默认情况下根据 icode 就可以判断了。
- call ： 根据地址进行跳转 ValC/顺序ValP
- cnd ： condition 哟关于 jxx 跳 先择 ValC ， 不跳 ValP
- ret ： ValM 到内存中读取一个地址并跳转


## 整体设计


![700](https://s2.loli.net/2025/02/08/tqoUgxVGZ1vuwhn.png)



General Principles of pipelining

![700](https://s2.loli.net/2025/02/08/HIl1KB7DmvzUnNo.png)


reg ： 时钟寄存器。   

**时钟寄存器**

时钟到了才会修改值

![700](https://s2.loli.net/2025/02/08/pXnDCZkRHVKWPMv.png)


吞吐量 ： 1s 可以执行的命令的条数

![700](https://s2.loli.net/2025/02/08/bmwTJ2kAeLiYr3z.png)


使用分阶段的方法提高吞吐量

![700](https://s2.loli.net/2025/02/08/Kpu5JLMtPkUlDN8.png)


![700](https://s2.loli.net/2025/02/08/kGNiQY7PbuUFvl8.png)


![700](https://s2.loli.net/2025/02/08/BNkHjvSaKf7AIzp.png)


![700](https://s2.loli.net/2025/02/08/3wTJV7tzQsyr9aD.png)

**如果每个阶段的时间不一样**


![700](https://s2.loli.net/2025/02/08/sNI8ZqY1aOg5SCP.png)

**划分更多的阶段**

![700](https://s2.loli.net/2025/02/08/R1oqZXb3mAtaskr.png)


**控制依赖**  jmp 这种命令需要按照前一条命令的cc来运行。


![700](https://s2.loli.net/2025/02/08/LBKMeo8ZdI1pRrc.png)

## 流水线

![700](https://s2.loli.net/2025/02/09/Q94f2bBXVorR3av.png)


### predict select PC


多了预测PC的阶段。 同时之间多了一些寄存器进行存储。

![700](https://s2.loli.net/2025/02/09/dSGICn5pEMohgwl.png)


![700](https://s2.loli.net/2025/02/09/YFzArqtZKfRC9Uy.png)

**问题**

![700](https://s2.loli.net/2025/02/09/MV4KW1ok63J5yaD.png)

## 数据冒险

访存阶段，才会写回 rdx。 **数据冒险/冲突** --- 计算结果错误。

方法1 ： 进行等待。

![700](https://s2.loli.net/2025/02/09/qhS4VY1sK6PRaEw.png)


方法2 ： fwd 旁路方法  --- 无需暂停  --- 需要额外判断是否冒险

![700](https://s2.loli.net/2025/02/09/TP7rawA28iqceLO.png)


**fwd 方法无法解决所有问题**

![700](https://s2.loli.net/2025/02/09/tXkTeALjEJ3Py78.png)


部分操作内存的命令，无法通过前递解决。

M ： 访存的时候  此时 add 处于 计算阶段。 无法拿到数据。！！！ -- 至少等一个周期。


## 控制冒险

执行 jxx ret 这些指令的时候，下一条指令可能不确定。 ---- 

![700](https://s2.loli.net/2025/02/14/N1XvQ4peg2ahuSo.png)


分支预测 ： 总是预测跳转，或者总是预测不跳转。


预测错了 怎么办？ --- 只要不是执行阶段就不会产生影响

![700](https://s2.loli.net/2025/02/14/B3MWD675UamLOb1.png)


0->1 的时候 时钟寄存器才进行输出

![700](https://s2.loli.net/2025/02/14/flwN5QMz1ta6yxc.png)


stall = 1 , 时钟到了也不变化。 bubble = 1 --- 将寄存器清0， 不能同时为1.

**组合命令导致的控制冒险**

![700](https://s2.loli.net/2025/02/14/AmKSqaHCLh4pevk.png)


读的时候， mrmovq 还没有读取内存。 -- 转发太迟了

![700](https://s2.loli.net/2025/02/14/OZlTQepfxBU1IPY.png)


![700](https://s2.loli.net/2025/02/14/KmOfloNXHLdC7Eg.png)


在 exe 中插入气泡 ， 进行暂停。

**分支预测错误**  --- 在 Fetch 之后插入 两个 bubble 。

![700](https://s2.loli.net/2025/02/14/rLXIacuEqlo5bBw.png)


![700](https://s2.loli.net/2025/02/14/7d2DUoswXA1HiFK.png)




**ret  需要3个气泡**


![700](https://s2.loli.net/2025/02/14/3VoU6riGlwYZ7H8.png)



**跳转 和 ret 组合  跳转错了**  ： 1个暂停， 2个气泡


![700](https://s2.loli.net/2025/02/14/AOoErUTyKX1zinq.png)


**mrmovq 和 ret**


 ![700](https://s2.loli.net/2025/02/14/jBh7ZDFiJabSCns.png)


## CPI  cycles  per Instruction


每条指令需要多少时钟周期。


![700](https://s2.loli.net/2025/02/14/HSZLKnaU761b8zk.png)


