---
tags:
  - 面试
---
## bundleManager

### 1. 初始化

**offset ： 偏移值，用于防止解密**

1. 拿到 manifest 文件
2. 并加载 manifest 中的所有文件


```c#
    public readonly static BundleManager instance = new BundleManager();

    /// <summary>
    /// 加载bundle开始的偏移
    /// </summary>
    internal ulong offset { get; private set; }

    /// <summary>
    /// 获取资源真实路径回调
    /// </summary>
    private Func<string, string> m_GetFileCallback;

    /// <summary>
    /// bundle依赖管理信息
    /// </summary>
    private AssetBundleManifest m_AssetBundleManifest;

    /// <summary>
    /// 所有已加载的bundle
    /// </summary>
    private Dictionary<string, ABundle> m_BundleDic = new Dictionary<string, ABundle>();

    //异步创建的bundle加载时候需要先保存到该列表
    private List<ABundleAsync> m_AsyncList = new List<ABundleAsync>();

    /// <summary>
    /// 需要释放的bundle
    /// </summary>
    private LinkedList<ABundle> m_NeedUnloadList = new LinkedList<ABundle>();

    /// <summary>
    /// 初始化
    /// </summary>
    /// <param name="platform">平台</param>
    /// <param name="getFileCallback">获取资源真实路径回调</param>
    /// <param name="offset">加载bundle偏移</param>
    internal void Initialize(string platform, Func<string, string> getFileCallback, ulong offset)
    {
        m_GetFileCallback = getFileCallback;
        this.offset = offset;

        string assetBundleManifestFile = getFileCallback.Invoke(platform);

        AssetBundle manifestAssetBundle = AssetBundle.LoadFromFile(assetBundleManifestFile); // xx/xx/Window.manifest
        Object[] objs = manifestAssetBundle.LoadAllAssets(); // 加载文件

        if (objs.Length == 0)
        {
            throw new Exception($"{nameof(BundleManager)}.{nameof(Initialize)}() AssetBundleManifest load fail.");
        }

        m_AssetBundleManifest = objs[0] as AssetBundleManifest;
    }
```

### 2. Load 资源加载

分为同步加载和异步加载

```c#
/// <summary>
/// 同步加载bundle
/// </summary>
/// <param name="url">asset路径</param>
internal ABundle Load(string url)
{
	return LoadInternal(url, false);
}

/// <summary>
/// 异步加载bundle
/// </summary>
/// <param name="url">asset路径</param>
internal ABundle LoadAsync(string url)
{
	return LoadInternal(url, true);
}
```

**真实的 加载方法**

类似 ResourceManager

- 先找缓存
- 根据情况 选择两种类型 ： 是否为异步
- 然后加载依赖，递归加载
- 添加索引，并 load bundle


```c#
/// <summary>
/// 内部加载bundle
/// </summary>
/// <param name="url">asset路径</param>
/// <param name="async">是否异步</param>
/// <returns>bundle对象</returns>
private ABundle LoadInternal(string url, bool async)
{
	ABundle bundle;
	if (m_BundleDic.TryGetValue(url, out bundle))
	{
		if (bundle.reference == 0)
		{
			m_NeedUnloadList.Remove(bundle);
		}

		//从缓存中取并引用+1
		bundle.AddReference();

		return bundle;
	}

	//创建ab
	if (async)
	{
		bundle = new BundleAsync();
		bundle.url = url;
		m_AsyncList.Add(bundle as ABundleAsync);
	}
	else
	{
		bundle = new Bundle();
		bundle.url = url;
	}

	m_BundleDic.Add(url, bundle);

	//加载依赖
	string[] dependencies = m_AssetBundleManifest.GetDirectDependencies(url);
	if (dependencies.Length > 0)
	{
		bundle.dependencies = new ABundle[dependencies.Length];
		for (int i = 0; i < dependencies.Length; i++)
		{
			string dependencyUrl = dependencies[i];
			ABundle dependencyBundle = LoadInternal(dependencyUrl, async);
			bundle.dependencies[i] = dependencyBundle;
		}
	}

	bundle.AddReference();

	bundle.Load();

	return bundle;
}
```

### 3. GetFileUrl

```c#
/// <summary>
/// 获取bundle的绝对路径
/// </summary>
/// <param name="url"></param>
/// <returns>bundle的绝对路径</returns>
internal string GetFileUrl(string url)
{
	if (m_GetFileCallback == null)
	{
		throw new Exception($"{nameof(BundleManager)}.{nameof(GetFileUrl)}() {nameof(m_GetFileCallback)} is null.");
	}

	//交到外部处理
	return m_GetFileCallback.Invoke(url);
}
```


### 4. Update

异步的加载 资源

```c#
public void Update()
{
	for (int i = 0; i < m_AsyncList.Count; i++)
	{
		if (m_AsyncList[i].Update())
		{
			m_AsyncList.RemoveAt(i);
			i--;
		}
	}
}
```


### 5. LateUpdate

主要用于卸载 bundle 包

```c#
public void LateUpdate()
{
	if (m_NeedUnloadList.Count == 0)
		return;

	while (m_NeedUnloadList.Count > 0)
	{
		ABundle bundle = m_NeedUnloadList.First.Value;
		m_NeedUnloadList.RemoveFirst();
		if (bundle == null)
			continue;

		m_BundleDic.Remove(bundle.url);

		if (!bundle.done && bundle is BundleAsync)
		{
			BundleAsync bundleAsync = bundle as BundleAsync;
			if (m_AsyncList.Contains(bundleAsync))
				m_AsyncList.Remove(bundleAsync);
		}

		bundle.UnLoad();

		//依赖引用-1
		if (bundle.dependencies != null)
		{
			for (int i = 0; i < bundle.dependencies.Length; i++)
			{
				ABundle temp = bundle.dependencies[i];
				UnLoad(temp);
			}
		}
	}
}
```

### 6. UnLoad

WillUnload --- 放入一个列表中，用于存放将要释放的资源

```c#
/// <summary>
/// 卸载bundle
/// </summary>
/// <param name="bundle">要卸载的bundle</param>
internal void UnLoad(ABundle bundle)
{
	if (bundle == null)
		throw new ArgumentException($"{nameof(BundleManager)}.{nameof(UnLoad)}() bundle is null.");

	//引用-1
	bundle.ReduceReference();

	//引用为0,直接释放
	if (bundle.reference == 0)
	{
		WillUnload(bundle);  // 不直接释放， 而是 异步的释放
	}
}
```

## Bundle 类

### ABundle

```C#
internal abstract class ABundle
{
    /// <summary>
    /// AssetBundle
    /// </summary>
    internal AssetBundle assetBundle { get; set; }

    /// <summary>
    /// 是否是场景
    /// </summary>
    internal bool isStreamedSceneAssetBundle { get; set; }

    /// <summary>
    /// bundle url
    /// </summary>
    internal string url { get; set; }

    /// <summary>
    /// 引用计数器
    /// </summary>
    internal int reference { get; set; }

    //bundle是否加载完成
    internal bool done { get; set; }

    /// <summary>
    /// bundle依赖
    /// </summary>
    internal ABundle[] dependencies { get; set; }

    /// <summary>
    /// 加载bundle
    /// </summary>
    internal abstract void Load();

    /// <summary>
    /// 卸载bundle
    /// </summary>
    internal abstract void UnLoad();

    /// <summary>
    /// 异步加载资源
    /// </summary>
    /// <param name="name">资源名称</param>
    /// <param name="type">资源Type</param>
    /// <returns>AssetBundleRequest</returns>
    internal abstract AssetBundleRequest LoadAssetAsync(string name, Type type);

    /// <summary>
    /// 加载资源
    /// </summary>
    /// <param name="name">资源名称</param>
    /// <param name="type">资源Type</param>
    /// <returns>指定名字的资源</returns>
    internal abstract Object LoadAsset(string name, Type type);

    /// <summary>
    /// 增加引用
    /// </summary>
    internal void AddReference()
    {
        //自己引用+1
        ++reference;
    }

    /// <summary>
    /// 减少引用
    /// </summary>
    internal void ReduceReference()
    {
        //自己引用-1
        --reference;

        if (reference < 0)
        {
            throw new Exception($"{GetType()}.{nameof(ReduceReference)}() less than 0,{nameof(url)}:{url}.");
        }
    }
}
```


### 1. Load

1. 先尝试拼接路径
2. 分平台 处理一下 --- editor 找到包资源
3. 根据是否是异步，使用不同的 assetbundle api

#### 1.1 同步

```c#
/// <summary>
/// 加载AssetBundle
/// </summary>
internal override void Load()
{
	if (assetBundle)
	{
		throw new Exception($"{nameof(Bundle)}.{nameof(Load)}() {nameof(assetBundle)} not null , Url:{url}.");
	}

	string file = BundleManager.instance.GetFileUrl(url);

#if UNITY_EDITOR || UNITY_STANDALONE
		if (!File.Exists(file))
		{
			throw new FileNotFoundException($"{nameof(Bundle)}.{nameof(Load)}() {nameof(file)} not exist, file:{file}.");
		}
#endif

	assetBundle = AssetBundle.LoadFromFile(file, 0, BundleManager.instance.offset);

	isStreamedSceneAssetBundle = assetBundle.isStreamedSceneAssetBundle;

	done = true;
}
```

#### 1.2 异步

```c#
/// <summary>
/// 异步bundle的AssetBundleCreateRequest
/// </summary>
private AssetBundleCreateRequest m_AssetBundleCreateRequest;

/// <summary>
/// 加载AssetBundle
/// </summary>

internal override void Load()
{
	if (m_AssetBundleCreateRequest != null)
	{
		throw new Exception($"{nameof(BundleAsync)}.{nameof(Load)}() {nameof(m_AssetBundleCreateRequest)} not null, {this}.");
	}

	string file = BundleManager.instance.GetFileUrl(url);

#if UNITY_EDITOR || UNITY_STANDALONE
		if (!File.Exists(file))
		{
			throw new FileNotFoundException($"{nameof(BundleAsync)}.{nameof(Load)}() {nameof(file)} not exist, file:{file}.");
		}
#endif

	m_AssetBundleCreateRequest = AssetBundle.LoadFromFileAsync(file, 0, BundleManager.instance.offset);
}
```


### 2. LoadAsset

**这里 Loadasset 的方式 是类似的 只是  异步bundle 资源会额外判断是否含有  异步的bundle 包是否加载**

**同时两种 bundle 资源都可以进行 同步/异步加载资源**  --- **原因是 部分同步 bundle 中含有 异步 bundle  ，此时 ，会将异步 bundle 刷新成同步的 bundle **  [[面试 - AssetBundle-3 ResourceManager#3. 将异步资源变为同步]]

```c#
/// <summary>
/// 异步加载资源
/// </summary>
/// <param name="name">资源名称</param>
/// <param name="type">资源Type</param>
/// <returns>AssetBundleRequest</returns>
internal override AssetBundleRequest LoadAssetAsync(string name, Type type)
{
	if (string.IsNullOrEmpty(name))
		throw new ArgumentException($"{nameof(BundleAsync)}.{nameof(LoadAssetAsync)}() name is null.");

	if (m_AssetBundleCreateRequest == null) // ================== 多出的判断 ====================
		throw new NullReferenceException($"{nameof(BundleAsync)}.{nameof(LoadAssetAsync)}() m_AssetBundleCreateRequest is null.");

	if (assetBundle == null)
		assetBundle = m_AssetBundleCreateRequest.assetBundle;

	return assetBundle.LoadAssetAsync(name, type);
}

/// <summary>
/// 加载资源
/// </summary>
/// <param name="name">资源名称</param>
/// <param name="type">资源Type</param>
/// <returns>指定名字的资源</returns>
internal override Object LoadAsset(string name, Type type)
{
	if (string.IsNullOrEmpty(name))
		throw new ArgumentException($"{nameof(BundleAsync)}.{nameof(LoadAsset)}() name is null.");

	if (m_AssetBundleCreateRequest == null)  // ================== 多出的判断 ====================
		throw new NullReferenceException($"{nameof(BundleAsync)}.{nameof(LoadAsset)}() m_AssetBundleCreateRequest is null.");

	if (assetBundle == null)
		assetBundle = m_AssetBundleCreateRequest.assetBundle;

	return assetBundle.LoadAsset(name, type);
}

```


### 3. Update 在处理异步的 bundle 信息时，每一帧处理一个资源

- 如果已经处理完成 返回 true，
- 如果 含有依赖返回同时 依赖没有处理完成 返回false
- bundle 没有处理完成 返回 false
- 处理资源
	- 如果索引为0 则卸载



```c#
internal override bool Update()
{
	if (done)
		return true;


	if (dependencies != null)
	{
		for (int i = 0; i < dependencies.Length; i++)
		{
			if (!dependencies[i].done)
				return false;
		}
	}

	if (!m_AssetBundleCreateRequest.isDone)
		return false;

	done = true;

	assetBundle = m_AssetBundleCreateRequest.assetBundle;

	isStreamedSceneAssetBundle = assetBundle.isStreamedSceneAssetBundle;

	if (reference == 0)
	{
		UnLoad();
	}

	return true;
}
```

### 4. unLoad

#### 4.3 同步

```c#
/// <summary>
/// 卸载bundle
/// </summary>
internal override void UnLoad()
{
	if (assetBundle)
		assetBundle.Unload(true);

	assetBundle = null;
	done = false;
	reference = 0;
	isStreamedSceneAssetBundle = false;
}
```

##### 4.2 Async

unload --- true : 会见生成资源一起释放

```c#
/// <summary>
/// 卸载bundle
/// </summary>
internal override void UnLoad()
{
	if (assetBundle)
	{
		assetBundle.Unload(true);
	}
	else
	{
		//正在异步加载的资源也要切到主线程进行释放
		if (m_AssetBundleCreateRequest != null)
		{
			assetBundle = m_AssetBundleCreateRequest.assetBundle;
		}

		if (assetBundle)
		{
			assetBundle.Unload(true);
		}
	}

	m_AssetBundleCreateRequest = null;
	done = false;
	reference = 0;
	assetBundle = null;
	isStreamedSceneAssetBundle = false;
}

```

