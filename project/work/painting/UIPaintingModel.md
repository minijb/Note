
```c#
    public class CanvasLayers
    {
        public CanvasLayers(RawImage rawImage,WorkType type)
        {
            ORawImage = rawImage;
            switch (type)
            {
                case WorkType.Material:
                    CurType = CanvasType.Mat;
                    break;
                case WorkType.Painting:
                    CurType = CanvasType.Pic;
                    break;
                case WorkType.GIF:
                    CurType = CanvasType.Gif;
                    break;
            }
        }
        public List<CanvasModel> Canvas { get; private set; } = new List<CanvasModel>();
        private CanvasModel mSelectModel;
        private RawImage ORawImage;
        public bool IsGif;

        public CanvasType CurType;
        public RawImage mLayerRawImage;//fix
        public RawImage LayerRawImage
        {
            get
            {
                if (CurType == CanvasType.Mat)
                {
                    return mLayerRawImage;
                }

                return CurRawImage;
            }
            set
            {
                mLayerRawImage = value;
            }
        } //fix

        public RawImage CurRawImage
        {
            get
            {
                if (GetSelectCanvasModel() is Canvas64Model)
                {
                    return ORawImage;
                }

                return mRawImage;
            }
            private set
            {
                mRawImage = value;
            }
        }
        public RawImage mRawImage { get; private set; }

        public CanvasModel CurSelectModel
        {
            get
            {
                return GetSelectCanvasModel();
            }
            set
            {
                if (value!=null)
                {
                    mSelectModel = value;
                }
            }
        }
        public int CurSelectModelIndexOf
        {
            get
            {
                var model = GetSelectCanvasModel();
                if (model!=null)
                {
                    return Canvas.IndexOf(model);
                }
                return 0;
            }
        }
        public event Action<CanvasModel> SelectHandler = null;

        public int Size
        {
            get
            {
                if (CurSelectModel!=null)
                {
                    return CurSelectModel.Size;
                }
                return 0;
            }
        }

        public Color[] OriginColors
        {
            get
            {
                if (CurSelectModel!=null)
                {
                    return CurSelectModel.OriginColors;
                }
                return null;
            }
        }

        private int mSelectIndex;

        private int SelectIndex
        {
            get
            {
                mSelectIndex = Mathf.Clamp(mSelectIndex,0,Canvas.Count-1);
                return mSelectIndex;
            }
            set
            {
                mSelectIndex = value;
                mSelectIndex = Mathf.Clamp(mSelectIndex,0,Canvas.Count-1);
            }
        }

        public CanvasModel GetSelectCanvasModel()
        {
            if (Canvas.Count > 0)
            {
                if (Canvas.Count<=SelectIndex)
                {
                    SelectIndex = 0;
                }
                return Canvas[SelectIndex];
            }
            return null;
        }

        public Texture2D CanvasTexture2D
        {
            get
            {
                if (CurSelectModel != null)
                {
                    return CurSelectModel.CanvasTexture2D;
                }
                return null;
            }
        }
        public void ApplyColor()
        {
            if (CurSelectModel != null)
            {
                CurSelectModel.ApplyColor();
            }
        }
        public Color[] Colors
        {
            get
            {
                if (CurSelectModel != null)
                {
                    return CurSelectModel.Colors;
                }
                return null;
            }
            set
            {
                if (CurSelectModel != null)
                {
                    CurSelectModel.Colors = value;
                }
            }
        }
        public Color[] GetPixels(Color[] preColors = null)
        {
            if (CurSelectModel != null)
            {
                return CurSelectModel.GetPixels(preColors);
            }
            return null;
        }
        public Vector4 GetPixel(Vector2Int point)
        {
            if (CurSelectModel != null)
            {
                return CurSelectModel.GetPixel(point);
            }

            return Color.clear;
        }
        public Vector4 GetPixel(int x, int y)
        {
            if (CurSelectModel != null)
            {
                return CurSelectModel.GetPixel(x,y);
            }

            return Color.clear;
        }
        public void SetPixel(int x, int y, Color color)
        {
            if (CurSelectModel != null)
            {
                CurSelectModel.SetPixel(x,y,color);
            }
        }

        //设置 刷新
        public void Set(CanvasLayers cs)
        {
            Canvas = cs.Canvas;

            RefreshActive();
        }

        public void RefreshActive()
        {
            if (Canvas.Count > 0)
            {
                for (int index = 0; index < Canvas.Count; index++)
                {
                    Canvas[index].SetActive(Canvas[index].TargetRIActive);
                }
            }
        }

        public void Select(CanvasModel c)
        {
            if (Canvas.Count > 0 && Canvas.Contains(c))
            {
                SelectIndex = Canvas.IndexOf(c);
            }

            CurRawImage = c.TargetRI;
            SelectHandler?.Invoke(c);
        }
        public void Select(int i)
        {
            if (Canvas.Count > 0 && i<= Canvas.Count -1 && i>0)
            {
                SelectIndex = i;

                CurRawImage = Canvas[SelectIndex].TargetRI;
                SelectHandler?.Invoke(Canvas[SelectIndex]);
            }
        }
        public CanvasModel Copy(CanvasModel model)
        {
            if (Canvas.Count >= 10)
            {
                UIHelper.Instance.ShowToast("not_more_than_ten_layer");
                return null;
            }
            
            if (Canvas.Contains(model))
            {
                var index = Canvas.IndexOf(model);

                CanvasModel newModel = null;
                if (model is Canvas256Model)
                {
                    newModel = this.Create<Canvas256Model>();
                }
                else if (model  is Canvas64Model)
                {
                    newModel = this.Create<Canvas256Model>();
                }

                if (newModel == null)
                {
                    return null;
                }
                
                newModel.Colors = model.GetPixels();
                newModel.ApplyColor();
                
                Canvas.Insert(index+1,newModel);
                var Siblingindex = model.TargetRI.transform.GetSiblingIndex() + 1;
                newModel.TargetRI.transform.SetSiblingIndex(Siblingindex);
                
                SelectIndex = index + 1;
                newModel.Name = model.Name;
            
                CurRawImage = Canvas[SelectIndex].TargetRI;
                SelectHandler?.Invoke(Canvas[SelectIndex]);

                return newModel;
            }
            return null;
        }
        public CanvasModel MergeToNext(CanvasModel model)
        {
            if (Canvas.Contains(model))
            {
                var index = Canvas.IndexOf(model);

                if (index <= 0)
                {
                    return model;
                }

                var target = Canvas[index - 1];
                
                
                var cls = PaintService.Instance.CombineTexture(this,model.TargetRI,target.TargetRI);
                GameObject.Destroy(target.TargetRI.gameObject);
                Canvas.Remove(target);
                model.Colors = cls;
                model.ApplyColor();

                return model;
            }
            return null;
        }

        public CanvasModel Add<T>(bool dirty = true) where T:CanvasModel
        {
            var model = Create<T>(dirty);
            if (model != null)
            {
                Add(model);
                model.Name = string.Format("Layer{0}", Canvas.Count());
            }
            return model;
        }
    
        public CanvasModel Create<T>(bool dirty = true) where T:CanvasModel
        {
            var go = GameObject.Instantiate(ORawImage.gameObject);
            go.SetActive(true);
            go.transform.SetParent(ORawImage.transform.parent);
            go.transform.SetAsLastSibling();
            go.transform.localScale = Vector3.one;
            (go.transform as RectTransform).anchoredPosition3D = Vector3.zero;
            if (typeof(T) == typeof(Canvas256Model))
            {
                var m = new Canvas256Model(go.GetComponent<RawImage>());
                return m;
            }
            else if (typeof(T) == typeof(Canvas64Model))
            {
                var m = new Canvas64Model(go.GetComponent<RawImage>(), dirty);
                return m;
            }

            return null;
        }
        
        public void Add(CanvasModel cs)
        {
            if (Canvas.Count >= 10)
            {
                UIHelper.Instance.ShowToast("not_more_than_ten_layer");
                return;
            }
            
            Canvas.Add(cs);
            SelectIndex += 1;
            
            CurRawImage = Canvas[SelectIndex].TargetRI;
            SelectHandler?.Invoke(Canvas[SelectIndex]);
        }
        public void Del(CanvasModel cs)
        {
            if (Canvas.Count <= 1)
            {
                UIHelper.Instance.ShowToast("cannot_del_layer".GetLanguageStr());
                return;
            }

            var index = Canvas.IndexOf(cs);
            if (cs!=null)
            {
                if (index == SelectIndex)
                {
                    SelectIndex -= 1;
                }
                
                GameObject.Destroy(cs.TargetRI.gameObject);
                Canvas.Remove(cs);
                
                CurRawImage = Canvas[SelectIndex].TargetRI;
                SelectHandler?.Invoke(Canvas[SelectIndex]);
            }
        }

        public void Undo()
        {
            if (CurSelectModel!=null)
            {
                CurSelectModel.Undo();
            }
        }
        public bool CanUndo()
        {
            if (CurSelectModel!=null)
            {
                return CurSelectModel.CanUndo();
            }

            return false;
        }
        public void Redo()
        {
            if (CurSelectModel!=null)
            {
                CurSelectModel.Redo();
            }
        }
        public bool CanRedo()
        {
            if (CurSelectModel!=null)
            {
                return CurSelectModel.CanRedo();
            }
            return false;
        }

        public void SaveTextureColorsToCache(UniWorkSaveContext ctx)
        {
            if (CurSelectModel != null)
            {
                CurSelectModel.SaveTextureColorsToCache(ctx);
            }
        }
        public void InitPaintHistory(Color[] cls=null)
        {
            if (CurSelectModel != null)
            {
                CurSelectModel.InitPaintHistory(cls);
            }
        }
        public void DoRecordColor()
        {
            if (CurSelectModel != null)
            {
                CurSelectModel.DoRecordColor();
            }
        }
        public bool DataIsDirty
        {
            get
            {
                if (CurSelectModel != null && CurSelectModel is Canvas64Model canvas)
                {
                    return canvas.DataIsDirty;
                }

                return false;
            }
            set
            {
                if (CurSelectModel != null && CurSelectModel is Canvas64Model)
                {
                    foreach (var v in Canvas)
                    {
                        (v as Canvas64Model).DataIsDirty = value;
                    }
                }
            }

        }
        
        public bool CanvasInfoIsDirty()
        {
            foreach (var vCanva in Canvas)
            {
                for (int i = 0; i < vCanva.OriginColors.Length; i++)
                {
                    if (!UniCommonTool.ColorCompare(vCanva.Colors[i], vCanva.OriginColors[i]))
                    {
                        return true;
                    }
                }
            }
            return false;
        }
        
        public void Dispose()
        {
            if (Canvas == null)
            {
                return;
            }
            foreach (var vCanva in Canvas)
            {
                vCanva?.Dispose();
            }
            Canvas.Clear();
            Canvas = null;
        }
    }
	public class UIPaintingModel : UIModelBase
    {
        public IBoolListenable PenBarActive = new IBoolListenable(true);
        public IBoolListenable EraserBarActive = new IBoolListenable(true);
        public IBoolListenable ShapeBarActive = new IBoolListenable(true);
        public IBoolListenable LassoBarActive = new IBoolListenable(true);
        public IBoolListenable ExtendsBarActive = new IBoolListenable(true);

        public IBoolListenable UndoActive = new IBoolListenable(true);
        public IBoolListenable RedoActive = new IBoolListenable(true);

        public IBoolListenable ColorDiskActive = new IBoolListenable(true);
        public IBoolListenable ColorCurDiskActive = new IBoolListenable(true);
        public IBoolListenable CanvasOverLayerActive = new IBoolListenable(false);

        public IBoolListenable BottomActive = new IBoolListenable(true);
        public IBoolListenable RightActive = new IBoolListenable(true);

        public IBoolListenable AnimActive = new IBoolListenable(true); 
        public IBoolListenable AnimBottomActive = new IBoolListenable(true); 
        public IBoolListenable ProprtyActive = new IBoolListenable(true);
        public IBoolListenable SettingInspector = new IBoolListenable(true);

        public IBoolListenable PreviousFrame = new IBoolListenable(true); 
        public IBoolListenable NextFrame = new IBoolListenable(true); 
        public IBoolListenable CopyFrame = new IBoolListenable(true); 
        public IBoolListenable AddFrame = new IBoolListenable(true); 
        public IBoolListenable DelFrame = new IBoolListenable(true);

        public void RedoUndo(CanvasLayers model)
        {
            if (model != null)
            {
                this.RedoActive.Value = model.CanRedo();
                this.UndoActive.Value = model.CanUndo();
            }
            else
            {
                this.RedoActive.Value = false;
                this.UndoActive.Value = false;
            }
        }

        public void PenBarChange()
        {
            EraserBarActive.Value = false;
            ShapeBarActive.Value = false;
            LassoBarActive.Value = false;
            PenBarActive.Value = !PenBarActive.Value;
            ExtendsBarActive.Value = false;
        }
        public void PeErasernBarChange()
        {
            PenBarActive.Value = false;
            ShapeBarActive.Value = false;
            LassoBarActive.Value = false;
            EraserBarActive.Value = !EraserBarActive.Value;
            ExtendsBarActive.Value = false;
        }
        public void ShapeBarChange()
        {
            PenBarActive.Value = false;
            EraserBarActive.Value = false;
            LassoBarActive.Value = false;
            ShapeBarActive.Value = !ShapeBarActive.Value;
            ExtendsBarActive.Value = false;
        }
        public void LassoBarChange()
        {
            PenBarActive.Value = false;
            EraserBarActive.Value = false;
            ShapeBarActive.Value = false;
            LassoBarActive.Value = !LassoBarActive.Value;
            ExtendsBarActive.Value = false;
        }

        public void ExtendsBarChange()
        {
            PenBarActive.Value = false;
            EraserBarActive.Value = false;
            ShapeBarActive.Value = false;
            LassoBarActive.Value = false;
            ExtendsBarActive.Value = !ExtendsBarActive.Value;
        }

        //todo 合为一个 加动画
        public void SwitchSimpleDisk(bool ishow = true)
        {
            ColorCurDiskActive.Value= ishow;
            ColorDiskActive.Value = !ishow;
        }

        public void CloseScendBar()
        {
            PenBarActive.Value = false;
            EraserBarActive.Value = false;
            ShapeBarActive.Value = false;
            LassoBarActive.Value = false;
            ExtendsBarActive.Value = false;
        }

        public void ShowPicView(UIName thisUI, bool ishow = true)
        {
            ShowScendView(UIName.BudPic,thisUI,ishow);
        }
        public void ShowScendView(UIName uIName, UIName thisUI, bool ishow = true)
        {
            if (ishow)
            {
                UISystem.Inst.ShowUIScene(uIName, thisUI,false);
                this.RightActive.Value = false;
            }
            else
            {
                UISystem.Inst.IsUIActive(uIName, true);
                this.RightActive.Value = true;
            }
        }

        //--------------------Anim----------------
        public void ShowAnim(bool show = true) 
        {
            this.AnimActive.Value = show;
            this.AnimBottomActive.Value = show;
            this.ProprtyActive.Value = false;
            this.SettingInspector.Value = false;
        }

        public void ShowAnimContent(bool show = true)
        {
            this.ProprtyActive.Value = show;
            this.AnimBottomActive.Value = show;
        }

        public void ShowAnimProprty(bool previousFrame, bool nextFrame, bool copyFrame, bool addFrame, bool delFrame)
        {
            this.PreviousFrame.Value = previousFrame;
            this.NextFrame.Value = nextFrame;
            this.CopyFrame.Value = copyFrame;
            this.AddFrame.Value = addFrame;
            this.DelFrame.Value = delFrame;
        }

        private int proprtyStatus;//todo model view 
        public void UpdateGIFProprtyView(int status = 0)
        {
            proprtyStatus = status.Equals(0)?1: proprtyStatus % 2 + 1;
            this.ProprtyActive.Value = proprtyStatus > 1;
        }
        public override void Dispose()
        {
            PenBarActive.Unbind();
            EraserBarActive.Unbind();
            ShapeBarActive.Unbind();
            LassoBarActive.Unbind();
            ColorCurDiskActive.Unbind();
            ColorDiskActive.Unbind();
            AnimActive.Unbind();
            AnimBottomActive.Unbind();
        }

	}
```

`CanvasLayers`

类用于在 Unity 中管理和操作绘画图层。该类包含多个字段和方法，用于处理图层的初始化、选择、复制、合并、撤销、重做、保存等功能。类中定义了一个构造函数 `CanvasLayers`，接受一个 `RawImage` 和一个 `WorkType` 类型的参数，根据工作类型设置当前画布类型。类中还定义了多个属性和方法，用于获取和设置当前选择的画布模型、画布纹理、颜色数据、像素数据等。

`CanvasLayers` 类中的 `LayerRawImage` 属性用于获取和设置图层的 `RawImage`，根据当前画布类型返回相应的 `RawImage`。`CurRawImage` 属性用于获取当前选择的画布模型的 `RawImage`。`CurSelectModel` 属性用于获取和设置当前选择的画布模型。`CurSelectModelIndexOf` 属性返回当前选择的画布模型在画布列表中的索引。`Size` 属性返回当前选择的画布模型的大小。`OriginColors` 属性返回当前选择的画布模型的原始颜色数据。`CanvasTexture2D` 属性返回当前选择的画布模型的纹理。

类中还定义了多个方法，用于操作画布模型和图层。`GetSelectCanvasModel` 方法用于获取当前选择的画布模型。`ApplyColor` 方法用于应用颜色到当前选择的画布模型。`GetPixels` 方法用于获取当前选择的画布模型的像素数据。`GetPixel` 方法用于获取指定位置的像素数据。`SetPixel` 方法用于设置指定位置的像素数据。`Set` 方法用于设置画布图层，并刷新激活状态。`RefreshActive` 方法用于刷新画布图层的激活状态。`Select` 方法用于选择指定的画布模型或索引，并触发选择事件。`Copy` 方法用于复制指定的画布模型，并插入到画布列表中。`MergeToNext` 方法用于将指定的画布模型合并到下一个画布模型。`Add` 方法用于添加新的画布模型。`Create` 方法用于创建新的画布模型。`Del` 方法用于删除指定的画布模型。`Undo` 和 `Redo` 方法分别用于撤销和重做操作。`SaveTextureColorsToCache` 方法用于将纹理颜色保存到缓存。`InitPaintHistory` 方法用于初始化绘画历史记录。`DoRecordColor` 方法用于记录颜色数据。`DataIsDirty` 属性用于获取和设置数据是否已修改。`CanvasInfoIsDirty` 方法用于检查画布信息是否已修改。`Dispose` 方法用于释放画布图层的资源。

在其他文件中，`CanvasLayers` 类被多次引用和使用。例如，在 `GifItem.cs` 文件中，`Refresh` 方法用于刷新 GIF 项，显示或隐藏画布图层的数据。在 `LayerEditManager.cs` 文件中，`CurCanvasLayer` 属性用于获取当前的画布图层，`Refresh` 方法用于刷新画布图层。在 `LayerSet.cs` 文件中，`OnOpen` 方法用于打开图层设置界面，并初始化画布图层和画布模型。在 `MaterialDisplayEditing.cs` 文件中，`OnOpen` 方法用于打开材质显示编辑界面，并初始化画布图层和目标 `RawImage`。

在 `UIPainting.cs` 文件中，`canvasInfos` 字段用于存储当前的画布图层，`gifCanvasList` 字段用于存储 GIF 动画的画布图层列表。`InitPaintService` 方法用于初始化绘画服务，并根据工作类型创建画布图层。`InitEmptyCanvasInfos` 方法用于初始化空的画布图层列表。`ReOpen` 方法用于重新打开绘画界面，并根据工作类型和 GIF 数据初始化画布图层列表。`AddFrame` 方法用于添加新的帧，并插入到 GIF 动画的画布图层列表中。

在 `UIPaintingModel.cs` 文件中，`CanvasLayers` 构造函数用于根据工作类型初始化画布图层。`Set` 方法用于设置画布图层，并刷新激活状态。`RedoUndo` 方法用于更新撤销和重做按钮的状态。在 `PaintService.cs` 文件中，`SaveGifToPng` 方法用于将 GIF 动画保存为 PNG 图片，并上传到服务器。`CombineTexture` 方法用于合并两个 `RawImage` 的纹理，并返回合并后的颜色数据。`CombineCanvasLayers` 方法用于合并画布图层的纹理，并返回合并后的纹理。

总体来说，`CanvasLayers` 类提供了丰富的功能，用于管理和操作绘画图层，包括初始化、选择、复制、合并、撤销、重做、保存等功能。通过这些方法，可以方便地在 Unity 中管理和操作复杂的绘画图层，提高开发效率。



