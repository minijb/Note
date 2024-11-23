---
tags:
  - games101
---

利用中心对三角形进行采样


## antialiasing  反走样

sampling artifact -- 图形学中一切不好的东西

空间，时间采样问题 --- 信号的速度快导致采样跟不上

如何做：在采样之前进行模糊/滤波，然后进行采样 -- 不能反过来

正弦和余弦滤波 -- 好处 ：参数不同 频率不同 --- 每隔多少就重复一次

![600](https://s2.loli.net/2024/04/23/2UGY7iSl3hRVHBL.png)


傅里叶基数展开：所有周期函数都可以写成一系列正弦和余弦函数的组合

![600](https://s2.loli.net/2024/04/23/vns19Uwxd8SQcr5.png)

![7V86debvlshLBik.png](https://s2.loli.net/2024/04/23/7V86debvlshLBik.png)

![600](https://s2.loli.net/2024/04/23/isjP7rWUd5zDwZf.png)

走样的定义

![600](https://s2.loli.net/2024/04/23/8uVozKBltZ6FgWQ.png)

傅里叶变换

![600](https://s2.loli.net/2024/04/23/4xiLQ5E37jCocNg.png)

![600](https://s2.loli.net/2024/04/23/DHpEUVWIz67G43d.png)

高通滤波

边界 --- 高频信息

![600](https://s2.loli.net/2024/04/23/ZMH7YLfVEeQSrXb.png)

低通滤波

![600](https://s2.loli.net/2024/04/23/UTq4vFRZDhH59pS.png)
![600](https://s2.loli.net/2024/04/23/DibVn9vs6prtXQ7.png)

## 卷积

![600](https://s2.loli.net/2024/04/23/zl4ArBU7eCJtP5j.png)


box 越大 得到的频率越低   box 越小 得到的频率越高


**采样** ： 重复频率上的结果

原始信号 乘 冲击函数  就是采样的结果

![600](https://s2.loli.net/2024/04/24/dDmsIBEwL9Hjqle.png)

时域上的乘积就是频域上的卷积 --- 就是重复原始信号的频谱

![600](https://s2.loli.net/2024/04/24/IMG5wmfSLlv6QOZ.png)

走样：就是在搬运的过程中进行了混合

## 反走样

- 增加采样率
- 反走样 --- 先模糊再走样 --- 拿走高频信息再进行采样

![600](https://s2.loli.net/2024/04/24/eJ6qrtiDbnvj4fL.png)

## 怎么进行滤波

- 使用低通滤波器进行卷积

![600](https://s2.loli.net/2024/04/24/Q8Ovw3A6rqSd9gm.png)

### MSAA -- 进行模糊

![600](https://s2.loli.net/2024/04/24/AZrcxnGihad4UNj.png)

![600](https://s2.loli.net/2024/04/24/H3IXZKgP9ywRpDe.png)


![600](https://s2.loli.net/2024/04/24/35GfJuWqya1pkoT.png)

## 现代 的反走样

MSAA 增加了计算量

FXAA --- fast approximate AA
TAA  --- temporal AA

DLSS --- deep learning super sampling

## z-buffer

画家算法 -- 从远到近 进行绘画

![600](https://s2.loli.net/2024/04/24/vtV4pJXhU7dSrWa.png)

![600](https://s2.loli.net/2024/04/24/R3W8DAkwJlafy5r.png)

![600](https://s2.loli.net/2024/04/24/sf5WF1ZpJB4u2iD.png)

![600](https://s2.loli.net/2024/04/24/rWLZcFsadz8pQ7K.png)


![600](https://s2.loli.net/2024/04/24/Kn6lEjfIc94Xmqx.png)

