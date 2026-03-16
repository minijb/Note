
```c#
    [System.Flags]
    public enum UniNodeNetworkFlag : byte
    {
        None = 0,
        Register = 1 << 0,
        RequireChange = 1 << 1,
        SyncAnyData = 1 << 2
    }

    public interface INodePoseChangeListener
    {
        void OnSetPosition(Vector3 position);
        void OnSetRotation(Vector3 rotation);
        void OnSetScale(Vector3 scale);
    }
    [UniModApi]
    public abstract class UniNode : MonoBehaviour
    {
        public static UniLogger Logger = UniLogManager.Get(nameof(UniNode));

        public virtual UniNodeChildren Childrens { get; } = null;

        [Sirenix.OdinInspector.ShowInInspector]
        public UniNodeNetworkFlag NetworkState { get; private set; } = UniNodeNetworkFlag.None;

        [Sirenix.OdinInspector.ShowInInspector]
        public UniNodeLoadState LoadState = UniNodeLoadState.None;
        [Sirenix.OdinInspector.ShowInInspector]
        public bool isClient => !Global.IsServerOnly();
        [Sirenix.OdinInspector.ShowInInspector]
        public bool isServer => !Global.IsClientOnly();
        public bool isServerOnly => Global.IsServerOnly();
        public bool isClientOnly => Global.IsClientOnly();

        private static List<UniPrimitiveRenderComponent> PrimitiveCalculateCacheList = new List<UniPrimitiveRenderComponent>();
        private UniPhysicsComponent m_PhysicsComponent;
        private static List<IUniComponent> findListCache = new List<IUniComponent>();
        private static Dictionary<System.Type, IUniComponent> findCacheType = new Dictionary<System.Type, IUniComponent>();
        private HashSet<(string, UnitUseType)> usedKeySet = new HashSet<(string, UnitUseType)>();

#if UNITY_EDITOR
        [Sirenix.OdinInspector.ShowInInspector]
        public uint AuthNodeId
        {
            get
            {
                if (authCharacterId > 0)
                {
                    var character = Global.Game.Characters.GetCharacterByNetid(authCharacterId);
                    if (character == null)
                    {
                        return 0;
                    }
                    else
                    {
                        return character.OwnerId;

                    }
                }

                return 0;
            }
        }
#endif
        public bool SyncAnyNetData
        {
            get
            {
                return HaveNetworkFlag(UniNodeNetworkFlag.SyncAnyData);
            }
            set
            {
                if (value) AddNetworkFlag(UniNodeNetworkFlag.SyncAnyData);
                else RemoveNetworkFlag(UniNodeNetworkFlag.SyncAnyData);
            }
        }

        [Sirenix.OdinInspector.ShowInInspector]
        public uint authCharacterId { get; private set; }
        [Sirenix.OdinInspector.ShowInInspector]
        public bool hasAuthority => (Global.IsHost() && Global.Game && Global.Game.IsEditMode()) 
                || (authCharacterId > 0 && UniGameCharacters.LocalId == authCharacterId);
        [Sirenix.OdinInspector.ShowInInspector]
        public virtual bool isLocalPlayer => hasAuthority && Id == authCharacterId;
        public UniObjectRuntimeFlag RuntimeFlag;
        public UniNode Parent;
        public UniScene Scene;
        public uint Id;
        public INodePoseChangeListener EditorPoseChangeListener;
        public UniBasicComponent TransformComponent { get; protected set; }
        public IUniNodeOwner Owner;
        public UniCustomComponent CustomComponent;
        /// <summary>
        /// 1隐藏，0显示
        /// </summary>
        public bool EditModeHideState;
        /// <summary>
        /// 1锁定 ，0 不锁
        /// </summary>
        public bool LockState;
        //是否显示addcompnent按钮

        public bool isShowAddComp = true;
        protected virtual UniBasicComponent NewBasicComponent()
        {
            var comp = new UniBasicComponent(this);
            UniComponentReflectionUtils.ConfigNode(this,comp);
            return comp;
        }
        public void CreateBasicComponent()
        {
            if(ReferenceEquals(TransformComponent, null))
            {
                TransformComponent = NewBasicComponent();
                if (TransformComponent != null)
                {
                    TransformComponent.OnUniAwake(this);
                }
            }
        }

        protected virtual void Awake()
        {
            CreateBasicComponent();
        }

        public virtual void OnUniStart()
        {
            UniMain.ComponentSyncModule.TryApplySyncData(this);
        }
        public virtual void AddRuntimeFlagRecursive(UniObjectRuntimeFlag runtimeFlag)
        {
            AddRuntimeFlag(runtimeFlag);
        }
        public virtual void RemoveRuntimeFlagRecursive(UniObjectRuntimeFlag runtimeFlag)
        {
            RemoveRuntimeFlag(runtimeFlag);
        }
        public void StartAuthority(uint cid)
        {
            authCharacterId = cid;
        }

        public void StopAuthority()
        {
            authCharacterId = 0;
        }

        // public UniRuntimeAssetLibrary GetGlobalLibrary()
        // {
        //     return Scene?.RuntimeAssetLibrary;
        // }

        // public UniRuntimeAssetLibrary GetLocalLibrary()
        // {
        //     UniRefNode refNode = GetComponentInParent<UniRefNode>();
        //     if (refNode)
        //     {
        //         return refNode.LocalLibrary;
        //     }
        //
        //     return GetGlobalLibrary();
        // }

        // public bool SetName(string name)
        // {
        //     var lib = GetLocalLibrary();
        //     if (lib != null) return lib.SetNodeName(Scene, Id, name);
        //     return false;
        // }

        // public string GetName()
        // {
        //     var lib = GetLocalLibrary();
        //     if (lib != null) return lib.GetNodeName(Id);
        //     return Id.ToString();
        // }

        public void AddRuntimeFlag(UniObjectRuntimeFlag flag)
        {
            RuntimeFlag |= flag;
        }

        public void RemoveRuntimeFlag(UniObjectRuntimeFlag flag)
        {
            RuntimeFlag &= ~flag;
        }

        [Sirenix.OdinInspector.Button]
        public bool HaveRuntimeFlag(UniObjectRuntimeFlag flag)
        {
            return (RuntimeFlag & flag) > 0;
        }

        public bool EqualRuntimeFlag(UniObjectRuntimeFlag flag)
        {
            return (RuntimeFlag & flag) == flag;
        }

        public UniPhysicsComponent GetUniPhysicsComponent(){
            if(m_PhysicsComponent==null){
                m_PhysicsComponent = this.GetComponentInParent<UniPhysicsComponent>(true);
            }
            return m_PhysicsComponent;
        }
        public List<UnityEngine.Component> GetUniComponents()
        {
            return transform.GetComponents<IUniComponent>().Select(o => (UnityEngine.Component)o).ToList();
        }
        public void GetUniComponents(List<IUniComponent> s)
        {
            transform.GetComponents(s);
            s.Add(TransformComponent);
        }
        protected virtual void OnExportBasicComponent(UniNodeData data)
        {
            
        }
        public virtual UniNodeData Export(UniNodeData data, UniNodeExportContext context)
        {
            data.Position = transform.localPosition;
            data.Scale = transform.localScale;
            data.Rotation = transform.localEulerAngles;
            data.Id = Id;
            data.EditModeHideState = EditModeHideState;
            data.LockState = LockState;
            if (TransformComponent != null)
            {
                data.isDisActive = !this.TransformComponent.IsActive;
                if (UniComponentReflectionUtils.GetMeta(TransformComponent.GetType(), out var meta))
                {
                    var basicSL = meta.NewSL();
                    meta.LifecycleMethod.OnUniSerializeBefore(TransformComponent,this,context);
                    ((IBasicSL)basicSL).ReadSampleFrom(TransformComponent);
                    meta.LifecycleMethod.OnUniSerializeAfter(TransformComponent,this,context);
                    if (context != null)
                    {
                        meta.CollectionScript.Invoke(TransformComponent,basicSL,context.ScriptList);
                        meta.LifecycleMethod.OnUniCollectionScript(TransformComponent, basicSL, context.ScriptList);
                    }
                    data.BasicComponent = basicSL;
                    OnExportBasicComponent(data);
                }
                
            }
            #if UNITY_EDITOR
            else
            {
                Logger.Warn("TransformComponent is null {0}",Id);
            }
            #endif
            return data;
        }
        public virtual void ClearTemplateID()
        {

        }

        protected virtual void OnAddChildren(UniNode child, bool needNotifyParent = false)
        {

        }
        protected virtual void OnRemoveChildren(UniNode child, bool needNotifyParent = false)
        {

        }

        public virtual void ChangeAllChildMeshColliderConvex(bool flag)
        {

        }
        // public virtual void SetParent(UniNode parent)
        // {
        //     if (parent == Parent) return;
        //     var oldParent = this.Parent;
        //     Parent = parent;
        //     this.transform.SetParent(Parent?.transform);
        //     this.NotifyParentChange(oldParent);
        //     if (oldParent)
        //     {
        //         oldParent.OnRemoveChildren(this);
        //     }
        //     if (parent)
        //     {
        //         parent.OnAddChildren(this);
        //     }
        // }


        public virtual void SetParent(UniNode parent, bool isUndoRedo = false, bool needNotifyParent = false)
        {
            if (parent == Parent) return;

            var oldParent = this.Parent;
            Parent = parent;
            if (isUndoRedo&& (this is UniUINode)){
                var disable = UniMain.Game.Scene.PlayerUIRoot.GetDisableTran();
                this.transform.SetParent(disable);
            }
            else{
                this.transform.SetParent(Parent?.transform);
            }
            this.NotifyParentChange(oldParent);
            if (oldParent)
            {
                oldParent.OnRemoveChildren(this, needNotifyParent);
            }
            if (parent)
            {
                parent.OnAddChildren(this, needNotifyParent);
            }
        }

        public virtual int GetPrefabId() { return -1; }

        public void SetWorldPositionAndRotation(Vector3 position, Quaternion rotation)
        {
            transform.SetPositionAndRotation(position, rotation);
        }

        public void SetIdentityPose()
        {
            SetPosition(Vector3.zero);
            SetRotation(Vector3.zero);
            SetScale(Vector3.one);
        }
        [UniModApi]
        public void SetPosition(Vector3 position)
        {
            transform.localPosition = position;
            EditorPoseChangeListener?.OnSetPosition(position);
        }

        public void SetRotation(Vector3 eulerAngles)
        {
            transform.localEulerAngles = eulerAngles;
            EditorPoseChangeListener?.OnSetRotation(eulerAngles);
        }

        public void SetScale(Vector3 scale)
        {
            transform.localScale = scale;
            EditorPoseChangeListener?.OnSetScale(scale);
        }

        public void SetWorldPosition(Vector3 position)
        {
            transform.position = position;
            EditorPoseChangeListener?.OnSetPosition(transform.localPosition);
        }

        public void SetWorldRotation(Vector3 eulerAngles)
        {
            transform.eulerAngles = eulerAngles;
            EditorPoseChangeListener?.OnSetRotation(transform.localEulerAngles);
        }

        public void SetActive(bool active, bool record = true)
        {
            this.gameObject.SetActive(active);
        }

        public void SetTransform(Vector3 position, Vector3 eulerAngles, Vector3 scale)
        {
            SetPosition(position);
            SetRotation(eulerAngles);
            SetScale(scale);
        }

        public void SetTransform(Vector3 position, Quaternion eulerAngles, Vector3 scale)
        {
            SetTransform(position, eulerAngles.eulerAngles, scale);
        }

        [Sirenix.OdinInspector.Button]
        public void MoveToZeroByBounds()
        {
            LODBatcher.RemoveSpaceTree(this);
            SetPosition(Vector3.zero);
            SetPivotToCenter(false, true);
            LODBatcher.AddSpaceTree(this);
        }

        [Sirenix.OdinInspector.Button]
        public void SetPivotToCenter(bool keepPosition, bool moveUpByBounds)
        {
            Transform parent = transform.parent;
            Quaternion quat = transform.rotation;
            Vector3 scale = transform.localScale;
            Vector3 pos = transform.position;
            transform.parent = null;
            transform.localScale = Vector3.one;
            transform.rotation = Quaternion.identity;
            //�ϵ����ݼ���
            Vector3 initPos = new Vector3(0, -1000, 0);
            transform.position = initPos;
            bool getBoundsOk = this.GetBounds(out Bounds bounds, true, true);
            if (getBoundsOk)
            {
                for (int i = 0; i < transform.childCount; i++)
                {
                    var child = transform.GetChild(i);
                    Vector3 p = child.localPosition - bounds.center + transform.position;
                    var uniObj = child.GetComponent<UniNode>();
                    if (uniObj)
                    {
                        uniObj.SetPosition(p);
                    }
                    else
                    {
                        child.localPosition = p;
                    }
                }
            }

            transform.SetParent(parent);
            transform.rotation = quat;
            transform.localScale = scale;
            transform.position = pos;
            if (getBoundsOk && (keepPosition || moveUpByBounds))
            {
                var newPos = transform.position;
                if (keepPosition)
                {
                    newPos += bounds.center - initPos;
                }

                if (moveUpByBounds)
                {
                    newPos.y += bounds.extents.y;
                }

                transform.position = newPos;
                SetPosition(transform.localPosition);
            }

            // UpdateCullingBounds();
            // StatePlay.Current?.Scene?.CullingGroupManager.SetCullingGroupBoundingSphere(this);
        }


        public virtual void Destroy()
        {
            if (Parent is UniGroup group)
            {
                group.Childrens.Remove(this);
            }
            
            var netIdentity = gameObject.GetComponent<Mirror.NetworkIdentity>();
            var nodes = this.gameObject.GetComponentsInChildren<UniNode>();
            foreach (var n in nodes)
            {
                n.NotifyDestroy();
                if (Scene) Scene.RemoveNode(n);
            }

            if (gameObject)
            {
                if (netIdentity && netIdentity.isServer)
                {
                    Mirror.NetworkServer.Destroy(gameObject);
                }
                else
                {
                    GameObject.Destroy(gameObject);
                }
            }
        }
        public void InvokeNewComponentEvent(IUniComponent component, IUniComponentEditor editor = null)
        {
            if (Global.Game.IsEditMode())
            {
                if(editor == null)editor = UniComponentReflectionUtils.GetComponentEditor(component);
                if (editor != null)
                {
                    var attr = component.GetType().GetCustomAttribute<EditUniComponentRequireAttribute>();
                    if (attr != null)
                    {
                        int ret= Global.Game.Scene.ComponentManager.CheckIsAddComponent(this, attr.reqType);

                        if (ret == 0)
                        {
                            this.AddUniComponent2(attr.reqType, true);
                        }
                    }
                    editor.OnAddToSceneFromInspector();
                    editor.Attach();
                }
            }
            
            if (component is UniBaseComponent baseComponent)
            {
                baseComponent.OnUniStart(this);
                editor?.AfterUniStart();
                if (LoadState == UniNodeLoadState.Complete)
                {
                    baseComponent.OnUniLogicReady(this);
                    baseComponent.OnUniRenderReady(this);
                }
            }
        }
        public System.ValueTuple<IUniComponent, IUniComponentEditor> AddUniComponent2(
            System.Type componenttype, bool isNewComponent = false, IUniSLData data = null, bool isAddInteractData = true, bool configNode = true, bool executeLifecycle = true)
        {
            IUniComponent comp;
            bool isBasic = typeof(UniBasicComponent).IsAssignableFrom(componenttype);
            if (isBasic)
            {
                comp = TransformComponent;
            }
            else
            {
                comp = gameObject.AddComponent(componenttype) as IUniComponent;
            }
            if (!isBasic && comp == null)
            {
                throw new Exception($"is not uni comp {componenttype}");
            }
            if (!isBasic)
            {
                this.UniAwake(comp);
            }
            if (!executeLifecycle)
            {
                return (comp, null);
            }

            IUniComponentEditor editor = null;
            if (!isBasic && Global.Game.IsEditMode())
            {
                editor = Uni.Component.UniComponentReflectionUtils.CreateComponentEditor(comp, gameObject);
                if (isAddInteractData && editor is UniInteractEditor interactEditor)
                {
                    interactEditor.IsRelyOn = true;
                }
            }  
           
            if (data != null)
            {
                if (data is IBasicSL basicSl)
                {
                    basicSl.WriteSampleTo(comp);
                }
                else
                {
                    data.WriteTo(comp);
                }
            }
            if(configNode) UniComponentReflectionUtils.ConfigNode(this,comp);
            if (!isBasic && isNewComponent)
            {
                InvokeNewComponentEvent(comp, editor);
            }

            return (comp, editor);
        }

        public IUniComponent AddUniComponent(System.Type type)
        {
            return AddUniComponent2(type).Item1;
        }
        public T AddUniComponent<T>() where T : UnityEngine.Component
        {
            return AddUniComponent(typeof(T)) as T;
        }
        public virtual void RemoveUniComponent(IUniComponent comp)
        {
            if (Global.Game.IsEditMode())
            {
                var editor = UniComponentReflectionUtils.GetComponentEditor(comp);
                if (editor != null)
                {
                    editor.Dettach();
                    editor.NotifyComponentDestroy();
                }

            }
            DestroyImmediate(comp as MonoBehaviour);
        }

        public UniTransformData GetTransformData()
        {
            if (transform is RectTransform rect)
            {
                return new UniTransformData() { Position = transform.localPosition, Rotation = transform.localEulerAngles, Scale = transform.localScale, SizeDelta = rect.sizeDelta };
            }
            else
            {
                return new UniTransformData() { Position = transform.localPosition, Rotation = transform.localEulerAngles, Scale = transform.localScale };
            }
        }

        public void RefAllModelCollider(int lodLevel = -1)
        {
            GetComponentsInChildren<UniPrimitiveRenderComponent>(PrimitiveCalculateCacheList);
            foreach (UniPrimitiveRenderComponent model in PrimitiveCalculateCacheList)
            {
                model.ChangeCollider(lodLevel);
            }

            PrimitiveCalculateCacheList.Clear();
        }

        [Sirenix.OdinInspector.Button]
        public void ChangeEditCollider(out TraversalState resultColliderState)
        {
            if (LoadState != UniNodeLoadState.Complete)
            {
                UIHelper.Instance.ShowToast("Edit_Modes_Model loading".GetLanguageStr());
                resultColliderState = TraversalState.Ignore;
                return;
            }

            var state = SetChildrenNodesWithModeValue(TraversalMode.Collider);
            resultColliderState = state;
            if (state == TraversalState.Inconsistent)
            {
                resultColliderState = SetChildrenNodesWithModeValue(TraversalMode.Collider, false);
            }
        }

        public virtual TraversalState SetChildrenNodesWithModeValue(TraversalMode mode, bool? enforce = null)
        {
            return TraversalState.Ignore;
        }
        public virtual void GetEditComponents(List<IUniComponentEditor> result)
        {
            GetComponents(result);
        }

        public bool IsChildrenRenderOver()
        {
            if (LoadState != UniNodeLoadState.Complete)
            {
                UIHelper.Instance.ShowToast("Edit_Modes_Model loading".GetLanguageStr());
                return false;
            }
            return true;
        }

        public UniNodeFile ToNodeFile(WorkType workType, bool openSource, bool serializeEnv, bool keepPivot = false,
            bool isRemoveRefNode = false, bool serializeCanvas = false, bool needBlackBoard = true, UniRuntimeAssetLibrary assetLibrary = null,
            string earlyCollectRefId = null)
        {
            UniFileType fileType = ((workType == WorkType.World || workType == WorkType.SubWorld) && this == Scene.Root) ? UniFileType.UniScene : UniFileType.UniData;
            UniNodeFile file = new UniNodeFile(Global.DataVersion.Full, fileType, openSource ? UniFileFlag.OpenSource : UniFileFlag.None);
            file.Context.TreeData = this.CreateExportData();
            file.Context.AssetLibrary = assetLibrary == null ? Scene.RuntimeAssetLibrary : assetLibrary;
            UniNodeExportContext context = new UniNodeExportContext() { Root = this, IsRemoveRefNode = isRemoveRefNode };

            if (!string.IsNullOrEmpty(earlyCollectRefId))
            {
                context.EarlyCollectRefInfos = new List<UniNodeRefInfo>();
                if (this is UniGroup g)
                {
                    g.CollectRefInfos(context, earlyCollectRefId);
                }
            }

            try
            {
                var parent = this.transform.parent;
                if (this != Scene.Root&&this is not UniUINode)
                {
                    this.transform.SetParent(null);
                }
                this.Export(file.Context.TreeData, context);
                if (this != Scene.Root && this is not UniUINode)
                {
                    this.transform.SetParent(parent);
                }
                //把组件的引用合并入总引用
                if (context != null && context.ComponentUsedRefInfos != null && context.ComponentUsedRefInfos.Count > 0)
                {
                    file.Context.Meta.AddRefNodeInfos(context.ComponentUsedRefInfos);
                }
                if (context != null && context.EarlyCollectRefInfos != null && context.EarlyCollectRefInfos.Count > 0)
                {
                    file.Context.Meta.AddRefNodeInfos(context.EarlyCollectRefInfos);
                }


                if (serializeEnv)
                {
                    file.Context.EnvData = new UniGroupData();
                    Scene.Env.Export(file.Context.EnvData, context);
                    file.Context.UIRootData = new UniUIRootData();
                    if (Scene.PlayerUIRoot)
                    {
                        Scene.PlayerUIRoot.Export(file.Context.UIRootData, context);
                    }
                    if (Scene.DefaultCameraNode != null)
                    {
                        file.Context.CameraData = new UniGroupData();
                        Scene.DefaultCameraNode.Export(file.Context.CameraData, context);
                    }
                }

                // if (this != Scene.Root)
                // {
                    ProcessScriptUsedIDList(context.ScriptList);
                // }
            }
            catch (System.Exception ex)
            {
                Debug.LogException(ex);
                return null;
            }



            return file;
        }

        public UniScriptMachineData_SLData GetScriptMachineData(IUniSLData slData)
        {
            if (slData is UniUGCScript_SLData ugcData)
            {
                return ugcData.Data;
            }
            else if (slData is UniBroadcastScriptNode_SLData broadcastData)
            {
                return broadcastData.Data;
            }
            else if (slData is UniCustomComponentScriptNode_SLData customData)
            {
                return customData.Data;
            }
            else
            {
                return null;
            }
        }

        public void ProcessScriptUsedIDList(List<(UniScriptNode, IUniSLData)> scriptList)
        {
            if (scriptList != null && scriptList.Count > 0)
            {
                for(int i = 0; i < scriptList.Count; i++)
                {
                    var scriptData = scriptList[i];
                    var scriptNode = scriptData.Item1;
                    var scriptSLData = scriptData.Item2;
                    if (scriptNode is UniUGCScript ugcScript)
                    {
                        UniScriptMachineData_SLData machineData = GetScriptMachineData(scriptSLData);
                        if (machineData == null)
                            continue;
                        var collectData = CollectScriptUnitUseIDList(ugcScript);
                        var idList = collectData.Item1;
                        if (machineData.UsedInnerNodeIdList == null)
                        {
                            machineData.UsedInnerNodeIdList = new List<uint>();
                        }
                        machineData.UsedInnerNodeIdList.Clear();
                        if (idList != null && idList.Count > 0)
                        {
                            machineData.UsedInnerNodeIdList.AddRange(idList);

                            var machine = ugcScript.GetUniScriptMachine();
                            machineData.Data = machine.GetSerializeJson();
                            
                        }
                        
                        if (machineData.UnitUseDataList == null)
                        {
                            machineData.UnitUseDataList = new List<UnitUseData_SLData>();
                        }
                        machineData.UnitUseDataList.Clear();
                        if (collectData.Item2 != null && collectData.Item2.Count > 0)
                        {
                            foreach (var item in collectData.Item2)
                            {
                                var useDataSLData = UniComponentReflectionUtils.NewSLData(typeof(UnitUseData)) as UnitUseData_SLData;
                                useDataSLData.ReadFrom(item);
                                machineData.UnitUseDataList.Add(useDataSLData);
                            }
                        }

                        if (ugcScript != null)
                        {
                            var machine = ugcScript.GetUniScriptMachine();
                            if (machine != null && machine.graph != null)
                            {
                                if (machineData.InnerScriptDataList == null)
                                {
                                    machineData.InnerScriptDataList = new List<InnerScriptData_SLData>();
                                }
                                machineData.InnerScriptDataList.Clear();
                                var unitList = machine.graph.units;
                                foreach (var unit in unitList)
                                {
                                    if (unit is PropertyScriptNodeSetterUnit scriptUnit && scriptUnit.OutputValue.hasValidConnection)
                                    {
                                        if (Global.Game.Scene.RuntimeAssetLibrary.InternalScript.TryGetValue(
                                                scriptUnit.ScriptGuid, out var script))
                                        {

                                            var innerCollectData = CollectScriptUnitUseIDList(script);
                                            var innerScriptIDList = innerCollectData.Item1;
                                            if (innerScriptIDList != null && innerScriptIDList.Count > 0)
                                            {
                                                machineData.InnerScriptDataList.Add(new InnerScriptData_SLData()
                                                {
                                                    InnerScriptGuid = scriptUnit.ScriptGuid,
                                                    UsedInnerNodeIdList = innerScriptIDList
                                                });

                                                // script.Data.
                                                var innerMachine = script.GetUniScriptMachine();
                                                script.Data.Data = innerMachine.GetSerializeJson();
                                            }

                                            Global.Game.Scene.RuntimeAssetLibrary.SerializeInternalScript.TryAdd(scriptUnit.ScriptGuid, script);
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

        public (List<uint>, List<UnitUseData>) CollectScriptUnitUseIDList(UniUGCScript script)
        {
            List<uint> idList = new List<uint>();
            List<UnitUseData> useDataList = new List<UnitUseData>();
            usedKeySet.Clear();
            if (script != null)
            {
                if (script is UniBroadcastScriptNode broadcastScriptNode)
                {
                    var broadcast = UniMain.Game.Scene.EnvComponent.AllBroadcast.FirstOrDefault(a =>
                        a.name == broadcastScriptNode.BroadcastName);

                    if (broadcast != null)
                    {
                        var newBroadcastInfo = new BroadcastInfo() { name = broadcast.name, };
                        newBroadcastInfo.parameterName.AddRange(broadcast.parameterName);
                        newBroadcastInfo.parameterTypes.AddRange(broadcast.parameterTypes);
                        newBroadcastInfo.parameterAssetTypes.AddRange(broadcast.parameterAssetTypes);
                        if (usedKeySet.Add((broadcastScriptNode.BroadcastName, UnitUseType.Broadcast)))
                        {
                            useDataList.Add(new UnitUseData()
                            {
                                UseType = UnitUseType.Broadcast, 
                                OriginKey = broadcastScriptNode.BroadcastName,
                                UseBroadcastInfo = newBroadcastInfo
                            });
                        }
                    }
                }
                
                var machine = script.GetUniScriptMachine();
                if (machine != null && machine.graph != null)
                {
                    var unitList = machine.graph.units;
                    var sortList = unitList.ToList();
                    sortList.Sort(((a, b) => b != null && a != null ? a.guid.GetHashCode().CompareTo(b.guid.GetHashCode()) : 1));
                    var uniModModule = UniMain.ModuleManager.Get<UniModModule>();
                    foreach (var unit in sortList)
                    {
                        if (unit is BaseScriptUnit scriptUnit)
                        {
                            bool hasValidConnection = false;
                            if (unit.valueOutputs != null)
                            {
                                foreach (var output in unit.valueOutputs)
                                {
                                    if (output.hasValidConnection)
                                    {
                                        hasValidConnection = true;
                                        break;
                                    }
                                }
                            }

                            if (!hasValidConnection)
                            {
                                if (scriptUnit.Enter != null)
                                {
                                    if (!scriptUnit.Enter.hasValidConnection)
                                    {
                                        if (scriptUnit.Exit != null)
                                        {
                                            if (!scriptUnit.Exit.hasValidConnection)
                                            {
                                                continue;
                                            }
                                        }
                                    }
                                }
                                else
                                {
                                    if (scriptUnit.Exit != null)
                                    {
                                        if (!scriptUnit.Exit.hasValidConnection)
                                        {
                                            continue;
                                        }
                                    }
                                }
                            }
                        }
                        
                        BaseNodeCompUnit nodeUnit = null;
                        if ((unit is GetNodeUnit getnode && getnode.OutputNode.hasValidConnection)
                            || (unit is PropertyUniNodeSetterUnitV2 v2 && v2.SelectIndex == 2))
                        {
                            nodeUnit = unit as BaseNodeCompUnit;
                            if (nodeUnit.GroupObjectRef.UintKey != 0)
                            {
                                if (script.Data.UsedInnerNodeIdList != null && nodeUnit.GroupObjectRef.idIndex != 0 && nodeUnit.GroupObjectRef.idIndex <= script.Data.UsedInnerNodeIdList.Count)
                                {
                                    nodeUnit.GroupObjectRef.UintKey = script.Data.UsedInnerNodeIdList[nodeUnit.GroupObjectRef.idIndex - 1];
                                }
                                UniNode node = UniMain.Game.Scene.GetNode(nodeUnit.GroupObjectRef.UintKey);
                                if (node == null)
                                {
                                    node = UniMain.Game.Players.Get(nodeUnit.GroupObjectRef.UintKey);
                                }

                                if (node != null && script.OwnerNode != null && node.transform.IsChildOf(script.OwnerNode.transform))
                                {
                                    nodeUnit.GroupObjectRef.idIndex = idList.Count + 1;
                                    idList.Add(nodeUnit.GroupObjectRef.UintKey);
                                }
                                else
                                {
                                    nodeUnit.GroupObjectRef.idIndex = 0;
                                }
                            }
                        }
                        else if (unit is GetGlobalBlackboardVariableUnit globalUnit)
                        {
                            if (!string.IsNullOrEmpty(globalUnit.BlackboardKey))
                            {
                                var baseValue = uniModModule.Blackboard.GetValue(globalUnit.BlackboardKey);
                                if(baseValue != null && usedKeySet.Add((globalUnit.BlackboardKey, UnitUseType.GlobalBlackBoard)))
                                {
                                    useDataList.Add(new UnitUseData()
                                    {
                                        UseType = UnitUseType.GlobalBlackBoard,
                                        OriginKey = globalUnit.BlackboardKey,
                                        UseValueType = baseValue.GetValueType()
                                    });
                                }
                            }
                        }
                        else if(unit is GetObjectCommandUnit commandUnit && commandUnit.CheckIsBroadcastCommand())
                        {
                            // if (!useDataList.ContainsKey(unit.guid.ToString()))
                            {
                                var broadcast = UniMain.Game.Scene.EnvComponent.AllBroadcast.FirstOrDefault(a =>
                                    a.name == commandUnit.BroadcastName);
                                if (broadcast != null && usedKeySet.Add((commandUnit.BroadcastName, UnitUseType.Broadcast)))
                                {
                                    var newBroadcastInfo = new BroadcastInfo() { name = broadcast.name, };
                                    newBroadcastInfo.parameterName.AddRange(broadcast.parameterName);
                                    newBroadcastInfo.parameterTypes.AddRange(broadcast.parameterTypes);
                                    newBroadcastInfo.parameterAssetTypes.AddRange(broadcast.parameterAssetTypes);
                                    useDataList.Add(new UnitUseData()
                                    {
                                        UseType = UnitUseType.Broadcast,
                                        OriginKey = commandUnit.BroadcastName,
                                        UseBroadcastInfo = newBroadcastInfo
                                    });
                                }
                            }
                        }
                        else if (unit is GetUniPropertyDataUnit getUniPropertyUnit && getUniPropertyUnit.CheckPlayerVariable(out var index))
                        {
                            if (getUniPropertyUnit.PropertyInfo != null && getUniPropertyUnit.PropertyInfo.Count > index)
                            {
                                var key = getUniPropertyUnit.PropertyInfo[index];
                                if (!string.IsNullOrEmpty(key))
                                {
                                    var baseValue = UniMain.Game.Scene.WorldComponent.PlayerBlackboardData.PlayerBlackboard.GetValue(key);
                                    if (baseValue != null && usedKeySet.Add((key, UnitUseType.PlayerBlackBoard)))
                                    {
                                        useDataList.Add(new UnitUseData()
                                        {
                                            UseType = UnitUseType.PlayerBlackBoard,
                                            IsCloudVariable = baseValue.IsCloudVar,
                                            OriginKey = key,
                                            UseValueType = baseValue.GetValueType()
                                        });
                                    }
                                }
                            }
                        }
                    }
                }
            }

            return (idList, useDataList);
        }

        public byte[] ToRawData(WorkType workType, bool openSource, bool serializeEnv, bool keepPivot = false, bool isRemoveRefNode = false, bool needBlackBoard = true)
        {
            var f = ToNodeFile(workType, openSource, serializeEnv, keepPivot, isRemoveRefNode);
            f.Context.NeedBlackBoard = needBlackBoard;
            return f.ToRawData();
        }
#if UNITY_EDITOR
        [Sirenix.OdinInspector.Button]
        void EditorSave(bool fixPivot = false, bool isRemoveRefNode = false, bool clearBlackBoard = false, bool clearInteractChinese = true)
        {
            if (clearBlackBoard)
            {
                var uniModModule = UniMain.ModuleManager.Get<UniModModule>();
                if (uniModModule != null && uniModModule.Blackboard != null)
                {
                    uniModModule.Blackboard.Clear();
                }
            }

            if (clearInteractChinese)
            {
                var temp = transform.GetComponentsInChildren<IUniComponentEditor>();
                foreach (var v in temp)
                {
                    v.ClearInteractTextData();
                }
            }

            ClearTemplateID();
            var path = UnityEditor.EditorUtility.SaveFilePanel("保存数据", Uni.UniCachePath.GetCacheDir(UniCachePathType.Model), "new_uni_data", "uni");
            var file = this.Scene.SerializeNode(this, true, false, !fixPivot, isRemoveRefNode);
            System.IO.File.WriteAllBytes(path, file.ToRawData());
        }


        [Sirenix.OdinInspector.Button]
        void EditorLoad(bool combineLib = true)
        {
            var path = UnityEditor.EditorUtility.OpenFilePanel("加载数据", Uni.UniCachePath.GetCacheDir(UniCachePathType.Model), "uni");
            if (System.IO.File.Exists(path))
            {
                var data = System.IO.File.ReadAllBytes(path);
                var f = Data.UniNodeFile.FromRawData(data, 0, data.Length, new Data.UniNodeDataFixer(), null);
                if (f != null)
                {
                    if (combineLib)
                    {
                        f.Context.AssetLibrary.CombineTo(Scene.RuntimeAssetLibrary);
                    }
                    f.Context.TreeData.ClearId();
                    var node = this.Scene.DynamicCreateNode(this.Scene.Root, f.Context.TreeData, new UniNodeLoadContext() { Owner = this.Owner, RuntimeFlag = this.RuntimeFlag, SyncLoad = true });
                    node.transform.localPosition = Vector3.zero;
                    //node.UpdateCullingBounds();
                    UnityEditor.Selection.activeObject = node.gameObject;
                }
            }
        }
#endif


        public virtual void GetUniComponents(List<IUniComponent> result, bool includeChild = false, params System.Type[] uniCompType)
        {
            findCacheType.Clear();
            findListCache.Clear();
            if (gameObject == null || transform == null) return;
            GetComponents<IUniComponent>(findListCache);
            if (TransformComponent != null)
                findCacheType.Add(TransformComponent.GetType(), TransformComponent);
            foreach (var comp in findListCache)
            {
                findCacheType[comp.GetType()] = comp;
            }

            if (uniCompType != null && uniCompType.Length > 0)
            {
                for (int i = 0; i < uniCompType.Length; i++)
                {
                    if (findCacheType.TryGetValue(uniCompType[i], out var sl))
                    {
                        result.Add(sl);
                    }
                }
            }
            else
            {
                foreach (var sl in findCacheType.Values)
                {
                    result.Add(sl);
                }
            }
            findCacheType.Clear();
            findListCache.Clear();
        }

        public bool IsLoadFinished()
        {
            //GroupNode:ChildrenLogicOver
            return LoadState == UniNodeLoadState.TreeLogicReady ||
                    LoadState == UniNodeLoadState.Complete;
        }
        public bool ShowInEdit()
        {
            bool isHide = this is UniRenderNode && HaveRuntimeFlag(UniObjectRuntimeFlag.HideInEditMode);
            return !isHide;
        }

        #region API

        [UniModApi]
        public UniModBlackboard GetGlobalBlackboard()
        {
            return UniMain.ModuleManager.Get<UniModModule>().Blackboard;
        }
        [UniModApi]
        public UniModBlackboard GetLoclaBlackBoard()
        {
            return UniMain.ModuleManager.Get<UniModModule>().Blackboard; ;
        }

        [UniModApi]
        public void SetPositionXYZ(float x, float y, float z)
        {
            SetPosition(new Vector3(x, y, z));
        }
        [UniModApi]
        public Vector3 GetPosition()
        {
            return transform.localPosition;
        }

        [UniModApi]
        public IUniComponent GetUniComponent(string name)
        {
            return transform.GetComponents<IUniComponent>().FirstOrDefault(o => o.GetType().Name == name);
        }

        public virtual IUniComponent GetUniComponent(Type uniCompType)
        {
            if (typeof(UniBasicComponent).IsAssignableFrom(uniCompType))
            {
                return TransformComponent;
            }
            else
            {
                return gameObject.GetComponent(uniCompType) as IUniComponent;
            }
        }

        public UniCustomComponentInfo GetUniComponentIncludeCustom(string componentName = null)
        {
            var customComponent = GetUniComponent(typeof(UniCustomComponent)) as UniCustomComponent;
            if (customComponent != null)
            {
                var result = customComponent.CustomComponentInfo.Find(x => x.Guid == componentName);
                return result;
            }

            return null;
        }

        public string GetNodeName()
        {
            return Scene.RuntimeAssetLibrary.GetNodeName(Id);
        }
        /// <summary>
        /// 慎重调用，虚拟节点专用方法
        /// </summary>
        public void ClearTransform()
        {
            TransformComponent = null;
        }
        #endregion

        //network
        public void AddNetworkFlag(UniNodeNetworkFlag flag)
        {
            var f = NetworkState;
            NetworkState |= flag;
            // if (f != NetworkState)
            // {
            //     this.NotifyNetworkFlagChange();
            // }
        }

        public void RemoveNetworkFlag(UniNodeNetworkFlag flag)
        {
            var f = NetworkState;
            NetworkState &= ~flag;
            // if (f != NetworkState)
            // {
            //     this.NotifyNetworkFlagChange();
            // }
        }

        public bool HaveNetworkFlag(UniNodeNetworkFlag flag)
        {
            return (NetworkState & flag) > 0;
        }
    }
```

`UniNode`

类是一个抽象类，继承自 `MonoBehaviour`，用于在 Unity 中管理和操作节点对象。该类包含多个字段和方法，用于处理节点的网络状态、加载状态、组件管理、位置和旋转设置、父子关系管理、导出数据等功能。

首先，类中定义了一个静态的 `Logger` 字段，用于记录日志信息。`Childrens` 属性返回节点的子节点集合，默认为 `null`。`NetworkState` 属性表示节点的网络状态，使用 `UniNodeNetworkFlag` 枚举类型。`LoadState` 属性表示节点的加载状态，使用 `UniNodeLoadState` 枚举类型。`isClient`、`isServer`、`isServerOnly` 和 `isClientOnly` 属性用于判断节点是否在客户端或服务器上运行。`PrimitiveCalculateCacheList` 是一个静态列表，用于缓存计算的原始渲染组件。`m_PhysicsComponent` 字段用于存储物理组件的引用。`findListCache` 和 `findCacheType` 是两个静态集合，用于缓存查找的组件。`usedKeySet` 是一个哈希集合，用于存储已使用的键值对。

在 Unity 编辑器中，`AuthNodeId` 属性用于获取授权节点的 ID。`SyncAnyNetData` 属性用于判断和设置节点是否同步任何网络数据。`authCharacterId` 属性存储授权角色的 ID。`hasAuthority` 属性用于判断节点是否具有权限。`isLocalPlayer` 属性用于判断节点是否为本地玩家。`RuntimeFlag` 字段用于存储节点的运行时标志。`Parent` 字段用于存储节点的父节点。`Scene` 字段用于存储节点所属的场景。`Id` 字段用于存储节点的唯一标识符。`EditorPoseChangeListener` 字段用于监听编辑器中的姿态变化。`TransformComponent` 字段用于存储节点的变换组件。`Owner` 字段用于存储节点的所有者。`CustomComponent` 字段用于存储自定义组件。`EditModeHideState` 和 `LockState` 字段用于存储编辑模式下的隐藏和锁定状态。`isShowAddComp` 字段用于指示是否显示添加组件按钮。

`NewBasicComponent` 方法用于创建新的基础组件，并配置节点。`CreateBasicComponent` 方法用于创建基础组件并调用其 `OnUniAwake` 方法。`Awake` 方法用于在节点唤醒时创建基础组件。`OnUniStart` 方法用于在节点启动时应用同步数据。`AddRuntimeFlagRecursive` 和 `RemoveRuntimeFlagRecursive` 方法用于递归添加和移除运行时标志。`StartAuthority` 和 `StopAuthority` 方法用于启动和停止节点的权限。`AddRuntimeFlag` 和 `RemoveRuntimeFlag` 方法用于添加和移除运行时标志。`HaveRuntimeFlag` 和 `EqualRuntimeFlag` 方法用于判断节点是否具有指定的运行时标志。

`GetUniPhysicsComponent` 方法用于获取物理组件的引用。`GetUniComponents` 方法用于获取节点的所有组件。`OnExportBasicComponent` 方法用于在导出基础组件时执行额外操作。`Export` 方法用于导出节点数据。`ClearTemplateID` 方法用于清除模板 ID。`OnAddChildren` 和 `OnRemoveChildren` 方法用于在添加和移除子节点时执行额外操作。`ChangeAllChildMeshColliderConvex` 方法用于更改所有子节点的网格碰撞器的凸面状态。`SetParent` 方法用于设置节点的父节点，并通知父节点变化。`GetPrefabId` 方法用于获取预制件 ID。`SetWorldPositionAndRotation` 方法用于设置节点的世界位置和旋转。`SetIdentityPose` 方法用于重置节点的姿态。`SetPosition`、`SetRotation` 和 `SetScale` 方法用于设置节点的本地位置、旋转和缩放。`SetWorldPosition` 和 `SetWorldRotation` 方法用于设置节点的世界位置和旋转。`SetActive` 方法用于设置节点的激活状态。`SetTransform` 方法用于设置节点的变换。

`MoveToZeroByBounds` 方法用于将节点移动到原点，并根据边界设置枢轴。`SetPivotToCenter` 方法用于将节点的枢轴设置到中心。`Destroy` 方法用于销毁节点及其子节点。`InvokeNewComponentEvent` 方法用于在添加新组件时触发事件。`AddUniComponent2` 方法用于添加组件，并根据需要执行生命周期方法。`AddUniComponent` 方法用于添加组件。`RemoveUniComponent` 方法用于移除组件。`GetTransformData` 方法用于获取节点的变换数据。`RefAllModelCollider` 方法用于刷新所有模型碰撞器。`ChangeEditCollider` 方法用于更改编辑碰撞器。`SetChildrenNodesWithModeValue` 方法用于设置子节点的模式值。`GetEditComponents` 方法用于获取编辑组件。`IsChildrenRenderOver` 方法用于判断子节点的渲染是否完成。`ToNodeFile` 方法用于将节点导出为文件。`GetScriptMachineData` 方法用于获取脚本机器数据。`ProcessScriptUsedIDList` 方法用于处理脚本使用的 ID 列表。`CollectScriptUnitUseIDList` 方法用于收集脚本单元使用的 ID 列表。`ToRawData` 方法用于将节点导出为原始数据。
