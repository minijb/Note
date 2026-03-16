
```c#
    public abstract class BaseLayout
    {
        public static HashSet<Type> StringCanDropTypes = new HashSet<Type>
        {
            typeof(string), typeof(byte),
            typeof(int), typeof(long),
            typeof(float), typeof(double), typeof(bool),
            typeof(Vector3), typeof(Vector2), typeof(Color),
            typeof(string[]), typeof(float[]),typeof(bool[]),
            typeof(Vector3[]), typeof(Vector2[]), typeof(Color[]),
        };

        public enum DragDropFlag
        {
            None = 0,
            Drop = 1 << 1,
            Drag = 1 << 2,
            DropAndDrag = Drop | Drag,
            CantDrag = 1 << 3,
            CantDrop = 1 << 4,
            CantDragAndDrop = CantDrop | CantDrop,
        }

        public enum LayoutDirection
        {
            Horizontal,
            Vertical
        }

        public virtual LayoutDirection Direction => LayoutDirection.Horizontal;
        public virtual IUnitLayoutElement LayoutElement => null;
        public int dragDropFlagValue = (int)DragDropFlag.None;
        public bool CanInteract = true;
        public virtual int DragDropFlagValue
        {
            get
            {
                return dragDropFlagValue;
            }
            set
            {
                dragDropFlagValue = value;
            }
        }

        public bool isDragCreateNew = false;
        public ValueInput MyValueInput;
        public ControlOutput MyControlOutput;
        public BaseScriptUnit Unit;
        public UniScriptUnitConfig.ScriptUnitConfigData UnitConfig;
        public UnitImageType UnitImageType;

        public BaseLayout(BaseScriptUnit ownerUnit)
        {
            this.Unit = ownerUnit;
            // SetDragTargetUnit(ownerUnit);
        }

        // public void SetDragTargetUnit(BaseScriptUnit unit)
        // {
        //     this.DragTargetUnit = unit;
        // }
        protected virtual void OnDragStart()
        {
        }

        protected virtual void OnDragUpdate()
        {
        }

        protected virtual void OnDragEnd()
        {
        }

        protected virtual void OnDrop()
        {
        }

        public virtual void SetCanInteract(bool canInteract)
        {
            CanInteract = canInteract;
        }

        public BaseScriptUnit GetConnectUnit()
        {
            if (Unit.Enter.hasValidConnection)
            {
                return Unit.Enter.validConnections.First().source.unit as BaseScriptUnit;
            }

            return null;
        }

        public void Disconnect()
        {
            // BaseScriptUnit previousUnit = null;
            // BaseScriptUnit nextUnit = null;
            ControlOutput previousControlOutput = null;
            ControlInput nextControlInput = null;
            if (Unit.Enter.hasValidConnection)
            {
                previousControlOutput = Unit.Enter.validConnections.First().source;
                Unit.Enter.Disconnect();
            }

            if (Unit.Exit.hasValidConnection)
            {
                nextControlInput = Unit.Exit.validConnections.First().destination;
                Unit.Exit.Disconnect();
            }

            if (previousControlOutput != null && nextControlInput != null)
            {
                previousControlOutput.ValidlyConnectTo(nextControlInput);
            }

            if (Unit.valueOutputs.Count > 0)
            {
                Unit.valueOutputs.First().Disconnect();
            }
        }

        public void Append(BaseScriptUnit unit)
        {
            if (!CheckDragDropFlag())
            {
                return;
            }

            if (Unit != null && Unit.Exit != null)
            {
                if (Unit.Exit.connection != null)
                {
                    var oldUnit = Unit.Exit.connection.destination.unit as BaseScriptUnit;
                    Unit.Exit.ValidlyConnectTo(unit.Enter);
                    unit.Exit.ValidlyConnectTo(oldUnit.Enter);
                }
                else
                {
                    Unit.Exit.ValidlyConnectTo(unit.Enter);
                }
            }
            if (unit is GetUniPropertyDataUnit getUniPropertyDataUnit)
            {
                getUniPropertyDataUnit.ChangeMod(GetUniPropertyDataMode.NormalProperty);
            }
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="unit"></param>
        /// <returns> (bool isSuccess, bool needRefreshRoot)</returns>
        public (bool, bool) Connect(BaseScriptUnit unit, bool isRecoverConnect = false)
        {
            if (!CheckCanDrop(unit))
            {
                return (false, false);
            }

            if (MyControlOutput != null)
            {
                MyControlOutput.ValidlyConnectTo(unit.Enter);
                return (true, false);
            }
            else if (MyValueInput != null)
            {
                foreach (var output in unit.valueOutputs)
                {
                    bool isSelected = false;
                    var type = new Type[]{ MyValueInput.type };
                    if (MyValueInput.type == typeof(object) && MyValueInput.LinkTypeArr != null)
                    {
                        type = MyValueInput.LinkTypeArr;
                    }
                    var dstType = output.type;
                    if (output.LinkType != null && !type.Contains(typeof(UniPropertyData)))
                    {
                        dstType = output.LinkType;
                    }
                    if (CheckTypeCanDrop(type, dstType) && CheckAssetTypeCanDrop(MyValueInput.LimitAssetTypeArr, output.assetType))
                    {
                        (bool, bool) returnValue = (true, false);
                        if (MyValueInput.hasValidConnection)
                        {
                            var preUnit = MyValueInput.connection.source.unit as BaseScriptUnit;
                            var parentUnit = GetParentUnit(preUnit);
                            if (parentUnit != null)
                            {
                                MyValueInput.Disconnect();
                                if (parentUnit.Exit.hasValidConnection)
                                {
                                    var preExitUnit = parentUnit.Exit.connection.destination.unit as BaseScriptUnit;
                                    parentUnit.Exit.Disconnect();
                                    parentUnit.Exit.ConnectToValid(preUnit.Enter);
                                    
                                    preUnit.Exit.ConnectToValid(preExitUnit.Enter);
                                }
                                else
                                {
                                    parentUnit.Exit.ConnectToValid(preUnit.Enter);
                                }
                                if (preUnit.layout.LayoutElement is UnitLayoutContainer container)
                                {
                                    if (container.Tree is UnitGraphTree graphTree)
                                    {
                                        graphTree.SelectElement(null, container);
                                        isSelected = true;
                                    }
                                }
                                // output.ValidlyConnectTo(MyValueInput);
                                returnValue = (true, true);
                            }
                        }
                        output.ValidlyConnectTo(MyValueInput);
                        if(MyValueInput.unit is NumberCompareUnit numberCompareUnit && MyValueInput == numberCompareUnit.InputCompareValue1)
                        {
                            numberCompareUnit.refreshPropertyDataUnit = true;
                        }
                        if (unit is GetUniPropertyDataUnit getUniPropertyDataUnit)
                        {
                            if (Unit is TriggerEventUnit)
                            {
                                getUniPropertyDataUnit.ChangeMod(GetUniPropertyDataMode.Event);
                            }
                            else
                            {
                                getUniPropertyDataUnit.ChangeMod(GetUniPropertyDataMode.NormalProperty);
                            }
                        }

                        if (!isSelected && !isRecoverConnect)
                        {
                            if (LayoutElement is UnitLayoutContainer container)
                            {
                                if (container.Tree is UnitGraphTree graphTree)
                                {
                                    graphTree.ClearSelect();
                                }
                            }
                            else if (LayoutElement is UnitLayoutElement element)
                            {
                                if (element.Tree is UnitGraphTree graphTree)
                                {
                                    graphTree.ClearSelect();
                                }
                            }
                        }
                        
                        return returnValue;
                    }
                }
            }
            return (false, false);
        }

        BaseScriptUnit GetParentUnit(BaseScriptUnit unit)
        {
            BaseScriptUnit parentUnit = unit;
            while (!parentUnit.Enter.hasValidConnection)
            {
                if (parentUnit.valueOutputs.First().hasValidConnection)
                {
                    parentUnit = parentUnit.valueOutputs.First().connections.First().destination.unit as BaseScriptUnit;
                }
                else
                {
                    break;
                }
            }

            return parentUnit;
        }

        public bool CheckDragDropFlag()
        {
            if (DragDropFlagValue == (int)DragDropFlag.None || (DragDropFlagValue & (int)DragDropFlag.Drop) == 0)
            {
                return false;
            }
            return true;
        }

        public virtual bool CheckCanDrop(BaseScriptUnit unit)
        {
            if (!CheckDragDropFlag())
                return false;

            //分支 / 下一条指令 使用ControlOutput
            if (MyControlOutput != null)
            {
                if (unit.Enter != null)
                {
                    return true;
                }
            }
            else if (MyValueInput != null)
            {
                foreach (var output in unit.valueOutputs)
                {
                    Type[] type = null;
                    if ((MyValueInput.type == typeof(object) || MyValueInput.type == typeof(UniPropertyData)) && MyValueInput.LinkTypeArr != null)
                    {
                        type = MyValueInput.LinkTypeArr;
                    }
                    else
                    {
                        type = new Type[] { MyValueInput.type };
                    }
                    
                    var dstType = output.type;
                    if (output.LinkType != null && !type.Contains(typeof(UniPropertyData)))
                    {
                        dstType = output.LinkType;
                    }
                    
                    int[] limitAssetType = MyValueInput.LimitAssetTypeArr;
                    
                    if (CheckTypeCanDrop(type, dstType) && CheckAssetTypeCanDrop(limitAssetType, output.assetType))
                    {
                        return true;
                    }
                }
            }

            return false;
        }

        private bool CheckAssetTypeCanDrop(int[] inputAssetType, int outputAssetType)
        {
            if (inputAssetType == null || inputAssetType.Length == 0)
            {
                return true;
            }
            if (outputAssetType == (int)Uni.Application.UI.AssetType.BGM)
            {
                return inputAssetType.Contains(outputAssetType) || inputAssetType.Contains((int)Uni.Application.UI.AssetType.Sound);
            }
            else if(outputAssetType == (int)Uni.Application.UI.AssetType.Sound)
            {
                return inputAssetType.Contains(outputAssetType) || inputAssetType.Contains((int)Uni.Application.UI.AssetType.BGM);
            }
            return inputAssetType.Contains(outputAssetType);
        }

        private bool CheckTypeCanDrop(Type[] srcArr, Type dst)
        {
            if (srcArr == null || dst == null)
                return false;
            if (srcArr.Length == 0)
                return true;
            if (dst == typeof((List<int>, List<List<UniPropertyData>>)))
                return srcArr.Contains(dst);
            if (srcArr.Contains(typeof((List<int>, List<List<UniPropertyData>>))))
                return dst == typeof((List<int>, List<List<UniPropertyData>>));
            if (dst == typeof(UniPropertyData))
                return true;
            if (dst == typeof(string))
            {
                foreach (var source in srcArr)
                {
                    if (source.IsNumeric())
                    {
                        return true;
                    }
                }
            }

            foreach (var src in srcArr)
            {
                if (src == null)
                {
                    return true;
                }
                if (src == dst)
                {
                    return true;
                }
                if (src == typeof(string))
                {
                    if (StringCanDropTypes.Contains(dst))
                    {
                        return true;
                    }
                }
                if (src == typeof(object))
                {
                    return true;
                }
                if (src.IsSubclassOf(dst))
                {
                    if (src == typeof(UniPlayer) && src != dst)
                    {
                        return false;
                    }
                    return true;
                }
                else if (dst.IsSubclassOf(src))
                {
                    if (dst == typeof(UniPlayer) && src != dst)
                    {
                        return false;
                    }
                    return true;
                }
                else if (src.IsAssignableFrom(dst))
                {
                    if (dst == typeof(UniPlayer) && src != dst)
                    {
                        return false;
                    }
                    return true;
                }
                else if (dst.IsAssignableFrom(src))
                {
                    if (src == typeof(UniPlayer) && src != dst)
                    {
                        return false;
                    }
                    return true;
                }
                //当src 和 dst为 int/float时，也可以进行转换
                if (dst.IsBoolAndNumeric() && src.IsBoolAndNumeric())
                {
                    return true;
                }
            }
            return false;
        }

        public virtual void OnShow()
        {
        }

        public virtual Uni.DragLayoutElement CreateLayoutElement(GameObject view = null)
        {
            return null;
        }

        public abstract GameObject GetLayoutGameObject();

        public abstract void SetLayoutGameObject(GameObject go);

        public virtual void CreateLayoutElementAfter() { }
    }
```


这段代码定义了一个名为 `BaseLayout` 的抽象类，用于在 Unity 中管理和处理布局元素。该类包含多个字段、枚举和方法，用于处理拖放操作、布局方向、交互性、连接和断开连接等功能。

首先，类中定义了一个静态的 `HashSet<Type>` 类型的字段 `StringCanDropTypes`，用于存储可以拖放的类型集合。这些类型包括基本数据类型（如 `string`、`int`、`float` 等）以及它们的数组类型。接下来，定义了一个名为 `DragDropFlag` 的枚举，用于表示拖放操作的标志，包括 `None`、`Drop`、`Drag`、`DropAndDrag`、`CantDrag`、`CantDrop` 和 `CantDragAndDrop` 等标志。另一个枚举 `LayoutDirection` 用于表示布局方向，包括 `Horizontal` 和 `Vertical`。

类中还定义了一些字段和属性，用于存储和管理布局元素的状态和行为。`Direction` 属性返回布局方向，默认为水平布局。`LayoutElement` 属性返回布局元素，默认为 `null`。`dragDropFlagValue` 字段用于存储拖放标志的值，`CanInteract` 字段用于指示布局元素是否可以交互。`DragDropFlagValue` 属性用于获取和设置拖放标志的值。`isDragCreateNew` 字段用于指示是否在拖动时创建新元素。`MyValueInput` 和 `MyControlOutput` 分别是 `ValueInput` 和 `ControlOutput` 类型的字段，用于存储输入和输出连接点。`Unit` 字段用于存储关联的脚本单元。`UnitConfig` 字段用于存储脚本单元的配置数据。`UnitImageType` 字段用于存储单元的图像类型。

`BaseLayout` 类的构造函数接受一个 `BaseScriptUnit` 类型的参数 `ownerUnit`，并将其赋值给 `Unit` 字段。类中还定义了一些虚方法和抽象方法，用于处理拖放操作和布局元素的显示和创建。`OnDragStart`、`OnDragUpdate`、`OnDragEnd` 和 `OnDrop` 方法分别用于处理拖放操作的开始、更新、结束和放置事件。`SetCanInteract` 方法用于设置布局元素是否可以交互。`GetConnectUnit` 方法用于获取连接的脚本单元。`Disconnect` 方法用于断开布局元素的连接，并重新连接前后单元。`Append` 方法用于将新的脚本单元追加到当前单元之后，并根据需要更新连接。

`Connect` 方法用于连接新的脚本单元，并根据输入和输出类型检查是否可以连接。`GetParentUnit` 方法用于获取父单元，遍历输入连接，找到父单元并返回。`CheckDragDropFlag` 方法用于检查拖放标志是否允许拖放操作。`CheckCanDrop` 方法用于检查是否可以放置新的脚本单元。`CheckAssetTypeCanDrop` 方法用于检查资产类型是否可以放置。`CheckTypeCanDrop` 方法用于检查类型是否可以放置，支持基本类型、数组类型和自定义类型的检查。

最后，类中定义了一些虚方法和抽象方法，用于处理布局元素的显示和创建。`OnShow` 方法用于处理布局元素的显示。`CreateLayoutElement` 方法用于创建布局元素，默认返回 `null`。`GetLayoutGameObject` 和 `SetLayoutGameObject` 方法是抽象方法，用于获取和设置布局元素的游戏对象。`CreateLayoutElementAfter` 方法用于在创建布局元素之后执行额外的操作，默认实现为空。

总体来说，这段代码实现了一个功能丰富的布局基类，提供了拖放操作、布局管理、连接和断开连接等功能。通过这些方法，可以方便地在 Unity 中管理和操作复杂的 UI 布局，提高开发效率。


1. 操作类型 ： DragDropFlag 定义可操作类型， 是否可 Drop、 Drag
2. 排列方向 ： LayoutDirection

**隐身不同类型的Layout 也就是不同的组件 如 Text Toggle  Vector2 等等等  用于可编程组件**

