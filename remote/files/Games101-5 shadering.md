---
tags:
  - games101
---

## shader

- 对不同物体应用不同的材质


定义：

![600](https://s2.loli.net/2024/04/24/DMOfsTlIap986kE.png)


shading != shadow

## diffuse reflection 漫反射


**光照角度不同，则反射程度也不同**

![600](https://s2.loli.net/2024/04/24/VKaQmYCxrM6XlwF.png)


**于此同时物体离光源越远，反射程度越低**

![600](https://s2.loli.net/2024/04/24/67t3PWwq25xgRdI.png)

![600](https://s2.loli.net/2024/04/24/m7qFx8MAEXPOYhv.png)

![600](https://s2.loli.net/2024/04/24/jG7X4KfWcTDZE32.png)

## 高光项

镜面反射和视线比较接近的时候

使用半程向量计算高光

![600](https://s2.loli.net/2024/04/26/GYqKsO7ragHXWZT.png)


注： 

- 半程向量比较好算，反射向量比较难算
- 指数 p ： cos 容忍度太高了，光斑太大  --- 200 - 600

![600](https://s2.loli.net/2024/04/26/dPJEupAaC365kY2.png)

![600](https://s2.loli.net/2024/04/26/hnV6B4WY5c78CHi.png)


## ambient term 环境光

![600](https://s2.loli.net/2024/04/26/JhLI2Ew3va96UFi.png)

![600](https://s2.loli.net/2024/04/26/SGimFXunvb6L8HQ.png)


## shading frequencies

![600](https://s2.loli.net/2024/04/26/WKAYEnReyBNPDcI.png)

![600](https://s2.loli.net/2024/04/26/AMX3JqkmQhWiCRZ.png)

![600](https://s2.loli.net/2024/04/26/PQRdaAbrEieGV72.png)

![600](https://s2.loli.net/2024/04/26/PpsE56SnbLwVtTA.png)


### 定义法线

**定义每个顶点的法线**

![600](https://s2.loli.net/2024/04/26/NSfaxdLtl79sI6c.png)


**定义每个像素的法线**

![600](https://s2.loli.net/2024/04/26/kImFaCGr4fWSy8j.png)

## 渲染管线

![600](https://s2.loli.net/2024/04/26/4adflLHFK3xQp2I.png)


Texture mapping -- 纹理映射

![600](https://s2.loli.net/2024/04/26/nKk6V9ZO8lqiu5v.png)


![600](https://s2.loli.net/2024/04/26/9G5hitVwfbQBSFT.png)

> shadertoy.com
> https://youtu.be/XuSnLbB1j6E

## Texture Mapping

不同材质的漫反射系数不同。 三维物体的表面都是二维的

![600](https://s2.loli.net/2024/04/26/RbFMY9zscG4v5eH.png)


![600](https://s2.loli.net/2024/04/26/uj6reHXGDM4RvB8.png)

![600](https://s2.loli.net/2024/04/26/QqtPcVwgjyFNErs.png)

UV坐标系 --- 都在 0-1， 每个三角形的顶点都对应一个UV坐标

![600](https://s2.loli.net/2024/04/26/oX3NzxDWtGanRFJ.png)



## 重心坐标  barycentric coordinate

在三角形内做插值

obtain smoothly varying values across triangles

![600](https://s2.loli.net/2024/04/27/klPDFqsd7iCnKJg.png)

常数 为非负数

![600](https://s2.loli.net/2024/04/27/BsTvFQSnifWkuqH.png)



![600](https://s2.loli.net/2024/04/27/AQI7PwcMfqELZRK.png)
根据面积计算

![600](https://s2.loli.net/2024/04/27/IwrS83at1JWpY4z.png)

### 使用重心坐标进行插值

![600](https://s2.loli.net/2024/04/27/PJOsvn5RZpMhIFw.png)

**问题：** 投影之后重心坐标会改变--- 不能对投影之后的三角形计算重心。


## 使用 texture

![600](https://s2.loli.net/2024/04/27/d36YWHE8sM4OePq.png)

## 问题：

**texture Magnification** 纹理放大。

![600](https://s2.loli.net/2024/04/27/E8PQzHjXkRhNwVn.png)


查找纹理的时候我们希望更加连续一点。
- 使用双线性插值

![600](https://s2.loli.net/2024/04/27/SbjdxtmsXefVhDH.png)

![600](https://s2.loli.net/2024/04/27/tVLjmHxi74fhAFI.png)

![600](https://s2.loli.net/2024/04/27/aolxpzjRHeNfh63.png)


### Bicubic

临近的16个

### texture is too big

![600](https://s2.loli.net/2024/04/27/Qp5sXbNhkHEdqGJ.png)

![600](https://s2.loli.net/2024/04/27/7uzMXCENvTldRfm.png)


![600](https://s2.loli.net/2024/04/27/Q9YXhlm1Seba5ci.png)


![600](https://s2.loli.net/2024/04/27/rxbg769ZQuGEp4X.png)

### mipmap

allowing (fast approx square) range queries

![600](https://s2.loli.net/2024/04/27/JaQP8s6FYd5qrBe.png)

![600](https://s2.loli.net/2024/04/27/Bw9sxKXP7VTJ6dN.png)


## 计算 mipmap 的level

![600](https://s2.loli.net/2024/04/27/wDCIjUKpxYuLWak.png)

![600](https://s2.loli.net/2024/04/27/Ij7hpi5TXFrRta3.png)


![600](https://s2.loli.net/2024/04/27/4qPpn3cutsCAXbr.png)


![600](https://s2.loli.net/2024/04/27/47utiElsDmyOxUq.png)

如果在 1.8层 这种非整数层 --- 使用三线性插值计算

Trilinear interpolation

![600](https://s2.loli.net/2024/04/27/Rxhw87gbI9mJjMW.png)

**三线性插值 的 资源消耗很小，但是效果很好**

![600](https://s2.loli.net/2024/04/27/MW6anN1sChXUzB7.png)


## mipmap 的限制

overblur

![600](https://s2.loli.net/2024/04/27/Y6reqhtPylm1Bb7.png)

**解决方案 -- anisotroptic filtering  各项异性过滤** ---部分解决

![600](https://s2.loli.net/2024/04/27/XHTm8q7sfZSGD4e.png)

![600](https://s2.loli.net/2024/04/27/i2Ar9tOdZ7poe5b.png)

EWA 过滤

![600](https://s2.loli.net/2024/04/27/PWTLUYo61ybeK7I.png)

## 纹理的应用

![600](https://s2.loli.net/2024/04/28/RjEndcQWXyT3C1g.png)

![600](https://s2.loli.net/2024/04/28/Q6NvLTtKar9JPVz.png)

问题： 贴图会扭曲。

![600](https://s2.loli.net/2024/04/28/WGPxpjKgLZJadIM.png)

![600](https://s2.loli.net/2024/04/28/ZltOzpyD4fNc3wi.png)


**凹凸贴图**

![600](https://s2.loli.net/2024/04/28/MawGQbizNpWgvk4.png)


**法线贴图**

![600](https://s2.loli.net/2024/04/28/wpkCfnQuLjFoG1W.png)


![600](https://s2.loli.net/2024/04/28/LhJzOVnlES2PK4a.png)

![600](https://s2.loli.net/2024/04/28/CcxKMZBw73tXduo.png)

**位移贴图**

![600](https://s2.loli.net/2024/04/28/8z3IvHqcXFpPQNK.png)


**3D噪声**

![600](https://s2.loli.net/2024/04/28/gpMaDzcYUFAvLNJ.png)

![600](https://s2.loli.net/2024/04/28/aiBVkEKZoQA1OHL.png)

**三维纹理**

![600](https://s2.loli.net/2024/04/28/BfbRUgX9lIJGxWj.png)

