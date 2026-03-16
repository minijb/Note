---
tags:
  - games101
---

## 辐射度量学  basic radiometry --- 精确的描述光

光线的强度 I is 10。

在屋里层次准确的描述光

**New terms:**

- radiant flux
- intensity
- irradiance
- radiance

### radiant energy and flux, radiant intensity

![600](https://s2.loli.net/2024/05/07/DPhmewKM3NE2FW6.png)

![600](https://s2.loli.net/2024/05/07/EJvWjTLMpaHPxZe.png)

![600](https://s2.loli.net/2024/05/07/3e1nU4sXauF67HK.png)

![600](https://s2.loli.net/2024/05/07/TMSOEL29F8Rn4fw.png)

Radiant intensity 中 **角度** 是如何定义的

![600](https://s2.loli.net/2024/05/07/ywjsJEm2er198na.png)

**单位立体角**

![600](https://s2.loli.net/2024/05/07/PFW5pAyiZBuCgk7.png)


![600](https://s2.loli.net/2024/05/07/5bVaynzQBSkduGo.png)

![600](https://s2.loli.net/2024/05/07/PVkt9XBaHjInhvE.png)

Radiant intensity --- 就是亮度 乘 单位立体角 ---- 方向上的强度

![600](https://s2.loli.net/2024/05/07/zof4Y1b3POHQnXI.png)

![600](https://s2.loli.net/2024/05/07/QIaVRosiqEjUdBe.png)


## Radiometry cont



## summary

![600](https://s2.loli.net/2024/05/10/yjPYTf7Zi3uQM8n.png)

![600](https://s2.loli.net/2024/05/10/dHxEUt2f95u4hN8.png)


## Irradiance 

![600](https://s2.loli.net/2024/05/10/v8OANLJyYlQjIPa.png)

## Radiance 


![600](https://s2.loli.net/2024/05/10/2BgVFmiJSEMqK3c.png)

![600](https://s2.loli.net/2024/05/10/2IpZ9jiXEorvm3J.png)

两次微分: 单位立体角+单位面积

### **Irradiance与Radiance的区别**

- Irradiance是对于一个点所接受到的所有的光线
- Radiance是对于一个点面向某个方向接受到的光线

![600](https://s2.loli.net/2024/05/10/bkShr1flIMzB26a.png)

![600](https://s2.loli.net/2024/05/10/BZ7l52yicNOuAge.png)

## BRDF

![600](https://s2.loli.net/2024/05/10/BZUvPqHOWg7RofL.png)

![600](https://s2.loli.net/2024/05/10/kP137fS2HbyqvmZ.png)

![600](https://s2.loli.net/2024/05/10/GTPASsJdfBHZcEv.png)

![600](https://s2.loli.net/2024/05/10/zdTchMsIUE4eSJ9.png)

问题: 不仅仅是光源作为入射光。

![600](https://s2.loli.net/2024/05/10/42XSLFAHM1tkEuf.png)


## 实践

![600](https://s2.loli.net/2024/05/10/52NVqxRL3uQ9Ilw.png)


![600](https://s2.loli.net/2024/05/10/flA1bstV94XygPJ.png)

![600](https://s2.loli.net/2024/05/10/BUKqHngJW7sYcwV.png)

![600](https://s2.loli.net/2024/05/10/2GIFSMmQVcbks1o.png)

![600](https://s2.loli.net/2024/05/10/klwCX6UbK1OS3IR.png)

![600](https://s2.loli.net/2024/05/10/Lz9amFChbg8Sik3.png)

![600](https://s2.loli.net/2024/05/10/JzpufPmgLlRjOVw.png)

**全局光照**

按照光栅化角度来看

![600](https://s2.loli.net/2024/05/10/W4MOqk5VIoRnbhi.png)

![600](https://s2.loli.net/2024/05/10/QDbzewmGnYtsKN2.png)


![600](https://s2.loli.net/2024/05/10/FEvrfRhZ5oy8OLT.png)

![600](https://s2.loli.net/2024/05/10/tIh3VkespUQ4a6K.png)

![600](https://s2.loli.net/2024/05/10/wFWkBPo4eXq23MR.png)

![600](https://s2.loli.net/2024/05/10/PNRVEvMZ9x4Qdm6.png)

## 怎么解全局光照

### 概率论

![600](https://s2.loli.net/2024/05/10/GgAacE5CWlpb2hN.png)

![600](https://s2.loli.net/2024/05/10/Hgq1UuFXCimnLPM.png)

![600](https://s2.loli.net/2024/05/10/5MjUgqJNs3ETS1Z.png)

![600](https://s2.loli.net/2024/05/10/Ioh5HqKgjuMWB1s.png)

![600](https://s2.loli.net/2024/05/10/f6TB9wjpldDAMCP.png)

## Monte carlo integration 蒙特卡洛积分

![600](https://s2.loli.net/2024/05/10/6gICBETaSViLRrK.png)


![600](https://s2.loli.net/2024/05/10/4d31z2v6NSLekB8.png)

![600](https://s2.loli.net/2024/05/10/ldfSQhoIv2FbuLy.png)

![600](https://s2.loli.net/2024/05/10/JHtNKROlUIAs4fG.png)


![600](https://s2.loli.net/2024/05/10/9IgNCH6dQuUzA3p.png)

![600](https://s2.loli.net/2024/05/10/7raG5jC1f6mQcNF.png)

## path tracing

![600](https://s2.loli.net/2024/05/10/GzmQPAOFV74TKyN.png)

不同的材质

![600](https://s2.loli.net/2024/05/10/HMo8UnNtDA37Wuc.png)


![600](https://s2.loli.net/2024/05/10/4RnQcIazh8wLXVK.png)

> the cornell box


![600](https://s2.loli.net/2024/05/10/ltX67g8AydFbSPs.png)


![600](https://s2.loli.net/2024/05/10/byjuporzJRCwhPH.png)


![600](https://s2.loli.net/2024/05/10/YAyuP51cmIWtqfF.png)



![600](https://s2.loli.net/2024/05/10/cdD4maJqIA3z6Mr.png)

![600](https://s2.loli.net/2024/05/10/MLm1AKSon8uNaiF.png)

**只考虑直接光照**

![600](https://s2.loli.net/2024/05/10/RLi29D6tBqJu4AV.png)


**考虑间接光照**

![600](https://s2.loli.net/2024/05/20/l5oSPyrOiQdhTWq.png)

![600](https://s2.loli.net/2024/05/10/RPOt5XxNJaryWih.png)


**问题** ：光线数量过多。

![600](https://s2.loli.net/2024/05/10/Gn7z3qla9BRUmLb.png)

![600](https://s2.loli.net/2024/05/10/2jKOxTvY57WAZBn.png)

![600](https://s2.loli.net/2024/05/10/vW9ZNdSjGRYaIs8.png)

**什么时候停**

![600](https://s2.loli.net/2024/05/10/Cn5gAvfW9byjmBV.png)

**使用 RR  Russian Roulete**

![600](https://s2.loli.net/2024/05/10/IXtm4o23A5WiQR8.png)

![600](https://s2.loli.net/2024/05/10/pRtf7U1cxydC4PT.png)

![600](https://s2.loli.net/2024/05/10/TFa3IvlVeG6b4cR.png)

### 小问题

 
![nco29YpsAlw7azP.png](https://s2.loli.net/2024/05/10/nco29YpsAlw7azP.png)

![600](https://s2.loli.net/2024/05/10/4qhuJQpVMFc1Ivd.png)

很多光线浪费了

![600](https://s2.loli.net/2024/05/10/dWwACqceB9y5lTb.png)

![600](https://s2.loli.net/2024/05/10/5PcBkzD23ngqylo.png)


![600](https://s2.loli.net/2024/05/10/DIFNY9boqjg1Pzk.png)


**重要：将之前的拆成两部分 **

- 光源和非光源

![600](https://s2.loli.net/2024/05/10/z8cLVXNuU5Sa7Wf.png)

![600](https://s2.loli.net/2024/05/10/aLSJH5ouC78yXKc.png)


## 还有一个问题

![600](https://s2.loli.net/2024/05/10/3GsHLy5WgRO9diD.png)


## 细节

![600](https://s2.loli.net/2024/05/10/A1iFzQw7kMcYe9N.png)

![600](https://s2.loli.net/2024/05/10/Do2ubIF7UGrgaJe.png)

![600](https://s2.loli.net/2024/05/10/3r6AlpJf15QzvET.png)

![600](https://s2.loli.net/2024/05/10/lTybJWfDdLj4wRF.png)

