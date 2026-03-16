---
tags:
  - unity
---
## install

 https://github.com/Unity-Technologies/AssetBundles-Browser.git


## 简单使用

在资源的右下角，输入名称就可以包含在一个包里。 --- 不能将代码打包。


**Asset Bundle** 窗口

- Build
	- build target 打包的目标平台
	- clear folder / copy to streamingAsset --- 推荐勾选
	- 推荐使用  LZ4 压缩方式
		- LZMA : 最小的，但是解压麻烦，用一个资源要全部解压
		- LZ4 ： 用啥解压啥

打包结构：
- 主包：包含很多关键信息，如依赖关系
- 其他的资源文件
- manifest : 配置文件 如版本依赖等


**加载资源**

```c#
void Start()
{
	AssetBundle ab = AssetBundle.LoadFromFile(Application.streamingAssetsPath + "/" + "model");
	GameObject obj = ab.LoadAsset<GameObject>("Cube");
	// GameObject obj = ab.LoadAsset("Cube", typeof(GameObject)) as GameObject; // 在lua中的时候，没有泛型，只能使用这种方法
	Instantiate(obj, transform);

	// 同一个 包 不能重复加载，否则报错
	// AssetBundle ab = AssetBundle.LoadFromFile(Application.streamingAssetsPath + "/" + "model");
	
}
```


**异步加载**

```c#
IEnumerator LoadABRes(string ABName, string resName){

	// 加载 ab 包
	AssetBundleCreateRequest ab = AssetBundle.LoadFromFileAsync(Application.streamingAssetsPath + "/" + ABName);
	yield return ab;

	// 加载资源
	AssetBundleRequest abq = ab.assetBundle.LoadAssetAsync(resName, typeof(GameObject));
	yield return abq;

	GameObject obj = Instantiate(abq.asset as GameObject);
	obj.transform.SetParent(target);

	// (abq.asset as GameObject).transform.parent = target;

}
```

**卸载**

```c#
if(Input.GetKeyDown(KeyCode.Space)){
	AssetBundle.UnloadAllAssetBundles(false); // true 会将加载的资源一起卸载
	ab.Unload(false); // 单个包卸载，参数同上
}
```


## 依赖

一个资源使用的资源会被自动打包。

场景:

gameobject : cube -> M1 **in model**
Material : M1  **in model1**

此时仅仅加载 model ab包，那么 cube 是没有材质

**解决方案**
- 存在依赖的，放在一个包里面
- 同时加载多个ab包。

```c#
AssetBundle ab = AssetBundle.LoadFromFile(Application.streamingAssetsPath + "/" + "model");
AssetBundle ab1 = AssetBundle.LoadFromFile(Application.streamingAssetsPath + "/" + "model1");
GameObject obj = ab.LoadAsset<GameObject>("Cube");
// GameObject obj = ab.LoadAsset("Cube", typeof(GameObject)) as GameObject; // 在lua中的时候，没有泛型，只能使用这种方法
Instantiate(obj, transform);
```


- **利用主包获得依赖关系**！！！

```c#
   void Start()
    {
        AssetBundle ab = AssetBundle.LoadFromFile(Application.streamingAssetsPath+"/"+"model");
        
        // load main package
        AssetBundle ab_main = AssetBundle.LoadFromFile(Application.streamingAssetsPath+"/"+"PC");
        AssetBundleManifest abMainfest = ab_main.LoadAsset<AssetBundleManifest>("AssetBundleManifest"); // 得到固定文件
        string[] strs = abMainfest.GetAllDependencies("model"); // 得到依赖关系

        for(int i = 0 ; i < strs.Length ; i++){ // 记载依赖包
            Debug.Log(strs[i]);
            AssetBundle.LoadFromFile(Application.streamingAssetsPath+"/"+strs[i]);
        }

        GameObject obj = ab.LoadAsset<GameObject>("Cube");
        Instantiate(obj, transform);

        ab.Unload(false);
    }
```


### 管理器

### 同步加载


加载步骤

1. 加载 AB 包
**加载依赖**
3. 加载主包
4. 加载主包中的关键配置文件 --- 得到依赖包
5. 加载依赖包

私有方法

```c#
    private void loadMainPackage(){
        if (AB_main == null)
        { // 加载 主包 及其配置文件
            AB_main = AssetBundle.LoadFromFile(PathForAssertBundle + MainPackageNameForAssertBundle);
            manifest = AB_main.LoadAsset<AssetBundleManifest>("AssetBundleManifest");
        }
    }

    private void loadDependencyPackages(string abName){
        // 得到依赖包的名称
        string[] nameOfDependencys = manifest.GetAllDependencies(abName);

        for (int i = 0; i < nameOfDependencys.Length; i++)
        {
            if (!packageDic.ContainsKey(nameOfDependencys[i]))
            { // 还未加载包
                AssetBundle ab = AssetBundle.LoadFromFile(PathForAssertBundle + nameOfDependencys[i]);
                packageDic.Add(nameOfDependencys[i], ab);
            }
        }
    }

    private AssetBundle loadTargetPackage(string abName){
        // 加载目标包
        AssetBundle targetAssetBundlePackage = null;

        if (!packageDic.ContainsKey(abName))
        { // 没有加载包则加载包资源
            targetAssetBundlePackage = AssetBundle.LoadFromFile(PathForAssertBundle + abName);
            packageDic.Add(abName, targetAssetBundlePackage);
        }
        targetAssetBundlePackage = packageDic[abName];

        return targetAssetBundlePackage;
    }
```

属性，

主包： 
- 如果没有必须加载，同时只能存在一个，因此单独存储
- 使用字典存储 ab 包
- 单独存储路径

```c#
    public static ABManager Instance;

    private AssetBundle AB_main = null;
    private AssetBundleManifest manifest = null;
    private Dictionary<string, AssetBundle> packageDic = new Dictionary<string, AssetBundle>();

    /// <summary>
    ///  指向资源文件夹
    /// </summary>
    private string PathForAssertBundle
    {
        get
        {
            return Application.streamingAssetsPath + "/";
        }
    }

    /// <summary>
    ///  主包名称 
    /// </summary>
    /// <value></value>
    private string MainPackageNameForAssertBundle
    {
        get
        {
#if UNITY_IOS
                return "IOS";
#elif UNITY_ANDROID
                return "Android"
#else
            return "PC";
#endif
        }
    }
```

加载包资源

```c#
    public Object LoadRes(string abName, string resName)
    {
        loadMainPackage();

        loadDependencyPackages(abName);

        AssetBundle targetPackage = loadTargetPackage(abName);

        return targetPackage.LoadAsset(resName);
    }

    public Object LoadRes(string abName, string resName, System.Type type)
    {
        loadMainPackage();

        loadDependencyPackages(abName);

        AssetBundle targetPackage = loadTargetPackage(abName);

        return targetPackage.LoadAsset(resName, type);
    }

    public T LoadRes<T>(string abName, string resName) where T: Object
    {
        loadMainPackage();

        loadDependencyPackages(abName);

        AssetBundle targetPackage = loadTargetPackage(abName);

        return targetPackage.LoadAsset<T>(resName);
    }


    public void UnLoadPackage(string abName){
        if(packageDic.ContainsKey(abName)){
            packageDic[abName].Unload(false);
            packageDic.Remove(abName);
        }
    }

    public void UnLoadAllPackage(){
        AssetBundle.UnloadAllAssetBundles(false);
        packageDic.Clear();
        manifest = null;
        AB_main = null;
    }
```


**异步加载资源**

三种类型的异步加载

```c#
// 原始类型
    public void LoadResAsync(string abName, string resName, UnityAction<Object> callBack){
        StartCoroutine(LoadResAsync_IE(abName, resName, callBack));
    }



    private IEnumerator LoadResAsync_IE(string abName, string resName, UnityAction<Object> callBack){
        loadMainPackage();

        loadDependencyPackages(abName);

        AssetBundle targetPackage = loadTargetPackage(abName);

        AssetBundleRequest assetBundleRequest =  targetPackage.LoadAssetAsync(resName);

        yield return assetBundleRequest;
        //空的 在外部判断
        callBack(assetBundleRequest.asset);
    }


// 原始类型 ， 使用 参数 type
    public void LoadResAsync(string abName, string resName, System.Type type, UnityAction<Object> callBack){
        StartCoroutine(LoadResAsync_IE(abName, resName, type, callBack));
    }



    private IEnumerator LoadResAsync_IE(string abName, string resName, System.Type type, UnityAction<Object> callBack){
        loadMainPackage();

        loadDependencyPackages(abName);

        AssetBundle targetPackage = loadTargetPackage(abName);

        AssetBundleRequest assetBundleRequest =  targetPackage.LoadAssetAsync(resName, type);

        yield return assetBundleRequest;
        //空的 在外部判断
        callBack(assetBundleRequest.asset);
    }
    
// 使用泛型
    public void LoadResAsync<T>(string abName, string resName, UnityAction<T> callBack) where T : Object{
        StartCoroutine(LoadResAsync_IE<T>(abName, resName, callBack));
    }



    private IEnumerator LoadResAsync_IE<T>(string abName, string resName, UnityAction<T> callBack) where T : Object{
        loadMainPackage();

        loadDependencyPackages(abName);

        AssetBundle targetPackage = loadTargetPackage(abName);

        AssetBundleRequest assetBundleRequest =  targetPackage.LoadAssetAsync<T>(resName);

        yield return assetBundleRequest;
        //空的 在外部判断
        callBack(assetBundleRequest.asset as T);
    }
```