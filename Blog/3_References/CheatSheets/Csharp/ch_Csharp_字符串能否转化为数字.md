
**方法1 :**

使用 Linq 进行快速遍历

```c#
if(number.All(char.IsDigit))
```

**方法2 :**

使用 tryParse

```c#
bool t = Int32.TryParse(number, out n);
```


