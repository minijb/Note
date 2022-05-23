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
