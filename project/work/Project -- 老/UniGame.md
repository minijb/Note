
### Initialize

添加一下 component

1.  Mirror 模块
2.  UniCharacters
3.  UniInteractManager  交互管理模块
4.  UniSwitchManager  服务器和客户端 时间交互通道/事件池
5.  UniUGVAvatarAnimationModule  动作管理
6.  UGCScriptExecuteService 代码执行 ？ 是不是自适应代码那个
7.  UniMissileManager  子弹管理？
8.  UniRankModule 排行管理 

根据 世界类型 在 UniScene 中 添加对应的 UnixxxScene.

[[UniScene#PreInitialize| Uniplay --> PreInitialize]]-- 进行预处理



### DownloadGameWork


实际调用 [[UniWork#Load]] 进行 世界数据加载 

### ParseGameWork -- 数据解析

[[UniWork#ParseUniFile]]

### StartRoomHost -- 连接服务器

KcpTransport + TelepathyTransport 


## 游戏场景加载
### LoadUnityGameScene

异步加载并正确的场景 Scene ， 同时将一些组件移动到这个 Scene

### LoadGameCamera

同理

### LoadGameUI

UI加载

1. 加载 inputSystem -- 
	1. 直接拿到新版输入系统的配置
	2. 便利 Player，UI 等配置，绑定对应的 event。
	3. *解绑就是解除 event*
2.  UI系统初始化
	1. UIHelper 初始化
