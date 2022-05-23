# CPP

## 变量

`::name`显式的访问全局变量

### 引用

引用不是对象，只是一个别名（不能定义引用的引用）

引用的初始值必须是一个对象，且对象的类型要相同

### 指针

指针不能直接赋值一个int变量

void* 可以存放任意对象的指针



* 指向指针的引用

`int *&r = p` 

> 一般都是从右往左读，一般最有边的符号起决定性作用，如本例中&说明它是一个引用



### const

可以设定常量，**且必须初始化**

如`const int i = 100;`如果修改则会引起错误

> 默认状态下，const对象仅在文件内有效，不同的文件内同名的const不互相影响
>
> 如果本文件中的const对象想要在其他文件中使用则可以
>
> `extern const int i = 100; // 声明并初始化了一个常量`

#### const的引用

**常量的引用**

```c++
 const int i = 100;                                
 const int &ri = i;
```

通过引用不能修改他的绑定

`int &r2 = i; // err`

* 常量引用的初始化

普通情况下引用要和绑定的类型一项

**但是有两种特殊情况**

1. 常量引用能够绑定任意的表达式，只要结果可以转化为引用的类型即可`const int & r3 = 100;`,**尤其允许绑定非常量/字面量**`const int &r4= num;`

> 常量引用仅仅是对引用可以参数的操作做出了限制，并不限定本身。

```c++
	int i = 100;
	int &r1 = i;
	const int &r2 = i;
	r1 += 1;
	r2 +=1 ; //err

```

#### 指针和const

**指向常量的指针**

```c++
const double pi = 3.14;
double *ptr = &pi;//err
const double *cptr = &pi;
*cptr = 14;//err
double pip = 15;
cptr=&pip;
```

同样指向常量的指针可以指向一个非常量。

道理跟常量的引用是一样的

**const指针**

指针是一个对象，而引用不是，因此可以讲指针定义为常量

```c++
int errNUM = 0;
int *const curERR = &errNUM;//curERR 将一直指向errNUM
const double *const pip1 = &pi;//pip1是一个指向常量的常量指针

```

*const 表示这个指针本身是一个常量，本身不能改变。

> 一般都是从右向左，右边的一般都是本身的总之
>
> 如: `*&p`指向指针的引用，其本身是一个引用
>
> 同样这里*const表示本身是一个常量指针。

### 顶层/底层const

顶层const：本身是不是一个常量

底层const：指向的是不是一个常量

拷贝操作下

* 顶层const不受有影响
* 底层const只有数据类型相同或可以转化才有资格

也就是说，本身是常量则不受影响，如果指向的对象是常量则需要注意。

> 如果要拷贝的本事是一个常量的话，接受的一定是一个常量
>
> 如果要接受的是一个常量的话，那拷贝的本身可以是常量也可以不是。

### constexpr

**常量表达式：**

1. 不会改变
2. 在在编译过程中能得到的计算结果

> 字面值：是一个不能改变的值，如数字、字符、字符串等。单引号内的是字符字面值，双引号内的是字符串字面值。
>
> 字面值类型（literal type）：算数类型、引用和指针等。
>
>
> 常量表达式（const experssion）：是指(1)值不会改变 并且 (2)在编译过程就能得到计算结果的表达式。字面量属于常量表达式，用常量表达式初始化的const对象也是常量表达式。
>
> 一个对象（或表达式）是不是常量表达式由它的数据类型和初始值共同决定。
>
> ```c++
> const int max=20; //yes
> const int limit = max +1; //yes
> int staff_size = 100; //no
> const int sz = get_size(); //no
> ```
>
> sz本身是一个常量，但是只有在程序运行后它的值才能获得，因此不是常量表达式

* 因此为了更好的分辨是不是常量表达式，加入constexpr

```c++
constexpr int mf = 200;//yes                       
constexpr int limit = mf +1 ;//yes                 
constexpr int sz = size();//只有在size是一个costexpr的函数时才正确   
```

* 字面量

算数类型，引用，指针

> 指针的初始值必须
>
> 1. 0
> 2. NULL
> 3. 固定地址的对象

> * 函数体内的变量，一般并非存放在固定的地址内，因此constexpr不能指向这样的变量，相反函数体外的地址固定可以定义
> * 函数允许定义一种超出自身范围的变量，这样的变量有固定的地址，因此可以使用constexpr定义



constexpr定义的**指针**只跟指针有关，与对象是无关。

> NULL==>0 可能被修改
>
> nullptr==>空指针

```c++
const int *p = nullptr;//p是指向整型常量的指针
constexpr int *q = nullptr;//q是指向整数的常量指针
int *const m = nullptr;//常量指针
```

同样常量指针可以指向常量也可以指向非常量

### 姓名别名

1. typedef

> typedef double *p;//p是double * 的同义词

2. using

`using SI = Salas_item; //SI是别名`

> 当类型别名和const同时使用的时候要注意！！！！
>
> ```c++
> typedef char *pstring;
> const pstring cstr = -;//一个指向char的常量
> const pstring *ps;//ps是一个指针，对象是指向char的常量指针
> ```
>
> ==也就是说cosnt+别名要看在一起，一起作为变量的类型==
>
> ==不能把pstring简单的转换为char *==

### auto类型

auto会自动的分析表达式，**必须有初始值**

在同一个语句定义中，auto必须是同种类型

`auto a = 0 , b = 3.14;//err`

* 当以引用作为auto类型的初始值的时候，会自动的根据引用原本的类型给auto
* 同时auto会忽略顶层const，保留底层const

```c++
const int ci = i , &cr =ci;                         auto b = ci; //ci是顶层const----b为整形               
auto c = cr; //cr本身是别名，因此看原数据，ci是顶层const，c是整形     
auto d = &i;//d是整形指针                           
auto e = &ci;//e是指向常数的指针（对常量对象取地址是底层const）
```

如果想要得到一个顶层const，需要`const auto f = ci`

同样也可以使用引用

```c++
auto &g = ci;//常量的引用
auto &h = 33;//err:不能为非常量引用绑定字面量
const auto &j= 33//ok
```

### decltype

得到某个方法的返回类型

`decltype(f()) num = x;`

并不会实际调用f，只是会返回这种类型。



* decltype处理顶层const和引用的方式与auto不同

decltype使用的表达式是变脸，则decltype会返回该变量的类型

```c++
const int ci =0 , &cj = ci;
decltype(ci) x = 0;//x----const int
decltype(cj) y =x ; //y----const int &
decltype(cj) z;//err：引用必须初始化
```

#### 简单介绍左值和右值

左值：能够出现在=左边的变量或者表达式（也就是说在内存中是有地址的）

右值：跟左值相反（不在内存中有确定位置）

```c++
int var;
var = 4;
4 = var;       // ERROR!
(var + 1) = 4; // ERROR!
//var是一个左值，4和(var+1)是右值，因为他们本身是临时存储在寄存器中的，没有地址
```

**************

如果decltype使用的表达式不是一个变量，则返回**结果**对应的类型

```c++
int i=42,*p=&i,&r=i;
decltype(0+r) b ; //b--int
decltype(r) e; //e为int&
decltype(*p) c;//err,为int&，必须初始化
```

如果为解引用类型如*p则结果的类型为int&而不是int

> 解引用：直接使用指针的内容

* 如果在变量上加一个括号，则会当成表达式`decltype((i))`结果将对变为引用

> 注：decltype((expressing))的结果永远是引用
>
> decltype(val)只有当val本身是一个引用的时候才是引用

### 自定义类型

struct

类内部名字不能重复，但是内部可与外部重复

如果在花括号之后加上命名则会定义。

```c++
struct data
{
    int i=0;
}accum;

struct data1
{
    int i=1;
};

data1 accum1;
```

两者相同

可以设置一个类内初始值，如果没有会被默认初始化

#### 自己的头文件

预处理器

`#define`将一个名字设定为预处理变量

另两个指令分别检查某个设定是否已定义：

* `#ifdef`当且仅当变量一定义时为真，
* `#ifndef`当且仅当变量未定义时为真，
* 一旦检测结果为真，则会执行操作至`#endif`

这样可以有效的防止他们重复

> 第一次包含.h的时候，`#ifndef`为真，会去定义，.h文件会被拷贝到我们的程序中，如果再一次包含.h文件的话就不会重复定义。

一般预处理值都是全部大写

## 字符串，向量，数组

### 命名空间

```c++
using namespace {name};
using {namespace}::{name};

using std::cin;//这中方式，不能一条语句声明多个；
```

头文件不应该有`using`因为头文件会被复制到引用它的文件中去

### String

**初始化**

```c++
string s1;
string s2 = s1;
string s3 = "hello";
string s4(10,'c');
string s5("hello");
```

**直接初始化和拷贝初始化**

使用'='就是拷贝初始化，使用()则是直接初始化

推荐使用直接初始化

#### 对象操作

> os<<s    讲s写入到输出流os中，返回os
>
> is>>s     将is中的字符串赋值给s，字符串以空白为分割，返回is
>
> getline(is,s)    从is中读取一行给s返回is
>
> s.empty()
>
> s.size()      位置从0开始
>
> s[n]
>
> s1+s2
>
> s1=s2
>
> s1==s2
>
> s1!=s2

**读取未知数量的string**

```c++
while(cin>>word){}
```

**读取一整行**

有时候我们希望**保留空白字符**这之后就用到`getline`会一直读取内容到换行符为止，如果一开始就是换行符，则返回空

`getline(cin,line)`

ps：line中不包含换行符

> string::size_type
>
> 这是s.size()的返回值类型，*一个无符号值*
>
> 当为<0的int时   s.size()<n  恒为正确，因为n会转变为一个**很大的无符号值**

**sting的比较**

* string对大小写敏感
* 如果两个string长度不同，但是前面的字符相同，则短的小
* 如果两个string的字符不同，则从第一个字符上开始比较

**相加**

两者相加

**字面值和string相加**

* 要保证字面值可以转化为string
* 混用时`+`两边至少有一个是string对象
* 可以使用`()`来实现连续字面量相加(但是括号内部必须有一个string对象)

> 使用cctype头文件的函数处理string对象中的字符
>
> isalnum()  如果参数是字母数字，即字母或者数字，函数返回true
> isalpha()  如果参数是字母，函数返回true
> iscntrl()  如果参数是控制字符，函数返回true
> isdigit()  如果参数是数字（0－9），函数返回true
> isgraph()  如果参数是除空格之外的打印字符，函数返回true
> islower()  如果参数是小写字母，函数返回true
> isprint()  如果参数是打印字符（包括空格），函数返回true
> ispunct()  如果参数是标点符号，函数返回true
> isspace()  如果参数是标准空白字符，如空格、换行符、水平或垂直制表符，函数返回true
> isupper()  如果参数是大写字母，函数返回true
> isxdigit() 如果参数是十六进制数字，即0－9、a－f、A－F，函数返回true
>
> tolower()  如果参数是大写字符，返回其小写，否则返回该参数
> toupper()  如果参数是小写字符，返回其大写，否则返回该参数

#### string使用for循环

```c++
for(auto c : line){
    statment
}
```

用来操作string对象中的每个字符

**使用for循环改变字符**

```c++
  for(auto &c : s3){
    c=toupper(c);
  }
  cout << s3 <<endl;

```

#### 只处理一部分字符

两种方法

* 下标运算符
* 迭代器

**下标**

`s[n]`

> n>0&&n<s.size()

使用下标进行迭代

```c++
  for (decltype(s3.size()) index = 0; index !=s3.size()&&!isspace(s3[index]) ; index++)
  {
    s3[index] = toupper(s3[index]);
  }
  cout << s3 << endl;
```

==要注意index的合法性！！！！==

### vector（容器）

vector是一种**类模板**本身不是类或函数，它是编辑器生产类或函数的一种说明。这一过程被称为**实例化**，当使用模板的时候要指定模板的类型

```c++
  vector<int> ivec;//尖括号内就是模板的类型
  vector<vector<string>> file;
```

vector可以容纳大部分对象，但是引用不是对象，不能存放在容器中。

#### 初始化

```c++
  vector<T> v1;//不含有任何对象
  vector<T> v2(v1);
  vector<T> v3=v1;
  vector<T> v3(n,val);
  vector<T> v4(n);//包含n个执行了初始化的对象
  vector<T> v5{a,b,c,d};
  vector<T> v6={a,b,c,d};
```

#### 添加元素

`push_back()`在结尾处添加元素

**其他操作**

> v.empty()
>
> v.size()
>
> v[n]

> vector<int>::size_type;//yes
>
> vector::size_type//err

#### 迭代器iterator

**得到迭代器**

`v.begin()`

`v.end()`

> 如果为空begin==end

**迭代器的运算符**

```c++
*iter;//返回所指元素的引用
iter->mem;//解引用iter并获得名为mem的成员
++iter;//指向下一个元素
--iter;//指向前一个元素
iter1==iter2;
```

iter和指针一样可以通过解引用来获取它所指的元素

```c++
  auto it = s3.begin();
  *it = toupper(*it);
  cout << s3 <<endl;
```

**移动迭代器**

```c++
for(auto it = s.begin();it!=e.end()&&!isspace(*it);++it){
    *it = toupper(*it);
}
```

##### 迭代器类型

```c++
  vector<int>::iterator it;
  string::iterator it1;

  vector<int>::const_iterator it3;//只读，不能写
```

**begin和end运算符**

begin和and返回的运算是由对象是否是常量决定

如果对象是常量则返回const_iterator否则返回iterator

```c++
  vector<int> v1;
  const vector<int> v2;
  v1.begin();
  v2.begin();
```

如果想要在一个普通的容器中得到const_iterator可以使用cbegin运算符

##### 结合解引用和成员访问操作

`(*it).empty()`注意圆括号必不可少，没有圆括号则会是迭代器的empty成员则会错误

为了简化这种操纵可以使用`->`这个结合了解引用和成员访问`it->empty()`

**迭代器运算**

=  -  >  <

### 数组

**初始化数组**

初始化数组的时候`[]`内必须是一个常量表达式

**字符数组的特殊性**

```c++
 char a1[]={'c','+','+'};
  char a2[]={'c','a','\0'};
  char a3[]="c++";
  const char a4[6]="Danial";//err 不能存放空白字符
```

* 不允许拷贝和复制

```c++
char a4[]=a1;//err
a2=a1;//err
```

#### 复杂类型的数组声明

```c++
int *ptrs[10];//整型指针的数组
int &refs[10];//err没有引用数组
int (*Parray)[10]=&arr;//Parray指向一个含有10个整数的数组
int (&arrRef)[10]=arr;//arrRef引用含有10个整数的数组
```

这种情况一般会从`()`从内向外阅读

`int *(&arry)[10]=ptrs//arry是数组的引用，该数组含有10个int指针`

#### 访问数组元素

可以通过下标访问元素

和string，vector一样也可以使用for

```c++
for(auto i : scores){
    cout << i << " ";
}
```

#### 数组和指针

在很多地方，数组的名字会被编译器自动替换为数组的首元素指针

```c++
int arr[]={1,2,3,4,5};
auto ia2(arr);//ia2是一个指针，指向arr的首元素
auto ia(&arr[0]);
```

**注意**

当使用decltype时不会发生以上操作会返回值为int类型数组

```c++
decltype(arr) ia3={0,1,3,4};
```

#### 指针也是迭代器

指针在数组中和迭代器一样可以进行`+  -`操作

数组的尾后指针不知想具体的元素，因此不能最尾后指针进行加减或解引用操作.

#### begin和end操作

返回头/尾后指针

```c++
int ia[]={1,2,3,4,5,6};
int *beg=begin(ia);
int *last=end(ia);
```

这样方便了操作

#### 指针运算

```c++
int arr[5]={1,2,3,4,5};
int *IP= arr;
```

加上某个整数值结果依旧是指针，这个指针前进了该整数值的n个int类型位置

在数组中，如果这个数值大于数组的长度则会错误

**指针的比较**

- 如果指针指向同一数组的元素，或者指向该数组的尾元素的下一个位置（尾后元素）那么就可以通过比较运算符比较

- 如果指向不相关的对象，则不能比较

> 上述运算和比较同样适用于空指针和所指对象并非数组的指针。

**解引用和指针运算交互**

```c++
int ia[]={1,2,3,4};
int last = *(ia+2);
```

#### 与旧代码的接口

##### string

* 允许使用字符换来初始化string
* 允许使用空字符结尾的char数组来初始化
* 加法运算时允许使用空字符结尾的char数组

以上反过来不行

##### vector

允许使用数组来初始化一个vector

```c++
int arr[]={1,2,3,4};
vector<int> ivec(begin(arr),end(err));
```

同理遵循左包右不包可以实现部分数组的初始化

#### 多维数组

##### 初始化

```c++
int ia[3][4]= {
    {0,1,3,4},
    {4,5,6,7},
    {8,9,10,11}
};

int ia[3][4]={0,1,2,3,4,5,6,7,8,9,10,11};//与上面等价


```

可以显式的初始化行首

```c++
int ia[3][4]={
    {0},
    {4},
    {8}
};
```

`int ia[3][4]={0,1,2,3,4}`只初始化第一行的元素

##### 多维数组下标的引用

`ia[0]`代表的是第一行不是单个元素

```c++
int  (&row)[4] = ia[1];
//把row定义为一个含有4个整数的数组引用，然后绑定ia的第二行

  int ia[3][4]= {0,1,2,3,4,5,6,7,8,9,10,11};

  (*ia)[0]=100;

  printf("%d\n",**ia);//100

  int (&row)[4] = ia[1];

  cout << row[1]<<endl;//5

```

**使用for循环来遍历数组**

```c++
  for (auto &col : ia){//如果不用改变值则不用加入引用符号
    for (auto &row : col){
      row = 1;
    }
  }
```

```c++
  for (const auto &col : ia){//此处使用引用类型是为了避免直接使用数组名，数组被自动转变为指针
    for (auto row : col){
      cout << row << endl ;
    }
  }
//如果没有&则会编译出错
```

##### 指针和多维数组

因为多维数组其实就是数组的数组

因此多为数组名转变来的是一个内层数组的指针

```c++
  int (*p)[4]=ia;//指向一个4个元素的数组
  int *p[4];//整型指针的数组
```

使用auto就可以谜面在数组前面加上指针类型了

```c++
//p指向一个数组
  for(auto p = ia ; p!=ia+3 ; ++p){
    for (auto q = *p; q!=*p+4 ;++q)//q指向一个元素
    {
      cout << *q << endl;
    }
    
  }
```

使用begin和end也可以实现同样功能

```c++
//p指向一个数组
  for(auto p = begin(ia) ; p!=end(ia) ; ++p){
    for (auto q = begin(*p); q!=end(*p) ;++q)//q指向一个元素
    {
      cout << *q << endl;
    }
    
  }
```

这样看起来更简便

**使用别名来简化多维数组的指针**

```c++
using int_array = int [4];
typedef int int_array[4];

//p指向一个数组
  for(int_array *p = begin(ia) ; p!=end(ia) ; ++p){
    for (int *q = begin(*p); q!=end(*p) ;++q)//q指向一个元素
    {
      cout << *q << endl;
    }
    
  }
```

使用int_arrary来定义外层变量看起来更加简洁

## 表达式

### 基础

#### 左值和右值

左值表达式的求值结果是一个对象和函数

归纳：当一个对象被用作右值的时候，用的是对象的值。用作左值的时候用的是对象的身份（内存中的位置）

* 取地址：需要一个左值，返回一个指针(右值)
* 解引用和小标运算符的求职结果是一个左值
* 内置类型和迭代器地震：作用域左值，返回一个左值

> 首先，让我们避开那些正式的定义。在C++中，一个左值是指向一个指定内存的东西。另一方面，右值就是不指向任何地方的东西。通常来说，右值是暂时和短命的，而左值则活的很久，因为他们以变量的形式（variable）存在。我们可以将左值看作为容器（container）而将右值看做容器中的事物。如果容器消失了，容器中的事物也就自然就无法存在了。
> int* y = &x;  //ok
>
> 在这里我通过取地址操作符`&`获取了`x`的内存地址并且把它放进了`y`。`&`操作符需要一个左值并且产生了一个右值，这也是另一个完全合法的操作：在赋值操作符的左边我们有一个左值（一个变量），在右边我们使用取地址操作符产生的右值。
>  然而，我们不能这样写：
>
> ```cpp
> int y;
> 666 = y; //error
> ```
>
> 
>
> 
>
> 
>
> 我们知道一个赋值的左操作数必须是一个左值，因此下面的这个函数肯定会抛出错误：`lvalue required as left operand of assignment`
>
> 
>
> ```cpp
> int setValue()
> {
>     return 6;
> }
> 
> // ... somewhere in main() ...
> 
> setValue() = 3; // error!
> ```
>
> 错误原因很清楚：`setValue()`返回了一个右值（一个临时值`6`），他不能作为一个赋值的左操作数。现在，我们看看如果函数返回一个左值，这样的赋值会发生什么变化。看下面的代码片段（snippet）：
>
> 
>
> ```csharp
> int global = 100;
> 
> int& setGlobal()
> {
>     return global;    
> }
> 
> // ... somewhere in main() ...
> 
> setGlobal() = 400; // OK
> ```
>
> 该程序可以运行，因为在这里`setGlobal()`返回一个引用（reference），跟之前的`setValue()`不同。一个引用是指向一个已经存在的内存位置（`global`变量）的东西，因此它是一个左值，所以它能被赋值。注意这里的`&`：它不是取地址操作符，他定义了返回的类型（一个引用）。
>  可以从函数返回左值看上去有些隐晦，它在你做一些进阶的编程例如实现一些操作符的重载（implementing overload operators）时会很有作用，这些知识会在未来的章节中讲述。
>
> 
>
> # 四、左值到右值的转换
>
> 一个左值可以被转换（convert）为右值，这完全合法且经常发生。让我们先用`+`操作符作为一个例子，根据C++的规范（specification），它使用两个右值作为参数并返回一个右值（译者按：可以将操作符理解为一个函数）。
>  让我们看下面的代码片段：
>
> 
>
> ```cpp
> int x = 1;
> int y = 3;
> int z = x + y;   // ok
> ```
>
> 等一下，`x`和`y`是左值，但是加法操作符需要右值作为参数：发生了什么？答案很简单：`x`和`y`经历了一个隐式（implicit）的左值到右值（lvalue-to-rvalue）的转换。许多其他的操作符也有同样的转换——减法、加法、除法等等。
>
> 
>
> # 五、左值引用
>
> 相反呢？一个右值可以被转化为左值吗？不可以，它不是技术所限，而是C++编程语言就是那样设计的。
>  在C++中，当你做这样的事：
>
> 
>
> ```cpp
> int y = 10;
> int& yref = y;
> yref++;        // y is now 11
> ```
>
> 这里将`yref`声明为类型`int&`：一个对`y`的引用，它被称作左值引用（lvalue reference）。现在你可以开心地通过该引用改变`y`的值了。
>  我们知道，一个引用必须只想一个具体的内存位置中的一个已经存在的对象，即一个左值。这里`y`确实存在，所以代码运行完美。
>  现在，如果我缩短整个过程，尝试将`10`直接赋值给我的引用，并且没有任何对象持有该引用，将会发生什么？
>
> 
>
> ```cpp
> int& yref = 10;  // will it work?
> ```
>
> 在右边我们有一个临时值，一个需要被存储在一个左值中的右值。在左边我们有一个引用（一个左值），他应该指向一个已经存在的对象。但是`10` 是一个数字常量（numeric constant），也就是一个左值，将它赋给引用与引用所表述的精神冲突。
>  如果你仔细想想，那就是被禁止的从右值到左值的转换。一个`volitile`的数字常量（右值）如果想要被引用，需要先变成一个左值。如果那被允许，你就可以通过它的引用来改变数字常量的值。相当没有意义，不是吗？更重要的是，一旦这些值不再存在这些引用该指向哪里呢？
>  下面的代码片段同样会发生错误，原因跟刚才的一样：
>
> 
>
> ```cpp
> void fnc(int& x)
> {
> }
> 
> int main()
> {
>     fnc(10);  // Nope!
>     // This works instead:
>     // int x = 10;
>     // fnc(x);
> }
> ```
>
> 我将一个临时值`10`传入了一个需要引用作为参数的函数中，产生了将右值转换为左值的错误。这里有一个解决方法（workaround），创造一个临时的变量来存储右值，然后将变量传入函数中（就像注释中写的那样）。将一个数字传入一个函数确实不太方便。
>
> # 六、常量左值引用
>
> 先看看GCC对于之前两个代码片段给出的错误提示：
>
> > error: invalid initialization of non-const reference of type 'int&' from an rvalue of type 'int'
>
> GCC认为引用不是`const`的，即一个常量。根据C++规范，你可以将一个`const`的左值绑定到一个右值上，所以下面的代码可以成功运行：
>
> 
>
> ```csharp
> const int& ref = 10;  // OK!
> ```
>
> 当然，下面的也是：
>
> 
>
> ```cpp
> void fnc(const int& x)
> {
> }
> 
> int main()
> {
>     fnc(10);  // OK!
> }
> ```
>
> 背后的道理是相当直接的，字面常量`10`是`volatile`的并且会很快失效（expire），所以给他一个引用是没什么意义的。如果我们让引用本身变成常量引用，那样的话该引用指向的值就不能被改变了。现在右值被修改的问题被很好地解决了。同样，这不是一个技术限制，而是C ++人员为避免愚蠢麻烦所作的选择。
>  *应用：C++中经常通过常量引用来将值传入函数中，这避免了不必要的临时对象的创建和拷贝。*
>  编译器会为你创建一个隐藏的变量（即一个左值）来存储初始的字面常量，然后将隐藏的变量绑定到你的引用上去。那跟我之前的一组代码片段中手动完成的是一码事，例如：
>
> 
>
> ```csharp
> // the following...
> const int& ref = 10;
> 
> // ... would translate to:
> int __internal_unique_name = 10;
> const int& ref = __internal_unique_name;
> ```
>
> 现在你的引用指向了真实存在的事物（知道它走出作用域外）并且你可以正常使用它，出克改变他指向的值。
>
> 
>
> ```cpp
> const int& ref = 10;
> std::cout << ref << "\n";   // OK!
> std::cout << ++ref << "\n"; // error: increment of read-only reference ‘ref’
> ```
>
> # 七、结论
>
> 理解左值和右值的含义让我弄清楚了几个C++内在的工作方式。C++11进一步推动了右值的限定，引入了右值引用（rvalue reference）和移动（move semantics）的概念。这些将在下一篇[文章](https://www.jianshu.com/p/31cea1b6ee24)中介绍。
>
> 
>
> 作者：琼蘂无徵朝霞难挹
> 链接：https://www.jianshu.com/p/94b0221f64a5
> 来源：简书
> 著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

#### 优先级和结合律

`&&` `||` `?:` `,`四个符号只有当左侧运算符的值为真的时候才可以继续求右侧运算的对象



`f()+g()*h()+j()`

优先级：g与h的返回值相乘

结合律：f加上gh乘的和再加上j

如果f，g，h，j是无关函数，那么函数调用顺序不受限制

如果某几个函数影响同一个对象，那就可以能产生未定义的后果

> 经验：
>
> * 拿不准的时候最好用括号
> * 如果改变了某个运算对象的值，在表达式的其他地方就不要在使用这个运算对象。

#### 逻辑运算符

短路求值：只有当运算符左侧的值无法确定表达式结果的时候，才会计算右侧运算符

``` c++
  vector<string> text{"123123123.","231","","qweqweqwe","asdasdqwe"};

  for (const auto &s : text){
    cout << s;
    if(s.empty()||s[s.size()-1]=='.'){
      cout << endl;
    }else cout << "";
  }
//s是引用对象，因为数组可能很大，尽量避免对元素的拷贝！！！

```

> 比较的时候除非比较的对象是bool不然最好不要使用bool字面量

> 复赋值运算满足右结合律
>
> 同时赋值的优先级较低，需要使用括号来增加优先级

**混用解引用和递增运算符**

```c++

  auto pbeg = num.begin();
  while(pbeg!=num.end()&&*pbeg>0){
    cout << *pbeg++ << endl;
  }
```

`*pbeg++  ==  *(pbeg++)`

后置递增运算符的有优先级高于解引用

#### 运算对象可按任意顺序求值

如果一个表达式中，一个子式中改变了对象，另一个子式也改变那么结果可能查出预想如：

```c++
  while (pbeg!=num.end())
  {
    *pbeg = toupper(*pbeg++);
  }
  
```

有两种方式来运行

`*pbeg=topper(*pbeg)`

`*(pbeg+1)=topper(*pbeg)`

遍历器可能按照任意下面一种思路来处理。

#### 成员访问运算符

```c++
  string s1 = "123123123",*p=&s1;
  int n=(*p).size();
  n=p->size();//与上文等价
```

`*p.size`因为解引用的优先级低于点运算符，所以加括号会出现一个错误，因为p是一个指针，指针没有成员。

#### 条件运算符

`cond ? expr: exper`

```c++
  int grade = 70;
  string abc= (grade < 60) ? "fail" : "sucess";
  cout << abc << endl ;
```

**嵌套条件运算符**

条件运算符本身也是算是一个expr

因此可以进行嵌套

如

```c++
  abc = (grade  > 90 ) ? "high" :(grade < 60) ? "fail" : "success";

  cout << abc << endl;
```

**在输出中是用条件运算符**

条件运算符的右县级很低，因此在一条长语句中想要加上括号

```c++
  cout << ((grade < 60) ? "fail" : "sucess") << endl;

  cout << (grade < 60) ? "fail" : "sucess" ;//0
```

第二条等价于

```c++
cout << (grade < 69);
cout ? "fail" : "success";
```

