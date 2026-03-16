
从网络获取文件的内容， UniNodeFile 为 内容 (UniFileContext)  外层套壳。

### FromRawData --- static ： 利用二进制信息获取一个 UniNodeFile

## UniNodeFile

HEAD: tag, version , flag, type, extend, datalength (4byte)


UniFileContext context : 数据内容

```c#
public class UniFileContext  
{  
    public UniFileMeta Meta;  
    public UniNodeData TreeData;  
    public UniNodeData UIRootData;  
    public UniNodeData EnvData;  
    public UniNodeData CameraData;  
  
    public UniNodeData AttachmentData;  
    public UniRuntimeAssetLibrary AssetLibrary;  
    public bool IsLegacyData;  
    public bool IsSerializeLibrary;  
    public bool IsDeserializeLibrary;  
    public IUniNodeDataFixer DataFixer;  
    public UniNodeData SpawnNode;  
    public uint NextRepeatIdFix;  
    public int[] PrimitiveShapeCount;  
    public bool WriteMaterialToLibrary = true;  
    public HashSet<int> AllInputChannels = new HashSet<int>();  
    public HashSet<int> AllOutputChannels = new HashSet<int>();  
    public string PatchError = string.Empty;  
    public HashSet<UniRefNodeData> AllRefs = new HashSet<UniRefNodeData>();  
    public List<uint> IDList;  
    /// <summary>  
    /// 这里记得编辑模式场景新建的也要加进来移除也是  
    /// </summary>  
    public Dictionary<string, List<UniBroadcastScriptNode>> AllBroadcastEvent = new Dictionary<string, List<UniBroadcastScriptNode>>();  
  
    public bool NeedBlackBoard = true;  
}
```

## UniFileMeta 元信息

1. Flag  int ： 使用 `|` 方法结合 enum 实现

```c#
public enum UniFileFlag  
{  
    None = 0,  
    LZ4Encode = 1 << 0,//lz4 压缩  
    SubType = 1 << 1,  
    CreateTime = 1 << 2,  
    OpenSource = 1 << 3,  
    NodeData = 1<<4,  
    HaveTemplates=1<<5,  
    HaveDataPosition = 1 << 7,  
    HavePreviewPose = 1<<8,  
  
```

2. Type : UniData,  UniScene
3. Subtye, CreateTime, Version , RefList（引用节点信息）， 

## UniFileContext 具体内容

```c#
public UniNodeData TreeData;  
public UniNodeData UIRootData;  
public UniNodeData EnvData;  
public UniNodeData CameraData;  
  
public UniNodeData AttachmentData;
public UniNodeData SpawnNode;
```

## UniNodeData  父类

基础信息如  Id， name， position，Rotation， Scale， RefTemplateId， UniNodeMeta meta Node 的元数据。 


## UniNodeMeta


```c#
public struct MetaData  
{  
    public Matrix4x4 WorldMatrix;  
    public Bounds WorldBounds;  
    public bool BoundsSet;  
    public int ChildCount;  
    public int ShapeCount;  
    public int LogicCount;  
}  
  
public UniNodeData Parent;  
public MetaData Data;  
public LinkedListNode<UniNodeLoadTask> LinkedListNode;  
public UniNodeLoadStatus LoadStatus;
```


## 常见的 UniGroupData 子类

### UniGroupData

包含 Childrens 属性用于存储 子节点信息