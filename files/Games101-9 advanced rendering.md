---
tags:
  - games101
---

[Physically Based Rendering: From Theory to Implementation (pbr-book.org)](https://www.pbr-book.org/3ed-2018/contents)


## advanced light transport

有/无偏的光线传播方法

![600](https://s2.loli.net/2024/05/15/TGBVjkymS8wbZlR.png)

![600](https://s2.loli.net/2024/05/15/Ky2ZxrHltPfA4Wi.png)

### 双向路径追踪

![600](https://s2.loli.net/2024/05/15/Ucs4SQo85kDaN6J.png)

![600](https://s2.loli.net/2024/05/15/rtLFIRulTD2vCZx.png)

这里主要的光照为间接光 --- 不是直接光源 --- 实现比较困难。

![600](https://s2.loli.net/2024/05/15/ncAj6HWMq85RVPb.png)

使用马尔科夫链进行推测。

![600](https://s2.loli.net/2024/05/15/Q3GAiJXHmMx6kTC.png)

- 优势: 对于光线复杂的情况来水，比较好。
- 劣势: 无法分析其解析速度。所有操作是局部的，因此比较脏

![600](https://s2.loli.net/2024/05/15/9XEfUoJpKce6hrT.png)

### 光子映射  --- 有偏

![600](https://s2.loli.net/2024/05/15/FvZUJDYBxd4Lu7p.png)

![600](https://s2.loli.net/2024/05/15/mf5kcE1d2XynWwe.png)

![600](https://s2.loli.net/2024/05/15/8XMByQSd7RuD9Jt.png)

局部密度估计。

![600](https://s2.loli.net/2024/05/15/C1OavNbAYKIX9yQ.png)


有偏 --- 模糊
一致 --- 如果样本足够就不模糊

**将双向路径追踪 结合  光子映射**

## IR

![600](https://s2.loli.net/2024/05/16/3sjivOIPBbSAmTk.png)


![600](https://s2.loli.net/2024/05/16/6lLvHbKzFo72CpG.png)


## appearance modeling

### participating media

![600](https://s2.loli.net/2024/05/16/dAQnEWhZkbiG3CJ.png)

![600](https://s2.loli.net/2024/05/16/uRGHZf5pT2IsUbO.png)

![600](https://s2.loli.net/2024/05/16/nxRDOmuVAoNZ468.png)

![600](https://s2.loli.net/2024/05/16/rvciwNHtRWfu412.png)

![600](https://s2.loli.net/2024/05/16/6CmWol9ectgXEK2.png)

![600](https://s2.loli.net/2024/05/16/4CbaZ9StckAj8zJ.png)

![600](https://s2.loli.net/2024/05/16/2FQXR9HCvWrhlA5.png)

![600](https://s2.loli.net/2024/05/16/myKQrwDLjpiBPHC.png)

![600](https://s2.loli.net/2024/05/16/Mg9UJzsBSYxwLPe.png)

![600](https://s2.loli.net/2024/05/16/Rmc96XkvuMjZlJ4.png)

![600](https://s2.loli.net/2024/05/16/1JKGcvyAtLd8rYw.png)

![600](https://s2.loli.net/2024/05/16/xKuUogj18W3MTnE.png)

![600](https://s2.loli.net/2024/05/16/KexXAnFCl5PBUOk.png)

![600](https://s2.loli.net/2024/05/16/5vCETDjldHq9J3A.png)

![600](https://s2.loli.net/2024/05/16/gvw2jFMCTELczXn.png)

![600](https://s2.loli.net/2024/05/16/UK8uaHOGjvfxTAw.png)
## 表面模型

### translucent 模型 

![600](https://s2.loli.net/2024/05/16/g59qaPyOw7zfNtc.png)

**次表面反射**

![600](https://s2.loli.net/2024/05/16/celh71XoMOabmZD.png)

![600](https://s2.loli.net/2024/05/16/VuRAg6YH2BTkLmU.png)

![600](https://s2.loli.net/2024/05/16/4hiRFyVYG5EPSb8.png)

![600](https://s2.loli.net/2024/05/16/VKfQXtbnZ92ha6R.png)

![600](https://s2.loli.net/2024/05/16/sgtRyFnwfVmpjuY.png)


![600](https://s2.loli.net/2024/05/16/DdKmLMzA2CreupJ.png)

![600](https://s2.loli.net/2024/05/16/nVct2AY4WqLfe8P.png)

![600](https://s2.loli.net/2024/05/16/QMI394TPiulFLzp.png)

### 复杂材质

![600](https://s2.loli.net/2024/05/16/R5eQzvjrDym6SHC.png)

![600](https://s2.loli.net/2024/05/16/qFTwQnEPbi742vG.png)

![600](https://s2.loli.net/2024/05/16/qyNJSXQnT8vc6EW.png)


![600](https://s2.loli.net/2024/05/16/AbQisyfuTkdhC8Z.png)

![600](https://s2.loli.net/2024/05/16/SNd3wUVAgGfakEF.png)

![600](https://s2.loli.net/2024/05/16/2Ddq97PYTtlznBo.png)

![600](https://s2.loli.net/2024/05/16/KPouI7qc4Jk6U58.png)

![600](https://s2.loli.net/2024/05/16/NYlwq1aBXZdKFUM.png)

![600](https://s2.loli.net/2024/05/16/hALcquzO1dmCPT9.png)

![600](https://s2.loli.net/2024/05/16/XVepwoEsHgOnUa2.png)

![600](https://s2.loli.net/2024/05/16/BHPYqCd3K4N5F6b.png)

![600](https://s2.loli.net/2024/05/16/qImaJfLFRoNOgGe.png)

![600](https://s2.loli.net/2024/05/16/Uyr28WxfmJMKns5.png)

![600](https://s2.loli.net/2024/05/16/Klp8H46vu57UCoV.png)

![600](https://s2.loli.net/2024/05/16/wDyURQxPBYevtfz.png)

![600](https://s2.loli.net/2024/05/16/oUaEzGH2TkQhVNw.png)

## procedural apperance

![600](https://s2.loli.net/2024/05/16/vCoiEuRVAKbGPfM.png)

![600](https://s2.loli.net/2024/05/16/pUoN2C9QKVSI47t.png)

![600](https://s2.loli.net/2024/05/16/aIFJYu6NwO8EHTB.png)

![600](https://s2.loli.net/2024/05/16/dnROA9JZMiyYQNC.png)

