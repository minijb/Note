
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



```c#
    public class UniNodeLoadAdapter
    {
        static UniLogger Logger = UniLogManager.Get(nameof(UniNodeLoadAdapter));
        private static UniGroupData generateParentMetaInfoGroupData = new UniGroupData();
        public UniScene Scene => Global.Game.Scene;

        //protected UniNodeData rootData;
        protected bool IsInitialized = false;
        public UniNodeLoadManager Manager;
        private HashSet<int> disabledComponentList;
        public static bool ShowDisableComponentToast = false;
        private HashSet<int> repeatTypeCheck = new HashSet<int>();

        public virtual void Initialize(string name, UniNodeLoadManager mgr)
        {
            Manager = mgr;
            IsInitialized = true;
            generateParentMetaInfoGroupData.GenerateMetaInfo(new GenerateMetaContext(), null);
        }

        public virtual UniNode Load(UniNode parent, UniNodeData data, UniNodeLoadContext context,
            Action<UniNode> onRenderReadyEvent = null, Action<UniNode> onLogicReadyEvent = null)
        {
            UniNodeLoadRefCounter dataRefCounter = new UniNodeLoadRefCounter();
            dataRefCounter.OnRenderReadyEvent = onRenderReadyEvent;
            dataRefCounter.OnLogicReadyEvent = onLogicReadyEvent;
            dataRefCounter.RefCount = 1;
            dataRefCounter.LogicRefCount = 1;
            // dataRefCounter.ParentNode = parent;
            context.CheckParentDestroy = parent != null;

            if (disabledComponentList == null)
            {
                if (Global.Game && Global.Game.Work)
                {
                    if (!Global.Game.IsSinglePlayerMode())
                    {
                        disabledComponentList = Global.DataModule.DisableComponentInMultiplePlayerWorld;
                    }
                    else
                    {
                        disabledComponentList = Global.DataModule.DisableComponentInOnePlayerWorld;
                    }
                }
            }

            if (context.EnableDisabledComponents)
            {
                context.DisabledComponentsList = disabledComponentList;
            }
            var node = CreateNode(parent, data, context, dataRefCounter);
            return node;
        }

        /// <summary>
        /// 目前是自己的作品都得加时间戳
        /// </summary>
        /// <param name="mapId"></param>
        /// <returns></returns>
        bool NeedAddTimeWhenLoadRefData(string mapId)
        {
#if UNITY_SERVER
            return false;
#endif
            if (!string.IsNullOrEmpty(mapId) && mapId.Contains(Global.UserId()))
            {
                return true;
            }

            return false;
        }

        public UniNode CreateNode(UniNode parent, UniNodeData data, UniNodeLoadContext context, UniNodeLoadRefCounter parentRefCounter)
        {
            UniNode root = data switch
            {
                UniPrimitiveShapeData primitiveShapeData => CreatePrimitiveShape(parent, primitiveShapeData, context, parentRefCounter),
                UniMultShapeData multShapeData => CreateMultShape(parent, multShapeData, context, parentRefCounter),
                UniTextNodeData textNodeData => CreateTextNode(parent, textNodeData, context, parentRefCounter),
                UniAsyncRefNodeData asyncRefNodeData => CreatRefNodeAsync(parent, asyncRefNodeData, context, parentRefCounter),
                //UniRefNodeData refNodeData => CreateGroupNew(parent, refNodeData, context, parentRefCounter),
                UniUICanvasData uniUICanvasData => CreateGroupNew<UniUICanvas, UniUICanvasData>(parent, uniUICanvasData, context, parentRefCounter),
                UniUIRootData uniUIRootData => CreateGroupNew<UniUIRoot, UniUIRootData>(parent, uniUIRootData, context, parentRefCounter),
                UniUIPanelData uniUIPanelData => CreateGroupNew<UniUIPanel, UniUIPanelData>(parent, uniUIPanelData, context, parentRefCounter),
                UniUINodeData uniUINodeData => CreateGroupNew<UniUINode, UniUINodeData>(parent, uniUINodeData, context, parentRefCounter),
                UniDynamicGroupData uniDynamicGroupData => CreateDynamicGroup(parent, uniDynamicGroupData, context, parentRefCounter),
                UniGroupData groupData => CreateGroupNew<Uni.UniGroup, UniGroupData>(parent, groupData, context, parentRefCounter),
                UniComponentsNodeData componentsNodeData => CreateComponnetsNode(parent, componentsNodeData, context, parentRefCounter),
                UniPlaneTextureNodeData planeTextureNodeData => CreatePlaneTextureNode(parent, planeTextureNodeData, context, parentRefCounter),
                UniCustomRenderNodeData customRenderNodeData => CustomRenderNode(parent, customRenderNodeData, context, parentRefCounter),
                UniFakeLightNodeData uniFakeLightNodeData => CreateFakeLightNode(parent, uniFakeLightNodeData, context, parentRefCounter),
                _ => null
            };
            if (context.SkipRenderNode && root is UniRenderNode rd && Scene.SpaceTree)
            {
                rd.UniSpaceLoadNodeEntity ??= new UniSpaceNodeEntity(rd);
                if (!rd.UniSpaceLoadNodeEntity.InSpaceTree)
                {
                    Scene.SpaceTree.InsertLoadedObj(rd.UniSpaceLoadNodeEntity);
                }
            }
            return root;
        }

        public TNode CreateUINode<TNode, TData>(UniNode parent, TData data, UniNodeLoadContext context, UniNodeLoadRefCounter parentRefCounter) where TNode : UniGroup where TData : UniGroupData
        {
            if (data.GetType() == typeof(UniUICanvasData))
            {
                if (parent != null && parent is not UniUIRoot && (context.RuntimeFlag & UniObjectRuntimeFlag.CreateFromUniFile) != 0)
                {
                    parentRefCounter?.OneLogicReady(null);
                    parentRefCounter?.OneRenderReady(null);
                    return null;
                }
            }
            var go = new GameObject(typeof(TNode).Name, typeof(RectTransform)) { layer = 5 };
            TNode uiNode = go.AddComponent<TNode>();
            uiNode.Scene = this.Scene;
            if (uiNode is UniUINode n && data is UniUINodeData nodeData)
            {
                int maxSort = 0;
                if (parent is UniUIPanel panel)
                {
                    maxSort = panel.MaxChildSortIndex + 1;
                }
                else if (parent is UniUINode ui && ui.IsUIGroup())
                {
                    maxSort = ui.MaxChildSortIndex + 1;
                }
                if (nodeData.BasicComponent == null)
                {
                    nodeData.BasicComponent = new UniUINodeComponent_SLData() { SortIndex = maxSort };
                }
                n.UINodeComponent.SortIndex = nodeData.UINodeComponent.SortIndex = maxSort;
            }
            SetNodeBaseData(parent, uiNode, data, context);
            ApplyNodeComponentData(uiNode, data, context, parentRefCounter);
            if (context.DontExecuteLifecycle)
            {
                return uiNode;
            }
            uiNode.NotifyStart();
            OnNotifyStart(uiNode);


            UniNodeLoadRefCounter canvasRefCounter = new UniNodeLoadRefCounter()
            {
                LogicRefCount = data.GetLogicCount(),
                ParentNode = uiNode,
                RefCount = data.Childrens == null || data.Childrens.Count == 0 ? 1 : data.Childrens.Count,
                Parent = parentRefCounter,
                OnRenderReadyEvent = (group) =>
                {
                    if (uiNode) uiNode.OnChildrenCreated();
                },
                OnLogicReadyEvent = (group) =>
                {
                    if (uiNode) uiNode.OnChildrenLogicReady();
                },
            };
            uiNode.OnLogicReady();
            if (canvasRefCounter.LogicRefCount == 0)
            {
                canvasRefCounter.LogicRefCount = 1;
                canvasRefCounter.OneLogicReady(uiNode);
            }

            if (data.Childrens == null || data.Childrens.Count == 0)
            {
                uiNode.OnCreated();
                canvasRefCounter.OneRenderReady(uiNode);
                return uiNode;
            }
            ForceCreateGroupChild(uiNode, data, context, canvasRefCounter);
            return uiNode;
        }

        public GameObject ClonePrimitive(int idx)
        {
            if (idx >= UniNodeLoadManager.PrimitiveShapes.Length || idx < 0)
            {
                return null;
            }

            return UniNodeLoadManager.PrimitiveShapes[idx] ? GameObject.Instantiate(UniNodeLoadManager.PrimitiveShapes[idx]) : null;
        }

        public virtual UniTextNode CreateTextNode(UniNode parent, UniTextNodeData data, UniNodeLoadContext context,
            UniNodeLoadRefCounter parentRefCounter)
        {
            var go = ClonePrimitive(0);
            if (!go)
            {
                go = new GameObject("UniTextNode");
            }

            var text = go.AddComponent<UniTextNode>();
            text.Scene = this.Scene;
            text.RuntimeFlag = context.RuntimeFlag;
            text.Owner = context.Owner;
            text.ComponentData = new UniTextColorData();
            if (data.Color != null && string.IsNullOrEmpty(data.Color.Text))
            {
                data.Color.Text = data.Text;
            }

            var comp = go.AddComponent<UniTextRenderComponent>();
            text.ApplyMaterialData(data);
            SetNodeBaseData(parent, text, data, context);
            SetRenderNodeBaseData(text, data, context);
            text.RenderComponent = comp;
            text.NotifyAwake();
            text.NotifyStart();
            OnNotifyStart(text);
            text.NotifyRenderReady();
            ParentRefCounterOneRendererReady(parentRefCounter, context.LoadWorkId, text);
            return text;
        }

        public virtual UniFakeLightNode CreateFakeLightNode(UniNode parent, UniFakeLightNodeData data, UniNodeLoadContext context,
            UniNodeLoadRefCounter parentRefCounter)
        {
            var id = data.Color.LightMode == FakeLightMode.Point ? 164 : 165;
            var go = ClonePrimitive(id);
            if (!go)
            {
                go = new GameObject("UniFakeLightNode");
            }

            var fakeLightNode = go.AddComponent<UniFakeLightNode>();
            fakeLightNode.Scene = this.Scene;
            fakeLightNode.RuntimeFlag = context.RuntimeFlag;
            fakeLightNode.Owner = context.Owner;
            fakeLightNode.ComponentData = data.Color;
            var comp = go.AddComponent<UniFakeLightRenderComponent>();
            fakeLightNode.ApplyMaterialData(data);
            SetNodeBaseData(parent, fakeLightNode, data, context);
            fakeLightNode.RemoveRuntimeFlag(UniObjectRuntimeFlag.ColliderEnable);

            SetRenderNodeBaseData(fakeLightNode, data, context);
            fakeLightNode.RenderComponent = comp;
            fakeLightNode.NotifyAwake();
            fakeLightNode.NotifyStart();
            OnNotifyStart(fakeLightNode);

            fakeLightNode.NotifyRenderReady();
            ParentRefCounterOneRendererReady(parentRefCounter, context.LoadWorkId, fakeLightNode);
            return fakeLightNode;
        }

        public virtual UniComponentsNode CreateComponnetsNode(UniNode parent, UniComponentsNodeData data,
            UniNodeLoadContext context, UniNodeLoadRefCounter parentRefCounter)
        {
            var go = new GameObject("UniComponentsNode");
            UniComponentsNode n = go.AddComponent<UniComponentsNode>();
            n.Scene = this.Scene;
            n.RuntimeFlag = context.RuntimeFlag;
            n.Owner = context.Owner;
            SetNodeBaseData(parent, n, data, context);
            ApplyNodeComponentData(n, data, context, parentRefCounter);
            if (context.DontExecuteLifecycle)
            {
                return n;
            }
            n.NotifyStart();
            OnNotifyStart(n);
            n.NotifyLogicReady();
            n.NotifyRenderReady();
            parentRefCounter.OneLogicReady(n);
            parentRefCounter.OneRenderReady(n);
            return n;
        }


        public void SetDataAndCreateChild<TNode, TData>(UniNode parent, UniGroupData data, UniNodeLoadContext context,
            UniNodeLoadRefCounter parentRefCounter, UniGroup refNode, UniCreateGroupFlow<TNode, TData> flow) where TNode : UniGroup where TData : UniGroupData
        {
            var uniReference = refNode.UniReference;
            var uniReferenceData = data.UniReferenceData;
            var n = refNode;
            var isRef = uniReference != null && uniReferenceData != null;
            if (isRef)
            {
                uniReference.SerializeRefNode = uniReference.SerializeRefNode || uniReferenceData.IsEditingVersion || uniReferenceData.IsSerializedByInheritanceChains();
                uniReference.InheritanceChains = uniReferenceData.InheritanceChains;
                uniReference.IsOpenSource = uniReference.IsOpenSource || uniReferenceData.EditForceOpen || uniReferenceData.AllowRecreate || uniReferenceData.IsOpenSourceByInheritanceChains() || (!string.IsNullOrEmpty(uniReferenceData.RefId) && !string.IsNullOrEmpty(UniMain.UserId()) && uniReferenceData.RefId.Contains(UniMain.UserId()));
                uniReference.AllowRecreate = uniReference.AllowRecreate || uniReferenceData.AllowRecreate;
                context.RuntimeFlag |= UniObjectRuntimeFlag.CreateFromUniFile | UniObjectRuntimeFlag.IsRefChild;
                var comp = n.gameObject.AddComponent<UniRefRenderComponent>();
            }
            context.BeforeCreateGroupNode?.Invoke(data);
            //SetNodeBaseData(parent, n, data, context);
            //ref可能合并过需要再设一次nodeEvents
            if (isRef && !context.RemoveNodeEvents)
            {
                SetNodeEvents(n, data);
            }
#if !UNITY_EDITOR || UNITY_SERVER
            if (!Global.Game.IsPlayMode())
#endif
            {
                if ((n.RuntimeFlag & UniObjectRuntimeFlag.CreateFromEditor) == 0)
                {
                    n.CreateCacheData(data.Childrens);
                }
            }
            flow.BeforeApplyNodeComponentData(parent, refNode, data, context, parentRefCounter);
            ApplyNodeComponentData(n, data, context, parentRefCounter);
            flow.AfterApplyNodeComponentData(parent, refNode, data, context, parentRefCounter);
            if (context.DontExecuteLifecycle)
            {
                return;
            }
            flow.BeforeNotifyStart(parent, refNode, data, context, parentRefCounter);
            n.NotifyStart();
            OnNotifyStart(n);
            flow.AfterNotifyStart(parent, refNode, data, context, parentRefCounter);
            UniNodeLoadRefCounter groupRefCounter = new UniNodeLoadRefCounter();
            groupRefCounter.LogicRefCount = data.GetLogicCount();
            groupRefCounter.ParentNode = n;
            groupRefCounter.RefCount = data.Childrens == null || data.Childrens.Count == 0 ? 1 : data.Childrens.Count;
            groupRefCounter.Parent = parentRefCounter;
            groupRefCounter.OnRenderReadyEvent = (group) =>
            {
                if (n) n.OnChildrenCreated();
            };
            groupRefCounter.OnLogicReadyEvent = (group) =>
            {
                if (n)
                {
                    n.OnChildrenLogicReady();
                    n.OnLogicReady();
                    if (uniReference != null && uniReference.InheritanceChains != null && n.Parent != null &&
                        n.Parent is UniGroup parentRefNode && parentRefNode.UniReference != null && parentRefNode.UniReference.InheritanceChains != null)
                    {
                        foreach (var inher in parentRefNode.UniReference.InheritanceChains)
                        {
                            if (inher.WorkId == n.UniReference.RefId)
                            {
                                parentRefNode.UniReference.RefTarget = n;
                                break;
                            }
                        }
                    }

                    if (isRef && uniReference.RefTarget == null)
                    {
                        uniReference.RefTarget = n;
                    }
                    flow.OnLogicReady(parent, refNode, data, context, parentRefCounter);
                }
            };
            if (context.SyncLoad)
            {
                if (groupRefCounter.LogicRefCount == 0)
                {
                    groupRefCounter.LogicRefCount = 1;
                    groupRefCounter.OneLogicReady(n);
                }

                if (data.Childrens == null || data.Childrens.Count == 0)
                {
                    n.OnCreated();
                    groupRefCounter.OneRenderReady(n);
                    return;
                }
                flow.BeforeCreateChildren(parent, refNode, data, context, parentRefCounter);
                CreateGroupChild(n, data, context, groupRefCounter);

                if (isRef)
                {
                    context.LoadWorkId = $"{uniReferenceData.RefId}_{uniReferenceData.RefVersion}";
                }
            }
            else
            {
                if (groupRefCounter.LogicRefCount == 0)
                {
                    groupRefCounter.LogicRefCount = 1;
                    groupRefCounter.OneLogicReady(n);
                }
                flow.BeforeCreateChildren(parent, refNode, data, context, parentRefCounter);
                //因为skiprender也会导致变成同步，所以logicReady提前
                CreateGroupChild(n, data, context, groupRefCounter);
                if (isRef)
                {
                    context.LoadWorkId = $"{uniReferenceData.RefId}_{uniReferenceData.RefVersion}";
                }

                if (data.Childrens == null || data.Childrens.Count == 0)
                {
                    n.OnCreated();
                    groupRefCounter.OneRenderReady(n);
                    return;
                }
            }
        }

        private UniNode CreatRefNodeAsync(UniNode parent, UniAsyncRefNodeData data, UniNodeLoadContext context, UniNodeLoadRefCounter parentRefCounter)
        {
            UniGroup group = null;
            var loader = Global.AssetModule.CreateUniDataLoader(data.UniReferenceData.RefId, data.UniReferenceData.RefVersion, null);
            if (loader == null)
            {
                parentRefCounter.OneLogicReady(null);
                parentRefCounter.OneRenderReady(null);
                return null;
            }
            loader.AddCallback((l) =>
            {
                if (!this.Scene || !this.Manager || loader.Status != UniAssetLoaderStatus.Loaded)
                {
                    parentRefCounter.OneLogicReady(null);
                    parentRefCounter.OneRenderReady(null);
                    return;
                }
                if (loader.Status == UniAssetLoaderStatus.Loaded)
                {
                    var file = loader.GetUniNodeFile(new UniNodeDataFixer(), data);
                    if (file.Context.TreeData != null)
                    {
                        if (this is UniEditNodeLoadAdapter editNodeLoadAdapter)
                        {
                            file.Context.TreeData.RecaculateId(new GenerateRefIdContext(0, editNodeLoadAdapter.IdCreater.Get()));
                        }

                        parentRefCounter.OnLogicReadyEvent += (uNode) =>
                        {
                            var uniGroup = uNode as UniGroup;
                            if (uniGroup)
                            {
                                if (uniGroup.UniReference == null)
                                {
                                    uniGroup.UniReference = new UniWorkReference();
                                }

                                uniGroup.UniReference.RefId = data.UniReferenceData.RefId;
                                uniGroup.UniReference.RefVersion = data.UniReferenceData.RefVersion;
                                uniGroup.UniReference.RefDataVersion = UniMain.DataVersion.Full;
                                uniGroup.UniReference.SerializeRefNode = true; //UI节点默认序列化
                                uniGroup.UniReference.AllowRecreate = data.UniReferenceData.AllowRecreate;
                                uniGroup.UniReference.IsOpenSource = uniGroup.UniReference.IsOpenSource || data.UniReferenceData.EditForceOpen ||
                                                                     data.UniReferenceData.AllowRecreate ||
                                                                     data.UniReferenceData.IsOpenSourceByInheritanceChains() ||
                                                                     (!string.IsNullOrEmpty(data.UniReferenceData.RefId) &&
                                                                      !string.IsNullOrEmpty(UniMain.UserId()) &&
                                                                      data.UniReferenceData.RefId.Contains(UniMain.UserId()));
                                if (uniGroup.UniReference.InheritanceChains == null)
                                {
                                    uniGroup.UniReference.InheritanceChains = new List<RefNodeInfo>();
                                }
                                else
                                {
                                    for (int j = uniGroup.UniReference.InheritanceChains.Count - 1; j >= 0; j--)
                                    {
                                        if (uniGroup.UniReference.InheritanceChains[j].WorkId == uniGroup.UniReference.RefId)
                                        {
                                            uniGroup.UniReference.InheritanceChains.RemoveAt(j);
                                        }
                                    }
                                }

                                uniGroup.UniReference.InheritanceChainsAddSelf();
                            }
                        };

                        group = CreateNode(parent, file.Context.TreeData, context, parentRefCounter) as UniGroup;
                        if (group)
                        {
                            if (group.UniReference == null)
                            {
                                group.UniReference = new UniWorkReference();
                            }

                            group.UniReference.RefId = data.UniReferenceData.RefId;
                            group.UniReference.RefVersion = data.UniReferenceData.RefVersion;
                        }
                    }
                    else
                    {
                        parentRefCounter.OneLogicReady(null);
                        parentRefCounter.OneRenderReady(null);
                    }
                }
            });
            return group;
        }

        // public virtual UniRefNode CreateRefNode2(UniNode parent, UniRefNodeData data, UniNodeLoadContext context,
        //     UniNodeLoadRefCounter parentRefCounter)
        // {
        //     var go = new GameObject(data.RefId);
        //     UniRefNode n = go.AddComponent<UniRefNode>();
        //     n.Scene = this.Scene;
        //     n.RuntimeFlag = (context.RuntimeFlag | UniObjectRuntimeFlag.IsRefNode);
        //     n.Owner = context.Owner;
        //     SetNodeBaseData(parent, n, data, context);
        //     n.RefId = data.RefId;
        //     n.RefVersion = data.RefVersion;
        //     context.SkipSpawnbox = true;
        //     context.LoadRefId = data.RefId;
        //     context.LoadRefNode = n;
        //     // if (string.IsNullOrEmpty(data.RefId))
        //     // {
        //     //     Global.GLogger.Warn($"refnode老数据,没有refId，节点id:{data.Id}");
        //     //     n.IsOpenSource = true;
        //     //     n.AllowRecreate = false;
        //     //     n.SerializeRefNode = true;
        //     //     SetRefDataAndCreateChild(parent, data, context, parentRefCounter, n);
        //     // }
        //     // else
        //      if (data.InheritanceChains == null)
        //         {
        //             if (data.RefNodesData != null)
        //             {
        //                 n.SerializeRefNode = true;
        //                 UniNodeFile file = null;
        //                 data.AssemblyDataBeforeMerge(context,out file);
        //                 n.RefDataVersion = data.RefDataVersion;
        //                 context.RefDataVersion = n.RefDataVersion;
        //                 data.RefMerge(context);
        //                 if (parent != null)
        //                 {
        //                     generateParentMetaInfoGroupData.Meta.Data.WorldMatrix = parent.transform.localToWorldMatrix;
        //                     data.GenerateMetaInfo(new GenerateMetaContext() { Root = data,NeedClone = true}, generateParentMetaInfoGroupData);
        //                 }
        //                 else
        //                 {
        //                     data.GenerateMetaInfo(new GenerateMetaContext() { Root = data,NeedClone = true }, null);
        //                 }
        //
        //               
        //                 SetDataAndCreateChild(parent, data, context, parentRefCounter, n);
        //             }
        //             else
        //             {
        //                 if (string.IsNullOrEmpty(data.RefId))
        //                 {
        //                     // Global.GLogger.Warn($"refnode老数据,没有refId，节点id:{data.Id}");
        //                     // n.IsOpenSource = true;
        //                     // n.AllowRecreate = false;
        //                     // n.SerializeRefNode = true;
        //                     // SetRefDataAndCreateChild(parent, data, context, parentRefCounter, n);\
        //
        //                     if (data.Childrens!=null&&data.Childrens.Count > 0)
        //                     {
        //                         n.SerializeRefNode = true;
        //                         n.RefDataVersion = UniMain.DataVersion.Full;
        //                         SetDataAndCreateChild(parent, data, context, parentRefCounter, n);
        //                     }
        //                     else
        //                     {
        //                         UniNodeLoadRefCounter groupRefCounter = new UniNodeLoadRefCounter();
        //                         groupRefCounter.LogicRefCount = 1;
        //                         groupRefCounter.ParentNode = n;
        //                         groupRefCounter.RefCount = 1;
        //                         groupRefCounter.Parent = parentRefCounter;
        //                         groupRefCounter.OneLogicReady(n);
        //                         groupRefCounter.OneRenderReady(n);
        //                     }
        //
        //                     
        //
        //
        //                     /////////////////
        //                 }
        //                 else
        //                 {
        //                     //历史数据，是非序列化节点但是有组件，需要当作序列化节点
        //                     if (data.Components != null && data.Components.Count > 0||
        //                         (data.Childrens!=null&&data.Childrens.Count > 0))
        //                     {
        //                         n.SerializeRefNode = true;
        //                     }
        //                     
        //                     System.Action loadRefDataCallback = () =>
        //                     {
        //                         if (!n || !Global.Game || !Scene) return;
        //                         if (data.PatchData != null) n.SerializeRefNode = true;
        //                         UniNodeFile file = null;
        //                         var fixer = data.AssemblyDataBeforeMerge(context, out file);
        //                         n.RefDataVersion = data.RefDataVersion;
        //                         context.RefDataVersion = n.RefDataVersion;
        //
        //                         data.RefMerge(context);
        //                         if (parent != null)
        //                         {
        //                             generateParentMetaInfoGroupData.Meta.Data.WorldMatrix =
        //                                 parent.transform.localToWorldMatrix;
        //                             data.GenerateMetaInfo(new GenerateMetaContext() { Root = data, NeedClone = true },
        //                                 generateParentMetaInfoGroupData);
        //                         }
        //                         else
        //                         {
        //                             data.GenerateMetaInfo(new GenerateMetaContext() { Root = data, NeedClone = true },
        //                                 null);
        //                         }
        //
        //
        //                         if (file != null)
        //                         {
        //                             n.IsOpenSource = file.OpenSource() || data.EditForceOpen;
        //                             n.AllowRecreate = file.OpenSource() || data.AllowRecreate;
        //                             if (context.CacheAssetLib) n.LocalLibrary = file.Context.AssetLibrary;
        //                             n.IsLegacy = file.Context.IsLegacyData;
        //                         }
        //
        //                         if (context.UseOriginRefScale && !n.HaveRuntimeFlag(UniObjectRuntimeFlag.IsRefChild) ||
        //                             (!n.HaveRuntimeFlag(UniObjectRuntimeFlag.CreateFromUniFile) &&
        //                              !n.HaveRuntimeFlag(UniObjectRuntimeFlag.IsRefChild) &&
        //                              n.HaveRuntimeFlag(UniObjectRuntimeFlag.CreateFromEditor) &&
        //                              !n.HaveRuntimeFlag(UniObjectRuntimeFlag.IsCopyObject)))
        //                         {
        //                             if (fixer != null)
        //                             {
        //                                 n.SetScale(fixer.OriginMetaScale);
        //                             }
        //                         }
        //                         
        //                         
        //                         SetDataAndCreateChild(parent, data, context, parentRefCounter, n);
        //
        //
        //                         
        //                     };
        //                    if (context.RefChecked)
        //                    {
        //                        //需要异步掉，服务器内存会暴涨crash
        //                        var tasks = Manager.GetTaskList(UniNodeLoadGroup.LocalPlayer);
        //                        tasks.AddLast(new UniNodeLoadTask() { Reqeust = loadRefDataCallback });
        //                   }
        //                     else
        //                     {

        //                         Global.AssetModule.LoadRefTree(data.RefId, data.RefVersion, data.PatchData,loadRefDataCallback);
        //                    }
        //                 }
        //                 
        //                 
        //             }
        //             
        //         }
        //         else
        //         {
        //             n.IsOpenSource = data.EditForceOpen || data.AllowRecreate || data.IsOpenSourceByInheritanceChains()
        //                 ||(!string.IsNullOrEmpty(data.RefId)&&!string.IsNullOrEmpty(UniMain.UserId())&& data.RefId.Contains(UniMain.UserId()));
        //             n.AllowRecreate = data.AllowRecreate;
        //             SetDataAndCreateChild(parent, data, context, parentRefCounter, n);
        //         }
        //
        //     return n;
        // }


//         public virtual UniRefNode CreateRefNode(UniNode parent, UniRefNodeData data, UniNodeLoadContext context,
//             UniNodeLoadRefCounter parentRefCounter)
//         {
//             UniNodeLoadRefCounter ugcRefCounter = new UniNodeLoadRefCounter();
//             ugcRefCounter.RefCount = 1;
//             ugcRefCounter.LogicRefCount = data.RefNodesData == null ? 1 : 0;
//             ugcRefCounter.Parent = parentRefCounter;
//             if (data.Childrens != null && data.Childrens.Count > 0)
//             {
//                 ugcRefCounter.RefCount += data.Childrens.Count;
//             }
//
//             ugcRefCounter.LogicRefCount += data.GetLogicCount();
//
//             if (parent != null)
//             {
//                 var parentRef = parent.GetComponentsInParent<UniRefNode>();
//                 foreach (var p in parentRef)
//                 {
//                     if (p.RefId == data.RefId && data.RefNodesData == null)
//                     {
//                         ugcRefCounter.OneLogicReady(null);
//                         ugcRefCounter.OneRenderReady(null);
//                         return null;
//                     }
//                 }
//             }
//
//             var go = new GameObject(data.RefId);
//             UniRefNode n = go.AddComponent<UniRefNode>();
//             n.Scene = this.Scene;
//             n.RuntimeFlag = (context.RuntimeFlag | UniObjectRuntimeFlag.IsRefNode);
//             n.Owner = context.Owner;
//             n.SerializeRefNode = data.IsEditingVersion;
//             if (n.TransformComponent != null && n.TransformComponent is UniGroupComponent groupComponent)
//             {
//                 if (data.Tags != null && data.Tags.Count > 0)
//                 {
//                     groupComponent.GroupTag = new List<string>(data.Tags.Count);
//                     groupComponent.GroupTag.AddRange(data.Tags);
//                 }
//                 if (data.OnReceivedBroadcast != null)
//                 {
//                     groupComponent.OnReceivedBroadcast = data.OnReceivedBroadcast;
//                     groupComponent.OnReceivedBroadcast.ConfigNode(n, UniGroupComponent_SLData.SLID, 20, 0);
//                     List<UniScriptNode> uniScriptNodes = groupComponent.OnReceivedBroadcast.Nodes;
//                     Dictionary<string, List<UniBroadcastScriptNode>> contextAllBroadcastEvent = Global.Game.Work.NodeFile.Context.AllBroadcastEvent;
//                     for (int i = 0; i < uniScriptNodes.Count; i++)
//                     {
//                         if (uniScriptNodes[i] is UniBroadcastScriptNode broadcastScriptNode)
//                         {
//                             if (contextAllBroadcastEvent.TryGetValue(broadcastScriptNode.BroadcastName, out var list))
//                             {
//                                 list.Add(broadcastScriptNode);
//                             }
//                             else
//                             {
//                                 contextAllBroadcastEvent.Add(broadcastScriptNode.BroadcastName, new List<UniBroadcastScriptNode>() { broadcastScriptNode });
//                             }
//                         }
//                     }
//                 }
//             }
//             var comp = n.gameObject.AddComponent<UniRefRenderComponent>();
//             SetNodeBaseData(parent, n, data, context);
// #if !UNITY_EDITOR || UNITY_SERVER
//             if (!Global.Game.IsPlayMode())
// #endif
//             {
//                 if ((n.RuntimeFlag & UniObjectRuntimeFlag.CreateFromEditor) == 0)
//                 {
//                     n.CreateCacheData(data.Childrens);
//                 }
//             }
//             n.RefId = data.RefId;
//             n.RefVersion = data.RefVersion;
//             n.IsOpenSource = data.EditForceOpen;
//             n.AllowRecreate = data.AllowRecreate;
//             ApplyNodeComponentData(n, data, context,parentRefCounter);
//             n.NotifyStart();
//             OnNotifyStart(n);
//             ugcRefCounter.ParentNode = n; 
//             ugcRefCounter.OnLogicReadyEvent = (group) =>
//             {
//                 if (n)
//                 {
//                     n.OnLogicReady();
//                     n.OnChildrenLogicReady();
//                 }
//             };
//             ugcRefCounter.OnRenderReadyEvent = (node) =>
//             {
//                 ugcRefCounter.OnRenderReadyEvent = null;
//                 if (n)
//                 {
//                     n.OnCreated();
//                     n.OnChildrenCreated();
//                 }
//             };
//             UniNodeData refNodesData = null;
//             if (data.RefNodesData != null)
//             {
//                 n.SerializeRefNode = true;
//                 n.RefDataVersion = data.RefDataVersion;
//                 if (context.RehashRefId > 0)
//                 {
//                     data.RefNodesData.RecaculateId(new GenerateRefIdContext(0,context.RehashRefId));
//                 }
//                 data.RefNodesData.GenerateMetaInfo(new GenerateMetaContext() { Root = data.RefNodesData }, data);
//                 refNodesData = data.RefNodesData.CullServerNoNeedData();
//             }
//             CreateGroupChild(n, data, context, ugcRefCounter);
//             context.LoadWorkId = $"{data.RefId}_{data.RefVersion}";
//
//             if (refNodesData != null)
//             {
//                 System.Action createAction = () =>
//                 {
//                     if (!n) return;
//                     if (!Global.Game.IsEditMode() && context.SkipRenderNode)
//                     {
//                         Scene.SpaceTree.InsertNotLoadedObj(data.RefNodesData as UniGroupData);
//                     }
//                     // OnRefNodeDataLoaded(n, data.RefNodesData, context);
//                     context.RuntimeFlag |= UniObjectRuntimeFlag.CreateFromUniFile | UniObjectRuntimeFlag.IsRefChild;
//                     //跳过依赖模型里面的出生点
//                     context.SkipSpawnbox = true;
//                     if (refNodesData.GetLogicCount() == 0)
//                     {
//                         ugcRefCounter.LogicRefCount = 1;
//                         ugcRefCounter.OneLogicReady(n);
//                     }
//
//                     TryFixRangeWeaponRotationV50(n, refNodesData as UniGroupData,  context);
//                     var childNode = CreateNode(n, refNodesData, context, ugcRefCounter);
//                     n.RefTarget = childNode;
//                     RefTargetIsSet(n);
//                 };
//                 if (context.SyncLoad)
//                 {
//                     createAction();
//                 }
//                 else
//                 {
//                     Manager.GetTaskList(context.Group).AddLast(LinkedListNodePool<UniNodeLoadTask>.QucikPool.Get(new UniNodeLoadTask() { Reqeust = createAction }));
//                 }
//             }
//             else
//             {
//                 if (data.PatchData != null)
//                 {
//                     n.SerializeRefNode = true;
//                 }
//
//                 var workType = WorkType.Model;
//                 if (context.RefWorkType != WorkType.World || context.RefWorkType != WorkType.SubWorld)
//                 {
//                     workType = context.RefWorkType;
//                 }
//
//                 bool needTime = NeedAddTimeWhenLoadRefData(data.RefId);
//                 
//                 var loader = Global.AssetModule.CreateUniDataLoader(data.RefId, data.RefVersion, needTime? new UniDataDescription(){ModifyTime =(int) System.DateTime.Now.GetTimeStamp()}:null );
//                 if (loader == null)
//                 {
//                     ugcRefCounter.OneLogicReady(n);
//                     ugcRefCounter.OneRenderReady(n);
//                     return n;
//                 }
//                 loader.AddCallback((l) =>
//                 {
//                     if (!n || !Global.Game || !Scene) return;
//                     var fixer = new UniNodeDataFixer()
//                     {
//                         WorldAssetLibrary = (Scene.WorkingType == WorkType.AvatarRoom || Scene.WorkingType == WorkType.Polycosm)
//                             ? null : Scene.Work?.NodeFile?.Context?.AssetLibrary,
//                         PatchData = data.PatchData,
//                         ResetMetaPosition = true,
//                         ResetMetaRotation = true,
//                         ResetMetaScale = true,
//                         ResetMetaPositionValue = n.transform.position,
//                         ResetMetaRotationValue = n.transform.rotation.eulerAngles,
//                         ResetMetaScaleValue = n.transform.lossyScale,
//                         IDList = new (),
//                         DisableFixPivotFlag = (context.RefWorkType == WorkType.Avatar || context.RefWorkType == WorkType.Cloth || context.RefWorkType == WorkType.HandProp)
//                     };
//                     if (context.SyncLoad && context.RefChecked)
//                     {
//                         CreateRefChild(n, data, fixer, loader.GetUniNodeFile(fixer,null), context, ugcRefCounter);
//                     }
//                     else
//                     {
//                         var task = loader.AsyncGetUniNodeFile(fixer, null);
//                         task.GetAwaiter().OnCompleted(() =>
//                         {
//                             CreateRefChild(n, data, fixer, task.Result, context, ugcRefCounter);
//                         });
//                     }
//                 });
//             }
//
//             return n;
//         }

        /// <summary>
        /// 场景里原本在的武器得转回来
        /// </summary>
        private Matrix4x4 handPropV50RotateMatrix = Matrix4x4.TRS(Vector3.zero, Quaternion.Euler(new Vector3(0, -90, -90)), Vector3.one);

        // bool TryFixRangeWeaponRotationV50(UniRefNode n,UniGroupData refNodesData, UniNodeLoadContext context)
        // {
        //     //(context.RuntimeFlag & UniObjectRuntimeFlag.IsHandProp) > 0 &&//手持
        //     if ((context.RuntimeFlag&UniObjectRuntimeFlag.OwnerByPlayer)==0 &&//表示不在人身上的
        //         (context.RuntimeFlag&UniObjectRuntimeFlag.CreateFromEditor)==0)//表示不是编辑里新拖出来的
        //     {
        //         if (n.RefDataVersion != 0 && ((UniVersionInfo)n.RefDataVersion).Major < 50)
        //         {
        //             if (refNodesData.Components != null)
        //             {
        //                 foreach (var component in refNodesData.Components)
        //                 {
        //                    if (component is UniUGCAvatarItemSceneEnvironmentComponent_SLData slData&&slData.Kind == UniUGCStoreItemInfo.Server_Attachment_Kind_Prop )
        //                    {
        //                        refNodesData.Position = handPropV50RotateMatrix * refNodesData.Position;
        //                         refNodesData.Rotation =
        //                             (handPropV50RotateMatrix.rotation * Quaternion.Euler(refNodesData.Rotation))
        //                             .eulerAngles;
        //                         n.SerializeRefNode = true;//旋转后需要把他序列化，且数据版本改了
        //                         return true;
        //                     }
        //                 }
        //             }
        //         }
        //     }
        //
        //     return false;
        // }

        // private void CreateRefChild(UniRefNode n, UniRefNodeData data,UniNodeDataFixer fixer,UniNodeFile file, UniNodeLoadContext context,UniNodeLoadRefCounter ugcRefCounter)
        // {
        //     if (!n || file?.Context?.TreeData == null)
        //     {
        //         ugcRefCounter.OneLogicReady(n);
        //         ugcRefCounter.OneRenderReady(n);
        //     }
        //     else
        //     {
        //         bool createVehicleFromUser = false;
        //         if (context.RefWorkType == WorkType.Vehicle)
        //         {
        //             if (file.Context.TreeData is UniGroupData gdata && !(file.Context.TreeData is UniRefNodeData))
        //             {
        //                
        //                 createVehicleFromUser = context.VehicleCreateSource == UniVehicleModule.VehicleCreateSource.Bag || context.VehicleCreateSource == UniVehicleModule.VehicleCreateSource.Spawner;
        //                 UniVehicle_SLData vehicleSlData = gdata.FindComponent(UniVehicle_SLData.SLID) as UniVehicle_SLData;
        //                 UniBoat_SLData boatSlData = gdata.FindComponent(UniBoat_SLData.SLID) as UniBoat_SLData;
        //                 UniVehiclePhysicalComponent_SLData vehiclePhySlData = gdata.FindComponent(UniVehiclePhysicalComponent_SLData.SLID) as UniVehiclePhysicalComponent_SLData;
        //                 gdata.MakeIdentityPose();
        //
        //                 //船的水位线记录的是相对老的bounds的中心Y,去记的localpos，新的pivot始终在bounds中心位置
        //                 if (boatSlData != null && gdata.Meta != null)
        //                 {
        //                     boatSlData.WaterLine = boatSlData.WaterLine - gdata.Meta.Data.WorldBounds.center.y /*- 0 )之前是对象（0,0，0）位置*/;
        //                 }
        //
        //                 if (vehiclePhySlData != null && gdata.Meta != null)
        //                 {
        //                     vehiclePhySlData.CenterOffset = vehiclePhySlData.CenterOffset - gdata.Meta.Data.WorldBounds.center;
        //                     if (vehiclePhySlData.Collider!=null)
        //                     {
        //                         vehiclePhySlData.Collider.Center = vehiclePhySlData.Collider.Center - gdata.Meta.Data.WorldBounds.center;
        //                     } 
        //                 }
        //
        //                 if (boatSlData==null)
        //                 {
        //                     if (!createVehicleFromUser || vehicleSlData == null || vehicleSlData.VehicleType == VehicleType.Car)
        //                     {
        //                         gdata = UniNodeDataUtility.TryCorrectionRuntimeVehicleData2(data.RefId, gdata);
        //                     }
        //                     else
        //                     {
        //                         gdata = UniNodeDataUtility.TryCorrectionRuntimeVehicleData(data.RefId, gdata);
        //                     }
        //                 }
        //
        //                 gdata.GenerateMetaInfo(new GenerateMetaContext(), null);
        //
        //                 file.Context.TreeData = gdata;
        //             }
        //             n.SerializeRefNode = true;
        //         }
        //
        //         uint seedId = 0;
        //         if (context.RehashRefId > 0)
        //         {
        //             seedId = context.RehashRefId;
        //         }
        //         else if (fixer.PatchData == null || !string.IsNullOrEmpty(file.Context.PatchError) || n.HaveRuntimeFlag(UniObjectRuntimeFlag.CreateFromEditor) || data.RefTemplateId != 0)
        //         {
        //             seedId = n.Id;
        //         }
        //
        //         if (seedId != 0)
        //         {
        //             file.Context.TreeData.RecaculateId(new GenerateRefIdContext(file.Context.TreeData.Id, seedId){IDList = fixer.GetIdList()});
        //         }
        //         if (!Global.Game.IsEditMode() && context.SkipRenderNode)
        //         {
        //             Scene.SpaceTree.InsertNotLoadedObj(file.Context.TreeData as UniGroupData);
        //         }
        //
        //         var refData = file.Context.TreeData.CullServerNoNeedData();
        //         if (context.CacheAssetLib) n.LocalLibrary = file.Context.AssetLibrary;
        //         //n.OriRawData = loader.ReponseRawData;
        //         n.IsOpenSource = file.OpenSource() || data.EditForceOpen;
        //         n.AllowRecreate = file.OpenSource();
        //         n.RefDataVersion = file.Context.Meta.Version;
        //         n.IsLegacy = file.Context.IsLegacyData;
        //         // if (n.LocalLibrary != null)
        //         // {
        //         //     Scene.RuntimeAssetLibrary.MergeNames(n.LocalLibrary, true);
        //         // }
        //
        //         //OnRefNodeDataLoaded(n, refData, context);
        //          if (file.Context.AssetLibrary != null && file.Context.TreeData is UniComponentsNodeData componentsNodeData)
        //          {
        //               Scene.RuntimeAssetLibrary.MergeInternalScript(file.Context.AssetLibrary,seedId,fixer.GetIdList());
        //          }
        //         context.RuntimeFlag |= UniObjectRuntimeFlag.CreateFromUniFile | UniObjectRuntimeFlag.IsRefChild;
        //         //跳过依赖模型里面的出生点
        //         context.SkipSpawnbox = true;
        //         bool isTryFixRangeWeaponInWorldV50 = TryFixRangeWeaponRotationV50(n,refData as UniGroupData, context);
        //         var childNode = CreateNode(n, refData, context, ugcRefCounter);
        //         if (!createVehicleFromUser && childNode)
        //         {
        //             childNode.SetPosition(Vector3.zero);
        //             childNode.SetScale(Vector3.one);
        //             if (context.RefWorkType != WorkType.Cloth && context.RefWorkType != WorkType.HandProp&&!isTryFixRangeWeaponInWorldV50)
        //             {
        //                 childNode.SetRotation(Vector3.zero);
        //             }
        //         }
        //         //编辑模式下新创建的RefNode,将节点的缩放设置为引用节点的缩放。
        //         if (context.UseOriginRefScale&&!n.HaveRuntimeFlag(UniObjectRuntimeFlag.IsRefChild) || 
        //             
        //             (!n.HaveRuntimeFlag(UniObjectRuntimeFlag.CreateFromUniFile) &&
        //              !n.HaveRuntimeFlag(UniObjectRuntimeFlag.IsRefChild) &&
        //              n.HaveRuntimeFlag(UniObjectRuntimeFlag.CreateFromEditor) &&
        //              !n.HaveRuntimeFlag(UniObjectRuntimeFlag.IsCopyObject)))
        //         {
        //             n.SetScale(fixer.OriginMetaScale);
        //         }
        //         n.RefTarget = childNode;
        //         RefTargetIsSet(n);
        //         //childNode.UpdateCullingBounds();
        //         //NodeLoaded(refData);
        //     }
        // }
        public virtual UniPlaneTextureNode CreatePlaneTextureNode(UniNode parent, UniPlaneTextureNodeData data, UniNodeLoadContext context,
            UniNodeLoadRefCounter parentRefCounter)
        {
            var go = ClonePrimitive(156);
            var planeTextureNode = go.AddComponent<UniPlaneTextureNode>();
            planeTextureNode.Scene = this.Scene;
            planeTextureNode.RuntimeFlag = context.RuntimeFlag;
            planeTextureNode.Owner = context.Owner;
            planeTextureNode.PicIco = data.PicIco;
            planeTextureNode.PicId = data.PicId;
            var comp = go.AddComponent<UniPlaneTextureRenderCompoent>();
            planeTextureNode.RenderComponent = comp;
            SetNodeBaseData(parent, planeTextureNode, data, context);
            SetRenderNodeBaseData(planeTextureNode, data, context);
            planeTextureNode.NotifyAwake();
            planeTextureNode.NotifyStart();
            OnNotifyStart(planeTextureNode);
            planeTextureNode.NotifyRenderReady();
            ParentRefCounterOneRendererReady(parentRefCounter, context.LoadWorkId, planeTextureNode);
            return planeTextureNode;
        }

        public virtual void OnPrimitiveShapeLoaded(UniPrimitiveShape s)
        {
        }

        public virtual void ConfigPrimitiveShape(UniNode parent, UniPrimitiveShape s, UniPrimitiveShapeData data, UniNodeLoadContext context)
        {
        }

        public virtual UniPrimitiveShape CreatePrimitiveShape(UniNode parent, UniPrimitiveShapeData data,
            UniNodeLoadContext context, UniNodeLoadRefCounter parentRefCounter)
        {
            GameObject go = ClonePrimitive(data.GetPoolIndex());
            //GameObject go = ClonePrimitive(Global.Pool.GetPoolIndex(data.Version - 1, data.PrefabId));
            if (go == null)
            {
                Logger.Warn("primitive not found {0}", data.GetPoolIndex());
                go = new GameObject("miss PrimitiveShape");
            }
#if UNITY_SERVER
            UniPrimitiveShape s = go.AddComponent<UniPrimitiveShape>();
#else
            UniPrimitiveShape s = go.GetComponent<UniPrimitiveShape>();
            if (!s)
            {
                Logger.Warn("UniPrimitiveShape Script Miss {0}", data.GetPoolIndex());
                s = go.AddComponent<UniPrimitiveShape>();
            }
#endif


            s.Scene = this.Scene;
            s.RuntimeFlag = context.RuntimeFlag;
            s.Owner = context.Owner;
#if UNITY_SERVER
            var comp = s.gameObject.AddComponent<UniPrimitiveRenderComponent>();
#else
            var comp = s.GetComponent<UniPrimitiveRenderComponent>();
            if (!comp)
            {
                Logger.Warn("UniPrimitiveRenderComponent Script Miss {0}", data.GetPoolIndex());
                comp = s.gameObject.AddComponent<UniPrimitiveRenderComponent>();
            }
#endif

            SetNodeBaseData(parent, s, data, context);
            SetRenderNodeBaseData(s, data, context);
            s.RenderComponent = comp;
            s.PrefabId = data.PrefabId;
            s.PrefabVersion = data.Version;
            s.Material = s.GetMaterial(0);
            s.ApplyMaterialData(data);
            OnPrimitiveShapeLoaded(s);
            s.NotifyAwake();
            s.NotifyStart();
            OnNotifyStart(s);
            s.NotifyRenderReady();
            ParentRefCounterOneRendererReady(parentRefCounter, context.LoadWorkId, s);

            return s;
        }

        protected void ConfigAssetLoader(string path, System.Action<GameObject> createAction, UniNodeLoadContext context)
        {
            var loader = Global.AssetModule.CreateLoader<UniAddressableLoader<GameObject>>(path);
            if (context.SyncLoad)
            {
                createAction.Invoke(loader.LoadAsset());
            }
            else
            {
                if (loader.IsDone)
                {
                    AddTask(context.Group, () =>
                    {
                        createAction.Invoke(loader.LoadAsset());
                    }, null);
                }
                else
                {
                    loader.AddCallback((UnityEngine.Events.UnityAction<UniAddressableLoader<GameObject>>)((l) =>
                    {
                        AddTask(context.Group, () =>
                        {
                            createAction.Invoke(loader.LoadAsset());
                        }, null);
                    }));
                }
            }
        }

        public UniCustomRenderNode CustomRenderNode(UniNode parent, GameObject renderObject, UniCustomRenderNodeData data,
            UniNodeLoadContext context, UniNodeLoadRefCounter parentRefCounter)
        {
            bool configShapeOnly = renderObject != null;
            if (renderObject == null)
            {
                renderObject = new GameObject("UniCustomRenderNode");
            }
            UniCustomRenderNode r = null;
            if (data.RenderData.GetObjectType() == typeof(UniSequenceFrameCompoent))
            {
                r = renderObject.AddComponent<UniSequenceRenderNode>();
            }
            else if (data.RenderData.GetObjectType() == typeof(UniParticleComponent))
            {
                r = renderObject.AddComponent<UniParticleRenderNode>();
            }
            else
            {
                r = renderObject.AddComponent<UniCustomRenderNode>();
            }
            r.Scene = this.Scene;
            r.RuntimeFlag = context.RuntimeFlag;
            r.Owner = context.Owner;
            r.PrefabId = data.PrefabId;
            AddComponent(r, data.RenderData);
            SetNodeBaseData(parent, r, data, context);
            SetRenderNodeBaseData(r, data, context);
            r.RenderComponent = r.GetComponent<UniRenderComponent>();
            r.NotifyAwake();
            r.NotifyStart();
            OnNotifyStart(r);
            if (configShapeOnly)
            {
                r.RenderObject = renderObject;
                r.NotifyRenderReady();
                ParentRefCounterOneRendererReady(parentRefCounter, context.LoadWorkId, r);
                return r;
            }

            bool isPrimitive = UniPrimitiveShapeData.GetPrimitiveIndex(data.PrefabId, out int idx);
            if (isPrimitive)
            {
                var privitive = ClonePrimitive(idx + 100);
                if (privitive)
                {
                    privitive.name = data.PrefabId;
                    privitive.transform.SetParent(r.transform);
                    privitive.transform.localPosition = Vector3.zero;
                    privitive.transform.localRotation = Quaternion.identity;
                    privitive.transform.localScale = Vector3.one;
                    r.RenderObject = privitive;
                }

                r.NotifyRenderReady();
                ParentRefCounterOneRendererReady(parentRefCounter, context.LoadWorkId, r);
                return r;
            }

            string prefabId = data.PrefabId;
            string path = $"prefabs/{BudLoadHelper.GetPrefabCustomPath(prefabId)}.unity3d";
            System.Action<GameObject> createAction = (prefab) =>
            {
                if (r)
                {
                    if (prefab)
                    {
                        if (r)
                        {
                            GameObject go = GameObject.Instantiate(prefab);
                            if (go)
                            {
                                go.name = prefabId;
                                go.transform.SetParent(r.transform);
                                r.RenderObject = go;
                            }
                        }
                    }
                    r.NotifyRenderReady();
                    ParentRefCounterOneRendererReady(parentRefCounter, context.LoadWorkId, r);
                }
            };
            ConfigAssetLoader(path, createAction, context);
            return r;
        }

        protected virtual UniCustomRenderNode CustomRenderNode(UniNode parent, UniCustomRenderNodeData data, UniNodeLoadContext context, UniNodeLoadRefCounter parentRefCounter)
        {
            if (data.RenderData == null || string.IsNullOrEmpty(data.PrefabId))
            {
                Logger.Error("CustomLoadError RenderData:{0}  PrefabId:{1}", data.RenderData, data.PrefabId);
                ParentRefCounterOneRendererReady(parentRefCounter, context.LoadWorkId, null);
                return null;
            }

            return CustomRenderNode(parent, null, data, context, parentRefCounter);
        }

        public virtual void OnMultShapeLoaded(UniMultShape shape)
        {
        }

        void ParentRefCounterOneRendererReady(UniNodeLoadRefCounter parentRefCounter, string loadWorkId, UniNode s)
        {
            if (parentRefCounter == null)
            {
                Logger.Error("id:{0} parentRefCounter is null", loadWorkId);
            }
            else
            {
                parentRefCounter.OneRenderReady(s);
            }
        }

        public UniMultShape CreateMultShape(UniNode parent, GameObject shapeObject, UniMultShapeData data,
            UniNodeLoadContext context, UniNodeLoadRefCounter parentRefCounter)
        {
            bool configShapeOnly = shapeObject != null;
            if (shapeObject == null)
            {
                shapeObject = new GameObject("UniMultShape");
            }
            UniMultShape s = shapeObject.GetComponent<UniMultShape>();
            if (!s)
            {
                s = shapeObject.AddComponent<UniMultShape>();
            }
            s.Scene = this.Scene;
            s.RuntimeFlag = context.RuntimeFlag;
            s.Owner = context.Owner;

            var comp = s.gameObject.GetComponent<UniMultRenderComponent>();
            if (!comp)
            {
                comp = s.gameObject.AddComponent<UniMultRenderComponent>();
            }
            s.PrefabId = data.PrefabId;
            s.ApplyMaterialData(data);
            s.RenderComponent = comp;
            SetNodeBaseData(parent, s, data, context);
            SetRenderNodeBaseData(s, data, context);
            s.NotifyAwake();
            s.NotifyStart();
            OnNotifyStart(s);
            if (string.IsNullOrEmpty(data.PrefabId))
            {
                s.NotifyRenderReady();
                ParentRefCounterOneRendererReady(parentRefCounter, context.LoadWorkId, s);
                return s;
            }

            if (!configShapeOnly)
            {
                string prefabId = data.PrefabId;
                string path = $"prefabs/{BudLoadHelper.GetPrefabCustomPath(prefabId)}.unity3d";
                System.Action<GameObject> createAction = (prefab) =>
                {
                    if (s)
                    {
                        if (prefab)
                        {
                            if (!s) return;
                            GameObject go = GameObject.Instantiate(prefab);
                            if (go)
                            {
                                go.name = prefabId;
                                comp.RenderObject = go;
                            }
                        }
                        OnMultShapeLoaded(s);
                        s.NotifyRenderReady();
                        ParentRefCounterOneRendererReady(parentRefCounter, context.LoadWorkId, s);
                    }
                };
                ConfigAssetLoader(path, createAction, context);
            }
            else
            {
                comp.RenderObject = s.gameObject;
                OnMultShapeLoaded(s);
                s.NotifyRenderReady();
                ParentRefCounterOneRendererReady(parentRefCounter, context.LoadWorkId, s);
            }

            return s;
        }

        protected virtual UniMultShape CreateMultShape(UniNode parent, UniMultShapeData data, UniNodeLoadContext context, UniNodeLoadRefCounter parentRefCounter)
        {
            return CreateMultShape(parent, null, data, context, parentRefCounter);
        }

        protected virtual void OnNotifyStart(UniNode node)
        {
        }

        public virtual void CreateGroupChild(UniGroup g, UniGroupData data, UniNodeLoadContext context, UniNodeLoadRefCounter groupRefCounter)
        {
            if (data.Childrens != null && data.Childrens.Count > 0)
            {
                int renderChild = 0;
                System.Action<UniNodeData> asyncCreate = (childData) =>
                {
                    LinkedList<UniNodeLoadTask> tasks;
                    if (childData.Meta == null)
                    {
                        tasks = Manager.GetTaskList(childData.PreLoad ? UniNodeLoadGroup.PreLoadEntity : context.Group);
                        var linkNode = LinkedListNodePool<UniNodeLoadTask>.QucikPool.Get(new UniNodeLoadTask()
                        {
                            Reqeust =
                                () =>
                                {
                                    if (g && Scene)
                                    {
                                        CreateNode(g, childData, context, groupRefCounter);
                                    }
                                }
                        });
                        tasks.AddLast(linkNode);
                        return;
                    }
                    switch (childData.Meta.LoadStatus)
                    {
                        case UniNodeLoadStatus.None:
                            childData.Meta.LoadStatus = UniNodeLoadStatus.InLoadingQueue;
                            tasks = Manager.GetTaskList(context.Group);
                            break;
                        case UniNodeLoadStatus.InPriorityLoadingQueue:
                            tasks = Manager.GetTaskList(UniNodeLoadGroup.AoiPriorityEntity);
                            break;
                        default:
                            tasks = Manager.GetTaskList(childData.PreLoad ? UniNodeLoadGroup.PreLoadEntity : context.Group);
                            break;
                    }
                    childData.Meta.LinkedListNode = LinkedListNodePool<UniNodeLoadTask>.QucikPool.Get(new UniNodeLoadTask()
                    {
                        Reqeust =
                            () =>
                            {
                                if (g && Scene)
                                {
                                    CreateNode(g, childData, context, groupRefCounter);
                                }
                            }
                    });
                    tasks.AddLast(childData.Meta.LinkedListNode);
                };
                foreach (var c in data.Childrens)
                {
                    if (context.SkipRenderNode && c is UniRenderNodeData rd)
                    {
                        renderChild++;
                        if (Scene.SpaceTree)
                        {
                            if (rd.Meta is UniRenderNodeMeta renderNodeMeta)
                            {
                                if (renderNodeMeta.Entity == null)
                                {
                                    UniSpaceNodeLoadEntity entity = new UniSpaceNodeLoadEntity(null)
                                    {
                                        Data = rd,
                                        Parent = g,
                                        RefCounter = groupRefCounter,
                                        LoadContext = context,
                                        Bounds = rd.Meta.Data.WorldBounds
                                    };
                                    renderNodeMeta.Entity = entity;
                                    Scene.SpaceTree.InsertNotLoadedObj(entity);
                                }
                                else
                                {
                                    renderNodeMeta.Entity.Parent = g;
                                    renderNodeMeta.Entity.RefCounter = groupRefCounter;
                                    renderNodeMeta.Entity.LoadContext = context;
                                    Scene.SpaceTree.CheckEntityIsLoad(renderNodeMeta.Entity);
                                }
                            }
                        }
                        continue;
                    }

                    if (context.SyncLoad)
                    {
                        CreateNode(g, c, context, groupRefCounter);
                    }
                    else
                    {
                        asyncCreate(c);
                    }
                }
            }
        }

        public virtual void ForceCreateGroupChild(UniGroup g, UniGroupData data, UniNodeLoadContext context, UniNodeLoadRefCounter groupRefCounter)
        {
            if (data.Childrens != null && data.Childrens.Count > 0)
            {
                foreach (var c in data.Childrens)
                {
                    CreateNode(g, c, context, groupRefCounter);
                }
            }
        }

        protected virtual UniDynamicGroup CreateDynamicGroup(UniNode parent, UniDynamicGroupData data, UniNodeLoadContext context,
            UniNodeLoadRefCounter parentRefCounter)
        {
            UniDynamicGroup group = null;
            if (!context.DisableDynamicGroupParent || string.IsNullOrEmpty(data.PrefabPath))
            {
                GameObject go = new GameObject("UniDynamicGroup");
                group = go.AddComponent<UniDynamicGroup>();
                group.Scene = this.Scene;
                group.RuntimeFlag = context.RuntimeFlag;
                group.Owner = context.Owner;

                SetNodeBaseData(parent, group, data, context);
                ApplyNodeComponentData(group, data, context, parentRefCounter);
                if (context.DontExecuteLifecycle)
                {
                    return group;
                }
                group.NotifyStart();
                OnNotifyStart(group);
            }
            if (string.IsNullOrEmpty(data.PrefabPath))
            {
                group.OnChildrenCreated();
                group.OnCreated();
                group.OnLogicReady();
                group.NotifyLogicReady();
                group.NotifyRenderReady();
                parentRefCounter?.OneLogicReady(group);
                parentRefCounter?.OneRenderReady(group);
#if !UNITY_SERVER
                Logger.Error("prefab path is null");
#endif
                return group;
            }
            context.SyncLoad |= context.DisableDynamicGroupParent;
            string path = data.PrefabPath;
            System.Action<GameObject> createAction = (prefab) =>
            {
                if (group || context.DisableDynamicGroupParent)
                {
                    if (prefab)
                    {
                        GameObject go = GameObject.Instantiate(prefab);
                        if (go)
                        {
                            if (context.DisableDynamicGroupParent)
                            {
                                group = go.AddComponent<UniDynamicGroup>();
                            }
                            else
                            {
                                group.transform.AddIdentityChild(go);
                            }
                            group.Target = go;
                            go.name = prefab.name;
                            List<UniNode> nodes = new List<UniNode>();
                            var components = group.GetComponentsInChildren<IUniComponent>();
                            for (int i = 0; i < components.Length; i++)
                            {
                                var comp = components[i] as MonoBehaviour;
                                var node = comp.GetComponent<UniNode>();
                                if (!node)
                                {
                                    node = comp.gameObject.AddComponent<UniGroup>();
                                }

                                if (node.Id == 0)
                                {
                                    node.Id = context.IdCreater.Get();
                                    if (group != node)
                                    {
                                        group.Childrens.Add(node);
                                    }
                                    node.Scene = Scene;
                                    node.Owner = context.Owner;
                                    node.RuntimeFlag = context.RuntimeFlag;
                                    Scene.AddNode(node);
                                    var netIdentity = node.GetComponent<NetworkIdentity>();
                                    if (netIdentity)
                                    {
                                        netIdentity.uniFlag = (byte)UniFlag.Static;
                                        netIdentity.sceneId = node.Id;
                                        netIdentity.ReinitializeNetworkBehaviours();
                                    }
                                    nodes.Add(node);
                                }
                            }

                            foreach (var node in nodes)
                            {
                                node.NotifyAwake();
                                node.NotifyStart();
                                node.NotifyLogicReady();
                                node.NotifyRenderReady();
                                if (node is UniGroup g)
                                {
                                    g.OnLogicReady();
                                    g.OnChildrenLogicReady();
                                    g.OnCreated();
                                    g.OnChildrenCreated();
                                }
                            }
                        }
                    }

                    if (!context.DisableDynamicGroupParent && group)
                    {
                        group.OnChildrenCreated();
                        group.OnCreated();
                        group.OnLogicReady();
                        group.NotifyLogicReady();
                        group.NotifyRenderReady();
                        parentRefCounter?.OneLogicReady(group);
                        parentRefCounter?.OneRenderReady(group);
                    }
                }
            };
            ConfigAssetLoader(path, createAction, context);

            return group;
        }

        protected virtual UniGroup CreateGroup(UniNode parent, UniGroupData data, UniNodeLoadContext context,
            UniNodeLoadRefCounter parentRefCounter)
        {
            context.BeforeCreateGroupNode?.Invoke(data);
            UniGroup g = null;
            GameObject go = UniNodeLoadManager.GetEmptyObject(null);
            go.SetActive(true);
            g = go.GetComponent<UniGroup>();
            g.Scene = this.Scene;
            g.RuntimeFlag = context.RuntimeFlag;
            g.Owner = context.Owner;
            g.CaptureRawData = data.CaptureRawData;
            //g.Layer = data.Layer;
            //生成节点后，立刻设置数据，绑定节点时候依赖id
            SetNodeBaseData(parent, g, data, context);
            //组件
#if !UNITY_EDITOR || UNITY_SERVER
            if (!Global.Game.IsPlayMode())
#endif
            {
                if ((g.RuntimeFlag & UniObjectRuntimeFlag.CreateFromEditor) == 0)
                {
                    g.CreateCacheData(data.Childrens);
                }
            }
            ApplyNodeComponentData(g, data, context, parentRefCounter);
            if (context.DontExecuteLifecycle)
            {
                return g;
            }
            g.NotifyStart();
            OnNotifyStart(g);
            UniNodeLoadRefCounter groupRefCounter = new UniNodeLoadRefCounter();
            groupRefCounter.LogicRefCount = data.GetLogicCount();
            groupRefCounter.ParentNode = g;
            groupRefCounter.RefCount = data.Childrens == null || data.Childrens.Count == 0 ? 1 : data.Childrens.Count;
            groupRefCounter.Parent = parentRefCounter;
            groupRefCounter.OnRenderReadyEvent = (group) =>
            {
                if (g) g.OnChildrenCreated();
            };
            groupRefCounter.OnLogicReadyEvent = (group) =>
            {
                if (g)
                {
                    g.OnChildrenLogicReady();
                    g.OnLogicReady();
                }
            };

            if (context.SyncLoad)
            {
                if (groupRefCounter.LogicRefCount == 0)
                {
                    groupRefCounter.LogicRefCount = 1;
                    groupRefCounter.OneLogicReady(g);
                }

                if (data.Childrens == null || data.Childrens.Count == 0)
                {
                    g.OnCreated();
                    groupRefCounter.OneRenderReady(g);
                    return g;
                }

                CreateGroupChild(g, data, context, groupRefCounter);
            }
            else
            {
                if (groupRefCounter.LogicRefCount == 0)
                {
                    groupRefCounter.LogicRefCount = 1;
                    groupRefCounter.OneLogicReady(g);
                }
                //因为skiprender也会导致变成同步，所以logicReady提前
                CreateGroupChild(g, data, context, groupRefCounter);


                if (data.Childrens == null || data.Childrens.Count == 0)
                {
                    g.OnCreated();
                    groupRefCounter.OneRenderReady(g);
                    return g;
                }
            }

            return g;
        }

        public TNode CreateGroupNew<TNode, TData>(UniNode parent, TData data, UniNodeLoadContext context,
            UniNodeLoadRefCounter parentRefCounter) where TNode : UniGroup where TData : UniGroupData
        {
            var flow = UniCreateGroupFlow<TNode, TData>.Create(data);
            var n = flow.CreateUniNode(data);
            n.Scene = this.Scene;
            n.Owner = context.Owner;
            n.RuntimeFlag = context.RuntimeFlag;
            var hasRef = data.UniReferenceData != null;
            if (hasRef)
            {
                n.gameObject.name = data.UniReferenceData.RefId;
                n.UniReference = new UniWorkReference();
                var refFlag = n.gameObject.AddComponent<UniGroupReferenceFlag>();
                refFlag.Group = n;
                n.RuntimeFlag |= UniObjectRuntimeFlag.IsRefNode;
                n.UniReference.RefId = data.UniReferenceData.RefId;
                n.UniReference.RefVersion = data.UniReferenceData.RefVersion;
                context.SkipSpawnbox = true;
                context.LoadRefId = data.UniReferenceData.RefId;
                context.LoadRefNode = n;
            }
            flow.BeforeSetNodeBaseData(parent, n, data, context, parentRefCounter);
            SetNodeBaseData(parent, n, data, context);
            flow.AfterSetNodeBaseData(parent, n, data, context, parentRefCounter);
            var refData = data.UniReferenceData;
            if (refData == null)
            {
                //不带引用的group
                SetDataAndCreateChild(parent, data, context, parentRefCounter, n, flow);
            }
            else
            {
                if (refData.InheritanceChains == null)
                {
                    if (refData.RefNodesData != null)
                    {
                        n.UniReference.SerializeRefNode = true;
                        UniNodeFile file = null;
                        data.AssemblyDataBeforeMerge(context, out file);
                        n.UniReference.RefDataVersion = refData.RefDataVersion;
                        context.RefDataVersion = n.UniReference.RefDataVersion;
                        data.RefMerge(context);
                        if (parent != null)
                        {
                            generateParentMetaInfoGroupData.Meta.Data.WorldMatrix = parent.transform.localToWorldMatrix;
                            data.GenerateMetaInfo(new GenerateMetaContext() { Root = data, NeedClone = true }, generateParentMetaInfoGroupData);
                        }
                        else
                        {
                            data.GenerateMetaInfo(new GenerateMetaContext() { Root = data, NeedClone = true }, null);
                        }


                        SetDataAndCreateChild(parent, data, context, parentRefCounter, n, flow);
                    }
                    else
                    {
                        if (string.IsNullOrEmpty(refData.RefId))
                        {
                            // Global.GLogger.Warn($"refnode老数据,没有refId，节点id:{data.Id}");
                            // n.IsOpenSource = true;
                            // n.AllowRecreate = false;
                            // n.SerializeRefNode = true;
                            // SetRefDataAndCreateChild(parent, data, context, parentRefCounter, n);\
                            if (data.Childrens != null && data.Childrens.Count > 0)
                            {
                                n.UniReference.SerializeRefNode = true;
                                n.UniReference.RefDataVersion = UniMain.DataVersion.Full;
                                SetDataAndCreateChild(parent, data, context, parentRefCounter, n, flow);
                            }
                            else
                            {
                                UniNodeLoadRefCounter groupRefCounter = new UniNodeLoadRefCounter();
                                groupRefCounter.LogicRefCount = 1;
                                groupRefCounter.ParentNode = n;
                                groupRefCounter.RefCount = 1;
                                groupRefCounter.Parent = parentRefCounter;
                                groupRefCounter.OneLogicReady(n);
                                groupRefCounter.OneRenderReady(n);
                            }
                        }
                        else
                        {
                            //历史数据，是非序列化节点但是有组件，需要当作序列化节点
                            if (data.Components != null && data.Components.Count > 0 ||
                                (data.Childrens != null && data.Childrens.Count > 0))
                            {
                                n.UniReference.SerializeRefNode = true;
                            }

                            System.Action loadRefDataCallback = () =>
                            {
                                if (!n || !Global.Game || !Scene) return;
                                if (refData.PatchData != null) n.UniReference.SerializeRefNode = true;
                                UniNodeFile file = null;
                                var fixer = data.AssemblyDataBeforeMerge(context, out file);
                                n.UniReference.RefDataVersion = refData.RefDataVersion;
                                context.RefDataVersion = n.UniReference.RefDataVersion;

                                data.RefMerge(context);
                                if (parent != null)
                                {
                                    generateParentMetaInfoGroupData.Meta.Data.WorldMatrix =
                                        parent.transform.localToWorldMatrix;
                                    data.GenerateMetaInfo(new GenerateMetaContext() { Root = data, NeedClone = true },
                                        generateParentMetaInfoGroupData);
                                }
                                else
                                {
                                    data.GenerateMetaInfo(new GenerateMetaContext() { Root = data, NeedClone = true },
                                        null);
                                }
                                if (file != null)
                                {
                                    n.UniReference.IsOpenSource = file.OpenSource() || refData.EditForceOpen;
                                    n.UniReference.AllowRecreate = file.OpenSource() || refData.AllowRecreate;
                                    if (context.CacheAssetLib) n.UniReference.LocalLibrary = file.Context.AssetLibrary;
                                    n.UniReference.IsLegacy = file.Context.IsLegacyData;
                                }

                                if (context.UseOriginRefScale && !n.HaveRuntimeFlag(UniObjectRuntimeFlag.IsRefChild) ||
                                    (!n.HaveRuntimeFlag(UniObjectRuntimeFlag.CreateFromUniFile) &&
                                     !n.HaveRuntimeFlag(UniObjectRuntimeFlag.IsRefChild) &&
                                     n.HaveRuntimeFlag(UniObjectRuntimeFlag.CreateFromEditor) &&
                                     !n.HaveRuntimeFlag(UniObjectRuntimeFlag.IsCopyObject)))
                                {
                                    if (fixer != null)
                                    {
                                        n.SetScale(fixer.OriginMetaScale);
                                    }
                                }
                                SetDataAndCreateChild(parent, data, context, parentRefCounter, n, flow);
                            };
                            if (context.RefChecked)
                            {
                                //需要异步掉，服务器内存会暴涨crash
                                var tasks = Manager.GetTaskList(UniNodeLoadGroup.LocalPlayer);
                                tasks.AddLast(new UniNodeLoadTask() { Reqeust = loadRefDataCallback });
                            }
                            else
                            {
                                Global.AssetModule.LoadRefTree(refData.RefId, refData.RefVersion, refData.PatchData, loadRefDataCallback);
                            }
                        }
                    }
                }
                else
                {
                    n.UniReference.IsOpenSource = refData.EditForceOpen || refData.AllowRecreate || refData.IsOpenSourceByInheritanceChains()
                                                  || (!string.IsNullOrEmpty(refData.RefId) && !string.IsNullOrEmpty(UniMain.UserId()) && refData.RefId.Contains(UniMain.UserId()));
                    n.UniReference.AllowRecreate = refData.AllowRecreate;

                    if (refData.InheritanceChains.Count > 0)
                    {
                        n.UniReference.RefDataVersion = refData.InheritanceChains[^1].DataVersion;
                    }
                    SetDataAndCreateChild(parent, data, context, parentRefCounter, n, flow);
                }
            }
            return n;
        }


        public virtual void OnRenderComponentLoaded(UniRenderComponent r)
        {
        }

        public virtual void OnCreateComponent(UniNode node, IUniComponent component)
        {
        }

        public UnityEngine.Component AddComponent(UniNode node, IUniSLData compInfo, bool executeLifecycle = true)
        {
            IUniComponent comp = node.AddUniComponent2(compInfo.GetObjectType(), false, null, false, false, executeLifecycle).Item1;
            if (executeLifecycle)
            {
                bool haveCycle = Uni.Component.UniComponentReflectionUtils.GetLifeCycle(comp.GetType(), out var cycle);
                if (haveCycle)
                {
                    cycle.OnUniDeserializeBefore(comp, node);
                    if (compInfo is IBasicSL basicSl)
                    {
                        basicSl.WriteSampleTo(comp);
                    }
                    else
                    {
                        compInfo.WriteTo(comp);
                    }
                    cycle.OnUniDeserializeAfter(comp, node);
                }
                else
                {
                    compInfo.WriteTo(comp);
                }
                UniComponentReflectionUtils.ConfigNode(node, comp);
                OnCreateComponent(node, comp);
            }
            return comp as UnityEngine.Component;
        }

        public void ApplyNodeComponentData(UniComponentsNode node, UniComponentsNodeData data, UniNodeLoadContext context, UniNodeLoadRefCounter parentRefCounter)
        {
            node.CreateBasicComponent();
            if (node.TransformComponent != null)
            {
                if (data.BasicComponent == null)
                {
                    if (!context.DontExecuteLifecycle)
                    {
                        OnCreateComponent(node, node.TransformComponent);
                    }
                }
                else
                {
                    AddComponent(node, data.BasicComponent, !context.DontExecuteLifecycle);
                }
                if (node.TransformComponent is UniGroupComponent groupComponent &&
                     groupComponent.OnReceivedBroadcast != null && groupComponent.OnReceivedBroadcast.Nodes.Count > 0)
                {
                    List<UniScriptNode> uniScriptNodes = groupComponent.OnReceivedBroadcast.Nodes;
                    groupComponent.ScriptCount += uniScriptNodes.Count;
                    Dictionary<string, List<UniBroadcastScriptNode>> contextAllBroadcastEvent = Global.Game.Work.NodeFile.Context.AllBroadcastEvent;
                    for (int i = 0; i < uniScriptNodes.Count; i++)
                    {
                        if (uniScriptNodes[i] is UniBroadcastScriptNode broadcastScriptNode)
                        {
                            broadcastScriptNode.OwnerNode = node;
                            if (broadcastScriptNode.BroadcastName != null)
                            {
                                if (contextAllBroadcastEvent.TryGetValue(broadcastScriptNode.BroadcastName, out var list))
                                {
                                    list.Add(broadcastScriptNode);
                                }
                                else
                                {
                                    contextAllBroadcastEvent.Add(broadcastScriptNode.BroadcastName, new List<UniBroadcastScriptNode>() { broadcastScriptNode });
                                }
                            }
                        }
                    }
                }
            }
            if (node.HaveRuntimeFlag(UniObjectRuntimeFlag.NoComponents))
            {
                return;
            }
            var dataList = data.Components;
            if (dataList == null || dataList.Count == 0) return;
            bool isFromEditor = (context.RuntimeFlag & UniObjectRuntimeFlag.CreateNewFromEditor) != 0;
            repeatTypeCheck.Clear();
            foreach (var compInfo in dataList)
            {
                if (!repeatTypeCheck.Add(compInfo.GetSLID())) continue;
                if (context.EnableDisabledComponents && context.DisabledComponentsList != null)
                {
                    if (context.DisabledComponentsList.Contains(compInfo.GetSLID()))
                    {
                        if (ShowDisableComponentToast)
                        {
                            ShowDisableComponentToast = false;
                            if (Global.Game?.Scene != null && !Global.Game.Scene.IsPlaying && Global.Game?.Work != null)
                            {
                                if (!Global.Game.IsSinglePlayerMode())
                                {
                                    UIHelper.Instance.ShowToast("editor_Toast_ComponentDisabled_Multiple".GetLanguageStr());
                                }
                                else
                                {
                                    UIHelper.Instance.ShowToast("editor_Toast_ComponentDisabled_Single".GetLanguageStr());
                                }
                            }
                        }

                        continue;
                    }
                }
                if (context.SkipSpawnbox && compInfo.GetSLID() == UniSpawnBox_SLData.SLID) continue;
                if (context.SkipUseComponent)
                {
                    if (compInfo.GetSLID() == UniUseComponent_SLData.SLID)
                    {
                        continue;
                    }
                }
                if (isFromEditor)
                {
                    if (compInfo.GetSLID() == UniEditInfoComponent_SLData.SLID)
                    {
                        var rNode = node.GetComponentInParent<UniGroupReferenceFlag>();
                        if (rNode && rNode.Group && rNode.Group.IsRef)
                        {
                            rNode.Group.UniReference.SerializeRefNode = true;
                        }
                        continue;
                    }
                }
                var comp = AddComponent(node, compInfo, !context.DontExecuteLifecycle);
                if (compInfo.GetSLID() == UniUGCAvatarItemSceneEnvironmentComponent_SLData.SLID)
                {
                    var s = (UniUGCAvatarItemSceneEnvironmentComponent)comp;
                    if (s.NeedMirror)
                    {
                        var counter = s.CreateMirrorNeedCloneData(data, context);
                        parentRefCounter.LogicRefCount += 1;
                        parentRefCounter.RefCount += 1;
                        counter.Parent = parentRefCounter;
                        counter.ParentNode = node;
                    }
                }
            }


            context.EditorAddToScene?.Invoke(node);
            var netIdentity = node.GetComponent<Mirror.NetworkIdentity>();
            if (netIdentity)
            {
                netIdentity.InitializeNetworkBehaviours();
            }
        }

        protected virtual void SetNodeEvents(UniNode node, UniNodeData data)
        {
            // if (node.TransformComponent != null)
            // {
            //     if (data.OnSpawnedNodeEvents!=null)
            //     {
            //         UniHash spawnHash = new UniHash();
            //         spawnHash.Append("OnSpawnedNodeEvents");
            //         spawnHash.Append(node.TransformComponent.GetType().Name);
            //         node.TransformComponent.OnSpawnedNodeEvents = data.OnSpawnedNodeEvents;
            //         node.TransformComponent.OnSpawnedNodeEvents.ConfigNode(node,UniGroupComponent_SLData.SLID,5, (int)spawnHash.GetHashCode());
            //     }
            //     if (data.OnDestroyedNodeEvents!=null)
            //     {
            //         UniHash destroyHash = new UniHash();
            //         destroyHash.Append("OnDestroyedNodeEvents");
            //         destroyHash.Append(node.TransformComponent.GetType().Name);
            //         node.TransformComponent.OnDestroyedNodeEvents = data.OnDestroyedNodeEvents;
            //         node.TransformComponent.OnDestroyedNodeEvents.ConfigNode(node,UniGroupComponent_SLData.SLID,7, (int)destroyHash.GetHashCode());
            //     }
            // }
        }

        public virtual void SetRenderNodeBaseData(UniRenderNode node, UniRenderNodeData data, UniNodeLoadContext context)
        {
            node.ColliderDisable = data.ColliderDisable;
            node.DisableCameraCollision = data.DisableCameraCollision;
        }

        protected virtual void SetNodeBaseData(UniNode parent, UniNode node, UniNodeData data, UniNodeLoadContext context)
        {
            node.Id = data.Id;
            node.EditModeHideState = data.EditModeHideState;
            node.LockState = data.LockState;

            node.SetParent(parent, needNotifyParent: (context.RuntimeFlag & UniObjectRuntimeFlag.CreateFromEditor) != 0);
            node.SetPosition(data.Position);
            node.SetRotation(data.Rotation);
            node.SetScale(data.Scale);
            if (node.TransformComponent != null)
            {
                node.TransformComponent.IsActive = !data.isDisActive;

                if (!context.RemoveNodeEvents)
                {
                    SetNodeEvents(node, data);
                }
            }
            if (node.Parent)
            {
                node.RuntimeFlag |= node.Parent.RuntimeFlag;
            }

            if (node is UniGroup group)
            {
                group.TemplateId = data.RefTemplateId;
            }

            if (node.EditModeHideState)
            {
                node.AddRuntimeFlag(UniObjectRuntimeFlag.HideInEditMode);
            }
            node.RemoveRuntimeFlag(UniObjectRuntimeFlag.CreateFromUniFile);
            node.RemoveRuntimeFlag(UniObjectRuntimeFlag.CreateNewFromEditor);
            if (!node.HaveRuntimeFlag(UniObjectRuntimeFlag.NoComponents) &&
                !node.HaveRuntimeFlag(UniObjectRuntimeFlag.DontAddToScene))
            {
                Scene.AddNode(node);
                data.Id = node.Id;
            }
            if (data.Meta != null)
            {
                data.Meta.LoadStatus = UniNodeLoadStatus.Loaded;
            }
#if UNITY_EDITOR
            node.name = node.Id.ToString();
#endif
        }

        public virtual void AddTask(UniNodeLoadGroup group, Action task, UniNodeData data)
        {
            if (task != null)
            {
                var tasks = Manager.GetTaskList(group);
                tasks.AddLast(LinkedListNodePool<UniNodeLoadTask>.QucikPool.Get(new UniNodeLoadTask() { Reqeust = task }));
            }
        }

        public IUniNodeOwner GetRootOwner()
        {
            switch (Global.GetMainWorkType())
            {
                case WorkType.Avatar:
                case WorkType.Cloth:
                case WorkType.HandProp:
                    return Global.Game.Players.GetLocalPlayer();
                default:
                    return Scene;
            }
        }

        public UniObjectRuntimeFlag GetRootRuntimeFlagByWorkType()
        {
            UniObjectRuntimeFlag defaultRuntimeFlag = UniObjectRuntimeFlag.CreateFromUniFile | UniObjectRuntimeFlag.ColliderEnable;
            switch (Global.GetMainWorkType())
            {
                case WorkType.HandProp:
                    defaultRuntimeFlag |= UniObjectRuntimeFlag.IsHandProp;
                    if (Scene.EditType != SceneEditType.Edit)
                        defaultRuntimeFlag &= ~UniObjectRuntimeFlag.ColliderEnable;
                    break;
                case WorkType.Cloth:
                    defaultRuntimeFlag |= UniObjectRuntimeFlag.IsCloth;
                    if (Scene.EditType != SceneEditType.Edit)
                        defaultRuntimeFlag &= ~UniObjectRuntimeFlag.ColliderEnable;
                    break;
                case WorkType.Vehicle:
                    defaultRuntimeFlag |= UniObjectRuntimeFlag.IsVehicle;
                    break;
                case WorkType.Avatar:
                    if (Scene.EditType != SceneEditType.Edit)
                        defaultRuntimeFlag &= ~UniObjectRuntimeFlag.ColliderEnable;
                    break;
            }

            return defaultRuntimeFlag;
        }

        public virtual void Destroy()
        {
            IsInitialized = false;
        }
    }
```



`UniNodeLoadAdapter`

类用于在 Unity 中管理和加载节点对象。该类包含多个字段和方法，用于处理节点的初始化、加载、组件管理、位置和旋转设置、父子关系管理、导出数据等功能。

首先，类中定义了几个字段，包括静态的 `Logger` 和 `generateParentMetaInfoGroupData`，用于记录日志信息和生成父节点元信息组数据。`Scene` 属性返回当前的场景对象。`IsInitialized` 字段用于指示是否已初始化。`Manager` 字段用于存储节点加载管理器的引用。`disabledComponentList` 和 `repeatTypeCheck` 分别用于存储禁用的组件列表和重复类型检查的哈希集合。`ShowDisableComponentToast` 是一个静态布尔字段，用于指示是否显示禁用组件的提示信息。

`Initialize` 方法用于初始化 `UniNodeLoadAdapter` 类。方法接受一个字符串类型的参数 `name` 和一个 `UniNodeLoadManager` 类型的参数 `mgr`，并将 `mgr` 赋值给 `Manager` 字段。然后，将 `IsInitialized` 设置为 `true`，并调用 `generateParentMetaInfoGroupData.GenerateMetaInfo` 方法生成元信息。

`Load` 方法用于加载节点对象。方法接受四个参数：父节点 `parent`、节点数据 `data`、加载上下文 `context` 和两个可选的回调函数 `onRenderReadyEvent` 和 `onLogicReadyEvent`。方法首先创建一个 `UniNodeLoadRefCounter` 对象 `dataRefCounter`，并将回调函数赋值给其对应的事件。然后，检查并设置禁用的组件列表。接着，调用 `CreateNode` 方法创建节点对象，并返回该节点。

`NeedAddTimeWhenLoadRefData` 方法用于判断是否需要在加载引用数据时添加时间戳。方法接受一个字符串类型的参数 `mapId`，并根据条件返回布尔值。

`CreateNode` 方法用于创建节点对象。方法接受四个参数：父节点 `parent`、节点数据 `data`、加载上下文 `context` 和引用计数器 `parentRefCounter`。方法使用 `switch` 表达式根据 `data` 的类型调用相应的创建方法，并返回创建的节点对象。

`CreateUINode` 方法用于创建 UI 节点。方法接受四个参数：父节点 `parent`、节点数据 `data`、加载上下文 `context` 和引用计数器 `parentRefCounter`。方法首先检查数据类型和父节点类型，然后创建 UI 节点对象，并设置其属性和组件数据。最后，调用 `ForceCreateGroupChild` 方法创建子节点，并返回 UI 节点对象。

`ClonePrimitive` 方法用于克隆原始对象。方法接受一个整数类型的参数 `idx`，并根据索引克隆相应的原始对象。

`CreateTextNode` 方法用于创建文本节点。方法接受四个参数：父节点 `parent`、节点数据 `data`、加载上下文 `context` 和引用计数器 `parentRefCounter`。方法首先克隆或创建新的文本节点对象，并设置其属性和组件数据。最后，调用 `ParentRefCounterOneRendererReady` 方法通知引用计数器渲染准备就绪，并返回文本节点对象。

`CreateFakeLightNode` 方法用于创建假光源节点。方法接受四个参数：父节点 `parent`、节点数据 `data`、加载上下文 `context` 和引用计数器 `parentRefCounter`。方法首先克隆或创建新的假光源节点对象，并设置其属性和组件数据。最后，调用 `ParentRefCounterOneRendererReady` 方法通知引用计数器渲染准备就绪，并返回假光源节点对象。

`CreateComponnetsNode` 方法用于创建组件节点。方法接受四个参数：父节点 `parent`、节点数据 `data`、加载上下文 `context` 和引用计数器 `parentRefCounter`。方法首先创建新的组件节点对象，并设置其属性和组件数据。最后，调用 `ParentRefCounterOneRendererReady` 方法通知引用计数器渲染准备就绪，并返回组件节点对象。

`SetDataAndCreateChild` 方法用于设置数据并创建子节点。方法接受六个参数：父节点 `parent`、组数据 `data`、加载上下文 `context`、引用计数器 `parentRefCounter`、引用节点 `refNode` 和创建组流程 `flow`。方法首先设置引用节点的属性和组件数据，然后调用 `CreateGroupChild` 方法创建子节点。

`CreatRefNodeAsync` 方法用于异步创建引用节点。方法接受四个参数：父节点 `parent`、异步引用节点数据 `data`、加载上下文 `context` 和引用计数器 `parentRefCounter`。方法首先创建一个 `UniGroup` 对象 `group`，并调用 `Global.AssetModule.CreateUniDataLoader` 方法创建数据加载器。然后，添加回调函数处理加载完成后的操作，并返回 `group` 对象。

`CreatePlaneTextureNode` 方法用于创建平面纹理节点。方法接受四个参数：父节点 `parent`、平面纹理节点数据 `data`、加载上下文 `context` 和引用计数器 `parentRefCounter`。方法首先克隆或创建新的平面纹理节点对象，并设置其属性和组件数据。最后，调用 `ParentRefCounterOneRendererReady` 方法通知引用计数器渲染准备就绪，并返回平面纹理节点对象。

`CreatePrimitiveShape` 方法用于创建原始形状节点。方法接受四个参数：父节点 `parent`、原始形状数据 `data`、加载上下文 `context` 和引用计数器 `parentRefCounter`。方法首先克隆或创建新的原始形状节点对象，并设置其属性和组件数据。最后，调用 `ParentRefCounterOneRendererReady` 方法通知引用计数器渲染准备就绪，并返回原始形状节点对象。

`ConfigAssetLoader` 方法用于配置资源加载器。方法接受三个参数：资源路径 `path`、创建操作 `createAction` 和加载上下文 `context`。方法根据同步加载或异步加载的条件调用相应的加载方法，并执行创建操作。

`CustomRenderNode` 方法用于创建自定义渲染节点。方法接受五个参数：父节点 `parent`、渲染对象 `renderObject`、自定义渲染节点数据 `data`、加载上下文 `context` 和引用计数器 `parentRefCounter`。方法首先检查渲染对象是否为空，如果为空则创建新的渲染对象。然后，根据渲染数据类型添加相应的组件，并设置节点的属性和组件数据。最后，调用 `ParentRefCounterOneRendererReady` 方法通知引用计数器渲染准备就绪，并返回自定义渲染节点对象。

`CreateMultShape` 方法用于创建多形状节点。方法接受四个参数：父节点 `parent`、形状对象 `shapeObject`、多形状数据 `data`、加载上下文 `context` 和引用计数器 `parentRefCounter`。方法首先检查形状对象是否为空，如果为空则创建新的形状对象。然后，设置节点的属性和组件数据，并根据条件加载资源。最后，调用 `ParentRefCounterOneRendererReady` 方法通知引用计数器渲染准备就绪，并返回多形状节点对象。

`CreateGroupChild` 方法用于创建组的子节点。方法接受四个参数：组节点 `g`、组数据 `data`、加载上下文 `context` 和引用计数器 `groupRefCounter`。方法遍历组数据的子节点，根据条件同步或异步创建子节点。

`ForceCreateGroupChild` 方法用于强制创建组的子节点。方法接受四个参数：组节点 `g`、组数据 `data`、加载上下文 `context` 和引用计数器 `groupRefCounter`。方法遍历组数据的子节点，并调用 `CreateNode` 方法创建子节点。

`CreateDynamicGroup` 方法用于创建动态组。方法接受四个参数：父节点 `parent`、动态组数据 `data`、加载上下文 `context` 和引用计数器 `parentRefCounter`。方法首先检查是否禁用动态组父节点或数据的预制路径是否为空。如果为空则创建新的动态组对象，并设置其属性和组件数据。然后，根据条件加载资源并执行创建操作。最后，调用 `ParentRefCounterOneRendererReady` 方法通知引用计数器渲染准备就绪，并返回动态组对象。

`CreateGroup` 方法用于创建组。方法接受四个参数：父节点 `parent`、组数据 `data`、加载上下文 `context` 和引用计数器 `parentRefCounter`。方法首先创建新的组对象，并设置其属性和组件数据。然后，调用 `CreateGroupChild` 方法创建子节点。最后，调用 `ParentRefCounterOneRendererReady` 方法通知引用计数器渲染准备就绪，并返回组对象。

`CreateGroupNew` 方法用于创建新的组。方法接受四个参数：父节点 `parent`、组数据 `data`、加载上下文 `context` 和引用计数器 `parentRefCounter`。方法首先创建新的组对象，并设置其属性和组件数据。然后，根据引用数据调用 `SetDataAndCreateChild` 方法创建子节点。最后，调用 `ParentRefCounterOneRendererReady` 方法通知引用计数器渲染准备就绪，并返回组对象。

`ApplyNodeComponentData` 方法用于应用节点组件数据。方法接受四个参数：组件节点 `node`、组件节点数据 `data`、加载上下文 `context` 和引用计数器 `parentRefCounter`。方法首先创建基础组件，并设置节点的属性和组件数据。然后，遍历组件数据列表，根据条件添加组件并执行生命周期方法。最后，调用 `InitializeNetworkBehaviours` 方法初始化网络行为。

`SetNodeEvents` 方法用于设置节点事件。方法接受两个参数：节点 `node` 和节点数据 `data`。方法根据条件设置节点的生成和销毁事件。

`SetRenderNodeBaseData` 方法用于设置渲染节点的基础数据。方法接受三个参数：渲染节点 `node`、渲染节点数据 `data` 和加载上下文 `context`。方法设置节点的碰撞器禁用和相机碰撞禁用属性。

`SetNodeBaseData` 方法用于设置节点的基础数据。方法接受四个参数：父节点 `parent`、节点 `node`、节点数据 `data` 和加载上下文 `context`。方法设置节点的 ID、编辑模式隐藏状态、锁定状态、父节点、位置、旋转和缩放等属性。然后，根据条件设置节点的运行时标志，并将节点添加到场景中。

`AddTask` 方法用于添加任务。方法接受三个参数：任务组 `group`、任务 `task` 和节点数据 `data`。方法将任务添加到任务列表中。

`GetRootOwner` 方法用于获取根节点的所有者。方法根据主工作类型返回相应的所有者对象。

`GetRootRuntimeFlagByWorkType` 方法用于根据工作类型获取根节点的运行时标志。方法根据主工作类型设置默认的运行时标志，并返回该标志。

`Destroy` 方法用于销毁 `UniNodeLoadAdapter` 类。方法将 `IsInitialized` 设置为 `false`。

