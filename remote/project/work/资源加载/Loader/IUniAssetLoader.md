
## interface  IUniAssetLoader

```c#
public interface IUniAssetLoader
{
	UniAssetLoaderStatus Status { get; }
	UniAssetLoaderType Type { get; }
	LoaderGroup Group { get; }
	bool IsDone { get; }
	string Error { get; }
	float Progress { get; }
	int Priority { get; set; }
	int ForcePriority { get; set; }
	float StartTime { get; }
	int RetryCount { get; set; }
	bool CanCacheMem { get; }
	string GetUrl();
	void SetUrl(string url);
	string GetCacheKey();
	void BeginLoad();
	void Release(bool releaseObject=true);
	void Cancel();
	bool TryUnloadCache();
	void AddICallback(UnityEngine.Events.UnityAction<IUniAssetLoader> loader);
}
```

**UniAssetLoaderStatus** ： loader 状态

```c#
public enum UniAssetLoaderStatus  
{  
    Waiting,  
    Loading,  
    Loaded,  
    Failed,  
    Cancel  
} 
```

**UniAssetLoaderType** : 资源类型 

```c#
public enum UniAssetLoaderType  
{  
    //local ab  
    LocalAssetBundle,  
    //http text asset  
    RemoteRawData,  
    Auto,  
}
```

**LoaderGroup** 资源分类

```c#
public enum LoaderGroup  
{  
    RpcReqeust,  
    NetReqeust,  
    LocalAssetBundle,  
    UniData,  
    NetTexture,  
    Audio,  
    Upload  
}
```


**用于cache**

m_CachedWeakUnityObjectDict
m_CachedWeakUnityObjectGCSwapDict

**用于加载流程**

m_WaitLoaders
m_LoadedLoaders
m_WaitDeletedLoaderKeys
m_LoadedGCSwapList
m_LoadingLoaders

**常用的变量**

lastActiveTime 上一次激活时间
CACHE_KEEP_TIME 一般为 3min 缓存保持时间
Start_Time : 开始加载时间
一般来说缓存就是 `AssetOperationHandle` 内部保存有资源
## interface IWeakCacheLoader  结合 网络资源使用

```c#
public interface IWeakCacheLoader  
{  
    bool TrySetCache(UnityEngine.Object cachedObject);  
    UnityEngine.Object GetCacheObject();  
}
```





