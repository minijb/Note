
# UniMain

## 初始化过程

### 1. PreInitialize

1. 对于 [[UniPluginInitializer]] 进行初始化
2. 创建 APPVersion
3. 初始化 Logger
4. 获得 [[UniModule -- 自定义模块#UniModuleManager|UniModuleManager]]   并得到内部注册的模块
5. UniModuleManager.onEnter
6. UniModuleManager.onInit
7. [[Loading UI]] --- init + setposition

### 2. Initialize

1. YooAsset 初始化 + 设置每帧最大时间片 (在 editor 模式下，使用模拟模式)
2. 具体过程 [[YooAsset#1. 初始化过程 | 实际调用的就是 YooAsset 的不同初始化策略]]

### 3. RequestLaunchGame 初始化游戏上下文 -- async

**Development 版本**

1. 新建上下文类
2. 等待之前的 YooAsset 初始化完成
3. [[UniGameLoadContext  load上下文#1. LoadPreAsset async|LoadPreAsset]]  添加更重全局设置
4. [[UniGameLoadContext  load上下文#2. LoadGameAsset async| LoadGameAsset]] 加载 Item 元素，以及 excel 内容信息
5.  加载 lua 模拟界面

### 4. 如何进入游戏

1. 使用lua 开启模拟器
2. 进入 `LuaDevRequestLaunchGame`, 启动游戏开启阶段

#### a. DevRequestLaunchGame

**LoadLaunchConfig**

1. 从 UniEnvironment 中得到  环境信息 (可变信息，如用户id， 场景信息等)， 用户id 这些， 服务器信息等
2.  将一些启动信息放入 UniLaunch 中， 并对 UniLaunch 和 UniEnvironment 中的信息做一些更改
3. 配置 NetworkSetting !!!
4. UserMe 用户自身信息初始化
5. 通过 RpcModule.QueryWork 得到 UniNetworkUniDataMetaLoader 进行异步加载?
6. 转 base.RequestLaunchGame

|
|
|

**UniMian.RequestLaunchGame** (Base)

1.  创建 UniPlayer  并初始化
	-  根据选择的世界类型，加载不同类型的世界
	- UniPlay -- Addwork
1.  UserSettingManager 注册时间, 用于setting修改后的配置更改 (Quality调整,  相机属性调整等)
2.  加载一个新的上下文  `UniGameLoadContext` ,  根据 launchConfig.EditType --- 找到需要加载的上下文
3. 重新执行 
	1. `ModuleManager.OnLoadPlay();  
	2. LoadPreAsset(loadContext);  
	3. LoadGameAsset(loadContext);`
4. [[UniPlay#Load|UniPlay.load(context)]]  根据上下文进行加载


> CharacterInfo :  角色在世界内的信息 ： 如 Avatar， Name .... 





