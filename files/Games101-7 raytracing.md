---
tags:
  - games101
---

shadow mapping

![600](https://s2.loli.net/2024/05/04/trIdOjCMi28zvVJ.png)


思想：光源可以看到点，人也可以看到的点。 --- 不在shadow中的点

**只能处理点光源**

![600](https://s2.loli.net/2024/05/04/z4dIo6KZHqiY2AB.png)

深度不一致

![600](https://s2.loli.net/2024/05/04/qsKOTAnSutCfkgJ.png)

![600](https://s2.loli.net/2024/05/04/BP3zOFl2ah5xKJM.png)

![600](https://s2.loli.net/2024/05/04/mJC83MXUtzi65hK.png)

![600](https://s2.loli.net/2024/05/04/tDgjNrHdmTyeGoq.png)

![600](https://s2.loli.net/2024/05/04/VYs9TyOdqopuLCZ.png)

浮点数的精度问题。

![600](https://s2.loli.net/2024/05/04/5vTQrmlIoYnME1N.png)

### 软/硬阴影

![600](https://s2.loli.net/2024/05/04/PDWecTHgdVZ1uYr.png)



## ray tracing

- 直线传播
- 不会碰撞
- 从光源出发，到人眼
- 光线是可以反射的

![600](https://s2.loli.net/2024/05/04/PDWecTHgdVZ1uYr.png)

![600](https://s2.loli.net/2024/05/06/QoL9N13H2xYgFWB.png)


多次弹射的光纤追踪

![600](https://s2.loli.net/2024/05/06/6eFmzxoE3nGOdsV.png)


## ray equation

![600](https://s2.loli.net/2024/05/06/8bqWzc6JyuxCHoK.png)

![600](https://s2.loli.net/2024/05/06/kfrpP1vJdb6AnBs.png)

![600](https://s2.loli.net/2024/05/06/bCgEFpMhlHL26ei.png)


对隐式表面

![600](https://s2.loli.net/2024/05/06/5jQ6WnDXIiurRM1.png)


对显示表面 --- 对三角形求交

![600](https://s2.loli.net/2024/05/06/9MtFyRPDa81eH7E.png)

和每个三角形求交 --- 0/1

简化问题：先和平面求交，再计算点是否再平面内

![600](https://s2.loli.net/2024/05/06/TIYShxvZMFawCpq.png)

平面的定义 ： 一个平面 = 一个点 + 一个发现

![600](https://s2.loli.net/2024/05/06/7fZKXIh6pPOTi8d.png)

![600](https://s2.loli.net/2024/05/06/Jk9P2c8j5OLMSqG.png)

直接计算 是否在三角形内

![600](https://s2.loli.net/2024/05/06/4Y6Hw3QluWPrDfS.png)



### 加速 计算

![600](https://s2.loli.net/2024/05/07/vaChp2xoWYmHwE6.png)

![600](https://s2.loli.net/2024/05/07/2XibRdZx6rVoyKW.png)


### Bounding Volumes

![600](https://s2.loli.net/2024/05/07/CSnY7EdLh4OpeJW.png)


保证物体一定在某个图形范围内。 --- AABB

![600](https://s2.loli.net/2024/05/07/16Yu2DaZoghTVk5.png)

光线和包围盒如何求教

![600](https://s2.loli.net/2024/05/07/FCuw8xBEDZlW2ih.png)

求交集 就可以得到。

![600](https://s2.loli.net/2024/05/07/7uN8UfG2JMXYnOg.png)

一些特殊情况

![600](https://s2.loli.net/2024/05/07/ZGQ4gryEmxp6JBn.png)

一些细节

![600](https://s2.loli.net/2024/05/07/yrxHbU4sjBO2KkM.png)


GTC news : DLSS RTXGI

### 使用AABB进行加速

![600](https://s2.loli.net/2024/05/07/uyPBH2rOfvY4tKW.png)

![600](https://s2.loli.net/2024/05/07/RdSGYKpeivn7DsI.png)

![600](https://s2.loli.net/2024/05/07/1le9cMZ3dHnXvVC.png)


如果物体大小不一，同时稀疏不一，那么就不适合使用格子的方法。

![600](https://s2.loli.net/2024/05/07/ComQPrkNjbLZOuB.png)

### KD-Tree

![600](https://s2.loli.net/2024/05/07/wNgmB9dvOGMFaUy.png)

![600](https://s2.loli.net/2024/05/07/uhSgRGjJOAZoEfQ.png)


**如何加速**

![600](https://s2.loli.net/2024/05/07/KvPCxDwirIZUAF2.png)

![600](https://s2.loli.net/2024/05/07/x8Smd7OCT3wAnir.png)

**问题：AABB和三角形是否有交集** 比较难判断
一个物体可能和多个节点内出现。

### Object Partitions 从物体进行划分 BVH Bounding Volume Hierarchy 

![600](https://s2.loli.net/2024/05/07/DJMih2n9jYmNUKf.png)
![600](https://s2.loli.net/2024/05/07/JFZvSz728OHNlqD.png)

问题: bounding box 可能会相交

### 如何划分BVH

> 找中位数， 快速划分

![600](https://s2.loli.net/2024/05/07/l1KgFwVxyUfOYQD.png)

![600](https://s2.loli.net/2024/05/07/FYo7gC2U8n9vy4W.png)

![600](https://s2.loli.net/2024/05/07/oLZR7HNCb2ukmnz.png)

### 两种划分的差异

![600](https://s2.loli.net/2024/05/07/XUoC37Lfsk4PIJx.png)


