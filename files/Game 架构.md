
## MVC

用户 -> UI <-> Data

model : 模型
view : 视图
controller ： view 和 model 之间交互

用于 业务逻辑(controller) 数据(model) view(界面) 分离

![500](https://s2.loli.net/2024/06/10/QA89NSGwFog3MDi.png)

**流程**

view 触发时间 -> controller 处理事务乘除法数据更新 -> 更新 Model 数据 -> Model 写回到 View -> view 更新数据

**主要用于 UI 系统**

- Model -- 数据支撑 ： 只需要注意数据的准确性 
	- 提供游戏存储和持久化数据
- View  -- 考虑如何展示数据
- Controller -- 中转，事件控制。

一个经典的框架 :


![600](https://s2.loli.net/2024/06/10/zyP9mkMWYp4s2BD.png)



**数据实体化** : 将 animation 存储在一个 ScriptObecjt 中，并存储hash数据



## MVP

- View只处理视图相关，不做任何逻辑处理
- Model的工作就是完成对数据的操纵，数据的获取、存储、数据状态变化都是model层的任务，如网络请求，持久化数据增删改查等任务
- Presenter作为桥梁

![3yf61ivaJGwKS2r.png](https://s2.loli.net/2024/06/11/3yf61ivaJGwKS2r.png)
## MVVM

1.使用ViewModel替代了Presenter。
2.原本P和V一对一的关系现在变为VM-V一对多的关系。

VM在一定程度上能够重用，就表示M层在一定程度上也可以复用了

![WmVcR2YIJpXa3Kl.png](https://s2.loli.net/2024/06/11/WmVcR2YIJpXa3Kl.png)




https://cloud.tencent.com/developer/article/1662265
https://www.bilibili.com/video/BV1FW421c7je/?spm_id_from=333.788&vd_source=8beb74be6b19124f110600d2ce0f3957
[MVC youtube obserableList](https://www.youtube.com/watch?v=v2c589RaiwY)
[ScriptObject](https://blog.csdn.net/qq_46044366/article/details/124310241)
[Event Bus ](https://blog.csdn.net/klscer/article/details/122692379)
https://zhuanlan.zhihu.com/p/498576422