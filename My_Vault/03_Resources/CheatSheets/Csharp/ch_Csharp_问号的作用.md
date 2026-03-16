
- 三目运算符
- 基本数据类型可空标识符

```C#
public int? iNull1;
```


- 在赋值的结果中的变量如果为空则用??后面的值替代前面的变量，否则直接用前面的变量

```c#
string str1 = null;
string str2 = str1?? "name";
```

- null 条件运算符

```c#
int num = test1?.Num;
```

