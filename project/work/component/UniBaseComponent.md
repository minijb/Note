
```c#
    public class UniBaseComponent : UniBaseComponentV2, IAnalysis
    {
        protected List<IUniSensor> connectedSensors = new List<IUniSensor>();//使用这个变量需要在调用GetOwnerCharacter赋值
        //是否监测性能
        protected virtual bool IsAnalysis => false;
        private void Awake() { }
        private void Start() { }

        public override void OnUniLogicReady(UniNode node)
        {
            base.OnUniLogicReady(node);
            if (node.Scene is not UniEditScene)
            {
                OnUniScenePlaying();
            }
        }

        public virtual void OnUniScenePlaying()
        {

        }
        
        public virtual void OnUniSceneStop()
        {

        }
        
        public override void OnUniRenderReady(UniNode node)
        {
            base.OnUniRenderReady(node);
        }
        
        protected void Connect(IUniSensor sensor, int signal, TriggleCondition conds, TriggleAction acts)
        {
            if (sensor == null) return;
            if (!connectedSensors.Contains(sensor))
            {
                connectedSensors.Add(sensor);
            }
            sensor.Slots.Attach(signal, this, (triggerBaseData) =>
            {
                if (!UniMain.Game.Scene.IsPlaying) return;
                if (triggerBaseData != null)
                {
                    if (UniOwner.IsChildOfCharacter((uint)triggerBaseData.playerNetId))
                    {
                        return;
                    }
                    //只有（死亡，蹦床，加速，不稳定，击退，门（三种），赛道，金币，检查点）这11个obby组件可以被载具触发
                    if (triggerBaseData.triggerUnit == TriggerUnit.Vehicle && !IsVehicleTrigger())
                    {
                        return;
                    }
                }
                if (conds == null || conds(triggerBaseData))
                {
                    try
                    {
                        acts(triggerBaseData);
                    }
                    catch (Exception e)
                    {
                        Console.WriteLine(e);
                    }
                }
            });
        }

        protected void Disconnect(IUniSensor sensor, int evt)
        {
            if (sensor != null)
            {
                sensor.Slots.Detach(evt, this);
            }
        }

        public void DisconnectAll()
        {
            if (connectedSensors == null) return;
            for (int i = 0; i < connectedSensors.Count; i++)
            {
                connectedSensors[i].Slots.DetachWithTarget(this);
            }
            connectedSensors.Clear();
        }
        
        public virtual void OnUniDestroy()
        {
            DisconnectAll();
        }
        
        public override void OnUniStart(UniNode node)
        {
            base.OnUniStart(node);
            if (IsAnalysis)
            {
                AddAnalysisMonitor();
            }
        }

        public virtual void OnDestroy()
        {
            if (IsAnalysis)
            {
                DelAnalysisMonitor(true);
            }
        }

        protected virtual void OnEnable()
        {
            if (IsAnalysis)
            {
                AddAnalysisMonitor();
            }
        }

        protected virtual void OnDisable()
        {
            if (IsAnalysis)
            {
                DelAnalysisMonitor(false);
            }
        }

        public virtual void OnTriggerEnterAction()
        {

        }

        public virtual void OnTriggerExitAction()
        {

        }
        
        public virtual void OnRefreshRuntimeFlag()
        {

        }

        public virtual bool CanGroup()
        {
            return true;
        }
        
        public virtual void RecordExtraData(EditorActionModifyComponentData actionModify)
        {

        }

        public virtual bool IsVehicleTrigger()
        {
            return false;
        }
        
        public void AddAnalysisMonitor()
        {
#if !UNITY_SERVER
            if (UniOwner && UniOwner.Scene && UniOwner.Scene.EditType != SceneEditType.Play)
            {
                bool isActive = UniOwner.gameObject.activeInHierarchy;
                if (isActive)
                {
                    UniOwner.Scene.AnalysisManager.AddComponent(GetComponentType(), UniOwner.Id);
                }
            }
#endif
        } 

        public void DelAnalysisMonitor(bool IsDestroy)
        {
#if !UNITY_SERVER
            if (UniOwner && UniOwner.Scene && UniOwner.Scene.EditType != SceneEditType.Play && !UniOwner.gameObject.activeInHierarchy)
            {
                if (IsDestroy)
                {
                    UniOwner.Scene.AnalysisManager.DelComponent(GetComponentType(), UniOwner.Id);
                }
                else
                {
                    bool isActive = UniOwner.gameObject.activeInHierarchy;
                    if (!isActive)
                    {
                        UniOwner.Scene.AnalysisManager.DelComponent(GetComponentType(), UniOwner.Id);
                    }
                }
                
            }
#endif
        }
        
        public virtual string GetComponentType()
        {
            return GetType().Name;
        }
    }
    
    [UniComponent(true,true)]
    public class UniDistrAuthorComponent : UniBaseComponent
    {
        public override void OnUniStart(UniNode node)
        {
            base.OnUniStart(node);
            if (!node.HaveNetworkFlag(UniNodeNetworkFlag.Register))
            {
                node.AddNetworkFlag(UniNodeNetworkFlag.Register);
                UniMain.ComponentSyncModule.RegisterAuthNode(node);
            }
            
        }
    }
```

类继承自 `UniBaseComponentV2` 并实现了 `IAnalysis` 接口，用于在 Unity 中管理和操作基础组件。该类包含多个字段和方法，用于处理组件的初始化、连接和断开传感器、场景播放和停止、性能监测等功能。

首先，类中定义了一个受保护的字段 `connectedSensors`，用于存储连接的传感器列表。`IsAnalysis` 是一个受保护的虚拟属性，指示是否监测性能，默认返回 `false`。`Awake` 和 `Start` 方法为空，表示在组件唤醒和启动时不执行任何操作。

`OnUniLogicReady` 方法重写了基类的方法，用于在节点逻辑准备就绪时调用。如果节点的场景不是 `UniEditScene`，则调用 `OnUniScenePlaying` 方法。`OnUniScenePlaying` 和 `OnUniSceneStop` 方法是虚拟方法，分别在场景播放和停止时调用，默认实现为空。

`OnUniRenderReady` 方法重写了基类的方法，用于在节点渲染准备就绪时调用。`Connect` 方法用于连接传感器，接受传感器、信号、触发条件和触发动作作为参数。如果传感器为空或已连接，则返回。否则，将传感器添加到 `connectedSensors` 列表，并附加信号处理函数。信号处理函数根据触发条件和触发动作执行相应的操作。

`Disconnect` 方法用于断开传感器，接受传感器和事件作为参数。如果传感器不为空，则从传感器的插槽中分离事件。`DisconnectAll` 方法用于断开所有连接的传感器，并清空 `connectedSensors` 列表。

`OnUniDestroy` 方法是虚拟方法，用于在组件销毁时调用，默认实现为断开所有传感器。`OnUniStart` 方法重写了基类的方法，用于在节点启动时调用。如果 `IsAnalysis` 为 `true`，则调用 `AddAnalysisMonitor` 方法添加性能监测。

`OnDestroy` 方法是虚拟方法，用于在组件销毁时调用。如果 `IsAnalysis` 为 `true`，则调用 `DelAnalysisMonitor` 方法删除性能监测。`OnEnable` 和 `OnDisable` 方法是虚拟方法，分别在组件启用和禁用时调用。如果 `IsAnalysis` 为 `true`，则分别调用 `AddAnalysisMonitor` 和 `DelAnalysisMonitor` 方法。

`OnTriggerEnterAction` 和 `OnTriggerExitAction` 方法是虚拟方法，分别在触发器进入和退出时调用，默认实现为空。`OnRefreshRuntimeFlag` 方法是虚拟方法，用于刷新运行时标志，默认实现为空。`CanGroup` 方法是虚拟方法，指示组件是否可以分组，默认返回 `true`。`RecordExtraData` 方法是虚拟方法，用于记录额外数据，默认实现为空。`IsVehicleTrigger` 方法是虚拟方法，指示组件是否为车辆触发器，默认返回 `false`。

`AddAnalysisMonitor` 方法用于添加性能监测。如果组件的所有者和场景存在且场景编辑类型不是 `Play`，并且组件的游戏对象在层级中处于激活状态，则将组件添加到场景的分析管理器中。`DelAnalysisMonitor` 方法用于删除性能监测。如果组件的所有者和场景存在且场景编辑类型不是 `Play`，并且组件的游戏对象在层级中不处于激活状态，则从场景的分析管理器中删除组件。

`GetComponentType` 方法是虚拟方法，返回组件的类型名称。通过这些方法，`UniBaseComponent` 类提供了丰富的功能，用于管理和操作基础组件，包括初始化、连接和断开传感器、场景播放和停止、性能监测等功能。