---
tags:
  - 面试
---
## Resource 类

### 1. IResource 接口

1. 得到资源
2. 多种初始化资源

```c#
public interface IResource
{
    string url { get; }
    Object GetAsset();
    T GetAsset<T>() where T : Object;
    GameObject Instantiate();
    GameObject Instantiate(bool autoUnload);
    GameObject Instantiate(Vector3 position, Quaternion rotation);
    GameObject Instantiate(Vector3 position, Quaternion rotation, bool autoUnload);
    GameObject Instantiate(Transform parent, bool instantiateInWorldSpace);
    GameObject Instantiate(Transform parent, bool instantiateInWorldSpace, bool autoUnload);
}
```

### 2. AResouce 抽象类，具体实现一些接口

**gameobject 是如何取出来的  ---- 是复制出来的**

```c#
public GameObject Instantiate()
{
	Object obj = asset;

	if (!obj)
		return null;

	if (!(obj is GameObject))
		return null;

	return Object.Instantiate(obj) as GameObject;
}
```

```c#
internal abstract class AResource : CustomYieldInstruction, IResource
{
    /// <summary>
    /// Asset对应的Url
    /// </summary>
    public string url { get; set; }

    /// <summary>
    /// 加载完成的资源
    /// </summary>
    public virtual Object asset { get; protected set; }

    /// <summary>
    /// 引用的Bundle
    /// </summary>
    internal ABundle bundle { get; set; }

    /// <summary>
    /// 依赖资源
    /// </summary>
    internal AResource[] dependencies { get; set; }

    /// <summary>
    /// 引用计数器
    /// </summary>
    internal int reference { get; set; }

    //是否加载完成
    internal bool done { get; set; }

    /// <summary>
    /// awaiter
    /// </summary>
    internal ResourceAwaiter awaiter { get; set; }

    /// <summary>
    /// 加载完成回调
    /// </summary>
    internal Action<AResource> finishedCallback { get; set; }

    /// <summary>
    /// 加载资源
    /// </summary>
    internal abstract void Load();

    /// <summary>
    /// 卸载资源
    /// </summary>
    internal abstract void UnLoad();

    /// <summary>
    /// 加载资源
    /// </summary>
    internal abstract void LoadAsset();

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

    /// <summary>
    /// 增加引用
    /// </summary>
    internal void AddReference()
    {
        ++reference;
    }

    /// <summary>
    /// 减少引用
    /// </summary>
    internal void ReduceReference()
    {
        --reference;

        if (reference < 0)
        {
            throw new Exception($"{GetType()}.{nameof(ReduceReference)}() less than 0,{nameof(url)}:{url}.");
        }
    }

    public Object GetAsset()
    {
        return asset;
    }

    public abstract T GetAsset<T>() where T : Object;

	// Instance 实例化对象 ----
}
```

### 3. 多种资源管理方案

1. editorResource  使用编辑器开发的时候使用的资源
2. ab 包资源
3. 异步资源

对于 异步资源， manager 中存在一个 list 用于加载。

#### 3.1 EditorResource

```c#
internal class EditorResource : AResource
{
    public override bool keepWaiting => !done;

    /// <summary>
    /// 加载资源
    /// </summary>
    internal override void Load()
    {
        if (string.IsNullOrEmpty(url))
            throw new ArgumentException($"{nameof(EditorResource)}.{nameof(Load)}() {nameof(url)} is null.");

        LoadAsset();
    }

    /// <summary>
    /// 加载资源
    /// </summary>
    internal override void LoadAsset()
    {
#if UNITY_EDITOR
            asset = UnityEditor.AssetDatabase.LoadAssetAtPath<Object>(url);
#endif
        done = true;

        if (finishedCallback != null)
        {
            Action<AResource> tempCallback = finishedCallback;
            finishedCallback = null;
            tempCallback.Invoke(this);
        }
    }

    public override T GetAsset<T>()
    {
        Object tempAsset = asset;
        Type type = typeof(T);
        if (type == typeof(Sprite))
        {
            if (asset is Sprite)
            {
                return tempAsset as T;
            }
            else
            {
#if UNITY_EDITOR
                    if (tempAsset && !(tempAsset is GameObject))
                    {
                        Resources.UnloadAsset(tempAsset);
                    }

                    asset = UnityEditor.AssetDatabase.LoadAssetAtPath<Sprite>(url);
#endif
                return asset as T;
            }
        }
        else
        {
            return tempAsset as T;
        }
    }

    /// <summary>
    /// 卸载资源
    /// </summary>
    internal override void UnLoad()
    {
        if (asset != null && !(asset is GameObject))
        {
            Resources.UnloadAsset(base.asset);
            asset = null;
        }

        asset = null;
        awaiter = null;
        finishedCallback = null;
    }
}
```


#### 3.1.1 unload

```c#
/// <summary>
/// 卸载资源
/// </summary>
internal override void UnLoad()
{
	if (asset != null && !(asset is GameObject))
	{
		Resources.UnloadAsset(base.asset);
		asset = null;
	}

	asset = null;
	awaiter = null;
	finishedCallback = null;
}
```



#### 3.2 ResourceAsync

##### 异步资源接口

```c#
internal abstract class AResourceAsync : AResource
{
    public abstract bool Update();

    /// <summary>
    /// 异步加载资源
    /// </summary>
    internal abstract void LoadAssetAsync();
}
```

##### Update

```c#
public override bool Update()
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

	if (!bundle.done)
		return false;

	if (m_AssetBundleRequest == null)
	{
		LoadAssetAsync();
	}

	if (m_AssetBundleRequest != null && !m_AssetBundleRequest.isDone)
		return false;

	LoadAsset();

	return true;
}
```

##### LoadAssetAsync

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


###### LoadAsset

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
			asset = bundle.LoadAsset(url, typeof(Object));
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



#### 3.3 Resource

##### 3.3.1 Load

- 当前的 bundle 应该为空， 进行判断， 
- 使用 BundleManager 进行加载

```c#
/// <summary>
/// 加载资源
/// </summary>
internal override void Load()
{
	if (string.IsNullOrEmpty(url))
		throw new ArgumentException($"{nameof(Resource)}.{nameof(Load)}() {nameof(url)} is null.");

    if (bundle != null) // 当前已经存在资源 ， 逻辑错误
		throw new Exception($"{nameof(Resource)}.{nameof(Load)}() {nameof(bundle)} not null.");

	string bundleUrl = null;
	if (!ResourceManager.instance.ResourceBunldeDic.TryGetValue(url, out bundleUrl)) // 在资源管理其中 找不到对应的bundle
		throw new Exception($"{nameof(Resource)}.{nameof(Load)}() {nameof(bundleUrl)} is null.");

	bundle = BundleManager.instance.Load(bundleUrl);
	LoadAsset();
}

```

##### 3.3.2 unLoad

- 简单来说就是  如果不是 GameObject  --- 直接卸载
- 通知 Bundle 尝试卸载对应的 bundle

```c#
/// <summary>
/// 卸载资源
/// </summary>
internal override void UnLoad()
{
	if (bundle == null)
		throw new Exception($"{nameof(Resource)}.{nameof(UnLoad)}() {nameof(bundle)} is null.");

	if (asset != null && !(asset is GameObject))
	{
		Resources.UnloadAsset(asset);
		asset = null;
	}

	BundleManager.instance.UnLoad(bundle); 

	bundle = null;
	awaiter = null;
	finishedCallback = null;
}
```