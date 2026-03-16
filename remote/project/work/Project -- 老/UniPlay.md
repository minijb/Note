
### Load

使用 play 加载上下文. --- `UniPlay.Load(context)`
	1. 这里需要加载 UniWork --- UniWork 为具体的世界场景 (一些基础信息如 workid 等)
	2. 进行 Lobby 网路连接 . ---  参数 : 上下文 ---- 很复杂....
	3. RequestEnterMainScene(loadContext);   请求进入 主场景 ---  参数 : 上下文
		-   设置上下文中的步骤信息 --- `EnterGameScene`
		-   注意!!! : 这里根据不同的游戏类型如 (联机游戏，世界/单人游戏做了不同的 env 处理)
			- 联机模式 -- 清理并重新配置 UniSession/UniWork/CharacterInfo (根据 网络 respone 的回应) / 会同步到 StoreModule
	1.  [[UniPlay#LoadGame --- 根据上下文 加载 游戏|LoadGame(loadContext);]]    加载 Game --- 游戏控制 ---  参数 : 上下文



## LoadGame --- 根据上下文 加载 游戏

1. 第一步 ： 创建 UniGame 实例。 InitializeGame() --> Game.Initialize
2. ModuleManager 中所有模块使用 onLoadGame
3. 调用 Game 中的加载方法
	1. [[UniGame#DownloadGameWork]]  加载世界数据
	2. [[UniGame#ParseGameWork -- 数据解析]]  根据 unifile 进行数据解析
	3. [[UniGame#StartRoomHost -- 连接服务器]]
	4. [[UniGame#LoadGameUI]]

### ParseGameWork -- 解析下载的文件内容

根据前者得到的信息，对文件进行解析。

根据之前得到的 fileLoader ([[UniWork#QueryWork]] --> [[UniWork#DownloadUniFile]])

