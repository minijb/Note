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
