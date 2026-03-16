
## 1. 初始化过程

### 1.1 初始化

1. YooAsset 初始化系统
2. 创建默认包资源

### 1.2  配置模式 (playmode)

在编辑器模式下使用模拟模式。

**具体步骤**
1.  `InitializeParameters.cs` 下创建对应 `xxxParameters`
	1.  editor 模拟 `EditorSimulateModeParameters`
	2. 离线模式 `OfflinePlayModeParameters`
	3. 网络模式 `WebPlayModeParameters`
2. 对不同的模式进行不同的处理，如添加资源路径，配置服务器等
3. 异步初始化 ， 注意需要添加 complete 回调函数(自定义)
