---
tags:
  - games101
---

![600](https://s2.loli.net/2024/05/13/p1s9JGQZgjTroUK.png)

![600](https://s2.loli.net/2024/05/13/CxSAD8wXKOtLMeZ.png)

漫反射的 prdf

glossy material  

![600](https://s2.loli.net/2024/05/13/N3OjgKzC7qcQSrE.png)

![600](https://s2.loli.net/2024/05/13/C27TJUPNqSkhdbr.png)

![600](https://s2.loli.net/2024/05/13/rRV8bNB6tWSYk4a.png)

![600](https://s2.loli.net/2024/05/13/CeDOQPf3t14R2Ja.png)

![600](https://s2.loli.net/2024/05/13/gvoKpZzSG8LNuMs.png)

**折射**  BTDF

![600](https://s2.loli.net/2024/05/13/w56HNnoPgFIlreD.png)

![600](https://s2.loli.net/2024/05/13/S3vwDy1rdiX2fpU.png)

![600](https://s2.loli.net/2024/05/13/6OjwRz2tLi3FX4K.png)


全反射的情况：

- $n_i$ 远大于 $n_{t}$  也就是说 入射密度大。
- 因此水底看空气 --- 会发生全反射情况。

![600](https://s2.loli.net/2024/05/13/NKdVhcZWFqMgYo2.png)


**fresnel reflection term 菲涅尔项**


![600](https://s2.loli.net/2024/05/13/UwGMvFori8kOcAp.png)

**绝缘体**
![600](https://s2.loli.net/2024/05/13/JRS7BwsmV4iDrLl.png)

见到那说就是 如果 如何入射光和法线几乎平行 --- 则大量会被反射。


**导体**

![600](https://s2.loli.net/2024/05/13/4TzGNRwa1iAkpVg.png)

![600](https://s2.loli.net/2024/05/13/Ov3QgzUBAW4xSMY.png)

## microfacet material 

![600](https://s2.loli.net/2024/05/13/XHOvp6Mk8RxfNPh.png)

**远处看是镜面， 近处看是几何**

![600](https://s2.loli.net/2024/05/13/ImZ6tPibRS9p4eM.png)

![600](https://s2.loli.net/2024/05/13/rtOxBjFHds4kT87.png)

把表面的粗糙程度使用发现的分布进行表示
- 集中 就是镜面
- 发散 就是漫反射

![600](https://s2.loli.net/2024/05/13/bdhiD8euWTFvYzQ.png)


![600](https://s2.loli.net/2024/05/13/RHg87Jel1YE5Mzx.png)


可以描述 大量 物体。 **当前在用的**  微表面模型有很多分类。

## Isotropic / Anisotropic materials BRDFs


**条形高光**

![600](https://s2.loli.net/2024/05/13/3tUfndLEXxCebyY.png)

- 各项同性 材质
- 各项异性 材质

![600](https://s2.loli.net/2024/05/13/wk7cIlmSsBniURu.png)

![600](https://s2.loli.net/2024/05/13/3Mh4xHLvWOjK1Qu.png)

![600](https://s2.loli.net/2024/05/13/gjkZ4Dwz7QX5KGJ.png)

![600](https://s2.loli.net/2024/05/13/uv8fUWzZEoGtI1F.png)

![600](https://s2.loli.net/2024/05/13/u1gaXpNBlFJcST6.png)

## BRDF

![600](https://s2.loli.net/2024/05/13/dRunrT4xNfoK8zY.png)

![600](https://s2.loli.net/2024/05/13/Frwd8tYy6ilfD9C.png)

![600](https://s2.loli.net/2024/05/13/ljdphucDwbEN8m9.png)

## 测量 BRDF

![600](https://s2.loli.net/2024/05/13/ZaDXk1xdSPGjV69.png)

![600](https://s2.loli.net/2024/05/13/YeG2V3yPujCl4ib.png)

![600](https://s2.loli.net/2024/05/13/HER6lX4mWbnQdBG.png)

![600](https://s2.loli.net/2024/05/13/f54z732kr1igjbF.png)

> MERL BRDF Database

