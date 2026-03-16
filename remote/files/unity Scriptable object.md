---
tags:
  - unity
---
是什么?  一堆我们定义的数据，方便我们之后进行初始化。

```c#
[CreateAssetMenu(fileName = "TestObject", menuName = "ScritableObjects/TestObject")]
public class TestObject : ScriptableObject
{
    public string MyString;
}
```

此时我们可以批量创建多个类型相同，但是内容不同的 scriptable object, 用于记录数据(用来记录grid大小以及特点)，也可以用来制作编辑器工具(如 URP 资源文件)。

可用来接解决资源，比如每种敌人都有武器，如果每个武器都有数据，如果有大量敌人，那么数据就会被大量复制。如果武器数据是 scriptable object 那么这就是一种引用，无需大量复制。

> [Minecraft Crafting System in Unity](https://www.youtube.com/watch?v=LmQ6U3YkHHk)

## 注意

build 之后 改变 scriptable obj 还会变为原始值