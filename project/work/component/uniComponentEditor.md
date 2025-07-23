
```c#
public class UniComponentEditor<T> : MonoBehaviour, IUniComponentEditor where T :IUniComponent
    {
        private static UniComponentReflectionUtils.SLID2Meta TargetMeta = UniComponentReflectionUtils.GetMeta(typeof(T));
        public T Target { get; set; }
        
        public IUniComponent GetTarget()
        {
            return Target;
        }

        public UniNodeEditor uniNodeEditor;
        public UniNodeEditor UniNodeEditor
        {
            get
            {
                if (uniNodeEditor == null)
                {
                    uniNodeEditor = GetComponent<UniNodeEditor>();
                }

                return uniNodeEditor;
            }
        }
        public virtual int AfterCopyCallSort => 10;

        public virtual void ClearInteractTextData(){}
        public virtual void OnHideFromScene(bool isHide)
        {
            if (UniMain.Game && UniMain.Game.Scene&&(UniMain.Game.Scene is UniEditScene editScene)) 
            {
                var componenttype = Target.GetType();
                if (componenttype == typeof(UniColliderBoxEntity))
                {
                    editScene.ModifyUniComponentCountStatistics(componenttype, !isHide);
                }
              
            }
           
        }

        //当物体被选中
        public virtual void Attach(){}
        public void OnBeforeApplyData()
        {
            if (Target is UniBaseComponentV2 baseComponent)
            {
                Global.Game.RefreshScriptCount(-baseComponent.ScriptCount);
                baseComponent.ScriptCount = 0;
            }
            else if (Target is UniBasicComponent basicComponent)
            {
                Global.Game.RefreshScriptCount(-basicComponent.ScriptCount);
                basicComponent.ScriptCount = 0;
            }
        }

        //当物体被取消选中
        public virtual void Dettach(){}

        protected virtual void Awake()
        {
            
        }

        public virtual void AfterUniStart()
        {
            var componenttype = Target.GetType();
            //条件判断处填需要统计的判断,UniColliderBoxEntity只是测试示例
            if (componenttype == typeof(UniColliderBoxEntity))
            {
                if (UniNodeEditor && !UniNodeEditor.IsRemoveFromScene)
                {
                    (UniMain.Game.Scene as UniEditScene).ModifyUniComponentCountStatistics(componenttype, true);
                }
            }
        }
        
        protected virtual void Start()
        {
            
        }

        protected virtual void OnDestroy()
        {

        }

        public virtual void ShowGizmo( )
        {
            
        }

        public virtual void OnComponentChange(Type type =null)
        {
            
        }

        public virtual void OnInspectorEvent(object arg)
        {

        }
        
        public virtual void OnAfterApplyData( )
        {

        }
        public virtual void OnAfterCopy()
        {

        }

        public virtual void OnAddToScene()
        {
            AddTriggerModeComponent();
        }
        
        public virtual void OnAddToSceneFromInspector()
        {
            OnAddToScene();
        }
 
        public virtual void OnAddToSceneFromBag()
        {
            OnAddToScene();
        }
        
        public virtual void SaveData()
        {

        }

        /// <summary>
        /// 编辑模式切游玩
        /// </summary>
        public virtual void OnUniEditorPlay()
        {
            Target.ClearSnap();
            if (Global.Game.Scene.IsPlaying)
            {
                TargetMeta?.LifecycleMethod.OnUniScenePlaying(Target);
            }
        }
        
        /// <summary>
        /// 游玩回编辑
        /// </summary>
        public virtual void OnUniEditorStop()
        {
            Target.ApplySnap();
            TargetMeta?.LifecycleMethod.OnUniSceneStop(Target);
        }
        
        /// <summary>
        /// 检测是否使用交互
        /// </summary>
        public virtual ComponentMode GetComponentMode()
        {
            return ComponentMode.None;
        }
        
        public virtual void AddTriggerModeComponent()
        {
            var group = GetComponent<UniGroup>();
            var groupEditor = GetComponent<UniGroupEditor>();
            switch (GetComponentMode())
            {
                case ComponentMode.Interact:
                    if (!group.transform.GetComponent(typeof(UniInteractComponent)))
                    {
                        group.AddUniComponent2(typeof(UniInteractComponent),true, null, false);
                        UniEditorProxy.RefreshInspector();
                    }
                    break;
                case ComponentMode.Trigger:
                    if (!group.transform.GetComponent(typeof(UniColliderBoxEntity)))
                    {
                        group.AddUniComponent2(typeof(UniColliderBoxEntity),true);
                        UniEditorProxy.RefreshInspector();
                    }
                    break;
            }
            
        }

        protected virtual void OnComponentDestroy()
        {
            
        }
        
        public virtual void NotifyComponentDestroy()
        {
            if (Target is UniBaseComponentV2 baseComponent)
            {
                Global.Game.RefreshScriptCount(-baseComponent.ScriptCount);
            }
            else if (Target is UniBasicComponent basicComponent)
            {
                Global.Game.RefreshScriptCount(-basicComponent.ScriptCount);
            }
            OnComponentDestroy();
            if(Target != null)
            {
                if (Target is UniBaseComponent a)
                {
                    a.DisconnectAll();
                }

                var node = GetComponent<UniNode>();
                if(node)
                {
                    node.gameObject.SendMessage($"On{Target.GetType().Name}Destroy",Target,SendMessageOptions.DontRequireReceiver);
                }
 
                if (UniMain.Game && UniMain.Game.Scene&&(UniMain.Game.Scene is UniEditScene editScene)
                    &&UniNodeEditor&&!UniNodeEditor.IsRemoveFromScene)
                {
                    var componenttype = Target.GetType();
                    if (componenttype == typeof(UniColliderBoxEntity))
                    {
                        editScene.ModifyUniComponentCountStatistics(componenttype, false);
                    }
                }
            }

           
            DestroyImmediate(this);//同组件一样立即删除
        }

        public virtual void OnSelected()
        {
            
        }
        
        public virtual void OnUnSelected()
        {
            
        }

        protected virtual GameObject GetVirualGameObject()
        {
            return null;
        }

        protected virtual void SetViewObjectsActive(bool isShow)
        {
            var vir = GetVirualGameObject();
            if (vir)
            {
                vir.SetActive(isShow);
            }
        }
        
        public virtual void OnHideStateChange(bool isShow)
        {
            SetViewObjectsActive(isShow);
        }

        public virtual void AddChannelUI(UniGroup UniGroup, int channelData, int obbyType)
        {
            if (channelData == 0) return;
            Messenger.Default.Publish<ChannelTipData>(new ChannelTipData()
            {
                UniGroup = UniGroup,
                channel = channelData,
                operation = 1,
                obbyType = obbyType,
            });                           
        }

        public virtual void DeleteChannelUI(UniGroup UniGroup, int channelData, int obbyType)
        {
            if (channelData == 0) return;
            Messenger.Default.Publish<ChannelTipData>(new ChannelTipData()
            {
                UniGroup = UniGroup,
                channel = channelData,
                operation = 0,
                obbyType = obbyType,
            });   
        }

        public virtual void ModifyChannelUI(UniGroup UniGroup, int channelData, int newChannelData, int obbyType)
        {
            Messenger.Default.Publish<ChannelTipData>(new ChannelTipData()
            {
                UniGroup = UniGroup,
                channel = newChannelData,
                originalChannel = channelData,
                operation = 2,
                obbyType = obbyType,
            });   
        }
        
        // public static void AddUseCompoent(UniComponentsNode node,bool addCapture =true)
        // {
        //     if (!node.TryGetComponent<UniUseComponent>(out var uniUseComponent))
        //     {
        //         var t= node.AddUniComponent2(typeof(UniUseComponent),true);
        //         var refNodes = node.GetComponentsInParent<UniRefNode>();
        //         foreach (var refNode in refNodes)
        //         {
        //             refNode.SerializeRefNode = true;
        //         }
        //         var networkIdentity =  node.GetComponent<NetworkIdentity>();
        //         if (networkIdentity)
        //         {
        //             networkIdentity.ReinitializeNetworkBehaviours();
        //         }
        //         if (addCapture)
        //         {
        //             (t.Item2 as UniUseEditor).NeedUpdateCapture = true;
        //             (t.Item2 as UniUseEditor).SetCapture();
        //         }
        //     }
        //     else
        //     {
        //         if (addCapture)
        //         {
        //             var e = uniUseComponent.GetComponent<UniUseEditor>();
        //             if (e)
        //             {
        //                 e.NeedUpdateCapture = true;
        //             }
        //         }
        //         
        //     }
        // }
        
        public void DeserializeUniscriptMachine(UniUGCScript ugcScript)
        {
            ugcScript.OnUniDeserializeAfter();
        }

        public virtual UniObjectLayoutContainer OnCreateHeaderInspectorElement(UniObjectLayoutContainer parent)
        {
            var compLayout = parent.CreateChildElement<UniComponentLayoutContainer>(null);
            compLayout.Component = Target;
            compLayout.LayoutStyle = DragLayoutElement.ELayoutStyle.Vertical;
            var config = UniComponentTable.QueryExcel(GetTarget().GetType());
            compLayout.SetName(config.Languagekey.GetLanguageStr());
            //if(Target is UniCustomComponent c)
            //{
            //    compLayout.SetName(c.CustomComponentInfo.ComponentName);
            //}
            if(Target is UniCustomComponent customc)
            {
                //todo 搞一个missing样式
               
            }
            return compLayout;
        }
        
        public virtual void OnCreateInspectorElement(UniObjectLayoutContainer parent)
        {
            var objEle = OnCreateHeaderInspectorElement(parent);
            objEle.RebuildElements();
        }
        public virtual void RefreshInspectorElement(UniObjectLayoutContainer parent)
        {
        }
        public virtual void AfterComponentsSwitchToPlay()
        {

        }
        // public void CreateGroupElement(InspectorDrawerGroupData groupData,UniObjectLayoutContainer parent)
        // {
        //     if (!string.IsNullOrEmpty(groupData.GroupName))
        //     {
        //         var compLayout = parent.CreateChildElement<UniObjectLayoutContainer>(null);
        //         compLayout.LayoutStyle = DragLayoutElement.ELayoutStyle.Vertical;
        //         compLayout.SetName(groupData.GroupName);
        //         parent = compLayout;
        //     }
        //
        //     foreach (var c in groupData.Child)
        //     {
        //         if (c.Attr.Expand)
        //         {
        //             var compLayout = parent.CreateChildElement<UniObjectLayoutContainer>(null);
        //             compLayout.LayoutStyle = DragLayoutElement.ELayoutStyle.Vertical;
        //             compLayout.SetName(c.Attr.GetDisplayName());
        //             var expandGroup = UniObjectInspectorV2.GetDrawerData(c.Member.GetValue(c.Target));
        //             foreach (var g in expandGroup)
        //             {
        //                 CreateGroupElement(g, compLayout);
        //             }
        //             
        //         }
        //         else
        //         {
        //             if (c.Attr.FieldType.IsArray || c.Attr.FieldType.IsGenericType)
        //             {
        //                 var n = c.Attr.GetDisplayName();
        //                 var transLayout = parent.CreateChildElement<UniArrayLayoutContainer>(c.Attr);
        //                 transLayout.LayoutStyle = DragLayoutElement.ELayoutStyle.Vertical;
        //                 transLayout.SetName(n);
        //                 // var v3Layout = transLayout.CreateChildElement<UniFieldLayoutElement>(c.Attr);
        //                 // v3Layout.Field.BindTo(c.Target,c.Member);
        //             }
        //             else
        //             {
        //                 var n = c.Attr.GetDisplayName();
        //                 var transLayout = parent.CreateChildElement<UniFieldLayoutContainer>(null);
        //                 transLayout.LayoutStyle = DragLayoutElement.ELayoutStyle.Vertical;
        //                 transLayout.SetName(n);
        //                 var v3Layout = transLayout.CreateChildElement<UniFieldLayoutElement>(c.Attr);
        //                 v3Layout.Field.BindTo(c.Target,c.Member);
        //             }
        //
        //         }
        //         
        //     }
        // }
        // public virtual void OnCreateFieldInspectorElement(UniObjectLayoutContainer parent)
        // {
        //
        //     var group = UniObjectInspectorV2.GetDrawerData(Target);
        //     foreach (var g in group)
        //     {
        //         CreateGroupElement(g, parent);
        //     }
        // }
    }
```

`UniComponentEditor<T>`

类是一个通用的 MonoBehaviour 类，用于在 Unity 中管理和操作组件编辑器。该类实现了 `IUniComponentEditor` 接口，并且泛型参数 `T` 必须实现 `IUniComponent` 接口。类中包含多个字段和方法，用于处理组件的初始化、显示、隐藏、销毁、添加到场景、编辑器事件等功能。

首先，类中定义了一个静态字段 `TargetMeta`，用于存储组件的元信息。`Target` 属性用于获取和设置当前编辑的组件。`GetTarget` 方法返回当前编辑的组件。`UniNodeEditor` 属性用于获取或设置节点编辑器的引用，如果引用为空，则通过 `GetComponent<UniNodeEditor>` 方法获取。

`AfterCopyCallSort` 属性返回一个整数值，表示在复制调用后的排序顺序，默认值为 10。`ClearInteractTextData` 方法是一个虚方法，用于清除交互文本数据，默认实现为空。`OnHideFromScene` 方法用于处理组件在场景中隐藏或显示的操作，如果当前场景是 `UniEditScene`，则修改组件统计数据。

`Attach` 和 `Dettach` 方法是虚方法，分别在物体被选中和取消选中时调用，默认实现为空。`OnBeforeApplyData` 方法用于在应用数据之前调用，重置组件的脚本计数。`Awake` 方法是虚方法，在组件唤醒时调用，默认实现为空。`AfterUniStart` 方法用于在组件启动后调用，如果组件类型是 `UniColliderBoxEntity`，则修改组件统计数据。

`Start` 和 `OnDestroy` 方法是虚方法，分别在组件启动和销毁时调用，默认实现为空。`ShowGizmo` 方法是虚方法，用于显示 Gizmo，默认实现为空。`OnComponentChange` 方法是虚方法，用于处理组件变化事件，默认实现为空。`OnInspectorEvent` 方法是虚方法，用于处理检查器事件，默认实现为空。

`OnAfterApplyData` 和 `OnAfterCopy` 方法是虚方法，分别在应用数据和复制后调用，默认实现为空。`OnAddToScene` 方法用于将组件添加到场景中，并调用 `AddTriggerModeComponent` 方法。`OnAddToSceneFromInspector` 和 `OnAddToSceneFromBag` 方法分别在从检查器和背包中添加到场景时调用，默认调用 `OnAddToScene` 方法。

`SaveData` 方法是虚方法，用于保存数据，默认实现为空。`OnUniEditorPlay` 方法用于在编辑模式切换到游玩模式时调用，清除组件的快照并调用元信息的 `OnUniScenePlaying` 方法。`OnUniEditorStop` 方法用于在游玩模式切换回编辑模式时调用，应用组件的快照并调用元信息的 `OnUniSceneStop` 方法。

`GetComponentMode` 方法是虚方法，返回组件模式，默认返回 `ComponentMode.None`。`AddTriggerModeComponent` 方法用于根据组件模式添加触发模式组件。`OnComponentDestroy` 方法是虚方法，在组件销毁时调用，默认实现为空。`NotifyComponentDestroy` 方法用于通知组件销毁，断开所有传感器连接，并发送销毁消息。

`OnSelected` 和 `OnUnSelected` 方法是虚方法，分别在组件被选中和取消选中时调用，默认实现为空。`GetVirualGameObject` 方法是虚方法，返回虚拟游戏对象，默认返回 `null`。`SetViewObjectsActive` 方法用于设置视图对象的激活状态。`OnHideStateChange` 方法用于处理隐藏状态变化，调用 `SetViewObjectsActive` 方法。

`AddChannelUI`、`DeleteChannelUI` 和 `ModifyChannelUI` 方法用于添加、删除和修改频道 UI，分别发布相应的消息。`DeserializeUniscriptMachine` 方法用于反序列化脚本机器。`OnCreateHeaderInspectorElement` 方法用于创建检查器头部元素，并设置组件的名称和布局样式。

`OnCreateInspectorElement` 方法用于创建检查器元素，并调用 `OnCreateHeaderInspectorElement` 方法。`RefreshInspectorElement` 方法是虚方法，用于刷新检查器元素，默认实现为空。`AfterComponentsSwitchToPlay` 方法是虚方法，在组件切换到游玩模式后调用，默认实现为空。