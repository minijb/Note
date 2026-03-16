---
tags:
  - unity
---
## OnEnable 造成的GC

OnEnable 的时候会初始化网格， 尤其是文字这些， 造成顶点在内存空间中频繁的创建和释放，这造成大量的GC。

解决
- 可以使用 canvas Group 通过设置透明度
- 将UI移出屏幕范围

https://zhuanlan.zhihu.com/p/609701493
