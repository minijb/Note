
## 可重定位目标文件

源代码  --- 编译 ----  可执行文件

- 预处理 -- 头文件整理，宏处理  `.i` 文件
- 编译 -- `.s`  汇编文件
- 汇编 -- 翻译成二进制文件 --- `.o` 可重定位目标文件
- 链接 -- 链接 `.o` 形成 可执行文件


![700](https://s2.loli.net/2025/03/15/dmMFjeW5vNwVo3r.png)


![700](https://s2.loli.net/2025/03/15/5psiUPd8jlJQuTF.png)


![700](https://s2.loli.net/2025/03/15/KbLSuRPIdZEJUrk.png)

![700](https://s2.loli.net/2025/03/15/RNIdoLkQu6j84g7.png)


![700](https://s2.loli.net/2025/03/15/XEWdFoJkaA1r8jS.png)

![700](https://s2.loli.net/2025/03/15/cVJalLYm3xkNj7R.png)


![700](https://s2.loli.net/2025/03/15/eEqfXucwNAUTmsn.png)

### relocatable object file 可重定位目标文件


![700](https://s2.loli.net/2025/03/15/pHgjkvbrdfZJGm8.png)

![700](https://s2.loli.net/2025/03/15/SBf6Frzx53ovY2Q.png)



### ELF

![700](https://s2.loli.net/2025/03/15/htaW1C7DMbidjLN.png)


- ELF header
- Section
- Section head table

`readelf -h main.o`  查看 elfheadr

![700](https://s2.loli.net/2025/03/15/6on37kxtZFdaQLh.png)


Magic ： 元数据

![700](https://s2.loli.net/2025/03/15/3nKG5R1xJevOTQZ.png)


ELF 大小

![700](https://s2.loli.net/2025/03/15/gvVARcq52SoOnLe.png)


13个 section header 每个 64bit

![700](https://s2.loli.net/2025/03/15/dw1QBlj9u7SfVhA.png)


![700](https://s2.loli.net/2025/03/15/ufXb6l9CPY4px15.png)

## 符号表

ELF 可执行可链接格式 

text / data  代码段   内容 ： 就是编译生成的二进制指令

![700](https://s2.loli.net/2025/03/15/MuJqDEepCvy2iYc.png)


![700](https://s2.loli.net/2025/03/15/duFEBns7HWrlZAJ.png)


data section  --- 数据 ： 经过初始化的**全局变量**和经过初始化的**静态局部变量** --- 注意 ： 这里是 count 和 a   注意 ： 小端法存储

![700](https://s2.loli.net/2025/03/15/3TqFowLd1zubnvN.png)

bss section  ---  Better save space  --- 占位符 不占用磁盘空间

rodata --- read only data， 字符串常量。  switch 跳转表

![700](https://s2.loli.net/2025/03/15/fy1xpHZe4FIcB3t.png)


![700](https://s2.loli.net/2025/03/15/UkF7ITd9ZrnLBJu.png)



symtab --- 符号表 --- 将多个可连接文件进行链接的主要工具

![700](https://s2.loli.net/2025/03/15/SrV4KWGlPYTbj8A.png)

![700](https://s2.loli.net/2025/03/15/vAnkKiI8YMz3tbh.png)

Type 类型  Bind 全局还是局部  Ndx 所处 section 的索引  value 起始位置，  size 大小 --- 得到函数所处在 elf 文件的位置。


**printf** --- value size  == 0 Type : NOTYPE   --- 链接的时候需要找
**value** --- COM
- bss  ---- **未初始化的静态变量** ， **初始化为0的全局/静态变量**
- COMMON --- 未初始化的全局变量


a，b  符号的修饰 --- 局部静态变量 
a  NDX 3 --- data
b  NDX 4 --- bss

还有一些  没有符号名 ---- 则 NDX 指向的值一样。

![700](https://s2.loli.net/2025/03/15/dNteuq6Z13kMxfL.png)


局部变量(非静态) --- 通过运行时的栈来保管。

Symbols:
- 全局符号  函数
- 外部符号  外部符号
- 局部符号 
	- static



## 静态链接 + 符号解析


```c++
void foo(void);

int main()
{
	foo();
	return 0;
}
```

Ndx UND -- undefine

![700](https://s2.loli.net/2025/03/15/dNteuq6Z13kMxfL.png)


此时报 链接错误。 ld return 1 ；

- **Strong symbols**   函数和已初始化的全局变量
	- 强符号 只能出现一次。
- **Weak symbols**   未初始化的全局变量
	- 弱符号可以出现多次。


![700](https://s2.loli.net/2025/03/15/9ZaIMzJuwmkhTCl.png)

类型不一样，但是命名相同

![700](https://s2.loli.net/2025/03/15/qnTU1jcALuG75tb.png)



### 静态库

一种称为存档的特殊文件格式 


![700](https://s2.loli.net/2025/03/15/YSMvL1bftQ7548C.png)


![700](https://s2.loli.net/2025/03/15/du9ie4ZXtQYRr1E.png)


![700](https://s2.loli.net/2025/03/15/eNA8bFQdGPrsqX3.png)


![700](https://s2.loli.net/2025/03/15/SY8MpHJOax5jWmv.png)


![700](https://s2.loli.net/2025/03/15/5K3uNawePdZxIvW.png)



### 过程

三个集合  

- E ： `.o` 文件
- U ： undefined
- D ： defined


- 未定义需要查找
- 定义的则存储

![700](https://s2.loli.net/2025/03/15/PhSf1ywmRVeUkaH.png)


这里  libvector.a 中有 add.o mul.o --- 这里不需要 mul 函数 因此

因此将 add.o 加入到 E 中，但时 mul 不加入 E 

然后 U 中 删除 addvec 

![700](https://s2.loli.net/2025/03/16/4CiOw8ITX19VyRu.png)


addvec.o 加入也同理。


![700](https://s2.loli.net/2025/03/16/916Jk4KMPWjaTt5.png)

**一旦 集合U中还有为定义的符号，则说明含有未定义的函数/全局变量**  此时报错 ld error

注意，输入到连接器时要有顺序的， 顺序从左到右。

![700](https://s2.loli.net/2025/03/16/FiK9ShHxDzoU4kR.png)

这里会先分析U是空的。此时加入 main.o 就找不到 addvec函数

![700](https://s2.loli.net/2025/03/16/VWIzbSOEyZh9YBJ.png)


此时 相互调用 --- 此时需要两个 libx.a.

## 重定位

将三个.o文件生成可执行文件

![700](https://s2.loli.net/2025/03/16/vapTdJ6O279Gzy4.png)


![700](https://s2.loli.net/2025/03/16/lwzCvWdfZnpaLHN.png)


第一步 ： 将相同的节合并

![700](https://s2.loli.net/2025/03/16/qdeRSw14hg7YLtZ.png)


第二步： call sum --- 没有目的地址， 暂时用0进行填充

![700](https://s2.loli.net/2025/03/16/tHWzqQPhXj3DM8K.png)


用到的数据结构：  offset ， type ， symbol ， addend 

有两种方式 ： PC相对地址， 绝对地址

指导起始地址。


![700](https://s2.loli.net/2025/03/16/T1Q5KtB8Uj6uw9f.png)


![700](https://s2.loli.net/2025/03/16/dxRXaCSBkbMufrF.png)

--- 根据符号表 进行寻址
PC相对寻址方法是 
- ref_addr = main + offset 开始地址。
- ref_ptr = sum - ref_addr + r.addend  --- 计算间隔

![700](https://s2.loli.net/2025/03/16/CV3RdGYaLXxB6lb.png)


绝对寻址： data section 内的地址得到。

![700](https://s2.loli.net/2025/03/16/L29UrlwQNJkmqde.png)


> 根据符号表进行符号解析


![700](https://s2.loli.net/2025/03/16/QWTCJoB5A9Vks7g.png)


![700](https://s2.loli.net/2025/03/16/ROfAYeEwI15G6vy.png)


![700](https://s2.loli.net/2025/03/16/mvgCLnh65rFORVa.png)


bss  better save section --- 未初始化的全局变量会放在这里。

![700](https://s2.loli.net/2025/03/16/WZqN7UyuOpAYdGe.png)


![700](https://s2.loli.net/2025/03/16/oicUfesnHvENL1K.png)



CTRL--- c runtime



## 动态链接

静态库的问题 ： 
- 静态库需要定期维护升级
- 所有C函数都使用标准IO函数---内存中有多个备份


Shared Libraries  `.so, .dll`

![700](https://s2.loli.net/2025/03/16/L8whUj5nz96Fp4E.png)


提取可重定位和符号表信息

![700](https://s2.loli.net/2025/03/16/53wkHc2VhxlJYug.png)


执行的时候，需要用到动态连接器的部件，调用在内存中存在的共享库文件。


![700](https://s2.loli.net/2025/03/16/itVGAd1uEO3XoNY.png)

**如何使用动态库**

![700](https://s2.loli.net/2025/03/16/q5THga69VBQXoNm.png)


![700](https://s2.loli.net/2025/03/16/oehk6fCQFrUT7sW.png)


call : 
- PC 压栈
- PC = PC + offset  (目的地址 - 当前地址)

> 重定位 ： 将替换原本的值， 就是 call 000000 这些  分为绝对和相对