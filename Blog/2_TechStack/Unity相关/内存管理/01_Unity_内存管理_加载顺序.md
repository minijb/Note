
一个 prefab 内的资源大概包含以下

- Gameobject  --- clone
- transform   --- clone
- mesh        --- 引用/clone
- texture     --- 引用/clone
- material    --- 引用
- shader      --- 引用
- script      --- clone
- 其他

destory 会销毁复制的对象，但是不会销毁引用对象

销毁引用对象 ： 

- `Resources.UnloadUnusedAssets`
- `AssetBundle.Unload(true)` -- 可以但是不安全
- `AssetBundle.Unload(false)` -- 不可以


**script**

还记得 Update 这些使用反射运行。  这里其实相当于 new 一个 class，并挂到主线程调用链中。  **数据块** 复制， **代码块** 进行引用。

![image.png](https://s2.loli.net/2025/10/14/jZGaFCEu23DsUh8.png)


### 1. 从外部加载资源的方法

- AssetBundle.CreateFrom.....：创建一个AssetBundle内存镜像，注意同一个assetBundle文件在没有Unload之前不能再次被使用  
- `WWW.AssetBundle` ：同上，当然要先new一个再 yield return 然后才能使用  
- AssetBundle.Load(name)： 从AssetBundle读取一个指定名称的Asset并生成Asset内存对象，如果多次Load同名对象，除第一次外都只会返回已经生成的Asset 对象，也就是说多次Load一个Asset并不会生成多个副本（singleton）。  
- Resources.Load(path&name)：同上,只是从默认的位置加载。  
- Instantiate（object)：Clone 一个object的完整结构，包括其所有Component和子物体（详见官方文档）,浅Copy，并不复制所有引用类型。有个特别用法，虽然很少这样 用，其实可以用Instantiate来完整的拷贝一个引用类型的Asset,比如Texture等，`要拷贝的Texture必须类型设置为 Read/Write able。`

### 2. 释放资源的方法

- Destroy: 主要用于销毁克隆对象，也可以用于场景内的静态物体，不会自动释放该对象的所有引用。虽然也可以用于Asset,但是概念不一样要小心，如果用于销毁从文 件加载的Asset对象会销毁相应的资源文件！但是如果销毁的Asset是Copy的或者用脚本动态生成的，只会销毁内存对象。  
- AssetBundle.Unload(false):释放AssetBundle文件内存镜像  
- AssetBundle.Unload(true):释放AssetBundle文件内存镜像同时销毁所有已经Load的Assets内存对象  
- Reources.UnloadAsset(Object):显式的释放已加载的Asset对象，只能卸载磁盘文件加载的Asset对象  
- Resources.UnloadUnusedAssets:用于释放所有没有引用的Asset对象  
- GC.Collect()强制垃圾收集器立即释放内存 Unity的GC功能不算好，没把握的时候就强制调用一下

从磁盘读取一个1.unity3d文件到内存并建立一个AssetBundle1对象  
AssetBundle AssetBundle1 = AssetBundle.CreateFromFile("1.unity3d");  
从AssetBundle1里读取并创建一个Texture Asset,把obj1的主贴图指向它  
obj1.renderer.material.mainTexture = AssetBundle1.Load("wall") as Texture;  
把obj2的主贴图也指向同一个Texture Asset  
obj2.renderer.material.mainTexture =obj1.renderer.material.mainTexture;  
1. Texture是引用对象，永远不会有自动复制的情况出现(除非你真需要，用代码自己实现copy)，只会是创建和添加引用  
如果继续：  
2. AssetBundle1.Unload(true) 那obj1和obj2都变成黑的了，因为指向的Texture Asset没了  
如果：  
3. AssetBundle1.Unload(false) 那obj1和obj2不变，只是AssetBundle1的内存镜像释放了  
继续：  
4. Destroy(obj1),//obj1被释放，但并不会释放刚才Load的Texture  
如果这时候：  
5. Resources.UnloadUnusedAssets();  
不会有任何内存释放 因为Texture asset还被obj2用着  
如果  
6. Destroy(obj2)  
obj2被释放，但也不会释放刚才Load的Texture  
继续  
7. Resources.UnloadUnusedAssets();  
这时候刚才load的Texture Asset释放了，因为没有任何引用了  
8. 最后CG.Collect();  
强制立即释放内存

### 4. 卸载资源可以按步卸载


```c#

TLlist<string> fileList;
int n=0;
IEnumerator OnClick()
{
	WWW image = new www(fileList[n++])；
	yield return image;
	obj.mainTexture = image.texture;
	n = (n>=fileList.Length-1)?0:n;
	Resources.UnloadUnusedAssets();
}

IEnumerator OnClick()
{
	WWW image = new www(fileList[n++])；
	yield return image;
	Texture tex = obj.mainTexture;
	obj.mainTexture = image.texture;
	n = (n>=fileList.Length-1)?0:n;
	Resources.UnloadAsset(tex);
}
```

### 5. 什么资源可以被 UnloadUnusedAssets 卸载


所以：UnusedAssets不但要没有被实际物体引用，也要没有被生命周期内的变量所引用，才可以理解为 Unused(引用计数为0)  
所以所以：如果你用个全局变量保存你Load的Assets，又没有显式的设为null，那 在这个变量失效前你无论如何UnloadUnusedAssets也释放不了那些Assets的。如果你这些Assets又不是从磁盘加载的，那除了 UnloadUnusedAssets或者加载新场景以外没有其他方式可以卸载之。

```c#
obj = null;  
Resources.UnloadUnusedAssets();
```


**Texture加载以后是到内存，显示的时候才进入显存的Texture Memory。**  
**所有的东西基础都是Object**  
**Load的是Asset,Instantiate的是GameObject和Object in Scene**  
**Load的Asset要Unload,new的或者Instantiate的object可以Destro**

![image.png](https://s2.loli.net/2025/10/15/jblqHD3udZsa2Qp.png)


### UnloadUnUsedAsset ， UnloadAsset

- `Resources.UnloadAsset(Object)`:
​​​​​​​只卸载特定资源
更精确但范围有限
对于已实例化的资源无效
- `Destroy()/DestroyImmediate()`:
​​​​​​​​​​​​​​销毁场景中的GameObject或Component
不会自动卸载相关资源
- `AssetBundle.Unload()`:
仅卸载特定AssetBundle中的资源
可选择是否卸载已实例化对象
