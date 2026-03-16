
```c#
public class PaintService : Singleton<PaintService>, IPaintService
{
    //private enum PaintingMode 
    //{
    //    shader,
    //    computeShader
    //}
    //private PaintingMode paintingMode = PaintingMode.computeShader;
    private IPaintService baseServicebase;
    private Material ImageMergeMat;
    private int ShaderId_MainTex = Shader.PropertyToID("_MainTex");
    private int ShaderId_OverlayTex = Shader.PropertyToID("_OverlayTex");
    private int ShaderId_OverlayPosition = Shader.PropertyToID("_OverlayPosition");
    private int ShaderId_OverlayRotation = Shader.PropertyToID("_OverlayRotation");
    private int ShaderId_OverlayScale = Shader.PropertyToID("_OverlayScale");
    UniLogger Logger = UniLogManager.Get<PaintService>();
    private GameObject mTakeShotSphere;
    private GameObject matEditPreviewObject;
    private Material mPreviewMaterial;
    private Material mTakeShotCubeMaterial;
    private UniNode previewObject;

    public PaintService()
    {
        //var res = BudEditRes.Load();
        //if (paintingMode == PaintingMode.computeShader)
        //{
        //    baseServicebase = new ComputeShaderPaint();
        //}
    }

    public void UpdateColors(CanvasModel canvasModel)
    {
        //baseServicebase?.UpdateColors(canvasModel);
        if (canvasModel.GpuComputeMode)
        {
            if (baseServicebase == null)
            {
                baseServicebase = new ComputeShaderPaint();
            }

            baseServicebase.UpdateColors(canvasModel);
        }
        else
        {
            canvasModel.CanvasTexture2D.SetPixels(canvasModel.Colors);
            canvasModel.CanvasTexture2D.Apply();
        }
    }

    public Color[] TextureToColorInfo(int width, int height, Texture2D tex = null)
    {
        ////computeshader不用再画了
        //Graphics.Blit(tex, canvasModel.CanvasTexture);
        if (tex && tex.isReadable)
        {
            //tex.filterMode = FilterMode.Point;
            Texture2D texture2d = new Texture2D(width, height, tex.format, false);
            Color[] colors = texture2d.GetPixels(0);
            float incX = (1.0f / (float)width);
            float incY = (1.0f / (float)height);
            var fl4s = new Color[colors.Length];
            for (int px = 0; px < colors.Length; px++)
            {
                colors[px] = tex.GetPixelBilinear(incX * ((float)px % width), incY * ((float)Mathf.Floor(px / height)));
                fl4s[px] = colors[px];
            }

            Texture2D.Destroy(texture2d);
            return fl4s;
        }
        else
        {
            var fl4s = new Color[width * height];
            for (int px = 0; px < fl4s.Length; px++)
            {
                fl4s[px] = new Vector4(0, 0, 0, 0);
            }

            return fl4s;
        }
    }

    public Vector4 ColorToVector4(Color color)
    {
        return new Vector4(color.r, color.g, color.b, color.a);
    }

    public Color Vector4ToColor(Vector4 color)
    {
        return new Color(color.x, color.y, color.z, color.w);
    }

    public void TextureToPng(WorkType workType, string name, string des, bool isOpen, List<Texture2D> canvasModels,
        UnityAction successCallback = null,
        UnityAction failedCallback = null)
    {
        //try
        //{
        //    if (canvasModel.CanvasTexture != null)
        //    {
        //        TextureToPng(workType,Name, canvasModel.CanvasTexture, successCallback, failedCallback);
        //    }
        //    else
        //    {
        //        //Graphics.Blit(texture,);
        //        byte[] bytes = canvasModel.CanvasTexture2D.EncodeToPNG();
        //        byte[] iconBytes = canvasModel.CanvasTexture2D.EncodeToPNG();
        //        SaveTextureToPng(workType,Name, iconBytes, bytes, successCallback, failedCallback);
        //    }
        //}
        //catch (IOException ex)
        //{
        //    Logger.Error("转换PNG失败:" + ex);
        //}
    }

    public void SaveTextureToPng(WorkType workType, string name, string des, bool isOpen, Texture2D CanvasTexture2D,
        Texture2D eTexture2D, List<UniNodeRefInfo> refList, UnityAction successCallback = null,
        UnityAction failedCallback = null,
        Uni.Application.UI.PrivateEnum publishState = Uni.Application.UI.PrivateEnum.publish)
    {
        try
        {
            // if (canvasModel.CanvasTexture != null)
            // {
            //     TextureToPng(workType, name, des, isOpen, canvasModel.CanvasTexture, successCallback, failedCallback);
            // }
            // else
            {
                //Graphics.Blit(texture,);
                byte[] bytes = CanvasTexture2D?.EncodeToPNG();
                byte[] iconBytes = CanvasTexture2D?.EncodeToPNG();
                if (bytes != null || iconBytes != null)
                {
                    var data = new UploadData()
                    {
                        workType = workType,
                        name = name,
                        des = des,
                        isOpen = isOpen,
                        textureBytes = bytes,
                        iconBytes = iconBytes,
                        exBytes = eTexture2D?.EncodeToPNG(),
                        refList = refList
                    };
                    SaveTextureToPng(data, successCallback, failedCallback, publishState);
                    return;
                }
            }
        }
        catch (IOException ex)
        {
            Logger.Error("转换PNG失败:" + ex);
        }

        failedCallback?.Invoke();
    }

    //todo 结构体
    public void SaveGifToPng(WorkType workType, string name, string des, bool isOpen, List<CanvasLayers> gifCanvasList,
        List<UniNodeRefInfo> refList, UniGIFDataInfo data, UnityAction successCallback = null,
        UnityAction failedCallback = null,
        Uni.Application.UI.PrivateEnum publishState = Uni.Application.UI.PrivateEnum.publish)
    {
        try
        {
            var textures = new List<Texture2D>();
            foreach (var layer in gifCanvasList)
            {
                if (layer.DataIsDirty)
                {
                    textures.Add(PaintService.Instance.CombineCanvasLayers(layer));
                }
            }

            data.MaxTotalFrame = textures.Count;
            byte[] iconBytes = MergeTexturesToGif(textures).EncodeToPNG();
            // iconBytes = UniComponentHelper.WirteToPng(iconBytes, data);

            string jsonStr = LitJson.JsonMapper.ToJson(data);
            var jsonBytes = System.Text.Encoding.UTF8.GetBytes(jsonStr);
            iconBytes = UniCommonTool.AddBytesToPNG(iconBytes, jsonBytes);

            //UniEditorHelper.ReadPngData(iconBytes);
            byte[] bytes = GifUtility.GifEncode(textures, data.FrameRate);
            //System.IO.File.WriteAllBytes(Application.streamingAssetsPath + "/textdds.gif", bytes);
            //return;
            if (bytes != null || iconBytes != null)
            {
                byte[] pngbytes = textures.First().EncodeToPNG();

                var gifData = new UploadData()
                {
                    workType = workType,
                    name = name,
                    des = des,
                    isOpen = isOpen,
                    textureBytes = pngbytes,
                    iconBytes = iconBytes,
                    exBytes = bytes,
                    refList = refList
                };
                SaveTextureToPng(gifData, successCallback, failedCallback, publishState);
                return;
            }
        }
        catch (IOException ex)
        {
            Logger.Error("转换PNG失败:" + ex);
        }

        failedCallback?.Invoke();
    }
    // public void TextureToPng(WorkType workType, string name, string des, bool isOpen, RenderTexture rt, UnityAction successCallback = null,
    //     UnityAction failedCallback = null, Uni.Application.UI.PrivateEnum publishState = Uni.Application.UI.PrivateEnum.publish)
    // {
    //     try
    //     {
    //         //var rt = new RenderTexture(,);
    //         int width = rt.width;
    //         int height = rt.height;
    //         var rt2 = RenderTexture.GetTemporary(width, height, 0, RenderTextureFormat.ARGB32);
    //         rt2.enableRandomWrite = true;
    //         rt2.filterMode = FilterMode.Point;
    //         Graphics.Blit(rt, rt2);
    //         rt = rt2;
    //         Texture2D texture2D = new Texture2D(width, height, TextureFormat.ARGB32, false);
    //         //Graphics.CopyTexture(rt, texture2D);
    //         RenderTexture.active = rt;
    //         texture2D.filterMode = FilterMode.Point;
    //         texture2D.ReadPixels(new Rect(0, 0, width, height), 0, 0);
    //
    //         texture2D.Apply();
    //         //Graphics.Blit(texture,);
    //         byte[] bytes = texture2D.EncodeToPNG();
    //         Texture2D.Destroy(texture2D);
    //         RenderTexture.ReleaseTemporary(rt2);
    //         RenderTexture.active = null;
    //         if (bytes != null)
    //         {
    //             var texData = new UploadData()
    //             {
    //                 workType = workType,
    //                 name = name,
    //                 des = des,
    //                 isOpen = isOpen,
    //                 textureBytes = bytes,
    //                 iconBytes = null,
    //                 exBytes = null
    //             };
    //             SaveTextureToPng(texData, successCallback, failedCallback, publishState);
    //             return;
    //         }
    //
    //     }
    //     catch (IOException ex)
    //     {
    //         Logger.Error("转换PNG失败:" + ex);
    //     }
    //     successCallback?.Invoke();
    // }

    //todo 代码合并
    void CreateNewTextureOnRemote(UploadData data, UnityAction succCallback = null, UnityAction failCallBack = null,
        Uni.Application.UI.PrivateEnum publishState = Uni.Application.UI.PrivateEnum.publish)
    {
        var workUpload = UniAssetUploader.Create<UniWorkUpLoader>(UniMain.Game);
        workUpload.IsNewContent = true;
        workUpload.Type = data.workType;
        workUpload.SetParameters(data.workType);
        workUpload.Parameters["open"] = data.isOpen ? 1 : 0;
        if(data.des != null)
            workUpload.Parameters["intro"] = data.des;
        workUpload.Parameters["name"] = data.name;
        workUpload.Parameters["private"] = (int)publishState;
        ToRefListData(workUpload, data.refList);
        if (data.textureBytes != null)
            workUpload.UpCoverData = data.textureBytes;
        if (data.iconBytes != null)
            workUpload.UpSpriteData = data.iconBytes;
        if (data.exBytes != null)
            workUpload.UpGifData = data.exBytes;

        workUpload.onFinished.AddListener((l) =>
        {
            if (l.Status == UniAssetLoaderStatus.Loaded)
            {
                if (l.CodeSucc())
                {
                    //UniMain.UserMe.QueryBag(null);
                    succCallback?.Invoke();
                }
                else //服务器返回错误码
                {
                    failCallBack?.Invoke();
                }
            }
            else //网络失败
            {
                failCallBack?.Invoke();
            }
        });
        workUpload.Upload();
    }

    private void ToRefListData(UniWorkUpLoader uniWorkUpLoader, List<UniNodeRefInfo> refInfos)
    {
        if (refInfos == null)
            return;
        var model_list_cs = new HashSet<string>();
        if (refInfos.Count > 0)
        {
            foreach (var refUGC in refInfos)
            {
                model_list_cs.Add($"{refUGC.RefId}-{refUGC.RefVersion}");
            }

            var model_list = new LitJson.JsonData();
            model_list.SetJsonType(LitJson.JsonType.Array);
            foreach (var refUGC in model_list_cs)
            {
                model_list.Add(refUGC);
            }

            uniWorkUpLoader.Parameters["model_list"] = model_list;
        }
    }

    public struct UploadData
    {
        public WorkType workType;
        public string name;
        public string des;
        public bool isOpen;
        public byte[] textureBytes;
        public byte[] iconBytes;
        public byte[] exBytes;
        public List<UniNodeRefInfo> refList;
    }

    //todo 代码合并
    void UpdateTextureOnRemote(UploadData data, UnityAction succCallback = null, UnityAction failCallBack = null,
        Uni.Application.UI.PrivateEnum publishState = Uni.Application.UI.PrivateEnum.publish)
    {
        var workUpload = UniAssetUploader.Create<UniWorkUpLoader>(UniMain.Game);
        workUpload.WorkId = UniMain.Game.Work.Id;
        workUpload.WorkVersion = UniMain.Game.Work.Version;
        workUpload.Type = data.workType;
        workUpload.SetParameters(data.workType);
        workUpload.Parameters["open"] = data.isOpen ? 1 : 0;
        if(data.des != null)
            workUpload.Parameters["intro"] = data.des;
        workUpload.Parameters["name"] = data.name;
        workUpload.Parameters["private"] = (int)publishState;
        ToRefListData(workUpload, data.refList);

        if (data.textureBytes != null)
            workUpload.UpCoverData = data.textureBytes;
        if (data.iconBytes != null)
            workUpload.UpSpriteData = data.iconBytes;
        if (data.exBytes != null)
            workUpload.UpGifData = data.exBytes;

        workUpload.IsNewContent = false;
        workUpload.onFinished.AddListener((l) =>
        {
            if (l.Status == UniAssetLoaderStatus.Loaded)
            {
                if (l.CodeSucc())
                {
                    //UniMain.UserMe.QueryBag(null);
                    succCallback?.Invoke();
                }
                else //服务器返回错误码
                {
                    failCallBack?.Invoke();
                }
            }
            else //网络失败
            {
                failCallBack?.Invoke();
            }
        });
        workUpload.Upload();
    }

    // public T MergeLayers<T>(List<CanvasModel> canvasModels) where T:CanvasModel
    // {
    //     if (canvasModels == null || canvasModels.Count <= 0)
    //     {
    //         return null;
    //     }
    //     if (canvasModels.Count <= 1)
    //     {
    //         return canvasModels.First() as T;
    //     }
    //
    //     new CanvasModel = canvasModels；
    //     CombineCanvasLayers(canvasModels);
    //
    //     // foreach (var VARIABLE in COLLECTION)
    //     // {
    //     //     
    //     // }
    //     var cm = canvasModels.First();
    //     
    //     cm.Colors = cls;
    //     cm.ApplyColor();
    //     
    //     return cm as T;
    // }

    public void SaveAndSharePic(Texture tex, bool isShare = false)
    {
        if (isShare)
        {
            Dictionary<string, object> dic = new Dictionary<string, object>();
            dic.Add("page_name", ConstValue.SHUSHU_PAGE_WORLD_SCENE);
            dic.Add("action", "share_model");
            dic.Add("type", "6");
            dic.Add("channel", "system");
            dic.Add("content", "picture");
            dic.Add("platform", "unity");
            UniMain.TrackEvent.UploadStatistics("share", () => dic);
        }
        else
        {
            Dictionary<string, object> dic = new Dictionary<string, object>();
            dic.Add("page_name", ConstValue.SHUSHU_PAGE_WORLD_SCENE);
            dic.Add("action", "share_model");
            dic.Add("type", "6");
            dic.Add("channel", "download");
            dic.Add("content", "picture");
            dic.Add("platform", "unity");
            UniMain.TrackEvent.UploadStatistics("share", () => dic);
        }

        var player = UniMain.Game.Players.GetLocalPlayer();
        GameObject waterMaskGo = UniMain.AssetModule.SyncLoad<GameObject>("prefabs/item/pic_watermask.unity3d");
        var timeSpan = System.DateTime.Now - new DateTime(1970, 1, 1, 0, 0, 0, 0);
        Int64 curTime = Convert.ToInt64(timeSpan.TotalSeconds);
        String savePath = Uni.UniCachePath.GetCacheFile(UniCachePathType.Cover, curTime + "_save.jpg");
        if (waterMaskGo)
        {
            var waterMaskGoo = GameObject.Instantiate(waterMaskGo);
            //waterMaskGoo.transform.position = new Vector3(10000, 0, 0);
            waterMaskGoo.name = "waterMaskGo";

            Transform raw = waterMaskGoo.transform.UniFindChildByName("rawImg_texture");
            Transform auther = waterMaskGoo.transform.UniFindChildByName("txt_author");
            if (raw && auther)
            {
                RawImage raw1 = raw.GetComponent<RawImage>();
                raw1.texture = tex;
                UnityEngine.UI.Text text = auther.GetComponent<UnityEngine.UI.Text>();
                text.text = "@" + player.CharacterInfo.Name;
            }

            Camera renderCamera = waterMaskGo.transform.UniFind("Camera").GetComponent<Camera>();
            //renderCamera.clearFlags = CameraClearFlags.Depth;
            int width = 720; //256;
            int height = 773; //275;
            RenderTexture texture = RenderTexture.GetTemporary(width, height, 0, RenderTextureFormat.ARGB32);

            renderCamera.targetTexture = texture;
            renderCamera.Render();
            RenderTexture.active = texture;

            Texture2D tex2D = new Texture2D(width, height);
            Rect rect = new Rect(0, 0, width, height);
            //Rect rect = new Rect(anchoredPosition.x, Screen.height - anchoredPosition.y - sizeDelta.y, sizeDelta.x, sizeDelta.y);
            tex2D.ReadPixels(rect, 0, 0);
            tex2D.Apply();

            renderCamera.targetTexture = null;
            RenderTexture.active = null;
            RenderTexture.ReleaseTemporary(texture);
            GameObject.Destroy(waterMaskGoo);
            var data = tex2D.EncodeToJPG();
            Texture2D.Destroy(tex2D);
            //Uni.Global.GLogger.Error(savePath);
            System.IO.File.WriteAllBytes(savePath, data);

            if (!isShare)
                UIHelper.Instance.ShowToast("Display_Download_sucsses".GetLanguageStr());
        }

        //下载到本地
        Uni.UniNative.DownloadPicture(savePath, player.CharacterInfo.UID + "_" + curTime, "1", isShare);
    }

    public void SaveTextureToPng(UploadData data, UnityAction succCallback, UnityAction failCallBack,
        Uni.Application.UI.PrivateEnum publishState = Uni.Application.UI.PrivateEnum.publish)
    {
        string saveId = string.Empty;

        if ((UniMain.Game.Scene.WorkingType == WorkType.Painting || UniMain.Game.Scene.WorkingType == WorkType.GIF ||
             UniMain.Game.Scene.WorkingType == WorkType.Material) && !string.IsNullOrEmpty(UniMain.Game.Work.Id))
        {
            UpdateTextureOnRemote(data, succCallback, failCallBack, publishState);
        }
        else
        {
            CreateNewTextureOnRemote(data, succCallback, failCallBack, publishState);
        }

        // try
        // {
        //     if (!string.IsNullOrEmpty(saveId))
        //     {
        //         var tName = saveId + AppConst.image_type;
        //         var url = UniMain.NetworkSetting.GetUploadImageUrl() + "?cover=1";
        //         var loader = UniMain.RpcManager.UploadCoverImage(bytes, url, tName);
        //         if(loader == null)return UniAsyncResult<bool>.DefaultFail;
        //         await loader.WaitCompleted();
        //         if(loader.Status != UniAssetLoaderStatus.Loaded)
        //         {
        //             return loader.GetDefaultAsyncResult();
        //         }
        //         UniMain.UserMe.QueryBag(null);
        //         //remove cache
        //         string cachePath = UniCachePath.GetCacheFile(UniCachePathType.Painting,"temp.png");
        //         if(System.IO.File.Exists(cachePath))
        //         {
        //             try
        //             {
        //                 System.IO.File.Delete(cachePath);
        //             }
        //             catch
        //             {
        //             }
        //         }
        //         return UniAsyncResult<bool>.Succ(true);
        //     }
        // }
        // catch (IOException ex)
        // {
        //     Debug.LogException(ex);
        // }
        // return UniAsyncResult<bool>.DefaultFail;
    }

    public Texture2D SpawnCapture(int width, int height, Color[] pixls)
    {
        Texture2D result = new Texture2D(width, height, TextureFormat.RGBA32, false);
        result.SetPixels(pixls);
        result.Apply();
        result.filterMode = FilterMode.Point;
        return result;
    }

    public Color[] CombineTexture(CanvasLayers canvasLayers, RawImage image2,RawImage image1 = null)
    {
        if (!image1)
        {
            image1 = canvasLayers.CurRawImage;
        }
        if (!ImageMergeMat)
        {
            var res = BudEditRes.Load();
            ImageMergeMat = res.GetImageMergeMat();
        }

        RenderTexture renderTexture =
            RenderTexture.GetTemporary(image1.texture.width, image1.texture.height, 0, RenderTextureFormat.ARGB32);
        renderTexture.enableRandomWrite = true;
        renderTexture.filterMode = FilterMode.Point;

        ImageMergeMat.SetTexture(ShaderId_MainTex, image1.texture);
        ImageMergeMat.SetTexture(ShaderId_OverlayTex, image2.texture);
        ImageMergeMat.SetVector(ShaderId_OverlayPosition,
            GetRelativePosition(canvasLayers.LayerRawImage.rectTransform, image2.rectTransform));
        ImageMergeMat.SetFloat(ShaderId_OverlayRotation,
            GetRotation(canvasLayers.LayerRawImage.rectTransform, image2.rectTransform));
        ImageMergeMat.SetVector(ShaderId_OverlayScale,
            GetScale(canvasLayers.LayerRawImage.rectTransform, image2.rectTransform));

        //var oldWrapMode2 = image2.texture.wrapMode;
        //image2.texture.wrapMode = TextureWrapMode.Repeat;
        //var oldWrapMode = image1.texture.wrapMode;
        //image1.texture.wrapMode = TextureWrapMode.Repeat;
        Graphics.Blit(image1.texture, renderTexture, ImageMergeMat);
        //image1.texture.wrapMode = oldWrapMode;
        //image2.texture.wrapMode= oldWrapMode2;

        var rt2 = RenderTexture.GetTemporary(renderTexture.width, renderTexture.height, 0, RenderTextureFormat.ARGB32);
        rt2.enableRandomWrite = true;
        rt2.filterMode = FilterMode.Point;
        Graphics.Blit(renderTexture, rt2);
        renderTexture = rt2;

        Texture2D result = new Texture2D(image1.texture.width, image1.texture.height, TextureFormat.RGBA32, false);
        result.ReadPixels(new Rect(0f, 0f, renderTexture.width, renderTexture.height), 0, 0);
        result.Apply();

        RenderTexture.ReleaseTemporary(renderTexture);
        RenderTexture.ReleaseTemporary(rt2);

        return result.GetPixels();
    }

    public Texture2D ScaleTo256Texture(Texture2D texture2)
    {
        if (texture2.width == 256 && texture2.height == 256)
        {
            return texture2;
        }

        Texture2D texture1 = new Texture2D(256, 256, TextureFormat.RGBA32, false);
        texture1.SetPixels(new Color[256 * 256]);
        texture1.Apply();
        if (!ImageMergeMat)
        {
            var res = BudEditRes.Load();
            ImageMergeMat = res.GetImageMergeMat();
        }

        RenderTexture renderTexture =
            RenderTexture.GetTemporary(texture1.width, texture1.height, 0, RenderTextureFormat.ARGB32);
        renderTexture.enableRandomWrite = true;
        renderTexture.filterMode = FilterMode.Point;

        ImageMergeMat.SetTexture(ShaderId_MainTex, texture1);
        ImageMergeMat.SetTexture(ShaderId_OverlayTex, texture2);
        ImageMergeMat.SetVector(ShaderId_OverlayPosition, Vector4.zero);
        ImageMergeMat.SetFloat(ShaderId_OverlayRotation, 0);

        ImageMergeMat.SetVector(ShaderId_OverlayScale,
            new Vector4(texture1.width / texture2.width, texture1.height / texture2.height, 1, 1));

        //var oldWrapMode2 = image2.texture.wrapMode;
        //image2.texture.wrapMode = TextureWrapMode.Repeat;
        //var oldWrapMode = image1.texture.wrapMode;
        //image1.texture.wrapMode = TextureWrapMode.Repeat;
        Graphics.Blit(texture1, renderTexture, ImageMergeMat);
        //image1.texture.wrapMode = oldWrapMode;
        //image2.texture.wrapMode= oldWrapMode2;

        var rt2 = RenderTexture.GetTemporary(renderTexture.width, renderTexture.height, 0, RenderTextureFormat.ARGB32);
        rt2.enableRandomWrite = true;
        rt2.filterMode = FilterMode.Point;
        Graphics.Blit(renderTexture, rt2);
        renderTexture = rt2;

        texture1.ReadPixels(new Rect(0f, 0f, renderTexture.width, renderTexture.height), 0, 0);
        texture1.Apply();

        RenderTexture.ReleaseTemporary(renderTexture);
        RenderTexture.ReleaseTemporary(rt2);

        return texture1;
    }

    public Texture2D CombineCanvasLayers(CanvasLayers canvasLayers)
    {
        if (canvasLayers.Canvas.Count <= 0)
        {
            return null;
        }

        var tex1 = canvasLayers.Canvas.First().CanvasTexture2D;

        if (canvasLayers.Canvas.Count <= 1)
        {
            return tex1;
        }

        var image1 = canvasLayers.Canvas.First().TargetRI;

        if (!ImageMergeMat)
        {
            var res = BudEditRes.Load();
            ImageMergeMat = res.GetImageMergeMat();
        }

        RenderTexture renderTexture =
            RenderTexture.GetTemporary(image1.texture.width, image1.texture.height, 0, RenderTextureFormat.ARGB32);
        renderTexture.enableRandomWrite = true;
        renderTexture.filterMode = FilterMode.Point;
        Texture2D result = new Texture2D(image1.texture.width, image1.texture.height, TextureFormat.RGBA32, false);
        RenderTexture rt2;
        result.SetPixels(tex1.GetPixels());
        result.Apply();
        RawImage image2;

        for (int i = 1; i < canvasLayers.Canvas.Count; i++)
        {
            //tex1 = canvasLayers.Canvas[i].CanvasTexture2D;
            image1 = canvasLayers.Canvas[i - 1].TargetRI;
            image2 = canvasLayers.Canvas[i].TargetRI;

            ImageMergeMat.SetTexture(ShaderId_MainTex, result);
            ImageMergeMat.SetTexture(ShaderId_OverlayTex, image2.texture);
            ImageMergeMat.SetVector(ShaderId_OverlayPosition,
                GetRelativePosition(image1.rectTransform, image2.rectTransform));
            ImageMergeMat.SetFloat(ShaderId_OverlayRotation, GetRotation(image1.rectTransform, image2.rectTransform));
            ImageMergeMat.SetVector(ShaderId_OverlayScale,
                GetScale(canvasLayers.LayerRawImage.rectTransform, image2.rectTransform));

            //var oldWrapMode2 = image2.texture.wrapMode;
            //image2.texture.wrapMode = TextureWrapMode.Repeat;
            //var oldWrapMode = image1.texture.wrapMode;
            //image1.texture.wrapMode = TextureWrapMode.Repeat;
            Graphics.Blit(result, renderTexture, ImageMergeMat);
            //image1.texture.wrapMode = oldWrapMode;
            //image2.texture.wrapMode= oldWrapMode2;

            rt2 = RenderTexture.GetTemporary(renderTexture.width, renderTexture.height, 0, RenderTextureFormat.ARGB32);
            rt2.enableRandomWrite = true;
            rt2.filterMode = FilterMode.Point;
            Graphics.Blit(renderTexture, rt2);
            renderTexture = rt2;

            result.ReadPixels(new Rect(0f, 0f, renderTexture.width, renderTexture.height), 0, 0);
            result.Apply();
            RenderTexture.ReleaseTemporary(rt2);
        }


        RenderTexture.ReleaseTemporary(renderTexture);

        return result;
    }

    private Vector4 GetScale(RectTransform image1, RectTransform image2)
    {
        // var canvasScale = image2.GetComponentInParent<Canvas>().transform.InverseTransformVector(image1.GetComponentInParent<Canvas>().transform.lossyScale);
        // //获取image2在image1局部坐标系中的缩放比例
        // Vector3 scale = Vector3.Scale(canvasScale,image1.InverseTransformVector(image2.lossyScale));
        Vector3 scale = image1.InverseTransformVector(image2.lossyScale);

        // scale = image2.localScale;

        //获取image1的宽高，用于计算相对缩放比例
        float width = image1.rect.width;
        float height = image1.rect.height;

        //计算image应该缩放的相对比例
        float newWidth = scale.x * image2.rect.width / width;
        float newHeight = scale.y * image2.rect.height / height;

        return new Vector4(1 / newWidth, 1 / newHeight, 1, 1);
    }

    private Vector2 GetRelativePosition(RectTransform image1, RectTransform image2)
    {
        //获取image2在Canvas中的位置
        Vector3 image2Pos = image2.position;
        //将image2的位置转换为相对于image1的局部坐标系的相对位置
        Vector3 localPos = image1.InverseTransformPoint(image2Pos);
        //将归一化值映射到(-0.5, -0.5)到(0.5,0.5) UV坐标
        return new Vector2(localPos.x / image1.rect.width, localPos.y / image1.rect.height);
    }

    private float GetRotation(RectTransform image1, RectTransform image2)
    {
        //获取image2相对于image1的旋转角度
        Vector3 euler = image2.rotation.eulerAngles - image1.rotation.eulerAngles;
        //转成弧度
        float rotation = euler.z * Mathf.Deg2Rad;

        return rotation;
    }

    public Texture2D MergeTexturesToGif(List<Texture2D> textures, int maxRows = 4, int maxColumns = 4, int spacingX = 0,
        int spacingY = 0)
    {
        int textureWidth = textures[0].width;
        int textureHeight = textures[0].height;

        int rowCount = Mathf.CeilToInt((float)textures.Count / maxColumns);
        int combinedWidth = Mathf.Min(maxColumns, textures.Count) * (textureWidth + spacingX) - spacingX;
        int combinedHeight = rowCount * (textureHeight + spacingY) - spacingY;

        Texture2D combinedTexture = new Texture2D(combinedWidth, combinedHeight);
        combinedTexture.filterMode = FilterMode.Point;

        Color[] combinedPixels = new Color[combinedWidth * combinedHeight];

        for (int i = 0; i < textures.Count; i++)
        {
            int row = i / maxColumns;
            int column = i % maxColumns;

            int startX = column * (textureWidth + spacingX);
            int startY = (rowCount - row - 1) * (textureHeight + spacingY); // Reverse the row index

            Color[] pixels = textures[i].GetPixels();

            for (int y = 0; y < textureHeight; y++)
            {
                for (int x = 0; x < textureWidth; x++)
                {
                    int combinedX = startX + x;
                    int combinedY = startY + y;

                    combinedPixels[combinedY * combinedWidth + combinedX] = pixels[y * textureWidth + x];
                }
            }
        }

        combinedTexture.SetPixels(combinedPixels);
        combinedTexture.Apply();

        return combinedTexture;
    }

    public List<Color[]> SplitCombinedTexture(Texture2D combinedTexture, int maxCount = 16, int originalWidth = 64,
        int originalHeight = 64, int maxRows = 4, int maxColumns = 4, int spacingX = 0, int spacingY = 0)
    {
        List<Color[]> splitTextures = new List<Color[]>();

        int combinedWidth = combinedTexture.width;
        int combinedHeight = combinedTexture.height;

        int textureWidth = originalWidth;
        int textureHeight = originalHeight;

        int rowCount = Mathf.CeilToInt((float)combinedHeight / textureHeight);
        int columnCount = Mathf.CeilToInt((float)combinedWidth / textureWidth);

        for (int row = rowCount; row > 0; row--)
        {
            for (int column = 0; column < columnCount; column++)
            {
                int startX = column * (textureWidth + spacingX);
                int startY = (row - 1) * (textureHeight + spacingY);

                if (startX + textureWidth <= combinedWidth && startY + textureHeight <= combinedHeight)
                {
                    Texture2D newTexture = new Texture2D(textureWidth, textureHeight);
                    newTexture.filterMode = FilterMode.Point;

                    Color[] pixels = new Color[textureWidth * textureHeight];

                    for (int y = 0; y < textureHeight; y++)
                    {
                        for (int x = 0; x < textureWidth; x++)
                        {
                            int combinedX = startX + x;
                            int combinedY = startY + y;

                            pixels[y * textureWidth + x] = combinedTexture.GetPixel(combinedX, combinedY);
                        }
                    }

                    splitTextures.Add(pixels);

                    if (splitTextures.Count >= maxCount)
                        return splitTextures;
                }
            }
        }

        return splitTextures;
    }

    public void GetWorkClipData(Action<Texture2D, byte[]> callback)
    {
        if (UniMain.Game.Scene.Work.Type != WorkType.GIF)
            return;
        string str = BudLoadHelper.GetSpriteDownloadUrl(UniMain.Game.Work.Id, UniMain.Game.Work.Version);
        DownloadImg.DownloadTexture2D2(null, str, UniMain.Game.Work.Meta.SpriteMD5, (loader) =>
        {
            if (loader.Texture != null)
            {
                callback.Invoke(loader.Texture, loader.ExtraData);
            }
        }, false, true);
    }

    public void GetWorkPicData(Action<Texture2D> callback)
    {
        if (UniMain.Game.Scene.Work.Type == WorkType.Painting || UniMain.Game.Scene.WorkingType == WorkType.Material)
        {
            var idStr = UniEditorHelper.GetImageVersionId(UniMain.Game.Work.Id, UniMain.Game.Work.Version);
            string url = string.Format("{0}/bud/{1}.png", UniMain.NetworkSetting.DownloadImageUrl(), idStr);
            DownloadImg.DownloadTexture2D2(null, url, UniMain.Game.Work.Meta.SpriteMD5, (loader) =>
            {
                if (loader.Texture != null)
                {
                    callback.Invoke(ScaleTo256Texture(loader.Texture));
                }
            }, false, true);
        }
    }

    public Texture2D ToMatTakeShot(Texture2D tex)
    {
        if (tex)
        {
            previewObject = GetMatPreviewObject(tex);
            previewObject.transform.localScale = new Vector3(1, 1.1f, 1);
            previewObject.gameObject.SetActive(true);

            Texture2D t2D;
            if (UniMain.GMain.IsEditMode())
            {
                var previewUtil = IOC.Resolve<IResourcePreviewUtility>();
                var recWidth = previewUtil.PreviewWidth;
                var recHeight = previewUtil.PreviewHeight;
                var recPreviewObjectScale = previewUtil.PreviewObjectScale;
                
                previewUtil.PreviewWidth = 256;
                previewUtil.PreviewHeight = 256;
                previewUtil.PreviewObjectScale = 0.75f * Vector3.one;
                previewUtil.Camera.GetUniversalAdditionalCameraData()?.SetRenderer(2);
                var size = Mathf.Sqrt(2) / 2 / 0.75f;
                t2D = previewUtil.CreatePreview(previewObject.gameObject, false,orthographicSize:size);
                
                previewUtil.PreviewWidth = recWidth;
                previewUtil.PreviewHeight = recHeight;
                previewUtil.PreviewObjectScale = recPreviewObjectScale;
            }
            else
            {
                t2D = UniRuntimePreviewGenerator.GenerateModelPreviewInternal(previewObject.gameObject, 256, 256);
            }


            previewObject.gameObject.SetActive(false);
            return t2D;
        }

        return null;
    }

    public UniNode GetMatPreviewObject(Texture2D tex)
    {
        if (tex)
        {
            if (!previewObject)
            {
                previewObject = AvatarUtility.LoadVirtualOfficialEmptyNode(10129,null);
                //previewSphere = BudLoadHelper.LoadBud("10132",out Material[] materials);
                if (UniMain.GMain.IsEditMode())
                {
                    previewObject.transform.SetParent(RTESystem.Inst.transform);
                }

                previewObject.name = "UNI_PreviewMat_Object";
                previewObject.transform.localScale = Vector3.one;
            }

            previewObject.gameObject.SetActive(true);

            var matInfo = new MaterialSampleInfo();
            matInfo.Initialize();
            matInfo.SetName("bud_item_mat_999");
            matInfo.SetTexture(tex, MaterialValueFlag.MainTexture);
            if (!mPreviewMaterial)
            {
                mPreviewMaterial = UniMain.Game.Scene.GetSharedMaterial("model/v2", ref matInfo);
            }
            matInfo.ApplayToMaterial(mPreviewMaterial);
            RenderUtility.SetRenderShareMaterial(previewObject.gameObject, mPreviewMaterial);

            return previewObject;
        }

        return null;
    }

    public GameObject CreateMatDisplayObject(Texture tex, out UnityEvent closeEvent, int id = 10129)
    {
        closeEvent = new UnityEvent();
        closeEvent.AddListener(() =>
        {
            matEditPreviewObject?.gameObject.SetActive(false);
        });
        return CreateTakeShotObject(tex,id);
    }
    public GameObject CreateTakeShotObject(Texture tex, int id = 10129)
    {
        if (!matEditPreviewObject || matEditPreviewObject.name != id.ToString())
        {
            var preGo = BudLoadHelper.LoadBud(id.ToString(), out Material[] materials);
            if (!preGo)
            {
                return matEditPreviewObject;
            }

            if (matEditPreviewObject)
            {
                GameObject.Destroy(matEditPreviewObject.gameObject);
            }

            matEditPreviewObject = preGo;
            if (UniMain.GMain.IsEditMode())
            {
                matEditPreviewObject.transform.SetParent(RTESystem.Inst.transform);
            }

            matEditPreviewObject.name = id.ToString();
            matEditPreviewObject.transform.localScale = Vector3.one;
            matEditPreviewObject.transform.position = Vector3.one * 1000f;
        }

        matEditPreviewObject.gameObject.SetActive(true);

        var uniMatInfo = new MaterialSampleInfo();
        uniMatInfo.Initialize();
        uniMatInfo.SetName("bud_item_mat_999");
        uniMatInfo.SetTexture(tex, MaterialValueFlag.MainTexture);
        uniMatInfo.IsStatic = false;
        uniMatInfo.SetColor(Color.white, MaterialValueFlag.Color);
        uniMatInfo.DisableKeyword(MaterialKeyword.AUTOUV_ON);

        uniMatInfo.SetTilingValue(1);
        uniMatInfo.SetAutoTilingValue(1);
        uniMatInfo.DisableKeyword(MaterialKeyword.DITHER_LOCAL_ON);
        uniMatInfo.SetInt(0, MaterialValueFlag.TintModel);
        //var mat = UniMain.Game.Scene.GetSharedMaterial(new UniVisualComponentMaterialData(),mTakeShotCube.GetInstanceID());
        if(!mTakeShotCubeMaterial)
            mTakeShotCubeMaterial = UniMain.Game.Scene.GetSharedMaterial("model/v2", ref uniMatInfo);
        mTakeShotCubeMaterial.SetInt("_VertOffsetSwitch", 0);
        uniMatInfo.ApplayToMaterial(mTakeShotCubeMaterial);
        RenderUtility.SetRenderShareMaterial(matEditPreviewObject, mTakeShotCubeMaterial);
        return matEditPreviewObject;
    }
    public override void Dispose()
    {
    }
}
```

`PaintService`

类继承自 `Singleton<PaintService>` 并实现了 `IPaintService` 接口，用于在 Unity 中管理和操作绘画服务。该类包含多个字段和方法，用于处理绘画操作、颜色更新、纹理合并、图像保存和分享等功能。

类中定义了多个私有字段，包括 `baseServicebase`、`ImageMergeMat`、`ShaderId_MainTex`、`ShaderId_OverlayTex`、`ShaderId_OverlayPosition`、`ShaderId_OverlayRotation`、`ShaderId_OverlayScale`、`Logger`、`mTakeShotSphere`、`matEditPreviewObject`、`mPreviewMaterial`、`mTakeShotCubeMaterial` 和 `previewObject`，用于存储绘画服务的相关信息和状态。

`UpdateColors` 方法用于更新画布模型的颜色。如果画布模型启用了 GPU 计算模式，则使用 `ComputeShaderPaint` 更新颜色；否则，直接设置画布模型的像素颜色并应用。

`TextureToColorInfo` 方法用于将纹理转换为颜色信息。方法中检查纹理是否可读，如果可读，则获取纹理的像素颜色并返回；否则，返回一个全黑的颜色数组。

`ColorToVector4` 和 `Vector4ToColor` 方法分别用于在颜色和向量之间进行转换。

`TextureToPng` 方法用于将纹理保存为 PNG 文件。方法中包含了注释掉的代码，表示该方法尚未实现。

`SaveTextureToPng` 方法用于将纹理保存为 PNG 文件，并上传到服务器。方法中检查纹理是否为空，如果不为空，则将纹理编码为 PNG 格式，并调用 `SaveTextureToPng` 方法上传。

`SaveGifToPng` 方法用于将 GIF 动画保存为 PNG 文件，并上传到服务器。方法中遍历 GIF 动画的每一帧，将其合并为一个纹理，并编码为 PNG 格式，然后调用 `SaveTextureToPng` 方法上传。

`CreateNewTextureOnRemote` 方法用于在远程服务器上创建新的纹理。方法中创建一个 `UniWorkUpLoader` 对象，并设置其参数和上传数据，然后调用 `Upload` 方法上传。

`ToRefListData` 方法用于将引用列表数据转换为 JSON 格式，并添加到上传参数中。

`UpdateTextureOnRemote` 方法用于在远程服务器上更新现有的纹理。方法中创建一个 `UniWorkUpLoader` 对象，并设置其参数和上传数据，然后调用 `Upload` 方法上传。

`SaveAndSharePic` 方法用于保存和分享图片。方法中根据是否分享，上传统计数据，并将图片保存到本地或分享。

`SpawnCapture` 方法用于生成捕获的纹理。方法中创建一个新的 `Texture2D` 对象，并设置其像素颜色和过滤模式，然后返回该纹理。

`CombineTexture` 方法用于合并两个纹理。方法中使用 `ImageMergeMat` 材质将两个纹理合并到一个 `RenderTexture` 中，然后读取像素颜色并返回。

`ScaleTo256Texture` 方法用于将纹理缩放到 256x256 大小。方法中使用 `ImageMergeMat` 材质将纹理缩放到目标大小，然后读取像素颜色并返回。

`CombineCanvasLayers` 方法用于合并画布图层。方法中遍历画布图层，将每个图层的纹理合并到一个 `RenderTexture` 中，然后读取像素颜色并返回。

`GetScale` 方法用于计算两个 `RectTransform` 之间的缩放比例。

`GetRelativePosition` 方法用于计算两个 `RectTransform` 之间的相对位置。

`GetRotation` 方法用于计算两个 `RectTransform` 之间的旋转角度。

`MergeTexturesToGif` 方法用于将多个纹理合并为一个 GIF 动画。方法中遍历纹理列表，将每个纹理的像素颜色合并到一个新的 `Texture2D` 对象中，然后返回该纹理。

`SplitCombinedTexture` 方法用于将合并的纹理拆分为多个原始纹理。方法中遍历合并纹理的每一行和每一列，将像素颜色拆分到多个新的 `Texture2D` 对象中，然后返回颜色数组列表。

`GetWorkClipData` 方法用于获取工作剪辑数据。方法中根据工作类型下载纹理，并调用回调函数返回纹理和额外数据。

`GetWorkPicData` 方法用于获取工作图片数据。方法中根据工作类型下载纹理，并调用回调函数返回缩放后的纹理。

`ToMatTakeShot` 方法用于生成材质预览图像。方法中获取材质预览对象，并使用预览工具生成预览图像，然后返回该图像。

`GetMatPreviewObject` 方法用于获取材质预览对象。方法中加载虚拟节点，并设置材质预览对象的属性，然后返回该对象。

`CreateMatDisplayObject` 方法用于创建材质显示对象。方法中创建一个拍摄对象，并设置关闭事件，然后返回该对象。

`CreateTakeShotObject` 方法用于创建拍摄对象。方法中加载预设对象，并设置材质和属性，然后返回该对象。

`Dispose` 方法用于释放资源，默认实现为空。