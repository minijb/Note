---
tags:
  - games101
---

implicit -- 隐式几何
explicit -- 显示几何

### implicit

- 点不需要知道位置，但是可以用点之间的关系表示 (按照类别归类)
	- E.g. all points in 3D, where $x^2+y^2+z^2=1$
	- 更通用的表示 $f(x,y,z) = 0$

劣势 ： 不直观
优势 ： 可以很简单的判断一个点是否再物体内或者外。

### explicit

![600](https://s2.loli.net/2024/05/04/sHvhfRILWzGuedZ.png)

![600](https://s2.loli.net/2024/05/04/AHpRKBW29kYmfMt.png)

很难判断点是否在体积内

## 隐式表示

![600](https://s2.loli.net/2024/05/04/8ZWBapYwObF6S7y.png)

![600](https://s2.loli.net/2024/05/04/oUV6wR2p9lbBsg8.png)

![600](https://s2.loli.net/2024/05/04/VdKbN7ACSaeinLX.png)

![600](https://s2.loli.net/2024/05/04/LR2vmYwDQEMaySJ.png)

![600](https://s2.loli.net/2024/05/04/LTjAOax4efVovDr.png)


**分形**

![600](https://s2.loli.net/2024/05/04/mDaNMVEv9yIQLiw.png)


![600](https://s2.loli.net/2024/05/04/Wnrj1epdVqP2Jhf.png)
## explicit

![600](https://s2.loli.net/2024/05/04/MpIgXWq4Uzn1HEJ.png)

![600](https://s2.loli.net/2024/05/04/Rbspo2DmIMuq1Af.png)


![600](https://s2.loli.net/2024/05/04/iVTKEQ2S9dbyAtf.png)

## curves 曲线

### 贝塞尔曲线

贝塞尔曲线：使用控制点来控制曲线

![600](https://s2.loli.net/2024/05/04/ZMKpArjebosOWTi.png)

 
 
 **三个点**
 
 ![600](https://s2.loli.net/2024/05/04/fGcKx6WdQ2R9m8B.png)
 
 ![600](https://s2.loli.net/2024/05/04/d2vxpY7GkHFh4Xj.png)

**四个点**

![600](https://s2.loli.net/2024/05/04/xTXqoWsDfNagVA3.png)

![600](https://s2.loli.net/2024/05/04/fQdPL1S2RqUI7pK.png)

![600](https://s2.loli.net/2024/05/04/IrfsZThKFOwEjQW.png)

多次线性插值

![600](https://s2.loli.net/2024/05/04/LZJdiCDnrgtRY4o.png)

![600](https://s2.loli.net/2024/05/04/DykoGO1cBIwebH7.png)


![600](https://s2.loli.net/2024/05/04/cTDpmSQqBxUbJv7.png)


![600](https://s2.loli.net/2024/05/04/Vn2JeOXj9gQAl78.png)


### 性质

![600](https://s2.loli.net/2024/05/04/ntuAXD54jkLrBsv.png)


投影变换 --- 直接投影控制点和起始终止点
凸包性质 --- 贝塞尔曲线必定在控制点形成的凸包内

**凸包**

![600](https://s2.loli.net/2024/05/04/KHSi3fZoDh89ayJ.png)


### piecewise 贝塞尔曲线

如果控制点过多，不好控制

习惯使用4个控制点控制一段曲线

![600](https://s2.loli.net/2024/05/04/UD1VbSAqT5QeMvO.png)

保证曲线光滑 --- 一个点相连的控制点长度相同，方向相反就是连续的

![600](https://s2.loli.net/2024/05/04/eSZnQ4yk9aqzHOX.png)

![600](https://s2.loli.net/2024/05/04/JIwGSROdXArej9b.png)



### 其他曲线

![600](https://s2.loli.net/2024/05/04/WPKZXym7tJvYbdk.png)


![600](https://s2.loli.net/2024/05/04/WCYmOTg5Hv1KrIB.png)
## 表面 surface

![600](https://s2.loli.net/2024/05/04/ojZQGS5dNrgVAXv.png)


使用贝塞尔曲线得到曲面

![600](https://s2.loli.net/2024/05/04/WexO8Sm1IcoKEZC.png)


![600](https://s2.loli.net/2024/05/04/vx75PMsz9VwqZng.png)

![600](https://s2.loli.net/2024/05/04/Sf8NvVAX94cOPDu.png)

![600](https://s2.loli.net/2024/05/04/1djzKVY6o2NO9gL.png)

![600](https://s2.loli.net/2024/05/04/Y9XTpmUaOd3ocQ6.png)


## Loop subdivisom

- 增加三角形的数量--- 一分四
- 对于新旧节点进行分类

![600](https://s2.loli.net/2024/05/04/YzgFoVjLd8M7wUJ.png)

对新顶点进行位置更新

![600](https://s2.loli.net/2024/05/04/OeRoQJqs7mCDdwF.png)

对旧顶点进行位置更新

![600](https://s2.loli.net/2024/05/04/4SrNfXGdC2OK8Eq.png)

n : 度 

## catmull-Clark subdivision

![600](https://s2.loli.net/2024/05/04/dHenAXjlTWyYEzG.png)


![600](https://s2.loli.net/2024/05/04/FwbuoYaO1q9tQJc.png)

问题：一次细分 所有非四边形面会消失，增加对应的奇异点。  之后奇异点数量不会增加。

![600](https://s2.loli.net/2024/05/04/pNgjaZynlv3TLq6.png)


![600](https://s2.loli.net/2024/05/04/JopQXWPAVxZIEGb.png)

![600](https://s2.loli.net/2024/05/04/sEW5QuNIw2ehKLM.png)

## mesh simplification

![600](https://s2.loli.net/2024/05/04/DrUw5MNdbpfqgsQ.png)

![600](https://s2.loli.net/2024/05/04/9SADLTVxUryoMKu.png)


![Xa3VIb9Wtfy1ASu.png](https://s2.loli.net/2024/05/04/Xa3VIb9Wtfy1ASu.png)


![600](https://s2.loli.net/2024/05/04/TA2eahkCEmlDUHt.png)

![600](https://s2.loli.net/2024/05/04/8nxPEJSGAperliT.png)


