---
tags:
  - 面试
---
## ResourceManager

### 1. 初始化

**重点**  editor --- 是否使用AssetDataBase加载，类似于debug版本 --- 不适用 editor 则需要解析

1. 初始化 bundleManager(内部先加载 manifest -- window.manifest) [[面试 - AssetBundle-4 bundle]]

```c#

private const string MANIFEST_BUNDLE = "manifest.ab";
private const string RESOURCE_ASSET_NAME = "Assets/Temp/Resource.bytes";
private const string BUNDLE_ASSET_NAME = "Assets/Temp/Bundle.bytes";
private const string DEPENDENCY_ASSET_NAME = "Assets/Temp/Dependency.bytes";
/// <summary>
///   保存资源对应的bundle
/// </summary>
internal Dictionary<string, string> ResourceBunldeDic = new Dictionary<string, string>();

/// <summary>
/// 保存资源的依赖关系
/// </summary>
internal Dictionary<string, List<string>> ResourceDependencyDic = new Dictionary<string, List<string>>();

/// <summary>
/// 所有资源集合
/// </summary>
private Dictionary<string, AResource> m_ResourceDic = new Dictionary<string, AResource>();

/// <summary>
/// 异步加载集合
/// </summary>
private List<AResourceAsync> m_AsyncList = new List<AResourceAsync>();

/// <summary>
/// 需要释放的资源
/// </summary>
private LinkedList<AResource> m_NeedUnloadList = new LinkedList<AResource>();

/// <summary>
/// 是否使用AssetDataBase进行加载
/// </summary>
private bool m_Editor;

/// <summary>
/// 初始化
/// </summary>
/// <param name="platform">平台</param>
/// <param name="getFileCallback">获取资源真实路径回调</param>
/// <param name="editor">是否使用AssetDataBase加载</param>
/// <param name="offset">获取bundle的偏移</param>
public void Initialize(string platform, Func<string, string> getFileCallback, bool editor, ulong offset)
{
	m_Editor = editor;

	if (m_Editor)
		return;

	BundleManager.instance.Initialize(platform, getFileCallback, offset); // 原始的 manifest

	string manifestBunldeFile = getFileCallback.Invoke(MANIFEST_BUNDLE);// manifest.ab --- 自己加入的资源列表
	AssetBundle manifestAssetBundle = AssetBundle.LoadFromFile(manifestBunldeFile, 0, offset); 

	TextAsset resourceTextAsset = manifestAssetBundle.LoadAsset(RESOURCE_ASSET_NAME) as TextAsset;
	TextAsset bundleTextAsset = manifestAssetBundle.LoadAsset(BUNDLE_ASSET_NAME) as TextAsset;
	TextAsset dependencyTextAsset = manifestAssetBundle.LoadAsset(DEPENDENCY_ASSET_NAME) as TextAsset;

	byte[] resourceBytes = resourceTextAsset.bytes;
	byte[] bundleBytes = bundleTextAsset.bytes;
	byte[] dependencyBytes = dependencyTextAsset.bytes;

	// 资源拿到了  直接携带
	manifestAssetBundle.Unload(true);
	manifestAssetBundle = null;

	//保存id对应的asseturl
	Dictionary<ushort, string> assetUrlDic = new Dictionary<ushort, string>();

	#region 读取资源信息
	{
	}
	#endregion

	#region 读取bundle信息
	{
	}
	#endregion

	#region 读取资源依赖信息
	{
	}
	#endregion
}
```

#### 1.1 读取资源信息

id -- asseturl

```c#
MemoryStream resourceMemoryStream = new MemoryStream(resourceBytes);
BinaryReader resourceBinaryReader = new BinaryReader(resourceMemoryStream);
//获取资源个数
ushort resourceCount = resourceBinaryReader.ReadUInt16();
for (ushort i = 0; i < resourceCount; i++)
{
	string assetUrl = resourceBinaryReader.ReadString();
	assetUrlDic.Add(i, assetUrl);
}
```

#### 1.2 读取bundle信息

asseturl - bundleurl

```c#
ResourceBunldeDic.Clear();
MemoryStream bundleMemoryStream = new MemoryStream(bundleBytes);
BinaryReader bundleBinaryReader = new BinaryReader(bundleMemoryStream);
//获取bundle个数
ushort bundleCount = bundleBinaryReader.ReadUInt16();
for (int i = 0; i < bundleCount; i++)
{
	string bundleUrl = bundleBinaryReader.ReadString();
	//string bundleFileUrl = getFileCallback(bundleUrl);
	string bundleFileUrl = bundleUrl;
	//获取bundle内的资源个数
	ushort resourceCount = bundleBinaryReader.ReadUInt16();
	for (int ii = 0; ii < resourceCount; ii++)
	{
		ushort assetId = bundleBinaryReader.ReadUInt16();
		string assetUrl = assetUrlDic[assetId];
		ResourceBunldeDic.Add(assetUrl, bundleFileUrl);
	}
}
```

#### 1.3 读取资源依赖信息

asseturl - List depencesurl

```c#
ResourceDependencyDic.Clear();
MemoryStream dependencyMemoryStream = new MemoryStream(dependencyBytes);
BinaryReader dependencyBinaryReader = new BinaryReader(dependencyMemoryStream);
//获取依赖链个数
ushort dependencyCount = dependencyBinaryReader.ReadUInt16();
for (int i = 0; i < dependencyCount; i++)
{
	//获取资源个数
	ushort resourceCount = dependencyBinaryReader.ReadUInt16();
	ushort assetId = dependencyBinaryReader.ReadUInt16();
	string assetUrl = assetUrlDic[assetId];
	List<string> dependencyList = new List<string>(resourceCount);
	for (int ii = 1; ii < resourceCount; ii++)
	{
		ushort dependencyAssetId = dependencyBinaryReader.ReadUInt16();
		string dependencyUrl = assetUrlDic[dependencyAssetId];
		dependencyList.Add(dependencyUrl);
	}

	ResourceDependencyDic.Add(assetUrl, dependencyList);
}
```

### 2. LoadCallBack

```c#
/// <summary>
/// 加载资源
/// </summary>
/// <param name="url">资源Url</param>
/// <param name="async">是否异步</param>
/// <param name="callback">加载完成回调</param>
public void LoadWithCallback(string url, bool async, Action<IResource> callback)
{
	AResource resource = LoadInternal(url, async, false);
	if (resource.done)
	{
		callback?.Invoke(resource);
	}
	else
	{
		resource.finishedCallback += callback;
	}
}
```

内部使用 LoadInternal 进行真实的资源加载

加载好之后会加上callback
### 3  LoadInternal

1. 尝试在缓存中拿到资源
	1. 注意：如果目标资源在缓存中，同时 reference 为0 --- 就是说明 当前资源在待卸载列表中
	2. 我们需要 添加 reference 同时 ，移除出 待卸载列表
2. 选择合适的 资源类型 [[面试 - AssetBundle-5 Resource#3. 多种资源管理方案|三种资源类型的详细描述]]
	- 对于 普通资源(ab包资源)， editorResource 这两种资源 --- 可以直接使用
	- 对于异步资源 ，存在一个 List `m_AsyncList` 辅助进行加载
3. 将资源添加到 `m_ResourceDic`
4. 进行依赖加载
5. 添加 reference ， 使用 Load 进行加载

```c#
/// <summary>
/// 内部加载资源
/// </summary>
/// <param name="url">资源url</param>
/// <param name="async">是否异步</param>
/// <param name="dependency">是否依赖</param>
/// <returns></returns>
private AResource LoadInternal(string url, bool async, bool dependency)
{
	AResource resource = null;
	if (m_ResourceDic.TryGetValue(url, out resource)) // 先查看缓存
	{
		//从需要释放的列表中移除
		if (resource.reference == 0)
		{
			m_NeedUnloadList.Remove(resource);// 分时卸载列表
		}

		resource.AddReference();

		return resource;
	}

	//创建Resource --- 选择合适的资源类型
	if (m_Editor)
	{
		resource = new EditorResource();
	}
	else if (async)
	{
		ResourceAsync resourceAsync = new ResourceAsync();
		m_AsyncList.Add(resourceAsync);
		resource = resourceAsync;
	}
	else
	{
		resource = new Resource();
	}

	resource.url = url;
	m_ResourceDic.Add(url, resource);

	//加载依赖
	List<string> dependencies = null;
	ResourceDependencyDic.TryGetValue(url, out dependencies);
	if (dependencies != null && dependencies.Count > 0)
	{
		resource.dependencies = new AResource[dependencies.Count];
		for (int i = 0; i < dependencies.Count; i++)
		{
			string dependencyUrl = dependencies[i];
			AResource dependencyResource = LoadInternal(dependencyUrl, async, true);
			resource.dependencies[i] = dependencyResource;
		}
	}

	resource.AddReference();
	resource.Load();

	return resource;
}
```

#### 2.2 LoadAsset

##### 2.2.1 同步

```c#
/// <summary>
/// 加载资源
/// </summary>
internal override void LoadAsset()
{
	if (bundle == null)
		throw new Exception($"{nameof(Resource)}.{nameof(LoadAsset)}() {nameof(bundle)} is null.");

	//正在异步加载的资源要变成同步 --- 部分同步资源内含有异步资源
	FreshAsyncAsset();

	if (!bundle.isStreamedSceneAssetBundle) // 是否是场景
		asset = bundle.LoadAsset(url, typeof(Object));

	asset = bundle.LoadAsset(url, typeof(Object));

	done = true;

	if (finishedCallback != null)
	{
		Action<AResource> tempCallback = finishedCallback;
		finishedCallback = null;
		tempCallback.Invoke(this);
	}
}


```


##### 2.2.2 异步 --- 这里将异步的资源作为同步的处理

```c#
/// <summary>
/// 加载资源
/// </summary>
internal override void LoadAsset()
{
	if (bundle == null)
		throw new Exception($"{nameof(ResourceAsync)}.{nameof(LoadAsset)}() {nameof(bundle)} is null.");

	if (!bundle.isStreamedSceneAssetBundle)
	{
		if (m_AssetBundleRequest != null)
		{
			asset = m_AssetBundleRequest.asset;
		}
		else
		{
			asset = bundle.LoadAsset(url, typeof(Object)); // 这里 将 同步的资源 进行异步的处理
		}
	}

	done = true;

	if (finishedCallback != null)
	{
		Action<AResource> tempCallback = finishedCallback;
		finishedCallback = null;
		tempCallback.Invoke(this);
	}
}


```

##### 2.2.3 LoadAssetAsync

```c#
/// <summary>
/// 异步加载资源
/// </summary>
internal override void LoadAssetAsync()
{
	if (bundle == null)
		throw new Exception($"{nameof(ResourceAsync)}.{nameof(LoadAssetAsync)}() {nameof(bundle)} is null.");

	m_AssetBundleRequest = bundle.LoadAssetAsync(url, typeof(Object));
}
```


### 4.  将异步资源变为同步


```c#
/// <summary>
/// 刷新异步资源（当同步资源的依赖包含异步时，需要立即刷新返回）
/// </summary>
internal void FreshAsyncAsset()
{
	if (done)
		return;

	if (dependencies != null)
	{
		for (int i = 0; i < dependencies.Length; i++)
		{
			AResource resource = dependencies[i];
			resource.FreshAsyncAsset();
		}
	}

	if (this is AResourceAsync)
	{
		LoadAsset();
	}
}
```

### 5. Update

```c#

public void Update()
{
	BundleManager.instance.Update();

	for (int i = 0; i < m_AsyncList.Count; i++)
	{
		AResourceAsync resourceAsync = m_AsyncList[i];
		if (resourceAsync.Update())
		{
			m_AsyncList.RemoveAt(i);
			i--;

			if (resourceAsync.awaiter != null)
			{
				resourceAsync.awaiter.SetResult(resourceAsync as IResource);
			}
		}
	}
}

```

### 6. LateUpdate

```c#
public void LateUpdate()
{
	if (m_NeedUnloadList.Count != 0)
	{
		while (m_NeedUnloadList.Count > 0)
		{
			AResource resource = m_NeedUnloadList.First.Value;
			m_NeedUnloadList.RemoveFirst();
			if (resource == null)
				continue;

			m_ResourceDic.Remove(resource.url);

			resource.UnLoad();

			//依赖引用-1
			if (resource.dependencies != null)
			{
				for (int i = 0; i < resource.dependencies.Length; i++)
				{
					AResource temp = resource.dependencies[i];
					Unload(temp);
				}
			}
		}
	}

	BundleManager.instance.LateUpdate();
}
```

## 使用 资源

```c#
    // Use this for initialization
    void Start()
    {
        m_BackgourndIndex = -1;
        m_BearIndex = -1;
        m_IconIndex = -1;
    }

    // Update is called once per frame
    void Update()
    {

    }

    /// <summary>
    /// 切换背景的sprite  循环切换背景图片
    /// </summary>
    public void OnChangeBackground()
    {
        if (m_Backgrounds.Length == 0)
            return;

        m_BackgourndIndex = ++m_BackgourndIndex % m_Backgrounds.Length;

        string backgroundUrl = m_Backgrounds[m_BackgourndIndex];

        //同步加载背景的sprite
        IResource resource = ResourceManager.instance.Load(backgroundUrl, false);
        m_RawImage_Background.texture = resource.GetAsset() as Texture;
    }
```

## 总结


Load的流程：
1. ResourceManager --> Load
	1. 先找缓存
	2. 根据不同资源类型创建资源 Resource
	3. 查找依赖 --- **递归的进行加载**
	4. 加载 Resource ---> load
		1. 确保资源没有加载
		2. 在 自己的 资源列表中 找到 bundle 资源
		3. bundleManager --> Load
			1. 使用 bundleManager 进行 load --- 加入 dic 。。
			2. 判断是否是异步加载
			3. 根据 window.manifest 找到依赖项目 --- **递归的进行加载**
			4. 加载 bundle --> load
				1. 确保没有被加载
				2. 找到url
				3. 进行 ab 资源加载
	5. **LoadAsset**  !!!!
		1. 如果 bundle 为空 报错
		2. 将异步的变为同步
		3. 同步的处理asset `LoadAsset`
		4. done = true !!!!!
		5. finishcallabcl
	5. LoadAssetAsync : 异步如何加载
		1. 提出请求
		2. `if (m_AssetBundleRequest != null && !m_AssetBundleRequest.isDone) ` == 已经发出请求， 同时请求完成才可以进行 loadAsset
		3. 取出  m_AssetBundleRequest 中的 asset 