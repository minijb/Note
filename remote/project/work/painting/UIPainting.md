


`UIPainting` 类中的代码片段展示了如何处理画布上的触摸和手势操作。该类继承自 `MonoBehaviour`，并实现了多个方法来管理和处理用户在画布上的交互。

首先，`OnPointDownCanvas` 方法在用户按下画布时调用。它关闭所有场景，并启动一个协程 `ReadyAbsorbStatus`，传递按下的位置作为参数。`OnPointUpCanvas` 方法在用户抬起手指时调用。如果当前正在绘制，则将 `canvasPixel.IsDrawing` 设置为 `false`。根据当前的绘制状态，方法会处理不同的绘制操作，例如矩形、圆形和其他形状。它还会应用颜色并创建覆盖层。

**绘制在 canvas 上**

`OnPointClickCanvas` 方法在用户点击画布时调用。如果当前的绘制状态是填充桶（Bucket），则调用 `DrawWtihPoint` 方法在指定位置绘制。否则，调用 `UpdateData` 方法更新数据，并调用 `OnPointUpCanvas` 方法处理抬起操作。

`OpenOverLayer` 方法用于打开或关闭覆盖层。当打开覆盖层时，它设置覆盖层的各种属性，并将触摸事件处理器 `mainTouch` 的目标设置为覆盖层的 `RectTransform`。当关闭覆盖层时，它恢复触摸事件处理器的目标为基础画布，并禁用旋转和平移功能。

`OnOpen` 方法在打开画布时调用。它初始化各种参数和组件，包括颜色调色板、滑块和切换按钮。它还设置触摸事件处理器 `mainTouch` 的各种事件处理方法，例如 `OnPinchDown`、`OnPinchUp`、`OnPinchClick` 和 `OnPinchOnDrag`。

`OnClose` 方法在关闭画布时调用。它清理各种资源和订阅，并移除触摸事件处理器的事件处理方法。它还上传统计数据，并处理 GIF 画布列表的清理工作。

总体来说，这段代码展示了如何在 Unity 中处理画布上的触摸和手势操作，包括按下、抬起、点击、平移、缩放和旋转等操作。通过这些方法，可以方便地在画布上进行绘制和编辑，提高用户交互体验。


```c#
public class UIPainting : UIBase<UIPaintingRef, UIPaintingModel>
    {
        public List<UniNodeRefInfo> RefList = new List<UniNodeRefInfo>();
        private CanvasPixelInfo canvasPixel;
        //private CanvasModel canvasInfo;
        private CanvasLayers canvasInfos;
        public Vector2Int resolution;   //原始图的大小

        private RectTransform thisRect
        {
            get
            {
                return  canvasInfos.LayerRawImage ? canvasInfos.LayerRawImage.rectTransform:this.UIRef.raw_CanvasImage.rectTransform;
            }
        }
        private Vector2 pixelSize;
        private Vector2Int lastPoint;
        private PaintingTouch mainTouch;
        private Int64 enterTime;
        private IDisposable ViewSubscription;
        private IDisposable eventDownLoadPic;
        private bool curIsShare = false;
        UniLogger Logger = UniLogManager.Get<UIPainting>();
        public override FormShowType ShowType { get => FormShowType.First; set { } }
        //public override bool Blur => true;
        public int cacheQuality = -1;

        public override void OnInit()
        {
            #region 绑定相关
            //
            this.Model.PenBarActive.BindingActive(this.UIRef.pen);
            this.Model.EraserBarActive.BindingActive(this.UIRef.Eraser);
            this.Model.ShapeBarActive.BindingActive(this.UIRef.Shape);
            this.Model.LassoBarActive.BindingActive(this.UIRef.Lasso);
            this.Model.ExtendsBarActive.BindingActive(this.UIRef.Extends);
            this.Model.RedoActive.BindingActive(this.UIRef.btn_nextStep.transform);
            this.Model.UndoActive.BindingActive(this.UIRef.btn_PreviousStep.transform);

            this.Model.BottomActive.BindingActive(this.UIRef.Bottom);
            this.Model.RightActive.BindingActive(this.UIRef.Right);

            this.Model.ColorCurDiskActive.BindingActive(this.UIRef.ColorDisk.transform);
            this.Model.ColorDiskActive.BindingActive(this.UIRef.ColorDisk.transform);
            this.Model.CanvasOverLayerActive.BindingActive(this.UIRef.rect_CanvasOverLayer.transform);

            this.Model.AnimActive.BindingActive(this.UIRef.Anim.transform);
            this.Model.AnimBottomActive.BindingActive(this.UIRef.AnimBottom.transform);
            this.Model.SettingInspector.BindingActive(this.UIRef.SettingInspector.transform);
            this.Model.ProprtyActive.BindingActive(this.UIRef.Proprty.transform);

            this.Model.PreviousFrame.BindingActive(this.UIRef.btn_previousFrame.transform);
            this.Model.NextFrame.BindingActive(this.UIRef.btn_nextStep.transform);
            this.Model.CopyFrame.BindingActive(this.UIRef.btn_CopyFrame.transform);
            this.Model.AddFrame.BindingActive(this.UIRef.btn_AddFrame.transform);
            this.Model.DelFrame.BindingActive(this.UIRef.btn_DelFrame.transform);
            #endregion

            #region 组件初始化和 监听相关
            this.UIRef.slider_PenSize.onValueChanged.AddListener((v) =>
            {
                if (canvasInfos != null && canvasPixel != null)
                {
                    if (canvasPixel.BrushType == BrushType.SquarePixel)
                    {

                        this.UIRef.slider_PenSize.minValue = 0;
                        this.UIRef.slider_PenSize.maxValue = Mathf.Log(canvasInfos.Size / 8, 2);
                        SetDrawSize((int)Mathf.Pow(2, Mathf.RoundToInt(v)));
                        //if (!Mathf.Approximately(Mathf.Pow(2,v), canvasPixel.Size))
                        //{
                        //    this.UIRef.slider_PenSize.value = canvasPixel.Size;
                        //}
                    }
                    else
                    {
                        this.UIRef.slider_PenSize.minValue = 1;
                        this.UIRef.slider_PenSize.maxValue = canvasInfos.Size / 8;
                        SetDrawSize(Mathf.FloorToInt(v));
                        //if (!Mathf.Approximately(v, canvasPixel.Size))
                        //{
                        //    this.UIRef.slider_PenSize.value = canvasPixel.Size;
                        //}
                    }
                    this.UIRef.txt_PenSizeNum.text = canvasPixel.Size.ToString();
                    //CloseAllScend();
                }
            });
            this.UIRef.slider_Eraser.onValueChanged.AddListener((v) =>
            {
                if (canvasInfos != null && canvasPixel != null)
                {
                    if (canvasPixel != null && canvasPixel.BrushType == BrushType.SquarePixel)
                    {

                        this.UIRef.slider_Eraser.minValue = 0;
                        this.UIRef.slider_Eraser.maxValue = Mathf.Log(canvasInfos.Size / 8, 2);
                        SetDrawSize((int)Mathf.Pow(2, Mathf.RoundToInt(v)));
                        //if (!Mathf.Approximately(Mathf.Pow(2,v), canvasPixel.Size))
                        //{
                        //    this.UIRef.slider_PenSize.value = canvasPixel.Size;
                        //}
                    }
                    else
                    {
                        this.UIRef.slider_Eraser.minValue = 1;
                        this.UIRef.slider_Eraser.maxValue = canvasInfos.Size / 8;
                        SetDrawSize(Mathf.FloorToInt(v));
                        //if (!Mathf.Approximately(v, canvasPixel.Size))
                        //{
                        //    this.UIRef.slider_Eraser.value = canvasPixel.Size;
                        //}
                    }
                    this.UIRef.txt_EraserSizeNum.text = canvasPixel.Size.ToString();
                    // CloseAllScend();
                }
            });

            this.UIRef.tog_Rectangle.onValueChanged.AddListener((b) =>
            {
                if (b && canvasPixel != null)
                {
                    PreChangeTools();
                    canvasPixel.BrushType = BrushType.SquarePixel;
                    canvasPixel.CurPaintSatus = PaintSatus.Draw;

                    this.UIRef.slider_PenSize.value = canvasPixel.BrushType != BrushType.SquarePixel ? canvasPixel.Size : Mathf.Log(canvasPixel.Size, 2);

                    CloseAllScend();
                }
            });
            this.UIRef.tog_Circle.onValueChanged.AddListener((b) =>
            {
                if (b && canvasPixel != null)
                {
                    PreChangeTools();
                    canvasPixel.BrushType = BrushType.CircleCenter;
                    canvasPixel.CurPaintSatus = PaintSatus.Draw;
                    CloseAllScend();
                }
            });
            this.UIRef.tog_pen.onValueChanged.AddListener((b) =>
            {
                if (b && canvasPixel != null)
                {
                    PreChangeTools();
                    if (!this.Model.PenBarActive.Value)
                    {
                        this.Model.PenBarChange();
                        this.UIRef.pen.GetComponent<ToggleGroup>().GetFirstActiveToggle()?.onValueChanged.Invoke(true);
                    }
                    this.Model.PenBarChange();
                    this.UIRef.slider_PenSize.value = canvasPixel.BrushType != BrushType.SquarePixel ? canvasPixel.Size : Mathf.Log(canvasPixel.Size, 2);
                }
            });

            this.UIRef.tog_Eraser.onValueChanged.AddListener((b) =>
            {
                if (b && canvasPixel != null)
                {
                    PreChangeTools();
                    var oldValue = this.Model.EraserBarActive.Value;
                    CloseAllScend();
                    this.Model.EraserBarActive.Value = oldValue;
                    this.Model.PeErasernBarChange();

                    this.UIRef.slider_Eraser.value = canvasPixel.BrushType != BrushType.SquarePixel ? canvasPixel.Size : Mathf.Log(canvasPixel.Size, 2);
                    canvasPixel.CurPaintSatus = PaintSatus.Eraser;
                }
            });
            this.UIRef.tog_Bucket.onValueChanged.AddListener((b) =>
            {
                if (b && canvasPixel != null)
                {
                    PreChangeTools();
                    canvasPixel.CurPaintSatus = PaintSatus.Bucket;
                    CloseAllScend();
                }
            });

            this.UIRef.tog_LIne.onValueChanged.AddListener((b) =>
            {
                if (b && canvasPixel != null)
                {
                    PreChangeTools();
                    canvasPixel.CurPaintSatus = PaintSatus.Line;
                    CloseAllScend();
                }
            });
            this.UIRef.tog_OutRectangle.onValueChanged.AddListener((b) =>
            {
                if (b && canvasPixel != null)
                {
                    PreChangeTools();
                    canvasPixel.CurPaintSatus = PaintSatus.OutlinedRectangle;
                    CloseAllScend();
                }
            });
            this.UIRef.tog_ShapeRectangle.onValueChanged.AddListener((b) =>
            {
                if (b && canvasPixel != null)
                {
                    PreChangeTools();
                    canvasPixel.CurPaintSatus = PaintSatus.Rectangle;
                    CloseAllScend();
                }
            });
            this.UIRef.tog_ShapeCircle.onValueChanged.AddListener((b) =>
            {
                if (b && canvasPixel != null)
                {
                    PreChangeTools();
                    canvasPixel.CurPaintSatus = PaintSatus.Circle;
                    CloseAllScend();
                }
            });
            this.UIRef.tog_Ring.onValueChanged.AddListener((b) =>
            {
                if (b && canvasPixel != null)
                {
                    PreChangeTools();
                    canvasPixel.CurPaintSatus = PaintSatus.Ring;
                    CloseAllScend();
                }
            });
            this.UIRef.tog_Shape.onValueChanged.AddListener((b) =>
            {
                if (b)
                {
                    PreChangeTools();
                    if (!this.Model.ShapeBarActive.Value)
                    {
                        this.Model.ShapeBarChange();
                        this.UIRef.Shape.GetComponent<ToggleGroup>().GetFirstActiveToggle()?.onValueChanged.Invoke(true);
                    }
                    this.Model.ShapeBarChange();
                }
            });
            this.UIRef.tog_Lasso.onValueChanged.AddListener((b) =>
            {
                if (b)
                {
                    PreChangeTools();
                    if (!this.Model.LassoBarActive.Value)
                    {
                        this.Model.LassoBarChange();
                        this.UIRef.Lasso.GetComponent<ToggleGroup>().GetFirstActiveToggle()?.onValueChanged.Invoke(true);
                    }
                    this.Model.LassoBarChange();
                }
            });
            this.UIRef.tog_extends.onValueChanged.AddListener((b) =>
            {
                if (b)
                {
                    PreChangeTools();
                    //if (!this.Model.ExtendsBarActive.Value)
                    //{
                    //    this.Model.ExtendsBarChange();
                    //    //this.UIRef.Extends.GetComponent<ToggleGroup>().GetFirstActiveToggle()?.onValueChanged.Invoke(true);
                    //}
                    this.UIRef.image_Absorb.gameObject.SetActive(false);
                    this.Model.ExtendsBarChange();
                }
                else
                {
                    this.UIRef.tog_choosepic.isOn = false;
                    this.UIRef.tog_download.isOn = false;
                    this.UIRef.tog_share.isOn = false;
                }
            });
            this.UIRef.tog_boxselect.onValueChanged.AddListener((b) =>
            {
                if (b && canvasPixel != null)
                {
                    PreChangeTools();
                    this.UIRef.image_Absorb.gameObject.SetActive(false);
                    canvasPixel.CurPaintSatus = PaintSatus.LassoRectangle;
                    CloseAllScend();
                }
            });
            this.UIRef.tog_circleselect.onValueChanged.AddListener((b) =>
            {
                if (b && canvasPixel != null)
                {
                    PreChangeTools();
                    PreChangeTools();
                    this.UIRef.image_Absorb.gameObject.SetActive(false);
                    canvasPixel.CurPaintSatus = PaintSatus.LassoCircle;
                    CloseAllScend();
                }
            });
            this.UIRef.tog_magicstick.onValueChanged.AddListener((b) =>
            {
                if (b && canvasPixel != null)
                {
                    PreChangeTools();
                    PreChangeTools();
                    this.UIRef.image_Absorb.gameObject.SetActive(false);
                    canvasPixel.CurPaintSatus = PaintSatus.LassoMagic;
                    CloseAllScend();
                }
            });
            //this.UIRef.tog_colour.onValueChanged.AddListener((b) =>
            //{
            //    this.Model.ColorDiskActive.Value = b;
            //    if (b)
            //    {
            //        RefreshScroll();
            //    }
            //});

            this.UIRef.btn_PreviousStep.onClick.AddListener(() =>
            {
                CloseAllScend();
                if (canvasInfos != null)
                {
                    canvasInfos.Undo();
                    this.Model.RedoUndo(canvasInfos);
                }
            });
            this.UIRef.btn_nextStep.onClick.AddListener(() =>
            {
                CloseAllScend();
                if (canvasInfos != null)
                {
                    canvasInfos.Redo();
                    this.Model.RedoUndo(canvasInfos);
                }
            });

            this.UIRef.btn_palette.onClick.RemoveAllListeners();
            this.UIRef.btn_palette.onClick.AddListener(() =>
            {
                CloseAllScend(); 
                this.Model.SwitchSimpleDisk(!this.Model.ColorCurDiskActive); 
            });
            this.UIRef.btn_CloseColorDisk.onClick.AddListener(() => this.Model.SwitchSimpleDisk(true));

            //this.UIRef.tog_Create.onValueChanged.AddListener((b) =>
            //{
            //    if (b)
            //    {
            //        SavePicture();
            //        UIHelper.Instance.ShowToast("保存成功");
            //    }
            //});
            //this.UIRef.tog_Save_Exit.onValueChanged.AddListener(async (b) =>
            //{
            //    if (b)
            //    {
            //        SavePicture();
            //        UIHelper.Instance.ShowToast("保存成功");
            //        UISystem.Inst.BackFirst();
            //    }
            //});

            bool requesting = true;

            this.UIRef.tog_more.GetComponent<EditTogMore>().InitEvent();
            this.UIRef.tog_more.GetComponent<EditTogMore>().tog_Publish.onValueChanged.RemoveAllListeners();
            this.UIRef.tog_more.GetComponent<EditTogMore>().tog_Publish.onValueChanged.AddListener((b) =>
            {
                if (b)
                {
                    CloseAllScend();

                    UnityAction<string, string, bool, PrivateEnum> publish = (name, des, isOpen, publishState) =>
                    {
                        UnityAction fail = () =>
                        {
                            OnExit();
                            UIHelper.Instance.ShowToast("save_tips1".GetLanguageStr());
                            requesting = true;
                        };
                        UnityAction success = () =>
                        {
                            OnExit();
                            UIHelper.Instance.ShowToast("txt_save_Picture".GetLanguageStr());
                            requesting = true;
                        };
                        if (!requesting)
                        {
                            return;
                        }
                        requesting = false;
                        if (workType == WorkType.GIF)
                        {
                            SavePicture(success, fail, name, des, isOpen, publishState);
                        }
                        else
                        {
                            var ret = true;
                            SavePicture(success, fail, name, des, isOpen, publishState);
                            if (!ret)
                            {
                                canvasInfos.SaveTextureColorsToCache(new UniWorkSaveContext());
                            }
                        }
                    };
                    if (workType == WorkType.GIF)
                    {
                        UISystem.Inst.ShowUIScene(UIName.BudPublish, UIName.PaintGif, PaintService.Instance.CombineCanvasLayers(gifCanvasList?.First()), publish);
                    }
                    else
                    {
                        var tex = PaintService.Instance.CombineCanvasLayers(canvasInfos);
                        if (workType == WorkType.Painting)
                        {
                            UISystem.Inst.ShowUIScene(UIName.BudPublish, UIName.Painting,tex, publish);
                        }
                        else
                        {
                            UISystem.Inst.ShowUIScene(UIName.BudPublish, UIName.PaintTexture,PaintService.Instance.ToMatTakeShot( tex), publish);
                        }
                    }
                }
                //_ = UIHelper.Instance.ShowDoubleBtnDialog("savenotice".GetLanguageStr(), "btn_confirm".GetLanguageStr(), "btn_cancel".GetLanguageStr(), async () =>
                //{
                //});
            });
            this.UIRef.tog_more.GetComponent<EditTogMore>().tog_Save_Exit.onValueChanged.RemoveAllListeners();
            this.UIRef.tog_more.GetComponent<EditTogMore>().tog_Save_Exit.onValueChanged.AddListener((b) =>
            {
                if (b)
                {
                    CloseAllScend();

                    UnityAction fail = () =>
                    {
                        OnExit();
                        UIHelper.Instance.ShowToast("save_tips1".GetLanguageStr());
                        requesting = true;
                    };
                    UnityAction success = () =>
                    {
                        OnExit();
                        UIHelper.Instance.ShowToast("txt_save_Picture".GetLanguageStr());
                        requesting = true;
                    };
                    _ = UIHelper.Instance.ShowDoubleBtnDialog("savenotice".GetLanguageStr(), "btn_confirm".GetLanguageStr(), "btn_cancel".GetLanguageStr(), async () =>
                    {
                        if (!requesting)
                        {
                            return;
                        }
                        requesting = false;

                        var defalutName = "";
                        var des = "";
                        if (UniMain.Game.Work && UniMain.Game.Work.Meta !=null)
                        {
                            defalutName = UniMain.Game.Work.Meta.Name;
                            des = UniMain.Game.Work.Meta.Description;
                        }
                        if (workType == WorkType.GIF)
                        {
                            SavePicture(success, fail, defalutName, des, false, PrivateEnum.save);
                        }
                        else
                        {
                            var ret = true;
                            SavePicture(success, fail, defalutName, des, false, PrivateEnum.save);
                            if (!ret)
                            {
                                canvasInfos.SaveTextureColorsToCache(new UniWorkSaveContext());
                            }
                        }
                    });
                }
            });

            this.UIRef.tog_choosepic.onValueChanged.AddListener((b) =>
            {
                this.Model.CloseScendBar();
                this.UIRef?.gameObject?.GetComponent<ToggleGroup>()?.SetAllTogglesOff();

                this.Model.ShowPicView(this.UIName, b);
            });

            this.UIRef.tog_share.onValueChanged.AddListener((b) =>
            {
                if (b)
                {
                    //调用分享
                    //Uni.Global.GLogger.Warn("-----------分享");
                    SavePaintingToLocal(true);
                    this.UIRef.tog_share.isOn = false;
                }
            });

            this.UIRef.tog_download.onValueChanged.AddListener((b) =>
            {
                if (b)
                {
                    //Uni.Global.GLogger.Warn("-----------下载");
                    SavePaintingToLocal();
                    this.UIRef.tog_download.isOn = false;
                }
            });

            //Bottom
            this.UIRef.btn_mirrorX.onClick.AddListener(() =>
            {
                if (this.UIRef.raw_CanvasOverLayerImage != null)
                {
                    this.UIRef.raw_CanvasOverLayerImage.transform.localScale = Vector3.Scale(this.UIRef.raw_CanvasOverLayerImage.transform.localScale, new Vector3(-1, 1, 1));
                }
            });

            this.UIRef.btn_mirrorY.onClick.AddListener(() =>
            {
                if (this.UIRef.raw_CanvasOverLayerImage != null)
                {
                    this.UIRef.raw_CanvasOverLayerImage.transform.localScale = Vector3.Scale(this.UIRef.raw_CanvasOverLayerImage.transform.localScale, new Vector3(1, -1, 1));
                }
            });
            this.UIRef.btn_copy.onClick.AddListener(() =>
            {
                if (PaintService.Instance != null && this.UIRef != null && canvasInfos.CurRawImage != null && this.UIRef.raw_CanvasOverLayerImage != null)
                {
                    canvasInfos.Colors = PaintService.Instance.CombineTexture(canvasInfos, this.UIRef.raw_CanvasOverLayerImage);
                    canvasInfos.DoRecordColor();
                    if (this.Model != null)
                    {
                        this.Model.RedoUndo(canvasInfos);
                    }
                    canvasInfos.ApplyColor();
                }
            });
            this.UIRef.btn_del.onClick.AddListener(() =>
            {
                OpenOverLayer(false);
                CloseAllScend();
                canvasInfos.DoRecordColor();
            });
            this.UIRef.btn_merge.onClick.AddListener(MergeImage);
            
            this.UIRef.btn_layer.onClick.AddListener(() =>
            {
                var status = !this.UIRef.LayerEdit.gameObject.activeSelf;
                CloseAllScend();
                this.UIRef.LayerEdit.gameObject.SetActive(status);//todo 
                if (status)
                {
                    this.UIRef.LayerEdit.GetComponent<LayerEditManager>().Refresh(canvasInfos);
                }
            });
            this.UIRef.btn_CloseLayerEditSet.onClick.AddListener(() =>
            {
                CloseAllScend();
            });
            this.UIRef.btn_CloseLayerEdit.onClick.AddListener(() =>
            {
                CloseAllScend();
                this.UIRef.LayerEdit.gameObject.SetActive(true);//todo 
            });
            //UIEventListener.Get(this.UIRef.raw_CanvasImage.gameObject).OnClickDataDown += OnPointDownCanvas;
            //UIEventListener.Get(this.UIRef.raw_CanvasImage.gameObject).OnClickDataUp += OnPointUpCanvas;
            #endregion

            GifInit();

            // if (Screen.safeArea.)
            // {
            //     (this.UIRef.Left.transform as RectTransform).anchoredPosition += Vector2.right*70;
            //     (this.UIRef.Topicon.GetChild(0).transform as RectTransform).anchoredPosition += Vector2.right*70;
            // }
        }

        public async void OnExit()
        {
            if (UniMain.Game.Scene.IsSupport2DEdit)
            {
                //await  UISystem.Inst.AsyncShowUIScene(UIName.UIEdit);
                // UIBase baseUI;
                // if (UIHelper.Instance.UIPool.TryGetValue(UIName.UIEdit, out baseUI)){
                //     var uiBud = baseUI as UIEditBudHome;
                //     uiBud?.ExitActionSelectMode();
                //     uiBud?.EnterActionSelectMode();
                // }
                UISystem.Inst.BackFirst();
            }
            else
            {
                UISystem.Inst.BackFirst();
            }
            
            if (UniMain.Game.Scene.WorkingType == WorkType.GIF || UniMain.Game.Scene.WorkingType == WorkType.Painting|| UniMain.Game.Scene.WorkingType == WorkType.Material)
            {
                UISystem.Inst.Back();
                if (UISystem.Inst.UICanvas != null)
                {
                    UISystem.Inst.UICanvas.gameObject.SetActive(false);
                    UISystem.Inst.tran_canvas_dynamic.gameObject.SetActive(false);
                }
                UISystem.Inst.ChangeGameState();
                return;
            }

            Messenger.Default.Publish(new ViewState() { uIName = workType == WorkType.GIF ? UIName.UniObjectInspector : this.UIName, isShow = false });
            // if (workType == WorkType.Material)
            // {
            //     if (Global.Game.Scene is UniEditScene editScene && editScene && editScene.Inspector)
            //     {
            //
            //         UIMaterial.UseMode = UIMaterial.Mode.Mat;
            //         var ctx = editScene.Inspector;
            //         ctx.Hide(true);
            //         var ui = (await UISystem.Inst.AsyncShowUIScene(UIName.Material)) as UIMaterial;
            //         UnityAction<bool> a = (b) =>
            //         {
            //             if (!b)
            //             {
            //                 ui.ActiveHandler.RemoveAllListeners();
            //                 ctx.Hide(false);
            //             }
            //         };
            //         ui.ActiveHandler.AddListener(a);
            //     }
            // }
        }

        private ColorPalette mColorPalette;
        WorkType workType;
        public override void OnOpen(params object[] args)
        {
            UniMain.QualityManager.StashTexturePara();

            if (Global.Game.Scene is UniEditScene editScene && editScene && editScene.Inspector && !editScene.Inspector.IsHide())
            {
                editScene.Inspector.Hide(true);
            }
            
            if (UniMain.Game.Work.Type != WorkType.GIF && UniMain.Game.Work.Type != WorkType.Painting && UniMain.Game.Work.Type != WorkType.Material)
            {
                workType = args.Length > 0 && args[0].ToString().Contains("GIF") ? WorkType.GIF :
                    args.Length > 0 && args[0].ToString().Contains("Mat") ? WorkType.Material : WorkType.Painting;
            }
            else
            {
                workType = args.Length > 0 && args[0].ToString() == "GIF" ? WorkType.GIF : UniMain.Game.Work.Type;
                RefList = UniMain.Game.Work.Meta?.ModeList ?? new List<UniNodeRefInfo>();
            }

            var timeSpan = System.DateTime.Now - new DateTime(1970, 1, 1, 0, 0, 0, 0);
            enterTime = Convert.ToInt64(timeSpan.TotalSeconds);

            Dictionary<string, object> dic = new Dictionary<string, object>
            {
                { "page_name", "model_edit" },
                { "page_element", "enter" },
                { "model_type", "picture" },
            };
            Uni.UniMain.TrackEvent.UploadStatistics(ConstValue.SHUSHU_EVENT_CLICK, () => dic);
            dic.Clear();

            //SetBlur();
            ReOpen(workType == WorkType.GIF);
            InitPaintService();
            //RefreshColor();

            mColorPalette = this.UIRef.ColorDisk.GetComponent<ColorPalette>();
            mColorPalette.TargetHueRing.RefreshColEvt.RemoveAllListeners();
            mColorPalette.TargetHueRing.RefreshColEvt.AddListener((c) =>
            {
                mColorPalette.RecColor.image.color = this.canvasPixel.CurPixelColor;
                this.canvasPixel.PixelColor = c;
                //CloseAllScend();
            });
            mColorPalette.AbsorbCol.onClick.RemoveAllListeners();
            mColorPalette.AbsorbCol.onClick.AddListener(() =>
            {
                this.UIRef.image_Absorb.gameObject.SetActive(true);
                this.UIRef.image_Absorb.color = Color.white;
                this.UIRef.image_Absorb.rectTransform.anchoredPosition = new Vector2(Screen.width / 2f, Screen.height / 2f);
                ToAbsorbStatus();
            });
            mColorPalette.CanvasPixel = canvasPixel;

            canvasPixel.SetPixelColor(Color.white);

            this.UIRef.slider_PenSize.minValue = 1;
            this.UIRef.slider_Eraser.minValue = 1;
            this.UIRef.slider_PenSize.wholeNumbers = true;
            this.UIRef.slider_Eraser.wholeNumbers = true;

            this.UIRef.tog_pen.isOn = true;
            if (!this.UIRef.tog_Circle.isOn)
            {
                this.UIRef.tog_Circle.isOn = true;
            }
            else
            {
                this.UIRef.tog_Circle.onValueChanged.Invoke(true);
            }

            canvasPixel.Size = 2;//fixdata to
            this.UIRef.slider_PenSize.onValueChanged.Invoke(canvasPixel.Size);

            var canvasRect = this.UIRef.Image_baseCanvas.GetComponent<RectTransform>();
            canvasRect.anchoredPosition = Vector2.zero;
            canvasRect.localEulerAngles = Vector2.zero;
            canvasRect.localScale = Vector3.one;


            SwitchSimpleDisk();
            this.UIRef.gameObject.GetComponent<ToggleGroup>().SetAllTogglesOff();
            this.UIRef.Uni_watermask.gameObject.SetActive(false);
            if (!this.UIRef.CanvasRoot.gameObject.TryGetComponent(out mainTouch))
            {
                mainTouch = this.UIRef.CanvasRoot.gameObject.AddComponent<PaintingTouch>();
                mainTouch.Target = this.UIRef.Image_baseCanvas.rectTransform;
            }
            mainTouch.OnPinchDown += OnPointDownCanvas;
            mainTouch.OnPinchUp += OnPointUpCanvas;
            mainTouch.OnPinchClick += OnPointClickCanvas;
            mainTouch.OnPinchOnDrag += UpdateData;
            mainTouch.OnGestureChange += OnAbsorbOver;

            this.ViewSubscription = Messenger.Default.Subscribe<ViewState>(ViewMsg);
            this.eventDownLoadPic = Messenger.Default.Subscribe<DownloadResult>(OnDownloadResult);

            //if (!SystemInfo.supportsComputeShaders || SystemInfo.gra == "PowerVR Rogue GE8320")//todo 无法显示原因
            //{
            //     UIHelper.Instance.ShowSingleBtnDialog("Painterror".GetLanguageStr());
            //}
        }
        private void MergeImage()
        {
            if (this.Model.CanvasOverLayerActive.Value && canvasInfos.CurRawImage != null && this.UIRef.raw_CanvasOverLayerImage.texture != null)
            {
                canvasInfos.Colors = PaintService.Instance.CombineTexture(canvasInfos, this.UIRef.raw_CanvasOverLayerImage);
                canvasInfos.DoRecordColor();
                this.Model.RedoUndo(canvasInfos);
                canvasInfos.DoRecordColor();
                canvasInfos.ApplyColor();
                OpenOverLayer(false);
                CloseAllScend();
            }
        }
        private void ViewMsg(ViewState msg)
        {
            if (msg.uIName == UIName.BudPic && !msg.isShow)
            {
                if (!string.IsNullOrEmpty(msg.content))
                {
                    if (UniNetworkTextureLoader.ImageUrlCheck(msg.content))
                    {
                        DownloadTexture2D(msg.content, () =>
                        {
                            if (string.IsNullOrEmpty(msg.des))
                                return;
                            var data = new UniNodeRefInfo()
                            {
                                RefId = msg.des,
                                RefVersion = 0 //只创建
                            };

                            if (RefList == null)
                            {
                                RefList = new List<UniNodeRefInfo>();
                            }
                            if (RefList != null && !(RefList.Where((d) => d.RefId == data.RefId).Count() > 0))
                            {
                                RefList.Add(data);
                                if (RefList.Count() > 100)
                                {
                                    RefList.Remove(RefList.First());
                                }
                            }
                        });
                    }

                    //默认开启 pen
                    this.UIRef.tog_Lasso.isOn = true;
                    this.Model.BottomActive.Value = true;
                }
                else
                {
                    this.UIRef.tog_pen.isOn = true;
                }
                this.Model.CloseScendBar();
            }
        }

        private void OpenOverLayer(bool open = true)
        {
            this.Model.CanvasOverLayerActive.Value = open;
            if (open)
            {
                this.UIRef.rect_CanvasOverLayer.transform.localScale = Vector3.one;
                this.UIRef.rect_CanvasOverLayer.transform.eulerAngles = Vector3.zero;
                this.UIRef.raw_CanvasOverLayerImage.transform.localScale = Vector3.one;
                this.UIRef.rect_CanvasOverLayer.GetComponent<RectTransform>().sizeDelta = canvasInfos.LayerRawImage.GetComponent<RectTransform>().sizeDelta;
                this.UIRef.rect_CanvasOverLayer.GetComponent<RectTransform>().anchoredPosition = Vector2.zero;

                mainTouch.OnPinchDown -= OnPointDownCanvas;
                mainTouch.OnPinchUp -= OnPointUpCanvas;
                mainTouch.OnPinchClick -= OnPointClickCanvas;
                mainTouch.OnPinchOnDrag -= UpdateData;
                mainTouch.OnGestureChange -= OnAbsorbOver;
                mainTouch.Target = this.UIRef.rect_CanvasOverLayer.GetComponent<RectTransform>();
                mainTouch.TargetBG = this.UIRef.rect_CanvasOverLayer.GetChild(0).GetComponent<RectTransform>();
                mainTouch.TargetBG.sizeDelta = this.UIRef.rect_CanvasOverLayer.GetComponent<RectTransform>().sizeDelta + Vector2.one * 10;
                mainTouch.CanRotate = true;
                mainTouch.CanPinchPan = true;
                mainTouch.MinZoomSize = 0.5f;
            }
            else
            {
                mainTouch.OnPinchDown += OnPointDownCanvas;
                mainTouch.OnPinchUp += OnPointUpCanvas;
                mainTouch.OnPinchClick += OnPointClickCanvas;
                mainTouch.OnPinchOnDrag += UpdateData;
                mainTouch.OnGestureChange += OnAbsorbOver;
                mainTouch.Target = this.UIRef.Image_baseCanvas.rectTransform;
                mainTouch.TargetBG = null;
                mainTouch.CanRotate = false;
                mainTouch.CanPinchPan = false;
                mainTouch.MinZoomSize = 0.5f;
                this.UIRef.raw_CanvasOverLayerImage.texture = null;
            }
        }

        private void DownloadTexture2D(string url, Action a = null)
        {
            DownloadImg.DownloadTexture2D(url, "", (tex, url) =>
            {
                if (tex)
                {
                    tex.filterMode = FilterMode.Point;
                    OpenOverLayer();
                    this.UIRef.raw_CanvasOverLayerImage.texture = tex;
                    a?.Invoke();
                }
            });
        }

        public void SwitchSimpleDisk(bool ishow = true)
        {
            if (this.Model != null)
            {
                this.Model.SwitchSimpleDisk(ishow);
                // if (ishow)
                // {
                //     if (colors != null && PaintService.Instance != null && canvasPixel != null)
                //     {
                //         int index = colors.IndexOf(PaintService.Instance.Vector4ToColor(canvasPixel.PixelColor));
                //         if (index >= 0)
                //         {
                //             RefreshColorSelected(index % COL_SIZE);
                //             RefreshScrollSelected();
                //         }
                //     }
                // }
                // else
                // {
                //     RefreshScroll();
                // }
            }
        }
        public override void Update()
        {
            //UpdateData();
        }
        public override void OnClose()
        {
            RefList.Clear();

            UniMain.QualityManager.RevertTexturePara();

            var timeSpan = System.DateTime.Now - new DateTime(1970, 1, 1, 0, 0, 0, 0);
            Int64 leftTime = Convert.ToInt64(timeSpan.TotalSeconds);
            Int64 stayTime = leftTime - enterTime;

            Dictionary<string, object> dic = new Dictionary<string, object>
            {
                { "page_name", "model_edit" },
                { "page_element", "quit" },
                { "model_type", "picture" },
                { "participate_interval", stayTime }
            };
            Uni.UniMain.TrackEvent.UploadStatistics(ConstValue.SHUSHU_EVENT_CLICK, () => dic);
            dic.Clear();

            if (mainTouch)
            {
                mainTouch.OnPinchDown -= OnPointDownCanvas;
                mainTouch.OnPinchUp -= OnPointUpCanvas;
                mainTouch.OnPinchClick -= OnPointClickCanvas;
                mainTouch.OnPinchOnDrag -= UpdateData;
                mainTouch.OnGestureChange -= OnAbsorbOver;

            }
            this.canvasInfos?.Dispose();
            this.canvasInfos = null;
            this.canvasPixel?.Dispose();
            this.canvasPixel = null;
            colors?.Clear();
            colors = null;
            this.ViewSubscription?.Dispose();
            this.eventDownLoadPic?.Dispose();
            if (UniMain.Game.Scene is UniEditScene editScene)
            {
                editScene.RenderFeatureObjectManager.ScreenCaptureDrity = false;
            }
            if (gifCanvasList != null)
            {
                foreach (var info in gifCanvasList)
                {
                    info?.Dispose();
                }
                gifCanvasList?.Clear();
                gifCanvasList = null;
            }
        }
        private void InitPaintService()
        {
            Dictionary<string, object> dic = new Dictionary<string, object>
            {
                { "page_name", "Painting" },
                { "page_element", "UniPlaneTextureCompoent" },
                { "campaign", "edit" }
            };
            Uni.UniMain.TrackEvent.UploadStatistics(ConstValue.SHUSHU_EVENT_IMPR, () => dic);
            dic.Clear();
            this.canvasPixel = new CanvasPixelInfo();
            if (workType != WorkType.GIF)
            {
                this.canvasInfos = new CanvasLayers(this.UIRef.raw_CanvasImage,workType);
                // this.canvasInfos.SelectHandler += (m) =>
                // {
                //     
                // };
                
                if (workType == WorkType.Material)
                {
                    var mMaterialDisplayEditing = this.UIRef.MaterialDisplay.GetComponent<MaterialDisplayEditing>();
                    this.UIRef.MaterialDisplay.gameObject.SetActive(true);
                    mMaterialDisplayEditing.OnOpen(this.canvasInfos,this.UIRef.raw_CanvasImage.rectTransform);
                }
                
                this.canvasInfos.Add<Canvas256Model>();
                if ((UniMain.Game.Scene.WorkingType == WorkType.Painting || UniMain.Game.Scene.WorkingType == WorkType.Material) && !string.IsNullOrEmpty(UniMain.Game.Work.Id))
                {
                    PaintService.Instance.GetWorkPicData((t) =>
                    {
                        canvasInfos.InitPaintHistory(t.GetPixels());
                        canvasInfos.ApplyColor();
                    });
                }

                AfterSwitchCanvas();
            }
            //加载图片
            //canvasInfo.Colors = PaintService.Instance.TextureToColorInfo(canvasInfo.Size, canvasInfo.Size);

            //PaintService.Instance.TextureToColorInfo(canvasInfo);

            //PaintService.Instance.UpdateColors(canvasInfo);
        }

        private void AfterSwitchCanvas()
        {
            // if (canvasInfos.CanvasTexture)
            // {
            //     this.UIRef.raw_CanvasImage.texture = canvasInfos.CanvasTexture;
            // }
            // else
            {
                //this.UIRef.raw_CanvasImage.texture = canvasInfos.CanvasTexture2D;
            }
            if (workType == WorkType.GIF)
            {
                this.UIRef.raw_CanvasImage.texture = canvasInfos.CanvasTexture2D;//todo gif图层
            }

            resolution = new Vector2Int(canvasInfos.Size, canvasInfos.Size);
            //计算一个像素占多大尺寸
            pixelSize = thisRect.rect.size / resolution;
            this.UIRef.slider_PenSize.maxValue = canvasInfos.Size / 8;
            this.UIRef.slider_Eraser.maxValue = canvasInfos.Size / 8;

            this.Model.RedoUndo(workType != WorkType.GIF || !isPlaying ? canvasInfos : null);
        }

        private void PreChangeTools()
        {
            OnAbsorbOver();
        }

        private void CloseAllScend()
        {
            if (UISystem.Inst != null)
            {
                UISystem.Inst.UntilBackToFirstUIActive();
            }
            if (this.Model != null && this.Model.BottomActive.Value)
            {
                MergeImage();
                this.Model.BottomActive.Value = false;
            }
            if (this.Model != null)
            {
                this.Model.ColorDiskActive.Value = false;
                this.Model.CloseScendBar();
            }
            if (this.UIRef != null)
            {
                this.UIRef.gameObject.GetComponent<ToggleGroup>()?.SetAllTogglesOff();
            }
            SwitchSimpleDisk();

            if (this.Model.AnimActive)
            {
                this.UIRef.tog_SetBG.isOn = false;
                this.UIRef.tog_Content.isOn = false;
            }
            
            this.UIRef.LayerSet.gameObject.SetActive(false);//todo 
            this.UIRef.LayerEdit.gameObject.SetActive(false);//todo 
            
            this.UIRef.tog_more.GetComponent<EditTogMore>().tog_more.isOn = false;
        }
        private void UpdateData(Vector2 pos)
        {
            BeginAbsorb = false;
            if (canvasPixel.CurPaintSatus == PaintSatus.Draw || canvasPixel.CurPaintSatus == PaintSatus.Eraser)
            {
                Draw(PointerDataToRelativePos(pos));
            }
            else if (canvasPixel.CurPaintSatus >= PaintSatus.Line && canvasPixel.CurPaintSatus <= PaintSatus.OutlinedRectangle)
            {
                DrawShape(PointerDataToRelativePos(pos));
            }
            else if (canvasPixel.CurPaintSatus >= PaintSatus.LassoRectangle && canvasPixel.CurPaintSatus <= PaintSatus.LassoCircle)
            {
                LassoTools(PointerDataToRelativePos(pos));
                //套索 ---->>>>  矩形 圆形 自由 魔法棒
                //抠图:新建图层 删除旧的 
                //合并图层:新图层对应 底图的像素 旋转和缩放
            }
            else if (canvasPixel.CurPaintSatus == PaintSatus.AbsorbColor)
            {
                AbsorbColor(pos);
                //吸取颜色
            }
        }
        public void SavePicture(UnityAction successCallback, UnityAction failedCallback, string name, string des,
            bool isOpen, PrivateEnum publishState = PrivateEnum.publish)
        {
            if (workType == WorkType.GIF)
            {
                if (gifCanvasList != null && gifCanvasList.Count > 0)
                    gifCanvasList.Remove(gifCanvasList.Last());

                bool isDirty = false;
                foreach (var canvasInfo in gifCanvasList)
                {
                    if (canvasInfo != null)
                    {
                        isDirty = canvasInfo.DataIsDirty && canvasInfo.CanvasInfoIsDirty();
                        if (isDirty)
                        {
                            break;
                        }
                    }
                }

                if (isDirty)
                {
                    var count = gifCanvasList.Where((info) => info != null && info.DataIsDirty).Count();
                    var data = new UniGIFDataInfo()
                    {
                        FrameRate = (int)FrameRata,
                        MaxTotalFrame = count,
                        HorizontalAmount = (int)Mathf.Min(4, count),
                        VerticalAmount = Mathf.CeilToInt((float)count / 4f)
                    };

                    if (PaintService.Instance != null)
                    {
                        PaintService.Instance.SaveGifToPng(workType, name, des, isOpen, gifCanvasList, RefList, data,
                            successCallback, failedCallback, publishState);
                    }
                    else
                    {
                        failedCallback?.Invoke();
                    }
                }
                else
                {
                    failedCallback?.Invoke();
                }
            }
            else
            {
                if (canvasInfos != null && canvasInfos.Colors != null && canvasInfos.OriginColors != null &&
                    canvasInfos.Colors != canvasInfos.OriginColors)
                {
                    if (canvasInfos.CanvasInfoIsDirty())
                    {
                        if (PaintService.Instance != null)
                        {
                            var tex = PaintService.Instance.CombineCanvasLayers(canvasInfos);
                            var matTex = workType == WorkType.Material? PaintService.Instance.ToMatTakeShot(tex): null;
                            PaintService.Instance.SaveTextureToPng(workType, name, des, isOpen,
                                tex, matTex,RefList, successCallback,
                                failedCallback, publishState);
                        }
                        else
                        {
                            failedCallback?.Invoke();
                        }
                    }
                    else
                    {
                        failedCallback?.Invoke();
                    }
                }
                else
                {
                    failedCallback?.Invoke();
                }
            }
        }
        private void SavePaintingToLocal(bool isShare = false)
        {
            curIsShare = isShare;
            this.Model.CloseScendBar();
            this.UIRef?.gameObject?.GetComponent<ToggleGroup>()?.SetAllTogglesOff();

            if (canvasInfos.Colors != canvasInfos.OriginColors)
            {
                bool isDirty = false;
                for (int i = 0; i < canvasInfos.OriginColors.Length; i++)
                {
                    if (!UniCommonTool.ColorCompare(canvasInfos.Colors[i], canvasInfos.OriginColors[i]))
                    {
                        isDirty = true;
                        break;
                    }
                }
                if (isDirty)
                {
                    //todo
                    PaintService.Instance.SaveAndSharePic(canvasInfos.CurRawImage.texture, isShare);
                }
                else
                {
                    UIHelper.Instance.ShowToast(isShare ? "txt_share_Picture_fail".GetLanguageStr() : "txt_download_Picture_fail".GetLanguageStr());
                    //Uni.Global.GLogger.Warn("无法下载，当前画板是空白的");
                    return;
                }
            }
        }


        private void OnDownloadResult(DownloadResult result)
        {
            if (result.IsSus)
            {
                //UIHelper.Instance.ShowToast("DownloadResult.Sus");
                if (!curIsShare)
                    UIHelper.Instance.ShowToast("txt_download_Picture_success".GetLanguageStr());
            }
        }

        #region 绘画相关
        Coroutine absorbCor;
        private void OnPointDownCanvas(Vector2 pos)
        {
            CloseAllScend();
            absorbCor = this.UIRef.StartCoroutine(ReadyAbsorbStatus(pos));
        }
        private void OnPointUpCanvas(Vector2 pos)
        {
            if (canvasPixel.IsDrawing)
            {
                canvasPixel.IsDrawing = false;
                if (canvasPixel.CurPaintSatus >= PaintSatus.LassoRectangle && canvasPixel.CurPaintSatus <= PaintSatus.Lasso)
                {
                    if (startPoint != lastPoint)
                    {
                        canvasInfos.Colors = canvasInfos.GetPixels(preColors);
                        Color[] colors;
                        int sizeX = 0, sizeY = 0, offesX = 0, offesY = 0;
                        Vector2 point = Vector2.zero;
                        if (canvasPixel.CurPaintSatus == PaintSatus.LassoCircle)
                        {
                            sizeX = Mathf.Abs(lastPoint.x - startPoint.x) + 1;
                            sizeY = Mathf.Abs(lastPoint.y - startPoint.y) + 1;
                            colors = CollectCircleCenter(canvasInfos.CurSelectModel, (startPoint + lastPoint) / 2, sizeX, sizeY, out point);
                        }
                        else/* if (canvasPixel.CurPaintSatus == PaintSatus.Ring)*/
                        {
                            offesX = lastPoint.x - startPoint.x;
                            offesY = lastPoint.y - startPoint.y;

                            sizeX = (int)(offesX + 1);
                            sizeY = (int)(offesY + 1);

                            colors = CollectSquareFramePixel(canvasInfos.CurSelectModel, startPoint, sizeX, sizeY);

                            point = new Vector2((float)((startPoint + lastPoint).x + 1f) / 2f, (float)((startPoint + lastPoint).y + 1f) / 2f);
                            point += offesX < 0 ? Vector2.right : Vector2.zero;
                            point += offesY < 0 ? Vector2.up : Vector2.zero;
                        }
                        canvasInfos.ApplyColor();

                        CreateOverLayer(colors, sizeY, sizeX, point);
                    }
                }
                else
                {
                    canvasInfos.DoRecordColor();
                    this.Model.RedoUndo(canvasInfos);
                }
            }

            OnAbsorbOver();

            if (this.canvasPixel.CurPaintSatus == PaintSatus.LassoMagic)
            {
                var colors = MagicCollectAndModifyOrigin(out int h, out int w, PointerDataToRelativePos(pos), out Vector2Int centerPoint);
                CreateOverLayer(colors, h, w, centerPoint);
            }
        }
        private void CreateOverLayer(Color[] colors, int height, int width, Vector2 centerPoint)
        {
            if (colors != null && colors.Length > 0)
            {
                OpenOverLayer();
                var rect = this.UIRef.rect_CanvasOverLayer.GetComponent<RectTransform>();
                this.UIRef.rect_CanvasOverLayer.GetComponent<RectTransform>().sizeDelta = new Vector2(Mathf.Abs(width) * rect.sizeDelta.x / canvasInfos.Size, Mathf.Abs(height) * rect.sizeDelta.y / canvasInfos.Size);
                this.UIRef.rect_CanvasOverLayer.GetComponent<RectTransform>().anchoredPosition = PixelPosToScreenPoint(centerPoint);
                mainTouch.TargetBG.sizeDelta = this.UIRef.rect_CanvasOverLayer.GetComponent<RectTransform>().sizeDelta + Vector2.one * 10;
                this.Model.BottomActive.Value = true;
                this.UIRef.raw_CanvasOverLayerImage.texture = PaintService.Instance.SpawnCapture(Mathf.Abs(width), Mathf.Abs(height), colors);
            }
        }
        private void OnPointClickCanvas(Vector2 pos)
        {
            if (canvasPixel.CurPaintSatus == PaintSatus.Bucket)
            {
                DrawWtihPoint(PointerDataToRelativePos(pos));
            }
            else
            {
                UpdateData(pos);
            }
            OnPointUpCanvas(pos);
        }

        private void OnAbsorbOver()
        {
            if (this.canvasPixel.CurPaintSatus == PaintSatus.AbsorbColor)
            {
                if (absorbCor != null)
                {
                    this.UIRef.StopCoroutine(absorbCor);
                    absorbCor = null;
                }
                this.UIRef.image_Absorb.gameObject.SetActive(false);
                this.canvasPixel.CurPaintSatus = absorbLastSatus;
            }
            BeginAbsorb = false;
        }
        public void SetDrawSize(int size)
        {
            if (Mathf.Approximately(size, canvasPixel.Size))
                return;
            //if (canvasPixel.BrushType == BrushType.SquarePixel) 
            //{
            //    var max = canvasInfo.Size / 8;
            //    Uni.Global.GLogger.Info(Mathf.Log(max, 2) * ((float)size / (float)max) );
            //    size = (int)Mathf.Pow(2, Mathf.RoundToInt( Mathf.Log(max, 2) * ((float)size / (float)max)));
            //}
            canvasPixel.Size = size;
        }
        public void Undo()
        {
            canvasInfos.Undo();
        }
        public void Redo()
        {
            canvasInfos.Redo();
        }

        private Vector2Int startPoint;
        private void Draw(Vector2Int newPoint)
        {
            //只处理在框内的
            if (newPoint.x < 0 || newPoint.x >= resolution.x || newPoint.y < 0 || newPoint.y >= resolution.y)
                return;
            if (!canvasPixel.IsDrawing)
            {
                canvasPixel.IsDrawing = true;
                if (canvasPixel.BrushType == BrushType.SquarePixel)
                {
                    newPoint = RasterizePoint(newPoint, canvasPixel.Size);
                }
                SetTexturePixels(newPoint);
                //texture.SetPixels(newPoint.x, newPoint.y, Size, Size, penColors);
                //texture.SetPixel(newPoint.x, newPoint.y, penColor);
                canvasInfos.ApplyColor();

                //Graphics.Blit(texture, renderTexture, mat);

                lastPoint = newPoint;
                return;
            }

            //如果移动一段距离了，就划线
            if (newPoint != lastPoint)
            {
                List<Vector2Int> points = DrawLineFrom(lastPoint, newPoint);

                if (points.Count > 0)
                {
                    for (int i = 0; i < points.Count; i++)
                    {
                        SetTexturePixels(points[i]);
                        //texture.SetPixels(p.x, p.y, Size, Size, penColors);
                        //texture.SetPixel(p.x, p.y, penColor);
                    }
                    canvasInfos.ApplyColor();
                    lastPoint = newPoint;
                }
            }
        }
        //单点绘画
        private void DrawWtihPoint(Vector2Int newPoint)
        {
            //只处理在框内的
            if (newPoint.x < 0 || newPoint.x >= resolution.x || newPoint.y < 0 || newPoint.y >= resolution.y)
                return;
            if (!canvasPixel.IsDrawing)
            {
                canvasPixel.IsDrawing = true;
                this.UIRef.StartCoroutine(PaintBucket(newPoint, canvasPixel.PixelColor));
            }
        }

        private Color[] preColors;
        private void DrawShape(Vector2Int newPoint)
        {
            //只处理在框内的
            if (newPoint.x < 0 || newPoint.x >= resolution.x || newPoint.y < 0 || newPoint.y >= resolution.y)
                return;
            if (!canvasPixel.IsDrawing)
            {
                canvasPixel.IsDrawing = true;
                preColors = canvasInfos.GetPixels();

                if (canvasPixel.CurPaintSatus == PaintSatus.Line)
                {
                    newPoint = RasterizePoint(newPoint, canvasPixel.Size);
                    SetTexturePixels(newPoint);
                    canvasInfos.ApplyColor();
                }
                //texture.SetPixels(newPoint.x, newPoint.y, Size, Size, penColors);
                //texture.SetPixel(newPoint.x, newPoint.y, penColor);
                lastPoint = newPoint;
                startPoint = newPoint;
            }

            if (startPoint != newPoint && newPoint != lastPoint)
            {
                //todo优化
                bool setPixels = false;
                canvasInfos.Colors = canvasInfos.GetPixels(preColors);
                List<Vector2Int> points;

                if (canvasPixel.CurPaintSatus == PaintSatus.Line)
                {
                    points = DrawLineFrom(startPoint, newPoint);
                    setPixels = true;

                }
                else if (canvasPixel.CurPaintSatus == PaintSatus.Circle)
                {
                    points = DrawCircleCenter((startPoint + newPoint) / 2, Mathf.Abs(newPoint.x - startPoint.x) + 1, Mathf.Abs(newPoint.y - startPoint.y) + 1);
                }
                else if (canvasPixel.CurPaintSatus == PaintSatus.Rectangle)
                {
                    float offesX = newPoint.x - startPoint.x;
                    float offesY = newPoint.y - startPoint.y;
                    points = DrawSquareFramePixel(RasterizePoint(startPoint, canvasPixel.Size), (int)(Mathf.Sign(offesX) * (Mathf.Abs(offesX) + 1)), (int)(Mathf.Sign(offesY) * (Mathf.Abs(offesY) + 1)));
                    //points = DrawSquareFramePixel(RasterizePoint(startPoint, canvasPixel.Size), Mathf.Abs(newPoint.x - startPoint.x) + 1, Mathf.Abs(newPoint.y - startPoint.y) + 1);
                    // points = DrawSquarePixel((startPoint + newPoint) / 2, Mathf.Abs(newPoint.x - startPoint.x) + 1, Mathf.Abs(newPoint.y - startPoint.y) + 1);
                }
                else if (canvasPixel.CurPaintSatus == PaintSatus.Ring)
                {
                    if (canvasPixel.BrushType == BrushType.CircleCenter)
                    {
                        points = DrawCircleCenter((startPoint + newPoint) / 2, Mathf.Abs(newPoint.x - startPoint.x) + 1, Mathf.Abs(newPoint.y - startPoint.y) + 1, canvasPixel.Size);
                    }
                    else
                    {
                        points = DrawCircleCenter(RasterizePoint((startPoint + newPoint) / 2, canvasPixel.Size), Mathf.Abs(newPoint.x - startPoint.x) + 1, Mathf.Abs(newPoint.y - startPoint.y) + 1, 1);
                        setPixels = true;
                    }
                }
                else/*(canvasPixel.CurPaintSatus == PaintSatus.OutlinedRectangle)*/
                {
                    float offesX = newPoint.x - startPoint.x;
                    float offesY = newPoint.y - startPoint.y;
                    if (canvasPixel.BrushType == BrushType.CircleCenter)
                    {
                        points = DrawSquareFramePixel(startPoint, (int)(offesX + 1), (int)(offesY + 1), 1);
                    }
                    else
                    {
                        points = DrawSquareFramePixel(RasterizePoint(startPoint, canvasPixel.Size), (int)(offesX + 1), (int)(offesY + 1), 1);
                        //points = DrawSquarePixel(RasterizePoint((startPoint + newPoint) / 2, canvasPixel.Size), Mathf.Abs(newPoint.x - startPoint.x) + 1, Mathf.Abs(newPoint.y - startPoint.y) + 1, 1);
                    }
                    setPixels = true;
                }

                if (points.Count > 0)
                {
                    for (int i = 0; i < points.Count; i++)
                    {
                        if (setPixels)
                        {
                            if (canvasPixel.BrushType == BrushType.SquarePixel)
                            {
                                var prePoint = RasterizePoint(points[i], canvasPixel.Size);
                                SetTexturePixels(prePoint);
                            }
                            else
                            {
                                SetTexturePixels(points[i]);
                            }
                        }
                        else
                        {
                            canvasInfos.SetPixel(points[i].x, points[i].y, canvasPixel.PixelColor);
                        }
                    }
                    canvasInfos.ApplyColor();
                    lastPoint = newPoint;
                }

            }
        }
        private void LassoTools(Vector2Int newPoint)
        {
            //只处理在框内的
            if (newPoint.x < 0 || newPoint.x >= resolution.x || newPoint.y < 0 || newPoint.y >= resolution.y)
                return;

            //if (canvasPixel.CurPaintSatus == PaintSatus.LassoMagic)
            //{
            //   var points = MagicCollect(newPoint);
            //    if (points.Count > 0)
            //    {
            //        for (int i = 0; i < points.Count; i++)
            //        {
            //            canvasInfo.SetPixel(points[i].x, points[i].y, canvasPixel.PixelColor);
            //        }
            //        canvasInfo.ApplyColor();
            //    }
            //}
            //else
            {
                List<Vector2Int> points;
                if (!canvasPixel.IsDrawing)
                {
                    canvasPixel.IsDrawing = true;
                    preColors = canvasInfos.GetPixels();

                    lastPoint = newPoint;
                    startPoint = newPoint;
                }

                if (startPoint != newPoint && newPoint != lastPoint)
                {
                    canvasInfos.Colors = canvasInfos.GetPixels(preColors);

                    if (canvasPixel.CurPaintSatus == PaintSatus.LassoCircle)
                    {
                        points = DrawCircleCenter((startPoint + newPoint) / 2, Mathf.Abs(newPoint.x - startPoint.x) + 1, Mathf.Abs(newPoint.y - startPoint.y) + 1, 1);
                    }
                    else/* if (canvasPixel.CurPaintSatus == PaintSatus.Ring)*/
                    {
                        float offesX = newPoint.x - startPoint.x;
                        float offesY = newPoint.y - startPoint.y;

                        points = DrawSquareFramePixel(startPoint, (int)(Mathf.Sign(offesX) * (Mathf.Abs(offesX) + 1)), (int)(Mathf.Sign(offesY) * (Mathf.Abs(offesY) + 1)), 1);
                    }

                    if (points.Count > 0)
                    {
                        for (int i = 0; i < points.Count; i++)
                        {
                            canvasInfos.SetPixel(points[i].x, points[i].y, canvasPixel.PixelColor);
                        }
                        canvasInfos.ApplyColor();
                        lastPoint = newPoint;
                    }
                }

            }

        }

        PaintSatus absorbLastSatus;
        bool BeginAbsorb;
        private IEnumerator ReadyAbsorbStatus(Vector2 pos)
        {
            BeginAbsorb = true;
            float time = 0;
            while (BeginAbsorb)
            {
                yield return null;
                time += Time.deltaTime;
                if (time > 1f)
                {
                    //absorbLastSatus = this.canvasPixel.CurPaintSatus;
                    //this.canvasPixel.CurPaintSatus = PaintSatus.AbsorbColor;
                    ToAbsorbStatus();
                    AbsorbColor(pos);
                    break;
                }
            }
        }

        private void ToAbsorbStatus()
        {
            BeginAbsorb = true;
            absorbLastSatus = this.canvasPixel.CurPaintSatus;
            this.canvasPixel.CurPaintSatus = PaintSatus.AbsorbColor;
        }

        private void AbsorbColor(Vector2 pos)
        {
            Vector2Int newPoint = PointerDataToRelativePos(pos);
            int idx = newPoint.x + newPoint.y * canvasInfos.Size;
            //只处理在框内的
            if (newPoint.x < 0 || newPoint.x >= resolution.x || newPoint.y < 0 || newPoint.y >= resolution.y ||
                idx >= canvasInfos.Colors.Length)
                return;
            this.UIRef.image_Absorb.gameObject.SetActive(true);
            this.UIRef.image_Absorb.rectTransform.anchoredPosition = pos;
            var c = canvasInfos.Colors[idx];

            if (c.a != 0)
            {
                this.UIRef.image_Absorb.color = c;
                mColorPalette.RecColor.image.color = this.canvasPixel.CurPixelColor;
                canvasPixel.PixelColor = c;
            }

        }

        public List<Vector2Int> DrawBrush(BrushType brushType, Vector2Int point, int size)
        {
            if (brushType == BrushType.SquarePixel)
            {
                return DrawSquarePixel(point, size, size);
            }
            else if (brushType == BrushType.CircleCenter)
            {
                return DrawRasterizeCircleCenter(point, size, size);
            }
            return null;
        }
        private List<Vector2Int> DrawSquarePixel(Vector2Int point, int sizeX, int sizeY, int sizeOut = 0)
        {
            var list = new List<Vector2Int>();
            float radiusX = (float)sizeX / 2f;
            float radiusY = (float)sizeY / 2f;
            int width = sizeX;
            int height = sizeY;
            Vector2Int starPoint = new Vector2Int((int)(point.x - radiusX), (int)(point.y - radiusY));
            for (int x = 0; x < width; x++)
            {
                for (int y = 0; y < height; y++)
                {
                    if (sizeOut <= 0 || (sizeOut > 0 && (x < sizeOut || Mathf.Abs(x - width) <= sizeOut || y < sizeOut || Mathf.Abs(y - height) <= sizeOut)))
                    {
                        var cx = starPoint.x + x;
                        var cy = starPoint.y + y;
                        if (cx < 0 || cx >= resolution.x || cy < 0 || cy >= resolution.y)
                            continue;

                        list.Add(new Vector2Int(cx, cy));
                    }
                }
            }
            return list;
        }
        private List<Vector2Int> DrawSquareFramePixel(Vector2Int start, int sizeX, int sizeY, int sizeOut = 0)
        {
            var list = new List<Vector2Int>();
            int width = Mathf.Abs(sizeX);
            int height = Mathf.Abs(sizeY);

            for (int x = 0; x < width; x++)
            {
                for (int y = 0; y < height; y++)
                {
                    if (sizeOut <= 0 || (sizeOut > 0 && (x < sizeOut || Mathf.Abs(x - width) <= sizeOut || y < sizeOut || Mathf.Abs(y - height) <= sizeOut)))
                    {
                        var cx = start.x + x * (int)Mathf.Sign(sizeX);
                        var cy = start.y + y * (int)Mathf.Sign(sizeY);
                        if (cx < 0 || cx >= resolution.x || cy < 0 || cy >= resolution.y)
                            continue;

                        list.Add(new Vector2Int(cx, cy));
                    }
                }
            }
            return list;
        }
        private Color[] CollectSquareFramePixel(CanvasModel canvasModel, Vector2Int start, int sizeX, int sizeY)
        {
            int width = Mathf.Abs(sizeX);
            int height = Mathf.Abs(sizeY);
            var colors = new Color[width * height];

            for (int x = 0; x < width; x++)
            {
                for (int y = 0; y < height; y++)
                {
                    var indexX = x * (int)Mathf.Sign(sizeX);
                    var indexY = y * (int)Mathf.Sign(sizeY);
                    var cx = start.x + indexX;
                    var cy = start.y + indexY;
                    if (cx < 0 || cx >= resolution.x || cy < 0 || cy >= resolution.y)
                        continue;

                    colors[indexX + (sizeX > 0 ? 0 : (width - 1)) + (indexY + (sizeY > 0 ? 0 : (height - 1))) * width] = canvasModel.Colors[cx + cy * canvasModel.Size];
                    canvasModel.Colors[cx + cy * canvasModel.Size] = Color.clear;
                }
            }
            return colors;
        }


        //todo 优化 区域
        private List<Vector2Int> DrawRasterizeCircleCenter(Vector2Int point, int sizeX, int sizeY, int sizeRing = 0)
        {
            Vector2 circlePos = new Vector2((float)point.x + 0.5f * (sizeX % 2 - 1), (float)point.y + 0.5f * (sizeY % 2 - 1));
            return DrawCircleCenter(point, circlePos, sizeX, sizeY, sizeRing);
        }
        private List<Vector2Int> DrawCircleCenter(Vector2Int point, int sizeX, int sizeY, int sizeRing = 0)
        {
            return DrawCircleCenter(point, point, sizeX, sizeY, sizeRing);
        }
        private Color[] CollectCircleCenter(CanvasModel canvasModel, Vector2Int point, int sizeX, int sizeY, out Vector2 centerPoint)
        {
            var colors = new Color[sizeX * sizeY];
            float radiusX = (float)sizeX / 2f;
            float radiusY = (float)sizeY / 2f;
            int width = sizeX;
            int height = sizeY;
            Vector2Int starPoint = new Vector2Int(point.x - Mathf.FloorToInt(radiusX), point.y - Mathf.FloorToInt(radiusY));
            // 遍历二维数组中的每个点，看看它是否在圆内
            for (int x = 0; x < width; x++)
            {
                for (int y = 0; y < height; y++)
                {
                    var cx = starPoint.x + x;
                    var cy = starPoint.y + y;
                    if (cx < 0 || cx >= resolution.x || cy < 0 || cy >= resolution.y)
                        continue;

                    float ratio = (float)sizeX / (float)sizeY;
                    //int distance = (int)Mathf.Round(Mathf.Sqrt(Mathf.Pow(circlePos.x - cx, 2) + Mathf.Pow((circlePos.y - cy) * ratio, 2)));
                    double distance = Mathf.Sqrt(Mathf.Pow(point.x - cx, 2) + Mathf.Pow((point.y - cy) * ratio, 2));
                    var uv = x + y * width;
                    if (distance <= radiusX)
                    {
                        colors[uv] = canvasModel.Colors[cx + cy * canvasModel.Size];
                        canvasModel.Colors[cx + cy * canvasModel.Size] = Color.clear;
                    }
                    else
                    {
                        colors[uv] = Color.clear;
                    }
                }
            }
            centerPoint = new Vector2(starPoint.x + (float)width / 2f, starPoint.y + (float)height / 2f);
            return colors;
        }
        private List<Vector2Int> DrawCircleCenter(Vector2Int point, Vector2 circlePos, int sizeX, int sizeY, int sizeRing = 0)
        {
            var list = new List<Vector2Int>();
            float radiusX = (float)sizeX / 2f;
            float radiusY = (float)sizeY / 2f;
            int width = sizeX;
            int height = sizeY;
            Vector2Int starPoint = new Vector2Int(point.x - Mathf.FloorToInt(radiusX), point.y - Mathf.FloorToInt(radiusY));
            // 遍历二维数组中的每个点，看看它是否在圆内
            for (int x = 0; x < width; x++)
            {
                for (int y = 0; y < height; y++)
                {
                    var cx = starPoint.x + x;
                    var cy = starPoint.y + y;
                    if (cx < 0 || cx >= resolution.x || cy < 0 || cy >= resolution.y)
                        continue;

                    float ratio = (float)sizeX / (float)sizeY;
                    //int distance = (int)Mathf.Round(Mathf.Sqrt(Mathf.Pow(circlePos.x - cx, 2) + Mathf.Pow((circlePos.y - cy) * ratio, 2)));
                    double distance = Mathf.Sqrt(Mathf.Pow(circlePos.x - cx, 2) + Mathf.Pow((circlePos.y - cy) * ratio, 2));
                    if (distance <= radiusX && (sizeRing <= 0 || sizeRing > 0 && (distance > radiusX - sizeRing)))
                    {
                        list.Add(new Vector2Int(cx, cy));
                    }
                }
            }
            return list;
        }
        private List<Vector2Int> DrawPixelCircleCenter(Vector2Int point, int sizeX, int sizeY, int sizeRing = 0)
        {
            var list = new List<Vector2Int>();
            float radiusX = (float)sizeX / 2f;
            float radiusY = (float)sizeY / 2f;
            int width = sizeX;
            int height = sizeY;
            Vector2Int starPoint = new Vector2Int(point.x - Mathf.FloorToInt(radiusX), point.y - Mathf.FloorToInt(radiusY));
            float2 circlePos = new float2((float)point.x + 0.5f * (sizeX % 2 - 1), (float)point.y + 0.5f * (sizeY % 2 - 1));
            // 遍历二维数组中的每个点，看看它是否在圆内
            for (int x = 0; x < width; x++)
            {
                for (int y = 0; y < height; y++)
                {
                    var cx = starPoint.x + x;
                    var cy = starPoint.y + y;
                    if (cx < 0 || cx >= resolution.x || cy < 0 || cy >= resolution.y)
                        continue;

                    float ratio = (float)sizeX / (float)sizeY;
                    //int distance = (int)Mathf.Round(Mathf.Sqrt(Mathf.Pow(circlePos.x - cx, 2) + Mathf.Pow((circlePos.y - cy) * ratio, 2)));
                    double distance = Mathf.Sqrt(Mathf.Pow(circlePos.x - cx, 2) + Mathf.Pow((circlePos.y - cy) * ratio, 2));
                    if (distance <= radiusX/* && (sizeRing <= 0 || sizeRing > 0 && (distance > radiusX - sizeRing))*/)
                    {
                        list.Add(new Vector2Int(cx, cy));
                    }
                }
            }
            return list;
        }
        private void DrawCircleCenterColors(Vector2Int point, int sizeX, int sizeY, int sizeRing = 0)
        {
            var list = new List<Vector2Int>();
            float radiusX = (float)sizeX / 2f;
            float radiusY = (float)sizeY / 2f;
            int width = sizeX;
            int height = sizeY;
            Vector2Int starPoint = new Vector2Int(point.x - Mathf.FloorToInt(radiusX), point.y - Mathf.FloorToInt(radiusY));
            float2 circlePos = new float2((float)point.x + 0.5f * (sizeX % 2 - 1), (float)point.y + 0.5f * (sizeY % 2 - 1));
            // 遍历二维数组中的每个点，看看它是否在圆内
            for (int x = 0; x < width; x++)
            {
                for (int y = 0; y < height; y++)
                {
                    var cx = starPoint.x + x;
                    var cy = starPoint.y + y;
                    if (cx < 0 || cx >= resolution.x || cy < 0 || cy >= resolution.y)
                        continue;

                    float ratio = (float)sizeX / (float)sizeY;
                    //int distance = (int)Mathf.Round(Mathf.Sqrt(Mathf.Pow(circlePos.x - cx, 2) + Mathf.Pow((circlePos.y - cy) * ratio, 2)));
                    double distance = Mathf.Sqrt(Mathf.Pow(circlePos.x - cx, 2) + Mathf.Pow((circlePos.y - cy) * ratio, 2));
                    if (distance <= radiusX/* && (sizeRing <= 0 || sizeRing > 0 && (distance > radiusX - sizeRing))*/)
                    {
                        list.Add(new Vector2Int(cx, cy));
                    }
                }
            }
        }
        //奇偶 栅格 中心点
        private Vector2Int RasterizePoint(Vector2Int newPoint, int pixelSize)
        {
            if (pixelSize > 1)
            {
                newPoint.x = Mathf.FloorToInt((newPoint.x / pixelSize) * pixelSize + (float)pixelSize / 2f);
                newPoint.y = Mathf.FloorToInt((newPoint.y / pixelSize) * pixelSize + (float)pixelSize / 2f);
            }
            return newPoint;
        }
        //坐标转换
        private Vector2Int PointerDataToRelativePos(Vector2 clickPosition)
        {
            if (!thisRect) return Vector2Int.zero;
            Vector2 result;
            var camera = UniGameCameras.GetInstance().GetUICamera();
            RectTransformUtility.ScreenPointToLocalPointInRectangle(thisRect, clickPosition, camera, out result);
            result += thisRect.rect.size / 2;
            Vector2Int intResult = Vector2Int.zero;
            pixelSize = thisRect.rect.size / resolution;
            intResult.Set(Mathf.FloorToInt(result.x / pixelSize.x), Mathf.FloorToInt(result.y / pixelSize.y));
            return intResult;
        }

        private Vector2 PixelPosToScreenPoint(Vector2 intResult)
        {
            if (!thisRect) return Vector2Int.zero;
            Vector2 result = Vector2.zero;
            pixelSize = thisRect.rect.size / resolution;
            result.x = intResult.x * pixelSize.x;
            result.y = intResult.y * pixelSize.y;
            result -= thisRect.rect.size / 2;
            RectTransformUtility.WorldToScreenPoint(UniGameCameras.GetInstance().GetUICamera(), result);
            return result;
        }

        public void SetTexturePixels(Vector2Int point)
        {
            var list = DrawBrush(canvasPixel.BrushType, point, canvasPixel.Size);

            foreach (var i in list)
            {
                //texture.SetPixel(i.x, i.y, penColor);
                if (i != null && canvasInfos != null && canvasPixel != null)
                    canvasInfos.SetPixel(i.x, i.y, canvasPixel.PixelColor);
            }
        }
        //连通域算法 广度优先 从叶节点
        private IEnumerator PaintBucket(Vector2Int newPoint, Color color)
        {
            if (canvasPixel.Bucketing)
            {
                yield break;
            }
            Color preColor = this.canvasInfos.GetPixel(newPoint);
            // 如果点 (x, y) 超出了数组的范围，或者它的值不等于 1，则退出函数
            if (newPoint.x < 0 || newPoint.x >= resolution.x || newPoint.y < 0 || newPoint.y >= resolution.y || preColor.Compare(color))
            {
                yield break;
            }

            canvasPixel.Bucketing = true;
            canvasInfos.SetPixel(newPoint.x, newPoint.y, color);
            //texture.SetPixel(newPoint.x, newPoint.y, color);

            Queue<Tuple<int, int>> queue = new Queue<Tuple<int, int>>();

            queue.Enqueue(new Tuple<int, int>(newPoint.x, newPoint.y));

            // 当队列不为空时，取出队头元素并搜索它的上下左右四个相邻点
            while (queue.Count > 0)
            {
                Tuple<int, int> point = queue.Dequeue();
                int x = point.Item1;
                int y = point.Item2;

                // 搜索 (x, y) 的上下左右四个相邻点
                if (x - 1 >= 0 && UniCommonTool.ColorCompare(this.canvasInfos.GetPixel(x - 1, y), preColor))
                {
                    canvasInfos.SetPixel(x - 1, y, color);
                    queue.Enqueue(new Tuple<int, int>(x - 1, y));
                }

                if (x + 1 < resolution.x && UniCommonTool.ColorCompare(canvasInfos.GetPixel(x + 1, y), preColor))
                {
                    canvasInfos.SetPixel(x + 1, y, color);
                    queue.Enqueue(new Tuple<int, int>(x + 1, y));
                }

                if (y - 1 >= 0 && UniCommonTool.ColorCompare(canvasInfos.GetPixel(x, y - 1), preColor))
                {
                    canvasInfos.SetPixel(x, y - 1, color);
                    queue.Enqueue(new Tuple<int, int>(x, y - 1));
                }

                if (y + 1 < resolution.y && UniCommonTool.ColorCompare(canvasInfos.GetPixel(x, y + 1), preColor))
                {
                    canvasInfos.SetPixel(x, y + 1, color);
                    queue.Enqueue(new Tuple<int, int>(x, y + 1));
                }
            }

            canvasInfos.ApplyColor();
            canvasPixel.Bucketing = false;
            lastPoint = newPoint;
        }
        private Color[] MagicCollectAndModifyOrigin(out int height, out int width, Vector2Int newPoint, out Vector2Int centerPoint)
        {
            height = 0;
            width = 0;
            centerPoint = Vector2Int.zero;
            var list = new List<Vector2Int>();
            Color preColor = this.canvasInfos.GetPixel(newPoint);

            if (newPoint.x < 0 || newPoint.x >= resolution.x || newPoint.y < 0 || newPoint.y >= resolution.y || UniCommonTool.ColorCompare(preColor, Color.clear))
            {
                return null;
            }

            HashSet<Vector2Int> visited = new HashSet<Vector2Int>();
            Queue<Vector2Int> queue = new Queue<Vector2Int>();

            visited.Add(newPoint);
            queue.Enqueue(newPoint);

            //当队列不为空，取队头元素搜索它的上下左右四个相邻点
            while (queue.Count > 0)
            {
                Vector2Int point = queue.Dequeue();

                //搜索 x, y 的上下左右四个相邻点
                foreach (Vector2Int neighbor in GetNeighbors(point))
                {
                    if (!visited.Contains(neighbor) && UniCommonTool.ColorCompare(this.canvasInfos.GetPixel(neighbor), preColor))
                    {
                        visited.Add(neighbor);
                        list.Add(neighbor);
                        queue.Enqueue(neighbor);
                    }
                }
            }

            //计算收集到的像素的高度和宽度
            int minX = int.MaxValue;
            int minY = int.MaxValue;
            int maxX = int.MinValue;
            int maxY = int.MinValue;
            foreach (Vector2Int pixel in list)
            {
                if (pixel.x < minX)
                {
                    minX = pixel.x;
                }
                if (pixel.y < minY)
                {
                    minY = pixel.y;
                }
                if (pixel.x > maxX)
                {
                    maxX = pixel.x;
                }
                if (pixel.y > maxY)
                {
                    maxY = pixel.y;
                }
            }

            height = maxY - minY + 1;
            width = maxX - minX + 1;

            //计算中心点
            centerPoint = new Vector2Int(minX + width / 2, minY + height / 2);

            //创建并填充颜色数组
            Color[] colors = new Color[height * width];

            //根据像素的位置修改数组中相应的元素为正确的颜色值
            list.Add(newPoint);
            foreach (Vector2Int pixel in list)
            {
                int x = pixel.x - minX;
                int y = pixel.y - minY;
                int index = y * width + x; //将像素坐标转换为数组下标
                colors[index] = preColor; //修改对应的数组元素为正确的颜色值
                canvasInfos.Colors[pixel.x + pixel.y * canvasInfos.Size] = Color.clear; // 原图改成透明
            }
            canvasInfos.ApplyColor();
            return colors;
        }

        private List<Vector2Int> GetNeighbors(Vector2Int point)
        {
            List<Vector2Int> neighbors = new List<Vector2Int>();

            if (point.x - 1 >= 0)
            {
                neighbors.Add(new Vector2Int(point.x - 1, point.y));
            }

            if (point.x + 1 < resolution.x)
            {
                neighbors.Add(new Vector2Int(point.x + 1, point.y));
            }

            if (point.y - 1 >= 0)
            {
                neighbors.Add(new Vector2Int(point.x, point.y - 1));
            }

            if (point.y + 1 < resolution.y)
            {
                neighbors.Add(new Vector2Int(point.x, point.y + 1));
            }

            return neighbors;
        }

        private List<Vector2Int> DrawLineFrom(Vector2Int start, Vector2Int end)
        {
            return DrawLineFrom(start, end, canvasPixel.BrushType == BrushType.SquarePixel ? canvasPixel.Size : 0);
        }
        //Bresenham 算法
        private List<Vector2Int> DrawLineFrom(Vector2Int start, Vector2Int end, int pixelSize = 0)
        {
            // 计算两个点之间的直线
            List<Vector2Int> points = new List<Vector2Int>();

            if (pixelSize > 0)
            {
                end = RasterizePoint(new Vector2Int(end.x, end.y), pixelSize);
            }
            int dx = end.x - start.x;
            int dy = end.y - start.y;
            int step = Mathf.Abs(dx) > Mathf.Abs(dy) ? Mathf.Abs(dx) : Mathf.Abs(dy);

            float xIncrement = dx / (float)step;
            float yIncrement = dy / (float)step;
            float x = start.x;
            float y = start.y;

            for (int i = 0; i < step; i++)
            {
                //points.Add(new Vector2Int((int)Mathf.Round(x), (int)Mathf.Round(y)));

                if (pixelSize > 0)
                {
                    var pixelPoint = RasterizePoint(new Vector2Int((int)Mathf.Round(x), (int)Mathf.Round(y)), pixelSize);
                    if (!points.Contains(pixelPoint))
                    {
                        points.Add(pixelPoint);
                    }
                }
                else
                {
                    points.Add(new Vector2Int((int)Mathf.Round(x), (int)Mathf.Round(y)));
                }


                x += xIncrement;
                y += yIncrement;
            }

            // 将最后一个点加入列表
            if (!points.Contains(end))
            {
                points.Add(end);
            }
            //points.Add(new Vector2Int(end.x, end.y));
            return points;
        }
        #endregion

        #region 色盘
        private const int COL_SIZE = 6;
        private Vector2 ItemSpacing = new Vector2(10, 10);
        private UIInfiniteTable infiniteTable;
        private List<ColorItem> m_listItem = new List<ColorItem>();
        List<Color> colors;
        private UIInfiniteTable infiniteTableSelected;
        private List<ColorItem> m_listItemSelected = new List<ColorItem>();
        List<Color> colorsSelected = new List<Color>();
        private int indexcurDisk = 1;
        private int indexDisk = 1;


        // private void RefreshColor()
        // {
        //     if (colors != null)
        //     {
        //         colors.Clear();
        //         colors = null;
        //     }
        //     colors = UniColorPickConfig.CFGS.GetPaintingColors();
        // }
        // private void RefreshScroll()
        // {
        //     if (!infiniteTable)
        //     {
        //         RectTransform content = this.UIRef.rect_DiskScroll.GetComponent<RectTransform>();
        //         var item = this.UIRef.tran_Item.gameObject;
        //
        //         if (UISystem.Inst)
        //         {
        //             try
        //             {
        //                 infiniteTable = UISystem.Inst.InitLoopList(content, item.gameObject, 0, false, COL_SIZE, item.GetComponent<RectTransform>().sizeDelta, ItemSpacing);
        //                 infiniteTable.mTopSpacing = ItemSpacing.x;
        //                 infiniteTable.onGetItemComponent = OnGetItemComponent;
        //
        //                 infiniteTable.onReposition = OnReposition;
        //                 item.gameObject.SetActive(false);
        //                 var contentTran = content.Find("Content").GetComponent<RectTransform>();
        //                 contentTran.localEulerAngles = Vector3.zero;
        //             }
        //             catch (Exception e)
        //             {
        //                 Logger.Warn("", e);
        //             }
        //         }
        //     }
        //     if (infiniteTable)
        //     {
        //         infiniteTable.TableDataCount = colors.Count;
        //         infiniteTable.RefreshData();
        //     }
        // }
        // private void OnGetItemComponent(GameObject obj)
        // {
        //     var item = obj.AddComponent<ColorItem>();
        //     item.Init(RefrshDiskData);
        //     m_listItem.Add(item);
        //     var rect = item.GetComponent<RectTransform>();
        //     rect.localEulerAngles = Vector3.zero;
        // }
        // private void OnReposition(GameObject go, int dataIndex, int childIndex)
        // {
        //     m_listItem[childIndex].Refresh(ColorCompare(canvasPixel.PixelColor, colors[dataIndex]), colors[dataIndex]);
        // }
        //
        // private void RefrshDiskData(Image image)
        // {
        //     this.canvasPixel.PixelColor = image.color;
        //     CloseAllScend();
        //     SwitchSimpleDisk();
        // }

        //todo 有时间合成一个 
        // private void RefreshColorSelected(int col = 0)
        // {
        //     if (col < 0)
        //         return;
        //     if (colorsSelected.Count > 0)
        //     {
        //         colorsSelected.Clear();
        //     }
        //     while (col < colors.Count)
        //     {
        //         colorsSelected.Add(colors[col]);
        //         col += 6;
        //     }
        // }
        // private void RefreshScrollSelected()
        // {
        //     if (!infiniteTableSelected)
        //     {
        //         RectTransform content = this.UIRef.rect_curDiskScroll.GetComponent<RectTransform>();
        //         var item = this.UIRef.tran_curItem.gameObject;
        //         
        //         infiniteTableSelected = UISystem.Inst.InitLoopList(content, item.gameObject, 0, false, 1, item.GetComponent<RectTransform>().sizeDelta, ItemSpacing);
        //         infiniteTableSelected.mTopSpacing = ItemSpacing.x;
        //         infiniteTableSelected.onGetItemComponent = OnGetItemComponentSelected;
        //
        //         infiniteTableSelected.onReposition = OnRepositionSelected;
        //         item.gameObject.SetActive(false);
        //         var contentTran = content.Find("Content").GetComponent<RectTransform>();
        //         contentTran.localEulerAngles = Vector3.zero;
        //     }
        //     infiniteTableSelected.TableDataCount = colorsSelected.Count;
        //     infiniteTableSelected.RefreshData();
        // }
        // private void OnGetItemComponentSelected(GameObject obj)
        // {
        //     var item = obj.AddComponent<ColorItem>();
        //     //if (m_listItemSelected.Count == 0)
        //     //{
        //     //    item.Refresh = true;
        //     //}
        //     item.Init(RefrshData);
        //     m_listItemSelected.Add(item);
        //     var rect = item.GetComponent<RectTransform>();
        //     rect.localEulerAngles = Vector3.zero;
        // }
        // private void OnRepositionSelected(GameObject go, int dataIndex, int childIndex)
        // {
        //     m_listItemSelected[childIndex].Refresh(ColorCompare(canvasPixel.PixelColor, colorsSelected[dataIndex]), colorsSelected[dataIndex]);
        // }
        //
        // private void RefrshData(Image image)
        // {
        //     this.canvasPixel.PixelColor = image.color;
        //     CloseAllScend();
        // }
        #endregion

        //#region 高斯模糊
        //static RenderTexture m_BlurTexture;
        //static Camera m_BlurCamera;
        //private void SetBlur()
        //{
        //    try
        //    {
        //        var img = this.UIRef.BG.GetComponent<RawImage>();

        //        var mat = new Material(img?.material);

        //        if (!m_BlurTexture)
        //        {
        //            m_BlurTexture = new RenderTexture(Screen.width, Screen.height, 32);

        //        }
        //        if (!m_BlurCamera)
        //        {
        //            m_BlurCamera = new GameObject("Capture").AddComponent<Camera>();
        //            m_BlurCamera.gameObject.SetActive(false);
        //        }
        //        m_BlurCamera.CopyFrom(UniGameCameras.GetInstance().GetCurCamera());
        //        if (m_BlurCamera)
        //        {
        //            m_BlurCamera.cullingMask = ~(1 << 5);
        //            m_BlurCamera.backgroundColor = Color.clear;
        //            m_BlurCamera.clearFlags = CameraClearFlags.Skybox;
        //            m_BlurCamera.transform.position = RTESystem.Inst.EditCam.transform.position;
        //            m_BlurCamera.transform.rotation = RTESystem.Inst.EditCam.transform.rotation;
        //            m_BlurCamera.targetTexture = m_BlurTexture;
        //            m_BlurCamera.Render();

        //            if (mat)
        //            {
        //                mat.mainTexture = m_BlurTexture;
        //                mat.SetFloat("_BlurScale", 2f);
        //                mat.SetVector("_MainTex_TexelSize", new Vector4(1f / m_BlurTexture.width, 1f / m_BlurTexture.height, 0, 0));
        //                img.texture = m_BlurTexture;


        //                var temp = RenderTexture.GetTemporary(m_BlurTexture.width, m_BlurTexture.height, 0);
        //                //模糊次数
        //                for (int times = 0; times < 10; times++)
        //                {
        //                    Graphics.Blit(m_BlurTexture, temp, mat, 0);
        //                    Graphics.Blit(temp, m_BlurTexture, mat, 1);
        //                }
        //                img.material = mat;
        //                RenderTexture.ReleaseTemporary(temp);
        //            }
        //        }
        //    }
        //    catch (Exception e)
        //    {
        //        Logger.Debug(e.ToString());
        //    }
        //}
        //#endregion

        #region 序列帧
        private const int GIF_COL_SIZE = 9;
        private UIInfiniteTable GIFInfiniteTable;
        private List<GifItem> m_gifListItem = new List<GifItem>();
        List<CanvasLayers> gifCanvasList;
        private bool isPlaying;
        private float FrameRata = 8f;
        private int CurFrame
        {
            get { return m_curFrame; }
            set
            {
                m_curFrame = value;
            }
        }
        private int m_curFrame;
        private float ProprtyY;
        private int TotalFrame
        {
            get
            {
                if (gifCanvasList != null)
                    return gifCanvasList.Count - 1;
                return 0;
            }
        }


        private void GifInit()
        {
            this.UIRef.InputField_FPS.onValueChanged.AddListener((v) =>
            {
                if (string.IsNullOrEmpty(v) || !float.TryParse(v, out FrameRata))
                {
                    FrameRata = 8;
                }
                FrameRata = Mathf.Max(FrameRata, 1);
                FrameRata = Mathf.Min(FrameRata, 64);
            });
            this.UIRef.tog_SetBG.onValueChanged.AddListener((b) =>
            {
                this.UIRef.InputField_FPS.contentType = InputField.ContentType.IntegerNumber;
                this.UIRef.InputField_FPS.text = FrameRata.ToString();
            });
            this.UIRef.btn_CLose.onClick.AddListener(() =>
            {
                this.UIRef.tog_SetBG.isOn = false;
            });
            this.UIRef.tog_Content.onValueChanged.AddListener((b) =>
            {
                if (this.UIRef.SwitchTog.GetComponent<SwitchToggle>().onTog.isOn)
                {
                    this.UIRef.SwitchTog.GetComponent<SwitchToggle>().offTog.isOn = true;
                }
                else
                {
                    GifPause();
                }

                this.Model.ShowAnimContent(b);
                if (b)
                {
                    RefreshGifScroll();
                }
            });
            this.UIRef.SwitchTog.GetComponent<SwitchToggle>().Init((b) => { if (b) GifPause(); }, (b) => { if (b) GifPlay(); });

            this.UIRef.btn_previousFrame.onClick.AddListener(PreviousFrame);
            this.UIRef.btn_nextFrame.onClick.AddListener(NextFrame);
            this.UIRef.btn_CopyFrame.onClick.AddListener(CopyFrame);
            this.UIRef.btn_AddFrame.onClick.AddListener(AddFrame);
            this.UIRef.btn_DelFrame.onClick.AddListener(DelFrame);
        }

        private void RefreshGifScroll()
        {
            if (!GIFInfiniteTable)
            {
                RectTransform content = this.UIRef.ScrollView.GetComponent<RectTransform>();
                var item = this.UIRef.animItem.gameObject;

                GIFInfiniteTable = UISystem.Inst.InitLoopList(content, item.gameObject, GIF_COL_SIZE, true, 1, item.GetComponent<RectTransform>().sizeDelta, ItemSpacing);
                GIFInfiniteTable.onGetItemComponent = OnGetGifItemComponent;
                GIFInfiniteTable.onReposition = GifOnReposition;
                item.gameObject.SetActive(false);

                ProprtyY = this.UIRef.Proprty.position.y;
            }
            if (GIFInfiniteTable && gifCanvasList != null)
            {
                GIFInfiniteTable.TableDataCount = gifCanvasList.Count;
                GIFInfiniteTable.RefreshData();
            }
        }

        private void InitEmptyCanvasInfos()
        {
            gifCanvasList = new List<CanvasLayers>
                    {
                         new CanvasLayers(this.UIRef.raw_CanvasImage,workType){Canvas = { new Canvas64Model(this.UIRef.raw_CanvasImage,true) }},
                         new CanvasLayers(this.UIRef.raw_CanvasImage,workType){Canvas = { new Canvas64Model(this.UIRef.raw_CanvasImage,false) }},
                         new CanvasLayers(this.UIRef.raw_CanvasImage,workType){Canvas = { new Canvas64Model(this.UIRef.raw_CanvasImage,false) }},
                         new CanvasLayers(this.UIRef.raw_CanvasImage,workType){Canvas = { new Canvas64Model(this.UIRef.raw_CanvasImage,false) }},
                         new CanvasLayers(this.UIRef.raw_CanvasImage,workType){Canvas = { new Canvas64Model(this.UIRef.raw_CanvasImage,false) }},
                         new CanvasLayers(this.UIRef.raw_CanvasImage,workType){Canvas = { new Canvas64Model(this.UIRef.raw_CanvasImage,false) }},
                         new CanvasLayers(this.UIRef.raw_CanvasImage,workType){Canvas = { new Canvas64Model(this.UIRef.raw_CanvasImage,false) }},
                         new CanvasLayers(this.UIRef.raw_CanvasImage,workType){Canvas = { new Canvas64Model(this.UIRef.raw_CanvasImage,false) }},null,
                    };
        }

        private void RefreshProprty(float posX, int status = 0)
        {
            this.Model.UpdateGIFProprtyView(status);
            this.UIRef.Proprty.position = new Vector2(posX, ProprtyY);
            var anchoredPos = (this.UIRef.Proprty as RectTransform).anchoredPosition3D;
            (this.UIRef.Proprty as RectTransform).anchoredPosition3D = new Vector3(anchoredPos.x, anchoredPos.y, 0);
        }

        private void RefreshGifData(int curFrame, float posX)
        {
            if (curFrame.Equals(CurFrame))
            {
                if (!isPlaying)
                {
                    RefreshProprty(posX, 1);
                }
                else
                {
                    RefreshProprty(posX);
                }
                return;
            }
            else
            {
                RefreshProprty(posX);
            }

            if (curFrame <= TotalFrame)
            {
                this.canvasInfos = gifCanvasList[curFrame - 1];
                AfterSwitchCanvas();
                gifCanvasList[curFrame - 1].DataIsDirty = true;
                this.CurFrame = curFrame;
            }
            else
            {
                AddLastFrame();
            }

            GIFInfiniteTable.RefreshData();
        }

        private void OnGetGifItemComponent(GameObject obj)
        {
            var item = obj.GetComponent<GifItem>();
            item.Init(RefreshGifData);
            m_gifListItem.Add(item);
        }
        private void GifOnReposition(GameObject go, int dataIndex, int childIndex)
        {
            if (m_gifListItem != null && gifCanvasList != null && gifCanvasList.Count > dataIndex && m_gifListItem.Count > childIndex)
            {
                if (dataIndex < 0 || dataIndex > gifCanvasList.Count - 1 || childIndex < 0) return;
                m_gifListItem[childIndex].Refresh(dataIndex + 1, gifCanvasList[dataIndex]);
                m_gifListItem[childIndex].RefreshView(dataIndex + 1 == CurFrame);
            }
        }
        public IEnumerator OnAnimUpdate()
        {
            while (isPlaying && TotalFrame > 0 && FrameRata > 0)
            {
                yield return new WaitForSeconds(1f / FrameRata);
                OnPlayingChangeFrame(CurFrame % TotalFrame + 1);
            }
        }

        private void OnPlayingChangeFrame(int frame, bool totalFrameChange = false)
        {
            if (frame == CurFrame)
                return;
            CurFrame = frame;

            canvasInfos = gifCanvasList[CurFrame - 1];
            AfterSwitchCanvas();
            if (totalFrameChange)
            {
                RefreshGifScroll();
            }
            else
            {
                GIFInfiniteTable.RefreshData();
            }
        }

        private void ReOpen(bool showClip)
        {
            //todo
            this.UIRef.btn_layer.gameObject.SetActive(!showClip);
            this.UIRef.raw_CanvasImage.gameObject.SetActive(showClip);
            
            this.Model.ShowAnim(showClip);
            
            this.UIRef.tog_download.gameObject.SetActive(!showClip);
            this.UIRef.tog_share.gameObject.SetActive(!showClip);
            if (showClip)
            {
                if (gifCanvasList == null)
                {
                    if (UniMain.Game.Scene.WorkingType == WorkType.GIF && !string.IsNullOrEmpty(UniMain.Game.Work.Id))
                    {
                        PaintService.Instance.GetWorkClipData((t, c) =>
                        {


                            var dataInfo = UniGIFDataInfo.GetUniGIFDataInfoByBytes(c);

                            FrameRata = dataInfo.FrameRate;
                            this.UIRef.InputField_FPS.onValueChanged.Invoke(FrameRata.ToString());

                            if (!dataInfo.MaxTotalFrame.Equals(0) && !dataInfo.HorizontalAmount.Equals(0) && !dataInfo.VerticalAmount.Equals(0))
                            {
                                gifCanvasList = new List<CanvasLayers>();
                                var list = PaintService.Instance.SplitCombinedTexture(t, dataInfo.MaxTotalFrame);
                                foreach (var colors in list)
                                {
                                    var layers = new CanvasLayers(this.UIRef.raw_CanvasImage,workType);
                                    var newCanvas = new Canvas64Model(this.UIRef.raw_CanvasImage,true);
                                    newCanvas.Colors = colors;
                                    newCanvas.ApplyColor();
                                    layers.Add(newCanvas);
                                    gifCanvasList.Add(layers);
                                }
                                if (gifCanvasList.Count > 0)
                                {
                                    gifCanvasList.Add(null);
                                    InitCanvasData();
                                    return;
                                }
                            }
                            InitEmptyCanvasInfos();
                            InitCanvasData();
                        });
                    }
                    else
                    {
                        InitEmptyCanvasInfos();
                        InitCanvasData();
                        this.UIRef.raw_CanvasImage.texture = canvasInfos.CanvasTexture2D;//todo gif图层
                    }
                }

            }
        }

        private void InitCanvasData()
        {
            CurFrame = 1;
            if (!this.UIRef.tog_Content.isOn)
            {
                this.UIRef.tog_Content.isOn = true;
            }
            else
            {
                this.UIRef.tog_Content.onValueChanged.Invoke(true);
            }
            canvasInfos = gifCanvasList.First();
            AfterSwitchCanvas();
            RefreshGifScroll();
        }

        private Coroutine animCoroutine;
        private void GifPlay()
        {
            isPlaying = true;
            this.Model.UpdateGIFProprtyView();
            animCoroutine = this.UIRef.StartCoroutine(OnAnimUpdate());
            this.Model.ProprtyActive.Value = false;
        }
        private void GifPause()
        {
            isPlaying = false;
            if (animCoroutine != null)
            {
                this.UIRef.StopCoroutine(animCoroutine);
                animCoroutine = null;
            }
            this.Model.RedoUndo(canvasInfos);
        }
        private void PreviousFrame()
        {
            if (isPlaying)
                return;

            if (CurFrame > 1)
            {
                var data = this.gifCanvasList[CurFrame - 1];
                this.gifCanvasList[CurFrame - 1] = this.gifCanvasList[CurFrame - 2];
                this.gifCanvasList[CurFrame - 2] = data;
                CurFrame -= 1;
                RefreshGifScroll();
            }
        }

        private void NextFrame()
        {
            if (isPlaying)
                return;
            if (TotalFrame > 1 && CurFrame < TotalFrame)
            {
                var data = this.gifCanvasList[CurFrame - 1];
                this.gifCanvasList[CurFrame - 1] = this.gifCanvasList[CurFrame];
                this.gifCanvasList[CurFrame] = data;
                CurFrame += 1;
                RefreshGifScroll();
            }
        }
        private void CopyFrame()
        {
            if (isPlaying)
                return;
            if (TotalFrame >= 16)
            {
                UIHelper.Instance.ShowToast("A maximum of 16 frames is allowed!");
                return;
            }

            var newCanvas = new CanvasLayers(this.UIRef.raw_CanvasImage,workType);
            newCanvas.Add(new Canvas64Model(this.UIRef.raw_CanvasImage));
            
            //不用rtl 
            // if (this.gifCanvasList[CurFrame - 1].CanvasTexture != null)
            //     newCanvas.CanvasTexture = new RenderTexture(this.gifCanvasList[TotalFrame - 1].CanvasTexture);
            if (this.gifCanvasList[CurFrame - 1].CanvasTexture2D != null)
            {
                newCanvas.Colors = this.gifCanvasList[CurFrame - 1].CanvasTexture2D.GetPixels(0);
                newCanvas.ApplyColor();
            }
            AddFrame(CurFrame, newCanvas);
        }
        private void AddLastFrame()
        {
            AddFrame(TotalFrame);
        }
        private void AddFrame()
        {
            AddFrame(CurFrame);
        }
        private void AddFrame(int frame, CanvasLayers newCanvas = null)
        {
            if (isPlaying)
                return;
            if (TotalFrame >= 16)
            {
                UIHelper.Instance.ShowToast("A maximum of 16 frames is allowed!");
                return;
            }

            if (newCanvas == null)
            {
                newCanvas = new CanvasLayers(this.UIRef.raw_CanvasImage,workType);
                newCanvas.Add(new Canvas64Model(this.UIRef.raw_CanvasImage));
            }

            this.gifCanvasList.Insert(frame, newCanvas);

            canvasInfos = newCanvas;
            AfterSwitchCanvas();
            CurFrame = frame;

            RefreshGifScroll();
        }
        private void DelFrame()
        {
            if (isPlaying)
                return;
            if (TotalFrame <= 1)
            {
                UIHelper.Instance.ShowToast("More than one Frame!");
                return;
            }

            UIHelper.Instance.ShowDoubleBtnDialog("Clip_delete_ask".GetLanguageStr(), "btn_confirm".GetLanguageStr(), "btn_cancel".GetLanguageStr(), () =>
            {
                this.gifCanvasList.Remove(this.gifCanvasList[CurFrame - 1]);
                canvasInfos = this.gifCanvasList[TotalFrame - 1];
                AfterSwitchCanvas();
                CurFrame = TotalFrame;

                RefreshGifScroll();
            });

        }

        #endregion
    }
```

`UIPainting`

类继承自 `UIBase<UIPaintingRef, UIPaintingModel>`，用于在 Unity 中管理和操作绘画界面。该类包含多个字段和方法，用于处理绘画工具的初始化、绘画操作、图层管理、手势操作、保存和分享绘画等功能。

类中定义了多个字段，包括 `RefList`、`canvasPixel`、`canvasInfos`、`resolution`、`thisRect`、`pixelSize`、`lastPoint`、`mainTouch`、`enterTime`、`ViewSubscription`、`eventDownLoadPic`、`curIsShare` 和 `Logger`。这些字段用于存储绘画相关的信息和状态。`ShowType` 属性重写了基类的 `ShowType` 属性，返回 `FormShowType.First`，表示第一种显示类型。

`OnInit` 方法用于初始化绘画界面。方法中通过绑定模型的属性和 UI 元素，实现了绘画工具栏、颜色盘、图层管理等功能的初始化和事件监听。方法还设置了画笔和橡皮擦的大小滑块、绘画工具的切换按钮、撤销和重做按钮、调色板按钮、保存和分享按钮等的事件监听。

`OnOpen` 方法在打开绘画界面时调用。方法中初始化了绘画服务、颜色盘、画笔和橡皮擦的大小滑块、绘画工具的默认状态、画布的初始位置和缩放等。方法还设置了手势操作的事件监听，包括按下、抬起、点击、拖动和手势变化等。

`OnClose` 方法在关闭绘画界面时调用。方法中清理了绘画相关的资源和订阅，包括手势操作的事件监听、绘画数据、颜色盘、图层管理等。方法还上传了用户在绘画界面的停留时间统计数据。

`UpdateData` 方法用于更新绘画数据。方法根据当前的绘画状态，调用相应的绘画方法，包括绘制、绘制形状、套索工具和吸取颜色等。`SavePicture` 方法用于保存绘画作品，支持保存为 GIF 动画和静态图片，并调用回调函数处理保存成功或失败的情况。

`SavePaintingToLocal` 方法用于将绘画作品保存到本地，并支持分享功能。`OnDownloadResult` 方法处理下载结果，显示下载成功或失败的提示信息。`OnPointDownCanvas` 和 `OnPointUpCanvas` 方法分别在用户按下和抬起画布时调用，处理绘画操作和图层管理。

`CreateOverLayer` 方法用于创建覆盖图层，显示绘画的预览效果。`OnPointClickCanvas` 方法在用户点击画布时调用，处理绘画操作。`OnAbsorbOver` 方法在吸取颜色操作结束时调用，隐藏吸取颜色的 UI 元素。

`SetDrawSize` 方法用于设置画笔或橡皮擦的大小。`Undo` 和 `Redo` 方法分别用于撤销和重做绘画操作。`Draw` 方法用于绘制线条，`DrawWtihPoint` 方法用于单点绘画，`DrawShape` 方法用于绘制形状，`LassoTools` 方法用于套索工具操作。

`ReadyAbsorbStatus` 方法是一个协程，用于准备吸取颜色操作。`ToAbsorbStatus` 方法将当前绘画状态切换为吸取颜色状态。`AbsorbColor` 方法在指定位置吸取颜色，并更新颜色盘和画笔颜色。

`DrawBrush` 方法根据画笔类型和大小绘制图形。`DrawSquarePixel` 和 `DrawSquareFramePixel` 方法分别绘制方形像素和方形框架像素。`CollectSquareFramePixel` 方法收集方形框架像素的颜色数据。`DrawRasterizeCircleCenter` 和 `DrawCircleCenter` 方法分别绘制栅格化圆形中心和圆形中心。

`CollectCircleCenter` 方法收集圆形中心的颜色数据。`RasterizePoint` 方法将点栅格化到指定像素大小。`PointerDataToRelativePos` 方法将屏幕坐标转换为相对坐标。`PixelPosToScreenPoint` 方法将像素坐标转换为屏幕坐标。

`SetTexturePixels` 方法设置纹理像素。`PaintBucket` 方法是一个协程，使用广度优先算法填充区域。`MagicCollectAndModifyOrigin` 方法收集魔法棒工具选中的区域，并修改原始图像。`GetNeighbors` 方法获取指定点的相邻点。

`DrawLineFrom` 方法使用 Bresenham 算法绘制直线。`GifInit` 方法初始化 GIF 动画相关的 UI 元素和事件监听。`RefreshGifScroll` 方法刷新 GIF 动画的滚动视图。`InitEmptyCanvasInfos` 方法初始化空的画布信息。

`RefreshProprty` 方法刷新 GIF 动画的属性视图。`RefreshGifData` 方法刷新 GIF 动画的数据。`OnGetGifItemComponent` 方法获取 GIF 动画项组件。`GifOnReposition` 方法重新定位 GIF 动画项。

`OnAnimUpdate` 方法是一个协程，用于更新 GIF 动画的播放。`OnPlayingChangeFrame` 方法在播放 GIF 动画时切换帧。`ReOpen` 方法重新打开绘画界面。`InitCanvasData` 方法初始化画布数据。

`GifPlay` 和 `GifPause` 方法分别用于播放和暂停 GIF 动画。`PreviousFrame` 和 `NextFrame` 方法分别切换到上一帧和下一帧。`CopyFrame` 方法复制当前帧。`AddLastFrame` 和 `AddFrame` 方法添加帧。`DelFrame` 方法删除当前帧。