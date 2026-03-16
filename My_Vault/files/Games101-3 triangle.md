---
tags:
  - games101
---

rasterize == drawing onto the screen

color = (red, green, blue)

![600](https://s2.loli.net/2024/04/22/pmFgPaqSx4BIyV2.png)



pixel indices are from (0,0) to (width-1, height-1)
pixel (x,y) is centered at (x+0.5, y+0.5) 

![600](https://s2.loli.net/2024/04/22/cp3hzKSCRPFrIyo.png)


![600](https://s2.loli.net/2024/04/22/hpCZuMPbdG7UAHz.png)


## 光栅化

判断一个像素的中心点是否需要draw

### 采样的方法 -- 将函数离散化

如果中心再三角形内。

![600](https://s2.loli.net/2024/04/22/saYLhyH1EQINmoq.png)


如何判断 inside -- 三次 cross product
如果再边界上 -- 不做处理或者特殊处理都可以 -- 这里不做处理

**加速方法**

- bounding box --- 包围盒 -- 不需要检查所有的像素点

jaggies -- 锯齿

