---
tags:
  - 面试
---

## 四元数

用于表示旋转

### 1. 优点

1. 避免万向锁
2. 只需要一个四维的四元数可以执行绕任意原点的向量的旋转
3. 可以提供平滑的插值

### 2. 欧拉角

绕 xyz 三个轴的旋转角度

#### 2.1 静态

绕世界坐标系三个轴的旋转

#### 2.2 动态

绕物体坐标系三个轴的旋转。

unity 3D 欧拉角的旋转顺序（父子关系) y - x - z


## unity 生命周期

Awake 脚本创建时调用
OnEnable ： 可用或激活状态调用
Start ： Update 第一次执行前调用
Update ： 每帧调用
FixedUpdate ： 固定物理时间间隔调用
LateUpdate ： 每帧 Update 结束后调用 。常用于处理场景和状态，以及相机
OnGUI ： 处理 OnGUI 时间
OnDisable ： 当前物体不可用或者非激活时调用
OnDestory ： 在对象被摧毁时调用

## unity 协程

实现原理时迭代器， 

yield return 会将程序挂起。 在return 之前 和普通方法一样。  走的是单线程。

挂起之后，在 update 之后， lateupdate之前 运行。 
**enable 对协程是没有影响的。。但是 如果 setactivate(false) 则 已经启动的协程完全停止了** 


## rectTransform 和 transform

recttransform 可以 强转 transform 反之不行。

**锚点： ** 为 当前物体在父物体中的位置 0-1
确定了父物体改变的时候子物体的大小和位置

**anchoredPostion** 忽略z坐标。一般使用 anchoredPostion3D 进行设置

https://blog.csdn.net/ChinarCSDN/article/details/86729600

Position ： 

在UGUI中Pos X与Pos Y分别表示UI**轴心点**到**锚点**的水平与方向距离。  
Position值的显示只和UI自身**锚点**及**轴心点**的位置有关系。

![r6w3NfgIysJ8zHk.png](https://s2.loli.net/2024/08/18/r6w3NfgIysJ8zHk.png)

![49e3P1YJN2SwoBW.png](https://s2.loli.net/2024/08/18/49e3P1YJN2SwoBW.png)

![Vr7v9YhPHK2XCUW.png](https://s2.loli.net/2024/08/18/Vr7v9YhPHK2XCUW.png)
### 1. api


换句话就是轴心点与锚点的向量，即UI坐标。 它根据AnchorMin和AnchorMax是否重合要分别计算。

![WRiduBq4ETepVAz.png](https://s2.loli.net/2024/08/18/WRiduBq4ETepVAz.png)

anchoredPosition3D —— UI坐标系的3D坐标

offsetMax、offsetMin —— 偏移量

## collider and trigger

碰撞体 有碰撞效果 ，isTrigger = false  可以调用给 OnCollisionEnter/Stay/Exit -- 对应三个阶段
触发器 没有碰撞跳过 isTrigger = true  可以调用 OnTrggerEnter/Stay/Exit

**物体发生碰撞的必要条件：**

1. 必须带有 collider ， rigidbody 或者 人物控制器
2. 另一个必须带有 Collider 

**characterController 和 rigidbody 区别**

characterController 是受到限制的 righidbody

**发生碰撞的时候， 几种释放压力的方式**

`rigidbody.AddForce/AddForceAtPosition`  

## 光源的类别

`DirectionalLight, PointLight, SpotLight, AreaLight`

平行，点，聚光灯，区域
## FixedUpdate

通常用于物理更新，  `Maximum.Allowed.Timestep` 限制了帧率下降时物理计算和 fixedUpdate 事件可以使用的时间。

## 相机移动放在哪个函数

LateUpdate 

## 对象池

用于存放反复调用的资源的一个空间， 常用于 敌人，子弹，以及重复的对象

## MeshRender 中的 material 和 sharedMaterial 的区别

修改 sharedMaterial  所有使用这个材质的物体都会改变， 并且改变存储在 project 中的材质设置 (牵一发动全身)。**不推荐修改 sharedMaterial 返回的材质**

如果希望修改渲染器的材质，使用 material代替

*************

**主要区别**

1. material属性指向的是一个实例化的材质对象。当你通过renderer.material获取或设置材质时，Unity会创建该材质的一个副本，并将其应用于当前的MeshRenderer。这意味着，**对于同一个MeshRenderer，如果多次获取其material属性，你将得到多个不同的材质实例。**
2. `sharedMaterial`属性指向的是材质的一个共享实例。多个`MeshRenderer`可以共享同一个`sharedMaterial`实例，这有助于减少内存使用和提高性能。

**修改影响**

1. 修改通过`material`属性获取的材质的属性（如颜色、贴图等）只会影响当前的`MeshRenderer`，不会影响其他使用相同材质的`MeshRenderer`。因为每次通过`material`获取的都是材质的副本。
2. 修改sharedMaterial的属性会影响所有共享该材质的MeshRenderer。但是，直接修改sharedMaterial可能会导致意外的结果，因为其他MeshRenderer也可能正在使用该材质。因此，在修改sharedMaterial之前，通常建议先获取一个材质的副本进行修改，然后再决定是否将更改应用回sharedMaterial。



## TCP/IP 各个层次及功能

**网络接口层** ：  完成数据帧的实际发送和接收  ( 对应 物理层 和 数据链路层)
**网络层** : 处理分组在网络中的活动， 例如 路由选择和转发， **协议** ：IP ARP 
**传输层** ： 程序之间的通信  协议 ： TCP/UDP 
**应用层** ： 处理特定引用之间的 传输， FTP协议 SMTP http 等


## GPU 工作原理

1. 顶点处理
2. 光栅化计算
3. 纹理贴图
4. 像素处理
5. 输出

## 渲染管道

1. 本地坐标
2. 视图坐标
3. 背面裁剪
4. 光照
5. 裁剪
6. 投影
7. 视图变换
8. 光栅化

## 优化内存

1. 压缩自带类库
2. 不用的隐藏起来 而不是 destory
3. 释放 assetBundle 占用的资源
4. 降低模型面数，骨骼数，贴图大小
5. 使用光照贴图，使用LOD， 使用着色器，使用Prefeb

## 动态加载资源

1. Resource
2. AssetBundle

## 旋转函数

Transform.Rotate()

## 动画分类及原理

1. 单一网格动画 ： 关键帧动画 
2. 关节动画 ： 将角色分为若干独立部分，一个部分对应一个网格模型，部分的动画连接一个整体的动画
3. 骨骼动画 ： 结合两者的优点，谷歌按角色特点组成一定的层次结构。有关节相连，可做相对运动，皮肤作为单一网格蒙在谷歌外。

## LOD

多层次细节。按照模型的位置/重要程度决定物体渲染的资源分配，降低非重要物体的面数和细节度，从而获得高效率的渲染运算。


## MipMap 

加快渲染进度，减少图像锯齿。贴图被处理成一系列被云翔计算和优化过的图片组成的文件。

## .Net Mono

Mono 是 .Net 一个开源跨平台工具，类似于java虚拟机。

## Unity3D 协程

yield return + xxx

- WaitForSeconds 受到 timeScale 影响， 等待 x s
- WaitForSecondsRealTime 不受 timeScale 影响
- WaitForEndOfFrame : 这一帧所有代码完成后执行
- WaitForFixedUpdate ： fixedUpdate 完成后执行
- null/0 ： Update 完成后执行

## image and rawimage

- image 更加消耗性能
- image 只能使用 sprite 图片， 但是 Rawimage 各种形式都可以
- image 适合放有操作的图片如 裁剪拼图旋转等，
- rawimage 适合放单独展示的图片

## 矩阵相乘的注意点

注意蠕变：误差累积

## 细小高速物体撞向较大物体

穿透，碰撞检测失败

## 动态合批 静态合批

动态合批 ： 如果动态物体共用相同材质，那么Unity会自动对物体进行批处理。
区别：
- 动态是自动的，而且物体时可以移动的，但是限制较多
- 静态批处理：自由度高，限制少，但是占用更多内存，静态批处理后的所有物体都不可以移动

**静态合批采用了以空间换时间的策略来提升渲染效率**。

静态合批**并不减少Draw call的数量**，但是由于我们预先把所有的子模型的顶点变换到了世界空间下，并且这些子模型共享材质，所以在**多次Draw call调用之间并没有渲染状态的切换**，**渲染API会缓存绘制命令，起到了渲染优化的目的**。另外，**在运行时所有的顶点位置处理不再需要进行计算，节约了计算资源**。

**静态合批采用了以空间换时间的策略来提升渲染效率**。

静态合批**并不减少Draw call的数量**，但是由于我们预先把所有的子模型的顶点变换到了世界空间下，并且这些子模型共享材质，所以在**多次Draw call调用之间并没有渲染状态的切换**，**渲染API会缓存绘制命令，起到了渲染优化的目的**。另外，**在运行时所有的顶点位置处理不再需要进行计算，节约了计算资源**。

## LightMap

将场景各个表面的光照输出到贴图上，最后通过引擎贴到场景上

## 射线检测

一个点像一个方向发射无终点的想，发射轨迹中与其他物体发生碰撞后停止。

## 客户端和服务的交互方式

socket --- TCP/UDP协议
http 协议 post get 

## Clipping Planes 的作用，

裁剪平面，用于表示相机开始渲染到中止渲染之间的距离

## 查看常见的 drawcall, 如何降低

- Game 视图 右上角 的 State
- drawcall， batching， unity 内置的 剔除

## 移动设备上优化i资源的方法


1. 使用 assetbundle 实现资源的分离和共享
2. 降低顶点数，到 8 万以下
3. 只是用一盏动态光，不适用阴影， 不适用光照探头
4. 粒子系统注意
5. 裁剪粒子系统
6. 合并同时出现的粒子系统
7. animator 出视野不更新
8. 删除无意义的 animator
9. 除了主角不适用 骨骼运动
10. 绝对禁止使用不带刚体带包围盒的物体 static collider 运动
11. 每帧递归的计算 finalalpha 改为只有初始化和变动计算
12. 去除发现计算
13. 不要每帧计算 viewSize 和 windowSize
14. fill draw call 时构建顶点缓存使用 array.copy
15. 少使用smooth group


## camera 组件的 clearFlags  选为 Depth only

仅深度， 用于对象不被裁剪


## gameobject 设置为 static

当被今天物体挡住不可见的时候， 将会被剔除/禁用网格对象。

## 如何保证 A组 比 B组 先渲染

A 组的渲染队列 小于 B 组

## 水面倒影 

对睡眠贴图纹理巾扰动，产生波光粼粼的感觉。 可以通过 shader 实现像素级的扰动， 顶点少，速度快

## 跨平台

通过Mono 虚拟机实现。

之后通过 IL2CPP ， 把原本mono的转化为 cpp代码，利用c的跨平台特性。

## 网络

### 1. 状态同步

只同步状态： 计算在服务器进行，结果下发给客户端。客户端根据得到的数据驱动显示即可。

**缺点**

1. 流量大
2. 响应速度较慢 --- 因为服务器需要计算
3. 容易出现拉扯现象 ： 角色突然出现在某个位置，物探死亡。
	- 原因： 网络波动，数据未能及时下放

**场景**

1. 实时性要求不高
2. 交互简单
3. MMO

### 2. 帧同步

只同步命令，客户端自己计算结果。**优点** 流量小，适用于高频互动游戏。

缺点：
1. 无法保证计算的一致性。

**注意事项**

1. 不使用浮点数，使用整数
2. 不同客户端之间保证频率一致
3. 随机种子相同
4. 使用排序同期，保证遍历顺序
5. 逻辑和显示需要分离
6. 使用补间过度，调整速率，掩盖卡顿

**优化**

1. 每次广播的数据要足够小
2. 推荐提前广播，采用时钟同步
3. 客户端逻辑先行，通过平滑追赶的方式处理。

使用UDP。因为UDP对于 RTT 不受影响

## drawcall， batch， setpasscall

drawcall ： CPU 通知 GPU 进行渲染的命令

Batch ： 渲染批次 合并渲染操作，减少Drawcall

渲染 Pass ： 渲染pass的数量， 每一个 pass 都需要 Unity 运行时绑定一个新的着色器


- 内置渲染管线 ： 所有材质球的渲染pass的数量
- URP ： 5个材质球， shader 和关键字都一样， shader 有两个通过， 值就是2.


## 批处理

### 1. 静态批处理

静态合批是Unity的一种优化技术, 本质是将`相同材质`并且`始终不动`的的`Mesh合并`成为一个大Mesh
然后由`CPU合并`为一个批次发送给GPU处理,从而减少DrawCall带来的消耗.


静态批处理的工作原理是将静态游戏对象转换为世界空间，并为它们建立一个共享的顶点和索引缓冲区。 在后续的绘制过程中，根据Unity引擎渲染排序函数，将符合静态合批的对象，一次性提交整个合并模型的顶点数据，然后设置一次渲染状态，调用多次Draw call分别绘制每一个子模型 , 而多次 Draw call 调用之间并没有渲染状态的切换

**为什么会增加包体呢？** 答： 因为在Build项目的时候，Unity会把符合静态合批的对象生成一个大的合并网格，这个多出来的网格会导致包体增加

**为什么会增加运行时内存呢？** 答： 渲染一个对象，CPU会从硬盘拿到渲染这个物体的数据（网格，材质，贴图等）加载到内存中，然后传送到显存中，渲染完成后，自动删除这部分内存。渲染合批的对象时，因为是直接加载Build的时候生成的合并后的大的Mesh，所以运行时的内存就增加了。合并后的网格越大，则运行时增加的内存就越大

Unity还提供了一种灵活度很高的运行时静态合批方法我们可以在运行时调用StaticBatchingUtility.Combine实现将一些模型合并成一个完整模型。使用这种方法我们可以避免最终打包的应用体积增大，但是由于在运行时通过CPU做模型的合并，会到来一次性的运行时内存和CPU开销


限制 ： 最多可以合并 64000 个顶点

### 2. 动态合批

与静态拿批不同,动态合批是的物体是可以运动的,但是需要符合Unity内部执行的步骤,我们需要其规则去开发.

**规则**
1. 限制相关
2. 不同 Mesh 网格之间的合批
3. 单个网格最多支持 225个顶点

**限制**

1): 拿批Mesh点数不超过225
2): 不同Mesh相同材质可以合批
3): 相同材质复制出来的材质实例不能合批(修改实例中材质参数会自动创建材质实例)
4): 照片贴图材质必须使用相同光照贴图位置
5): 采用具有多个Pass的Shader将无法合批
6): 合批成功的对像只受一个光照影响
7): 延迟渲染不支持动态合批操作
8): 收集合批信息将加大CPU负担


**缺点**：
1. 会带来CPU性能消耗。它与静态批处理带来性能优化不一样，动态批处理是将多个对象通过一个Draw Call来渲染。那么就需要在渲染之前，将这些小模型的顶点从本地坐标系转换成[世界坐标系](https://zhida.zhihu.com/search?q=%E4%B8%96%E7%95%8C%E5%9D%90%E6%A0%87%E7%B3%BB&zhida_source=entity&is_preview=1)，模型顶点变换的操作是由CPU完成的，所以这会带来CPU的性能消耗。计算的模型顶点数量不宜太多，否则CPU串行计算耗费的时间太长会造成场景渲染卡顿。
2. 动态批处理有很多严格的限制条件，具体可以参考官网，这里就不一一列举

### 3. GPU Instancing

针对 GPU 的优化

**注意** ： 静态的优先级比 GPU Instancing 高，两者都有默认 静态批处理

**合并批次的前提条件是同网格同材质，但材质的参数可以不同，然后基于一个Instanced Draw Call，一次性绘制多个模型。**

其本质是使用一个DrawCall渲染多个相同材质的网格对像.  
从而减少CPU和GPU的开销.比较适合场景中大量重复的物体如树木和草地等.

1.会合并使用相同材质和Mesh的对象
2.材质需要支持GPU Instancing,例如默认标准材质就有
3.Tranform信息需要有所不同,(完全重合了渲染出来也没有意义)
4.未使用SRP Batcher,如有会优先使用SRP Batcher.(在URP渲染管线中是默认开启的)
5.粒子对像不能合批
6.使用MaterialPropertyBlocks的游戏不能合批
7.Shader必须是使用compatible的

1. 不需要静态，
2. 不会增加内存的使用

GPU实例化让你可以非常高效地绘制相同的网格几次。Unity通过向GPU传递转一个Transform列表来做到这一点。毕竟，每块GameObject都有自己的位置，旋转和缩放。

但是，创建Transform列表会降低性能。如果在游戏过程中没有物体移动/旋转/缩放，则只需支付一次此开销。但是，如果对象每帧都更改一次，则需要每帧支付一次开销，这一点需要特别注意。所以如果需要在Update修改物体的位置，旋转和缩放就不要使用GPU Instancing。

**和 static batching 之间的区别** ：

1. 静态批处理：不需要网格相同， GPU Instance 必须网格相关 



### 4. SRP Batcher

SRP Batcher是Unity提供的一种渲染优化技术，它可以将多个网格合并成单个批次进行渲染，从而提高性能。  
与其他合批不同,SRP Batcher将未改变属性的Mesh缓存起来,从而减少消耗


在标准的渲染流程下,CPU需要收集所有场景物体的参数,场景中的材质越多CPU提交给GPU的数据就越多.  
而在SRP中流程下GPU拥有数据管理的"生命权",管理大量不同材质但Shader变动较小的的内容  
让数据在GPU中持久存在,从而减少消耗.

1. 把调用draw call前，一大堆CPU的设置工作给一口气处理了，增加了效率。
2. 把材质的属性数据直接永久放入到显卡的CBUFFER里，那只要数据不变，CPU就可以.不需要把这些数据重新做设置工作。节省了CPU调用，增加了效率。
3. 用专用的代码将引擎的属性（比如objects transform）直接放入到GPU显存，这个专用的代码是不是更快更强呢，官方是这样么说的，用的词语是quickly，就是快。
4. SRP Batcher并没有减少drawcalls，而仅仅是提高了效率。相当于一个人减肥了，减去了多余的脂肪和水分，但是器官结构啥的一个没少。总之就是有用。

没有减少 drawcall ， 但是 减少的 CPU 消耗

**条件**

1. 物体必须时一个 mesh / skinned mesh
2. shader 必须兼容
3. 必须声明所有内建引擎properties 在一个名为"UnityPerDraw"的CBUFFER里。

### 5. 总结

|            | Static Batching | Dynamic Batching  | GPU Instancing | SRP Batching     |
| ---------- | --------------- | ----------------- | -------------- | ---------------- |
| 原理         | 离线合并网格          | 运行时合并网格           | 切换矩阵变换渲染相同物体   | 使用大块常量缓冲区避免切换上下文 |
| 目的         | 降低SetPass calls | 降低Drawcall        | 降低Drawcall     | 降低SetPass calls  |
| 优点         | 限制少             | 自动                | 性能极好           | 相同Shader不同材质加速   |
| 缺点         | 加大包体,加大内容,要求同材质 | 加大CPU消耗,对顶点与材质有要求 | 要求相同物体         | 只能用于SRP          |
| 要求相同Mesh   | 否               | 否                 | 是              | 否                |
| 要求相同材质     | 是               | 是                 | 是              | 否                |
| 要求相同Shader | 是               | 是                 | 是              | 是                |
| 要求Shader兼容 | 否               | 否                 | 是              | 是                |
| 适用情形       | 静态场景            | 小物体,特效,UI动态       | 大量相同物体         | 较为广泛,特效和蒙皮网格除外   |
## set pass call

https://zhuanlan.zhihu.com/p/353856280
https://zhuanlan.zhihu.com/p/76562300

渲染流程 :

![1000](https://pic1.zhimg.com/v2-d748d8d908d4dfb2baa84b7cf2fa9dfa_r.jpg)

**drawcall** : 渲染命令
**batches**  一个batch 至少包含一个 drawcall (消耗时间的点： **上传物体的数据到乡村，并设置渲染状态**)
**setpasscall** ： 每个 pass 都需要 unity 在运行的时候绑定一个新的着色器，简单来说就是切换渲染状态




## GPU 工作原理

1. 顶点计算
2. 光栅化处理
	- 显示器由像素组成， 通过算法生成的图形上的点通过一定的算法转化到对应的像素点。
3. 纹理贴图
4. 像素处理
5. 输出

## 渲染管道

见到那来说就是将从一个坐标系中变化到另一个

主要步骤

**本地坐标** -> **视图坐标** -> **背面裁剪** -> **光照** -> **裁剪** -> **投影**  -> **视图变换** -> **光栅化**


## 常用坐标变换

**shader**

- WorldToClipPos
- ViewToClipPos
- ObjectToViewPos
- WorldToViewPos
- ObjectToWorldDir
- WorldToObjectDir
- ObjectToWorldNormal

**C#**

ScreenToViewportPoint  屏幕转视口
ScreenToWorldPoint      屏幕转世界
ViewportToScreenPoint  视口转屏幕
ViewportToWorldPoint    视口转世界
WorldToScreenPoint       世界转屏幕
WorldToViewportPoint     世界转视口

**鼠标发射射线**
Ray ray= Camera.main,ScreenPointToRay(Input.mousePosition);


**屏幕坐标转世界坐标**
关于ScreenToWorldPoint的使用说明：
1：如果是2D，Camera.main.ScreenToWorldPoint（Input.mousePosition），那么转换后的坐标，直接用没有问题，原因是2D的Z轴默认是0，所以转后没有问题

2：如果是3D，Camera.main.ScreenToWorldPoint（Input.mousePosition），那么转换后的坐标是不正确的，因为此时的摄像机是投影摄像机，n多个面，所以必须指定要转换哪个面上的坐标，即z距离所对应的面：Camera.main.ScreenToWorldPoint(new Vector3(Input.mousePosition.x, Input.mousePosition.y, transform.position.z))，这样转换后的坐标才是正确的！

## UI 自动适应屏幕分辨率

Canvas Scaler

1.恒定像素模式（Constant Pixel Size）
无论屏幕大小如何，UI 元素都保持相同的像素大小。

2.根据屏幕缩放（Scale With Screen Size）
即：屏幕越大，UI 元素越大。

3.恒定物理尺寸（Constant Physical Size）
UI 元素无论屏幕大小和分辨率如何都保持相同的物理大小。

比较常用的是根据屏幕缩放（Scale With Screen Size），它有三种模式：


## Canvas 三种渲染模式

https://blog.csdn.net/qq_15020543/article/details/82594332
https://www.yuque.com/chengxuyuanchangfeng/qxodkp/dnolr5y57fiaifo9

**Overlay** 
画布会填满整个屏幕空间，并将画布下面的所有的UI元素置于屏幕的最上层，或者说画布的画面永远“覆盖”其他普通的3D画面
**空间z轴对于前后位置对于元素不起作用， 而是使用 sort order**

**Screen Camera**

渲染需要绑定对应的Camera， 想要非UI元素加入推荐这个模式， 但是对于z轴不为0的元素，会单独渲染不参与合并。

**World Space** ： 世界空间上的UI


## Image ，RawImage

Image仅能展示图集中的图元，但是可以进行合并。
RawImage 能展示单张图片但是无法合并。