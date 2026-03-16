---
tags:
  - unity
---
## 位移

```c#
// 手动

transformer.position  = transformer.position + xxxx;

// api
transfromer.Translate(Vector3.forward); // local_transformer
transfromer.Translate(Vector3.forward, Space.World);
transfromer.Translate(this.transformer.forward, Space.World); // 自己的坐标系 
```

![hWqeFyQj4dco7Y9.png](https://s2.loli.net/2024/07/19/hWqeFyQj4dco7Y9.png)

https://www.cnblogs.com/unity3ds/p/10996476.html

vector3.forward的值永远等于（0，0，1）。

transform.forward的值则等于当前物体的自身坐标系z轴在世界坐标上指向，因此不一定等于(0,0,1)，但是其magnitude长度是1。

## 父子关系

```c#
this.transform.parent = null; //去除父对象，也可以得到
this.transform.SetParent(xxx.transform);
// 参数二： 是否保持本对象的transformer 的内容
this.transform.Find("xxx"); // 找子对象
this.transform.childCount; // 找儿子(失活也算) 不算孙子
this.transform.Getchild(x); 


// 儿子操作
son.IsChildOf(transform)
son.GetSiblingIndex();// 得到儿子编号
son.SetAsFirst/LastSibling();
son.SetAsFirstSiblingIndex(x);
```
