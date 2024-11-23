
配合 spaceTree 进行进行渲染辅助

**基类 ： UniEntity**

- Bounds -- 包围盒
- bool  --- isInTree/ isShow

**UniNodeEntity : UniEntity**

- UniRenderNode renderNode --- 继承自 uniNode --- 基础节点。 用于存储真实渲染信息 (加了一层)

	主要用于得到真实的 bounds 以及 渲染组件的属性

**UniLoadNodeEntity**

```c#
public UniRenderNodeData Data;  
public UniGroup Parent;  
public UniNodeLoadRefCounter RefCounter;  
public UniNodeLoadContext LoadContext;  
private GameObject prefab;  
private UniNodeLoadAdapter loadAdapter;  
private bool inLoadAsset = false;  
private bool inInstantiateAsset = false;
```

`InstantiatePrefab` : 利用 prefab 进行初始化 -- >  调用 `OnInstantiateTask`

```c#
public override bool GetBounds(out Bounds bounds)  // 得到 render node 的 bound
public override void SetShow(bool show) // 设置是都机械能展示
private bool LoadPrefab(bool syncLoad) // 加载 prefab， 根据不同的 renderNode 类型实现不同的加载策略
private void OnInstantiateTask() // 真实加载任务
// 根据不同的类型 利用 loadAdapter + prefab 进行构建

// 回调函数 --- 创建 Node 自动加载
public void OnCreateRenderNode(UniNodeLoadAdapter loadAdapter, bool syncLoad)  
{  
    this.loadAdapter = loadAdapter;  
    Load(syncLoad);  
}  
  
private void Load(bool syncLoad)  
{  
    if (LoadPrefab(syncLoad))  
    {        InstantiatePrefab(syncLoad);  
    }}
```