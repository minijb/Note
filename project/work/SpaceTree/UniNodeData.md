
```c#
[ProtoContract]
    public class UniNodeData
    {
        public static UniLogger Logger = UniLogManager.Get(nameof(UniNodeData));
        public uint Id;
        public string Name;
        public Vector3 Position;
        public Vector3 Rotation;
        public Vector3 Scale=Vector3.one;
        public uint RefTemplateId;
        public bool isDisActive;
        public bool EditModeHideState;
        public bool LockState;
        public IUniSLData BasicComponent;

        //只有在反序列化时有该信息
        public UniNodeMeta Meta;
        public bool PreLoad;

        public virtual void RecaculateId(GenerateRefIdContext ctx)
        {
            if (ctx.Seed > 0)
            {
                var hash = UniHash.Compute(Id);
                hash.Append(ctx.Seed);
                Id = (uint)hash.GetHashCode();
                if (BasicComponent != null)
                {
                    BasicComponent.GenerateRefId(ctx);
                }
               
            }
        }

        public virtual void ClearId()
        {
            Id = 0;
        }

        public virtual UniNodeDataType TypeId()
        {
            return 0;
        }

        public virtual string DumpString()
        {
            return $"id:{Id}\npos:{Position}\nrot:{Rotation}\n:scale:{Scale}";
        }

        public virtual void OnCollectionId(List<uint> idList)
        {
            if(idList != null)idList.Add(Id);
        }

        public virtual void GenerateMetaInfo(GenerateMetaContext context, UniNodeData parent)
        {
            if (context.NeedClone && Meta != null)
            {
                var newMeta = GetUniNodeMeta();
                newMeta.Clone(Meta);
                Meta = newMeta;
            }
            else
            {
                this.Meta = GetUniNodeMeta();
            }
            this.Meta.Parent = parent;
            if (parent != null && parent.Meta != null)
            {
                this.Meta.Data.WorldMatrix = parent.Meta.Data.WorldMatrix *
                                             Matrix4x4.TRS(Position, Quaternion.Euler(Rotation), Scale);
            }
            else
            {
                this.Meta.Data.WorldMatrix = Matrix4x4.TRS(Position, Quaternion.Euler(Rotation), Scale);
            }
        }
        public virtual void MultiplyFromPose(ref Matrix4x4 from)
        {
            Position = from.MultiplyPoint(Position);
            Scale = from.MultiplyVector(Scale);
            Rotation = (from.rotation * Quaternion.Euler(Rotation)).eulerAngles;
        }
        public virtual void OnAfterDeserialize()
        {
        }

        public virtual void ShallowCopy(UniNodeData node)
        {
            node.Id = this.Id;
            node.Name = this.Name;
            node.Position = this.Position;
            node.Rotation = this.Rotation;
            node.Scale = this.Scale;
            node.RefTemplateId = this.RefTemplateId;
            node.isDisActive = this.isDisActive;
            node.EditModeHideState = this.EditModeHideState;
            node.LockState = this.LockState;
            node.Meta = this.Meta;
            node.BasicComponent = BasicComponent;
        }

        protected virtual void CopyData(GenerateRefIdContext ctx,UniNodeData node)
        {
            ShallowCopy(node);
            if(BasicComponent != null)
            {
                node.BasicComponent = BasicComponent.Clone();
            }
            if (ctx.Seed > 0 && this.Id > 0)
            {
                var hash = UniHash.Compute(node.Id);
                hash.Append(ctx.Seed);
                node.Id = (uint)hash.GetHashCode();
                if (node.BasicComponent != null)
                {
                    node.BasicComponent.GenerateRefId(ctx);
                }
            }
            if (ctx.IDCollection != null)
            {
                ctx.IDCollection.Add(node.Id);
            }
            if (this.Meta != null)
            {
                node.Meta = GetUniNodeMeta();
                node.Meta.Data = this.Meta.Data;
            }
            
        }

        public virtual UniNodeMeta GetUniNodeMeta()
        {
            return new UniNodeMeta();
        }

        public virtual UniNodeData Clone(GenerateRefIdContext ctx)
        {
            UniNodeData clone = new UniNodeData();
            CopyData(ctx, clone);
            return clone;
        }
/// <summary>
/// parentData是nodeData的parent
/// </summary>
/// <param name="nodeData"></param>
/// <param name="parentData"></param>
        public virtual void AddData(UniNodeData nodeData,UniNodeData parentData)
        {
            
            isDisActive =isDisActive && nodeData.isDisActive;
            if (nodeData.BasicComponent != null)
            {
                if (BasicComponent == null)
                {
                    BasicComponent = nodeData.BasicComponent.Clone();
                }
                else
                {
                    IBasicSL basicSl = nodeData.BasicComponent as IBasicSL;
                    IBasicSL selfBasicSl = BasicComponent as IBasicSL;
                    if (basicSl is IScriptSL sl1 && sl1.NodesSL != null && sl1.NodesSL.Count>0)
                    {
                        if(selfBasicSl.OnSpawnedNodeEventsSL == null)
                        {
                            selfBasicSl.OnSpawnedNodeEventsSL =basicSl.OnSpawnedNodeEventsSL.Clone();
                        }
                        else
                        {
                            var sl2 = selfBasicSl.OnSpawnedNodeEventsSL as IScriptSL;
                            sl2.NodesSL.AddRange(sl1.NodesSL);
                        }
                    }
                    if (basicSl.OnDestroyedNodeEventsSL is IScriptSL sl3 && sl3.NodesSL != null && sl3.NodesSL.Count>0)
                    {
                        if(selfBasicSl.OnDestroyedNodeEventsSL == null)
                        {
                            selfBasicSl.OnDestroyedNodeEventsSL = basicSl.OnDestroyedNodeEventsSL.Clone();
                        }
                        else
                        {
                            var sl4 = selfBasicSl.OnDestroyedNodeEventsSL as IScriptSL;
                            sl4.NodesSL.AddRange(sl3.NodesSL);
                        }
                    }
                }
            }                                                     
            
        }
        
        public virtual int GetLogicCount()
        {
            return 0;
        }

        public UniNodeData CullServerNoNeedData()
        {
            #if UNITY_SERVER
            if (this is UniGroupData groupData)
            {
                List<UniNodeData> res = ChildHasServerNeed(this);
                if (CheckServerNeed(this))
                {
                    UniNodeData temp = res[0];
                    ListPool<UniNodeData>.QuickPool.Release(res);
                    int logic = 0;
                    if (groupData.Childrens != null && groupData.Childrens.Count > 0)
                    {
                        foreach (var c in groupData.Childrens)
                        {
                            if (c is UniComponentsNodeData)
                            {
                                logic++;
                            }
                        }
                    }
                    groupData.Meta.Data.LogicCount = logic;
                    return temp;
                }
                else
                {
                    groupData.Childrens = res;
                    int logic = 0;
                    if (groupData.Childrens != null && groupData.Childrens.Count > 0)
                    {
                        foreach (var c in groupData.Childrens)
                        {
                            if (c is UniComponentsNodeData)
                            {
                                logic++;
                            }
                        }
                    }
                    groupData.Meta.Data.LogicCount = logic;
                }

            }
            else
            {
                return this;
            }
            #endif
            return this;
        }

        private static List<UniNodeData> ChildHasServerNeed(UniNodeData data)
        {
            if (!(data is UniGroupData groupData) || groupData.Childrens == null || groupData.Childrens.Count == 0)
            {
                if (CheckServerNeed(data))
                {
                    List<UniNodeData> res = ListPool<UniNodeData>.QuickPool.Get();
                    res.Add(data);
                    return res;
                }

                return null;
            }

            List<UniNodeData> childs = ListPool<UniNodeData>.QuickPool.Get();
            foreach (var node in groupData.Childrens)
            {
                List<UniNodeData> temp = ChildHasServerNeed(node);
                if (temp != null)
                {
                    childs.AddRange(temp);
                    ListPool<UniNodeData>.QuickPool.Release(temp);
                }
            }

            if (CheckServerNeed(groupData))
            {
                ListPool<UniNodeData>.QuickPool.Release(groupData.Childrens);
                groupData.Childrens = childs;
                int logic = 0;
                if (childs != null)
                {
                    foreach (var c in childs)
                    {
                        if (c is UniComponentsNodeData)
                        {
                            logic++;
                        }
                    }
                }

                groupData.Meta.Data.LogicCount = logic;
                List<UniNodeData> res = ListPool<UniNodeData>.QuickPool.Get();
                res.Add(data);
                return res;
            }

            return childs;
        }

        private static bool CheckServerNeed(UniNodeData data)
        {
            if (data is UniGroupData{IsRef:true})
            {
                return true;
            }

            if (!(data is UniComponentsNodeData componentsNode) || componentsNode.Components == null || componentsNode.Components.Count == 0)
            {
                return false;
            }

            foreach (IUniSLData item in componentsNode.Components)
            {
                if (item.ServerCannotCulling())
                {
                    return true;
                }
            }

            return false;
        }
        
        [ProtoBeforeSerialization]
        public void OnBeforeSerialization(SerializationContext context)
        {
            var ctx = context.Context as UniNodeFile.UniSerializationCtx;
            UniFileContext fctx = new UniFileContext();
            UniNodeWriter.Serialize(ctx.Writer,this,ref fctx);
        }
        [ProtoBeforeDeserialization]
        public void OnBeforeDeserialization(SerializationContext context)
        {
            var ctx = context.Context as UniNodeFile.UniSerializationCtx;
            UniFileContext fctx = new UniFileContext();
            UniNodeReader.Deserialize(ctx.Reader, this , ref fctx);
        }
        
        
        
    }
```

`UniNodeData`

类是一个用于在 Unity 中管理和操作节点数据的类。它使用 `ProtoContract` 特性进行标记，以便支持序列化和反序列化。该类包含多个字段和方法，用于处理节点的标识、位置、旋转、缩放、模板引用、组件管理、元信息生成、ID 重新计算、数据复制、服务器数据裁剪等功能。

首先，类中定义了几个字段，包括静态的 `Logger`，用于记录日志信息。`Id`、`Name`、`Position`、`Rotation` 和 `Scale` 分别用于存储节点的唯一标识符、名称、位置、旋转和缩放。`RefTemplateId` 用于存储模板引用的 ID。`isDisActive`、`EditModeHideState` 和 `LockState` 分别用于指示节点是否禁用、编辑模式下是否隐藏和是否锁定。`BasicComponent` 用于存储节点的基础组件。`Meta` 用于存储节点的元信息，只有在反序列化时才有该信息。`PreLoad` 用于指示节点是否预加载。

`RecaculateId` 方法用于重新计算节点的 ID。方法接受一个 `GenerateRefIdContext` 类型的参数 `ctx`，并根据上下文中的种子值重新计算 ID。如果节点具有基础组件，则调用其 `GenerateRefId` 方法重新生成引用 ID。

`ClearId` 方法用于清除节点的 ID，将其设置为 0。`TypeId` 方法返回节点数据类型的 ID，默认返回 0。`DumpString` 方法返回节点的字符串表示形式，包括 ID、位置、旋转和缩放信息。`OnCollectionId` 方法用于收集节点的 ID，并将其添加到传入的 ID 列表中。

`GenerateMetaInfo` 方法用于生成节点的元信息。方法接受一个 `GenerateMetaContext` 类型的参数 `context` 和一个父节点数据 `parent`。如果上下文需要克隆且节点已有元信息，则克隆元信息并设置为新的元信息。否则，创建新的元信息并设置为节点的元信息。然后，根据父节点的元信息计算节点的世界矩阵。

`MultiplyFromPose` 方法用于根据传入的矩阵更新节点的位置、旋转和缩放。`OnAfterDeserialize` 方法在反序列化后调用，默认实现为空。

`ShallowCopy` 方法用于浅拷贝节点数据，将当前节点的数据复制到传入的节点中。`CopyData` 方法用于复制节点数据，接受一个 `GenerateRefIdContext` 类型的参数 `ctx` 和一个目标节点 `node`。方法首先浅拷贝节点数据，然后根据上下文中的种子值重新计算 ID，并生成新的引用 ID。如果节点具有基础组件，则克隆基础组件并设置到目标节点中。

`GetUniNodeMeta` 方法返回一个新的 `UniNodeMeta` 对象。`Clone` 方法用于克隆节点数据，接受一个 `GenerateRefIdContext` 类型的参数 `ctx`，并返回克隆的节点数据。

`AddData` 方法用于将节点数据添加到当前节点中，接受两个参数：节点数据 `nodeData` 和父节点数据 `parentData`。方法根据传入的节点数据更新当前节点的禁用状态和基础组件。

`GetLogicCount` 方法返回节点的逻辑计数，默认返回 0。`CullServerNoNeedData` 方法用于裁剪服务器不需要的数据，返回裁剪后的节点数据。

`ChildHasServerNeed` 方法用于检查子节点是否需要服务器数据，返回需要的数据列表。`CheckServerNeed` 方法用于检查节点是否需要服务器数据，返回布尔值。

`OnBeforeSerialization` 方法在序列化前调用，接受一个 `SerializationContext` 类型的参数 `context`，并调用 `UniNodeWriter.Serialize` 方法进行序列化。`OnBeforeDeserialization` 方法在反序列化前调用，接受一个 `SerializationContext` 类型的参数 `context`，并调用 `UniNodeReader.Deserialize` 方法进行反序列化。

总体来说，`UniNodeData` 类提供了丰富的功能，用于管理和操作节点数据，包括标识、位置、旋转、缩放、组件管理、元信息生成、ID 重新计算、数据复制和服务器数据裁剪等功能。通过这些方法，可以方便地在 Unity 中管理和操作复杂的节点数据，提高开发效率。