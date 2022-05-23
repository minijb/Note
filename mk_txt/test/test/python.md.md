# python

## 1 内置类型

* 数字
* 字符串
* 列表
* 字典
* 元组
* 文件
* 集合
* 其他（None，布尔）
* 程序单元类型

### 数字

** 幂运算

**常用模块**

math

random

### 字符串

```python
S = '123'
S[1]#2
```

序号从0开始

下标-1可以反向

```python
S[-1]
S[len(s)-1]
#3
```

**分片操作**

```python
S[1:3]
#23,左包右不包
S[1:]
#1-len(s)
S[:3]#S[0:3]
S[:-1]#12 everything除了S[-1]
S[:]#everything
```

**其他操作**

```python
S1+S2
S1*{num}
```

**不可变性**

不可以单独修改字符串里的某个或一些值

`S[1]='z'#err`

但是可以中国建立一个新的字符串以同一个变量名进行复制，这样之前的会被清除。

`S='z'+S[1：]`

> python中每一个对象都会被归类为可变或者不可变的，
>
> * 在核心数据类型中，数字，字符串和元组不可改变
> * 列表，字典，集合不是这样

**其他操作**

```python
s.find('123')#返回查找子串
s,replace(A,B)#返回用B代替A的字符串
s.split(',')#以,进行字符串分割，返回一个分割后的列表
s.lower()#字符串转为小写
s.upper()#字符串转为大写
S.isalpha()#判断字符串是否是英文
s.isdigit()#判断是否是数字
s.restrip()#返回去除右边空白后的字符串
len(S)#返回字符串的查高度
ord('x')#返回x的ASCII
```

**字符串格式化**

```python
'%s hello %s' % ('span','ok')
```

```python
'{1} is {0}'.format('A','B')
'{0} is {1}'.format('A','B')
'{} is {}'.format('A','B')
```

```python
'{:,.2f}'.format(296999.2642)#'296,999.26'
'%.2f | %+05d' % (3.132312,-43)#'3.13 | -0043'
```

**多行字符串**

```python
S="""
asdasdas
dasd
asda
sda
a'sdas'asdas'dasda
sdas'da
sdasd
"""
```

**字符串字面量**

即忽略反斜线造成的转义机制

```python
r'asdasdasd\n\nasda\n'
#'asdasdasd\\n\\nasda\\n'
```

#### Unicode字符

在python3中str字符串可以处理Unicode字符

```python
'saam'.encode('utf8')
#b'saam'
```

python3中禁止普通字符串和字节串混合使用

**模式匹配**

`import re`

主要是使用正则表达式来处理字符串

### 列表

```python
L = [123,'123123',1]
len(L)
```

同样可以在上面进行索引和切片以及`+ *`

**特定操作**

```python
L.append('qweqwe')#在结尾处增加
L.pop()#在结尾处减少，并返回
L.sort()#默认排序
L.reverse()#列表反转
```

**边界检查**

添加修改不允许超出索引范围i，超出索引返回会报错

**列表支持嵌套**

```python
M=[
    [1,23,4],
    [1,2,34],
    [12312,123123,123]
]
```

#### 推导

```python
cols = [row[1] for row in M]#后半是去除元素，前半是对元素的操作
cols#[23, 2, 123123]
```

```python
cols = [row[1]+1 for row in M]
cols#[24, 3, 123124]
```

同样可以加入判断

```python
cols = [row[1] for row in M if row[1]%2==0]#在从for中得到元素后经过if的条件筛选后得到结果返回
cols#[2]
```

同样可以通过此方法简单的筛选出一些值

```python
col1 = [M[i][i] for i in [0,1,2]]#取M这个3x3矩阵中的对角线上的值
col1#[1, 2, 123]
```

通过range函数以及list函数可以生成一串连续的数

```python
list(range(5))#[0, 1, 2, 3, 4]
```

```python
[ [i**2,i**3] for i in range(5)]
#[[0, 0], [1, 1], [4, 8], [9, 27], [16, 64]]
```

这种类似的函数很多，如：

- sum()可以放入列表来求和
- map(function,iterable)通过function来处理iterable返回一个迭代器

> 注意前面的类型处理要符合但要初始化的序列类型

### 字典

一种键值对的映射

```python
maps = {
    'food' : 'inasd',
    'quantity' : 4
}
```

可以通过索引来修改或者取出值

```python
maps['food']=12
```

**通过dict()来创建字典**

```python
bob1=dict(name='bob',age=14)
#zip(iter,)可以实现将连个数组打包成元组
bob2=dict(zip(['name','age'],['bob',14]))
#{'name': 'bob', 'age': 14}
```

同样字典可以嵌套字典

可以使用多个索引来取出嵌套中的值

#### 不存在的键：if测试

如果访问一个不存在的键会产生错误

因此可以使用`in`来进行某个键是否存在

```python
'f' in D#true/false
```

除此之外还有很多方式避免获取不存在的键

* get()带有默认值的条件索引

```python
bob2.get('name',0)#如果没有f则返回默认的值，有则返回对应的值
```

* try
* if的三元表达式

```python
value = bob2['x']  if 'x' in bob2 else 0
```

#### for循环

```python
for key in sorted(D):
    print(xxx)
```

### 元组

具有不可更改性

可以通过下标进行索引

**专有方法**

```python
T.index(4)#返回4出现的位置
T.count(4)#返回4出现的次数
```

可以进行分片和

```python
T = (2,) + T[4:]#只有一个的元组需要以,结尾
```

元组内部可以有多种类型

同时元组的括号可以省略

### 文件

通过open()来打开文件

常见用法

```python
for line in open('data.txt'): print(line)
```

* 处理二进制字节文件
* 处理unicode文件

```python
file = open('data.txt','w',encoding='utf-8')#打开utf-8的文件
file = open('none.txt','w',encoding='utf-8')
file.write('sp\xc4m')
file.close()
Text = open('none.txt',encoding='utf-8').read()
```

如果没有选定字符类型，那么可以直接把这个当成内存中的字符串来处理也行

### 其他核心类型

**set**

就像一个无值的自建的键组合

```python
Y = {'p','a','m'}
X = set('spam')
X|Y
X&Y
X-Y
X>Y
#可以使用推到进行初始化
```

这种对象可以过滤重复对象，分离集合差异，进行非顺序的等价判断

**分数**

用来处理十进制数的精度问题

`import decimal`

**type**

通过type()可以查看一个变量的类型

type的type类型是type

**自定义类**

之后介绍

## 2 数值类型

* 整数和浮点对象
* 复数对象
* 小数：固定精度对象
* 分数
* 集合
* 布尔
* 内置函数
* 表达式
* 第三方扩展

### 数值字面量

|            字面量            |           解释           |
| :--------------------------: | :----------------------: |
|             123              |    整数（无大小限制）    |
|          1.23，12.2          |          浮点数          |
|    0o1677,0x9f,0b1011110     | 八进制，十六进制，二进制 |
|          3+4j，3+4J          |           复数           |
|   set('spam')，{1,2,34,2}    |           集合           |
| Decimal('1.0'),Fraction(1,3) |        小数和分数        |
|      bool(x),True,False      |           布尔           |

### 内置工具

* 运算符:+   -    *   /  >>  **  &
* 内置数学函数：`pow  abs  round  int hex bin`
* 工具模块: random  math

**表达式运算符**

| 运算符                  | 描述                        |
| ----------------------- | --------------------------- |
| yield x                 | 生成器函数send协议          |
| lambda args: expression | 创造匿名函数                |
| x if y else z           | 当y为真时，x才被计算        |
| x or y                  |                             |
| x and y                 |                             |
| not x                   | 逻辑非                      |
| x in y  , x not in y    |                             |
| x is y  , x is  not y   | 对象同一性测试              |
| x==y,x!=y               | 值等价性运算                |
| x ^ y                   | 异或    集合的子集和超集    |
| x//y                    | 下位取整除法                |
| -x，+x                  | 取负，去正                  |
| ~x                      | 按位非                      |
| x(....)                 | 调用函数方法或者类          |
| x[A:B:C]                | slice(A,B,C) start end step |

在python中运算符可以链式使用



混合类型运算，会向上转化类型

强制类型转换

```python
int(3.14)
float(3)
```

#### 进制中间的转换

>oct() 十进制转为八进制
>
>hex() 十进制转为十六进制
>
>bin()  十进制转为二进制
>
>eval() 将其他进制转换为十进制

> 同样在字符串的格式化中
>
> o十进制  {0:o}
>
> x十六进制
>
> b二进制

#### 二进制操作

> << , >>  , | , &

查看二进制的长度

> len(bin(x))
>
> x.bit_length()

#### 其他内置工具

**math模块**

- math.pi    3.14......
- math.e  2.71......
- math.sin(2.math.pi/180)
- math.sqrt(144)开平方
- pow(2,4)  2的四次方
- 2**4
- abs()绝对值
- sum()
- min()   max()
- math.floor() 向下取整
- math.trunc() 向上取整
- round()四舍五入

**random模块**

- random.random() 随机数
- random.randint(1,10) 
- random.choice(list)
- random.shuffle(list)打乱list的顺序

#### **小数类型**

浮点数缺乏精确度

使用小数对象可以使对象更加精确

```python
from decimal import Decimal
Decimal('0.1')+Decimal('0.1')+Decimal('0.1')-Decimal('0.3')
#Decimal('0.0')
```

同样也可以通过浮点数来初始化小数对象

**设置全局小数精度**

如小数可以指定精度(默认28)和舍入模式

如

```python
decimal.getcontext().prec=4
Decimal(1)/Decimal(7)
#Decimal('0.1429')
```

**小数上下文管理器**

使用with上下文管理器可以临时设置小数精度

```python
with decimal.localcontext() as ctx: 
    ctx.prec = 4
    Decimal(1) / Decimal(7)
```

#### 分数类型

**创建分数**

```python
from fractions import  Fraction
x= Fraction(1,3)
y= Fraction(1,7)
print(y)
x+y
x*y
```

**可以通过浮点数字符串来创建**

```pytho
Fraction('.25')#Fraction(1, 4)
```

**分数和混用类型**

浮点数对象有一个方法可以产生分子和分母对象

```python
(2.5).as_integer_ratio()
#(5, 2)
```

可以通过分数的混用来建立分数

```python
f=(2.5).as_integer_ratio()
Fraction(*f)
#Fraction(5, 2)
```

>Franction+int=F
>
>F+float=float
>
>F+F=F

注意不是所有的浮点数都是精准的

通过计算得来的浮点数因为精度原因分数会显得很奇怪

#### 集合

**初始化**

```python
x = set('abcd')
x#{'a', 'b', 'c', 'd'}
```

就跟数学中的集合一样

`x-y`得出不同的地方

`x|y`求；并集

`x&y`求交集

`'e' in x`判断e是否在x中

add添加一个元素

update在原集合中求并集

remove删除一个元素

intersection在原集合中求并集

**新的特性**

可以通过列表来初始化

```python
x=set([1,1,2,3,4,4,5])
x
```

同时可以通过花括号来代表集合

> 就好像一个无值字典

**推导**

```python
{x*2 for x in 'apsn'}
```

**集合的作用**

- 可以过滤重复项
- 无序
- 可迭代对象
- 因为无序所以在判断的时候可以比较成员是否相同
- 在处理大数据时可以查看共有对象

#### 布尔型

true的值为1

但是类型不是1

```python
True == 1
True is 1#false

```

## 3 动态类型

`a=3`

1. 创建一个对象代表3
2. 创建一个变量a
3. 创建一个新的对象链接3

> 在内部其实时一个指针

变量不是对象

类型属于对象

**共享应用**

```python
a=3
b=a#指向同一个内存
b='span'#只会改变b
```

对于不可变对象，永远需要一个新的对象进行替代

但是对于可变对象就需要小心了

比如改变列表的元素共享类型就是两者就会同时改变

> 一、python中数据类型（红色为可变类型）
>
> 1、字符串   str
> 2、布尔类型  bool
> 3、整数   int 
> 4、浮点数   float
> 5、数字   (int和float)
> **6、列表    list**
> 7、元组   tuple
> **8、字典   dict**
> 9、日期   date

如果想要分开修改动画可以使用分片来估值一个

```python
a=[1,2,3,4,5]
b=a[:]
b[0]=100
a#[1, 2, 3, 4, 5]
```

字典和列表可以通过`X.copy()`来复制

> 需要import copy

#### 相等

`==`值相同

`is`对象相同，即指向同一个对象

## 4 字符类型

**常见字符操作**

```python
S=''
S='\n'#转义
S="""  """
S=r''
B=b'asd'#字节串
U=u'asdf'#Unicode字符
S1+S2
S*3
S[i]
S[i:j]
len(s)
"asdasd %d " % a #格式化
“啊实打实{0}”.format(a)
S.find()
S.restrip()#去除右侧空白
S.replace('as','aq')
S.split(',')
S.lower()#大小写转化
S.endwith('s')#结尾测试
S.encode('utf8')#编码
B.decode('utf8')#解码
[C*2 for C in 'spam']
map(ord,"spam")#ord反坏单个字符的ASCII
re.match('sdfsdf',line)#模式匹配
```

`S[i:j:k]`

k为步长，就是说每隔k-1个元素进行写入

```python
S='abcdefgh'
S[::2]#'aceg'
```

如果k为负数那么就是反向操作

**形式转换**

```python
int('42')
str(42)
float('1,3')
```

**字符串代码转换**

```python
ord('a')#返回整数字节码
chr(115)#返回整数字节码对应的字符
```

因为ord返回的是一个整数因此可以通过加减来改变字符

```python
S='a'
S=chr(ord(S)+1)
S#b
```

**进制之间的转换**

```python
int('1101',2)#13
bin(13)#0b1101
```

#### 字符串的修改

**字符串是不可修改对象因此字符串不支持索引修改**

- 可以通过拼接来修改
- 可以通过replace方法来修改

```python
S="Hello"
S=S.replace('el','ooooo')
S#'Hooooolo'
```

**我们可以通过字符串的格式化来创建文本**

#### 一些例子

字符串的修改

----------

**通过find来找到偏移量**

**然后通过分片来替换**

```python
S='xxxxxxxxxxxxxSPAMxxxxxxxxxxxxxxxxx'
where = S.find('SPAM')
S=S[:where]+"HELLP"+S[(where+4):]
S#'xxxxxxxxxxxxxHELLPxxxxxxxxxxxxxxxxx'
```

**replace方法**

默认情况下是全部替换

`S.replace('a','b)`

可以通过添加数字来修改替换的个数

`S.replace('x','a',3)`

**通过list方法返回一个列表在通过join方法合成一个字符串**

```python
L=list(S)
L[12]='A'
S=''.join(L)
S#'xxxxxxxxxxxxAHELLPxxxxxxxxxxxxxxxxx'
```

> join可以添加多个参数来实现字符串的连接

--------

字符串发剖析

--------------

在字符串出现固定偏移量的时候可以通过split方法将字符串进行分割,返回一个字符串列表

```python
S='aa,bb,cc'
S.split()#['aa,bb,cc']
```

通过分割字符也可能是一个字符串

----------

#### 字符串格式化

**表达式**

`'xx%sx' % (values)`

**方法调用**

`'xxxx{}'.format(values)`

##### 格式化表达式

%左侧是字符串通过以%开头的代码进行转换

字符串的类型码

| 代码 | 意义             |
| ---- | ---------------- |
| s    | 字符串           |
| c    | 字符（int或str） |
| d    | 十进制数字       |
| i    | 整数             |
| o    | 八进制           |
| x，X | 十六进制         |
| e，E | 带指数浮点数     |
| f，F | 十进制浮点数     |
| g，G | 浮点数e或f       |

在%和类型码之间可以添加一些参数

`%[(keyname)][flags][width][.precision]`

* 如果后边是字典可以通过keyname进行索引

`'my name is %(name)s,my age is %(age)d' % {'name':'ray','age':30} `

* 罗列说明格式的标签如：左对齐(-），数值的符号(+)，

零填充(0)

* 替换文本的宽度**（默认右对齐）**、
* 小数点后为小数的精度

##### 格式化表达式可以基于字典

`'my name is %(name)s,my age is %(age)d' % {'name':'ray','age':30} `

**可以通过vars函数来进行方便的操作**

```python
a=100
'%(a)d' % vars()
```

vars函数可以进行取得当前存在的所有变量，并返回一个字典

##### 字符串格式化方法的调用

{}内可以使用数字进行索引，可以通过名称进行索引

如果是空则按照顺序进行索引，里面的值可以是一个对象

##### 添加键，属性和偏移量

如：

```python
L = list('sapn')
'{0} {0[1]} {map[kind]}'.format(L,map={'kind':'abv'})
#"['s', 'a', 'p', 'n'] a abv"
```

##### 高级可视化语法

可以加上：进行补充

可是如下

`[align][sign][#][0][width][,][.precision][typcode]`

- alingn:  > , < , = , ^:分别为左对齐，右对齐，符号字符后的填充，居中
- 后面的就跟格式化表达式一样

### 通用类型分类

**三大操作类型**：他们共享方法

* 数字
* 序列：字符串，列表，元组
* 映射：字典

**是否是可以变类型**

* 不可变类型：数字，字符串，元组，集合
* 可以变类型：列表，字典

## 5 字典和列表

### 列表

特点：

* 任意对象的有序结合
* 通过偏倚访问
* 可变长度，可嵌套
* 可变序列
* 对象引用数组

**常用操作**

- y=[]
- y=list()
- L[]
- L[:]
- L1+L2
- L*3
- for x in L
- 3 in L
- L.append()尾部添加
- L.extend(list)尾部扩展
- L.index(X)索引
- L.sort()排序
- L.reverse()反转
- L.copy()复制
- L.clear()清除
- L.pop(i)清除并返回i处元素，默认是尾部元素
- L.remove(i)清除i出元素
- del L[i]
- del L[i:j]
- 推导
- 分片处可进行删除修改或赋值

### 字典

特点：

- 通过键来进行读取
- 无序
- 长度可变，任意嵌套
- 可变映射
- 散列表

**操作**

| 操作                              | 解释             |
| --------------------------------- | ---------------- |
| D=dict(name='bob',age=18)         | 关键字构造       |
| D=dict(('name','age'),('bob',18)) | 键值对构造       |
| D=dict(map(keylist,vallist))      | 拉链式键值对构造 |
| 'age' in F                        | 键存在测试       |
| D.keys()                          | 全部键           |
| D.values()                        | 全部值           |
| D.items()                         | 所有键值元组     |
| D.copy()                          |                  |
| D.clear()                         |                  |
| D.update(D2)                      | 通过键合并       |
| D.get(key,default？)              | 通过键获取       |
| D.pop(key,default?)               | 通过键删除       |
| D.popitem()                       | 删除返回所有键   |
| len(D)                            |                  |
| del D [key]                       |                  |
| list(D.keys())                    | 产看字典的键     |
| 推导                              |                  |
| for  x in D                       | 键遍历           |

**如何将值映射为键**

`[ title for (title,year) in  D.items() if xxx]`

通过items方法取得键值对的元组最终实现反向映射

> 键不一定只是字符串，可以是数字

**通过元组作为键**

`D[(1,2,3)]=99`

**避免不存在的错误**

可以使用try，`x in D`来避免不存在键的错误

#### 字典的初始化

- 正常的方法
- `dict.formkeys([list],val)`

通过默认值来初始化字典

##### 通过zip搭配dict创建字典

通过两个列表分别代表键和值来初始化字典

`dict(zip(['a','b','v'],[1,2,3]))`

##### 通过推导进行初始化

`D= {k:v for (k,v) in zip (['a','b','v'],[1,2,3])}`

`D= {x:x**2 for x in [1,2,3,4]}`

#### 字典视图

keys，values，items都返回视图对象

视图是可迭代对象，也就是一次只产生一个结果的对象，同时字典视图还保留了字典的顺序，因为不是列表，所以不能通过索引进行存取。

但是可以通过list方法转换为列表

-----------

视图可以与其他视图，集合，字典混合

如

`|`，`&`

它可以像集合一样被操作

## 6 元组，文件，其他核心类型

### 元组

特点

- 任意对象**有序**集合
- 通过偏移量存取
- 不可变序列
- 固定长度，任意嵌套，多样性
- 对象引用的数组

**常用操作**

| 运算                         | 解释                     |
| ---------------------------- | ------------------------ |
| T=(1,2,3)                    |                          |
| T=1,2,3,4,5                  |                          |
| T=tuple(‘spam’)              | 通过可迭代对象进行初始化 |
| T[I], T[i] [j],T[i:j]        |                          |
| len(T)                       |                          |
| T1+T2                        |                          |
| T*3                          |                          |
| for x in T                   |                          |
| 'sapm' in T                  |                          |
| T.index('NI')                | 返回最前面相符元素的索引 |
| T.count('NI')                | 返回该元素的数量         |
| namedtuple('EMP',['name',1]) | 有名元组可扩展类型       |

> 注意元组是不可变的
>
> -----------
>
> 如果元组只有单个元素，（25,）

因为不可变性，+，*都是返回一个新的元组

元组单层是不可改变的，但是元组内有列表等可变对象可以修改该对象

我们可以将字典的一部分转换为元组

`tuple(D.values())`

####  有名元组

通过引入collections中的namedtuple可以同时支持序号和属性访问组件，也可以转化为键的类字典访问形式

```python
from collections import namedtuple
Rec =namedtuple('Rec',['name','age','job'])
bob=Rec('Bob',age=40.5,job=['dev','mgr'])
bob#Rec(name='Bob', age=40.5, job=['dev', 'mgr'])
bob[0]#'Bob'
bob.age#40.5
D=bob._asdict()#可以转化为字典
D
```

有名元组是一个元组，类，字典的混合体

支持字典的values，keys等方法

> 同样有名元组支持解包元组赋值和迭代上下文
>
> ```python
> name , age ,job= bob
> for x in bob
> ```
> 但是字典不可以使用解包元组赋值

### 文件

操作

| 操作                       | 解释                                  |
| -------------------------- | ------------------------------------- |
| in=open('xxxx','w')        | w:写入  r:读取  r为默认值             |
| in.read()                  | 把整个文件读取为一个字符串            |
| in.read(N)                 | 读取N个字符                           |
| in.readline()              | 读取下一行（包括\n）                  |
| in.readlines()             | 读取所有行到一个列表中                |
| out.write(S)               | 写入文件，返回写入的个数              |
| out.writelines(list)       | 列表中所有的字符串写入文件,不自动分行 |
| out.close()                |                                       |
| out.flash()                | 把输出缓冲区刷入硬盘中，但不关闭文件  |
| f.seek(N)                  | 把文件偏倚到N处，以便进行下一个操作   |
| for line in open('xxx'):   |                                       |
| open('xxx',encoding='xxx') | 通过Unicode文本打开文件               |
| open('xxx','rb')           | 字节码文件                            |

#### 打开文件

处理模式

- w:写入
- r：默认
- a：在结尾追加内容
- b：二进制模式
- +: 同时支持输入和输出

#### 使用文件

* 文件迭代器适合逐行阅读文件
* 内容是字符串不是对象
* 输出的文件是被缓冲的，可定位的
* close是可选的，回收时自动关闭

#### 文本和二进制

可以通过b来读取二进制

#### 使用JSON格式存储对象

需要`import json`

字典是一个字面量，可以几乎原封不动的转化为json

```python
name = dict(first = 'zhouhao',second='jack')
rec=dict(name = name ,job=[1,2,3],age=10)
import json 
json.dumps(rec)#'{"name": {"first": "zhouhao", "second": "jack"}, "job": [1, 2, 3], "age": 10}'----str
o=json
o=json.loads(S)
o==rec
```

可以将json存储在文件中

```python
json.dump(rec,fp=open('testjson.txt','w'),indent=4)
print(open('testjson.txt','r').read())
p=json.load('testjson.txt')
```

> 存储打包二进制数据
>
> `import struct`

#### 上下文管理器

```python
with open(xxxx,xxx) as f:
    xxxx
```

相当于

```python
f=open(xxxx,xx)
try:
    xxxxx
finally:
    f.close()
```

#### 其他工具

- 标准流sys.stdout
- os模块中的描述文件
- 套接字，管道，fifo
- pickle
- shell命令流

### 注意

#### 应用和复制

可变对象内容改变的时候需要注意引用他的对象一会相应的改变

这时如果不想改变原对象可以使用复制

- 没有参数的分片：D[:]
- copy()方法
- list等内置函数

#### 比较

- ==   测试值的等价性
- is   对象的相同性

**不同类型的比较**

- 字符串是按照从左到右的顺序ord比较
- 列表元组从左到右比较
- 集合是无序的，相等代表内部有相同的元素
- 不同类型不能比较

#### True  Flase

- 数字如果等于0 为假
- 其他对象为空为假

| 'spam' | true  |
| ------ | ----- |
| ''     | false |
| [1,2]  | true  |
| []     | false |
| 0.0    | false |
| None   | False |

#### None对象

相当于c++中的NULL

可以用来初始化列表

#### 类型对象

dict,list,str,tuple,int,float,complex,bytes.set

`type(x)`

可以用来判断类型

`type(x)==list`

## 7 python语句

常用语句

| 语句              | 功能         | 实例                      |
| ----------------- | ------------ | ------------------------- |
| 赋值=             | 创建引用     |                           |
| .                 |              |                           |
| if/elif/else      | 选择         |                           |
| for/else          | 迭代         |                           |
| while/else        | 循环         |                           |
| pass              | 空占位符     | while True:  Pass         |
| break             | 循环退出     |                           |
| continue          | 循环继续     |                           |
| def               | 函数         |                           |
| return            | 函数返回结果 |                           |
| yield             | 函数生成器   |                           |
| global            | 命名空间     | globa  a,b                |
| nonlocal          | 3.x命名空间  |                           |
| import            |              |                           |
| from              |              |                           |
| class             | 创建对象     |                           |
| try/catch/finally | 捕获异常     |                           |
| raise             | 触发异常     | raise EndSeach()          |
| assert            | 调试检查     | assert  x>y,'x too small' |
| with/as           | 上下文管理器 |                           |
| del               | 删除引用     |                           |

**if**

```python
if x > y :
    x=1
```

> 规则
>
> - 如果一行中有多个语句我们可以使用；隔开
>
> ```python
> x=1;x=2
> ```
>
> - 如果程序要分行，那么可以使用括号
>
> ```python
> x=(x+y
>   +1+2)
> ```
>
> ```py
> if (x==1 and
> 	y==2 and
> 	q==3
> 	):
> 	pass
> ```

**通过测试检测输入的语句**

`x.isdigit()`str内容可以检测x是否是int

**使用try处理错误**

使用try语句捕捉错误并完成修复

```python
try:
    num=int(S)
except:
    print('bad!!!')
```

## 8 赋值，表达式，语句

### 赋值语句

#### 赋值语句的形式

| 运算                    | 解释           |
| ----------------------- | -------------- |
| S = 'sapn'              | 基础形式       |
| S,A='span','adc'        | 元组形式       |
| [spam,ham]=['yun','abc] | 列表形式       |
| a,b,c,d='sapm'          | 推广的序列赋值 |
| a,*b='saon'             | 推广的序列解包 |
| sapm=SD='spam'          | 多目标赋值     |
| spam+=2                 |                |

**元组和列表解包赋值**

如2.3中会按照相应位置进行赋值

**序列赋值**

按照下标的顺序依次进行赋值

a->'s'  b->'a'

**扩展序列解包	**

如表5中，a匹配第一个字符，b匹配剩下的所有字符

**多目标赋值**

注意，两者获得的是同一个对象

> 这时候就要注意列表等可变序列的影响了

#### 序列赋值

通过元组或者列表同时对两者进行赋值

**高级序列赋值**

因为序列赋值需要两边的数目相同，如果不同就会出现错误，因此，可以使用扩展解包*。

那如何时前后一致

*通过分片*

```python
string='abcd'
#第一种，使用序号和分片操作
a,b,c=string[1],string[2],string[2:]
#通过list来为牧歌目标创建对应的部分
a,b,c=list(string[:2]) + [string[2:]]
#通过对赋值内容分片达到目的
(a,b),c=string[:2],string[2:]
#((a,b),c)=('ab','cd')
a,b,c
```

#### 扩展序列解包

就跟linux的字符通过*来匹配一样，可以通过解包来实现，序列划分为**前面**和**剩余**部分

**实际使用**

```python
a,*b=string
a,b#('a', ['b', 'c', 'd'])
*a,b=string
a,b#(['a', 'b', 'c'], 'd')
```

**在for循环中的使用**

```python
for (a,*b,c) in [(1,2,3,4),(5,6,7,8)]:
    print(a,b)
```

这样可以简化操作

#### 多目标赋值

相当于共享引用

**增量赋值**

可以使用在列表

#### 增量赋值和共享引用

一般情况下在处理可变类型中都会使用一个新的对象代替，但是增量赋值不同，相当于在原位置修改，

#### 命名惯例

变量的名字一般都是以下划线和字母开头

- 下划线开头的名称不会被from  xxx  import *导入
- 前后都有双下划线是系统定义的名称
- 以双下划线开头但*没有双下划线*结尾是外围类的本地变量
- 通过交互式命令运行时，单个下划线的名称会保存最后一个表达式的结果

### 表达式语句

#### 打印操作

```python
print([objects,][,seq=' '][,end='\n'][,file=sys.stout][,flush=False])
```

- seq的参数为使用xxx分割
- end：在结尾添加
- file：指定输出流的对象
- flush：决定是否刷新缓冲区，强制刷新输出流

#### 打印流重定向

默认的输出流对象是

```python
import sys
sys.stdout.write("xxx")
```

**手动重定向输出流**

也就是设置sys.stdout对象

如

```python
import sys
sys.stdout=open('1.txt','a')
print('xxxx')
```

这是就是在文件的结尾添加想要输出的东西

`stdout`都可以设置为一个非文件对象，只要对象满足预期协议

**自动流重定向**

通过print函数中的file参数，可以一次性的将文字打印到文件中

如

```python
log=open('open','a')
print('xxx',file=log)
```

这种方式同样也常用于将错误信息打印到标准错误流`sys.stderr`中

在python3中还可以直接使用文件来写入

## 9 if测试和语法规则

有时候可以使用字典的索引来代替switch

```python
choice = '1'
print({'spam':1
      '1':2
      }[choice])
```

**处理选择语句的默认情况**

字典的get函数可以在没有匹配的情况下获得默认值

```python
print(D.get(choice,'bad!!'))
```

使用if，else可以获得同样效果

使用try语句一样

### 语法规则

#### 语句分隔符：行与行间的连接符

- 如果使用括号对可以横跨数行
- 如果以反斜杠结尾可以横跨数行（不推荐使用）

同一行上多个语句可以使用;分隔

**真值和布尔测试**

规则和c++同差不多

但是当不是布尔值使用and 和 or时

```python
2 or 3#2
3 or 2#3
[] or 3#3
2 and 3#3
```

#### if/else三元表达式

简化

```python
if X:
    A=Y
else:
    A=Z
    
    
A= T if x else Z
```

bool函数会返回0或1

```python
[Z,Y][bool('x')]#Y
[Z,Y][bool('')]#Z
```

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
>     print(  '%05d   |   %s' % (i,line.rstrip()))
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
>

## 11 迭代和推导

### 迭代器

**迭代协议**

举一个文件对象工作的例子

当我们打开文件后

每次调用readline方法，他就会读取下一行

```python
f=open('1.py')
print(f.readline())
print(f.readline())
'''
new = open('data.txt','w')

L=['aaaaaa\n','bbbbbbbbbb','ccccccccccccccc']
'''
```

当达到结尾时，会返回空字符串

同样，有一个`__next__()`方法有相同效果，但是在结尾时会返回错误

这个接口就是迭代协议

`__next__()`会前进到下一个结果，如果在结果的末尾会引发`StopIteration`错误

所以我们可以使用for来迭代

```python
for line in open('1.txt'):
    print(line,end='')
```

同样可以使用readlines()来进行迭代，但是不是最好的方法，因为从内存中来看，它一次性将文件中的内容存储到内存中 ，可能造成内存爆炸，而迭代器一次只读取一行！！！！

同时使用while没有for速度快，因为迭代器内部时通过c来运行的，而while循环内部时通过python虚拟机来运行的

#### 手动迭代：iter和next

为了简化手动迭代代码，提供了一个内置函数next()他会自动的调用`__nexr__()`方法并返回同样的内容

```python
f=open('1.py')
print(next(f))
print(next(f))

```

还要注意一点，for循环开始时，会把迭代对象传入到一个内置函数`iter`，并由此拿到一个迭代器：iter返回的迭代器对象有这所需要的next方法，就是调用内部的`__iter__`方法

#### 完整的迭代协议

![1](img/Snipaste_2021-09-13_13-45-06.png)

- 可迭代对象：迭代的被调对象
- 迭代器对象：可迭代对象的返回结果，在迭代对象中提供值的对象，结束时触发`Stopiteration`异常

模拟for循环

```python
L=[1,2,3]
I=iter(L)
I.__next__()
```

对于文件来说，第一步时不需要的

```python
f=open('1.py')
iter(f) is f#True
```

文件有自己的next方法

列表等内置对象，本身不是迭代器，因此需要iter来启动迭代

#### 其他内置类型可迭代对象

遍历字典，通过对keys()方法获得键的迭代器

在p3中，字典自带一个迭代器

```python
I=iter(D)
next(I)
```

因此可以直接`for key in D`

**os.popen**

shelve和os.poepn返回的结果也是可迭代的

```python
import os
P=os.popen('dir')
P.__next__()
#' 驱动器 D 中的卷是 新加卷\n'
```

注意，popen不支持`next()`但是可以通过调用iter来时它成为一个可迭代对象

### 推导

**列表推导**

```python
[x+10 for x in range(10)]
```

**文件上的列表推导**

我们通常

```python
lines= open('1.txt').readlines()
```

就可以获得一个列表

这样的结果会使每行的结尾有换行符号

因此我们需要在每一行上进行相似的修改

```python
lines=[line.rstrip() for line in lines]
```

它会像for循环一样进行迭代

#### 扩展的列表推导语法

**筛选分句：if**

通过在结尾加上一个以if为开头的语句来进行过滤

如我们想筛选以p为开头的语句

```python
lines=[line.rstrip() for line in open('1.txt').readlines() if line[0]=='p']
```

if语句会检查每个迭代元素的开头相当于一个简化的for循环

```python
[line.rstrip() for line in open('1.txt').readlines() if line.restrip()[-1].isdigit()]
```

**嵌套循环：for**

包含多个for循环，同时每个循环都可以有if，

```python
[ x+y for x in 'abc' for y in 'efg' ]
```

相当于

```python
res=[]
for x in 'abc':
    for y in 'efg':
        res.append(x+y)
```

###  其他可迭代对象

map

extend

zip

### 多遍迭代器，单遍迭代器

range对象本身不是迭代器，需要进行iter才可以进行迭代，但是同时range支持多个迭代器同时使用，同时会记住位置

```python
R=range(3)
I1=iter(R)
next(I1)#0
I2=iter(R)
next(I2)#0
```

相反，zip，map，filter不支持多个迭代器

```python
Z=zip((1,2,3),(1,2,3))
I1=iter(Z)
I2=iter(Z)
next(I1)
next(I2)#(2, 2)
```

之后会详细介绍

简单来说就是，单个迭代器意味着一个对象返回自身，也就是说它生成的对象和map一样

```python
I1 is Z#True
```

> 字典的keys方法返回的不是一个列表，是一个keys对象

## 12 函数

- def使可执行的代码
- def创建一个对象并将赋值给某个变量名
- lambda：创建一个对象并最为结果返回
- return：将结果对象返回给调用者
- yield：向调用者发回一个结果对象，但是会记住它离开的位置
- global： 声明了一个模块级的可被赋值的变量。因为在函数中一般都是局部变量，为了给外层变量赋值就需要用到global
- nonlocal声明了一个需要被赋值的外层函数变量：允许函数在其外层的def语句作用域中已有的名称进行赋值
- 参数是通过赋值传递函数的（对象引用）

### def

def会创建一个对象并将其赋值给一个变量名

```python
def name (args):
    xxxxx
```

def可以包含return语句，return可以出现在函数中的任何位置，但是一旦调用函数就会结束，如果没有return就返回`None`

函数也可以通过yield语句，他被设计为，随事件变化产生一系列的值

> def可以出现在程序的任何地方，他其实相当于=，将函数名和代码绑定在一起。
>
> 可以通过if来实现同一个函数名绑定不同的代码
>
> ```python
> if test:
>     def func():
>         xxxx
> else:
>     def func():
>         xxxx
> func()
> ```
>
> 因为函数是一个对象随意可以
>
> ```python
> other = func()
> other()
> ```

### 局部变量

函数内的所有变量都是局部变量（内部的变量，参数）

## 13 作用域

在函数内的变量作为局部变量遵循:

- def内的变量只能在def内使用，不能在函数外部调用
- def内和def外的变量并冲突

变量可以在三个不同的地方被赋值，分别对应三个作用域:

- 如果在def内部赋值，对于该函数时内部的
- 如果一个变量在def外部的def赋值，对于外层来说它是非局部的
- 如果变量在所有def外赋值，对于文件来说时全局的

**作用域细节**

模块定义了如下的全局作用域

- **外围模块时全局作用域**：每一个模块都是一个全局作用域，在模块导入后，相对的外部世界而言的全局变量就成了模块对象的属性，但是在这个模块文件自身中也能像简单变量一样使用全局变量
- **全局作用域的作用单位仅限单个文件**
- **赋值对象除非被声明为global和nonlocal，否则都是局部变量：**默认情况下所有函数定义内的变量都是局部变量，==如果你要给一个位于函数外层模块文件的顶层作用域变量名赋值，就需要在def内部使用`global`，如果想要在外层def作用域中的变量赋值，可以使用`nonlocal`==
- **所有其他的变量名都是外层函数的局部变量、全局变量或内置变量**：函数定义内部尚未赋值的变量名被假定时嵌套作用域的局部变量，或假定时外层命名空间的全局变量；或时内置变量
- **函数每次调用都会创建一个新的作用域**：在递归中有体现

> 注意，原位置改变对象，并不会将变量化为布局，只有赋值后才会
>
> 如L是全局的列表，在函数内L.append(1)
>
> ```python
> L=[]
> def ok():
>     
>     L.append(1)
>     
> ok()
> L#[1]
> #如果在append之后使用赋值，会报错因为局部不可以修改全局
> 
> L=[]
> def ok():
>     L=[123]
>     L.append(1)
>     
> ok()
> L#[]
> 
> L=[]
> def ok():
>     # L.append(1)
>     global L
>     L=[123]
> ok()
> L#[123]
> ```

### LEGB规则

之前规则的简化

- 默认情况下，变量名赋值会创建或改变局部变量
- 变量名引用之多可以在四种作用域内查找：局部，外层函数，全局，内置
- `global`和`nonloacal`语句声明的名称将赋值的变量名分别映射到外围模块和函数的作用域中

LEGB规则

- 在函数中使用未限定的变量名时，将查找四个作用域中第一次找到该变量的地方:局部，外层函数，全局，内置
- 函数在给一个变量赋值时，python对创建或改变局部作用域的变量名，除非被声明为全局

> class属于局部作用域

### 例子

```python
X=99
def func(Y):
    Z=X+Y
    return Z
func(1)
```

全局：X func

局部：Y  Z

--------------

使用内置作用域（如：使用自己的类来代替内置函数）需要`import builtins`

### global

global主要用于在def中声明一个或多个全局变量（一个和全局变量同名的变量只要在函数中没有被赋值它依旧时全局变量，一旦赋值就是局部变量）

```python
L=[123]
def ok():
    # L.append(1)
    L.append(111)#[123, 111]
    print(L)
ok()
L#[123, 111]
```

因此总结一下：

- 全局变量不进行声明也可以引用
- 如果想要在函数中修改(也就是赋值)全局变量，就需要引用

```python
L=[123]
def ok():
    L=[111]#此时为全局变量
ok()
L#[123]

L=[123]
def ok():
    global L
    L=[111]#此时为全局变量
ok()
L#[111]
```

> 普通函数使用全局变量会引发设计问题，因此要减少函数中全局变量的使用，同时以来形参和返回值

----------------------

> 最小跨文件修改
>
> 尽量少修改其他文件的变量
>
> 因此最好的方式时写一个函数来得到返回值，通过访问函数来修改其他文件的变量
>
> ```python
> #1
> X=99
> def setX(new):
>     global X
>     X=new
> 
>     
> #2
> import 1
> 1.setX(1)
> ```
>
> 这样可以增加可读性，直接修改其他文件可能完全不知道是在干什么

#### 其他全局变量的方法

```python
#thismod.py
var = 99


def glob1():
    import thismod
    thismod.var+=1
    
def glob2():
    import sys
    glob=sys.modules('thismod')
    glob.car+=1
```

也就是说我们可以通过跨文件的导入模块来修改全局作用域下的变量

### 嵌套作用域

- 一个引用，python会从内向外找
- 但是global是直接使用全局的变量

```python
X=99
def func1():
    X=88
    def f2():
        print(X)
    f2()
func1()#88
```

**工厂函数**

通过一个方法返回另一个方法

```python
def maker(N):
    def action(X):
        return X**N
    return action

f=maker(2)#返回一个action但是不执行
f(2)#4
```

注意：此时虽然函数引进退出但是action依旧记住了N为2

实际上是外层嵌套局部作用域的N被作为执行状态被保存下来，并附加到action函数中，同时注意我们如果在创建一个新的action函数，他们之间不会相互影响

```python
g=maker(3)
g(3)#27
f(2)#4
```

因为每一个工厂函数的调用都将得到属于自己的状态信息

>  python2需要使用默认参数值来保存外层作用域状态,有时候也需要使用默认参数来保存状态，如下节

#### 循环变量的特殊情况

```python
def maker():
    array=[]
    for i in range(5):
        array.append(lambda x : i**x)
    return array
arr=maker()
arr[0](2)#16
arr[2](2)#16
```

因为是通过嵌套作用域来获得i的值因此所有的i都会被定义在循环的最后一次中

这时候我们就需要通过默认参数来保存外层作用域的中的状态

```python
def maker():
    array=[]
    for i in range(5):
        array.append(lambda x ,i=i: i**x)
    return array
arr=maker()
arr[0](2)#0
arr[2](2)#4
```

### nonlocal

用来声明外层作用域的变量

注意该声明是从外层def开始不是从本身开始

注意声明的变量必须在外层出现，不能添加一个新的变量

```python
x=3
def f1():
    x=2
    def f2():
        nonlocal y
        print(x)
    f2()
    print(x)
f1()
print(x)
#SyntaxError: no binding for nonlocal 'y' found
```

**为什么使用nonloacl**

需要求改外层def的变量，但是同时外层不能找到nonloacal声明的变量

```python
def test():
    state=5
    def next(label):
        nonlocal state
        state+=1
        print(label,state)
    return next
f1=test()
f1('12')#12 6
f1.state#err
```

### 函数的属性状态

通过函数的属性（类似与类的属性）可以更好的达到nonlocal的效果

同时函数属性允许状态变量从内联函数的外部被访问，就像类的属性一样

```python
def maker(start):
    def nexted(label):
        print(label,nexted.state)
        nexted.state+=1
    nexted.state=start
    return nexted
F=maker(0)
F('qq')#qq 0
F('qq')#qq 1
F.state#2
```

## 14 参数

- 参数的实现是通过自动将对象赋值给局部变量来实现
- 函数内部赋值参数名不会影响调用者
- 改变参数的可变参数对象的值可能对调用者有影响



- 不可变参数本质上传送的是值
- 可变参数传递的是指针

### 参数和共享引用

```python
a=88
def f1(a):
    a=99
f1(99)
print(a)#88

L=[12]
def f2(L):
    L[0]=100
f2(L)
print(L)#100


L=[12]
def f3(L):
    L=[123]
f3(L)
print(L)#[12]
```

可以看到其实是参数引用了同一个对象，可以把他当成共享引用

**避免修改可变参数**

为了避免修改可变参数（尽量通过返回值来达到想同的效果）可以选择：

- 通过复制一个对象如copy，分片等在参数中或在函数内部使用

### 参数匹配基础

| 语法                  | 位置   | 解释                                                         |
| --------------------- | ------ | ------------------------------------------------------------ |
| func(v)               | 调用者 | 位置匹配                                                     |
| func(n=v)             |        | 名称匹配                                                     |
| func(*iterable)       |        | 将迭代器的每一项作为单独参数输入(基于位置)                   |
| func(**dict)          |        | 将字典中的键值作为单独的参数输入                             |
| def func(n)           | 函数   |                                                              |
| def func(n=v)         |        | 默认参数值，没有参数时使用默认值                             |
| def func(*n)          |        | 将剩下位置匹配的基于位置的参数收集到一个**元组**中           |
| def func(**n)         |        | 将剩下的关键字参数匹配收集到一个元组中                       |
| def func(*other,name) |        | 在调用时必须通过关键字传入的参数（因为*o表示任意长度的参数） |
| def func(*,n=v)       |        | 在调用时必须通过关键字传入的参数                             |

**一些细节**

- 在函数调用时，参数必须按照顺序出现：基于位置，所用基于name的参数和*iter的组合，之后时**dict
- 在函数头部，参数必须按照一下顺序：一般参数，含有默认值(n=v)，之后时*name形式，之后时只能通过函数名调用的key-only参数，之后时**name形式

函数中出现**arg形式的参数必须放在最后

python调用函数的基本顺序：

1. 通过位置
2. 匹配名称分配的关键字
3. 剩下的非关键字参数分配到*name
4. 剩下的关键字匹配的参数分配到**name中
5. 加默认值分配到未匹配的参数中

**可变参数实例**

```python
def fun1(m,*arg , **args):
    print(m)
    print(arg)
    print(args)
fun1(2,3,4,a=1,b=2)
'''
2
(3, 4)
{'a': 1, 'b': 2}
'''
```

### 解包参数

在调用函数时可以使用`*`,`**`韩式来实现参数的解包

```python
def func(a,b,c):
    print(a,b,c)
a=[1,2,3]
func(*a)
#1 2 3
```

同样**可以用来解包字典来实现name对应val的形式

但是注意**在调用时要放在`*`之后

**泛化的使用函数**

可以通过if来实现同时对函数以及参数的选择，并通过解包函数传入参数

```python
if xxx:
    action , args = fun1,(1,)
else:
    action , args = fun2,(1,2,3,4)
action(*args)
```

注意函数对象也是可以作为参数传入的

**key-only参数**

在*后面的参数必须通过n=v的形式来掺入参数

**实例**

**通用set函数**

```python
def intersect(*args):
    res=[]
    for x in args[0]:
        if x in res: continue
        for other in args[1:]:
            if x not in other:break
        else:#for的else只有在for正常完成时才可以允许因此只有某个值为剩下字符串共有的才可以进入
            res.append(x)
    return res

def union(*args):
    res=[]
    for seq in args:
        for x in seq:
            if x not in res:
                res.append(x)
    return res
```

  编写一个函数通过传入方法和参数来完成运行

```python
U=('a','abc','abdst')
def tester(func,items,trace=True):
    for i in range(len(items)):
        items = items[1:]+items[:1]#将元组的顺序循环的向前移动
        if trace: print(items)
        print(sorted(func(*items)))
tester(intersect,U)
'''
('abc', 'abdst', 'a')
['a']
('abdst', 'a', 'abc')
['a']
('a', 'abc', 'abdst')
['a']
'''

tester(union,U)
'''
('abc', 'abdst', 'a')
['a', 'b', 'c', 'd', 's', 't']
('abdst', 'a', 'abc')
['a', 'b', 'c', 'd', 's', 't']
('a', 'abc', 'abdst')
['a', 'b', 'c', 'd', 's', 't']
'''
```

通过测试保证了交并集的正确性

同样我们可以通过

```python
def print3(*arg,**keys):
    sep=keys.get('sep','')
```

来模拟print函数

## 15 函数的高级话题

- 耦合性：在输入时使用参数，在输出时使用return
- 耦合性：只有在必要情况下使用全局变量
- 耦合性：不要改变类型的参数
- 内聚性：每一个函数都应该有一个单一的，统一的目标
- 大小：每一个函数应该相对较小
- 耦合性：避免直接使用模块文件中的变量

### 递归函数

简单的来说就是函数中调用自己

如使用递归求和：

```python
def sum(L):
    print(L)
    if not L: return 0
    else: return L[0]+sum(L[1:])
sum([1,2,3])
'''
[1, 2, 3]
[2, 3]
[3]
[]
6
'''
```

可以使用三元if/else来简化代码

```python
def sum1(L):
    return 0 if not L else L[0]+sum1(L[1:])
sum1([1,2,3,4])


```

### 循环和递归

递归能够遍历任意形式的结构如

`[1,[2,[3,4]],12]`

简单的循环语句在这里并不起到作用

我们可以如下图所示

```python
L=[1,[2,[3,4]],12]
def sumtree(L):
    tot=0
    for x in L:
        if not isinstance(x,list):
            tot+=x
        else:
            tot+=sumtree(x)
    return tot

sumtree(L)#22
```

### 递归vs队列和栈

```python
#使用显式列表来安排进度
def sumtree(L):
    tot=0
    items=list(L)
    while items:
        front=items.pop(0)
        #isinstance() 函数来判断一个对象是否是一个已知的类型，类似 type()。
        if not isinstance(front,list):
            tot +=front
            print('添加',front,'此时和为tot= ',tot,sep='')
            print('**********************************************')
        else:
            print("将",front,'放到最后',sep='')
            items.extend(front)
            print('修改后的表结构为:',items,sep='')
            print('***********************************************')
    return tot
sumtree(L)
'''
添加1此时和为tot= 1
**********************************************
将[2, [3, 4]]放到最后
修改后的表结构为:[12, 2, [3, 4]]
***********************************************
添加12此时和为tot= 13
**********************************************
添加2此时和为tot= 15
**********************************************
将[3, 4]放到最后
修改后的表结构为:[3, 4]
***********************************************
添加3此时和为tot= 18
**********************************************
添加4此时和为tot= 22
**********************************************
22
'''
```

### 属性和注解

**间接函数调用**

因为函数时对象所以我们可以通过通用函数来使用他们，同时函数对象可以赋值给其他的名称，传递到其他函数，嵌入到数据结构中，

```python
def tester(func,arg):
    func(arg)
```

也可以把它放入发哦数据结构中

```python
schedule=[(fun1,arg1),(fun2,arg2)]
for (func,arg) in schedule:
    func(arg)
```

同样也可以使用工厂函数，来让返回的方法记住外层作用域的状态

```python
def maker(val1):
    def func(message):
        print(val1,message)
    return func
```

#### 函数自省

因为函数时一个对象，所以我们可以使用他的属性

`dir(func)`

```python
func.__name__
func.__code__
func.__code__.co_varnames
```

#### 函数的属性

同样我们可以在函数对象中任意添加属性

```python
func.count=100
```

属性可以直接把状态信息附加到函数对象上，而不必使用全局或非局部和类等其他技术，类似与'静态局部变量'

#### 注解

可以通过`__annotations__`查看

```python
def func(a:int,b: float, c: (1,10))->str:
    return a+b+c
func(1,2,3)
func.__annotations__#{'a': int, 'b': float, 'c': (1, 10), 'return': str}
```

### 匿名函数:lambda

`lambda argument1,2,3 : expression using args`

- lambda是一个表达式，不是语句，它允许出现在def不能出现在的地方，他会返回一个函数，可以选择性的赋值一个变量名
- lambda不是一个代码块

```python
f=lambda x,y : x+y
f(1,2)#3
```

lambda中的代码遵循函数的作用域

**为什么使用lambda**

lambda是函数的简写，我们可以通过def的各种方式来代替它

**switch语句**

我们可以通过字典数据结构来实现很多动作代替switch

```python
key='got'
{
    'al': (lambda:2+2),
    'got':(lambda:2*4),
    'one':(lambda:222)
}[key]()#8
```

同样我们可以通过def来代替lambda

`lower=(lambda x,y:x if x<y else y)`

`showall= lambda x: [print(line,end='') for line in x]`

#### 作用域，lambda也可以嵌套

```python
def action(x):
    return (lambda x,y : x+y)
act=action(99)
act(2)#101
```

### 函数式编程工具

**在可迭代对象上映射函数**

```python
L=[1,2,3,4]
def inc(x): return x+10
list(map(inc,L))
#[11, 12, 13, 14]
```

如果有多个序列，他会并列的将多个序列并列的去除数值放入到函数中

```python
list(map(pow,[1,2,3],[1,2,3]))
#[1, 4, 27]
```

同样我们可以使用推导，但是map更快

```python
[inc(x) for x in [1,2,3]]
#[11, 12, 13]
#如果有多行，
```

**选择可迭代对象：filter**

```python
list(filter((lambda x : x>0),range(-5,5)))
#[1, 2, 3, 4]
```

也通过推导来代替

```python
[x for x in range(-5,5) if x > 5]
```

**合并可迭代对象元素：reduce**

```python
from functools import reduce
reduce((lambda x,y:x+y),[1,2,3,4]) #10 用于展示可迭代对象的合
reduce((lambda x,y:x*y),[1,2,3,4])#24
```

相当于

```python
L=[1,2,3,4]
res=L[0]
for x in L[1:]:
    res=res+x
```

## 16 推导和生成

**列表推导vsmap**

输入字符串返回ASCII的列表

```python
S='spam'
[ord(x) for x in S ]
#[115, 112, 97, 109]

list(map(ord,S))
```

**使用filter增加测试和循环嵌套**

如

```python
[x for x in range(5) if x%2==0]#[0, 2, 4]
list(filter((lambda x:x%2==0),range(5)))
```

如果我们想要筛选出偶数并平方

```python
[x**2 for x in range(5) if x %2==0]
list(map((lambda x: x**2),filter((lambda x : x%2==0),range(5))))
#[0, 4, 16]
```

**列表推导和矩阵**

```python
M=[
    [1,2,3],
    [2,3,4],
    [3,4,5]
]
[row[0] for row in M]
[M[row][1] for row in (0,1,2)]
```

也可以提取对角线

```python
[M[i][i] for i in (0,1,2)]
```

### 生成器函数与表达式

- 生成器函数：常规的def编写，但是使用yield语句一次返回一个结构哦，在每次结果产生之间挂起和恢复它的状态
- 生成器表达式：类似于推导，但是返回按需产生结果的一个对象，而不是创建一个结果的列表

#### 生成器函数：yield vs return

传回一个值并随后从器挂起的地方继续的函数，这就是生成器函数

**状态挂起**

和返回一个值并退出的常规函数不同，生成器函数能够自动挂起并在生成值的时刻恢复之前的状态并继续函数执行。

因此它可以方便的代替提前计算整个一系列值或是在类中恢复状态的方式。

由于生成器函数在挂起时保存的状态包含它的代码位置和整个局部作用域，因此函数恢复时，局部变量保持了信息并且可用

yield产生一个值而不是返回一个值，yield会传回一个值，同时保存状态使函数可以从它离开的位置继续，当继续时，函数在上一个yield传回后立即继续执行。它能够随时间产生一系列值

**与迭代协议集成**

他与迭代协议密切相关，迭代协议对象定义了一个`__next__`方法，它要么返回下一项，要么异常，一个可迭代对象的迭代器用iter内置函数来接受值

为了支持这个协议，函数必须包含一条yield语句，该函数别特别编译为生成器。当调用时，他们返回一个生成器对象，该对象支持用一个自动创建的名为`__next__`的方法接口，来开始或恢复执行

生成器函数也可以有return，但是总是出现在def的结尾，用来中止值的生成：从技术上来讲，任意函数退出时会出现异常来中止值的生成。

#### 应用

```python
def gen(N):
    for i in range(N):
        yield i**2
for i in gen(5):
    print(i,end=' ; ')
#0 ; 1 ; 4 ; 9 ; 16 ;
```

为了中止值的生成可以使用无值返回

可以看一下具体的步骤

```python
x=gen(5)
next(x)
next(x)
next(x)
next(x)
next(x)
next(x)
#StopIteration: 
```

注意x就是可迭代对象

```python
iter(x) is x#true
```

#### 扩展生成器函数

生成器函数协议中增加了一个send方法，send可以生成一系列结果的下一个元素，有点类似next，但是它提供了调用者和生成器函数之间通信的方式，从而影响生成器函数

yield时一个表达式形式，不是语句，他会返回发送给send函数的元素（yield表达式尽量在括号内如：`X=(yield Y)+42`）

调用：可以通过`G.send(v)`发送给一个生成器G，之后恢复生成器代码的执行，并且yield表达式返回给send函数的值

如果提前调用了next自然yield会返回none

```python
def gen():
    for i in range(5):
        X=(yield i)
        print(X)
G=gen()
next(G)
G.send(99)
'''
123
1
'''
next(G)
#None
#2
```

> 因为赋值语句从等号右边开始
>
> 第一次Next调用后，执行等号右边的表达式 yield val，执行完后函数暂停运行，赋值操作根本没有被执行。
>
> 当第二次再运行时才执行赋值（等号左半部分），而生成器恢复运行时，yield初始值为None，所以 y = None
>
> 这段代码中Next返回的始终是 0 ，如何在外部与生成器沟通，让她返回不一样的值？ 于是用到了send方法

### 生成器表达式

就跟推导的语法一样

```python
(x**2 for x in range(6))
#<generator object <genexpr> at 0x0000020CAA64E9C8>
```

不一样的时它返回一个生成器对象

```python
G=(x**2 for x in range(6))
iter(G) is G
#true
```

使用生成器表达式可以对内存空间优化，不用一次算出所有数值

#### 生成器表达式 vs map

如使用join

```python
line='aa,bb,cc'
''.join([x.upper() for x in line.split(',')])
''.join(x.upper() for x in line.split(','))
''.join(map(str.upper,line.split(',')))
```

- 列表推导会产生临时列表
- map的话不够简洁

map和生成器表达式都是可以任意嵌套的，但是生成器不用产生临时列表

#### 生成器表达式 vs filter

生成器表达式也支持if语法

```python
line ='aa bbb c'
''.join(x for x in line.split(',') if len(x)>1)
''.join(filter(lambda x : len(x)>1,line.split(',')))
```

如果想要对filter的结果进行操作，就需要使用map，因此可以看出生成器表达式很方便

### 生成器是单遍历对象

见11章最后

因为生成器和生成器表达式本身就是迭代器，因此只能但单遍历。

> 扩展语法 yield from
>
> 可以委托给子生成器
>
> ```python
> def both(N):
>     yield from range(5)
>     yield from (x**2 for x in range(100))
> ```
>

### 内置工具

#### 目录遍历器

```python
import os
for (root,subs,files) in os.walk('.'):
    for name in files:
        if name.startswith('call'):
            print(root,name)
```

注意因为返回的结果本身就是一个生成器函数，因此只能单遍

**函数的引用**

注意在之前函数的调用中我们可以有使用`*`来解包迭代器，来生成参数

```python
def f(a,b,c):
    print(a,b,c)
f(*range(3))#0 1 2
```

**打乱序列**

平常我们可以使用函数来

```python
def sramble(seq):
    return [seq[i:]+seq[:i] for i in len(seq)]
```

这样的话就需要创造一个完整的列表

我们可以使用生成器来更好的创造

```python
def sramble(seq):
    for i in range(len(seq)):
        seq=seq[1:]+seq[:1]
        yield seq 
list(sramble('spam')）#['pams', 'amsp', 'mspa', 'spam']
```

### 生成器表达式

使用圆括号的推导

`G=(x for x in range(5))`

多数情况下我们通过函数来包括这个语句，这样可以将生成器推广到一个主体

```python
F=lambda seq:(seq[i:]+seq[:i] for i in range(len(seq)))
list(F('spam'))
```

## 17 模块

模块导入步骤

1. 找到模块文件
2. 编译成字节码
3. 执行模块的代码来创建所定义的对象

**搜索路径**

1. 程序的主目录
2. PYTHONPATH目录（如果设置了的话）
3. 标准库目录
4. 任何.pth文件的内容
5. 第三方拓展的目录

这些组合在一起就是`sys.path`

**import**

使用后可以引用模块对象，将整个模块赋值给单独的名称

**from import**

可以将某个特定名称从一个文件复制到另一个作用域

**from ***

主要他将所有名称复制到当前作用域中

**导入只发生一次**

**注意form和import都是赋值**

因此可能会改变某些已有模块

> `from module import name1`
>
> ```
> import module 
> name1=module.name1
> ```
>
> 等价

如果两个模块有相同的函数，那么只能使用import不能使用from

### 模块命名空间

#### 文件产生命名空间

在模块文件顶层（也就是不在函数和类中的赋值）会编程模块的属性

- 模块语句会在首次导入时执行
- 顶层赋值语句会创建模块属性
- 模块的命名空间可以使用属性`__dict__`或`dir(M)`来获取
- 模块是一个独立的作用域

> 模块的全局作用域会在模块加载后编程模块的属性字典，并在之后持续存在，从而提供工具(注意和局部作用域区分)，我们可以通过.来访问属性

```python
#module.py
print("loading")
import sys
name=42
def func():pass
class klass:pass
print('done')


import module
print(module.sys)
'''
loading
done
<module 'sys' (built-in)>
'''
```

### 作用域

```python
#m
X=88
def f():
    global X
    X=99
```



```python
#l
X=11
import m
m.f()
print(X,m.X)#11 99
```

m.f修改的是m中的X而不是l中的，也就是说m.f的全局作用域是m不是调用的文件

- 函数绝对无法看到其他函数内的名称，除非物理上处于这个函数中
- 模块代码无法看到其他模块内的名称，除非被显式的导入了

### 重新加载模块

使用reload函数强制重新加载模块

- 当模块第一次在进程中被导入时才加载和执行模块的代码
- 之后的导入只会使用已加载的模块对象，不会重新执行代码
- reload函数会强制已加载的模块重新载入并执行，文件中的新的代码的赋值语句会在原位置修改现在的模块对象

### reload

- 是一个函数不是语句
- 掺入的参数必须时已加载的模块
- 必须导入才可以使用

```python
import m
from imp import reload
reload(m)
```

## 18 导入包

- 将路径添加到PATHONPATH中，如`C:\mycode`\
- `import dir1.dir2.m`

### `__init__.py`

如果选择使用包导入，必须遵循一个约束：包导入语句中的路径中的每一个目录都必须有`__init__.py`文件

如有一下结构

d0\d1\d2\d3\m.py

对应的import

import d1.d2.m

必须遵循一下规则

- d1和d2中必须含有一个`__init__.py`文件
- d0时容器不需要
- d0必须在模块的搜索路径的sys.path列表中(PATHONPATH或.pth文件中)

### 包初始化文件角色

**包的初始化**

python在首次导入某个目录的时候会自动执行该目录下的init文件中所有的代码，如可以创建需要的数据文件，连接数据库等，一般来说没什么用

**模块使用声明**

**模块命名空间的初始化**

在包导入模型中，你脚本中的目录路径在导入之后会编程真实的嵌套对象路径，如上文中d1.d2运行后会返回一个模块对象，而此对象的命名空间包含了d2中的init文件赋值的所用名称

例子见P702

包机制可以结局重名模块问题，只要在不同的文件中，就可以获得不同包的相同名字的模块

## 19 高级模块话题

### 模块中的数据隐藏:_X和`__all__`

使用`_X`命名的方法可以防止`form *`语句导入模块名，这不是私有，可以通过import m 在通过`m._X`来访问

另外可以通过在模块顶层吧变量名的字符串列表赋值给`__all__`，来达到类似于_X的效果，但是all是指明要复制的名称如

```python
__all__=['a','_c']
a=0
b=0
_c=1
```



```python
from m import *
a#0
b#err
_c=1
```

这两者只对from有效对import无效

### 混合使用模式:`__name__`,`__main__`

每个模块都有name的内置属性

- 如果文件作为顶层程序文件，在启动时name会被设置为字符串`__main__`
- 如果被导入则name就是模块名

所以

```python
if __name__=='__main__':
    xxx
```

就是只有在运行而不是导入是才可以执行的代码

## 20 类

- 每个class语句会生成一个新的对象类
- 每次类调用时，就会生成一个新的实例对象
- 实例自动连接到创建它的类
- 类连接到其父类的方式是，将父类列在class的头部括号中；括号中从左至有的顺序会决定书中的次序

```python
class c2:xxx
class c3:xxx
class c1(c2,c3):xxxx
```

多继承中，最左边是默认会使用的，但是可以显示的知名所在的类来选择父类如C3.z

所以你要把属性附加到那个对象就变的很重要：这个选择决定了属性名称的作用域。附加到实例上的只属于实例，但是附加到类上的属性则由子类和实例共享

- 属性通常实在class语句的顶层语句块中通过赋值语句添加到类中，而不是嵌入到def中
- 属性通常是通过特殊的self的第一位参数的赋值来附加给实例的，这个self参数也被传入类中编写的方法函数

```python
class c2:xxx
class c3:xxx
class c1(c2,c3):
    def setname(self,who):
        self.name=who
```

self用于存储两个实例中的分别的内部名称

### 多态和类
我们有一个通用的父类
```python
class 