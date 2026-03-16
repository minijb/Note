---
tags:
  - games101
---
## Animation

![600](https://s2.loli.net/2024/05/24/rtDkCs2wyqLxMV6.png)

![600](https://s2.loli.net/2024/05/24/jrbAzSVZ3RdY6tK.png)


简单来说就是 插值

![600](https://s2.loli.net/2024/05/24/bv8EkZIxlQLdHmF.png)

**物理模拟**

最简单的模拟 : $F = ma$

![600](https://s2.loli.net/2024/05/24/l6CpveHLsUfXb7h.png)


### mass spring system 质点弹簧系统

![600](https://s2.loli.net/2024/05/24/3JHvjrMgwEO7AsW.png)

![600](https://s2.loli.net/2024/05/24/73yhvIkidc56V1P.png)


**是什么**

![600](https://s2.loli.net/2024/05/24/Y6hzCpItjKsv5q1.png)

拉多长就有多大的力 , a受到的力： a指向b

![600](https://s2.loli.net/2024/05/24/KCcvPzypjBeaiYb.png)


此时会永远的震度 --- 能量守恒。

加入摩擦力

![600](https://s2.loli.net/2024/05/24/7TqI29yYErbHj83.png)

![600](https://s2.loli.net/2024/05/24/VnypIfWNBaXFsht.png)


问题：所有的运动都会结束 

- 只能描述外部的力，不能描述内部的力 --- 弹簧内部的损耗


![600](https://s2.loli.net/2024/05/24/Tb2AecvXCJMpwjR.png)

和 ab之间的相对速度有关系 --- 摩擦力只有相对速度有关系

红框: 相对速度投影到方向上

### 不同的弹簧结构

![600](https://s2.loli.net/2024/05/24/edUgp6CZoS9cWE3.png)


- 切边
- 非平面的变化

![600](https://s2.loli.net/2024/05/24/ZrRM2Kb6aVwOY1D.png)

![600](https://s2.loli.net/2024/05/24/mA1QwlPIjkF9SCt.png)


红线 --- 不是强链，蓝色的 --- 强度较大

**粒子系统**

![600](https://s2.loli.net/2024/05/24/FHL5DXjhN6vJEms.png)


问题:

- 需要很多力
- 需要加速结构

![600](https://s2.loli.net/2024/05/24/mkPqb2w1ycsoYW5.png)

![600](https://s2.loli.net/2024/05/24/bTyzBhaeivAS2mE.png)

![600](https://s2.loli.net/2024/05/24/gEfnqM6eFZkAJcj.png)

![600](https://s2.loli.net/2024/05/24/4yLdTqC5nY7hR1U.png)

### 正向运动学

![600](https://s2.loli.net/2024/05/24/MIr6vTXJW8VBGbE.png)

![600](https://s2.loli.net/2024/05/24/ADo6adMZPjl72b4.png)

**问题**

![600](https://s2.loli.net/2024/05/24/2pXVYGx9m5TqSnJ.png)

### 逆向运动学

![600](https://s2.loli.net/2024/05/24/dh1zySkQAbKWt2a.png)

![600](https://s2.loli.net/2024/05/24/CO2ekcIpMnzXTfS.png)

固定 p 点，其他关节怎么动

- 解不唯一
- 存在无解

![600](https://s2.loli.net/2024/05/24/BALpFzws7lC8r1y.png)

### rigging -- 逆运动学的应用

木偶操作

![600](https://s2.loli.net/2024/05/24/42ULgbpry18hE6G.png)


**blend space** 使用插值生成动画

**动作捕捉**

![600](https://s2.loli.net/2024/05/24/VQi3DMSA6hHLYnB.png)

![600](https://s2.loli.net/2024/05/24/8c4i1FOTwGkWVsn.png)

## 欧拉方法

速度场

![600](https://s2.loli.net/2024/05/25/ka65cmYT1FsR3Zq.png)

ODE 常微分方程

![600](https://s2.loli.net/2024/05/25/VW2baULp61YZlDE.png)

### 欧拉方法

![600](https://s2.loli.net/2024/05/25/RkSvhKO4yVTtQba.png)

**误差**

![600](https://s2.loli.net/2024/05/25/6devaZQonqT4Rsj.png)


**稳定性问题**

![600](https://s2.loli.net/2024/05/25/ZhpmNgnW8Otx1rb.png)

![600](https://s2.loli.net/2024/05/25/ODoG25yFCMQzxSH.png)


### 解决方法

![600](https://s2.loli.net/2024/05/25/W2gnmwH1qGdeEUI.png)


**中点法**

![600](https://s2.loli.net/2024/05/25/jpJIUt2cORvC1EP.png)

![600](https://s2.loli.net/2024/05/25/tiaLQRn4g5Pevjw.png)

**自适应步长法**

如果差较大，则分

![600](https://s2.loli.net/2024/05/25/DyPorQvsIKOHGL4.png)


**隐式欧拉/后向方法**

![600](https://s2.loli.net/2024/05/25/VnDyBvb3p1L25qH.png)

![600](https://s2.loli.net/2024/05/25/wUcM1osn3lgENVf.png)

不好解。

**稳定性**

局部的误差，全局的误差
直接研究是无意义的，而是研究阶

![600](https://s2.loli.net/2024/05/25/VqIJXsU2NZRSQ51.png)


**Runge-Kutta** 方法

![600](https://s2.loli.net/2024/05/25/8QakoVtNJuYRhMF.png)


**postion-based** 方法 --- 基于非物理的

![600](https://s2.loli.net/2024/05/25/snfUc32eBriJ7pI.png)

### 刚体模拟

![600](https://s2.loli.net/2024/05/25/62iVDeRwAYIN9Kf.png)

**简单的例子**

- 水使用小球模拟
- 假设水不能压缩
- 密度应该是一样的

![600](https://s2.loli.net/2024/05/25/g654AkNQSiyw8Xh.png)

梯度下降。

![600](https://s2.loli.net/2024/05/25/EAceZXRhfS5DbCU.png)

![600](https://s2.loli.net/2024/05/25/damJCuyRc7zbwVE.png)

