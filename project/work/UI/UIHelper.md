
UIPathDic ： UI 路由 --- 生成路径 ： `dic<UIName, string>`
UIFactory ： 工厂 --- enum ,   `Func<UIBase>`
UIPool : 缓存池
FirstUI ： enum --- 第一个 UI

一些常用的小组件 ： dialog ， MessagePop，gameloading

```c#
private static GameObject toastParent;  
public static UIGizmosManager GizmosMgr = new UIGizmosManager();
private Transform uiParent;
private Transform hudCanvas;
GameObject Toast;

```



```c#
    private void LoadUIConfig()
    {
        /*-----------------------------------------UI路由--------------------------------------------------*/
        UIPathDic[UIName.BUDHome] = RouteHelper.UI_UniEditorHome;
        UIPathDic[UIName.AvatarBudHome] = RouteHelper.UI_UniEditorHome;
        UIPathDic[UIName.UIUGCAvatarItemHome] = RouteHelper.UI_UniEditorHome;
        UIPathDic[UIName.UIEdit] = RouteHelper.UI_UniEditorHome;

        UIPathDic[UIName.PlayHome] = RouteHelper.UI_PlayHome;
        UIPathDic[UIName.PlayFly] = RouteHelper.UI_PlayFly;

        UIPathDic[UIName.Material] = RouteHelper.UI_Material;
        UIPathDic[UIName.Scene] = RouteHelper.UI_Scene;
        UIPathDic[UIName.BudPublish] = RouteHelper.UI_BudPublish;
        UIPathDic[UIName.BudHoleMask] = RouteHelper.UI_HoleMask;
        UIPathDic[UIName.Shop] = RouteHelper.UI_Shop;
        UIPathDic[UIName.EditSet] = RouteHelper.UI_EditSet;
        UIPathDic[UIName.Clothes] = RouteHelper.UI_Clothes;
        UIPathDic[UIName.Bag] = RouteHelper.UI_Bag;
        UIPathDic[UIName.Inventory] = RouteHelper.UI_Inventory;
        UIPathDic[UIName.BagTips] = RouteHelper.UI_BagTips;
        UIPathDic[UIName.BudText] = RouteHelper.UI_BudText;
        UIPathDic[UIName.UGCPropSetAction] = RouteHelper.UI_UGCPropSetAction;
        UIPathDic[UIName.Loading] = RouteHelper.UI_Loading;
        UIPathDic[UIName.PlaySet] = RouteHelper.UI_PlaySet;
        UIPathDic[UIName.PlayerInfo] = RouteHelper.UI_PlayerInfo;
        UIPathDic[UIName.MeBG] = RouteHelper.UI_MeBG;
        UIPathDic[UIName.UIScoreRank] = RouteHelper.UI_ScoreRank;
        UIPathDic[UIName.EventBlock] = RouteHelper.UI_EventBlock;
        UIPathDic[UIName.UIAnimEdit] = RouteHelper.UI_AnimEdit;
        UIPathDic[UIName.UIAvatarAnimationEdit] = RouteHelper.UI_AvatarAnimationEdit;

        UIPathDic[UIName.Options] = RouteHelper.UI_Options;
        UIPathDic[UIName.Painting] = RouteHelper.UI_Painting;
        UIPathDic[UIName.BudPic] = RouteHelper.UI_BudPic;
        UIPathDic[UIName.MapTip] = RouteHelper.UI_MapTip;
        UIPathDic[UIName.CustomDialog] = RouteHelper.UI_CustomDialog;//弃用 todo remove
        UIPathDic[UIName.UICountDownTip] = RouteHelper.UI_CountDownTip;
        //UIPathDic[UIName.Storage] = RouteHelper.UI_Storage;
        UIPathDic[UIName.UIUpload] = RouteHelper.UI_Upload;
        UIPathDic[UIName.UITechTips] = RouteHelper.UI_TechTips;
        UIPathDic[UIName.UITechBook] = RouteHelper.UI_TechBook;
        UIPathDic[UIName.ColorInspector] = RouteHelper.UI_ColorInspector;
        UIPathDic[UIName.TextureInspector] = RouteHelper.UI_TextureInspector;
        UIPathDic[UIName.ParticleForce] = RouteHelper.UI_ParticleForce;
        UIPathDic[UIName.Profile] = RouteHelper.UI_Profile;
        UIPathDic[UIName.Friend] = RouteHelper.UI_Friend;
        UIPathDic[UIName.UI_UniChannelSelector] = RouteHelper.UI_UniChannelSelector;
        UIPathDic[UIName.Obtained] = RouteHelper.UI_Obtained;
        UIPathDic[UIName.MapRuler] = RouteHelper.UI_MapRuler;
        UIPathDic[UIName.Tag] = RouteHelper.UI_Tag;
        UIPathDic[UIName.UICompTechTips] = RouteHelper.UI_CompTechTips;
        UIPathDic[UIName.UIAvatarAnimationEditSecond] = RouteHelper.UI_AvatarAnimationEdit;
        UIPathDic[UIName.PopMsg] = RouteHelper.UI_PopMsg;
        UIPathDic[UIName.UIDisplayFrame] = RouteHelper.UI_DisplayFrame;
        UIPathDic[UIName.UGCModelInfo] = RouteHelper.UI_UGCModelInfo;
        UIPathDic[UIName.UIWaterLineEdit] = RouteHelper.UI_WaterLineEdit;
        UIPathDic[UIName.MusicStore] = RouteHelper.UI_MusicStore;
        UIPathDic[UIName.MusicBank] = RouteHelper.UI_MusicBank;
        UIPathDic[UIName.VehicleBank] = RouteHelper.UI_VehicleBank;
        UIPathDic[UIName.BGMBank] = RouteHelper.UI_BGMBank;
        UIPathDic[UIName.ScreenRecording] = RouteHelper.UI_ScreenRecording;

        UIPathDic[UIName.ConversationSentence] = RouteHelper.UI_ConversationSentence;
        UIPathDic[UIName.ConversationOption] = RouteHelper.UI_ConversationOption;
        UIPathDic[UIName.ConversationAddUnitsList] = RouteHelper.UI_ConversationAddUnitsList;
        UIPathDic[UIName.ConversationGraph] = RouteHelper.UI_ConversationGraph;
        UIPathDic[UIName.Conversation] = RouteHelper.UI_Conversation;
        UIPathDic[UIName.UnitSelector] = RouteHelper.UI_UnitSelector;
        UIPathDic[UIName.ConversationChooseVariableType] = RouteHelper.UI_ConversationChooseVariableType;
        UIPathDic[UIName.ConversationEditVariable] = RouteHelper.UI_ConversationEditVariable;
        UIPathDic[UIName.PlayerVariableSelector] = RouteHelper.UI_PlayerVariableSelector;
        UIPathDic[UIName.EditBag] = RouteHelper.UI_EditBag;
        UIPathDic[UIName.UIKeyChannelSelector] = RouteHelper.UI_KeyChannelSelector;
        UIPathDic[UIName.AtFriend] = RouteHelper.UI_AtFriend;
        UIPathDic[UIName.UIEditPrifleImage] = RouteHelper.UI_EditProfileImage;
        UIPathDic[UIName.RoadColorSelector] = RouteHelper.UI_RoadColorSelector;
        UIPathDic[UIName.ChangeWorld] = RouteHelper.UI_ChangeWorld;
        UIPathDic[UIName.ChooseWorld] = RouteHelper.UI_ChooseWorld;
        UIPathDic[UIName.BulletSettingsMenu] = RouteHelper.UI_BulletSettingsMenu;
        UIPathDic[UIName.ProjectAssetPopup] = RouteHelper.UI_ProjectAssetPopup;
        UIPathDic[UIName.AssetPopup] = RouteHelper.UI_AssetPopup;
        UIPathDic[UIName.UICommonAssetSelector] = RouteHelper.UI_CommonAssetSelector;
        UIPathDic[UIName.UICommonAssetPopup] = RouteHelper.UI_CommonAssetPopup;
        UIPathDic[UIName.UIBroadcast] = RouteHelper.UI_Broadcast;
        UIPathDic[UIName.UIFeedback] = RouteHelper.UI_Feedback;
        UIPathDic[UIName.UINewComponent] = RouteHelper.UI_NewComponent;
        UIPathDic[UIName.UICanvasEdit] = RouteHelper.UI_CanvasEdit;
        UIPathDic[UIName.UIRecharge] = RouteHelper.UI_Recharge;
        UIPathDic[UIName.MergeScriptInfo] = RouteHelper.UI_MergeScriptInfo;

        UIPathDic[UIName.UIWeb] = RouteHelper.UI_Web;
        UIPathDic[UIName.UIWeaponSource] = RouteHelper.UI_WeaponSource;
        UIPathDic[UIName.UIChangeUILayer] = RouteHelper.UI_ChangeUILayer;
        UIPathDic[UIName.UIUniComponentParamsTips] = RouteHelper.UI_UniComponentParamsTips;

        //UI_RoadColorSelectorRoadColorSelector
        /*-------------------------------------------------------------------------------------------*/


        /*---------------------------------------UI工厂----------------------------------------------------*/
        //UIFactory.Add(UIName.BUD, () => new UIBudPanel());
        UIFactory.Add(UIName.BUDHome, () => new UIUniEditorHome());
        UIFactory.Add(UIName.AvatarBudHome, () => new UIAvatarUniEditorHome());
        UIFactory.Add(UIName.UIUGCAvatarItemHome, () => new UIUGCAvatarItemBudHome());

        UIFactory.Add(UIName.UIEdit, () => new UIEditBudHome());

        UIFactory.Add(UIName.PlayHome, () => new UIPlayHome());
        UIFactory.Add(UIName.PlayFly, () => new UIPlayFly());
        UIFactory.Add(UIName.Material, () => new UIMaterial());
        UIFactory.Add(UIName.Scene, () => new UIScene());
        UIFactory.Add(UIName.BudPublish, () => new UIBudPublish());
        UIFactory.Add(UIName.BudHoleMask, () => new UIHoleMask());
        UIFactory.Add(UIName.Painting, () => new UIPainting());
        UIFactory.Add(UIName.UIDisplayFrame, () => new UIDisplayFrame());

        UIFactory.Add(UIName.Shop, () => new UIShop());
        UIFactory.Add(UIName.EditSet, () => new UIEditSet());
        UIFactory.Add(UIName.Clothes, () => new UIClothes());
        UIFactory.Add(UIName.Bag, () => new UIBag());
        UIFactory.Add(UIName.Inventory, () => new UIBagInventory());
        UIFactory.Add(UIName.BagTips, () => new UIBagTips());
        UIFactory.Add(UIName.EditBag, () => new UIEditBag());

        UIFactory.Add(UIName.BudText, () => new UIBudText());
        UIFactory.Add(UIName.UGCPropSetAction, () => new UIUGCPropSetAction());

        UIFactory.Add(UIName.Loading, () => new UILoading());
        UIFactory.Add(UIName.PlaySet, () => new UIPlaySet());
        UIFactory.Add(UIName.PlayerInfo, () => new UIPlayerInfo());
        UIFactory.Add(UIName.MeBG, () => new UIMeBG());
        UIFactory.Add(UIName.MusicStore, () => new UIMusicStore());
        UIFactory.Add(UIName.MusicBank, () => new UIMusicBank());
        UIFactory.Add(UIName.ScreenRecording, () => new UIScreenRecording());
        UIFactory.Add(UIName.BGMBank, () => new UIBGMBank());
        UIFactory.Add(UIName.VehicleBank, () => new UIVehicleBank());
        UIFactory.Add(UIName.UIScoreRank, () => new UIScoreRank());
        UIFactory.Add(UIName.EventBlock, () => new UIEventBlock());
        UIFactory.Add(UIName.UIAnimEdit, () => new UIAnimEdit());
        UIFactory.Add(UIName.UIAvatarAnimationEdit, () => new UIAvatarAnimationEdit());

        UIFactory.Add(UIName.Options, () => new UIOptions());
        UIFactory.Add(UIName.BudPic, () => new UIBudPic());

        UIFactory.Add(UIName.MapTip, () => new UIMapTip());

        UIFactory.Add(UIName.CustomDialog, () => new UICustomDialog());
        UIFactory.Add(UIName.UICountDownTip, () => new UICountDownTip());
        //UIFactory.Add(UIName.Storage, () => new UIStorage());
        UIFactory.Add(UIName.UIUpload, () => new UIUpload());
        UIFactory.Add(UIName.UITechTips, () => new UITechTips());
        UIFactory.Add(UIName.UITechBook, () => new UITechBook());
        UIFactory.Add(UIName.ColorInspector, () => new UIColorInspector());
        UIFactory.Add(UIName.TextureInspector, () => new UITextureInspector());
        UIFactory.Add(UIName.ParticleForce, () => new UIParticleForce());
        UIFactory.Add(UIName.Friend, () => new UIFriend());
        UIFactory.Add(UIName.Profile, () => new UIProfile());
        UIFactory.Add(UIName.UI_UniChannelSelector, () => new UIUniChannelSelector());
        UIFactory.Add(UIName.Obtained, () => new UIObtained());
        UIFactory.Add(UIName.MapRuler, () => new UIMapRuler());
        UIFactory.Add(UIName.Tag, () => new UITag());
        UIFactory.Add(UIName.UICompTechTips, () => new UICompTechTips());
        UIFactory.Add(UIName.UIAvatarAnimationEditSecond, () => new UIAvatarAnimationEditSecond());
        UIFactory.Add(UIName.PopMsg, () => new UIPopMsg());
        //UIFactory.Add(UIName.KeyTypeSelector, () => new UIKeyTypeSelector());
        UIFactory.Add(UIName.UGCModelInfo, () => new UIUGCModelInfo());
        UIFactory.Add(UIName.UIWaterLineEdit, () => new UIWaterLineEdit());
        UIFactory.Add(UIName.ConversationGraph, () => new UIConversationGraph());
        UIFactory.Add(UIName.ConversationSentence, () => new UIConversationSentence());
        UIFactory.Add(UIName.ConversationOption, () => new UIConversationOption());
        UIFactory.Add(UIName.ConversationAddUnitsList, () => new UIConversationAddUnitsList());
        UIFactory.Add(UIName.Conversation, () => new UIConversation());
        UIFactory.Add(UIName.UnitSelector, () => new UIUnitSelector());
        UIFactory.Add(UIName.ConversationChooseVariableType, () => new UIConversationChooseVariableType());
        UIFactory.Add(UIName.ConversationEditVariable, () => new UIConversationEditVariable());
        UIFactory.Add(UIName.PlayerVariableSelector, () => new UIPlayerVariableSelector());
        UIFactory.Add(UIName.UIKeyChannelSelector, () => new UIKeyChannelSelector());
        UIFactory.Add(UIName.AtFriend, () => new UIAtFriend());
        UIFactory.Add(UIName.UIEditPrifleImage, () => new UIEditProfileImage());
        UIFactory.Add(UIName.RoadColorSelector, () => new UIRoadColorSelector());
        UIFactory.Add(UIName.ChangeWorld, () => new UIChangeWorld());
        UIFactory.Add(UIName.ChooseWorld, () => new UIChooseWorld());
        UIFactory.Add(UIName.UICommonAssetSelector, () => new UICommonAssetSelector());
        UIFactory.Add(UIName.UICommonAssetPopup, () => new UICommonAssetPopup());
        UIFactory.Add(UIName.BulletSettingsMenu, () => new UIBulletSettingsMenu());
        UIFactory.Add(UIName.ProjectAssetPopup, () => new UIProjectAssetPopup());
        UIFactory.Add(UIName.AssetPopup, () => new UIAssetPopup());
        UIFactory.Add(UIName.UIBroadcast, () => new UIBroadcast());
        UIFactory.Add(UIName.UIFeedback, () => new UIFeedBack());
        UIFactory.Add(UIName.UINewComponent, () => new UINewComponent());
        UIFactory.Add(UIName.UIWeb, () => new UIWeb());
        UIFactory.Add(UIName.UICanvasEdit, () => new UICanvasInspector());
        UIFactory.Add(UIName.UIWeaponSource, () => new UIWeaponSource());
        UIFactory.Add(UIName.UIRecharge, () => new UIRecharge());
        UIFactory.Add(UIName.UIChangeUILayer, () => new UIChangeUILayer());
        UIFactory.Add(UIName.MergeScriptInfo, () => new UIMergeScriptInfo());
        UIFactory.Add(UIName.UIUniComponentParamsTips, () => new UIUniComponentParamsTips());
        /*-------------------------------------------------------------------------------------------*/
    }
    /// <summary>
    /// 入口界面
    /// </summary>
    public UIName FirstUI = UIName.BUDHome;
    /// <summary>
    /// UISpawn 工厂
    /// </summary>
    private Dictionary<UIName, Func<UIBase>> UIFactory;
    /// <summary>
    /// 保存实例化的界面（缓存池
    /// </summary>
    public Dictionary<UIName, UIBase> UIPool;
    /// <summary>
    /// 界面生成的路径   读取配置表
    /// </summary>
    public Dictionary<UIName, string> UIPathDic;
    private static UIDialog dialog;
    private static GameObject gameLoading;
    private static MessagePopup messagePopup;
    private static GameObject toastParent;
    public static UIGizmosManager GizmosMgr = new UIGizmosManager();
    public GameObject ToastParent
    {
        get
        {
            CheckWaringUI();
            return toastParent;
        }
    }
    private Transform uiParent;
    public const float ScreenWidth = 1920;
    public const float ScreenHeight = 1080;

    UniLogger Logger = UniLogManager.Get<UIHelper>();
    private Transform hudCanvas;
    public Transform HudCanvas
    {
        get
        {
            CheckHudCanvasUI();
            return hudCanvas;
        }
    }

    public void Init()
    {
        if (UIPool != null) return;
        UIPathDic = new Dictionary<UIName, string>();
        UIPool = new Dictionary<UIName, UIBase>();
        UIFactory = new Dictionary<UIName, Func<UIBase>>();
        uiParent = UISystem.Inst.gameObject.transform;
        LoadUIConfig();
        (UniMain.Game.Scene as UniEditScene)?.OnEditTypeChange.AddListener(OnSceneEditTypeChange);
    }

    public UIBase CreateUI(UIName uiName)
    {
        UIBase baseUI = null;
        if (UIFactory != null && UIFactory.ContainsKey(uiName))
        {
            baseUI = UIFactory[uiName].Invoke();
        }
        else
        {
            Debug.Log(string.Format("UIHelper未注册：", uiName));
            // Uni.UniDebug.Log("",);
        }
        return baseUI;
    }

    public async UniTask LoadUI(UIBase baseUI, UIName uiName)
    {
        baseUI.UIGameObject = await LoadUIPrefab(UIPathDic[uiName]);
        try
        {
            baseUI?.OnInit();
        }
        catch (System.Exception e)
        {
#if UNITY_EDITOR
            Debug.LogException(e);
#endif
        }
    }

    /// <summary>
    /// 左下、左上、右上、右下
    /// </summary>
    /// <param name="rt">ui</param>
    /// <param name="index">0、1、2、3</param>
    /// <returns></returns>
    public Vector3 GetCornerScreenPos(RectTransform rt, int index)
    {
        Vector3[] corners = new Vector3[4];
        rt.GetWorldCorners(corners);
        Vector3 wPos = corners[index];
#if UNITY_EDITOR
        Logger.Debug($"{rt.name}:wPos:{wPos}");
#endif
        var UICanvas = rt.GetComponentInParent<Canvas>();
        Vector3 screenPos = wPos;
        if (UICanvas.renderMode != RenderMode.ScreenSpaceOverlay)
        {
            Camera uCame = UICanvas.worldCamera;
            screenPos = uCame.WorldToScreenPoint(wPos);
        }
#if UNITY_EDITOR
        Logger.Debug($"{rt.name}:screenPos:{screenPos}");
#endif
        return screenPos;
    }

    //固定分辨率

    GameObject Toast;//todo 改队列依次弹出
    public async void ShowToast(string text, string toast = RouteHelper.UI_Toast, float duration = -1)
    {
#if !UNITY_SERVER
        if (Toast)
        {
            Toast.GetComponent<TimeToDestroy>().DestroyImmediate();
        }
        CheckWaringUI();
        var go = await LoadUIPrefab(toast);
        //加个防报错
        if (toastParent == null) return;
        go.transform.SetParent(toastParent.transform);
        var rectTrans = go.GetComponent<RectTransform>();
        rectTrans.localPosition = Vector3.zero;
        rectTrans.anchoredPosition = new Vector2(0, -30);
        rectTrans.rotation.eulerAngles.Set(0f, 0f, 0f);
        rectTrans.localScale = Vector3.one;
        go.transform.SetAsLastSibling();
        var textComp = go.GetComponentInChildren<UnityEngine.UI.Text>();
        textComp.text = text;
        if (textComp.preferredWidth > 800)
        {
            var sf = textComp.GetComponent<ContentSizeFitter>();
            if (sf)
            {
                textComp.GetComponent<ContentSizeFitter>().horizontalFit = ContentSizeFitter.FitMode.Unconstrained;
                textComp.rectTransform.sizeDelta = new Vector2(800, textComp.rectTransform.sizeDelta.y);
            }
        }
        else
        {
            var sf = textComp.GetComponent<ContentSizeFitter>();
            if (sf)
            {
                sf.horizontalFit = ContentSizeFitter.FitMode.PreferredSize;
            }
        }
        if (duration > 0)
        {
            var ttd = go.GetComponent<TimeToDestroy>();
            if (ttd)
            {
                ttd.m_timeWaitForDestroy = duration;
                ttd.DestroyAfterTime();
            }
        }
        Toast = go;
#endif 
    }
    
    private void OnSceneEditTypeChange(bool isEdit)
    {
        if (isEdit && Toast)
        {
            Toast.GetComponent<TimeToDestroy>().DestroyImmediate();
        }
    }

    private void CheckWaringUI()
    {
        Canvas warningCanvas = null;
        if (toastParent == null)
        {
            toastParent = new GameObject("ToastCanvas");
            toastParent.layer = LayerMask.NameToLayer("UI");
            toastParent.transform.SetParent(uiParent);
            //waringParent.transform.localPosition = new Vector3(0, -370, 0);
            toastParent.transform.localScale = Vector3.one;
            warningCanvas = toastParent.AddComponent<Canvas>();
            warningCanvas.renderMode = RenderMode.ScreenSpaceOverlay;
            warningCanvas.overrideSorting = true;
            warningCanvas.sortingOrder = 100;
            var canvasScaler = toastParent.gameObject.AddComponent<CanvasScaler>();
            toastParent.gameObject.AddComponent<GraphicRaycaster>();
            canvasScaler.uiScaleMode = CanvasScaler.ScaleMode.ScaleWithScreenSize;
            canvasScaler.referenceResolution = new Vector2(ScreenWidth, ScreenHeight);
            canvasScaler.referencePixelsPerUnit = 100;
            canvasScaler.matchWidthOrHeight = 0;
        }
        else 
        {
            warningCanvas = toastParent.GetComponent<Canvas>();
        }
        if (warningCanvas.worldCamera == null)
        {
            if (UniGameCameras.GetInstance() != null)
            {
                warningCanvas.worldCamera = UniGameCameras.GetInstance().GetUICamera();
            }
        }
    }

    private void CheckHudCanvasUI()
    {
        if (hudCanvas == null)
        {
            hudCanvas = new GameObject("HudCanvas").transform;
            hudCanvas.SetParent(uiParent);
            //waringParent.transform.localPosition = new Vector3(0, -370, 0);
            hudCanvas.transform.localScale = Vector3.one;
            var warningCanvs = hudCanvas.gameObject.AddComponent<Canvas>();
            warningCanvs.renderMode = RenderMode.ScreenSpaceOverlay;
            warningCanvs.overrideSorting = true;
            warningCanvs.sortingOrder = 100;
            var canvasScaler = hudCanvas.gameObject.AddComponent<CanvasScaler>();
            canvasScaler.uiScaleMode = CanvasScaler.ScaleMode.ScaleWithScreenSize;
            canvasScaler.referenceResolution = new Vector2(ScreenWidth, ScreenHeight);
            canvasScaler.referencePixelsPerUnit = 100;
            canvasScaler.matchWidthOrHeight = 0;
        }
    }

    //FIX Todo 修改成直接加载Canvas

    public UIDialog ShowSingleBtnDialog(string content, string btnOk = "btn_confirm", System.Action onClickOk = null, string tips = "", Action<bool> TipAction = null)
    {
        Logger.Debug("ShowSingleBtnDialog  : " + content);
        var dig = CheckDialogUI();
        dig?.ShowDialog(EDialogType.oneButton, content, btnOk: btnOk, onClickOk: onClickOk, tipsStr: tips, TipAction: TipAction);
        dig?.transform.parent.SetAsLastSibling();
        return dig;
    }
    public UIDialog ShowDoubleBtnDialog(string content, string btnOk = "btn_confirm", string btnCancel = "btn_cancel", System.Action onClickOk = null, System.Action onClickCancel = null, string tips = "", Action<bool> TipAction = null, System.Action onClickClose = null)
    {
        var dig = CheckDialogUI();
        //btnOk = btnOk.GetLanguageStr();
        //btnCancel = 
        if (btnOk == "btn_confirm")
        {
            btnOk = btnOk.GetLanguageStr();
        }

        if (btnCancel == "btn_cancel")
        {
            btnCancel = btnCancel.GetLanguageStr();
        }
        dig?.ShowDialog(EDialogType.twoButton, content, btnOk: btnOk, btnCancel: btnCancel, onClickOk: onClickOk, onClickCancel: onClickCancel, tipsStr: tips, TipAction: TipAction, onClickClose);
        dig?.transform.parent.SetAsLastSibling();
        return dig;
    }

    public void ShowGameLoading()
    {
        if (gameLoading == null)
        {
            var path = string.Format("prefabs/ui/{0}.unity3d", RouteHelper.UI_GameLoading.ToLower());
            var loader = UniMain.AssetModule.CreateLoader<UniAddressableLoader<GameObject>>(path);
            var obj = loader.LoadAsset();
            if (obj)
            {
                gameLoading = GameObject.Instantiate(obj);
            }
            GameObject.DontDestroyOnLoad(gameLoading);
            gameLoading.transform.SetParent(uiParent.Find("UI_Canvas"));
            var rect = gameLoading.GetComponent<RectTransform>();
            rect.localPosition = Vector3.zero;
            rect.anchoredPosition = Vector2.zero;
            rect.sizeDelta = new Vector2(Screen.width, Screen.height);
            rect.localScale = Vector3.one;
        }
        gameLoading?.SetGameObejctActive(true);
    }
    public void HideGameLoading()
    {
        gameLoading?.SetGameObejctActive(false);
    }
    public MessagePopup ShowMessagePopup(string title, string content, string confirmContent, float time = 5f, System.Action confirm = null, bool isReplaceable = true, bool isHighPriority = false, System.Action closeAction = null, bool isShowConfirmBtn = true)
    {
        var msg = CheckMessagePopupUI();
        msg?.ShowMessage(title, content, confirmContent, time, confirm: confirm, isReplaceable: isReplaceable, isHighPriority: isHighPriority, closeAction, isShowConfirmBtn);
        msg?.transform.parent.SetAsLastSibling();
        return msg;
    }

    private UIDialog CheckDialogUI()
    {
        //DIalog
        if (dialog == null)
        {
            var path = string.Format("prefabs/ui/{0}.unity3d", RouteHelper.UI_DIALOG.ToLower());
            var loader = UniMain.AssetModule.CreateLoader<UniAddressableLoader<GameObject>>(path);
            var obj = loader.LoadAsset();
            if (obj)
            {
                obj = GameObject.Instantiate(obj);
            }
            GameObject.DontDestroyOnLoad(obj.gameObject);

            obj.transform.SetParent(uiParent);
            obj.gameObject.name = "UIDialogCanvas";

            dialog = obj.GetComponentInChildren<UIDialog>();

            if (messagePopup == null)
            {
                messagePopup = dialog.transform.parent.GetComponentInChildren<MessagePopup>();
            }

            obj.transform.localPosition = Vector3.zero;
            obj.transform.localScale = Vector3.one;
            dialog.gameObject.SetActive(false);
            obj.gameObject.GetComponent<Canvas>().overrideSorting = true;
            obj.gameObject.GetComponent<Canvas>().sortingOrder = 100;
            var ui_trans = (dialog.transform as RectTransform);
            ui_trans.anchorMin = Vector2.zero;
            ui_trans.anchorMax = Vector2.one;
            ui_trans.offsetMin = Vector2.zero;
            ui_trans.offsetMax = Vector2.zero;
        }

        messagePopup.gameObject.SetActive(false);
        dialog.gameObject.SetActive(true);

        return dialog;
    }
    /// <summary>
    /// 打开快捷素材选择窗口
    /// </summary>
    /// <param name="param"></param>
    public void OpenQuickAssetSelector(QAssetSelectorParam param)
    {
        if (param.type == AssetType.BGM)
        {
            UISystem.Inst.ShowUIScene(UIName.BGMBank, param.OnBGMSelect);
        }
        else
        {
            UISystem.Inst.ShowUIScene(UIName.UICommonAssetSelector, param);
        }
    }
    /// <summary>
    /// 打开通用素材库窗口
    /// </summary>
    /// <param name="param"></param>
    public void OpenCommonAssetPopup(CommonAssetParam param)
    {
        UISystem.Inst.ShowUIScene(UIName.UICommonAssetPopup, param);
    }
    private MessagePopup CheckMessagePopupUI()
    {
        if (dialog == null)
        {
            CheckDialogUI();
        }

        dialog.gameObject.SetActive(false);
        messagePopup.gameObject.SetActive(true);

        return messagePopup;
    }
    public async UniTask<GameObject> LoadUIPrefab(string uiName)
    {
        return await UniMain.AssetModule.InstantiateAsync(string.Format("prefabs/{0}.unity3d", string.Format("ui/{0}", uiName.ToLower())));
    }
    public void LoadUIPrefab(Action<List<UniAddressableLoader<GameObject>>> callback, params string[] uiName)
    {
        List<string> paths = new List<string>();
        foreach (var n in uiName)
        {
            var path = string.Format("prefabs/ui/{0}", uiName);
            paths.Add(path);
        }
        UniMain.AssetModule.LoadAssets<GameObject>(paths, callback);
    }
    public async UniTask<GameObject> LoadPrefab(string uiName)
    {
        var loader = await UniMain.AssetModule.InstantiateAsync(string.Format("prefabs/{0}.unity3d", uiName));
        return (loader);
    }

    public override void Dispose()
    {
        base.Dispose();
        this.uiParent = null;
        this.UIFactory?.Clear();

        ClearAllUIPool();
        this.UIPathDic?.Clear();
        this.UIFactory = null;
        this.UIPathDic = null;
        GizmosMgr.Dispose();
    }

    /// <summary>
    /// 清理ui池子
    /// </summary>
    /// <returns></returns>
    public void ClearAllUIPool()
    {
        if (UIPool != null && UIPool.Count > 0)
        {
            foreach (var pair in UIPool.ToList())
            {
                UIPool[pair.Key].OnDestroy();
                UIPool.Remove(pair.Key);
            }
        }
        this.UIPool?.Clear();
        this.UIPool = null;
    }

    /// <summary>
    /// 背包等常用ui设置sprite方法
    /// </summary>
    public static void SetSpriteSimple(int ver, string id, string md5, Image icon, bool gray, bool isOfficial)
    {
        icon.sprite = null;
        if (string.IsNullOrEmpty(id) || id == "10001")
        {
            var sprite = LoadSprite.GetSprite(LoadSprite.GetItemBud(10001), "10001");
            icon.sprite = sprite;
            icon.color = new Color(1, 1, 1, 1);
            icon.rectTransform.sizeDelta = new Vector2(130, 130);
        }
        else
        {
            string str;
            if (ver > 1)
            {
                str = $"{Global.NetworkSetting.DownloadImageUrl()}/bud/{id}-{ver}.png?{AppConst.downloadSize_180_180}";
            }
            else
            {
                str = $"{Global.NetworkSetting.DownloadImageUrl()}/bud/{id}.png?{AppConst.downloadSize_180_180}";
            }

            DownloadImg downloadImg = icon.gameObject.GetComponent<DownloadImg>();
            downloadImg.isOfficial = isOfficial;
            downloadImg.Gray = gray;
            downloadImg.DownloadNetImg(str, md5);
            if (icon.sprite != null)
            {
                icon.color = new Color(1, 1, 1, 1);
            }
            else
            {
                icon.color = new Color(1, 1, 1, 0);
            }

            icon.rectTransform.sizeDelta = new Vector2(160, 160);
        }
    }

    public static void SetSpriteSimplePlayBag(int ver, string id, string md5, Image icon, bool gray, bool isOfficial)
    {
        icon.sprite = null;
        string str;
        if (ver > 1)
        {
            str = $"{Global.NetworkSetting.DownloadImageUrl()}/bud/{id}-{ver}.png?{AppConst.downloadSize_180_180}";
        }
        else
        {
            str = $"{Global.NetworkSetting.DownloadImageUrl()}/bud/{id}.png?{AppConst.downloadSize_180_180}";
        }

        DownloadImg downloadImg = icon.gameObject.GetComponent<DownloadImg>();
        downloadImg.isOfficial = isOfficial;
        downloadImg.Gray = gray;
        downloadImg.DownloadNetImg(str, md5);
        if (icon.sprite != null)
        {
            icon.color = new Color(1, 1, 1, 1);
        }
        else
        {
            icon.color = new Color(1, 1, 1, 0);
        }
    }

    public static void SetSpriteByUniGroup(UniGroup group, Image icon)
    {
        //临时
        Texture2D tex = new Texture2D((int)1, 1);
        if (group.TryGetComponent<UniUseComponent>(out var useComp))
        {
            tex.LoadImage(useComp.captureData);

            icon.sprite = Sprite.Create(tex, new Rect(Vector2.zero, AppConst.UniGroupCaptureSize), Vector2.one * 0.5f);
        }
    }
    public static GameObject WaiterView;
    public static void ShowWaitingMask(bool show)
    {
        if (WaiterView == null&&show)
        {
            WaiterView = UniMain.AssetModule.SyncLoad<GameObject>("prefabs/ui/ui_rpcwait.unity3d");
            if (WaiterView)
            {
                WaiterView = GameObject.Instantiate(WaiterView);
            }
        }
        if (WaiterView)
        {
            WaiterView.SetActive(show);
        }
    }
    
```

类继承自 `Singleton<UIHelper>`，用于在 Unity 中管理和操作各种 UI 元素。该类包含多个字段和方法，用于处理 UI 的初始化、加载、显示、隐藏、布局更新等功能。

首先，类中定义了一个私有方法 `LoadUIConfig`，用于加载 UI 配置。该方法通过将 UI 名称映射到对应的路径来初始化 `UIPathDic` 字典，并通过将 UI 名称映射到对应的工厂方法来初始化 `UIFactory` 字典。这样可以方便地根据 UI 名称获取对应的路径和实例化方法。

类中还定义了几个公共字段和属性，包括 `FirstUI`、`UIFactory`、`UIPool`、`UIPathDic`、`dialog`、`gameLoading`、`messagePopup`、`toastParent`、`GizmosMgr`、`ToastParent`、`uiParent`、`ScreenWidth`、`ScreenHeight`、`Logger`、`hudCanvas` 和 `HudCanvas`。这些字段和属性用于存储 UI 的初始界面、工厂方法、缓存池、路径字典、对话框、加载界面、消息弹窗、提示父对象、Gizmos 管理器、提示父对象属性、UI 父对象、屏幕宽度、高度、日志记录器、HUD 画布和 HUD 画布属性等信息。

`Init` 方法用于初始化 `UIHelper` 类。该方法首先检查 `UIPool` 是否为空，如果为空则初始化 `UIPathDic`、`UIPool` 和 `UIFactory` 字典，并将 `uiParent` 设置为 `UISystem.Inst.gameObject.transform`。然后调用 `LoadUIConfig` 方法加载 UI 配置，并订阅场景编辑类型变化事件。

`CreateUI` 方法用于创建 UI 实例。该方法首先检查 `UIFactory` 是否包含指定的 UI 名称，如果包含则调用对应的工厂方法创建 UI 实例，否则记录未注册的 UI 名称。

`LoadUI` 方法是一个异步方法，用于加载 UI 预制件并初始化 UI 实例。该方法首先调用 `LoadUIPrefab` 方法加载 UI 预制件，然后调用 `baseUI.OnInit` 方法初始化 UI 实例，并捕获和记录可能的异常。

`GetCornerScreenPos` 方法用于获取 UI 元素的屏幕位置。该方法首先获取 UI 元素的四个角的世界坐标，然后根据画布的渲染模式将世界坐标转换为屏幕坐标，并返回指定角的屏幕坐标。

`ShowToast` 方法是一个异步方法，用于显示提示信息。该方法首先检查是否已有提示信息正在显示，如果有则销毁当前提示信息。然后调用 `LoadUIPrefab` 方法加载提示信息的预制件，并设置其位置、缩放和文本内容。如果指定了持续时间，则设置提示信息的销毁时间。

`OnSceneEditTypeChange` 方法用于处理场景编辑类型变化事件。如果当前为编辑模式且有提示信息正在显示，则销毁提示信息。

`CheckWaringUI` 方法用于检查和初始化提示父对象。该方法首先检查 `toastParent` 是否为空，如果为空则创建新的提示父对象并设置其属性。然后检查提示画布的世界相机是否为空，如果为空则设置为 UI 相机。

`CheckHudCanvasUI` 方法用于检查和初始化 HUD 画布。该方法首先检查 `hudCanvas` 是否为空，如果为空则创建新的 HUD 画布并设置其属性。

`ShowSingleBtnDialog` 和 `ShowDoubleBtnDialog` 方法用于显示单按钮和双按钮对话框。方法首先调用 `CheckDialogUI` 方法检查和初始化对话框，然后调用 `ShowDialog` 方法显示对话框，并设置对话框的内容和按钮事件。

`ShowGameLoading` 和 `HideGameLoading` 方法用于显示和隐藏游戏加载界面。`ShowGameLoading` 方法首先检查 `gameLoading` 是否为空，如果为空则加载并实例化游戏加载界面，并设置其位置和缩放。然后显示游戏加载界面。`HideGameLoading` 方法用于隐藏游戏加载界面。

`ShowMessagePopup` 方法用于显示消息弹窗。方法首先调用 `CheckMessagePopupUI` 方法检查和初始化消息弹窗，然后调用 `ShowMessage` 方法显示消息弹窗，并设置消息弹窗的内容和按钮事件。

`CheckDialogUI` 方法用于检查和初始化对话框。方法首先检查 `dialog` 是否为空，如果为空则加载并实例化对话框，并设置其属性。然后隐藏消息弹窗并显示对话框。

`OpenQuickAssetSelector` 和 `OpenCommonAssetPopup` 方法用于打开快捷素材选择窗口和通用素材库窗口。方法根据传入的参数调用 `UISystem.Inst.ShowUIScene` 方法显示对应的 UI 界面。

`CheckMessagePopupUI` 方法用于检查和初始化消息弹窗。方法首先检查 `dialog` 是否为空，如果为空则调用 `CheckDialogUI` 方法初始化对话框。然后隐藏对话框并显示消息弹窗。

`LoadUIPrefab` 方法是一个异步方法，用于加载 UI 预制件。方法调用 `UniMain.AssetModule.InstantiateAsync` 方法加载并实例化 UI 预制件，并返回实例化的游戏对象。

`LoadUIPrefab` 方法的重载版本用于批量加载 UI 预制件。方法根据传入的 UI 名称列表构建路径列表，然后调用 `UniMain.AssetModule.LoadAssets` 方法加载 UI 预制件，并通过回调函数返回加载结果。

`LoadPrefab` 方法是一个异步方法，用于加载预制件。方法调用 `UniMain.AssetModule.InstantiateAsync` 方法加载并实例化预制件，并返回实例化的游戏对象。

`Dispose` 方法用于释放 `UIHelper` 类的资源。方法首先调用基类的 `Dispose` 方法，然后清空 `UIFactory` 和 `UIPathDic` 字典，并释放 `GizmosMgr` 资源。

`ClearAllUIPool` 方法用于清理 UI 缓存池。方法遍历 `UIPool` 字典，调用每个 UI 实例的 `OnDestroy` 方法销毁 UI 实例，并清空 `UIPool` 字典。

`SetSpriteSimple` 和 `SetSpriteSimplePlayBag` 方法用于设置 UI 图标的精灵。方法根据传入的参数构建图片下载路径，并调用 `DownloadImg` 组件下载图片。下载完成后设置图标的精灵和颜色。

`SetSpriteByUniGroup` 方法用于根据 `UniGroup` 设置 UI 图标的精灵。方法从 `UniGroup` 组件中获取图片数据，并创建精灵设置到图标上。

`ShowWaitingMask` 方法用于显示或隐藏等待遮罩。方法首先检查 `WaiterView` 是否为空，如果为空则加载并实例化等待遮罩。然后根据传入的参数设置等待遮罩的显示状态。