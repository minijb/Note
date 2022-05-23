## 10 while和for循环

### while循环

**break,continue,pass,else**

- break  跳出最近的循环
- continue  逃到最近的循环头部
- pass  什么都不做
- else  当循环正常退出时执行（**没有碰到break的时候**）

```python
while True:
    xxxxx
else:
    xxxxx
```

else经常搭配break使用，可以一定程度上代替flag的作用

```python
while x:
    if match(x[0]):
        print('Ni')
        break
    x=x[1:]
else:
    print("not found")
```

### for循环

```python
for x in x :
    xxxx
else:
    xxxx
```

一般都是用于可迭代对象

> 注意可以搭配扩展序列解包来使用，详细见8

**for循环可以嵌套，用于多层嵌套的列表等**

### 循环的技巧

range，zip，enumerate，map

#### 计数循环range

有三个参数

`range(start,end,step)`

**搭配len使用快速迭代**

```python
for i in range(len(s)):
    xxxxx
```

可以用来快速迭代字符串，列表等有下标的序列

#### 并行遍历

zip允许我们并行的访问多个序列

```python
L1=[1,2,3,4]
L2=[5,6,7,8]
Z=zip(L1,L2)
list(Z)#[(1, 5), (2, 6), (3, 7), (4, 8)]
```

zip返回一个可迭代对象，在这个对象中，我们按照顺序将两个序列按照顺序一次分割成元组，从而实现并行的访问两个序列

````python
for (x,y) in zip(L1,L2):
    print(x,y,sep=' | ')
```
1 | 5
2 | 6
3 | 7
4 | 8
```
````

**使用zip构建字典**

字典是键值一一对应，所以使用zip的特性就可以构建字典

```python
D=dict(zip(keys,values))
```

#### 同时给出偏移量和元素：enumerate

```python
for (offset,item) in enumerate(L):
    print(offset,item)
    
for (offset,item) in enumerate(L1):
    print(offset,item)
'''
0 1
1 2
2 3
3 4
'''
```

enumerate会返回一个生成器对象:这种对象支持迭代协议。每次迭代返回一个元组

> os.popen()可以读取命令，返回一个类文件对象
>
> 我们可以使用enumerate来进行简单的格式化
>
> 如
>
> ```python
> import os
> for (i,line) in enumerate(os.popen('systeminfo')):
>  print(  '%05d   |   %s' % (i,line.rstrip()))
> '''
> 00000   |   
> 00001   |   主机名:           DESKTOP-9P8Q3H5
> 00002   |   OS 名称:          Microsoft Windows 10 专业版
> 00003   |   OS 版本:          10.0.19043 暂缺 Build 19043
> 00004   |   OS 制造商:        Microsoft Corporation
> 00005   |   OS 配置:          独立工作站
> 00006   |   OS 构建类型:      Multiprocessor Free
> 00007   |   注册的所有人:     周豪
> 00008   |   注册的组织:       暂缺
> 00009   |   产品 ID:          00331-20300-00000-AA928
> 00010   |   初始安装日期:     2021/6/29, 21:21:59
> 00011   |   系统启动时间:     2021/9/4, 0:11:06
> 00012   |   系统制造商:       Micro-Star International Co., Ltd.
> 00013   |   系统型号:         MS-7B23
> 00014   |   系统类型:         x64-based PC
> 00015   |   处理器:           安装了 1 个处理器。
> 00016   |                     [01]: Intel64 Family 6 Model 158 Stepping 10 GenuineIntel ~2808 Mhz
> 00017   |   BIOS 版本:        American Megatrends Inc. A.00, 2018/3/12
> 00018   |   Windows 目录:     C:\WINDOWS
> 00019   |   系统目录:         C:\WINDOWS\system32
> '''
> ```
