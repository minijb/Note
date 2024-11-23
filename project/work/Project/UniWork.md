
### Load

判断是加载现有的， 还是需要新建、下载。

现有的直接加载 --- [[UniWork#OnLoadWork]]

TODO ： 新的需要新建 --- 上传。

### OnLoadWork

**本地加载**

先找本地的然后进行更新?    [[UniWork#QueryWork]]


**远程下载**  

直接 [[UniWork#DownloadUniFile]]


### QueryWork

简单过程 ： 根据类型创建一个  UniNetworkUniDataMetaLoader， 并加入一个 callback

```c#
var metaLoader = UniMain.RpcModule.QueryWork(Id, Version, type, category);  
metaLoader.AddCallback((l) =>  
{  
	
});
```


callback :

1. 确实是否接收成功
2. 如果成功
	1.  对特定的世界进行一些处理， 得到 meta
	2. 根据meta ，得到下载需要的数据  [[UniWork#DownloadUniFile]]


### DownloadUniFile  --- 得到 UniFile 文件

根据不同世界类型，做一些 数据更新，并填装世界数据(work data)

### OnWorkLoaded

更新 step数据

### ParseUniFile --- 根据 [[UniNetworkUniDataLoader]] 文件从网络获取具体地图信息

先通过的通过 [[UniNetworkUniDataLoader#GetUniNodeFile]] 获取 UniNodeFile , 并根据其获取真实的节点数据

UniWork --> CheckAndCreateDefaultNodeData 进行检查










