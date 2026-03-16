---
tags:
  - unity
---
大部分情况下，你可能会使用到这些函数：

- Quaternion.LookRotation，
- Quaternion.Angle
- Quaternion.Euler
- Quaternion.Slerp
- Quaternion.FromToRotation
- Quaternion.identity。

https://www.cnblogs.com/driftingclouds/p/6626183.html
https://blog.csdn.net/andrewfan/article/details/60866636

转,XYZ三个参数代表相应轴向按照顺归XYZ的旋转，因此(0、90、90)代表先进行+Z轴旋转90度，再沿着+Y轴进行90度旋转，