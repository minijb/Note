
本地资源加载

1. State --> waiting
2. Type --> LocalAssetBundle
3. Group --> LocalAssetBundle

AssetOperationHandle --- YooAsset 资源加载类

**beginLoad** ： 
设置 Status/Time , 调用 YooAsset 中的异步加载方法进行加载 (需要这只 OnCompleted 会掉函数，将 loader 加载完成)。

**LoadAsset** ：

- 没有加载完成则强制执行加载 --- `WaitForAsyncComplete`
- 加载完成，返回资源

**AddCallback**

添加完成后的回调函数

## UniAddressableLoaderSettings

本地资源上下文

