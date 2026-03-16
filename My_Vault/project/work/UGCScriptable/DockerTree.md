
右侧小栏可拖拽单元， 选中指定的组件，以及部分状态切换

```c#
    public class UnitDockerTree : UnitDragTree
    {
        public RectTransform DockerList;
        public Button CategoryButtonTemplate;
        public Dictionary<string, Button> CategoryButtonDict = new Dictionary<string, Button>();
        public GameObject Bg;
        public GameObject Mask;
        public GameObject SidebarGameObject;
        public Toggle SidebarToggleTemplate;

        private bool isClickSecondaryTitle = false;
        private List<Toggle> sidebarToggleList = new List<Toggle>();
        private List<RectTransform> sidebarWidthList = new List<RectTransform>();
        private UnitGraphTree graphTree;
        private FlowGraph mGraph;
        private string category;
        private Dictionary<string, List<(BaseScriptUnit, UniScriptUnitConfig.ScriptUnitConfigData)>> cacheCategoryUnitDict = new Dictionary<string, List<(BaseScriptUnit, UniScriptUnitConfig.ScriptUnitConfigData)>>();
        protected override bool inDragState => false;
        private const float dockerTreeScale = 1.1f;
        private ISubscription<CloseDockerList> closeDockerListMessageHandle;
        private DragLayoutElement preselectionElement;
        private bool isMoveSecondaryTitle = true;
        private Dictionary<string, string> secondaryTitleToIconName = new Dictionary<string, string>()
        {
            {"Moving", "icon_move"},
            {"Player", "icon_player"},
            {"Looks", "icon_looks"},
            {"Sound", "icon_sound"},
            {"Other", "icon_other"},
            {"Object", "icon_uninode"},
            {"Number", "icon_number"},
            {"Text", "icon_string"},
            {"Boolean", "icon_boolean"},
            {"Variable", "icon_variable"},
            {"Position", "icon_vector3"},
        };

        public override void Update()
        {
            bool layoutDirty = Root.LayoutDirty;
            if (graphTree != null)
            {
                if (beginDrag && DragElement != Root && graphTree.DragMove())
                {
                    IsInDragMove = true;
                    OnDragElement(Input.mousePosition);
                }
                graphTree.CheckRootPositionLimit();
            }
            base.Update();
            if (layoutDirty)
            {
                Vector2 size = Root.nextViewSize;
                size.y *= dockerTreeScale * (95f / 80);
                Root.nextViewSize = size;
                Root.GetViewTransform().sizeDelta = size;
            }
            if (!isClickSecondaryTitle && sidebarWidthList.Count > 0)
            {
                for (int i = 0; i < sidebarToggleList.Count; i++)
                {
                    if (sidebarWidthList[i] == null || Root.GetViewTransform().anchoredPosition.y <= -(sidebarWidthList[i].anchoredPosition.y + 15) * dockerTreeScale)
                    {
                        if (!sidebarToggleList[i].isOn)
                        {
                            isMoveSecondaryTitle = false;
                            sidebarToggleList[i].isOn = true;
                            isMoveSecondaryTitle = true;
                        }
                        break;
                    }
                }
            }
        }

        public void InitTree(UnitGraphTree graphTree)
        {
            Clean();
            rootDragLimit = RootDragLimit.Y;
            this.graphTree = graphTree;
            this.mGraph = new FlowGraph() { units = { new DirectExecuteUnit() } };
            this.mGraph.ScriptMachine = graphTree.CurGraph.ScriptMachine;
            // Root.Spacing = Spacing;
            // if (this.mGraph != null)
            // {
            //     this.mGraph.ScriptMachine.nest.embed = this.mGraph;
            // }
            category = null;
            cacheCategoryUnitDict.Clear();
            InitializeCategory();
            if (!Bg.gameObject.activeInHierarchy)
            {
                RefreshList("For You");
                Hide(false);
            }
            else if (Root.ChildCount == 0)
            {
                RefreshList("For You");
            }
            if (closeDockerListMessageHandle != null)
            {
                closeDockerListMessageHandle.Dispose();
                closeDockerListMessageHandle = null;
            }
            closeDockerListMessageHandle = Messenger.Default.Subscribe<CloseDockerList>(value => Hide(value.IsHide));
        }

        private void InitializeCategory()
        {
            var datas = UniScriptUnitConfig.GetUnitMetaDic().Values;
            foreach (var btn in CategoryButtonDict.Values)
            {
                btn.gameObject.SetActive(false);
            }
            foreach (var d in datas)
            {
                if (!CategoryButtonDict.ContainsKey(d.Category))
                {
                    var btn = Instantiate(CategoryButtonTemplate, DockerList);
                    btn.gameObject.SetActive(true);
                    btn.GetComponentInChildren<Text>().text = d.Category;
                    btn.GetComponentInChildren<Image>().sprite = LoadSprite.GetSprite(LoadSprite.Conversation, $"script_category_{d.Category.ToLower().Replace(" ", "_")}");
                    btn.onClick.AddListener(() =>
                    {
                        RefreshList(d.Category);
                        Hide(false);
                    });
                    CategoryButtonDict.Add(d.Category, btn);
                    btn.gameObject.SetActive(true);
                }
                else
                {
                    if (!CategoryButtonDict[d.Category].gameObject.activeSelf)
                    {
                        CategoryButtonDict[d.Category].gameObject.SetActive(true);
                    }
                }
            }
        }

        public void RefreshList(string category)
        {
            if (this.category == category)
            {
                return;
            }
            UniMain.TrackEvent.UploadStatistics(ConstValue.SHUSHU_EVENT_PV, () => {
                return new Dictionary<string, object>(){
                    {"page_name", "unity_command"},
                    {"tab", category.ToLower().Replace(" ", "_")},
                };
            });
            if (this.category != null && CategoryButtonDict.TryGetValue(this.category, out Button oldBtn))
            {
                oldBtn.GetComponentInChildren<Text>().color = Color.white;
                oldBtn.GetComponentInChildren<Image>().color = Color.white;
            }
            if (category != null && CategoryButtonDict.TryGetValue(category, out oldBtn))
            {
                oldBtn.GetComponentInChildren<Text>().color = new Color(0xE1 / 255f, 0xBA / 255f,0x43 / 255f);
                oldBtn.GetComponentInChildren<Image>().color = new Color(0xE1 / 255f, 0xBA / 255f,0x43 / 255f);
            }
            this.category = category;
            RectTransform thisTran = transform as RectTransform;
            if (category == "For You")
            {
                thisTran.sizeDelta = new Vector2(450, -160);
            }
            else
            {
                thisTran.sizeDelta = new Vector2(930, -160);
            }
            Clean();
            graphTree.CloseAllDropDown();
            var datas = UniScriptUnitConfig.GetUnitMetaDic().Values;
            bool isShowSidebar = category == "For You" || category == "Expression";
            if(isShowSidebar)
            {
                foreach (var tog in sidebarToggleList)
                {
                    tog.onValueChanged.RemoveAllListeners();
                    GameObject.Destroy(tog.gameObject);
                }
                sidebarToggleList.Clear();
                sidebarWidthList.Clear();
            }
            SidebarToggleTemplate.transform.parent.gameObject.SetActive(isShowSidebar);
            if (!cacheCategoryUnitDict.ContainsKey(category))
            {
                cacheCategoryUnitDict.Add(category, new List<(BaseScriptUnit, UniScriptUnitConfig.ScriptUnitConfigData)>());
                int nodeType = 0;
                if (UIConversationGraphData.Instance.ConversationUIParams.ScriptOwnerNode.TryGetComponent<UniObjectEdit>(out var editor))
                {
                    nodeType = (int)editor.CurrentNodeType;
                }
                else
                {
                    nodeType = (int)UniObjectEdit.Get(UIConversationGraphData.Instance.ConversationUIParams.ScriptOwnerNode.gameObject).CurrentNodeType;
                }
                int simpleCommandCount = 0;
                List<(BaseScriptUnit, UniScriptUnitConfig.ScriptUnitConfigData)> list = cacheCategoryUnitDict[category];
                if (simpleCommandCount == 0 && list.Count > 0 && list[^1].Item2 is UniScriptUnitConfig.SecondaryTitleUnitConfigData)
                {
                    list.RemoveAt(list.Count - 1);
                }
                foreach (var d in datas)
                {
                    if (d.Category != category)
                    {
                        continue;
                    }
                    if (d.UnitType == typeof(AdvertisementUnit) && !Global.HasAuthority(Authority.AdvertiseUser))
                    {
                        continue;
                    }
                    if (d.UnitType == typeof(CurrentPlayerUnit) && !UniMain.Game.Scene.IsSupport2DEdit)
                    {
                        continue;
                    }
                    if (d.UnitType == typeof(CurrentCharacterUnit) && !UniMain.Game.Scene.IsCharacterUIEdit)
                    {
                        continue;
                    }
                    if (d.UnitType == typeof(CurrentVehicleUnit) && !UniMain.Game.Scene.IsVehicleUIEdit)
                    {
                        continue;
                    }
                    if (d.UnitType == typeof(CurrentPropUnit) && !UniMain.Game.Scene.IsPropUIEdit)
                    {
                        continue;
                    }
                    if (category == "For You" && d is UniScriptUnitConfig.SimpleCommandUnitConfigData)
                    {
                        if (UniMain.DataModule.GetExcelItem<SimpleCommandData>(d.CommandName, out var data))
                        {
                            if (!data.Isshow)
                            {
                                continue;
                            }
                            int mode = UIConversationGraphData.Instance.PreUgcScript != null ? 3 : 1;
                            if (UIConversationGraphData.Instance.ConversationUIParams.IsTalkConversation)
                            {
                                mode++;
                            }
                            if (Global.Game.Scene.IsSupport2DEdit)
                            {
                                mode += 4;
                            }
                            if (data.Disabledscriptmode.Contains(mode))
                            {
                                continue;
                            }
                            if (!data.Enabledscriptmode.Contains(nodeType))
                            {
                                if (data.Disablednetworkmode.Length == 0)
                                {
                                    continue;
                                }
                                else if(data.Disablednetworkmode.Contains(UniMain.Game.IsSinglePlayerMode() ? 2 : 1))
                                {
                                    continue;
                                }
                            }
                        }
                        simpleCommandCount++;
                    }
                    else
                    {
                        simpleCommandCount = 0;
                    }
                    if (d is UniScriptUnitConfig.TriggerEventUnitConfigData)
                    {
                        if (!UIConversationGraphData.Instance.isShowTriggerEvent || UIConversationGraphData.Instance.PreUgcScript != null)
                        {
                            continue;
                        }
                    }
                    if (simpleCommandCount == 0 && category == "For You" && list.Count > 0 && list[^1].Item2 is UniScriptUnitConfig.SecondaryTitleUnitConfigData)
                    {
                        list.RemoveAt(list.Count - 1);
                    }
                    list.Add((null, d));
                }
                for (int i = 0; i < list.Count; i++)
                {
                    UniScriptUnitConfig.ScriptUnitConfigData d = list[i].Item2;
                    var unit = d.GetUnit(this.mGraph);
                    if (unit == null)
                    {
                        list.RemoveAt(i);
                        i--;
                        continue;
                    }
                    var layout = new UnitLayout(unit, BaseLayout.LayoutDirection.Vertical, null, unit.Exit);
                    unit.layout = layout;
                    layout.UnitConfig = d;
                    (Root as UnitLayoutContainer).SetFlow(graphTree.CurFlow);
                    CreateLayoutElement(Root, layout);
                    list[i] = (unit, d);
                    if (isShowSidebar && d is UniScriptUnitConfig.SecondaryTitleUnitConfigData secondaryTitleUnitConfigData)
                    {
                        Toggle temp = GameObject.Instantiate(SidebarToggleTemplate, SidebarToggleTemplate.transform.parent);
                        temp.gameObject.SetActive(true);
                        Image img = temp.transform.Find("Label").GetComponent<Image>();
                        img.sprite = LoadSprite.GetSprite(LoadSprite.TypeIcon, secondaryTitleToIconName[secondaryTitleUnitConfigData.Title]);
                        sidebarToggleList.Add(temp);
                        if (i != 0)
                        {
                            sidebarWidthList.Add(unit.layout.GetLayoutGameObject().transform as RectTransform);
                        }
                        Text txt = temp.GetComponentInChildren<Text>();
                        txt.text = secondaryTitleUnitConfigData.Title;
                        temp.onValueChanged.RemoveAllListeners();
                        temp.onValueChanged.AddListener(isOn =>
                        {
                            if (isOn)
                            {
                                img.color = new Color(0xE1 / 255f, 0xBA / 255f,0x43 / 255f);
                                txt.color = new Color(0xE1 / 255f, 0xBA / 255f,0x43 / 255f);
                                MoveToSecondaryTitleUnit(layout);
                            }
                            else
                            {
                                img.color = Color.white;
                                txt.color = Color.white;
                            }
                        });
                    }
                }
                sidebarWidthList.Add(null);
            }
            else
            {
                List<(BaseScriptUnit, UniScriptUnitConfig.ScriptUnitConfigData)> valueTuples = cacheCategoryUnitDict[category];
                for (int i = 0; i < valueTuples.Count; i++)
                {
                    var unitAndData = valueTuples[i];
                    var layout = new UnitLayout(unitAndData.Item1, BaseLayout.LayoutDirection.Vertical, null, unitAndData.Item1.Exit);
                    unitAndData.Item1.layout = layout;
                    layout.UnitConfig = unitAndData.Item2;
                    CreateLayoutElement(Root, layout);
                    if (isShowSidebar && unitAndData.Item2 is UniScriptUnitConfig.SecondaryTitleUnitConfigData secondaryTitleUnitConfigData)
                    {
                        Toggle temp = GameObject.Instantiate(SidebarToggleTemplate, SidebarToggleTemplate.transform.parent);
                        temp.gameObject.SetActive(true);
                        Image img = temp.transform.Find("Label").GetComponent<Image>();
                        img.sprite = LoadSprite.GetSprite(LoadSprite.TypeIcon, secondaryTitleToIconName[secondaryTitleUnitConfigData.Title]);
                        sidebarToggleList.Add(temp);
                        if (i != 0)
                        {
                            sidebarWidthList.Add(layout.GetLayoutGameObject().transform as RectTransform);
                        }
                        Text txt = temp.GetComponentInChildren<Text>();
                        txt.text = secondaryTitleUnitConfigData.Title;
                        temp.onValueChanged.RemoveAllListeners();
                        temp.onValueChanged.AddListener(isOn =>
                        {
                            if (isOn)
                            {
                                img.color = new Color(0xE1 / 255f, 0xBA / 255f,0x43 / 255f);
                                txt.color = new Color(0xE1 / 255f, 0xBA / 255f,0x43 / 255f);
                                MoveToSecondaryTitleUnit(layout);
                            }
                            else
                            {
                                img.color = Color.white;
                                txt.color = Color.white;
                            }
                        });
                    }
                }
                sidebarWidthList.Add(null);
            }
            if (sidebarToggleList.Count > 0)
            {
                sidebarToggleList[0].isOn = true;
            }
            Root.GetViewTransform().localScale = Vector3.one * dockerTreeScale;
            DragElementDisplayPosition = Vector2.zero;
            DisplayPosition = DragElementDisplayPosition;
            Root.GetViewTransform().anchoredPosition = DragElementDisplayPosition;
        }

        private void MoveToSecondaryTitleUnit(UnitLayout layout)
        {
            if (!isMoveSecondaryTitle)
            {
                return;
            }
            isClickSecondaryTitle = true;
            if (layout == null)
            {
                return;
            }
            GameObject layoutGameObject = layout.GetLayoutGameObject();
            if (layoutGameObject != null && layoutGameObject.transform is RectTransform rt)
            {
                DragElementDisplayPosition = new Vector2(0, -(rt.anchoredPosition.y + 15) * dockerTreeScale);
                RectTransform viewTransform = Root.GetViewTransform();
                var viewSize = (viewTransform.parent as RectTransform).rect.size;
                var maxSize = viewTransform.rect.size;
                var maxOffset = maxSize.y - viewSize.y;
                DragElementDisplayPosition.y = Mathf.Min(DragElementDisplayPosition.y, maxOffset);
                DisplayPosition = DragElementDisplayPosition;
                viewTransform.anchoredPosition = DragElementDisplayPosition;
            }
        }

        public void Hide(bool isHide = false)
        {
            Bg?.SetActive(!isHide);
            Mask?.SetActive(!isHide);
            if (isHide)
            {
                foreach (Button btn in CategoryButtonDict.Values)
                {
                    btn.GetComponentInChildren<Text>().color = Color.white;
                    btn.GetComponentInChildren<Image>().color = Color.white;
                }
                SidebarToggleTemplate.transform.parent.gameObject.SetActive(false);
            }
            else
            {
                SidebarToggleTemplate.transform.parent.gameObject.SetActive(category == "For You" || category == "Expression");
            }
        }

        public override void OnBeginDragElement(Vector2 screenPosition, DragLayoutElement ele)
        {
            SidebarGameObject.SetActive(false);
            DockerList.gameObject.SetActive(false);
            if (ele is UnitLayoutContainer unitLayoutContainer)
            {
                var unit = unitLayoutContainer.Layout.Unit;
                if (unit != null)
                {
                    var def = new UnitLayout(unit);
                    def.UnitConfig = unitLayoutContainer.Layout.UnitConfig;
                    DragElement = graphTree.CreateLayoutElement(null, def);
                    def.OnShow();
                    var t = DragElement.GetViewTransform();
                    var et = ele.GetViewTransform();
                    t.SetParent(graphTree.FreeMoveLayer);
                    t.localScale = Vector3.one;
                    t.position = et.position;
                    Camera camera = UniGameCameras.GetInstance().GetUICamera();
                    RectTransformUtility.ScreenPointToLocalPointInRectangle(et, screenPosition, camera, out var dragLocalPosition);
                    dragLocalPosition += t.anchoredPosition;
                    RectTransformUtility.ScreenPointToLocalPointInRectangle(graphTree.FreeMoveLayer, screenPosition, camera, out var viewLocal);
                    t.anchoredPosition += (viewLocal - dragLocalPosition);
                    DragElement.MarkLayoutDirty();
                    if (PreIndicator == null)
                    {
                        PreIndicator = Instantiate(Global.AssetModule.SyncLoad<GameObject>("prefabs/ui/unitview/preindicator.unity3d")).GetComponent<RectTransform>();
                    }
                    PreIndicator.SetParent(DragElement.GetViewTransform());
                    PreIndicator.localPosition = Vector3.zero;
                    PreIndicator.anchoredPosition = new Vector3(3, -3);
                    PreIndicator.localEulerAngles = Vector3.zero;
                    PreIndicator.localScale = Vector3.one;
                    Hide(true);
                }
            }
        }

        public override void OnEndDragElement(Vector2 screenPosition, bool isReverse = false)
        {
            SidebarGameObject.SetActive(true);
            DockerList.gameObject.SetActive(true);
            if (graphTree != null)
            {
                UnitLayoutContainer dragContainer = DragElement as UnitLayoutContainer;
                if (graphTree.AcceptDrop(dragContainer, screenPosition, true))
                {
                    graphTree.OnAddHistoryEvent?.Invoke();
                }
                // else
                // {
                //  DeleteElement(graphTree.CurFlow, DragElement);
                // }
            }
            base.OnEndDragElement(screenPosition, isReverse);
            Hide(false);
        }

        public override void OnPointerClick(PointerEventData eventData)
        {
            // base.OnPointerClick(eventData);
            DragLayoutElement oldElement = CurrentSelectedElement;
            var ele = Root.GetElement(eventData.position, CheckElementIsTitle);
            Transform rect = eventData.pointerCurrentRaycast.gameObject.transform;
            bool isOnElement = false;
            if (ele != null)
            {
                do
                {
                    if (rect == ele.GetViewTransform())
                    {
                        isOnElement = true;
                        break;
                    }
                    rect = rect.parent;
                } while (rect != null);
            }
            if (isOnElement && ele != Root)
            {
                CurrentSelectedElement = ele;
                while (CurrentSelectedElement.Parent != null && CurrentSelectedElement.Parent != Root)
                {
                    CurrentSelectedElement = CurrentSelectedElement.Parent;
                }

                OnSelectedElementChange(oldElement, CurrentSelectedElement);
            }
            else
            {
                if (CurrentSelectedElement != null)
                {
                    CurrentSelectedElement = null;
                    OnSelectedElementChange(oldElement, CurrentSelectedElement);
                }
            }
            if (graphTree != null && CurrentSelectedElement != null && preselectionElement == CurrentSelectedElement)
            {
                preselectionElement = null;
                graphTree.AcceptDropAtLast(CurrentSelectedElement as UnitLayoutContainer, true);
                OnSelectedElementEvent?.Invoke(CurrentSelectedElement, null);
            }
            else
            {
                preselectionElement = null;
            }
        }

        protected override bool CheckCanDrag(DragLayoutElement ele)
        {
            return (ele.Parent == Root || ele == Root) && CheckElementIsTitle(ele);
        }

        public override void OnBeginDrag(PointerEventData eventData)
        {
            isClickSecondaryTitle = false;
            base.OnBeginDrag(eventData);
        }

        private bool CheckElementIsTitle(DragLayoutElement x)
        {
            if (x is UnitLayoutContainer unitLayoutContainer && unitLayoutContainer.Layout.Unit is SecondaryTitleUnit)
            {
                return false;
            }
            return true;
        }

        public override void OnPointerDown(PointerEventData eventData)
        {
            base.OnPointerDown(eventData);
            var ele = Root.GetElement(eventData.position, null);
            if (ele != null && ele != Root)
            {
                preselectionElement = ele;
                while (preselectionElement.Parent != null && preselectionElement.Parent != Root)
                {
                    preselectionElement = preselectionElement.Parent;
                }
            }
        }

        public void HideTree()
        {
            closeDockerListMessageHandle?.Dispose();
            Hide(true);
        }
    }

    public struct CloseDockerList
    {
        public bool IsHide;
    }
```


类继承自 `UnitDragTree`，用于在 Unity 中管理和操作脚本单元的拖放树结构。该类包含多个字段和方法，用于处理脚本单元的初始化、拖放、布局更新等功能。

首先，类中定义了几个字段，包括 `DockerList`、`CategoryButtonTemplate`、`CategoryButtonDict`、`Bg`、`Mask`、`SidebarGameObject`、`SidebarToggleTemplate`、`isClickSecondaryTitle`、`sidebarToggleList`、`sidebarWidthList`、`graphTree`、`mGraph`、`category`、`cacheCategoryUnitDict`、`closeDockerListMessageHandle`、`preselectionElement`、`isMoveSecondaryTitle` 和 `secondaryTitleToIconName`。这些字段用于存储脚本单元的 UI 元素、状态、事件订阅和缓存数据等信息。

`Update` 方法重写了基类的 `Update` 方法，用于更新脚本单元的拖放树结构。方法首先检查根节点的布局是否脏，如果是，则更新根节点的大小。接着，如果 `graphTree` 不为空且正在拖动元素，则调用 `DragMove` 方法更新拖动位置，并检查根节点的位置限制。最后，方法遍历侧边栏的切换列表，根据当前滚动位置更新切换状态。

`InitTree` 方法用于初始化脚本单元的拖放树结构，接受一个 `UnitGraphTree` 类型的参数 `graphTree`。方法首先清理当前的树结构，然后设置新的图形和流程，并根据传入的图形和流程初始化根节点的布局和位置。方法还订阅了关闭拖放列表的消息事件。

`InitializeCategory` 方法用于初始化类别按钮。方法遍历脚本单元配置数据，根据类别创建或更新按钮，并设置按钮的点击事件，用于刷新列表和隐藏拖放列表。

`RefreshList` 方法用于刷新脚本单元列表，接受一个字符串类型的参数 `category`。方法首先检查当前类别是否与传入类别相同，如果相同则返回。接着，方法更新当前类别的按钮颜色，并根据类别调整拖放列表的大小。然后，方法清理当前列表，关闭所有下拉菜单，并根据类别和配置数据创建新的脚本单元布局元素。

`MoveToSecondaryTitleUnit` 方法用于移动到次级标题单元，接受一个 `UnitLayout` 类型的参数 `layout`。方法首先检查是否允许移动次级标题，如果允许则更新拖动位置，并根据次级标题单元的位置调整根节点的位置。

`Hide` 方法用于显示或隐藏拖放列表，接受一个布尔类型的参数 `isHide`。方法根据参数设置背景和遮罩的显示状态，并更新侧边栏的显示状态。

`OnBeginDragElement` 方法重写了基类的 `OnBeginDragElement` 方法，用于处理拖动元素的开始事件。方法首先隐藏侧边栏和拖放列表，然后根据拖动元素的类型和状态，创建新的拖动元素，并设置其位置和缩放。

`OnEndDragElement` 方法重写了基类的 `OnEndDragElement` 方法，用于处理拖动元素的结束事件。方法首先显示侧边栏和拖放列表，然后检查拖动元素是否被接受，如果被接受则触发添加历史事件。

`OnPointerClick` 方法重写了基类的 `OnPointerClick` 方法，用于处理点击事件。方法首先获取点击位置的拖放元素，并检查是否在元素上点击。如果在元素上点击，则更新当前选中的元素，并触发选中元素变化事件。

`CheckCanDrag` 方法重写了基类的 `CheckCanDrag` 方法，用于检查是否可以拖动元素。方法检查拖动元素是否为根节点或根节点的子元素，并检查元素是否为标题单元。

`OnBeginDrag` 方法重写了基类的 `OnBeginDrag` 方法，用于处理拖动开始事件，并重置次级标题点击状态。

`CheckElementIsTitle` 方法用于检查元素是否为标题单元，接受一个 `DragLayoutElement` 类型的参数 `x`。方法检查元素是否为 `UnitLayoutContainer` 类型，并检查其关联的单元是否为次级标题单元。

`OnPointerDown` 方法重写了基类的 `OnPointerDown` 方法，用于处理指针按下事件。方法获取按下位置的拖放元素，并设置预选中的元素。

`HideTree` 方法用于隐藏拖放树，并取消订阅关闭拖放列表的消息事件。

总体来说，这段代码实现了一个功能丰富的拖放树结构类，提供了脚本单元的拖放、布局、显示和隐藏等功能。通过这些方法，可以方便地在 Unity 中管理和操作复杂的脚本单元拖放树结构，提高开发效率。