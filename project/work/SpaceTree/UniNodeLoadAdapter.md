
父类

子类有 UniAOINodeLoadAdapter， UniEditNodeLoadAdapter，  UniPlayNodeLoadAdapter

`private static UniGroupData generateParentMetaInfoGroupData = new UniGroupData();` 

生成父组节点的源数据


## `UniObjectPool<T>`

使用队列管理对象池

**UniGameObjectPool**  抓门用来处理 GameObj. 

### Load

`public virtual UniNode Load(UniNode parent, UniNodeData data, UniNodeLoadContext context, Action<UniNode> onRenderReadyEvent = null, Action<UniNode> onLogicReadyEvent = null)`

UniNodeLoadRefCounter ： 用来记录递归的深度的

添加两个事件 ： 1. OnRenderReadyEvent 2. OnLogicReadyEvent

