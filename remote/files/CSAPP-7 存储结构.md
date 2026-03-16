---
tags:
  - csapp
---
循环展开 --- 多使用并行，少使用函数，减少内存访问


## cache

高速缓存 --- CPU和内存之间的

- 寄存器
- L1  L2  L3  高速缓存  SRAM --- 持久性
- 内存  DRAM --- 没有持久性
- 硬盘-固态
- 远程

![700](https://s2.loli.net/2025/03/14/rMsucmIOUxj6akt.png)


和 内存控制器 连接。

1. 发送行地址 --- 读取到 行 buffer 中
2. 发送列地址 ---  从 row buffer 中返回具体的内容

地址越大，引脚越多。

![700](https://s2.loli.net/2025/03/14/a2gkdsecOy6WS3p.png)


![700](https://s2.loli.net/2025/03/14/asugBkWl2UCNPDA.png)


DDR  --- DRAM
LP  --- LOW POWER


固态

![700](https://s2.loli.net/2025/03/14/YjkO1XgRNe4WxMQ.png)


![700](https://s2.loli.net/2025/03/14/AvfI3UNCo16kxyD.png)

![700](https://s2.loli.net/2025/03/14/2lxGyn14wKdrICE.png)


FTL 有部分不需要擦除的，  会先将其移动到其他地方。

局部性原则 ： 时间/空间局部性

行优先 >  列优先 ---- 内存那一层

- cache hit
- cache miss


![700](https://s2.loli.net/2025/03/14/LZHx1Uoqh6ElwJ2.png)

![700](https://s2.loli.net/2025/03/14/iXWLtFgsYqSmlEK.png)

地址 ： 划分为三部分 ： 

![700](https://s2.loli.net/2025/03/14/JqjsPvLCugXYE3K.png)


组在中间？ - --- 对局部性的程序不友好 --- 刚好以4为一跳

![700](https://s2.loli.net/2025/03/14/caQ6iD9tvBO8WSH.png)



## 高速缓存


如何选择

- set selection 组选择
- line matching 行匹配
- word extraction  字抽取


![700](https://s2.loli.net/2025/03/15/OyVszunqFY3UPwS.png)


物理地址 分为三部分 ： tag  set offset

5位 --- $[0,2^5-1]$


![700](https://s2.loli.net/2025/03/15/J5PElA8NRC3OpSf.png)


- 查找 valid 是否为1  - 0 则无效
- 查找并对比 tag 位，

![700](https://s2.loli.net/2025/03/15/DLlKnyvHwMgeC8Y.png)


block offset  偏移量为4字节

tag 不一致则需要进行替换


![700](https://s2.loli.net/2025/03/15/BhFreRVqH3Pt9lo.png)


m为4位。 2个位 -- set ，   offset -- 1位，    tag 1位

![700](https://s2.loli.net/2025/03/15/HeNV5CKbEBdkJcQ.png)


![700](https://s2.loli.net/2025/03/15/uydSYOoBcferqRw.png)


**具体步骤**

![700](https://s2.loli.net/2025/03/15/MtYuIa6jeBP9VRJ.png)
![700](https://s2.loli.net/2025/03/15/A6L2TD7ZUvgK8SO.png)
![700](https://s2.loli.net/2025/03/15/gitJC8kfc1zTZ5v.png)




**冲突 miss 的例子**

![700](https://s2.loli.net/2025/03/15/59HjYNeSVWgoM73.png)


![700](https://s2.loli.net/2025/03/15/YSW2jFHI7CtJRQk.png)

![700](https://s2.loli.net/2025/03/15/aLWgo4Nj82eS9Du.png)
冲突--- cache 会进行替换！！！ ---- cache 抖动

将 y映射到  set 1 中！！！！。  --- 就不存在冲突


![700](https://s2.loli.net/2025/03/15/zRkmT9DpfgOJIls.png)


### 另一种方式 --- 组相连

2路组相联，  组内的多少行 cache

![700](https://s2.loli.net/2025/03/15/S9QKCjrxUu3MdGm.png)


行匹配稍微不一样 ： 

![700](https://s2.loli.net/2025/03/15/HkNWyXMdACwxstP.png)


- 找到 tag 相同 同时 valid 也位 1  则命中
- 随后进行抽取

### 替换算法

- 随机替换
- 最不常使用
- 最近最少不使用 LRU

### 全相联cache  -- 用于容量小的 cache

E= C/B  全相连cache


### 写

- 写命中
	- 写穿透  -- 写到 cache -> 内存
	- 写回  -- 但此行数据需要被替换的时候才写回到内存。 此时需要额外一个 数据位！  -- 脏位。
- 写不命中 不在 cache
	- 写分配 -- 先读到cache  然后修改
	- 写不分配 -- 不读到cache  直接写内存

写分配 -- 写回
写不分配 --- 写穿透


**i7** cache

![700](https://s2.loli.net/2025/03/15/O91tucl8DGTEy5b.png)


L1 分为 数据和命令 cache 
L2 共有 (一个核共有)
L3 CPU 贡献


L1缓存每个核上有两个缓存，一个用于存储数据（Data Cache），一个用于存储指令（Instruction Cache）
L2缓存的存储容量比L1缓存的存储容量大，存储速度比L1小 --- 指令和数据共享同一个物理缓存
L3缓存的存储速度最小，但存储容量最大，L3缓存是由所有CPU物理核心共享的。