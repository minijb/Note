---
title: materialDisplayEditing
date: 2026-03-16
tags:
  - untagged
type: knowledge
aliases:
  -
description: public class MaterialDisplayEditing : MonoBehaviour,IPointerDownHandler,IPointerUpHandler
draft: false
---

# materialDisplayEditing

```c#
public class MaterialDisplayEditing : MonoBehaviour,IPointerDownHandler,IPointerUpHandler
{
    private const int CRICLE_ID = 10132;
    private const int RECTANGLE_ID = 10129;
    private const int TRIANGLE_ID = 10141;
    
    private RawImage TargetRawImage;
    private UniSnapshot itemSnapshot = new UniSnapshot();
    private UnityEvent closeEvent ;
    private bool draging;
    private Vector3 prescale;
    private Vector3 preEulerAngles;
    private Camera cam;
    private Vector2 mSizeDelta;
    private RectTransform rwTarget;
    private RawImage rwRtTarget;
    private Canvas PaintCanvas;
    private int id = 0;
    
    [SerializeField]
    private Toggle togCricle;
    [SerializeField]
    private Toggle togRectangle;
    [SerializeField]
    private Toggle togTriangle;

    private void Awake()
    {
        togCricle.onValueChanged.AddListener((b) =>
        {
            DoUpdateObject(CRICLE_ID);
        });
        togRectangle.onValueChanged.AddListener((b) =>
        {
            DoUpdateObject(RECTANGLE_ID);
        });
        togTriangle.onValueChanged.AddListener((b) =>
        {
            DoUpdateObject(TRIANGLE_ID);
        });
    }

    public void OnOpen(CanvasLayers target,RectTransform preRawTarget)
    {
        rwTarget = preRawTarget;
        TargetRawImage = this.GetComponentInChildren<RawImage>();
        itemSnapshot.Init((int)SnapModelType._300X300);
        itemSnapshot.Reset();
        
        closeEvent?.RemoveAllListeners();
        itemSnapshot.DistanceFov = 3;

        //var cur = RTESystem.Inst.ActiveUniObjEdit;
        // if (cur!=null)
        // {
        //     itemSnapshot.avatarToSnapshot = cur.gameObject;
        //     
        //     var matInfo = new MaterialSampleInfo();
        //     matInfo.Initialize();
        //     matInfo.SetName("bud_item_mat_999");
        //     matInfo.SetTexture(target, MaterialValueFlag.MainTexture);
        //     var mat = UniMain.Game.Scene.GetSharedMaterial("model/v2", ref matInfo);
        //     RenderUtility.SetRenderShareMaterial(cur.gameObject,mat);
        // }
        // else
        //{
            cam = Uni.Utility.CaptureSceneRT(UniPhysicsLayer.Mask_UI, UniGameCameras.GetInstance().CaptureCamera,new Vector2(256, 256),CameraClearFlags.Color, newCam:true,rtEqualSize: true);
            cam.gameObject.SetActive(true);
            target.LayerRawImage = CreatAndAddCanvas(cam.transform,cam,rwTarget);
            cam.targetTexture.filterMode = FilterMode.Point;
            cam.targetTexture.wrapMode = TextureWrapMode.Repeat;
            DoUpdateObject(RECTANGLE_ID);
            
        //}
        itemSnapshot.SetLayersRecursively(itemSnapshot.avatarToSnapshot);
        
        itemSnapshot.rectTransform = this.GetComponent<RectTransform>();
        itemSnapshot.UICamera = UniGameCameras.GetInstance()?.GetUICamera();
        itemSnapshot.DragLock = true;
        //prescale = itemSnapshot.avatarToSnapshot.transform.localScale;;
        //preEulerAngles = itemSnapshot.avatarToSnapshot.transform.eulerAngles;
        //itemSnapshot.avatarToSnapshot.transform.localScale = Vector3.one*0.7f;
        togRectangle.isOn = true;
    }

    public void UpdatePreview()
    {
        var snapshotTexture = itemSnapshot.UpdatePreview();
        if (snapshotTexture != null)
        {
            TargetRawImage.texture = snapshotTexture;
            //this.GetComponent<RawImage>().material.SetColor(ShaderColorID, Color.white);
        }
    }
    
    public void OnDisable()
    {
        OnReset();
        id = 0;
        itemSnapshot.avatarToSnapshot.transform.localScale = prescale;
        itemSnapshot.avatarToSnapshot.transform.localScale = preEulerAngles;
        cam.targetTexture.Release();
        itemSnapshot.Close();
        closeEvent?.Invoke();
        itemSnapshot.Reset();
        this.gameObject.SetActive(false);
    }

    private void Update()
    {
        UpdatePreview();

        if (Input.GetKeyDown(KeyCode.UpArrow))
        {
            var mID =id + 1;
            DoUpdateObject(mID);
        }
        else if (Input.GetKeyDown(KeyCode.DownArrow))
        {
            var mID = id - 1;
            DoUpdateObject(mID);
        }
    }

    private void DoUpdateObject(int mId)
    {
        if (mId == id)
        {
            return;
        }
        id = Mathf.Clamp(mId,10100, 10200);
        itemSnapshot.avatarToSnapshot = PaintService.Instance.CreateMatDisplayObject(cam.targetTexture,out closeEvent,id); 
        itemSnapshot.avatarToSnapshot.transform.localScale = Vector3.one * 0.78f;//1/1.414会有边
        itemSnapshot.avatarToSnapshot.transform.eulerAngles = new Vector3(30, 30, 0);
        closeEvent.AddListener(()=>GameObject.Destroy(cam.gameObject));
    }


    public void OnPointerDown(PointerEventData eventData)
    {
        itemSnapshot.DragLock = false;
    }

    private RawImage CreatAndAddCanvas(Transform uiParent,Camera camera,RectTransform rwTarget)
    {
        var size = new Vector2(256, 256);
        GameObject mParent = null;
        if (PaintCanvas!=null)
        {
            mParent = PaintCanvas.transform.parent.gameObject;
        }
        if (mParent == null)
        {
            mParent = new GameObject("PaintCanvas");
            mParent.layer = LayerMask.NameToLayer("UI");
            mParent.transform.SetParent(uiParent);
            //waringParent.transform.localPosition = new Vector3(0, -370, 0);
            mParent.transform.localScale = Vector3.one;
            PaintCanvas = mParent.AddComponent<Canvas>();
            PaintCanvas.renderMode = RenderMode.ScreenSpaceCamera;
            PaintCanvas.worldCamera = camera;
            PaintCanvas.overrideSorting = true;
            PaintCanvas.sortingOrder = 100;
            var canvasScaler = mParent.gameObject.AddComponent<CanvasScaler>();
            canvasScaler.uiScaleMode = CanvasScaler.ScaleMode.ScaleWithScreenSize;
            canvasScaler.referenceResolution = size;
            canvasScaler.referencePixelsPerUnit = 100;
            canvasScaler.matchWidthOrHeight = 0;
        }

        var go = GameObject.Instantiate(rwTarget.gameObject);
        go.SetActive(true);
        go.transform.SetParent(rwTarget.transform.parent);
        go.transform.SetAsLastSibling();
        go.transform.localScale = Vector3.one;
        (go.transform as RectTransform).anchoredPosition3D = Vector3.zero;
        rwRtTarget = go.GetComponent<RawImage>();
        rwRtTarget.texture = camera.targetTexture;
        
        mSizeDelta = rwTarget.sizeDelta;
        rwTarget.transform.SetParent(PaintCanvas.transform);
        rwTarget.sizeDelta = size;

        return rwRtTarget;
    }

    private void OnReset()
    {
        id = 10129;
        rwTarget.SetParent(rwRtTarget.transform.parent);
        rwTarget.sizeDelta = mSizeDelta;
        rwTarget.transform.localScale = Vector3.one;
        GameObject.Destroy(rwRtTarget);
    }

    public void OnPointerUp(PointerEventData eventData)
    {
        itemSnapshot.DragLock = true;
        itemSnapshot.UnDraging();
    }
```

`MaterialDisplayEditing`

类继承自 `MonoBehaviour` 并实现了 `IPointerDownHandler` 和 `IPointerUpHandler` 接口，用于在 Unity 中管理和操作材质显示编辑界面。该类包含多个字段和方法，用于处理材质显示对象的初始化、更新、预览、拖动、重置等功能。

类中定义了几个常量，包括 `CRICLE_ID`、`RECTANGLE_ID` 和 `TRIANGLE_ID`，分别表示圆形、矩形和三角形的 ID。类中还定义了多个私有字段，包括 `TargetRawImage`、`itemSnapshot`、`closeEvent`、`draging`、`prescale`、`preEulerAngles`、`cam`、`mSizeDelta`、`rwTarget`、`rwRtTarget`、`PaintCanvas` 和 `id`，用于存储材质显示对象的相关信息和状态。

在 `Awake` 方法中，设置了三个切换按钮的事件监听器，当切换按钮的值发生变化时，调用 `DoUpdateObject` 方法更新材质显示对象。`OnOpen` 方法用于打开材质显示编辑界面，接受两个参数：目标画布图层 `target` 和预先设置的 `RectTransform` `preRawTarget`。方法中初始化了 `rwTarget` 和 `TargetRawImage`，重置了 `itemSnapshot`，并设置了相机和画布的相关属性。然后，调用 `DoUpdateObject` 方法更新材质显示对象，并设置默认的矩形切换按钮为选中状态。

`UpdatePreview` 方法用于更新材质显示对象的预览图像。方法中调用 `itemSnapshot.UpdatePreview` 方法获取快照纹理，并将其设置为目标 `RawImage` 的纹理。`OnDisable` 方法在材质显示编辑界面禁用时调用，重置材质显示对象的状态，释放相机的目标纹理，并关闭 `itemSnapshot`。

`Update` 方法在每帧更新时调用，更新材质显示对象的预览图像，并根据用户按下的方向键更新材质显示对象的 ID。`DoUpdateObject` 方法用于更新材质显示对象，接受一个整数类型的参数 `mId`，表示材质显示对象的 ID。方法中检查传入的 ID 是否与当前 ID 相同，如果不同，则更新 ID 并创建新的材质显示对象。

`OnPointerDown` 方法在用户按下指针时调用，解锁 `itemSnapshot` 的拖动锁定。`CreatAndAddCanvas` 方法用于创建并添加画布，接受三个参数：UI 父对象 `uiParent`、相机 `camera` 和 `RectTransform` `rwTarget`。方法中初始化了画布的相关属性，并将目标 `RawImage` 的纹理设置为相机的目标纹理。

`OnReset` 方法用于重置材质显示对象的状态，将目标 `RectTransform` 的父对象设置为原始父对象，并恢复其大小和缩放比例。最后，销毁目标 `RawImage`。`OnPointerUp` 方法在用户抬起指针时调用，锁定 `itemSnapshot` 的拖动锁定，并调用 `itemSnapshot.UnDraging` 方法停止拖动。

总体来说，`MaterialDisplayEditing` 类提供了丰富的功能，用于管理和操作材质显示编辑界面，包括初始化、更新、预览、拖动、重置等功能。通过这些方法，可以方便地在 Unity 中管理和操作材质显示对象，提高开发效率。