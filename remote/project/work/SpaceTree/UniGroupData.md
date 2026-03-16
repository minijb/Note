```c#
public class UniGroupData : UniComponentsNodeData
    {
        //public UniNodeEvents_SLData OnReceivedBroadcast;
        public bool NeedFixPivot;

        public List<UniNodeData> Childrens;
        //public List<string> Tags;

        
        //public int Layer;
        public byte[] CaptureRawData;

        public UniWorkReferenceData UniReferenceData;
        public bool IsRef => UniReferenceData != null;
        public override string DumpString()
        {
            StringWriter sw = new StringWriter();
            sw.WriteLine(base.DumpString());
            sw.WriteLine("child begin----------------------------------");
            if (Childrens != null)
            {
                foreach (var c in Childrens)
                {
                    sw.WriteLine(c.DumpString());
                }
            }
            sw.WriteLine("child end----------------------------------");
            return sw.ToString();
        }

        public override void OnCollectionId(List<uint> idList)
        {
            base.OnCollectionId(idList);
            if (Childrens != null && idList!=null)
            {
                foreach (var d in Childrens)
                {
                    if (d is UniGroupData groupData)
                    {
                        groupData.OnCollectionId(idList);
                    }
                }
            }
        }
        

        public override (UniNodeData, IUniSLData) FindComponent2(int id)
        {
            var t = base.FindComponent2(id);
            if (t.Item2 == null && Childrens !=null)
            {
                foreach (var c in Childrens)
                {
                    if (c is UniComponentsNodeData cc)
                    {
                        t = cc.FindComponent2(id);
                        if(t.Item2 != null)break;
                    }
                }
            }

            return t;
        }
        public override void ClearId()
        {
            base.ClearId();
            if (Childrens != null)
            {
                foreach (var d in Childrens)
                {
                    d.ClearId();
                }
            }
        }

        public virtual void CollectRefInfos(ref List<UniNodeRefInfo>  EarlyCollectRefInfos,string exceptId)
        {
            if (EarlyCollectRefInfos!=null)
            {
                foreach (var c in Childrens)
                {
                    // else 
                    if(c is UniGroupData g)
                    {
                        g.CollectRefInfos(ref EarlyCollectRefInfos,exceptId);
                    }
                }
            }
            
        }

        public override void RecaculateId(GenerateRefIdContext ctx)
        {
            base.RecaculateId(ctx);
            if (Childrens != null)
            {
                foreach (var d in Childrens)
                {
                    d.RecaculateId(ctx);
                }
            }
        }

        protected virtual void OnMakeChildIdentityPose(ref Matrix4x4 mat)
        {
            if (Childrens != null)
            {
                foreach (var child in Childrens)
                {
                    var oriScale = child.Scale;
                    child.Scale = new Vector3(Mathf.Abs(oriScale.x), Mathf.Abs(oriScale.y), Mathf.Abs(oriScale.z));
                    
                    
                    var cmat = mat * Matrix4x4.TRS(child.Position, Quaternion.Euler(child.Rotation), child.Scale);
                    var oriPos = child.Position;
                    var oriRot = Quaternion.Euler(child.Rotation);
                    
                    child.Position = cmat.GetPosition();
                    child.Rotation = cmat.rotation.eulerAngles;
                    child.Scale = Vector3.Scale(Scale, oriScale);
                    if (Meta.Data.BoundsSet)
                    {
                        child.Position += -Meta.Data.WorldBounds.center;
                    }

                    if (child is UniComponentsNodeData groupData && groupData.Components != null)
                    {
                        foreach (var c in groupData.Components)
                        {
                            if (c is UniBackForthEntity_SLData sl)
                            {
                                sl.Target += child.Position - oriPos;
                                sl.Rotate = (Quaternion.Euler(sl.Rotate) * (Quaternion.Inverse(oriRot) * cmat.rotation)).eulerAngles;
                                // sl.Scale.x *= oriScale.x/Scale.x;
                                // sl.Scale.y *= oriScale.x/Scale.y;
                                // sl.Scale.z *= oriScale.x/Scale.z;
                            }
                            else if (c is UniVehicle_SLData vehicle)
                            {
                                
                            }
                        }
                    }
                }
            }
        }

        public void MakeIdentityPose()
        {
            if (Meta == null)
            {
                GenerateMetaInfo(new GenerateMetaContext() { Root = this }, null);
            }

            Quaternion fixRotation = Quaternion.identity;
            //老的车身体部分和vehicle部分有旋转偏移得需要修复一下
            // var vehicleBodyFix = FindComponent2(UniVehicleBody_SLData.SLID);
            // if (vehicleBodyFix.Item2 != null && vehicleBodyFix.Item1.Meta != null)
            // {
            //     fixRotation = Quaternion.Euler(Rotation)*Quaternion.Inverse(vehicleBodyFix.Item1.Meta.Data.WorldMatrix.rotation);
            // }

            var mat = Matrix4x4.TRS(Position, Quaternion.Euler(Rotation)*fixRotation, Scale);
            var oriMat = mat;
            OnMakeChildIdentityPose(ref mat);
            if (this is UniComponentsNodeData groupData && groupData.Components != null)
            {
                var mat2_inver = oriMat.inverse;
                foreach (var c in groupData.Components)
                {
                    if (c is UniBackForthEntity_SLData sl)
                    {
                        sl.Target = mat2_inver.MultiplyPoint3x4(sl.Target);
                        sl.Rotate = (Quaternion.Euler(sl.Rotate)*mat2_inver.rotation).eulerAngles;
                        sl.Scale.x /= Scale.x;
                        sl.Scale.y /= Scale.y;
                        sl.Scale.z /= Scale.z;
                    }
                }
            }

            
            
            Position = Vector3.zero;
            Rotation = Vector3.zero;
            Scale = Vector3.one;
        }

        public virtual void OnBeginGenerateMetaInfo(GenerateMetaContext context)
        {
        }

        public override void GenerateMetaInfo(GenerateMetaContext context, UniNodeData parent)
        {
            base.GenerateMetaInfo(context, parent);
            OnBeginGenerateMetaInfo(context);
            if (UniReferenceData!=null && UniReferenceData.RefNodesData != null && UniReferenceData.RefTargetOriginalData==null)
            {
                this.Meta.Data.ChildCount += 1;
                UniReferenceData.RefNodesData.GenerateMetaInfo(context, this);
            }
            if (Childrens != null)
            {
                this.Meta.Data.ChildCount += Childrens.Count;
                foreach (var d in Childrens)
                {
                    d.GenerateMetaInfo(context, this);
                }

                if (parent != null && parent.Meta != null)
                {
                    parent.Meta.Data.ShapeCount += this.Meta.Data.ShapeCount;
                    if (parent.Meta.Data.BoundsSet)
                    {
                        parent.Meta.Data.WorldBounds.Encapsulate(this.Meta.Data.WorldBounds);
                    }
                    else
                    {
                        parent.Meta.Data.BoundsSet = true;
                        parent.Meta.Data.WorldBounds = this.Meta.Data.WorldBounds;
                    }
                }

                if (NeedFixPivot)
                {
                    NeedFixPivot = false;
                    if (Meta.Data.BoundsSet && !context.DisableFixPivot)
                    {
                        if (!((context.SkipFixRootNode && context.Root == this) || (context.FixRootOnly && context.Root != this)))
                        {
                            context.PivotFixed = true;
                            Vector3 localCenter = Meta.Data.WorldMatrix.inverse.MultiplyPoint3x4(Meta.Data.WorldBounds.center);
                            foreach (var c in Childrens)
                            {
                                c.Position -= localCenter;
                            }
                        }
                    }
                }
            }

            if (context.PivotFixed && context.Root == this)
            {
                context.PivotFixed = false;
                GenerateMetaInfo(context, parent);
            }
        }

        public override void ShallowCopy(UniNodeData node)
        {
            base.ShallowCopy(node);
            if(node is UniGroupData data)
            {
                data.CaptureRawData = this.CaptureRawData;
                if(Childrens != null)data.Childrens = new List<UniNodeData>(Childrens);
                if (UniReferenceData != null)
                {
                    data.UniReferenceData = new UniWorkReferenceData();
                    UniReferenceData.CloneToOther(data.UniReferenceData);
                }
            }
        }

        public override void AddData(UniNodeData nodeData,UniNodeData parentData)
        {
            base.AddData(nodeData,parentData);
         
            if (nodeData is UniGroupData uniGroupData)
            {
                if (uniGroupData.Childrens != null)
                {
                    if (Childrens == null)
                    {
                        Childrens = new List<UniNodeData>();
                    }
                    Childrens.AddRange(uniGroupData.Childrens);
                }
                
                
                if (uniGroupData .IsRef)
                {
                    if (Childrens == null)
                    {
                        Childrens = new List<UniNodeData>();
                    }

                    if (uniGroupData.UniReferenceData.RefTargetOriginalData != null)
                    {
                        Childrens.Insert(0,uniGroupData.UniReferenceData.RefTargetOriginalData);
                    }

                    UniReferenceData.RefDataVersion = UniMain.DataVersion.Full;
                }
            }
        }

        protected override void CopyData(GenerateRefIdContext ctx,UniNodeData node)
        {
            base.CopyData(ctx,node);
            var data = node as UniGroupData;
            if (Childrens != null)
            {
                data.Childrens = new List<UniNodeData>(Childrens.Count);
                foreach (var c in Childrens)
                {
                    var clone = c.Clone(ctx);
                    if (clone.Meta != null)
                    {
                        clone.Meta.Parent = this;
                    }

                    data.Childrens.Add(clone);
                }
            }
        }

        public override UniNodeData Clone(GenerateRefIdContext ctx)
        {
            var data = new UniGroupData();
            CopyData(ctx,data);
            return data;
        }

        public override UniNodeDataType TypeId()
        {
            return UniNodeDataType.UniGroupData;
        }

        // public UniStreamingGroupData CastToStreaming()
        // {
        //     if (this.GetType() == typeof(UniStreamingGroupData)) return this as UniStreamingGroupData;
        //     UniStreamingGroupData data = new UniStreamingGroupData();
        //     ShallowCopy(data);
        //     return data;
        // }

        public override int GetLogicCount()
        {
            if (Meta != null)
            {
                return Meta.Data.LogicCount;
            }
            else
            {
                int logic = 0;
                if (Childrens != null)
                {
                    foreach (var c in Childrens)
                    {
                        if (!(c is UniRenderNodeData))
                        {
                            logic++;
                        }
                    }
                }
                return logic;
            }
            return 0;
        }

        public override void GetComponents(List<IUniSLData> result, bool includeChild = false, params Type[] uniCompType)
        {
            base.GetComponents(result, includeChild, uniCompType);
            if (includeChild)
            {
                if (Childrens != null)
                {
                    foreach (var c in Childrens)
                    {
                        if (c is UniComponentsNodeData cn)
                        {
                            cn.GetComponents(result, true, uniCompType);
                        }
                    }
                }
            }
        }


  

      
        public void GetCouldMergeGroupNodeData(ref List<UniGroupData> nodeDatas)
        {
            if (nodeDatas == null)
            {
                nodeDatas = new List<UniGroupData>();
            }

            if (UniReferenceData == null) return;
            nodeDatas.Add(this);
            if( UniReferenceData.InheritanceChains!=null) return;
            // if (UniReferenceData.RefTargetOriginalData.IsRef)
            // {
            //     UniReferenceData.RefTargetOriginalData.GetCouldMergeGroupNodeData( ref nodeDatas);
            // }
            // else if (UniReferenceData.RefTargetOriginalData!=null)
            // {
            //     nodeDatas.Add(UniReferenceData.RefTargetOriginalData);
            // }
            var refTargetData = UniReferenceData.RefTargetOriginalData;
            if (refTargetData != null)
            {
                if (refTargetData.IsRef)
                {
                    refTargetData.GetCouldMergeGroupNodeData(ref nodeDatas);
                }
                else
                {
                    nodeDatas.Add(refTargetData);
                }
            }
            
        }
        
        public bool CheckLoopRef()
        {
            if (UniReferenceData == null) return false;
            var p = Meta?.Parent as UniGroupData;
            while (p != null)
            {
                if (p.IsRef)
                {
                    var parentRefData = p.UniReferenceData;
                    if (!string.IsNullOrEmpty(UniReferenceData.RefId)&&parentRefData.RefId == UniReferenceData.RefId&&parentRefData.RefVersion==UniReferenceData.RefVersion && UniReferenceData.RefNodesData == null
                        &&UniReferenceData.InheritanceChains==null)
                    {
#if UNITY_EDITOR
                        Debug.LogError($"loop ref:{UniReferenceData.RefId}");
#endif
                        return true;
                    }
                }

                p = p.Meta?.Parent as UniGroupData;
            }
            return false;
        }
    }
```

`UniGroupData`

类继承自 `UniComponentsNodeData`，用于在 Unity 中管理和操作节点组数据。该类包含多个字段和方法，用于处理节点组的标识、位置、旋转、缩放、模板引用、组件管理、元信息生成、ID 重新计算、数据复制、服务器数据裁剪等功能。

首先，类中定义了几个字段，包括 `NeedFixPivot`，用于指示是否需要修复枢轴；`Childrens`，用于存储子节点的列表；`CaptureRawData`，用于存储捕获的原始数据；`UniReferenceData`，用于存储工作引用数据；以及 `IsRef` 属性，用于判断是否有引用数据。

`DumpString` 方法用于返回节点组的字符串表示形式，包括子节点的字符串表示。`OnCollectionId` 方法用于收集节点组及其子节点的 ID，并将其添加到传入的 ID 列表中。`FindComponent2` 方法用于查找组件，如果在当前节点组中找不到，则在子节点中继续查找。

`ClearId` 方法用于清除节点组及其子节点的 ID。`CollectRefInfos` 方法用于收集引用信息，并将其添加到传入的引用信息列表中。`RecaculateId` 方法用于重新计算节点组及其子节点的 ID。

`OnMakeChildIdentityPose` 方法用于根据传入的矩阵更新子节点的位置、旋转和缩放。`MakeIdentityPose` 方法用于重置节点组及其子节点的姿态。`OnBeginGenerateMetaInfo` 方法是一个虚方法，用于在生成元信息之前执行额外操作。

`GenerateMetaInfo` 方法用于生成节点组的元信息，并递归生成子节点的元信息。如果需要修复枢轴，则调整子节点的位置。`ShallowCopy` 方法用于浅拷贝节点组数据，包括子节点和引用数据。`AddData` 方法用于将节点数据添加到当前节点组中，并合并子节点和引用数据。

`CopyData` 方法用于复制节点组数据，包括子节点和引用数据。`Clone` 方法用于克隆节点组数据，并返回克隆的节点组。`TypeId` 方法返回节点组数据类型的 ID。

`GetLogicCount` 方法返回节点组的逻辑计数，包括子节点的逻辑计数。`GetComponents` 方法用于获取节点组及其子节点的组件。`GetCouldMergeGroupNodeData` 方法用于获取可以合并的节点组数据，并将其添加到传入的节点组数据列表中。

`CheckLoopRef` 方法用于检查节点组是否存在循环引用。如果存在循环引用，则返回 `true`，否则返回 `false`。通过这些方法，`UniGroupData` 类提供了丰富的功能，用于管理和操作节点组数据，包括标识、位置、旋转、缩放、组件管理、元信息生成、ID 重新计算、数据复制和服务器数据裁剪等功能。