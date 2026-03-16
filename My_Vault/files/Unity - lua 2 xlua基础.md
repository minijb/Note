---
tags:
  - unity
  - lua
---
```c#
void Start()
{
	LuaEnv env = new LuaEnv(); // 推荐 全局唯一


	env.DoString("print('hello world')", "error");

	// 默认在 Resources.Load 进行加载， 文件： xxx.lua.txt
	env.DoString("require('Main')");

	env.Tick(); // 垃圾回收 ， 帧更新，或者加载的时候回收
	env.Dispose(); // 销毁
}
```


文件加载重定向

```c#
    void Start()
    {
        LuaEnv env = new LuaEnv(); // 推荐 全局唯一


        // env.DoString("print('hello world')", "error");

        env.AddLoader(MyLoader);
        // 默认在 Resources.Load 进行加载， 文件： xxx.lua.txt
        env.DoString("require('Main')");

        env.Tick(); // 垃圾回收 ， 帧更新，或者加载的时候回收
        env.Dispose(); // 销毁
    }

    private byte[] MyLoader(ref string filepath){
        string path = Application.dataPath + "/Lua/"+filepath+".lua";
        Debug.Log(path);

        if(File.Exists(path)){
            return File.ReadAllBytes(path);
        }else{
            Debug.LogError("can't find file");
        }
        return null;
    }
```


## Lua 解析器管理

```c#

    private byte[] AssetBundleLoader(ref string filepath){

        string AssetBundlePath = Application.streamingAssetsPath + "/lua";

        AssetBundle ab = AssetBundle.LoadFromFile(AssetBundlePath);
        TextAsset tx = ab.LoadAsset<TextAsset>(filepath+".lua");
        return tx.bytes;
    }
```


**属性**

```c#
    public static LuaManager instance {get; private set;}

    void Awake()
    {
        if(instance == null)
          instance = this;
        else
            Destroy(gameObject);
    }
    


    private LuaEnv luaEnv;
    public LuaTable Global{
        get {
            // 得到 _G
            if(luaEnv != null) return luaEnv.Global;
            else return null;
        }
    }
```

一些常用的函数

```c#
    public void Init(){
        if(luaEnv != null) return;
        luaEnv = new LuaEnv();
        luaEnv.AddLoader(FileLoader);
        luaEnv.AddLoader(AssetBundleLoader);
    }
    public void Tick(){
        if(luaEnv == null) return;
        luaEnv.Tick();
    }

    public void doString(string luaString){
        if(luaEnv == null) return;
        luaEnv.DoString(luaString);
    }

    public void doFile(string fileName){
        if(luaEnv == null) return;
        luaEnv.DoString("require('"+fileName+"')");
    }
```


**Loader**

```c#
    private byte[] FileLoader(ref string filepath){
        string path = Application.dataPath + "/Lua/"+filepath+".lua";
        Debug.Log(path);

        if(File.Exists(path)){
            return File.ReadAllBytes(path);
        }else{
            Debug.Log("can't find file in file lua");
        }
        return null;
    }

    private byte[] AssetBundleLoader(ref string filepath){

        //这里的文件名为  xxx.lua.txt
        TextAsset asset = ABManager.Instance.LoadRes<TextAsset>("lua", filepath+".lua");       

        if(asset != null){
            return asset.bytes;
        }else{
            Debug.Log("assetBundle 重定向失败");
        }
        return null;

    }
```


**asserBundle loader** 平常不用，只有打包之后才使用
**推荐制作小工具，用于把lua文件的东西转化到 ab包里**

> lua 内部使用 require 也会自动进行重定向


## c# 使用 lua 内的变量

```c#
LuaManager.instance.Init();
// LuaManager.instance.doString("require('Main')");
LuaManager.instance.doFile("Main");

int testNum = LuaManager.instance.Global.Get<int>("testNum"); //得到变量 --- 仅仅是复制
LuaManager.instance.Global.Set("testNum", 1000); // 设置变量

Debug.Log(testNum);
```


## c# 使用 lua 内的全局函数

```c#
    public delegate void CustomCall();

    [CSharpCallLua] // 需要点击 xlua 生成代码
    public delegate int d1(int a);
    [CSharpCallLua]
    public delegate int  d3(int a, out bool c, out int d);

    [CSharpCallLua]
    public delegate void  d4(int a, params object[] args); // 也可以是 固定类型
    // Start is called before the first frame update
    void Start()
    {
        LuaManager.instance.Init();
        LuaManager.instance.doFile("Main");
        
        // 无参无返回值 也可以使用 Action
        CustomCall call = LuaManager.instance.Global.Get<CustomCall>("testFun");
        // call();

        // 有参，有一个返回值
        //也可以使用 Func
        d1 call2 = LuaManager.instance.Global.Get<d1>("testFun2");
        Debug.Log(call2(100));
        LuaFunction lf = LuaManager.instance.Global.Get<LuaFunction>("testFun2");
        Debug.Log(lf.Call(30)[0]);




        // 多返回值 使用 out 和 ref 区别 out 需要初始化， ref 需要初始化， out 不需要 只需要声明
        d3 call3 = LuaManager.instance.Global.Get<d3>("testFun3");
        int c;
        bool ss;
        Debug.Log(call3(100,out ss,out c)); //默认返回第一个
        Debug.Log(""+  ss + c);// 剩下的 使用 out 捕获
        LuaFunction lf1 = LuaManager.instance.Global.Get<LuaFunction>("testFun3");
        object[] objs = lf1.Call(11);

        // 变长参数 同理 LuaFunction 也可以处理
        d4 call4 = LuaManager.instance.Global.Get<d4>("testFun4");
        call4(100,12,3,4,5);
    }
```


总结：
- 多参数 ： params object[] args
- 多返回 :  使用 out / ref
- LuaFunction : 都可以
- 自定义的委托需要生成 code

## table 映射

```c#
    void Start()
    {
        LuaManager.instance.Init();
        LuaManager.instance.doFile("Main");


        // 都是 值拷贝
        List<int> l = LuaManager.instance.Global.Get<List<int>>("tlist"); //浅拷贝

        foreach(int i in l){
            Debug.Log(i);
        }


        Dictionary<string, int> dic = LuaManager.instance.Global.Get<Dictionary<string, int>>("tDic"); //浅拷贝

        foreach(string i in dic.Keys){
            Debug.Log(i);
        }
    }
```


```lua
tlist = {1,2,3,4,5}
tlist2 = {1, ture , 3,5}

tDic = {
    ["1"] = 1,
    ["2"] = 2,
    ["3"] = 3,
    ["4"] = 4,
    ["5"] = 5,
}


tDic2 = {
    ["1"] = 1,
    [true] = 2,
    [false] = 3,
    ["4"] = true,
    ["5"] = 5,
}
```

- 不清楚类型 可以  Object
- 都是值拷贝

## 类/接口映射


```c#
// 属性多了少了都可以
// 命名必须一样, 多一些变量，少一些变量都可以
public class CallLuaClass{ // 值拷贝
    public int testInt;
    public bool testBool;
    public float testFloat;
    public string testString;


    public UnityAction func;
}

public interface CallInterface{ // 引用拷贝
	int testInt{get;set;}
	....
}


public class CSharpCallLua : MonoBehaviour
{

    void Start()
    {
        LuaManager.instance.Init();
        LuaManager.instance.doFile("Main");

        CallLuaClass obj  = LuaManager.instance.Global.Get<CallLuaClass>("testClass");
        Debug.Log(obj.testString);
        obj.func();
    }

}


```


```lua
testClass = {
    testInt = 100,
    testBool = true,
    testFloat = 10.1,
    testString = "123",
    func = function ()
        print(100)
    end

}
```

**接口是引用 拷贝 ！！！！！！！**

**也可以使用LuaTable**

```c#
void Start()
{
	LuaManager.instance.Init();
	LuaManager.instance.doFile("Main");

	LuaTable table = LuaManager.instance.Global.Get<LuaTable>("testClass");

	Debug.Log(table.Get<int>("testInt"));
}
```

> 不推荐使用 LuaTable LuaFunction !!!!!! 效率较低


> LuaTable 需要 手动 释放 Dispose

