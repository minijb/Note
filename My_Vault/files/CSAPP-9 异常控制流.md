---
tags:
  - csapp
---
## 控制流

![700](https://s2.loli.net/2025/03/19/gTVvfJndSktZY2e.png)


顺序执行，跳转，非正常的控制流变化。

从磁盘读文件 cpu - cache - memory - disk， 此时会进行进程切换，读取完成会打断现在的进程，并执行原本的进程。

![700](https://s2.loli.net/2025/03/19/2Gip9K1cPlvQAsL.png)


### 异常处理

异常处理表 --- 数据结构 --- 启动的时候创建


![700](https://s2.loli.net/2025/03/19/5PIwqFVAYc7b2G8.png)

异常寄存器

![700](https://s2.loli.net/2025/03/19/nZVTSLJYhMisqyz.png)


![700](https://s2.loli.net/2025/03/19/GxRStHnVyhcQ1Ud.png)


![700](https://s2.loli.net/2025/03/19/gJndiYfSWpwZQom.png)


![700](https://s2.loli.net/2025/03/19/QFj4NPMhr1vGZT7.png)


异常分类 ：  中断， 陷阱， 故障， 中止。

中断 ： IO 信号  -- 引脚

![700](https://s2.loli.net/2025/03/21/zBRjlN95ibyXvae.png)



陷阱：故意的异常  使用声卡这些， 向操作系统申请服务

![700](https://s2.loli.net/2025/03/21/zNTM2KdneLYxG4B.png)



故障 ： 访问数据   缺页故障  保护故障


![700](https://s2.loli.net/2025/03/21/5rSXFRPnZTsQ4Dy.png)


中止 ： 硬件错误

![700](https://s2.loli.net/2025/03/21/WvoOYr9EFXifSby.png)



![700](https://s2.loli.net/2025/03/21/AMOe5C9Iuo1sztL.png)


![700](https://s2.loli.net/2025/03/21/NsGozOxAwQL3H7C.png)

![700](https://s2.loli.net/2025/03/21/tm7Jp1jWE5nlgse.png)


系统调用 ： rax 调用系统调用号    ，  其他对应参数的寄存器。



## 进程  Processes

**抽象**
- 程序独占的使用处理器
- 程序独占的使用内存系统

![700](https://s2.loli.net/2025/03/21/InaP5q2kXcRTCJK.png)


用户态 ： 受限制
内核态 ： 不受限制

读文件 ： 发起IO操作 --- 此时就需要切换到内核态

如何进入内核模式  `read`。

除了陷入等 ， 中断也会让程序进入内核态。  ---- 怎么切换 --- cpu 内部有一个 **control register 控制寄存器** --- 来改变当前的模式

### Context 上下文


简单来说就是运行状态
- 普通寄存器，浮点寄存器
- pc， 栈， 状态寄存器
- 内核栈， 内核数据结构(打开的文件)


### 上下文切换


- 保存当前进程的上下文  --- 保存到内核栈中
- 恢复抢占进程的上下文  
- 控制传递个新恢复的进程

![700](https://s2.loli.net/2025/03/21/kta1AKZFLnRYUJl.png)


### 进程的状态

--- 程序员视角


- Running ，  
- Stopped， （暂停）
- Terminated  

 ![700](https://s2.loli.net/2025/03/21/i6HFNnevL9EW4jM.png)
 
![700](https://s2.loli.net/2025/03/21/ZIiFj6vYmSgRrAd.png)


![700](https://s2.loli.net/2025/03/21/HymS9Na3lTno8bd.png)


![700](https://s2.loli.net/2025/03/21/1TxojW5BhKLrMwV.png)


在fork执行之前， 是一样的， 之后就不一样了。

![700](https://s2.loli.net/2025/03/21/o5K6QykJAjtznNr.png)

1. 在父进程中，fork返回新创建子进程的进程ID；
2. 在子进程中，fork返回0；
3. 如果出现错误，fork返回一个负值；

## execve 和 shell

zombie  --- 不运行的了但是还占资源

![700](https://s2.loli.net/2025/03/21/CMi325uzJGxQB4E.png)

![700](https://s2.loli.net/2025/03/21/C9jRsNaedKv47np.png)

![700](https://s2.loli.net/2025/03/21/MRgVp5UwKeGqdTI.png)

![700](https://s2.loli.net/2025/03/21/XYUlyQZaC453eBd.png)


![700](https://s2.loli.net/2025/03/21/dBrneZcifxSGEMl.png)


![700](https://s2.loli.net/2025/03/21/hOuLN89AwfnbBmH.png)


![700](https://s2.loli.net/2025/03/21/Yibn3M6By9Nr47P.png)


![700](https://s2.loli.net/2025/03/21/cPSYquthLrQOl9f.png)

![700](https://s2.loli.net/2025/03/21/VcqBSPyh84UAGxQ.png)


eval  分析字符串

![700](https://s2.loli.net/2025/03/21/614n7K9CN2R8HEx.png)


parseline  --- 解析字符串

- 删除开始的空格

![700](https://s2.loli.net/2025/03/21/UOMXNpBfgD3Wco9.png)


是否是内置的命令。

![700](https://s2.loli.net/2025/03/21/5GCIW3nDRAPmhls.png)


![700](https://s2.loli.net/2025/03/21/hBUe8IkM1KPzjq4.png)


后台运行。

## 信号

![700](https://s2.loli.net/2025/03/22/bqotFxBjkUsdvwz.png)


简单来说就是通知进程。。。。。

**信号处理**

![700](https://s2.loli.net/2025/03/22/lHqYvgkVr6zsxa2.png)


**发送信号**

- kill 命令
- 键盘
- 发送 kill function
- 使用 alarm 给自己发送信号

**进程组**

父进程创建子进程  ----  父子默认属于一个进程组  pgid --- 进程组id

![700](https://s2.loli.net/2025/03/22/p3egaWCsvPSzk7c.png)


![700](https://s2.loli.net/2025/03/22/emKBRit4PqM6VbC.png)

![700](https://s2.loli.net/2025/03/22/coxN5ACSKheDjRs.png)


使用 kill 函数发送信号 


![700](https://s2.loli.net/2025/03/22/mNkGl4y5Q1Pi8od.png)


![700](https://s2.loli.net/2025/03/22/SAZDBEKLNmrlux7.png)


![700](https://s2.loli.net/2025/03/22/J5AF96K8pfcox3u.png)

### 处理信号

待处理信号， 待处理信号结合


![700](https://s2.loli.net/2025/03/22/RQbuHqTXMhJgnEj.png)


从内核模式回到用户模式的时候就需要处理 待处理信号集合

![700](https://s2.loli.net/2025/03/22/rkDt3OdFBQA16LR.png)



### 接受信号的执行

![700](https://s2.loli.net/2025/03/22/M98AjRZ42pIDKHE.png)


![700](https://s2.loli.net/2025/03/22/N8zBvJVwm5MLgEf.png)

![700](https://s2.loli.net/2025/03/22/mINA1Lp6fsHSO8Z.png)


![700](https://s2.loli.net/2025/03/22/kSroyWFf9nuBhHz.png)


### 隐式阻塞， 显示阻塞  ---- 屏蔽

![700](https://s2.loli.net/2025/03/22/1dVS2JjaQU6A47P.png)


隐式的 --- 和之前差不多。


正在处理s，则收到s放入阻塞集合。

显示 --- sigprocmask函数 指明进行发送变量


## 信号处理程序


![700](https://s2.loli.net/2025/03/22/Jgf8uZMXmqCHAFn.png)

G2 ： 不修改全局变量  ！！！！
volatile ---- 对编译器进行限定，不对全局变量进行优化，**每次都是从内存中进行读取而不是寄存器**


![700](https://s2.loli.net/2025/03/22/QsmYWEZ5KhxRpJy.png)

![700](https://s2.loli.net/2025/03/22/MSkBsTegdZX68AQ.png)


![700](https://s2.loli.net/2025/03/22/u7vO1afos2NzU8C.png)

保存和恢复错误号。


问题 ： 只回收了两个资源

![700](https://s2.loli.net/2025/03/22/l1byTqI2G4DW9fL.png)

![700](https://s2.loli.net/2025/03/22/28MIsozBQGvLDj5.png)


**原因 ：**  1个在执行，一个在待处理， 剩下的父进程会忽略
![700](https://s2.loli.net/2025/03/22/q7vhCkQmsF9W1iu.png)

![700](https://s2.loli.net/2025/03/22/be4kz25KNqSxP9J.png)


不适用 if  而是使用 while


### 例子2

子进程运行过快，导致先delete 然后 add。

![700](https://s2.loli.net/2025/03/22/ovL5ZgV7Fsp8euE.png)



![700](https://s2.loli.net/2025/03/22/vam9usRgKOYMrPV.png)

![700](https://s2.loli.net/2025/03/22/p9auOyHgkv8t4Br.png)



![700](https://s2.loli.net/2025/03/22/2FY1mWjqR59ZlpV.png)


### 例子3 使用循环等待信号

![700](https://s2.loli.net/2025/03/22/uhCpoWbPz4OLMTJ.png)

![700](https://s2.loli.net/2025/03/22/8W3OItBTrPiEHjV.png)


此时一直while 浪费资源

![700](https://s2.loli.net/2025/03/22/EZOIkY1FaiCyUzb.png)

![700](https://s2.loli.net/2025/03/22/H7fCESAvXBoN5YU.png)

![700](https://s2.loli.net/2025/03/22/OHZXYDFurAvbh6k.png)


### 非本地跳转

用户级别的异常控制

![700](https://s2.loli.net/2025/03/22/dcWFj7BYZMAixKN.png)

保存环境  --- env buffer  包括 pc sp 寄存器。。。。。
调用一次返回多次

![700](https://s2.loli.net/2025/03/22/OFc5A8GanbPDIKk.png)


恢复环境 
- 会触发setjump 的回调函数


![700](https://s2.loli.net/2025/03/22/pG1I7b4T8cUVLoO.png)

![700](https://s2.loli.net/2025/03/22/9nyzwKpob8jZ5Q6.png)


![700](https://s2.loli.net/2025/03/22/Bmlx2Oyr5btTh3F.png)

### 例子

![700](https://s2.loli.net/2025/03/22/HyjPtn4mhR2iKVg.png)


![700](https://s2.loli.net/2025/03/22/YPhDNunQ5lGKgVH.png)

![700](https://s2.loli.net/2025/03/22/IrRUVAuNKwstYby.png)


