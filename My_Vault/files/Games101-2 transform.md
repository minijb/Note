---
tags:
  - games101
---

- 2D point  = $(x,y,1)^T$
- 2D vector = $(x,y,0)^T$ --- 平移不变性

![600](https://s2.loli.net/2024/04/21/8FS5imYNu7jzwLQ.png)


## transform

### translation

![600](https://s2.loli.net/2024/04/21/jAXFC2tK5OZ16qU.png)

### Affine transformner

![600](https://s2.loli.net/2024/04/21/IS4Aye1aziFobjd.png)

![600](https://s2.loli.net/2024/04/21/gpjuTIEFXnYMzSt.png)


## 逆变换

就是逆矩阵

## 变换的组合

矩阵的乘法

## 变换的分解

- 变换到中心
- 旋转
- 变换回原始位置

## 三维

![600](https://s2.loli.net/2024/04/21/nX7GsE8wdILb1zq.png)


![600](https://s2.loli.net/2024/04/21/GXF68lWnpxQtcfy.png)


## 3D 旋转

![600](https://s2.loli.net/2024/04/21/eaO4VpzP5TWQb2h.png)
## view transformation

- model transform
- view transform
- projection transform

![600](https://s2.loli.net/2024/04/21/3IFfJPgBVrQknbR.png)


关键特征：

- 如果相机和物体同时移动，则 效果相同
- 约定
	- 相机永远在原点
	- 看向 -z
	- Y轴为向上方向

![600](https://s2.loli.net/2024/04/21/z58Q3PGKOgrxHC9.png)


Model --- $M_{view}$  --- 将相机移动到原点


![600](https://s2.loli.net/2024/04/21/UTeMgpZLd1JFNvE.png)

![600](https://s2.loli.net/2024/04/21/mFev7lhKEyfs6Gt.png)

先求逆的旋转 再求逆变换。

### 投影

从三维到二维

两种投影
- 正交投影 
- 透视投影 -- 近大远小


- 约定
	- 人在画面的 z方向，面向 -z

### 正交投影

![600](https://s2.loli.net/2024/04/21/stoGApvB8gDOzyZ.png)

![600](https://s2.loli.net/2024/04/21/lPRi2Jk5QNyBfts.png)
![600](https://s2.loli.net/2024/04/21/SJzUgA7IF9YXLc5.png)

## 透视投影

- 平行的线不再平行

![600](https://s2.loli.net/2024/04/22/NKxc9TMF78ynroY.png)

![600](https://s2.loli.net/2024/04/22/b83J1fQkCXHMTcK.png)

![600](https://s2.loli.net/2024/04/22/j37V8cWBLtS4Tsv.png)


![600](https://s2.loli.net/2024/04/22/Dd1TbuE5itfGCo6.png)


z点的变换

- any point on the near plane will not change
- any point's z on the far plane will not change

![600](https://s2.loli.net/2024/04/22/qm5RbTAjLKPNUBk.png)

![600](https://s2.loli.net/2024/04/22/I1QFadRjJxzAeiS.png)

 ![600](https://s2.loli.net/2024/04/22/ywcAZ6H5IoSDtXR.png)


fov -- 可视角度 -- 分x和y

![600](https://s2.loli.net/2024/04/22/GgU2ROxbtrWLdpn.png)

