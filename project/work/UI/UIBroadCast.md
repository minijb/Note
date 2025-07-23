
```c#
    public class UIBroadcast : UIBase<UIBroadcastRef, UIBroadcastModel>
    {
        public static Action<string> OnCreateBroadcast;

        public Action<string> OnSelelctBroadcast;
        public List<UIBroadcastNameItem> broadcastNameList = new List<UIBroadcastNameItem>();
        public List<UIBroadcastParameterItem> broadcastParameterList = new List<UIBroadcastParameterItem>();
        public List<UIBroadcastParameterTypeItem> broadcastParameterTypeList = new List<UIBroadcastParameterTypeItem>();

        private UIBroadcastNameItem uiBroadcastNameItemTemplate;
        private UIBroadcastParameterItem uiBroadcastParameterItemTemplate;
        private UIBroadcastParameterTypeItem uiBroadcastParameterTypeItemTemplate;

        private UIBroadcastNameItem uiBroadcastNameItemSelected;
        private string broadcastParameterNameItemSelected;
        private string broadcastName;
        private List<string> broadcastInfoName = new List<string>();
        private List<Type> broadcastInfoTypes = new List<Type>();
        private List<AssetType> broadcastInfoAssetTypes = new List<AssetType>();
        private Type parameterType = typeof(float);
        private AssetType parameterAssetType = AssetType.None;
        private Type elementType = typeof(float);
        private AssetType elementAssetType = AssetType.None;
        private bool isSelectElementType = false;

        private static List<(Type type, AssetType assetType, string typeName, string defaultName, string iconName)> parameterTypeList = new List<(Type, AssetType, string, string, string)>()
        {
            (typeof(float), AssetType.None, "uniscripts_Numbers", "uniscripts_Number", "icon_number"),
            (typeof(string), AssetType.None, "uniscripts_Text", "uniscripts_Text", "icon_string"),
            (typeof(bool), AssetType.None, "uniscripts_True/False", "uniscripts_Boolean", "icon_boolean"),
            (typeof(Vector3), AssetType.None, "uniscripts_Vector", "uniscripts_Vector", "icon_vector3"),
            (typeof(Vector2), AssetType.None, "uniscripts_Vector2", "uniscripts_Vector2", "icon_vector2"),
            (typeof(Color), AssetType.Color, "chooseType_ColorType", "chooseType_ColorType", "icon_color"),
            (typeof(string), AssetType.Material, "chooseType_TextureType", "chooseType_TextureType", "icon_material"),
            (typeof(UniNode), AssetType.None, "chooseType_UniNodeType", "chooseType_UniNodeType", "icon_uninode"),
            (typeof(UniPlayer), AssetType.None, "chooseType_PlayerType", "chooseType_PlayerType", "icon_player"),
            (typeof(UniAudioAsset), AssetType.BGM, "chooseType_AudioType", "chooseType_AudioType", "icon_audio"),
            (typeof(PropSpawnerData), AssetType.Clothing, "chooseType_ClothingType", "chooseType_ClothingType", "icon_clothing"),
            (typeof(PropSpawnerData), AssetType.Prop, "chooseType_PropType", "chooseType_PropType", "icon_prop"),
            (typeof(PropSpawnerData), AssetType.Vehicle, "chooseType_VehicleType", "chooseType_VehicleType", "icon_vehicle"),
            (typeof(CharacterAnimationData), AssetType.Animation, "chooseType_ActiveType", "chooseType_ActiveType", "icon_active"),
            (typeof(Array), AssetType.None, "chooseType_Array", "chooseType_Array", "icon_array"),
        };

        public override FormShowType ShowType { get => FormShowType.Third; set { } }

        public override void OnInit()
        {
            uiBroadcastNameItemTemplate = this.UIRef.rectran_BroadcastItem.gameObject.AddComponent<UIBroadcastNameItem>();
            uiBroadcastNameItemTemplate.onSelect = this.UIRef.rectran_BroadcastItem.GetChild(0).GetComponent<Button>();
            uiBroadcastNameItemTemplate.bg = uiBroadcastNameItemTemplate.onSelect.GetComponent<Image>();
            uiBroadcastNameItemTemplate.broadcastName = uiBroadcastNameItemTemplate.onSelect.transform.GetChild(0).GetComponent<Text>();
            uiBroadcastNameItemTemplate.delete = this.UIRef.rectran_BroadcastItem.GetChild(1).GetComponent<Button>();

            uiBroadcastParameterItemTemplate = this.UIRef.rectran_BroadcastParameterItem.gameObject.AddComponent<UIBroadcastParameterItem>();
            uiBroadcastParameterItemTemplate.edit = this.UIRef.rectran_BroadcastParameterItem.GetChild(0).GetComponent<Button>();
            uiBroadcastParameterItemTemplate.icon = uiBroadcastParameterItemTemplate.edit.transform.GetChild(0).GetComponent<Image>();
            uiBroadcastParameterItemTemplate.parameterName = this.UIRef.rectran_BroadcastParameterItem.GetChild(1).GetChild(0).GetComponent<InputField>();
            uiBroadcastParameterItemTemplate.parameterName.characterLimit = 16;
            uiBroadcastParameterItemTemplate.delete = this.UIRef.rectran_BroadcastParameterItem.GetChild(2).GetComponent<Button>();

            uiBroadcastParameterTypeItemTemplate = this.UIRef.btn_TypeItem.gameObject.AddComponent<UIBroadcastParameterTypeItem>();
            uiBroadcastParameterTypeItemTemplate.onSelect = this.UIRef.btn_TypeItem;
            uiBroadcastParameterTypeItemTemplate.bg = this.UIRef.btn_TypeItem.GetComponent<Image>();
            uiBroadcastParameterTypeItemTemplate.icon = uiBroadcastParameterTypeItemTemplate.transform.GetChild(0).GetComponent<Image>();
            uiBroadcastParameterTypeItemTemplate.typeName = uiBroadcastParameterTypeItemTemplate.transform.GetChild(1).GetComponent<Text>();
            uiBroadcastParameterTypeItemTemplate.Press = uiBroadcastParameterTypeItemTemplate.transform.GetChild(2).gameObject;

#region 多语言设置
            this.UIRef.txt_BroadcastNameListName.text = "uniscripts_Select_Broadcast".GetLanguageStr();
            this.UIRef.txt_BroadcastNameConfirm.text = "uniscripts_Confirm".GetLanguageStr();
            this.UIRef.txt_AddBroadcastPanelName.text = "uniscripts_Select_Broadcast".GetLanguageStr();
            this.UIRef.txt_NameLable.text = "uniscripts_Name:".GetLanguageStr();
            this.UIRef.txt_AddParameterList.text = "uniscripts_Parameter_List:".GetLanguageStr();
            this.UIRef.txt_AddBroadcastConfirm.text = "uniscripts_Confirm".GetLanguageStr();
            this.UIRef.txt_ChooseVariableTybe.text = "uniscripts_Choose_Variable_Type".GetLanguageStr();
            UIRef.txt_CreateElementTypeTitle.text = "Script_array_choose_toast".GetLanguageStr();
            this.UIRef.txt_CreateElementTypeConfirm.text = "uniscripts_Confirm".GetLanguageStr();
#endregion

            Button closeButton = this.UIRef.GetComponent<Button>();
            closeButton.onClick.RemoveAllListeners();
            closeButton.onClick.AddListener(() =>
            {
                OnSelelctBroadcast?.Invoke(null);
                UISystem.Inst.UntilBackToSecondActiveUI();
            });
            this.UIRef.btn_AddBroadcast.onClick.AddListener(() =>
            {
                OnSelectBroadcastNameItem(null);
                OpenAddBroadcastPanel(null);
            });
            broadcastNameList.Clear();
            List<BroadcastInfo> envComponentAllBroadcastName = Global.Game.Scene.EnvComponent.AllBroadcast;
            if (envComponentAllBroadcastName.Count > 0)
            {
                this.UIRef.scr_BroadcastNameList.gameObject.SetActive(true);
                for (int i = 0; i < envComponentAllBroadcastName.Count; i++)
                {
                    CreateBroadcastNameItem(envComponentAllBroadcastName[i].name);
                }
            }
            else
            {
                this.UIRef.scr_BroadcastNameList.gameObject.SetActive(false);
            }
            OnCreateBroadcast = CreateBroadcastNameItem;
            this.UIRef.btn_BroadcastNameConfirm.onClick.AddListener(() =>
            {
                if (uiBroadcastNameItemSelected)
                {
                    OnSelelctBroadcast?.Invoke(uiBroadcastNameItemSelected.broadcastName.text);
                }
                else
                {
                    OnSelelctBroadcast?.Invoke(null);
                }
                UISystem.Inst.UntilBackToSecondActiveUI();
            });
            this.UIRef.btn_BroadcastNameEdit.onClick.AddListener(() =>
            {
                if (uiBroadcastNameItemSelected)
                {
                    OpenAddBroadcastPanel(uiBroadcastNameItemSelected.broadcastName.text);
                }
            });
            this.UIRef.btn_AddParameterList.onClick.AddListener(() =>
            {
                broadcastParameterNameItemSelected = null;
                OpenChooseVariableType(null, AssetType.None);
            });
            this.UIRef.btn_AddBroadcastConfirm.onClick.AddListener(() =>
            {
                string newName = this.UIRef.inputfield_BroadcastName.text;
                if (uiBroadcastNameItemSelected == null)
                {
                    if (!string.IsNullOrWhiteSpace(this.UIRef.inputfield_BroadcastName.text) && Global.Game.Scene.EnvComponent.AllBroadcast.FindIndex(x => x.name == newName) == -1)
                    {
                        CreateBroadcastNameItem(newName);
                        Global.Game.Scene.EnvComponent.AllBroadcast.Add(new BroadcastInfo()
                        {
                            name = newName,
                            parameterName = broadcastInfoName,
                            parameterTypes = broadcastInfoTypes,
                            parameterAssetTypes = broadcastInfoAssetTypes
                        });
                        broadcastInfoName = new List<string>();
                        broadcastInfoTypes = new List<Type>();
                        broadcastInfoAssetTypes = new List<AssetType>();
                        OpenBroadcastNameListPanel();
                    }
                    else
                    {
                        //弹窗
                        UIHelper.Instance.ShowToast("uniscripts_broadcast_toast".GetLanguageStr());
                    }
                }
                else
                {
                    if (uiBroadcastNameItemSelected.broadcastName.text != newName)
                    {
                        if (Global.Game.Scene.EnvComponent.AllBroadcast.FindIndex(x => x.name == newName) == -1)
                        {
                            int index = Global.Game.Scene.EnvComponent.AllBroadcast.FindIndex(x => x.name == uiBroadcastNameItemSelected.broadcastName.text);
                            broadcastNameList[index].broadcastName.text = newName;
                            BroadcastInfo broadcastInfo = Global.Game.Scene.EnvComponent.AllBroadcast[index];
                            broadcastInfo.name = newName;
                            OpenBroadcastNameListPanel();
                        }
                        else
                        {
                            //弹窗
                            UIHelper.Instance.ShowToast("uniscripts_broadcast_toast".GetLanguageStr());
                        }
                    }
                    else
                    {
                        OpenBroadcastNameListPanel();
                    }
                }
            });
            this.UIRef.inputfield_BroadcastName.onEndEdit.RemoveAllListeners();
            this.UIRef.inputfield_BroadcastName.characterLimit = 16;
            this.UIRef.inputfield_BroadcastName.onEndEdit.AddListener(str => broadcastName = str);
            broadcastParameterTypeList.Clear();
            for (int i = 0; i < parameterTypeList.Count; i++)
            {
                Type type = parameterTypeList[i].type;
                AssetType assetType = parameterTypeList[i].assetType;
                string parameterName = parameterTypeList[i].defaultName;
                broadcastParameterTypeList.Add(Object.Instantiate(uiBroadcastParameterTypeItemTemplate, this.UIRef.rectran_ParameterType));
                broadcastParameterTypeList[i].gameObject.SetActive(true);
                broadcastParameterTypeList[i].icon.sprite = LoadSprite.GetSprite(LoadSprite.TypeIcon, parameterTypeList[i].iconName);
                broadcastParameterTypeList[i].typeName.text = parameterTypeList[i].typeName.GetLanguageStr();
                if (typeof(Array).IsAssignableFrom(type))
                {
                    broadcastParameterTypeList[i].onSelect.onClick.AddListener(() =>
                    {
                        OpenCreateElementType(typeof(float), AssetType.None);
                    });
                }
                else
                {
                    broadcastParameterTypeList[i].onSelect.onClick.AddListener(() =>
                    {
                        if (isSelectElementType)
                        {
                            OpenCreateElementType(type, assetType);
                        }
                        else
                        {
                            CreateParamType(parameterName, type, assetType);
                        }
                    });
                }
            }
            UIRef.btn_CloseCreateElementType.onClick.AddListener(() =>
            {
                isSelectElementType = false;
                OpenChooseVariableType(parameterType, parameterAssetType);
            });
            UIRef.btn_CreateElementType.onClick.AddListener(() =>
            {
                OpenChooseVariableType(elementType, elementAssetType);
            });
            UIRef.btn_CreateElementTypeConfirm.onClick.AddListener(() =>
            {
                isSelectElementType = false;
                CreateParamType("chooseType_Array".GetLanguageStr(), elementType.MakeArrayType(), elementAssetType);
            });
        }

        private void CreateParamType(string parameterName, Type type, AssetType assetType)
        {
            if (string.IsNullOrEmpty(broadcastParameterNameItemSelected))
            {
                var parameName = broadcastInfoName;
                BroadcastInfo info = null;
                if (uiBroadcastNameItemSelected != null)
                {
                    info = Global.Game.Scene.EnvComponent.AllBroadcast.Find(x => x.name == uiBroadcastNameItemSelected.broadcastName.text);
                }
                if (info != null)
                {
                    parameName = info.parameterName;
                }
                broadcastParameterNameItemSelected = ReName(parameterName.GetLanguageStr(), str => parameName.Contains(str));
                CreatBroadcastParameterTypeItem(type, assetType);
            }
            else
            {
                var parameName = broadcastInfoName;
                var parameTypes = broadcastInfoTypes;
                var parameAssetTypes = broadcastInfoAssetTypes;
                BroadcastInfo info = null;
                if (uiBroadcastNameItemSelected != null)
                {
                    info = Global.Game.Scene.EnvComponent.AllBroadcast.Find(x => x.name == uiBroadcastNameItemSelected.broadcastName.text);
                }
                if (info != null)
                {
                    parameName = info.parameterName;
                    parameTypes = info.parameterTypes;
                    parameAssetTypes = info.parameterAssetTypes;
                }
                int index = parameName.IndexOf(broadcastParameterNameItemSelected);
                if (index != -1)
                {
                    parameTypes[index] = type;
                    parameAssetTypes[index] = assetType;
                }
            }
            if (uiBroadcastNameItemSelected != null)
            {
                OpenAddBroadcastPanel(uiBroadcastNameItemSelected.broadcastName.text);
            }
            else
            {
                OpenAddBroadcastPanel(broadcastName);
            }
        }

        public override void OnOpen(params object[] args)
        {
            if (args.Length > 0)
            {
                OnSelelctBroadcast = args[0] as Action<string>;
            }
            OpenBroadcastNameListPanel();
        }

        public override void OnClose()
        {
        }

        private void OpenBroadcastNameListPanel()
        {
            this.UIRef.rectran_BroadcastNameListPanel.gameObject.SetActive(true);
            this.UIRef.rectran_AddBroadcastPanel.gameObject.SetActive(false);
            this.UIRef.rectran_ChooseVariableTybe.gameObject.SetActive(false);
            this.UIRef.rectran_CreateElementType.gameObject.SetActive(false);
            OnSelectBroadcastNameItem(null);
            // await UniTask.Delay(5000);
            RefreshBroadcastNameList();
        }

        private void OpenAddBroadcastPanel(string broadcastNameText)
        {
            this.UIRef.rectran_BroadcastNameListPanel.gameObject.SetActive(false);
            this.UIRef.rectran_AddBroadcastPanel.gameObject.SetActive(true);
            this.UIRef.rectran_ChooseVariableTybe.gameObject.SetActive(false);
            this.UIRef.rectran_CreateElementType.gameObject.SetActive(false);
            this.UIRef.size_BroadcastParameterView.enabled = true;
            this.UIRef.size_BroadcastParameterView.GetComponent<VerticalLayoutGroup>().enabled = true;
            this.UIRef.scr_BroadcastParameterList.GetComponent<ContentSizeFitter>().enabled = true;
            this.UIRef.scr_BroadcastParameterList.GetComponent<VerticalLayoutGroup>().enabled = true;
            this.UIRef.scr_BroadcastParameterList.enabled = false;
            if (string.IsNullOrEmpty(broadcastNameText))
            {
                broadcastNameText = ReName("uniscripts_broadcast".GetLanguageStr(), str => Global.Game.Scene.EnvComponent.AllBroadcast.Find(x => x.name == str) != null);
            }
            this.UIRef.inputfield_BroadcastName.text = broadcastNameText;
            broadcastName = broadcastNameText;
            var parameName = broadcastInfoName;
            var parameTypes = broadcastInfoTypes;
            var parameAssetTypes = broadcastInfoAssetTypes;
            var info = Global.Game.Scene.EnvComponent.AllBroadcast.Find(x => x.name == broadcastNameText);
            if (info != null)
            {
                parameName = info.parameterName;
                parameTypes = info.parameterTypes;
                parameAssetTypes = info.parameterAssetTypes;
            }
            for (int i = broadcastParameterList.Count - 1; i >= 0; i--)
            {
                broadcastParameterList[i].transform.SetParent(null);
                Object.Destroy(broadcastParameterList[i].gameObject);
            }
            broadcastParameterList.Clear();
            for (int i = 0; i < parameName.Count; i++)
            {
                Type parameType = parameTypes[i];
                AssetType parameAssetType = parameAssetTypes[i];
                parameType = typeof(Array).IsAssignableFrom(parameType) ? typeof(Array): parameType;
                parameAssetType = typeof(Array).IsAssignableFrom(parameType) ? AssetType.None : parameAssetType;
                CreateParameterItem(parameName[i], parameTypes[i], parameAssetTypes[i], parameterTypeList.Find(info=> info.type == parameType && info.assetType == parameAssetType).iconName);
            }
            if (broadcastParameterList.Count == 0)
            {
                this.UIRef.size_BroadcastContent.gameObject.SetActive(true);
            }
            // await UniTask.Delay(5000);
            RefreshBroadcastParameterList();
        }

        private void OpenChooseVariableType(Type type, AssetType assetType)
        {
            if (isSelectElementType)
            {
                elementType = type;
                elementAssetType = assetType;
            }
            else
            {
                parameterType = type;
                parameterAssetType = assetType;
            }
            this.UIRef.rectran_BroadcastNameListPanel.gameObject.SetActive(false);
            this.UIRef.rectran_AddBroadcastPanel.gameObject.SetActive(false);
            this.UIRef.rectran_ChooseVariableTybe.gameObject.SetActive(true);
            this.UIRef.rectran_ChooseVariableTybe.transform.SetSiblingIndex(isSelectElementType ? 3 : 2);
            this.UIRef.rectran_CreateElementType.gameObject.SetActive(false);
            for (int i = 0; i < parameterTypeList.Count; i++)
            {
                uiBroadcastParameterTypeItemTemplate.Press.SetActive(false);
                if (typeof(Array).IsAssignableFrom(parameterTypeList[i].Item1))
                {
                    if (isSelectElementType)
                    {
                        broadcastParameterTypeList[i].gameObject.SetActive(false);
                    }
                    else
                    {
                        broadcastParameterTypeList[i].gameObject.SetActive(true);
                        bool isSelected = typeof(Array).IsAssignableFrom(type);
                        broadcastParameterTypeList[i].Press.SetActive(isSelected);
                        //broadcastParameterTypeList[i].bg.sprite = LoadSprite.GetSprite(LoadSprite.Conversation, isSelected ? "bg_basicdirectives_4" : "bg_common");
                    }
                }
                else
                {
                    bool isSelected = parameterTypeList[i].Item1 == type && parameterTypeList[i].Item2 == assetType;
                    broadcastParameterTypeList[i].Press.SetActive(isSelected);
                    //broadcastParameterTypeList[i].bg.sprite = LoadSprite.GetSprite(LoadSprite.Conversation, isSelected ? "bg_basicdirectives_4" : "bg_common");
                }
            }
            LayoutRebuilder.ForceRebuildLayoutImmediate(this.UIRef.rectran_ChooseVariableTybe);
        }

        private void CreateBroadcastNameItem(string name)
        {
            UIBroadcastNameItem broadcastNameItem = Object.Instantiate(uiBroadcastNameItemTemplate, UIRef.rectran_BroadcastItem.parent);
            broadcastNameItem.gameObject.SetActive(true);
            broadcastNameList.Add(broadcastNameItem);
            if (broadcastNameList.Count == 1)
            {
                this.UIRef.scr_BroadcastNameList.gameObject.SetActive(true);
            }
            else if (broadcastNameList.Count == 5)
            {
                this.UIRef.size_BroadcastNameView.enabled = false;
                this.UIRef.size_BroadcastNameView.GetComponent<VerticalLayoutGroup>().enabled = false;
                this.UIRef.scr_BroadcastNameList.GetComponent<ContentSizeFitter>().enabled = false;
                this.UIRef.scr_BroadcastNameList.GetComponent<VerticalLayoutGroup>().enabled = false;
                this.UIRef.scr_BroadcastNameList.enabled = true;
            }
            broadcastNameItem.broadcastName.text = name;
            broadcastNameItem.onSelect.onClick.RemoveAllListeners();
            broadcastNameItem.onSelect.onClick.AddListener(() =>
            {
                OnSelectBroadcastNameItem(broadcastNameItem);
            });
            broadcastNameItem.delete.onClick.RemoveAllListeners();
            broadcastNameItem.delete.onClick.AddListener(() =>
            {
                if (uiBroadcastNameItemSelected == broadcastNameItem)
                {
                    OnSelectBroadcastNameItem(null);
                }
                if (broadcastNameList.Count == 1)
                {
                    this.UIRef.scr_BroadcastNameList.gameObject.SetActive(false);
                }
                else if (broadcastNameList.Count == 5)
                {
                    //TODO 打开size的layout
                    this.UIRef.size_BroadcastNameView.enabled = true;
                    this.UIRef.size_BroadcastNameView.GetComponent<VerticalLayoutGroup>().enabled = true;
                    this.UIRef.scr_BroadcastNameList.GetComponent<ContentSizeFitter>().enabled = true;
                    this.UIRef.scr_BroadcastNameList.GetComponent<VerticalLayoutGroup>().enabled = true;
                    this.UIRef.scr_BroadcastNameList.enabled = false;
                }
                broadcastNameList.Remove(broadcastNameItem);
                Global.Game.Scene.EnvComponent.AllBroadcast.RemoveAll(x => x.name == name);
                broadcastNameItem.transform.SetParent(null);
                Object.Destroy(broadcastNameItem.gameObject);
                RefreshBroadcastNameList();
            });
        }

        private void OnSelectBroadcastNameItem(UIBroadcastNameItem broadcastNameItem)
        {
            if (uiBroadcastNameItemSelected!=null && uiBroadcastNameItemSelected == broadcastNameItem)
            {
                return;
            }
            if (broadcastNameItem)
            {
                broadcastNameItem.bg.color = Color.white;
                broadcastNameItem.broadcastName.color = new Color(74 / 255f, 74 / 255f, 79 / 255f,1f);
                broadcastNameItem.delete.image.color = new Color(74 / 255f, 74 / 255f, 79 / 255f,1f);
            }
            if (uiBroadcastNameItemSelected)
            {
                uiBroadcastNameItemSelected.bg.color = new Color(128 / 255f, 131 / 255f, 146 / 255f, 1f);
                uiBroadcastNameItemSelected.broadcastName.color = Color.white;
                uiBroadcastNameItemSelected.delete.image.color = Color.white;
            }
            {
                if (broadcastNameItem)
                {
                    this.UIRef.btn_BroadcastNameConfirm.targetGraphic.color = new Color(255 / 255f, 195 / 255f, 31 / 255f);
                    this.UIRef.txt_BroadcastNameConfirm.color = Color.black;
                    this.UIRef.btn_BroadcastNameEdit.targetGraphic.color = Color.white;
                    this.UIRef.img_BroadcastNameEdit.color = Color.black;
                    this.UIRef.btn_BroadcastNameConfirm.interactable = true;
                    this.UIRef.btn_BroadcastNameEdit.interactable = true;
                }
                else
                {
                    this.UIRef.btn_BroadcastNameConfirm.targetGraphic.color = new Color(159 / 255f, 128 / 255f, 42 / 255f);
                    this.UIRef.txt_BroadcastNameConfirm.color = new Color(80 / 255f, 64 / 255f, 37 / 255f);
                    this.UIRef.btn_BroadcastNameEdit.targetGraphic.color = new Color(154 / 255f, 154 / 255f, 154 / 255f);
                    this.UIRef.img_BroadcastNameEdit.color = new Color(77 / 255f, 77 / 255f, 77 / 255f);
                    this.UIRef.btn_BroadcastNameConfirm.interactable = false;
                    this.UIRef.btn_BroadcastNameEdit.interactable = false;
                }
            }
            uiBroadcastNameItemSelected = broadcastNameItem;
        }

        private void CreateParameterItem(string name, Type type, AssetType assetType, string iconName)
        {
            UIBroadcastParameterItem broadcastParameterItem = Object.Instantiate(uiBroadcastParameterItemTemplate, this.UIRef.rectran_BroadcastParameterItem.parent);
            broadcastParameterList.Add(broadcastParameterItem);
            broadcastParameterItem.gameObject.SetActive(true);
            broadcastParameterItem.edit.onClick.RemoveAllListeners();
            broadcastParameterItem.edit.onClick.AddListener(() =>
            {
                broadcastParameterNameItemSelected = broadcastParameterItem.parameterName.text;
                OpenChooseVariableType(type, assetType);
            });
            broadcastParameterItem.icon.sprite = LoadSprite.GetSprite(LoadSprite.TypeIcon, iconName);
            broadcastParameterItem.parameterName.text = name;
            broadcastParameterItem.parameterName.onEndEdit.RemoveAllListeners();
            broadcastParameterItem.parameterName.onEndEdit.AddListener(str =>
            {
                var parameName = broadcastInfoName;
                var parameTypes = broadcastInfoTypes;
                var parameAssetTypes = broadcastInfoAssetTypes;
                BroadcastInfo info = null;
                if (uiBroadcastNameItemSelected != null)
                {
                    info = Global.Game.Scene.EnvComponent.AllBroadcast.Find(x => x.name == uiBroadcastNameItemSelected.broadcastName.text);
                }
                if (info != null)
                {
                    parameName = info.parameterName;
                    parameTypes = info.parameterTypes;
                    parameAssetTypes = info.parameterAssetTypes;
                }
                int index = parameName.IndexOf(name);
                int tempIndex = parameName.IndexOf(str);
                bool hasName = tempIndex != -1 && tempIndex != index;

                bool DetectionDuplicateName(string str)
                {
                    return parameName.Contains(str) && str != parameName[index];
                }
                if (hasName || string.IsNullOrWhiteSpace(str))
                {
                    if (str == null || str.Length >= 16)
                    {
                        str = ReName(parameterTypeList.Find(x => x.type == type && x.assetType == assetType).defaultName.GetLanguageStr(), DetectionDuplicateName);
                    }
                    else
                    {
                        str = ReName(str, DetectionDuplicateName);
                        if (str.Length > 16)
                        {
                            str = ReName(parameterTypeList.Find(x => x.type == type && x.assetType == assetType).defaultName.GetLanguageStr(), DetectionDuplicateName);
                        }
                    }
                    broadcastParameterItem.parameterName.SetTextWithoutNotify(str);
                }
                parameName[index] = str;
                parameTypes[index] = type;
                parameAssetTypes[index] = assetType;
                name = str;
            });
            if (broadcastParameterList.Count == 1)
            {
                this.UIRef.size_BroadcastContent.gameObject.SetActive(true);
            }
            else if (broadcastParameterList.Count == 5)
            {
                //TODO 关闭size的layout
                this.UIRef.size_BroadcastParameterView.enabled = false;
                this.UIRef.size_BroadcastParameterView.GetComponent<VerticalLayoutGroup>().enabled = false;
                this.UIRef.scr_BroadcastParameterList.GetComponent<ContentSizeFitter>().enabled = false;
                this.UIRef.scr_BroadcastParameterList.GetComponent<VerticalLayoutGroup>().enabled = false;
                this.UIRef.scr_BroadcastParameterList.enabled = true;
            }
            broadcastParameterItem.delete.onClick.RemoveAllListeners();
            broadcastParameterItem.delete.onClick.AddListener(() =>
            {
                if (broadcastParameterList.Count == 1)
                {
                    this.UIRef.size_BroadcastContent.gameObject.SetActive(false);
                }
                else if (broadcastParameterList.Count == 5)
                {
                    //TODO 打开size的layout
                    this.UIRef.size_BroadcastParameterView.enabled = true;
                    this.UIRef.size_BroadcastParameterView.GetComponent<VerticalLayoutGroup>().enabled = true;
                    this.UIRef.scr_BroadcastParameterList.GetComponent<ContentSizeFitter>().enabled = true;
                    this.UIRef.scr_BroadcastParameterList.GetComponent<VerticalLayoutGroup>().enabled = true;
                    this.UIRef.scr_BroadcastParameterList.enabled = false;
                }
                broadcastParameterList.Remove(broadcastParameterItem);
                var parameName = broadcastInfoName;
                var parameTypes = broadcastInfoTypes;
                var parameAssetTypes = broadcastInfoAssetTypes;
                BroadcastInfo info = null;
                if (uiBroadcastNameItemSelected != null)
                {
                    info = Global.Game.Scene.EnvComponent.AllBroadcast.Find(x => x.name == uiBroadcastNameItemSelected.broadcastName.text);
                }
                if (info != null)
                {
                    parameName = info.parameterName;
                    parameTypes = info.parameterTypes;
                    parameAssetTypes = info.parameterAssetTypes;
                }
                int index = parameName.IndexOf(broadcastParameterItem.parameterName.text);
                parameName.RemoveAt(index);
                parameTypes.RemoveAt(index);
                parameAssetTypes.RemoveAt(index);
                broadcastParameterItem.transform.SetParent(null);
                Object.Destroy(broadcastParameterItem.gameObject);
                RefreshBroadcastParameterList();
            });
        }

        private void CreatBroadcastParameterTypeItem(Type type, AssetType assetType)
        {
            var parameName = broadcastInfoName;
            var parameTypes = broadcastInfoTypes;
            var parameAssetTypes = broadcastInfoAssetTypes;
            BroadcastInfo info = null;
            if (uiBroadcastNameItemSelected != null)
            {
                info = Global.Game.Scene.EnvComponent.AllBroadcast.Find(x => x.name == uiBroadcastNameItemSelected.broadcastName.text);
            }
            if (info != null)
            {
                parameName = info.parameterName;
                parameTypes = info.parameterTypes;
                parameAssetTypes = info.parameterAssetTypes;
            }
            for (int i = 0; i < parameName.Count; i++)
            {
                if (broadcastParameterNameItemSelected == parameName[i])
                {
                    parameName[i] = broadcastParameterNameItemSelected;
                    parameTypes[i] = type;
                    parameAssetTypes[i] = assetType;
                    return;
                }
            }
            parameName.Add(broadcastParameterNameItemSelected);
            parameTypes.Add(type);
            parameAssetTypes.Add(assetType);
        }

        private void OpenCreateElementType(Type elementType, AssetType elementAssetType)
        {
            isSelectElementType = true;
            this.elementType = elementType;
            this.elementAssetType = elementAssetType;
            this.UIRef.rectran_BroadcastNameListPanel.gameObject.SetActive(false);
            this.UIRef.rectran_AddBroadcastPanel.gameObject.SetActive(false);
            this.UIRef.rectran_ChooseVariableTybe.gameObject.SetActive(false);
            this.UIRef.rectran_CreateElementType.gameObject.SetActive(true);
            var info = parameterTypeList.Find(info => info.type == elementType && info.assetType == elementAssetType);
            this.UIRef.txt_ElementTypeName.text = info.typeName.GetLanguageStr();
            this.UIRef.img_ElementTypeImg.sprite = LoadSprite.GetSprite(LoadSprite.TypeIcon, info.iconName);
        }

        private async void RefreshBroadcastNameList()
        {
            await UniTask.DelayFrame(1);
            if (this.UIRef.scr_BroadcastNameList.enabled)
            {
                LayoutRebuilder.ForceRebuildLayoutImmediate(this.UIRef.size_BroadcastNameContent.transform as RectTransform);
                await UniTask.DelayFrame(1);
                LayoutRebuilder.ForceRebuildLayoutImmediate(this.UIRef.size_BroadcastNameContent.transform as RectTransform);
                RectTransform rect = this.UIRef.size_BroadcastNameView.transform as RectTransform;
                rect.sizeDelta = new Vector2(562, 390);
                rect = this.UIRef.scr_BroadcastNameList.transform as RectTransform;
                rect.sizeDelta = new Vector2(562, 395);
                this.UIRef.rectran_BroadcastNameListPanel.sizeDelta = new Vector2(700, 866);
                this.UIRef.scr_BroadcastNameList.horizontalNormalizedPosition = 0;
                this.UIRef.scr_BroadcastNameList.velocity = Vector2.zero;
            }
            else
            {
                LayoutRebuilder.ForceRebuildLayoutImmediate(this.UIRef.size_BroadcastNameContent.transform as RectTransform);
                await UniTask.DelayFrame(1);
                LayoutRebuilder.ForceRebuildLayoutImmediate(this.UIRef.size_BroadcastNameContent.transform as RectTransform);
                await UniTask.DelayFrame(1);
                LayoutRebuilder.ForceRebuildLayoutImmediate(this.UIRef.rectran_BroadcastNameListPanel);
                await UniTask.DelayFrame(1);
                LayoutRebuilder.ForceRebuildLayoutImmediate(this.UIRef.rectran_BroadcastNameListPanel);
            }
        }

        private async void RefreshBroadcastParameterList()
        {
            await UniTask.DelayFrame(1);
            if (this.UIRef.scr_BroadcastParameterList.enabled)
            {
                LayoutRebuilder.ForceRebuildLayoutImmediate(this.UIRef.size_BroadcastParameterContent.transform as RectTransform);
                await UniTask.DelayFrame(1);
                LayoutRebuilder.ForceRebuildLayoutImmediate(this.UIRef.size_BroadcastParameterContent.transform as RectTransform);
                RectTransform rect = this.UIRef.scr_BroadcastParameterList.transform as RectTransform;
                rect.sizeDelta = new Vector2(600, 605);
                rect = this.UIRef.size_BroadcastParameterView.transform as RectTransform;
                rect.sizeDelta = new Vector2(600, 605);
                this.UIRef.scr_BroadcastParameterList.horizontalNormalizedPosition = 0;
                this.UIRef.scr_BroadcastParameterList.velocity = Vector2.zero;
            }
            else
            {
                LayoutRebuilder.ForceRebuildLayoutImmediate(this.UIRef.size_BroadcastParameterContent.transform as RectTransform);
                await UniTask.DelayFrame(1);
                LayoutRebuilder.ForceRebuildLayoutImmediate(this.UIRef.size_BroadcastParameterContent.transform as RectTransform);
                await UniTask.DelayFrame(1);
                LayoutRebuilder.ForceRebuildLayoutImmediate(this.UIRef.rectran_AddBroadcastPanel);
                await UniTask.DelayFrame(1);
                LayoutRebuilder.ForceRebuildLayoutImmediate(this.UIRef.rectran_AddBroadcastPanel);
            }
        }

        private string ReName(string name, Func<string, bool> detectionDuplicateName)
        {
            int count = 1;
            string parameter;
            while (true)
            {
                parameter = $@"{name}{count}";
                if (!detectionDuplicateName(parameter))
                {
                    break;
                }
                count++;
            }
            return parameter;
        }

        public override void OnDestroy()
        {
            OnCreateBroadcast = null;
            base.OnDestroy();
        }
    }

    public class UIBroadcastNameItem : MonoBehaviour
    {
        public Button onSelect;
        public Image bg;
        public Text broadcastName;
        public Button delete;
    }

    public class UIBroadcastParameterItem : MonoBehaviour
    {
        public Button edit;
        public Image icon;
        public InputField parameterName;
        public Button delete;
    }

    public class UIBroadcastParameterTypeItem : MonoBehaviour
    {
        public Button onSelect;
        public Image bg;
        public Image icon;
        public Text typeName;
        public GameObject Press;
    }
```

`UIBroadcast`

类继承自 `UIBase<UIBroadcastRef, UIBroadcastModel>`，用于在 Unity 中管理和操作广播 UI 元素。该类包含多个字段和方法，用于处理广播名称和参数的创建、选择、编辑、删除等功能。

首先，类中定义了几个字段，包括静态的 `OnCreateBroadcast` 事件和实例的 `OnSelelctBroadcast` 事件，用于处理广播的创建和选择。`broadcastNameList`、`broadcastParameterList` 和 `broadcastParameterTypeList` 分别用于存储广播名称项、广播参数项和广播参数类型项的列表。`uiBroadcastNameItemTemplate`、`uiBroadcastParameterItemTemplate` 和 `uiBroadcastParameterTypeItemTemplate` 是模板项，用于创建新的广播名称、参数和参数类型项。`uiBroadcastNameItemSelected` 和 `broadcastParameterNameItemSelected` 分别用于存储当前选中的广播名称项和参数名称项。`broadcastName`、`broadcastInfoName`、`broadcastInfoTypes` 和 `broadcastInfoAssetTypes` 分别用于存储广播名称、参数名称、参数类型和参数资产类型。`parameterType` 和 `parameterAssetType` 分别用于存储当前选择的参数类型和资产类型。`elementType` 和 `elementAssetType` 分别用于存储当前选择的元素类型和资产类型。`isSelectElementType` 是一个布尔字段，用于指示是否选择元素类型。`parameterTypeList` 是一个静态列表，用于存储参数类型、资产类型、类型名称、默认名称和图标名称的元组。

`ShowType` 属性重写了基类的 `ShowType` 属性，返回 `FormShowType.Third`，表示第三种显示类型。`OnInit` 方法用于初始化广播 UI 元素。方法首先通过添加组件和获取子对象的方式初始化广播名称项、参数项和参数类型项的模板。接着，设置多语言文本内容，并为关闭按钮、添加广播按钮、确认按钮、编辑按钮、添加参数按钮和确认添加广播按钮添加点击事件。方法还清空广播名称列表，并根据全局游戏场景中的广播信息创建广播名称项。最后，设置 `OnCreateBroadcast` 事件为 `CreateBroadcastNameItem` 方法。

`CreateParamType` 方法用于创建参数类型。方法首先检查 `broadcastParameterNameItemSelected` 是否为空，如果为空则根据当前选中的广播名称项或全局广播信息初始化参数名称，并调用 `CreatBroadcastParameterTypeItem` 方法创建广播参数类型项。如果不为空，则根据当前选中的广播名称项或全局广播信息更新参数类型和资产类型。最后，根据当前选中的广播名称项或广播名称打开添加广播面板。

`OnOpen` 方法重写了基类的 `OnOpen` 方法，用于打开广播 UI 面板。方法首先检查传入的参数，如果有参数则将第一个参数设置为 `OnSelelctBroadcast` 事件。然后，调用 `OpenBroadcastNameListPanel` 方法打开广播名称列表面板。`OnClose` 方法重写了基类的 `OnClose` 方法，用于关闭广播 UI 面板。

`OpenBroadcastNameListPanel` 方法用于打开广播名称列表面板。方法首先设置广播名称列表面板为激活状态，并隐藏添加广播面板、选择变量类型面板和创建元素类型面板。然后，调用 `OnSelectBroadcastNameItem` 方法取消选中广播名称项，并调用 `RefreshBroadcastNameList` 方法刷新广播名称列表。

`OpenAddBroadcastPanel` 方法用于打开添加广播面板。方法首先隐藏广播名称列表面板、选择变量类型面板和创建元素类型面板，并设置添加广播面板为激活状态。然后，根据传入的广播名称文本初始化广播名称和参数信息，并清空广播参数列表。接着，根据参数信息创建广播参数项，并调用 `RefreshBroadcastParameterList` 方法刷新广播参数列表。

`OpenChooseVariableType` 方法用于打开选择变量类型面板。方法首先根据是否选择元素类型更新元素类型和资产类型或参数类型和资产类型。然后，隐藏广播名称列表面板、添加广播面板和创建元素类型面板，并设置选择变量类型面板为激活状态。接着，根据参数类型列表更新选择变量类型项的显示状态，并调用 `LayoutRebuilder.ForceRebuildLayoutImmediate` 方法强制重建布局。

`CreateBroadcastNameItem` 方法用于创建广播名称项。方法首先实例化广播名称项模板，并将其添加到广播名称列表中。然后，根据广播名称列表的数量更新广播名称列表的显示状态。接着，为广播名称项的选择按钮和删除按钮添加点击事件。最后，调用 `RefreshBroadcastNameList` 方法刷新广播名称列表。

`OnSelectBroadcastNameItem` 方法用于选中广播名称项。方法首先检查当前选中的广播名称项是否与传入的广播名称项相同，如果相同则返回。然后，更新传入的广播名称项和当前选中的广播名称项的显示状态。接着，根据传入的广播名称项更新确认按钮和编辑按钮的显示状态和交互状态。最后，将传入的广播名称项设置为当前选中的广播名称项。

`CreateParameterItem` 方法用于创建广播参数项。方法首先实例化广播参数项模板，并将其添加到广播参数列表中。然后，为广播参数项的编辑按钮和删除按钮添加点击事件。接着，根据参数类型和资产类型设置广播参数项的图标和名称，并为参数名称输入框添加结束编辑事件。最后，根据广播参数列表的数量更新广播参数列表的显示状态，并调用 `RefreshBroadcastParameterList` 方法刷新广播参数列表。

`CreatBroadcastParameterTypeItem` 方法用于创建广播参数类型项。方法首先根据当前选中的广播名称项或全局广播信息初始化参数名称、参数类型和资产类型。然后，检查参数名称列表中是否已存在当前选中的参数名称，如果存在则更新参数类型和资产类型，否则添加新的参数名称、参数类型和资产类型。

`OpenCreateElementType` 方法用于打开创建元素类型面板。方法首先设置 `isSelectElementType` 为 `true`，并更新元素类型和资产类型。然后，隐藏广播名称列表面板、添加广播面板和选择变量类型面板，并设置创建元素类型面板为激活状态。接着，根据元素类型和资产类型更新元素类型名称和图标。

`RefreshBroadcastNameList` 方法是一个异步方法，用于刷新广播名称列表。方法首先延迟一帧，然后根据广播名称列表的显示状态强制重建布局，并更新广播名称列表面板的大小和位置。

`RefreshBroadcastParameterList` 方法是一个异步方法，用于刷新广播参数列表。方法首先延迟一帧，然后根据广播参数列表的显示状态强制重建布局，并更新广播参数列表面板的大小和位置。

`ReName` 方法用于重命名参数名称。方法接受一个名称和一个检测重复名称的函数作为参数，并返回一个不重复的参数名称。

`OnDestroy` 方法重写了基类的 `OnDestroy` 方法，用于销毁广播 UI 元素。方法首先将 `OnCreateBroadcast` 事件设置为 `null`，然后调用基类的 `OnDestroy` 方法。