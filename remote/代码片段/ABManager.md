```c#
using System.Collections;
using System.Collections.Generic;
using Unity.VisualScripting;
using UnityEngine;
using UnityEngine.Events;



public class ABManager : MonoBehaviour
{

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


    #region LoadRes
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
    #endregion



    #region LoadRes Async
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
    #endregion

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

    void Awake()
    {
        if (Instance == null){
            Instance = this;
        }else{
            Destroy(this);
        }
    }
    
    #region private Function
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
    #endregion

}
```