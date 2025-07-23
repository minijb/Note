
## GC

1. 处理 `m_LoadedLoaders` 列表
- 如果存在可转化的弱引用 [[C Sharp WeakReference]] -- IWeakCacheLoader  则将对应的资源转化为弱引用，保存在  `m_CachedWeakUnityObjectGCSwapDict`
- 否则(没有弱引用资源) 直接装入到 `m_LoadedGCSwapList` 中

2. 交换 `m_LoadedGCSwapList` , `m_LoadedLoaders`

此时就 `m_LoadedLoaders` 就没有弱引用了

3. 将 `m_CachedWeakUnityObjectGCSwapDict` 资源合并到 `m_CachedWeakUnityObjectDict`

如果是服务器 则需要 `Resources.UnloadUnusedAssets();`


## 根据 tag/Address 获得资源

利用 YooAsset 特性 根据 package 的 package/path/label/泛型 得到资源。返回 YooAssetHandle

## 默认缓存机制

1. check Persisitent path
2. 写入

## 资源装载卸载流程 -- loader

**Remove** : 删除位置 ： loaded,wait,loading 三个位置的loader
**TryLoad** ：每帧执行

- 对 waitLoaders 进行排序
- 根据分类(local/remote) 填充到 loaders中
	- 根据 MaxLocal/RemoteThread 进行填充，防止同时加载的loader的数量过多
	- 将加载的loader.BeginLoad()

**OnLoaderLoaded** : 结束的时候将自身在 loading 列表中删除，并加入到 loaded 列表

**Clear** 根据组(Loader的资源类型)进行清除 可变参数

**加载静态资源**： Text文件 --- 常用于加载本地的资源类型表。

**CreateLoader** 创建loader， 并加入到 WaitLoader 中 --- 异步加载