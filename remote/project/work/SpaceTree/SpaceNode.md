
```C#
  
public SpaceIndex Index;  
public readonly List<UniLoadNodeEntity> UnLoadUniNodeEntityList = new List<UniLoadNodeEntity>();  
public List<UniEntity>[] Renderers;  
public readonly List<UniEntity> LoadedUniNodeEntityList = new List<UniEntity>();  
public List<UniRefNodeData> RefNodes = new List<UniRefNodeData>(); private AOINodeState state = AOINodeState.None;  
private byte IsInRefine;  
private bool isCullingInit;  
private int lastDistance;
```

**InsertNotLoadedObj** -- 添加未加载的 obj

1. 将物体添加到 UnLoadUniNodeEntityList  --- 用于几步加载

根据状态有不同的方法 ： loaded - 载入加载完成列表， 没有在加载 unload列表，  loading 

**InsertLoadedObj** -- 添加已加载的 obj

`SpaceTree` 输入一个 Entity -- 得到他的 bounds , 然后 LoadedUniNodeEntityList
需要没有 flag !!  将它放到 lodGroupCreatQueue.

**RemoveLoadedObj** -- 移除已经加载的物体

`public void RemoveLoadedObj(UniEntity entity, SpaceTree ownerTree, Queue<SpaceNode> lodGroupCreatQueue)` 

**Renderers**  

根据 lodSize 在 添加到 Renders : 

需要注意的是 :   添加到 第一个 大于 lodSize 的位置

```c#
public void InsertRenderer(UniEntity ren)  
{  
    float[] lodSizes = QualitySetting.Instance.refine4CullingSize;  
    int lodLevelCount = lodSizes.Length;  
    Vector3 boundsSize = ren.Bounds.size;  
    // int globalSize = 48;  
    float size = boundsSize.magnitude;  
    for (int i = 0; i < lodLevelCount; i++)  
    {        
	    if (size > lodSizes[i])  
        {            
	        Renderers[i].Add(ren);  
            break;  
        }    
    }
}
```

**LoadObject**

将自己添加到对应队列

**LoadObjectOnce**

`public bool LoadObjectOnce(SpaceTree tree, Queue<SpaceNode> lodGroupCreatQueue)`

1. 如果 没有 Init 直接返回 
2. 如果 NodeEntityList  没有 值
	-  添加 Loaded 状态
	-  添加到 Queue
	-  移除 State  : NodeInLoadQueue
	-  return
3.  UnloadList 删除最后一个， 
	-   `entity.OnCreateRenderNode(tree.NodeLoadAdapter, tree.isFirstLoaded);` 利用 LoadAdapter 进行 prefab 构建
	-  在 LoadedUniNodeEntityList 中添加 entity

`public void LoadObjectOnce(SpaceTree tree, UniLoadNodeEntity entity, Queue<SpaceNode> lodGroupCreatQueue)`

类似于 上一条中的 3


**AddLodCreateQueue**

添加状态，并传入对应的 Queue


**Renders**  二维数组， 是如何划分的。 根据包围盒大小进行划分的 ： 三个点的三位向量长度 ！！！

```c#
public void InsertRenderer(UniEntity ren)  
{  
    float[] lodSizes = QualitySetting.Instance.refine4CullingSize;  
    int lodLevelCount = lodSizes.Length;  
    Vector3 boundsSize = ren.Bounds.size;  
    // int globalSize = 48;  
    float size = boundsSize.magnitude;  
    for (int i = 0; i < lodLevelCount; i++)  
    {        if (size > lodSizes[i])  
        {            Renderers[i].Add(ren);  
            break;  
        }        
    }
}
```


**Setculling**  ！！！！

`public void SetCulling(int currentDistance, bool visible, bool isEnable)`

currentDistance ： 


LODBatcher