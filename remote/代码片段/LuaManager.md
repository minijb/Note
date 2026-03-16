
```c#
using System.Security.Cryptography;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEngine;
using UnityEngine.UI;
using XLua;
using XLua.LuaDLL;

public class LuaManager : MonoBehaviour
{
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



    #region luaFunction
    public void Init(){
        if(luaEnv != null) return;
        luaEnv = new LuaEnv();
        luaEnv.AddLoader(FileLoader);
        // luaEnv.AddLoader(AssetBundleLoader);
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
    #endregion

    #region loader
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
    #endregion
}

```