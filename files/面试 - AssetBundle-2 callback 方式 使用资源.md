---
tags:
  - 面试
---




## callback 方式解包

###  1. 一些初始化 如路径和平台

```c#
private string PrefixPath { get; set; }
private string Platform { get; set; }

private void Start()
{
	Platform = GetPlatform();
	PrefixPath = Path.GetFullPath(Path.Combine(Application.dataPath, "../../AssetBundle")).Replace("\\", "/");
	PrefixPath += $"/{Platform}";
	ResourceManager.instance.Initialize(GetPlatform(), GetFileUrl, false, 0);

	Initialize();
}

private string GetPlatform()
{
	switch (Application.platform)
	{
		case RuntimePlatform.WindowsEditor:
		case RuntimePlatform.WindowsPlayer:
			return "Windows";
		case RuntimePlatform.Android:
			return "Android";
		case RuntimePlatform.IPhonePlayer:
			return "iOS";
		default:
			throw new System.Exception($"未支持的平台:{Application.platform}");
	}
}
private string GetFileUrl(string assetUrl) // 返回真实路径的回调函数
{
	return $"{PrefixPath}/{assetUrl}";
}

```


### 2. 场景初始化

使用 callback 初始化

让 ResourceManager 进行加载，我们只需要传入 callback 将加载后的资源进行使用就可以了

```c#
private void Initialize()
{
// uiRootResource --- 就是我们那拿到的资源
	ResourceManager.instance.LoadWithCallback("Assets/AssetBundle/UI/UIRoot.prefab", true, uiRootResource => 
	{
		uiRootResource.Instantiate();

		Transform uiParent = GameObject.Find("Canvas").transform;

		ResourceManager.instance.LoadWithCallback("Assets/AssetBundle/UI/TestUI.prefab", true, testUIResource =>
		{
			testUIResource.Instantiate(uiParent, false);
		});
	});
}


```