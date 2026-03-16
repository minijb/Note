---
tags:
  - unity
  - DrawCall
---

## 什么是 Draw Call

简单来说就是 CPU 调用 图形化接口 如 `glDrawElement`

## 如何减少 Draw Call

### 方法1  :  使用Batch

#unity-batch 

将很多小的 DrawCall 合并成一个大的DrawCall。 <span style="background:#40a9ff">注意</span> : 此方法适用于静态物体，对于动态物体也适用，但是由于空间和时间的影响，效果一般。

```ad-tip
title: 一些建议
- 避免使用大量小网格，如果必须则考虑合并
- 避免使用过多的材质，因为只有相同材质的物体才可以进行 batch
```

