---
tags:
  - 面试
---
## 动画的分类

- 动画片段
- 动画状态机
- 动画组件
- 替身/人形动画


## Animation Clip

直接在 Animation 中进行创建

- 可以控制对于不同的组件进行变换。
- 点击 curves 来查看动画状态


**动画的复用**

- 只要存在对应的组件， 都可以进行的复用

**处理多个物体**

- 会存在一个名字 ： path ，对应子物体！！！！ 只要名字相同就可以进行复用
- **主要这就是人形动画 可以 复用的原理**
	- 主要有两个文件 ： 一个骨骼文件(不需要全部的骨骼，只需要发生变化的部分)， 一个动画片段


## Avatar

**动画复用 --- unity 解决方案 Avatar**

将A的骨骼使用 AAvatar 进行对应，B同理 得到 BAvatar

通过 Avatar 对应不同的肌肉拉伸变换


### 创建

在Model -> Rig 

- 修改 animation type
- 在 Avatar Definition 中创建

点击 confige 可以进行 Avatar 设置

- 可以设置骨骼/肌肉

**骨骼**
- 虚线：可选，实线：必选


**复用**

- 在 Animator 组件中设置对应的 Avatar 就可以复用动画

## Animator

注意 animator 组件是作为根节点，对应 animation 中的path。 --- 有层级关系 (Avatar除外！！)

**apply root motion** 使用动画的位移

**update mode** 刷新模式 (重新计算的模式 update 和 update 同步 )  
- ACT游戏可以使用 和 fixedupdate 同步
- unscaled time 
- update

**culling mode** 
- 相机没看到的时候是否执行

## 状态机

Layer ： 用于组合动画（比如上半身和下半身的动画进行混合）
Parameters ： 参数

**三种动画状态**

- 单独的动画片段
- blendtree --- 多个动画进行混合
- 另一个状态机

### 动画状态的属性

1. name
2. tag
3. motion 当前使用的 动画片段 / blend tree ---  混合树
4. Speed 动画的速度
5. multipiler : 可以绑定一个变量， 用于在代码中修改动画的速度 (具体速度 = speed * multiplier)
6. motion Time : 播放动画一个特定时间点 **范围 : 0-1** 
7. Mirror : 镜像动画 ： 只对人形有用
8. Cycle Offset ： 循环开始的偏移量 ： (没有切割， 只是开始的点不一样)
9. Foot IK ： 人形 Avatar 的脚绑定上 节点

```c#
animator.SetIKPosition(AvatarIKGoal.xx, new vector3);
animator.SetIKPositionWeight(AvatarIKGoal.xx, wight);
```

10. write Defaults!!！！！！ 对于  没有变化的属性 是否需要写入默认值 (本意是用来管理对象池内的物体 )

https://blog.csdn.net/rickshaozhiheng/article/details/77838379 : 管理池化对象

**默认值： onenbale 的时候产生的值就是默认值**

**常用方法**

`animator.GetCurrentAnimatorStateInfo([layerIndex])` 得到当前的动画状态。 通过这些状态就可以使用对应的属性

![700](https://s2.loli.net/2024/09/08/vsimJaM32UouAPK.png)


![700](https://s2.loli.net/2024/09/08/q9cxAZPRv3fV1FK.png)







可以使用 hash 值操作 参数 --- 

```c#
int xxHash = Animator.StringToHash('xxx')
animator.setFloat(xxHash, xxx);
```

## 动画状态转换

相同路径可以存在多个转换 -- solo(转换只考虑) mute(永远不考虑mute)

**has Exit time** ：

- has Exit Time 我的理解翻译过来是：**是否有一个结束的时间**
- 关闭has Exit Time：无退出等待时间，立即开启下一动画
- 开启has exit time：有退出等待时间，需等待目前动画完成到一定阶段才可切换至下一动画。
https://www.cnblogs.com/SouthBegonia/p/11748429.html

**Transistion xxx** 过度动画的时间长度， offset 是过度到的动画的位置。
**Interruption Source**： 默认None ， 能否打断当前动画/及其来源， https://blog.unity.com/technology/wait-ive-changed-my-mind-state-machine-transition-interruptions
- current Source： 可以被当前状态的转换打断 (如果ordered inpterruption 被勾选) 只有高优先级的转换才可以打断。
- next Source : 目标的状态的转换可以打断， oredered inpterruption 同理
- Current State Then Next State
- Next State then Current STate

## 混合树

使用一个或者多个参数控制 一套动画片段

## root motion

使用 动画自带的位移。具体来说就是 使用插值而不是绝对值。(使用 Animator.deltaRotation, Animator.deltaPosition)

`OnAnimatorMove` 方法会自动的控制 rootmotion 也就是自己控制插值动画。

```c#
transform.position += animator.dletaPositon; //旋转同理
```


## Generic 动画中的 Avatar 和 root motion

在 Generic 中创建 Avatar ， 并添加 Root Node

在动画片段中，Copy from other Avatar 添加对应的 Avatar

**简单来说就是，将角色根骨骼的绝对坐标和角度运用到游戏对象上**

### Root Motion 部分

https://www.bilibili.com/video/BV1fq4y1Y7Sz/?spm_id_from=333.788.top_right_bar_window_history.content.click&vd_source=8beb74be6b19124f110600d2ce0f3957

1. Root Transform Rotation (Y轴的旋转)
2. Root Transform Posotion （Y)
3. Root Transform Posotion （XZ)


**三者的设置属性都相同！！！**

Bake into pose  ： 勾选 ： 不要将**根骨骼**根节点的旋转当作 root motion 的一部分(而是普通动画！！！！) （勾选之后只有蒙皮旋转了 ， ）

> 解释 ： 对于物体的旋转分为两部分 ： 对于 Root 的旋转， 对于 Hips 的旋转。如果勾选Bake into Pose : 不希望动画带动游戏旋转的时候。

**Based Upon** 游戏对象在动画开始的时候，游戏对象的面朝方向， 可以在下方 offset 来修改。(推荐 Origin) **推荐 使用 OnAnimatorMove**

