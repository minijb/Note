---
tags:
  - 面试
---
## StopWatch 

提供一组方法和属性，可用于准确地测量运行时间。

## Profiler

作用： 用于记录处理完成的时间，

使用stack做类似于广度遍历的的搜索，根据层级输出时间

## 打包的具体步骤

### 1. 切换对应平台的平台

```c#
/// <summary>
/// 切换平台
/// </summary> 
public static void SwitchPlatform()
{
	string platform = PLATFORM;

	switch (platform)
	{
		case "windows":
			EditorUserBuildSettings.SwitchActiveBuildTarget(BuildTargetGroup.Standalone, BuildTarget.StandaloneWindows64);
			break;
		case "ios":
			EditorUserBuildSettings.SwitchActiveBuildTarget(BuildTargetGroup.iOS, BuildTarget.iOS);
			break;
		case "android":
			EditorUserBuildSettings.SwitchActiveBuildTarget(BuildTargetGroup.Android, BuildTarget.Android);
			break;
	}
}
```


### 2. 使用xml 解析 buildsetting.xml 文件

```c#
public static BuildSetting LoadSetting(string settingPath)
{
	buildSetting = XmlUtility.Read<BuildSetting>(settingPath);
	if (buildSetting == null)
	{
		throw new Exception($"Load buildSetting failed, Setting path : {settingPath}");
	}

	(buildSetting as ISupportInitialize)?.EndInit(); // 后处理

	buildPath = Path.GetFullPath(buildSetting.buildRoot).Replace("\\", "/");
	if (buildPath.Length > 0 && buildPath[buildPath.Length - 1] != '/')
	{
		buildPath += "/";
	}

	buildPath += $"{PLATFORM}/";


	return buildSetting;
}
```


### 3. collect 文件信息收集阶段 并根据收集到的信息生成 bundle


[[面试 - AssetBundle-1#1. 收集直接资源 -- 非依赖资|1. 收集直接资源 -- 非依赖资]]
[[面试 - AssetBundle-1#2. 收集依赖信息|2. 收集依赖信息]]
#### 3.1  收集直接资源 -- 非依赖资源

```c#
HashSet<string> files = buildSetting.Collect(); // 得到所有符合条件的 file 1. 前后缀符合， 2. 不符合忽略路径 

// hashset --- 中存放左右直接需求的文件，

/// <summary>
/// 获取所有在打包设置的文件列表 
/// </summary>
/// <returns>文件列表</returns>
public HashSet<string> Collect()
{
	// 设置进度条
	float min = Builder.collectRuleFileProgress.x;
	float max = Builder.collectRuleFileProgress.y;

	EditorUtility.DisplayProgressBar($"{nameof(Collect)}", "搜集打包规则资源", min);

	//处理每个规则忽略的目录,如路径A/B/C,需要忽略A/B
	for (int i = 0; i < items.Count; i++)
	{
		BuildItem buildItem_i = items[i];

		if (buildItem_i.resourceType != EResourceType.Direct) // 目标资源不是 直接资源, 而是依赖 则 --- 忽略
			continue;

		buildItem_i.ignorePaths.Clear();
		for (int j = 0; j < items.Count; j++)
		{
			BuildItem buildItem_j = items[j];
			if (i != j && buildItem_j.resourceType == EResourceType.Direct) // j 也是直接资源
			{
				if (buildItem_j.assetPath.StartsWith(buildItem_i.assetPath, StringComparison.InvariantCulture)) // 第二个参数表示 是否忽略大小写，同时确定文字的区域
				{
					buildItem_i.ignorePaths.Add(buildItem_j.assetPath);
				}
			}
		}
	}

	//存储被规则分析到的所有文件
	// NOTE : IMPORTANT
	HashSet<string> files = new HashSet<string>();

	for (int i = 0; i < items.Count; i++)
	{
		BuildItem buildItem = items[i];

		EditorUtility.DisplayProgressBar($"{nameof(Collect)}", "搜集打包规则资源", min + (max - min) * ((float)i / (items.Count - 1)));

		if (buildItem.resourceType != EResourceType.Direct)
			continue;
		// 得到指定路径下的文件 -- 根据前后缀判定符合的结果
		List<string> tempFiles = Builder.GetFiles(buildItem.assetPath, null, buildItem.suffixes.ToArray());
		for (int j = 0; j < tempFiles.Count; j++) // 是否需要被忽略
		{
			string file = tempFiles[j];

			//过滤被忽略的
			if (IsIgnore(buildItem.ignorePaths, file))
				continue;

			files.Add(file);
		}

		EditorUtility.DisplayProgressBar($"{nameof(Collect)}", "搜集打包设置资源", (float)(i + 1) / items.Count);
	}

	return files;

}


```


**简单步骤**

1. 查看是否含有重复目录，
2. 根据前缀后缀---将符合条件的文件放入 hashset中


##### 如何 getfiles

1. 使用 Directory.GetFile 获得目录下所有文件
2. 根据前后缀判断文件是否符合要求

```c#
/// <summary>
/// 获取指定路径的文件
/// </summary>
/// <param name="path">指定路径</param>
/// <param name="prefix">前缀</param>
/// <param name="suffixes">后缀集合</param>
/// <returns>文件列表</returns>
public static List<string> GetFiles(string path, string prefix, params string[] suffixes)
{

	string[] files = Directory.GetFiles(path, $"*.*", SearchOption.AllDirectories); // 得到所有文件路径
	List<string> result = new List<string>(files.Length); // 初始化列表


	for (int i = 0; i < files.Length; ++i)
	{
		string file = files[i].Replace('\\', '/');

		// 处理前缀  忽略没有 已 prefix 为前缀的文件
		if (prefix != null && !file.StartsWith(prefix, StringComparison.InvariantCulture))
		{
			continue;
		}

		// 处理后缀  1.符合后缀的添加到结果列表 2. .meta 结尾的忽略
		if (suffixes != null && suffixes.Length > 0) 
		{
			bool exist = false;

			// 符合任意一个后缀则通过
			for (int ii = 0; ii < suffixes.Length; ii++)
			{
				string suffix = suffixes[ii];
				if (file.EndsWith(suffix, StringComparison.InvariantCulture))
				{
					exist = true;
					break;
				}
			}

			if (!exist)
				continue;
		}

		result.Add(file);
	}

	return result;
}
```

#### 3.2 收集依赖信息 


1. hashset - files => list - files
2. 利用 `AssetDatabase.GetDependencies(url, is recursive)` ---  会得到列表
3. 过滤 依赖列表 --- fileList 需要的文件列表  denpendency list 依赖别表
	1. cs, dll 代码文件 不需要
	2. dependency List --- 添加
	3. 如果不在文件列表  添加
	4. **结束后** fileList 中 添加了依赖文件， 返回依赖字典 --- `<asseturl(string), depdencyList(list)>`

```c#
/// <summary>
/// 收集指定文件集合所有的依赖信息
/// </summary>
/// <param name="files">文件集合</param>
/// <returns>依赖信息</returns>
private static Dictionary<string, List<string>> CollectDependency(ICollection<string> files)
{

	float min = ms_GetDependencyProgress.x;
	float max = ms_GetDependencyProgress.y;

	Dictionary<string, List<string>> dependencyDic = new Dictionary<string, List<string>>();

	//声明fileList后，就不需要递归了
	List<string> fileList = new List<string>(files);

	for (int i = 0; i < fileList.Count; i++)
	{

		string assetUrl = fileList[i];

		if (dependencyDic.ContainsKey(assetUrl)) // 依赖已经存在 --- 忽略
			continue;


		if (i % 10 == 0) // 进度模拟
		{
			//只能大概模拟进度
			float progress = min + (max - min) * ((float)i / (files.Count * 3));
			EditorUtility.DisplayProgressBar($"{nameof(CollectDependency)}", "搜集依赖信息", progress);
		}

		string[] dependencies = AssetDatabase.GetDependencies(assetUrl, false); // 得到依赖列表
		List<string> dependencyList = new List<string>(dependencies.Length);

		//过滤掉不符合要求的asset
		for (int ii = 0; ii < dependencies.Length; ii++)
		{
			string tempAssetUrl = dependencies[ii];
			string extension = Path.GetExtension(tempAssetUrl).ToLower();
			if (string.IsNullOrEmpty(extension) || extension == ".cs" || extension == ".dll") // c# 代码忽略
				continue;
			dependencyList.Add(tempAssetUrl);
			if (!fileList.Contains(tempAssetUrl))
				fileList.Add(tempAssetUrl);
		}

		dependencyDic.Add(assetUrl, dependencyList); // 资源对应的资源列表

	}

	return dependencyDic;


}
```


#### 3.3 将目标资源进行分类标记

此时资源有两个： 
1. hashset --  files **所有**需要的文件列表
2. dependencyDic -- **依赖字典**
3. 生成 -- assetDic -- **所有**资源的资源类型(直接资源，依赖资源)

```c#
//标记所有资源的信息
Dictionary<string, EResourceType> assetDic = new Dictionary<string, EResourceType>();

//被打包配置分析到的直接设置为Direct --- 直接获取的资源
foreach (string url in files)
{
	assetDic.Add(url, EResourceType.Direct);
}

//依赖的资源标记为Dependency，已经存在的说明是Direct的资源 --- 依赖资源
foreach (string url in dependencyDic.Keys)
{
	if (!assetDic.ContainsKey(url))
	{
		assetDic.Add(url, EResourceType.Dependency);
	}
}
```

#### 3.4 处理 bundle 信息

这里将资源分为两种 : bundle资源 - 外部资源  返回 `bundle dic < bundle name , path url of asset>` 

**处理所有文件信息**

1. 处理资源并生成 包名  ---[[面试 - AssetBundle-1#根据 asseturl 得到 bundle name|getBundle Name]]  --- **针对assetDic** --- **所有**资源对应资源类型
	1. 没有名字 则是外部资源
2. 根据 bundle name 对资源进行分类
	1. 存放到 bundleDic 点中， bundle_Name --- List(string of asset path)
3. 如果有外部资源 报错， 随后进行排序

**生成 bundle_dic** --- `bundle_name,  list(string)(asset path)`

```c#
/// <summary>
/// 搜集bundle对应的ab名字
/// </summary>
/// <param name="buildSetting"></param>
/// <param name="assetDic">资源列表</param>
/// <param name="dependencyDic">资源依赖信息</param>
/// <returns>bundle包信息</returns>
private static Dictionary<string, List<string>> CollectBundle(BuildSetting buildSetting, Dictionary<string, EResourceType> assetDic, Dictionary<string, List<string>> dependencyDic)
{
	float min = ms_CollectBundleInfoProgress.x;
	float max = ms_CollectBundleInfoProgress.y;

	EditorUtility.DisplayProgressBar($"{nameof(CollectBundle)}", "搜集bundle信息", min);


	Dictionary<string, List<string>> bundleDic = new Dictionary<string, List<string>>(); // 用于记录
	//外部资源
	List<string> notInRuleList = new List<string>();

	// --------------------------------------- 处理直接资源 bundle -----------------------------------------
	int index = 0;
	foreach (KeyValuePair<string, EResourceType> pair in assetDic)
	{
		index++;
		string assetUrl = pair.Key;
		string bundleName = buildSetting.GetBundleName(assetUrl, pair.Value);

		//没有bundleName的资源为外部资源
		if (bundleName == null)
		{
			notInRuleList.Add(assetUrl);
			continue;
		}

		List<string> list;
		if (!bundleDic.TryGetValue(bundleName, out list)) // 找不到 则加入资源
		{
			list = new List<string>();
			bundleDic.Add(bundleName, list);
		}

		list.Add(assetUrl);

		EditorUtility.DisplayProgressBar($"{nameof(CollectBundle)}", "搜集bundle信息", min + (max - min) * ((float)index / assetDic.Count));
	}

	//存在外部资源 ---- 生成异常消息
	if (notInRuleList.Count > 0)
	{
		string massage = string.Empty;
		for (int i = 0; i < notInRuleList.Count; i++)
		{
			massage += "\n" + notInRuleList[i];
		}
		EditorUtility.ClearProgressBar();
		throw new Exception($"资源不在打包规则,或者后缀不匹配！！！{massage}");
	}

	//排序
	foreach (List<string> list in bundleDic.Values)
	{
		list.Sort();
	}

	return bundleDic;
}
```


##### 根据 asseturl 得到 bundle name

1. 根据 url 匹配已经需要打包的 item --- url 越长 优先级越高 --- 也就是说明越匹配
2. 如果没有匹配 return null
3. 如果资源是依赖类型的
	1. 当前资源的后缀应该匹配 item 内的后缀类型 --- 才可以进行打包
4. 根据资源的类型进行处理
	1. all ： name 就是 assetPath.ab
	2. Directory : 文件的最后的文件夹.ab
	3. file : 文件路径.ab


```c#
/// <summary>
/// 获取BundleName
/// </summary>
/// <param name="assetUrl">资源路径</param>
/// <param name="resourceType">资源类型</param>
/// <returns>BundleName</returns>
public string GetBundleName(string assetUrl, EResourceType resourceType)
{
	BuildItem buildItem = GetBuildItem(assetUrl); // ========================== 1 =========================

	if (buildItem == null)
	{
		return null;
	}

	string name;

	//依赖类型一定要匹配后缀
	if (buildItem.resourceType == EResourceType.Dependency) // 依赖 -- 匹配后缀
	{
		string extension = Path.GetExtension(assetUrl).ToLower();
		bool exist = false;
		for (int i = 0; i < buildItem.suffixes.Count; i++)
		{
			if (buildItem.suffixes[i] == extension) // 后缀等于扩展 
			{
				exist = true;
			}
		}

		if (!exist)
		{
			return null;
		}
	}

	switch (buildItem.bundleType)
	{
		case EBundleType.All:
			name = buildItem.assetPath;
			if (buildItem.assetPath[buildItem.assetPath.Length - 1] == '/')
				name = buildItem.assetPath.Substring(0, buildItem.assetPath.Length - 1);
			name = $"{name}{Builder.BUNDLE_SUFFIX}".ToLowerInvariant();
			break;
		case EBundleType.Directory:
			name = $"{assetUrl.Substring(0, assetUrl.LastIndexOf('/'))}{Builder.BUNDLE_SUFFIX}".ToLowerInvariant();
			break;
		case EBundleType.File:
			name = $"{assetUrl}{Builder.BUNDLE_SUFFIX}".ToLowerInvariant();
			break;
		default:
			throw new Exception($"无法获取{assetUrl}的BundleName");
	}

	buildItem.Count += 1;

	return name;
}

/// <summary>
/// 通过资源获取打包选项
/// </summary>
/// <param name="assetUrl">资源路径</param>
/// <returns>打包选项</returns>
public BuildItem GetBuildItem(string assetUrl)
{
	BuildItem item = null;
	for (int i = 0; i < items.Count; ++i)
	{
		BuildItem tempItem = items[i];
		//前面是否匹配
		if (assetUrl.StartsWith(tempItem.assetPath, StringComparison.InvariantCulture))
		{
			//找到优先级最高的Rule,路径越长说明优先级越高
			if (item == null || item.assetPath.Length < tempItem.assetPath.Length)
			{
				item = tempItem;
			}
		}
	}

	return item;
}
```
#### 3.5 生成 manifest 临时文件

1. 找到 temp 文件夹
2. assetIDDic --- 资源映射 ID
3. 


```c#
/// <summary>
/// 生成资源描述文件
/// <param name="assetDic">资源列表</param>
/// <param name="bundleDic">bundle包信息</param>
/// <param name="dependencyDic">资源依赖信息</param>
/// </summary>
private static void GenerateManifest(Dictionary<string, EResourceType> assetDic, Dictionary<string, List<string>> bundleDic, Dictionary<string, List<string>> dependencyDic)
{

	float min = ms_GenerateBuildInfoProgress.x;
	float max = ms_GenerateBuildInfoProgress.y;

	EditorUtility.DisplayProgressBar($"{nameof(GenerateManifest)}", "生成打包信息", min);

	//生成临时存放文件的目录
	if (!Directory.Exists(TempPath))
		Directory.CreateDirectory(TempPath);


	//资源映射id
	Dictionary<string, ushort> assetIdDic = new Dictionary<string, ushort>();

	/// <summary>
	///  1. 先删除  资源描述文件 + 二进制文件
	/// </summary>
	#region 生成资源描述信息
	{
		//删除资源描述文本文件
		if (File.Exists(ResourcePath_Text))
			File.Delete(ResourcePath_Text);

		//删除资源描述二进制文件
		if (File.Exists(ResourcePath_Binary))
			File.Delete(ResourcePath_Binary);

		//写入资源列表
		StringBuilder resourceSb = new StringBuilder();
		MemoryStream resourceMs = new MemoryStream();
		BinaryWriter resourceBw = new BinaryWriter(resourceMs);
		if (assetDic.Count > ushort.MaxValue)
		{
			EditorUtility.ClearProgressBar();
			throw new Exception($"资源个数超出{ushort.MaxValue}");
		}

		//写入个数
		resourceBw.Write((ushort)assetDic.Count);
		List<string> keys = new List<string>(assetDic.Keys);
		keys.Sort();

		for (ushort i = 0; i < keys.Count; i++)
		{
			string assetUrl = keys[i];
			assetIdDic.Add(assetUrl, i);
			resourceSb.AppendLine($"{i}\t{assetUrl}");
			resourceBw.Write(assetUrl);
		}

		resourceMs.Flush();
		byte[] buffer = resourceMs.GetBuffer();
		resourceBw.Close();
		//写入资源描述文本文件
		File.WriteAllText(ResourcePath_Text, resourceSb.ToString(), Encoding.UTF8);
		File.WriteAllBytes(ResourcePath_Binary, buffer);
	}
	#endregion

	EditorUtility.DisplayProgressBar($"{nameof(GenerateManifest)}", "生成打包信息", min + (max - min) * 0.3f);


	#region 生成bundle描述信息
	{

	}
	#endregion

	EditorUtility.DisplayProgressBar($"{nameof(GenerateManifest)}", "生成打包信息", min + (max - min) * 0.8f);

	#region 生成资源依赖描述信息
	{

	}
	#endregion
	AssetDatabase.Refresh();

	EditorUtility.DisplayProgressBar($"{nameof(GenerateManifest)}", "生成打包信息", max);

	EditorUtility.ClearProgressBar();
}

```


##### 3.5.1 生成资源描述信息

先清楚文件 ， 然后根据 assetDic 资源对应 资源类型 ， 生成assetIDDic 的内容， 并写入资源描述信息

```c#
{
	//删除资源描述文本文件
	if (File.Exists(ResourcePath_Text))
		File.Delete(ResourcePath_Text);

	//删除资源描述二进制文件
	if (File.Exists(ResourcePath_Binary))
		File.Delete(ResourcePath_Binary);

	//写入资源列表
	StringBuilder resourceSb = new StringBuilder();
	MemoryStream resourceMs = new MemoryStream();
	BinaryWriter resourceBw = new BinaryWriter(resourceMs);
	if (assetDic.Count > ushort.MaxValue)
	{
		EditorUtility.ClearProgressBar();
		throw new Exception($"资源个数超出{ushort.MaxValue}");
	}

	//写入个数
	resourceBw.Write((ushort)assetDic.Count);
	List<string> keys = new List<string>(assetDic.Keys);
	keys.Sort();

	for (ushort i = 0; i < keys.Count; i++)
	{
		string assetUrl = keys[i];
		assetIdDic.Add(assetUrl, i);
		resourceSb.AppendLine($"{i}\t{assetUrl}");
		resourceBw.Write(assetUrl);
	}

	resourceMs.Flush();
	byte[] buffer = resourceMs.GetBuffer();
	resourceBw.Close();
	//写入资源描述文本文件
	File.WriteAllText(ResourcePath_Text, resourceSb.ToString(), Encoding.UTF8);
	File.WriteAllBytes(ResourcePath_Binary, buffer);
}
```


```txt
0	Assets/AssetBundle/Atlas/Role/Hog_Attack_000.png
1	Assets/AssetBundle/Atlas/Role/Hog_Attack_001.png
2	Assets/AssetBundle/Atlas/Role/Hog_Attack_002.png
3	Assets/AssetBundle/Atlas/Role/Hog_Attack_003.png
4	Assets/AssetBundle/Atlas/Role/Hog_Attack_004.png
5	Assets/AssetBundle/Atlas/Role/Hog_Attack_005.png
6	Assets/AssetBundle/Atlas/Role/Hog_Attack_006.png
7	Assets/AssetBundle/Atlas/Role/Hog_Attack_007.png
8	Assets/AssetBundle/Atlas/Role/Hog_Attack_008.png
9	Assets/AssetBundle/Atlas/Role/Hog_Attack_009.png
10	Assets/AssetBundle/Atlas/Role/Hog_Attack_010.png
11	Assets/AssetBundle/Atlas/Role/Hog_Attack_011.png
12	Assets/AssetBundle/Background/1.png
13	Assets/AssetBundle/Background/2.png
14	Assets/AssetBundle/Background/3.png
15	Assets/AssetBundle/Background/4.png
16	Assets/AssetBundle/Background/5.png

```

##### 3.5.2 生成bundle描述信息

bundleDic Bundle - 资源路径列表

写入 bundle 对应的资源列表

这里二进制文件使用 ID ---- 减少内存消耗

```c#
{
	//删除bundle描述文本文件
	if (File.Exists(BundlePath_Text))
		File.Delete(BundlePath_Text);

	//删除bundle描述二进制文件
	if (File.Exists(BundlePath_Binary))
		File.Delete(BundlePath_Binary);

	//写入bundle信息
	StringBuilder bundleSb = new StringBuilder();
	MemoryStream bundleMs = new MemoryStream();
	BinaryWriter bundleBw = new BinaryWriter(bundleMs);

	//写入bundle个数
	bundleBw.Write((ushort)bundleDic.Count);
	foreach (var kv in bundleDic)
	{
		string bundleName = kv.Key;
		List<string> assets = kv.Value;

		//写入bundle
		bundleSb.AppendLine(bundleName);
		bundleBw.Write(bundleName);

		//写入资源个数
		bundleBw.Write((ushort)assets.Count);

		for (int i = 0; i < assets.Count; i++)
		{
			string assetUrl = assets[i];
			ushort assetId = assetIdDic[assetUrl];
			bundleSb.AppendLine($"\t{assetUrl}");
			//写入资源id,用id替换字符串可以节省内存
			bundleBw.Write(assetId);
		}
	}

	bundleMs.Flush();
	byte[] buffer = bundleMs.GetBuffer();
	bundleBw.Close();
	//写入资源描述文本文件
	File.WriteAllText(BundlePath_Text, bundleSb.ToString(), Encoding.UTF8);
	File.WriteAllBytes(BundlePath_Binary, buffer);
}
```


```txt
assets/assetbundle/common/model.rendertexture.ab
	Assets/AssetBundle/Common/Model.renderTexture
assets/assetbundle/atlas/role.ab
	Assets/AssetBundle/Atlas/Role/Hog_Attack_000.png
	Assets/AssetBundle/Atlas/Role/Hog_Attack_001.png
	Assets/AssetBundle/Atlas/Role/Hog_Attack_002.png
	Assets/AssetBundle/Atlas/Role/Hog_Attack_003.png
	Assets/AssetBundle/Atlas/Role/Hog_Attack_004.png
	Assets/AssetBundle/Atlas/Role/Hog_Attack_005.png
	Assets/AssetBundle/Atlas/Role/Hog_Attack_006.png
	Assets/AssetBundle/Atlas/Role/Hog_Attack_007.png
	Assets/AssetBundle/Atlas/Role/Hog_Attack_008.png
	Assets/AssetBundle/Atlas/Role/Hog_Attack_009.png
	Assets/AssetBundle/Atlas/Role/Hog_Attack_010.png
	Assets/AssetBundle/Atlas/Role/Hog_Attack_011.png
assets/assetbundle/background/1.png.ab
	Assets/AssetBundle/Background/1.png
assets/assetbundle/background/2.png.ab
	Assets/AssetBundle/Background/2.png
assets/assetbundle/background/3.png.ab
	Assets/AssetBundle/Background/3.png
assets/assetbundle/background/4.png.ab
	Assets/AssetBundle/Background/4.png

```


##### 3.5.3 生成依赖描述信息

根据资源依赖字典 生成依赖信息

- 如果没有依赖不写
- **规则： 使用的资源 + 依赖资源(使用\t间隔)**
- 二进制书写： 一个单元 ： 个数 + 元素列表



```c#
{
	//删除资源依赖描述文本文件
	if (File.Exists(DependencyPath_Text))
		File.Delete(DependencyPath_Text);

	//删除资源依赖描述二进制文件
	if (File.Exists(DependencyPath_Binary))
		File.Delete(DependencyPath_Binary);

	//写入资源依赖信息
	StringBuilder dependencySb = new StringBuilder();
	MemoryStream dependencyMs = new MemoryStream();
	BinaryWriter dependencyBw = new BinaryWriter(dependencyMs);

	//用于保存资源依赖链
	List<List<ushort>> dependencyList = new List<List<ushort>>();
	foreach (var kv in dependencyDic)
	{
		List<string> dependencyAssets = kv.Value;

		//依赖为0的不需要写入
		if (dependencyAssets.Count == 0)
			continue;

		string assetUrl = kv.Key;

		List<ushort> ids = new List<ushort>();
		ids.Add(assetIdDic[assetUrl]);

		string content = assetUrl;
		for (int i = 0; i < dependencyAssets.Count; i++)
		{
			string dependencyAssetUrl = dependencyAssets[i];
			content += $"\t{dependencyAssetUrl}";
			ids.Add(assetIdDic[dependencyAssetUrl]);
		}

		dependencySb.AppendLine(content);

		if (ids.Count > byte.MaxValue)
		{
			EditorUtility.ClearProgressBar();
			throw new Exception($"资源{assetUrl}的依赖超出一个字节上限:{byte.MaxValue}");
		}

		dependencyList.Add(ids);
	}

	//写入依赖链个数
	dependencyBw.Write((ushort)dependencyList.Count);
	for (int i = 0; i < dependencyList.Count; i++)
	{
		//写入资源数
		List<ushort> ids = dependencyList[i];
		dependencyBw.Write((ushort)ids.Count);
		for (int ii = 0; ii < ids.Count; ii++)
			dependencyBw.Write(ids[ii]);
	}

	dependencyMs.Flush();
	byte[] buffer = dependencyMs.GetBuffer();
	dependencyBw.Close();
	//写入资源依赖描述文本文件
	File.WriteAllText(DependencyPath_Text, dependencySb.ToString(), Encoding.UTF8);
	File.WriteAllBytes(DependencyPath_Binary, buffer);
}
```

```txt
Assets/AssetBundle/Model/Ji.prefab	Assets/AssetBundle/Model/ji/ji_02.fbx	Assets/AssetBundle/Model/ji/cai/lambert2.mat	Assets/AssetBundle/Model/ji_02.controller
Assets/AssetBundle/UI/TestUI.prefab	Assets/AssetBundle/Atlas/Role/Hog_Attack_011.png	Assets/AssetBundle/Common/Model.renderTexture	Assets/AssetBundle/Icon/1.png	Assets/AssetBundle/Background/6.png
Assets/AssetBundle/UI/Test/TestUI.prefab	Assets/AssetBundle/Common/Model.renderTexture
Assets/AssetBundle/Model/ji/cai/lambert2.mat	Assets/AssetBundle/Model/ji/cai/CAIXUK.png
Assets/AssetBundle/Model/ji_02.controller
```

### 4. 打包 generate bundle

**重点： BuildPipeline.BuildAssetBundles** 使用APi 进行打包
https://docs.unity3d.com/ScriptReference/BuildPipeline.BuildAssetBundles.html


`public static AssetBundleManifest BuildAssetBundles(string outputPath, AssetBundleBuild[] builds, BuildAssetBundleOptions assetBundleOptions, BuildTarget targetPlatform);`

Parameters

|                    |                                   |                            |
| ------------------ | --------------------------------- | -------------------------- |
| outputPath         | Output path for the AssetBundles. | 输出目录                       |
| builds             | AssetBundle building map.         | AssetBundleBuild[]  一个资源列表 |
| assetBundleOptions | AssetBundle building options.     | build 选项                   |
| targetPlatform     | Target build platform.            | 平台                         |
输出 manifest

#### 4.1 生成 AssetBundleBuild[]

直接从 bundleTable 中得到名字

```c#
/// <summary>
/// 获取所有需要打包的AssetBundleBuild
/// </summary>
/// <param name="bundleTable">bunlde信息</param>
/// <returns></returns>
private static AssetBundleBuild[] GetBuilds(Dictionary<string, List<string>> bundleTable)
{
	int index = 0;
	AssetBundleBuild[] assetBundleBuilds = new AssetBundleBuild[bundleTable.Count];
	foreach (KeyValuePair<string, List<string>> pair in bundleTable)
	{
		assetBundleBuilds[index++] = new AssetBundleBuild()
		{
			assetBundleName = pair.Key,
			assetNames = pair.Value.ToArray(),
		};
	}

	return assetBundleBuilds;
}

```


### 5. 清楚多余的asset bundle

删除 manifest.ab !!!!!

具体步骤
- 得到 文件 set
- 对于 文件.ab .manifest 不删除
- 对于 总的 .manifest 不删除
- 剩余的就是多余的 bundle


```c#
/// <summary>
/// 清空多余的assetbundle
/// </summary>
/// <param name="path">打包路径</param>
/// <param name="bundleDic"></param>
private static void ClearAssetBundle(string path, Dictionary<string, List<string>> bundleDic)
{
	float min = ms_ClearBundleProgress.x;
	float max = ms_ClearBundleProgress.y;

	EditorUtility.DisplayProgressBar($"{nameof(ClearAssetBundle)}", "清除多余的AssetBundle文件", min);

	List<string> fileList = GetFiles(path, null, null);
	HashSet<string> fileSet = new HashSet<string>(fileList);

	foreach (string bundle in bundleDic.Keys)
	{
		fileSet.Remove($"{path}{bundle}");
		fileSet.Remove($"{path}{bundle}{BUNDLE_MANIFEST_SUFFIX}");
	}
	// 移除 manifest 的原因是 --- 保证热更新  防止更新所有的依赖

	fileSet.Remove($"{path}{PLATFORM}");
	fileSet.Remove($"{path}{PLATFORM}{BUNDLE_MANIFEST_SUFFIX}");

	Parallel.ForEach(fileSet, ParallelOptions, File.Delete); // 并行运行

	EditorUtility.DisplayProgressBar($"{nameof(ClearAssetBundle)}", "清除多余的AssetBundle文件", max);
}
```


### 6. 自定义 需要的  manifest.ab 文件

使用自定义的 manifest 文件信息代替 打包

```c#
    /// <summary>
    /// 把Resource.bytes、bundle.bytes、Dependency.bytes 打包assetbundle
    /// </summary>
    private static void BuildManifest()
    {
        float min = ms_BuildManifestProgress.x;
        float max = ms_BuildManifestProgress.y;

        EditorUtility.DisplayProgressBar($"{nameof(BuildManifest)}", "将Manifest打包成AssetBundle", min);

        if (!Directory.Exists(TempBuildPath))
            Directory.CreateDirectory(TempBuildPath);

        string prefix = Application.dataPath.Replace("/Assets", "/").Replace("\\", "/");

        AssetBundleBuild manifest = new AssetBundleBuild(); // 添加新下 manifest
        manifest.assetBundleName = $"{MANIFEST}{BUNDLE_SUFFIX}";
        manifest.assetNames = new string[3]
        {
                ResourcePath_Binary.Replace(prefix,""),
                BundlePath_Binary.Replace(prefix,""),
                DependencyPath_Binary.Replace(prefix,""),
        };

        EditorUtility.DisplayProgressBar($"{nameof(BuildManifest)}", "将Manifest打包成AssetBundle", min + (max - min) * 0.5f);

        AssetBundleManifest assetBundleManifest = BuildPipeline.BuildAssetBundles(TempBuildPath, new AssetBundleBuild[] { manifest }, BuildAssetBundleOptions, EditorUserBuildSettings.activeBuildTarget);

        //把文件copy到build目录
        if (assetBundleManifest)
        {
            string manifestFile = $"{TempBuildPath}/{MANIFEST}{BUNDLE_SUFFIX}";
            string target = $"{buildPath}/{MANIFEST}{BUNDLE_SUFFIX}";
            if (File.Exists(manifestFile))
            {
                File.Copy(manifestFile, target);
            }
        }

        //删除临时目录
        if (Directory.Exists(TempBuildPath))
            Directory.Delete(TempBuildPath, true);

        EditorUtility.DisplayProgressBar($"{nameof(BuildManifest)}", "将Manifest打包成AssetBundle", max);
    }

```


