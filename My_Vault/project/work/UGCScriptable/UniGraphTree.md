
```c#
    public struct RequestCreateGlobalVariableUnit
    {
        public string key;
    }

    public class CopyUnitData
    {
        public BaseScriptUnit unit;
        public Dictionary<string, CopyUnitData> valueInputs = new Dictionary<string, CopyUnitData>();
        public Dictionary<string, object> defaultValues = new Dictionary<string, object>();
        public Dictionary<string, CopyUnitData> controlOutputs = new Dictionary<string, CopyUnitData>();
    }

    public class UnitGraphTree : UnitDragTree
    {
        protected FlowGraph graph;
        protected Flow flow;
        private DragLayoutContainer oldDragParent;
        private int oldDragIndex = -1;
        public Flow CurFlow => flow;
        public FlowGraph CurGraph => graph;
        public UnitDockerTree dockerTree;
        public RectTransform DeleteImageRectTransform;
        public Image DeleteBGImage;
        public Image DeleteImage;
        public RectTransform CopyImageRectTransform;
        public Image CopyBGImage;
        public Image CopyImage;
        public Button helpButton;
        public UniPropertyDropdown OpenPropertyDropdown;
        private ISubscription<RequestCreateGlobalVariableUnit> requestCreateGlobalVariableUnitHandle;
        private ISubscription<RefreshUniListRequest> refreshUniListRequestHandle;
        private RectTransform selectImage;
        private Vector3[] worldCorners = new Vector3[4];
        public bool isDirty = false;

        public static DirectExecuteUnit GetStartUnit(FlowGraph graph)
        {
            foreach (var unit in graph.units)
            {
                if (unit is DirectExecuteUnit directExecuteUnit)
                {
                    return directExecuteUnit;
                }
            }
            return null;
        }

        protected override void Start()
        {
            base.Start();
            Root.GetViewTransform().localScale = Vector3.one * UniMain.DataModule.ScriptLayoutSetting.DefaultScale;
            helpButton.onClick.AddListener(() =>
            {
                UnityEngine.Application.OpenURL("UNI-script-tips".GetLanguageStr());
            });
        }

        public void InitTree(FlowGraph graph, Flow flow, Vector2 rootPos)
        {
            this.Clean();
            this.graph = graph;
            this.flow = flow;
            CurrentSelectedElement = null;
            if (graph != null)
            {
                this.DisplayPosition = rootPos;
                var unit = GetStartUnit(graph);
                var start = unit as BaseScriptUnit;
                var unitRoot = Root as UnitLayoutContainer;
                var unitLayout = new UnitLayout(start);
                start.layout = unitLayout;
                unitRoot.SetLayout(unitLayout);
                unitRoot.SetFlow(flow);
                Root.RebuildElements();
            }
            OnSelectedElementEvent += OnSelectedElement;
            if (requestCreateGlobalVariableUnitHandle != null)
            {
                requestCreateGlobalVariableUnitHandle.Dispose();
            }
            requestCreateGlobalVariableUnitHandle = Messenger.Default.Subscribe<RequestCreateGlobalVariableUnit>(CreateGlobalVariableUnit);
            if (refreshUniListRequestHandle != null)
            {
                refreshUniListRequestHandle.Dispose();
            }
            refreshUniListRequestHandle = Messenger.Default.Subscribe<RefreshUniListRequest>((request) =>
            {
                Root.RebuildElements();
            });
        }

        public BaseScriptUnit GetLastUnit()
        {
            BaseScriptUnit unit = null;
            if (graph != null && graph.units != null)
            {
                unit = GetStartUnit(graph);
                while (unit != null && unit.Exit != null && unit.Exit.unit != null && unit.Exit.connection != null)
                {
                    if (unit.Exit.connection.destination?.unit is BaseScriptUnit nextUnit)
                    {
                        unit = nextUnit;
                    }
                    else
                    {
                        break;
                    }
                }
            }
            return unit;
        }

        void CreateGlobalVariableUnit(RequestCreateGlobalVariableUnit req)
        {
            if (graph != null)
            {
                var curLastUnit = GetLastUnit();
                if (curLastUnit != null)
                {
                    var unit = new GetGlobalBlackboardVariableUnit();
                    graph.units.Add(unit);
                    unit.BlackboardKey = req.key;
                    (curLastUnit as BaseScriptUnit).Exit.ValidlyConnectTo(unit.Enter);
                    Root.RebuildElements();
                }
            }
        }

        public void SetDockerTree(UnitDockerTree dockerTree)
        {
            this.dockerTree = dockerTree;
        }

        public void SelectElement(DragLayoutElement ele)
        {
            CurrentSelectedElement = ele;
            OnSelectedElementEvent?.Invoke(null, ele);
        }

        private void OnSelectedElement(DragLayoutElement oldElement, DragLayoutElement currentElement)
        {
            if (currentElement != null && currentElement.View != null)
            {
                if (selectImage == null)
                {
                    selectImage = Instantiate(Global.AssetModule.SyncLoad<GameObject>("prefabs/ui/unitview/checkbox.unity3d")).GetComponent<RectTransform>();
                }
                else
                {
                    selectImage.GetComponent<Image>().enabled = true;
                }
                selectImage.SetParent(currentElement.GetViewTransform());
                selectImage.localScale = Vector3.one;
                selectImage.localEulerAngles = Vector3.zero;
                selectImage.anchoredPosition3D = Vector3.zero;
                selectImage.sizeDelta = Vector3.zero;
            }
            else if (selectImage)
            {
                selectImage.SetParent(null);
            }
        }

        public override void Update()
        {
            if (!isInDeleteOrCopy && beginDrag && DragElement != Root && DragMove())
            {
                IsInDragMove = true;
                OnDragElement(Input.mousePosition);
            }
            if (Root == null)
            {
                return;
            }
            CheckRootPositionLimit();
            bool layoutDirty = Root.LayoutDirty || isDirty;
            if (isDirty && !Root.LayoutDirty)
            {
                Root.RebuildElements();
                isDirty = false;
            }
            base.Update();
            if (layoutDirty)
            {
                Vector2 size = Root.nextViewSize;
                size.y += (Root.ChildCount + 1) * Root.YSpacing;
                Root.nextViewSize = size;
                Root.GetViewTransform().sizeDelta = size;
                for (int i = 0; i < Root.ChildCount; i++)
                {
                    if (Root.GetElement(i) is TitleLayoutContainer titleLayoutContainer)
                    {
                        titleLayoutContainer.SetTitleLength(size.y - 40);
                        break;
                    }
                }
            }
        }

        public bool DragMove()
        {
            bool isMove = false;
            Vector3 mousePosition = Input.mousePosition;
            float dragSize = 0.1f;
            float height = Screen.height * dragSize;
            float heightDeltaTime = Screen.height * Time.deltaTime;
            float ratio = dragSize * Screen.height / Screen.width;
            float width = Screen.width * ratio;
            float widthDeltaTime = Screen.width * Time.deltaTime;
            if (mousePosition.y > Screen.height * (1 - dragSize))
            {
                isMove = true;
                float lerp = Mathf.Lerp(maxDragSpeed, minDragSpeed, (Screen.height - mousePosition.y) / height);
                dragPositionOffset += new Vector2(0, -lerp * heightDeltaTime);
            }
            else if (mousePosition.y < height)
            {
                isMove = true;
                float lerp = Mathf.Lerp(maxDragSpeed, minDragSpeed, mousePosition.y / height);
                dragPositionOffset += new Vector2(0, lerp * heightDeltaTime);
            }
            if (mousePosition.x > Screen.width * (1 - ratio))
            {
                isMove = true;
                float lerp = Mathf.Lerp(maxDragSpeed, minDragSpeed, (Screen.width - mousePosition.x) / width);
                dragPositionOffset += new Vector2(-lerp * widthDeltaTime, 0);
            }
            else if (mousePosition.x < width)
            {
                isMove = true;
                float lerp = Mathf.Lerp(maxDragSpeed, minDragSpeed, mousePosition.x / width);
                dragPositionOffset += new Vector2(lerp * widthDeltaTime, 0);
            }
            return isMove;
        }

        public void CheckRootPositionLimit()
        {
            if (Root != null && dragPositionOffset != Vector2.zero)
            {
                var size = ViewTransform.rect.size;
                var scale = Root.GetViewTransform().localScale;
                float minx = -Root.GetViewSize().x * scale.x;
                float maxx = size.x;
                float x = DisplayPosition.x + dragPositionOffset.x;
                float miny = -size.y;
                float maxy = Root.GetViewSize().y * scale.x;
                float y = DisplayPosition.y + dragPositionOffset.y;
                if (x < minx)
                {
                    dragPositionOffset.x += minx - x;
                }
                else if (x > maxx)
                {
                    dragPositionOffset.x += maxx - x;
                }
                if (y < miny)
                {
                    dragPositionOffset.y += miny - y;
                }
                else if (y > maxy)
                {
                    dragPositionOffset.y += maxy - y;
                }
            }
        }

        public void RebuildLayoutByLayout(UnitLayoutContainer container, bool rebuildParent = true)
        {
            if (container != null)
            {
                if (rebuildParent)
                {
                    var parent = GetParentContainer(container);
                    if (parent != null)
                    {
                        if (parent.Layout != null && (parent.Layout.Unit is SetPropertyToUnit || parent.Layout.Unit is TweenUnit))
                        {
                            parent.Layout.Unit.refreshPropertyDataUnit = true;
                        }
                        parent.RebuildElements();
                    }
                }
                else
                {
                    container.RebuildElements();
                }
            }
        }

        public void RebuildLayoutBlackboardRef(string key, BaseScriptUnit excludeUnit, string changeNewKey = "")
        {
            foreach (var unit in CurGraph.units)
            {
                if (unit.guid == excludeUnit.guid)
                    continue;
                if (unit is not GetLocalBlackboardVariableUnit gbunit || gbunit.BlackboardKey != key)
                    continue;
                if (!gbunit.OutputValue.hasValidConnection)
                    continue;
                var connectUnit = gbunit.OutputValue.connections.First().destination.unit;
                if ((connectUnit is SetPropertyToUnit setPropertyToUnit && gbunit.OutputValue.connections.First().destination == setPropertyToUnit.InputPropertyData)
                    || (connectUnit is NumberCompareUnit numberCompareUnit && gbunit.OutputValue.connections.First().destination == numberCompareUnit.InputCompareValue1)
                    || (connectUnit is TweenUnit tweenUnit && gbunit.OutputValue.connections.First().destination == tweenUnit.InputPropertyData))
                {
                    if (gbunit.layout == null || gbunit.layout.LayoutElement is not UnitLayoutContainer container)
                        continue;
                    (connectUnit as BaseScriptUnit).refreshPropertyDataUnit = true;
                    if (!string.IsNullOrEmpty(changeNewKey) && changeNewKey != key)
                    {
                        gbunit.BlackboardKey = changeNewKey;
                    }
                    RebuildLayoutByLayout(container);
                }
            }
        }

        protected override bool CheckCanDrag(DragLayoutElement ele)
        {
            return ele is UnitLayoutContainer;
        }

        protected override DragLayoutElement GetElement(PointerEventData eventData, Func<DragLayoutElement, bool> filter = null)
        {
            if (eventData.pointerCurrentRaycast.gameObject == Root.GetViewTransform().parent.gameObject)
            {
                return null;
            }
            var ele = base.GetElement(eventData, filter);
            return ele;
        }

        public override void OnBeginDragElement(Vector2 screenPosition, DragLayoutElement ele)
        {
            if (ele is UnitLayoutContainer unitLayoutContainer)
            {
                if (unitLayoutContainer.Layout.Unit is TitleUnit)
                    return;
                if ((unitLayoutContainer.Layout.DragDropFlagValue & (int)BaseLayout.DragDropFlag.Drag) == 0)
                {
                    if (unitLayoutContainer is VectorLayoutContainer || unitLayoutContainer is PropertyUnitLayoutElement)
                    {
                        unitLayoutContainer = unitLayoutContainer.Parent as UnitLayoutContainer;
                        if (unitLayoutContainer == null || (unitLayoutContainer.Layout.DragDropFlagValue & (int)BaseLayout.DragDropFlag.CantDrag) != 0)
                            return;
                    }
                    else
                    {
                        return;
                    }
                    if ((unitLayoutContainer.Layout.DragDropFlagValue & (int)BaseLayout.DragDropFlag.Drag) == 0)
                    {
                        return;
                    }
                }
                if (!unitLayoutContainer.Layout.isDragCreateNew)
                {
                    DragElement = unitLayoutContainer;
                    oldDragParent = unitLayoutContainer.Parent as UnitLayoutContainer;
                    oldDragIndex = oldDragParent.IndexOf(unitLayoutContainer);
                    unitLayoutContainer.SetParent(null);
                    unitLayoutContainer.GetViewTransform().SetParent(FreeMoveLayer);
                    unitLayoutContainer.Layout.Disconnect();
                    //graph.units.Remove(unitLayoutContainer.Layout.Unit);
                    oldDragParent.RebuildElements();
                }
                else
                {
                    var unit = unitLayoutContainer.Layout.Unit;
                    if (unit != null)
                    {
                        // oldDragParent = unitLayoutContainer.Parent;
                        // oldDragIndex = oldDragParent.IndexOf(unitLayoutContainer);
                        var def = new UnitLayout(unit);
                        def.isDragCreateNew = true;
                        def.UnitConfig = unitLayoutContainer.Layout.UnitConfig;
                        DragElement = CreateLayoutElement(null, def);
                        var t = DragElement.GetViewTransform();
                        var et = ele.GetViewTransform();
                        t.SetParent(FreeMoveLayer);
                        t.localScale = Vector3.one;
                        t.position = et.position;
                        Camera camera = UniGameCameras.GetInstance().GetUICamera();
                        RectTransformUtility.ScreenPointToLocalPointInRectangle(et, screenPosition, camera, out var dragLocalPosition);
                        dragLocalPosition += t.anchoredPosition;
                        RectTransformUtility.ScreenPointToLocalPointInRectangle(FreeMoveLayer, screenPosition, camera, out var viewLocal);
                        t.anchoredPosition += (viewLocal - dragLocalPosition);
                        DragElement.MarkLayoutDirty();
                        def.OnShow();
                        // oldDragParent.RebuildElements(flow);
                    }
                }
                if (DragElement != null)
                {
                    dockerTree.SidebarGameObject.SetActive(false);
                    dockerTree.DockerList.gameObject.SetActive(false);
                    if (PreIndicator == null)
                    {
                        PreIndicator = Instantiate(Global.AssetModule.SyncLoad<GameObject>("prefabs/ui/unitview/preindicator.unity3d")).GetComponent<RectTransform>();
                    }
                    PreIndicator.SetParent(DragElement.GetViewTransform());
                    PreIndicator.anchoredPosition = new Vector2(3, -3);
                    PreIndicator.localPosition = Vector3.zero;
                    PreIndicator.localEulerAngles = Vector3.zero;
                    PreIndicator.localScale = Vector3.one;
                }
            }
        }

        public override void OnEndDragElement(Vector2 screenPosition, bool isReverse = false)
        {
            dockerTree.SidebarGameObject.SetActive(true);
            dockerTree.DockerList.gameObject.SetActive(true);
            var dragContainer = DragElement as UnitLayoutContainer;
            if (isReverse || !AcceptDrop(dragContainer, screenPosition, dragContainer.Layout.isDragCreateNew))
            {
                // DeleteElement(CurFlow, DragElement);
                if (DragElement is UnitLayoutContainer unitLayoutContainer)
                {
                    // if (tempLayout != null)
                    // {
                    //     oldDragParent.RemoveElement(tempLayout.LayoutElement as DragLayoutElement);
                    // }
                    //graph.units.Add(unitLayoutContainer.Layout.Unit);
                    DragLayoutElement ele = null;
                    if (oldDragIndex >= 0)
                    {
                        if (oldDragParent is UnitLayoutContainer oldDragContainer)
                        {
                            if (oldDragContainer.Layout.Unit is DirectExecuteUnit)
                            {
                                oldDragIndex = oldDragIndex - 1;
                            }
                        }
                        ele = oldDragParent.GetElement(oldDragIndex, true);
                    }
                    else
                    {
                        ele = oldDragParent;
                    }

                    if (ele is UnitLayoutContainer container)
                    {
                        container.Layout.Append(unitLayoutContainer.Layout.Unit);
                        if (container.Parent == null)
                        {
                            Root.RebuildElements();
                        }
                        else
                        {
                            container.Parent.RebuildElements();
                        }
                    }
                    else if (ele is UnitLayoutElement unitElement)
                    {
                        var result = unitElement.Layout.Connect(unitLayoutContainer.Layout.Unit, true);
                        if (result.Item1)
                        {
                            if (result.Item2)
                            {
                                Root.RebuildElements();
                            }
                            else
                            {
                                unitElement.Parent.RebuildElements();
                            }
                        }
                    }
                }
            }
            else
            {
                OnAddHistoryEvent?.Invoke();
            }
            base.OnEndDragElement(screenPosition, isReverse);
        }

        BaseScriptUnit CloneOrGetPrefabUnit(UniScriptUnitConfig.ScriptUnitConfigData unitConfig, BaseScriptUnit unit, UnitLayout layout)
        {
            if (unitConfig != null)
            {
                unit = unitConfig.GetReallyUnit(graph);
                if (!unitConfig.IsAdded)
                {
                    graph.units.Add(unit);
                }
            }
            else
            {
                unit = Clone(unit);
                graph.units.Add(unit);
            }
            unit.Initialize();
            // unit.layout = layout;
            return unit;
        }

        public bool AcceptDrop(UnitLayoutContainer ele, Vector2 screenPosition, bool cloneUnit)
        {
            if (ele == null) return false;
            if (Root.ChildCount == 1)
            {
                var unit = ele.Layout.Unit;
                var unitConfig = ele.Layout.UnitConfig;
                if (cloneUnit)
                {
                    unit = CloneOrGetPrefabUnit(unitConfig, unit, ele.Layout as UnitLayout);
                }
                currentSelectUnit = unit;
                (Root.GetFirst() as IUnitLayoutElement).GetLayout().Append(unit);
                Root.RebuildElements();
                if (cloneUnit && unit is ModifyObjectPropertysUnit)
                {
                    Messenger.Default.Publish(new ModifyUnitMessage() { Unit = unit });
                }
                return true;
            }
            else
            {
                var unitRoot = Root as UnitLayoutContainer;
                //以左上角的坐标为测试点
                var targetTransform = ele.GetViewTransform();
                screenPosition = RectTransformUtility.WorldToScreenPoint(UniGameCameras.GetInstance().GetUICamera(), targetTransform.position);
                var conEle = unitRoot.GetElement(screenPosition, (dragItem) =>
                {
                    if (dragItem.Parent == null)
                    {
                        return true;
                    }
                    if (dragItem is IUnitLayoutElement layoutElement)
                    {
                        if (layoutElement.GetLayout() is TextLayout)
                        {
                            return false;
                        }
                    }
                    return true;
                });
                //插入到所选节点的上面
                // if ((positionType & DragLayoutElement.GetElementPositionType.Up) > 0 && conEle.LayoutStyle == DragLayoutElement.ELayoutStyle.Vertical)
                // {
                //     if (frontEle == null || frontEle.LayoutStyle == DragLayoutElement.ELayoutStyle.Horizontal)
                //     {
                //         conEle = conEle.Parent;
                //     }
                //     else
                //     {
                //         conEle = frontEle;
                //     }
                // }
                for (int i = DragLayoutElement.ResultAllElement.Count - 1; i >= 0; i--)
                {
                    conEle = DragLayoutElement.ResultAllElement[i].element;
                    if (conEle is IUnitLayoutElement unitLayoutElement)
                    {
                        //为根节点
                        if (conEle.Parent == null)
                        {
                            conEle = null;
                            continue;
                        }
                        var layout = unitLayoutElement.GetLayout();
                        if ((layout.dragDropFlagValue & (int)BaseLayout.DragDropFlag.CantDrop) != 0)
                        {
                            continue;
                        }
                        if (layout is UnitLayout unitLayout)
                        {
                            var unit = ele.Layout.Unit;
                            if (layout.CheckCanDrop(unit))
                            {
                                var unitConfig = ele.Layout.UnitConfig;
                                if (cloneUnit)
                                {
                                    unit = CloneOrGetPrefabUnit(unitConfig, unit, ele.Layout as UnitLayout);
                                }
                                currentSelectUnit = unit;
                                if (layout.MyValueInput != null)
                                {
                                    var result = layout.Connect(unit);
                                    if (result.Item1)
                                    {
                                        if (result.Item2)
                                        {
                                            Root.RebuildElements();
                                        }
                                        else
                                        {
                                            conEle.Parent.RebuildElements();
                                        }
                                    }
                                }
                                else
                                {
                                    unitLayoutElement.GetLayout().Append(unit);
                                    conEle.Parent.RebuildElements();
                                }
                                if (cloneUnit && unit is ModifyObjectPropertysUnit)
                                {
                                    Messenger.Default.Publish(new ModifyUnitMessage() { Unit = unit });
                                }
                                return true;
                            }
                        }
                        else
                        {
                            var unit = ele.Layout.Unit;
                            if (unitLayoutElement.GetLayout().CheckCanDrop(unit))
                            {
                                var unitConfig = ele.Layout.UnitConfig;
                                if (cloneUnit)
                                {
                                    unit = CloneOrGetPrefabUnit(unitConfig, unit, ele.Layout as UnitLayout);
                                }
                                currentSelectUnit = unit;
                                var result = unitLayoutElement.GetLayout().Connect(unit);
                                if (result.Item1)
                                {
                                    if (result.Item2)
                                    {
                                        Root.RebuildElements();
                                    }
                                    else
                                    {
                                        conEle.Parent.RebuildElements();
                                    }
                                }
                                if (cloneUnit && unit is ModifyObjectPropertysUnit)
                                {
                                    Messenger.Default.Publish(new ModifyUnitMessage() { Unit = unit });
                                }
                                return true;
                            }
                        }
                    }
                }

                conEle = unitRoot.GetElement(screenPosition.y, (dragItem) =>
                {
                    if (dragItem.Parent == null)
                    {
                        return true;
                    }
                    if (dragItem is IUnitLayoutElement layoutElement)
                    {
                        if (layoutElement.GetLayout() is TextLayout)
                        {
                            return false;
                        }
                    }
                    return true;
                });
                for (int i = DragLayoutElement.ResultAllElement.Count - 1; i >= 0; i--)
                {
                    conEle = DragLayoutElement.ResultAllElement[i].element;
                    if (conEle is IUnitLayoutElement unitLayoutElement)
                    {
                        //为根节点
                        if (conEle.Parent == null)
                        {
                            conEle = null;
                            continue;
                        }
                        var layout = unitLayoutElement.GetLayout();
                        if (layout is UnitLayout unitLayout)
                        {
                            var unit = ele.Layout.Unit;
                            var tLayout = unitLayoutElement.GetLayout();
                            if (tLayout.CheckCanDrop(unit) && tLayout.MyValueInput == null)
                            {
                                var unitConfig = ele.Layout.UnitConfig;
                                if (cloneUnit)
                                {
                                    unit = CloneOrGetPrefabUnit(unitConfig, unit, ele.Layout as UnitLayout);
                                }
                                currentSelectUnit = unit;
                                unitLayoutElement.GetLayout().Append(unit);
                                conEle.Parent.RebuildElements();

                                if (cloneUnit && unit is ModifyObjectPropertysUnit)
                                {
                                    Messenger.Default.Publish(new ModifyUnitMessage() { Unit = unit });
                                }
                                return true;
                            }
                        }
                        else
                        {
                            var unit = ele.Layout.Unit;
                            if (unitLayoutElement.GetLayout().CheckCanDrop(unit))
                            {
                                var unitConfig = ele.Layout.UnitConfig;
                                if (cloneUnit)
                                {
                                    unit = CloneOrGetPrefabUnit(unitConfig, unit, ele.Layout as UnitLayout);
                                }
                                currentSelectUnit = unit;
                                if (unitLayoutElement.GetLayout().MyControlOutput != null)
                                {
                                    var result = unitLayoutElement.GetLayout().Connect(unit);
                                    if (result.Item1)
                                    {
                                        if (result.Item2)
                                        {
                                            Root.RebuildElements();
                                        }
                                        else
                                        {
                                            conEle.Parent.RebuildElements();
                                        }
                                    }
                                    if (cloneUnit && unit is ModifyObjectPropertysUnit)
                                    {
                                        Messenger.Default.Publish(new ModifyUnitMessage() { Unit = unit });
                                    }
                                    return true;
                                }
                            }
                        }
                    }
                }
                if (conEle == null)
                {
                    if (screenPosition.y > RectTransformUtility.WorldToScreenPoint(UniGameCameras.GetInstance().GetUICamera(), Root.GetViewTransform().position).y - 15)
                    {
                        AcceptDropAtFirst(ele, cloneUnit);
                    }
                    else
                    {
                        AcceptDropAtLast(ele, cloneUnit);
                    }
                    return true;
                }
            }
            return false;
        }

        public void AcceptDropAtLast(UnitLayoutContainer ele, bool cloneUnit)
        {
            var unit = ele.Layout.Unit;
            var unitConfig = ele.Layout.UnitConfig;
            if (cloneUnit)
            {
                unit = CloneOrGetPrefabUnit(unitConfig, unit, ele.Layout as UnitLayout);
            }
            currentSelectUnit = unit;
            if (Root.GetLast() is IUnitLayoutElement unitLayoutElement)
            {
                unitLayoutElement.GetLayout().Append(unit);
            }
            Root.RebuildElements();
            if (cloneUnit && unit is ModifyObjectPropertysUnit)
            {
                Messenger.Default.Publish(new ModifyUnitMessage() { Unit = unit });
            }
            OnAddHistoryEvent?.Invoke();
        }

        public void AcceptDropAtFirst(UnitLayoutContainer ele, bool cloneUnit)
        {
            var unit = ele.Layout.Unit;
            var unitConfig = ele.Layout.UnitConfig;
            if (cloneUnit)
            {
                unit = CloneOrGetPrefabUnit(unitConfig, unit, ele.Layout as UnitLayout);
            }
            currentSelectUnit = unit;
            if (Root.GetFirst() is IUnitLayoutElement unitLayoutElement)
            {
                unitLayoutElement.GetLayout().Append(unit);
            }
            Root.RebuildElements();
            if (cloneUnit && unit is ModifyObjectPropertysUnit)
            {
                Messenger.Default.Publish(new ModifyUnitMessage() { Unit = unit });
            }
            OnAddHistoryEvent?.Invoke();
        }

        public void CopyAndPasteDragElement(IUnitLayoutElement dragElement)
        {
            if (dragElement != null)
            {
                var layout = dragElement.GetLayout();
                if (layout == null)
                    return;
                var unit = layout.Unit;
                
                if(unit == null)
                    return;
                var newUnitData = CopyUnit(unit); 
                PasteUnit(newUnitData);

                if (CurrentSelectedElement is UnitLayoutContainer container)
                {
                    var containerLayout = container.Layout;
                    if(containerLayout == null)
                        return;
                    var selectUnit = containerLayout.Unit;
                    if (selectUnit == null)
                    {
                        selectUnit = unit;
                    }
                    if (selectUnit.Exit.hasValidConnection)
                    {
                        var curExitUnit = selectUnit.Exit.connection.destination.unit;
                        selectUnit.Exit.Disconnect();
                        selectUnit.Exit.ConnectToValid(newUnitData.unit.Enter);

                        newUnitData.unit.Exit.ConnectToValid((curExitUnit as BaseScriptUnit).Enter);
                    }
                    else
                    {
                        selectUnit.Exit.ValidlyConnectTo(newUnitData.unit.Enter);
                    }
                }
                else
                {
                    GetLastUnit().Exit.ValidlyConnectTo(newUnitData.unit.Enter);
                }

                currentSelectUnit = newUnitData.unit;

                isDirty = true;
                if (unit is ModifyObjectPropertysUnit)
                {
                    Messenger.Default.Publish(new ModifyUnitMessage() { Unit = newUnitData.unit });
                }
                OnSelectedElementEvent?.Invoke(CurrentSelectedElement, null);
            }
        }

        public void CopyAndPasteSelectedElement(Flow flow)
        {
            if (CurrentSelectedElement is UnitLayoutContainer unitLayoutElement)
            {
                var unit = unitLayoutElement.Layout.Unit;
                var newUnitData = CopyUnit(unit);
                PasteUnit(newUnitData);

                currentSelectUnit = newUnitData.unit;

                if (unit.Exit.hasValidConnection)
                {
                    var curExitUnit = unit.Exit.connection.destination.unit;
                    unit.Exit.Disconnect();
                    unit.Exit.ConnectToValid(newUnitData.unit.Enter);

                    newUnitData.unit.Exit.ConnectToValid((curExitUnit as BaseScriptUnit).Enter);
                }
                else
                {
                    unit.Exit.ValidlyConnectTo(newUnitData.unit.Enter);
                }

                isDirty = true;
                if (unit is ModifyObjectPropertysUnit)
                {
                    Messenger.Default.Publish(new ModifyUnitMessage() { Unit = newUnitData.unit });
                }
                OnSelectedElementEvent?.Invoke(CurrentSelectedElement, null);
            }
        }

        public void CopySelectedElement(Flow flow)
        {
            if (CurrentSelectedElement is UnitLayoutContainer unitLayoutElement)
            {
                var uniModModule = UniMain.ModuleManager.Get<UniModModule>();
                if (uniModModule != null)
                {
                    uniModModule.CurrentCopiedElement = new UnitLayoutContainer();
                    unitLayoutElement.Clone(uniModModule.CurrentCopiedElement);

                    uniModModule.CurrentCopiedUnitData = CopyUnit(unitLayoutElement.Layout.Unit);
                    OnSelectedElementEvent?.Invoke(null, CurrentSelectedElement);
                }
            }
        }

        public void PasteElement(Flow flow)
        {
            var uniModModule = UniMain.ModuleManager.Get<UniModModule>();
            if (uniModModule != null && uniModModule.CurrentCopiedElement != null && uniModModule.CurrentCopiedUnitData != null)
            {
                var unit = uniModModule.CurrentCopiedElement.Layout.Unit;
                var newUnitData = uniModModule.CurrentCopiedUnitData;
                PasteUnit(newUnitData);

                if (CurrentSelectedElement is UnitLayoutContainer container)
                {
                    var selectUnit = container.Layout.Unit;
                    if (selectUnit == null)
                    {
                        selectUnit = unit;
                    }
                    if (selectUnit.Exit.hasValidConnection)
                    {
                        var curExitUnit = selectUnit.Exit.connection.destination.unit;
                        selectUnit.Exit.Disconnect();
                        selectUnit.Exit.ConnectToValid(newUnitData.unit.Enter);

                        newUnitData.unit.Exit.ConnectToValid((curExitUnit as BaseScriptUnit).Enter);
                    }
                    else
                    {
                        selectUnit.Exit.ValidlyConnectTo(newUnitData.unit.Enter);
                    }
                }
                else
                {
                    GetLastUnit().Exit.ValidlyConnectTo(newUnitData.unit.Enter);
                }

                currentSelectUnit = newUnitData.unit;
                // Root.RebuildElements();
                isDirty = true;
                if (unit is ModifyObjectPropertysUnit)
                {
                    Messenger.Default.Publish(new ModifyUnitMessage() { Unit = newUnitData.unit });
                }
                uniModModule.CurrentCopiedElement = null;
                OnSelectedElementEvent?.Invoke(null, CurrentSelectedElement);
            }
        }

        private void PasteUnit(CopyUnitData data)
        {
            if (!Global.Game.Scene.IsSupport2DEdit)
            {
                if (data.unit is GetNodeUnit getNodeUnit && ((UniNode)getNodeUnit.GroupObjectRef) is UniUINode)
                {
                    getNodeUnit.GroupObjectRef.UintKey = 0;
                }
                if (data.unit is PropertyUniNodeSetterUnitV2 setterUnitV2 && ((UniNode)setterUnitV2.GroupObjectRef) is UniUINode)
                {
                    setterUnitV2.GroupObjectRef.UintKey = 0;
                }
            }
            if (data.unit is AdvertisementUnit)
            {
                UniMain.TrackEvent.UploadStatistics(ConstValue.SHUSHU_EVENT_CLICK, () => {
                    return new Dictionary<string, object>(){
                        {"page_name", "unity_command"},
                        {"page_element", "play_ad"},
                        {"is_copy ", true},
                    };
                });
            }
            graph.units.Add(data.unit);
            foreach (var vi in data.valueInputs)
            {
                if (data.unit.valueInputs.TryGetValue(vi.Key, out var newVi))
                {
                    PasteUnit(vi.Value);
                    newVi.ValidlyConnectTo(vi.Value.unit.valueOutputs.First());
                }
            }

            foreach (var viDefault in data.defaultValues)
            {
                if (data.unit.valueInputs.TryGetValue(viDefault.Key, out var newVi))
                {
                    newVi.SetDefaultValue(viDefault.Value);
                }
            }

            foreach (var co in data.controlOutputs)
            {
                if (data.unit.controlOutputs.TryGetValue(co.Key, out var newCo))
                {
                    PasteUnit(co.Value);
                    newCo.ValidlyConnectTo(co.Value.unit.Enter);
                }
            }
            data.unit.Initialize();
        }

        private CopyUnitData CopyUnit(BaseScriptUnit unit, bool includeExit = false)
        {
            var newUnit = (BaseScriptUnit)Activator.CreateInstance(unit.GetType());
            unit.CopyData(newUnit);
            newUnit.Define();
            var data = new CopyUnitData();
            data.unit = newUnit;
            // graph.units.Add(newUnit);
            foreach (var vi in unit.valueInputs)
            {
                if (vi.hasValidConnection)
                {
                    var n = CopyUnit(vi.connection.source.unit as BaseScriptUnit);
                    data.valueInputs.Add(vi.key, n);
                }
                else
                {
                    if (newUnit.valueInputs.TryGetValue(vi.key, out var newVi))
                    {
                        if (unit.defaultValues.TryGetValue(vi.key, out var value))
                        {
                            data.defaultValues.Add(vi.key, value);
                        }
                    }
                }
            }
            foreach (var co in unit.controlOutputs)
            {
                if (co.hasValidConnection)
                {
                    if (!includeExit && co.key == "Exit")
                        continue;
                    var n = CopyUnit(co.connection.destination.unit as BaseScriptUnit, true);
                    data.controlOutputs.Add(co.key, n);
                }
            }
            return data;
        }

        public void DisableUnit(bool isDisable)
        {
            if (CurrentSelectedElement is UnitLayoutContainer unitLayoutElement)
            {
                var unit = unitLayoutElement.Layout.Unit;
                if (string.IsNullOrEmpty(unit.category))
                    return;
                if (unit != null && unit.category != "Expression")
                {
                    unit.isDisabled = isDisable;
                    unitLayoutElement.RebuildElements();
                    OnSelectedElementEvent?.Invoke(null, CurrentSelectedElement);
                }
            }
        }

        public override void OnScroll(PointerEventData eventData)
        {
            base.OnScroll(eventData);
#if UNITY_STANDALONE || UNITY_EDITOR
            var t = Root.GetViewTransform();
            var oldScale = t.localScale;
            ScaleRoot(eventData.position, oldScale.x * (eventData.scrollDelta.y * 0.1f + 1));
#endif
        }

        public override void OnBeginDrag(PointerEventData eventData)
        {
            base.OnBeginDrag(eventData);
            if (DragElement != null && DragElement != Root && DragElement is UnitLayoutContainer container && !container.Layout.isDragCreateNew)
            {
                dockerTree.Hide(true);
                DeleteImageRectTransform.gameObject.SetActive(true);
                CopyImageRectTransform.gameObject.SetActive(true);
            }
        }

        protected bool isInDeleteOrCopy = false;

        public override void OnDrag(PointerEventData eventData)
        {
            base.OnDrag(eventData);
            var camera = UniGameCameras.GetInstance().GetUICamera();
            RectTransformUtility.ScreenPointToLocalPointInRectangle(DeleteImageRectTransform, eventData.position, camera, out var pos);
            //DeleteImageRectTransform.GetWorldCorners(worldCorners);
            if (DeleteImageRectTransform.gameObject.activeSelf
                && DeleteImageRectTransform.rect.Contains(pos))
            {
                isInDeleteOrCopy = true;
                DeleteBGImage.color = new Color(1, 1, 1, 1);
                DeleteImage.color = new Color(0, 0, 0, 1);
            }
            else
            {
                isInDeleteOrCopy = false;
                DeleteBGImage.color = new Color(0, 0, 0, 0.5f);
                DeleteImage.color = new Color(1, 1, 1, 1);
            }
            RectTransformUtility.ScreenPointToLocalPointInRectangle(CopyImageRectTransform, eventData.position, camera, out var copyPos);
            //DeleteImageRectTransform.GetWorldCorners(worldCorners);
            if (CopyImageRectTransform.gameObject.activeSelf
                && CopyImageRectTransform.rect.Contains(copyPos))
            {
                isInDeleteOrCopy = true;
                CopyBGImage.color = new Color(1, 1, 1, 1);
                CopyImage.color = new Color(0, 0, 0, 1);
            }
            else
            {
                //不需要在这里 isInDeleteOrCopy = false 因为上面改为true时这里不能改为false
                CopyBGImage.color = new Color(0, 0, 0, 0.5f);
                CopyImage.color = new Color(1, 1, 1, 1);
            }
        }

        public override void OnEndDrag(PointerEventData eventData)
        {
            isInDeleteOrCopy = false;
            isUseEndDrag = false;
            beginDrag = false;
            var camera = UniGameCameras.GetInstance().GetUICamera();
            bool isDelete = DeleteImageRectTransform.gameObject.activeSelf;
            bool isCopy = CopyImageRectTransform.gameObject.activeSelf;
            DeleteImageRectTransform.gameObject.SetActive(false);
            CopyImageRectTransform.gameObject.SetActive(false);
            RectTransformUtility.ScreenPointToLocalPointInRectangle(DeleteImageRectTransform, eventData.position, camera, out var pos);
            if (isDelete && DeleteImageRectTransform.rect.Contains(pos))
            {
                DeleteImageRectTransform.gameObject.SetActive(false);
                DeletedDragElement();
                dockerTree.SidebarGameObject.SetActive(true);
                dockerTree.DockerList.gameObject.SetActive(true);
                base.OnEndDragElement(pos);
                return;
            }
            RectTransformUtility.ScreenPointToLocalPointInRectangle(CopyImageRectTransform, eventData.position, camera, out var copyPos);
            if (isCopy && CopyImageRectTransform.rect.Contains(copyPos))
            {
                var drag = DragElement as IUnitLayoutElement;
                CopyImageRectTransform.gameObject.SetActive(false);
                OnEndDragElement(pos, true);
                CopyAndPasteDragElement(drag);
                dockerTree.SidebarGameObject.SetActive(true);
                dockerTree.DockerList.gameObject.SetActive(true);
                return;
            }
            base.OnEndDrag(eventData);
        }

        public override void OnPointerClick(PointerEventData eventData)
        {
            if (DragElement != null && DragElement != Root)
            {
                return;
            }
            if (Vector2.Distance(eventData.pointerPressRaycast.screenPosition, eventData.pointerCurrentRaycast.screenPosition) < 10)
            {
                CloseAllDropDown();
            }
            base.OnPointerClick(eventData);
        }

        public override void OnPointerUp(PointerEventData eventData)
        {
            base.OnPointerUp(eventData);
            if (this.dockerTree != null)
            {
                this.dockerTree.Hide(true);
            }
            // if (UISystem.Inst.IsUIActive(UIName.ConversationAddUnitsList))
            // {
            //     UISystem.Inst.CLoseCurrentPopPanel();
            // }
        }

        protected override void ScaleRoot(Vector2 pointer, float scale)
        {
            scale = Mathf.Clamp(scale, UniMain.DataModule.ScriptLayoutSetting.ScaleMin, UniMain.DataModule.ScriptLayoutSetting.ScaleMax);
            base.ScaleRoot(pointer, scale);
        }

        public void CloseAllDropDown()
        {
            Root.AllElementsDepthTraversal(x =>
            {
                if (x is PropertyUnitLayoutElement { Layout: PropertyDropdownLayout propertyDropdownLayout })
                {
                    propertyDropdownLayout.MyDropdown.Hide(false);
                }
                else if (x is CurveDropdownLayoutElement { Layout: CurveDropdownLayout curveDropdownLayout })
                {
                    curveDropdownLayout.Hide();
                }
            });
        }

        public bool CheckUnitError(out IUnit errorUnit)
        {
            errorUnit = null;
            if (graph == null || graph.units == null)
            {
                return false;
            }
            foreach (IUnit unit in graph.units)
            {
                errorUnit = unit;
                if (unit is not BaseScriptUnit baseScriptUnit || (baseScriptUnit.Enter == null && baseScriptUnit.Exit == null && !baseScriptUnit.Enter.hasAnyConnection && !baseScriptUnit.Exit.hasAnyConnection) || baseScriptUnit.layout == null || baseScriptUnit.layout.LayoutElement is not DragLayoutElement dragLayoutElement || dragLayoutElement.Tree is not UnitGraphTree)
                {
                    continue;
                }
                bool isDisabled = false;
                while (dragLayoutElement.Parent != null)
                {
                    if (dragLayoutElement.Parent is UnitLayoutContainer unitLayoutContainer && unitLayoutContainer.Layout.Unit.isDisabled)
                    {
                        isDisabled = true;
                        break;
                    }
                    dragLayoutElement = dragLayoutElement.Parent;
                }
                if (isDisabled)
                {
                    continue;
                }
                if (unit is GetNodeUnit getNodeUnit)
                {
                    if (getNodeUnit.GroupObjectRef.UintKey == 0 && getNodeUnit.OutputNode.hasAnyConnection) //没有父节点不算错误
                    {
                        return true;
                    }
                }
                else if (unit is PropertyUniNodeSetterUnitV2 uniNodeSetterUnitV2)
                {
                    if (uniNodeSetterUnitV2.SelectIndex == 2 && uniNodeSetterUnitV2.GroupObjectRef.UintKey == 0 && uniNodeSetterUnitV2.OutputValue.hasAnyConnection) //没有父节点不算错误
                    {
                        return true;
                    }
                }
                else if (unit is GetUniPropertyDataUnit uniPropertyDataUnit)
                {
                    if (uniPropertyDataUnit.FuncList.Count == 0 || uniPropertyDataUnit.InputObject.connection == null) //input没链接也算错误
                    {
                        return true;
                    }
                }
                else if (unit is GetObjectCommandUnit getObjectCommandUnit)
                {
                    if (getObjectCommandUnit.FuncList.Count == 0 || getObjectCommandUnit.InputNode.connection == null) //input没链接也算错误
                    {
                        return true;
                    }
                }
            }
            return false;
        }

        public void MoveUnitToScreenMiddle(BaseScriptUnit baseScriptUnit)
        {
            var camera = UniGameCameras.GetInstance().GetUICamera();
            RectTransform viewTransform = (baseScriptUnit.layout.LayoutElement as DragLayoutElement).GetViewTransform();
            Vector2 size = viewTransform.sizeDelta;
            RectTransform rectTransform = Root.GetViewTransform();
            var localScale = rectTransform.localScale;
            RectTransformUtility.ScreenPointToLocalPointInRectangle(rectTransform, RectTransformUtility.WorldToScreenPoint(camera, viewTransform.position), camera, out var pos);
            DisplayPosition = new Vector2((1920 - size.x * localScale.x) / 2f - pos.x * localScale.x, (size.y * localScale.x - 1080) / 2f - pos.y * localScale.x);
            dragPositionOffset = Vector2.zero;
            Image img = viewTransform.GetComponentInChildren<Image>();
            if (img != null)
            {
                Color color = img.color;
                DOTween.To(() => img.color, x => img.color = x, Color.red, 0.25f).OnComplete(() =>
                {
                    DOTween.To(() => img.color, x => img.color = x, color, 0.25f);
                });
            }
        }
    }
```



Update : if is dirty --> 进行重新排版. 













类继承自 `UnitDragTree`，用于在 Unity 中管理和操作脚本单元的图形树结构。该类包含多个字段和方法，用于处理脚本单元的初始化、拖放、复制、粘贴、删除、布局更新等功能。

首先，类中定义了几个字段，包括 `graph`、`flow`、`oldDragParent`、`oldDragIndex`、`dockerTree`、`DeleteImageRectTransform`、`DeleteBGImage`、`DeleteImage`、`CopyImageRectTransform`、`CopyBGImage`、`CopyImage`、`helpButton`、`OpenPropertyDropdown`、`requestCreateGlobalVariableUnitHandle`、`refreshUniListRequestHandle`、`selectImage`、`worldCorners` 和 `isDirty`。这些字段用于存储脚本单元的图形、流程、拖放操作的状态、UI 元素和事件订阅等信息。

`GetStartUnit` 方法用于获取流程图中的起始单元，遍历流程图中的所有单元，如果某个单元是 `DirectExecuteUnit` 类型，则返回该单元。`Start` 方法重写了基类的 `Start` 方法，用于初始化脚本单元的图形树结构，并设置帮助按钮的点击事件，打开脚本提示的 URL。

`InitTree` 方法用于初始化脚本单元的图形树结构，接受一个 `FlowGraph` 类型的参数 `graph` 和一个 `Flow` 类型的参数 `flow`，以及一个 `Vector2` 类型的参数 `rootPos`。方法首先清理当前的图形树结构，然后设置新的图形和流程，并根据传入的图形和流程初始化根节点的布局和位置。方法还订阅了全局变量单元创建请求和刷新列表请求的事件。

`GetLastUnit` 方法用于获取流程图中的最后一个单元，从起始单元开始，沿着连接遍历所有单元，直到找到最后一个单元。`CreateGlobalVariableUnit` 方法用于创建全局变量单元，并将其添加到流程图中。

`SetDockerTree` 方法用于设置 `dockerTree` 字段。`SelectElement` 方法用于选择一个拖放元素，并触发选中元素事件。`OnSelectedElement` 方法用于处理选中元素事件，更新选中元素的高亮显示。

`Update` 方法重写了基类的 `Update` 方法，用于更新脚本单元的图形树结构。如果正在拖动元素，则调用 `DragMove` 方法更新拖动位置。方法还检查根节点的位置限制，并根据需要重新构建布局。

`DragMove` 方法用于处理拖动操作，根据鼠标位置更新拖动偏移量。`CheckRootPositionLimit` 方法用于检查根节点的位置限制，并根据需要调整拖动偏移量。

`RebuildLayoutByLayout` 方法用于根据布局容器重新构建布局。`RebuildLayoutBlackboardRef` 方法用于根据黑板引用重新构建布局。

`CheckCanDrag` 方法重写了基类的 `CheckCanDrag` 方法，用于检查是否可以拖动元素。`GetElement` 方法重写了基类的 `GetElement` 方法，用于获取拖放元素。

`OnBeginDragElement` 方法重写了基类的 `OnBeginDragElement` 方法，用于处理拖动元素的开始事件。方法根据拖动元素的类型和状态，设置拖动元素的父节点和位置，并断开连接。

`OnEndDragElement` 方法重写了基类的 `OnEndDragElement` 方法，用于处理拖动元素的结束事件。方法根据拖动位置和拖动元素的状态，决定是否接受拖动元素，并重新构建布局。

`CloneOrGetPrefabUnit` 方法用于克隆或获取预制单元，并将其添加到流程图中。`AcceptDrop` 方法用于检查是否接受拖动元素，并根据拖动位置和状态决定是否接受拖动元素。

`AcceptDropAtLast` 和 `AcceptDropAtFirst` 方法分别用于在最后和最前接受拖动元素，并重新构建布局。

`CopyAndPasteDragElement` 方法用于复制和粘贴拖动元素。`CopyAndPasteSelectedElement` 方法用于复制和粘贴选中元素。`CopySelectedElement` 方法用于复制选中元素。`PasteElement` 方法用于粘贴元素。

`PasteUnit` 方法用于粘贴单元数据，并根据连接关系重新连接单元。`CopyUnit` 方法用于复制单元数据，并返回复制的数据对象。

`DisableUnit` 方法用于禁用或启用选中单元。`OnScroll` 方法重写了基类的 `OnScroll` 方法，用于处理滚动事件，并根据滚动位置缩放根节点。

`OnBeginDrag` 方法重写了基类的 `OnBeginDrag` 方法，用于处理拖动开始事件，并显示删除和复制图标。`OnDrag` 方法重写了基类的 `OnDrag` 方法，用于处理拖动事件，并更新删除和复制图标的状态。

`OnEndDrag` 方法重写了基类的 `OnEndDrag` 方法，用于处理拖动结束事件，并根据拖动位置决定是否删除或复制拖动元素。

`OnPointerClick` 方法重写了基类的 `OnPointerClick` 方法，用于处理点击事件，并关闭所有下拉菜单。`OnPointerUp` 方法重写了基类的 `OnPointerUp` 方法，用于处理指针抬起事件，并隐藏 `dockerTree`。

`ScaleRoot` 方法重写了基类的 `ScaleRoot` 方法，用于缩放根节点。`CloseAllDropDown` 方法用于关闭所有下拉菜单。

`CheckUnitError` 方法用于检查单元是否有错误，并返回错误单元。`MoveUnitToScreenMiddle` 方法用于将单元移动到屏幕中间，并高亮显示。