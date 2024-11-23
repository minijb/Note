---
tags:
  - games101
---
## imageing = synthesis + capture

![400](https://s2.loli.net/2024/05/22/3A6qYtCbgf5x7aI.png)


传感器记录 irradiance

![600](https://s2.loli.net/2024/05/22/KfGeaHUcpSJtTx8.png)


### fov 

![600](https://s2.loli.net/2024/05/22/FUesSV5ObokG3Kv.png)

![600](https://s2.loli.net/2024/05/22/3DLvsrwbENzHUtp.png)

![600](https://s2.loli.net/2024/05/22/U945TICqekiNYx1.png)

![600](https://s2.loli.net/2024/05/22/LjpQrhiNA7fw6gz.png)

### exposure

![600](https://s2.loli.net/2024/05/22/9Awj7HlCNar4LKy.png)

光圈 : aperture

曝光控制

- 光圈大小
- 快门 --- 速度
- ISO gain 感光度 --- 后期处理

![600](https://s2.loli.net/2024/05/22/KDiobFZYv8TkIfL.png)


ISO --- 可以放大光，但是也会放大噪声

![600](https://s2.loli.net/2024/05/22/9C6EPjQOMqmt5kf.png)


光圈: N 直径的逆

![600](https://s2.loli.net/2024/05/22/8WChRN1JnFYB2Ub.png)

![600](https://s2.loli.net/2024/05/22/xIavCg6hMybmJXd.png)

![600](https://s2.loli.net/2024/05/22/qbL6A3T29fFKOrR.png)

![600](https://s2.loli.net/2024/05/22/j9YmbGBHncfMSdT.png)

![600](https://s2.loli.net/2024/05/22/MjWcPxvoZDtV5mL.png)

景深。

![600](https://s2.loli.net/2024/05/22/F6ZexmRrMUndjIg.png)

![600](https://s2.loli.net/2024/05/22/PXk8j7iRGWmYuAn.png)

## the lens appreximation

![600](https://s2.loli.net/2024/05/22/pY3xULG5zEHP1WA.png)

![600](https://s2.loli.net/2024/05/22/AgrVdzfhKQ9yZea.png)

![600](https://s2.loli.net/2024/05/22/C5T2DSNPIEWydZs.png)


$z_{i}$ 像距 $z_{o}$ 物距

![600](https://s2.loli.net/2024/05/22/v3iASZ5anx2zKUk.png)


![600](https://s2.loli.net/2024/05/22/zdsobfQl2WE5AGa.png)


## 景深

Coc size 

![600](https://s2.loli.net/2024/05/22/1Ui5NrXavnMGZDj.png)

![600](https://s2.loli.net/2024/05/22/cjRtyBeNXJrDxQS.png)

![600](https://s2.loli.net/2024/05/22/tXDIveVN3QcpBrH.png)

![600](https://s2.loli.net/2024/05/22/s9nDh8OlAJ3rM1N.png)


![600](https://s2.loli.net/2024/05/22/tbTNJSxMvqu3agz.png)

![600](https://s2.loli.net/2024/05/22/rDOiAmJBVa1LjwM.png)

![600](https://s2.loli.net/2024/05/22/v2zERkdhw5bBPyX.png)

![600](https://s2.loli.net/2024/05/22/jZ5GrtDxb9gP78w.png)

![600](https://s2.loli.net/2024/05/22/P67N1njHrabJhAp.png)

![600](https://s2.loli.net/2024/05/22/xbDECFsgOzcvdtK.png)

![600](https://s2.loli.net/2024/05/22/onERtdXVy3TjM7u.png)


## 光场

![600](https://s2.loli.net/2024/05/23/TjGh1QZknR2Dm3E.png)


![600](https://s2.loli.net/2024/05/23/Eq6aFK3OlB58jCk.png)

![600](https://s2.loli.net/2024/05/23/DsL1bBwukZt7rep.png)


![600](https://s2.loli.net/2024/05/23/SQyHmDcP3C1zrj4.png)

![600](https://s2.loli.net/2024/05/23/lWcaCLg3N1fAFOd.png)

![600](https://s2.loli.net/2024/05/23/BLmfOwjHtG3bF7i.png)


定义光线

![600](https://s2.loli.net/2024/05/23/pa9qUPIGDHAeiVO.png)

![600](https://s2.loli.net/2024/05/23/L2hRiKJWeYsIzDG.png)


此时 我们使用 4个值就可以表示光线 

![600](https://s2.loli.net/2024/05/23/MqopGirPEncQLYf.png)



![600](https://s2.loli.net/2024/05/23/eCmIdj6BKtMgGnD.png)


![600](https://s2.loli.net/2024/05/23/hokSdJVuKLNAzWP.png)

不需要知道黑盒内部的东西。

此时我们就可以使用两个平面来表示广场并使用 uv定位

![600](https://s2.loli.net/2024/05/23/Byi683VNs2vDJrK.png)


![600](https://s2.loli.net/2024/05/23/RvGzk5tMDydpHh2.png)

![600](https://s2.loli.net/2024/05/23/jsygN9HXWFqS6l1.png)

![600](https://s2.loli.net/2024/05/23/aEhxupqfYFkQMV6.png)

记录的不是radiance，而是每一种颜色的值

### light field camera

![600](https://s2.loli.net/2024/05/23/sVXZyYvfiEgHQ5n.png)

![600](https://s2.loli.net/2024/05/23/RW5nwzTkJpFdoCH.png)

![600](https://s2.loli.net/2024/05/23/pkixoIdOZTSNDM4.png)

![600](https://s2.loli.net/2024/05/23/S46yPkJCRx2vA3c.png)

## 颜色

![600](https://s2.loli.net/2024/05/23/Xt25dNVmqSC47WD.png)

![600](https://s2.loli.net/2024/05/23/FETBRIcsQZdhv51.png)

## color

![600](https://s2.loli.net/2024/05/23/ys21Q7xFI8Kilrn.png)

![600](https://s2.loli.net/2024/05/23/6VID24o9f8dFwvG.png)


![600](https://s2.loli.net/2024/05/23/xcywLQbs2iDfGFP.png)

### 同色异普

![600](https://s2.loli.net/2024/05/23/I4OJSTsX2VH7DvM.png)

![600](https://s2.loli.net/2024/05/23/ql5BYgoH3bP7S8V.png)

![600](https://s2.loli.net/2024/05/23/ILlaExJ91pTOKMZ.png)

![600](https://s2.loli.net/2024/05/23/4LDMEYFOmKZAbh6.png)

![600](https://s2.loli.net/2024/05/23/Oye54Y2LXqfM7rv.png)

![600](https://s2.loli.net/2024/05/23/KGiPLBFdtmYNaCq.png)

![600](https://s2.loli.net/2024/05/23/PMepL5l9JtnRAvK.png)

![600](https://s2.loli.net/2024/05/23/f9AhwspKbj2JXQY.png)


## 颜色空间

![600](https://s2.loli.net/2024/05/23/txvbicH9kF5uP8Q.png)

![600](https://s2.loli.net/2024/05/23/VcorTxA4vnLhGdf.png)

![600](https://s2.loli.net/2024/05/23/NuSPwgYMsDXz6Jx.png)


![600](https://s2.loli.net/2024/05/23/xgVDiWBLAMnj7y5.png)

![600](https://s2.loli.net/2024/05/23/Rk5HwWK3AaEzZCB.png)

![600](https://s2.loli.net/2024/05/23/f12DroXs8VWuESY.png)

![600](https://s2.loli.net/2024/05/23/wvTq7jzyL6dpOi9.png)

![600](https://s2.loli.net/2024/05/23/cpsik7Xt46FvGzQ.png)

![600](https://s2.loli.net/2024/05/23/6RGLxNipEfWMhI4.png)

