
```c#
[RequireComponent(typeof(Image))]
public class PaintingTouch : MonoBehaviour, IDisposable
{
    //UniLogger Logger = UniLogManager.Get(name: nameof(PaintingTouch));
    public bool CanPinchPan;
    public bool CanRotate;
    public float MinZoomSize =0.5f;
    public RectTransform Target 
    {
        set
        {
            m_Target = value;
            resolutionX = m_Target.sizeDelta.x;
            resolutionY = m_Target.sizeDelta.y;
        }
    }
    private RectTransform m_Target;
    public RectTransform TargetBG;

    public delegate void TouchPicEventHandler(Vector2 pos);
    public event TouchPicEventHandler OnPinchDown;
    public event TouchPicEventHandler OnPinchUp;
    public event TouchPicEventHandler OnPinchOnDrag;
    public event TouchPicEventHandler OnPinchClick;
    public event Action OnGestureChange;

    private MulTouchHandler m_Touch;
    private float resolutionX;
    private float resolutionY;

    bool isClick;
    bool beginPinch;
    bool beginPan;
    bool beginPinchPan;
    bool beginZoom;
    bool beginRotate;

    Vector2 panBeginCenter;
    Vector3 panBeginPicPos;
    Vector2 startData;

    float zoomBeginSize;
    float zoomBeginScale;
    

    private void Awake()
    {
        if (!this.gameObject.TryGetComponent(out m_Touch))
        {
            m_Touch = this.gameObject.AddComponent<MulTouchHandler>();
        }

        m_Touch.OnFingerAdded += OnStartGesture;
        m_Touch.OnFingerRemoved += OnFingerUp;
    }
    
    private void OnStartGesture(int touchCount, MulTouchHandler sender)
    {
        if (touchCount == 1)
        {
            isClick = true;
            var fc = sender.GetFingerCombination(0);
            fc.OnChange += OnChangePinchGesture;
        }
        else if (touchCount == 2)
        {
            isClick = false; 
            var fc = sender.GetFingerCombination(0, 1);
            fc.OnChange += OnChangeGesture;
        }
        startData = sender.Center;
        OnPinchDown?.Invoke(sender.Center);
    }
    private void OnChangePinchGesture(MyGesture gesture, FingerCombination sender)
    {
        isClick = false;
        if (m_Touch.FingersCount() != 1)
        {
            return;
        }
        if (!beginPinch)
        {
            beginPinch = true;
        }
        if (CanPinchPan)
        {
            if (!beginPinchPan)
            {
                RectTransformUtility.ScreenPointToWorldPointInRectangle(m_Target as RectTransform,sender.Center, UniGameCameras.GetInstance().GetUICamera(), out var pos);
                panBeginPicPos = this.m_Target.position - pos;
                beginPinchPan = true;
            }
            else
            {
                OnPan(gesture, sender);
            }
        }
        //OnPinchOnDrag?.Invoke(startData);
        OnPinchOnDrag?.Invoke(sender.Center);
    }

    //热更新修复
    private float GetTouchSize(FingerCombination sender)
    {
        if (sender.Data.Count < 2) return 0;
        var magnitudeSum = 0f;
        for (int i = 1; i < sender.Data.Count; i++)
        {
            Camera camera = UniGameCameras.GetInstance().GetUICamera();
            RectTransformUtility.ScreenPointToLocalPointInRectangle(m_Target.parent as RectTransform, sender.Data[0].position, camera, out var pos1);
            RectTransformUtility.ScreenPointToLocalPointInRectangle(m_Target.parent as RectTransform, sender.Data[1].position, camera, out var pos2);
            var dif = pos2-pos1;
            magnitudeSum += dif.magnitude;
        }
        return magnitudeSum / (sender.Data.Count - 1);
    }
    private void OnChangeGesture(MyGesture gesture, FingerCombination sender)
    {
        if (!beginPan)
        {
            RectTransformUtility.ScreenPointToWorldPointInRectangle(m_Target as RectTransform, sender.Center, UniGameCameras.GetInstance().GetUICamera(), out var pos);
            panBeginPicPos = this.m_Target.position - pos;
            beginPan = true;
        }
        else
        {
            OnPan(gesture, sender);
        }

        if (!beginZoom)
        {
            //热更包修复

            zoomBeginSize = GetTouchSize(sender);
            zoomBeginScale = m_Target.transform.localScale.x;
            beginZoom = true;
        }
        else
        {
            OnZoom(gesture, sender);
        }
        if (CanRotate)
        {
            OnRotate(gesture, sender);
        }
        OnGestureChange?.Invoke();

    }
    private void OnFingerUp(int touchCount, MulTouchHandler sender)
    {
        if (isClick) 
        {
            OnPinchClick?.Invoke(sender.Center);
            isClick = false;
        }
        if (touchCount == 0)
        {
            if (beginPinch)
            {
                beginPinch = false;
                OnPinchUp?.Invoke(sender.Center);
            }
        }
        
        if (touchCount != 1)
        {
            beginPinchPan = false;
        }

        if (touchCount != 2)
        {
            beginPan = false;
            beginZoom = false;
        }
    }
    private void OnZoom(MyGesture gesture, FingerCombination sender)
    {
        var newSize = GetTouchSize(sender);
        if (newSize > 0)
        {
            float newScale = Screen.height * 0.5f;
            newScale = zoomBeginScale / newScale * (newSize- zoomBeginSize + newScale);
            newScale = Mathf.Clamp(newScale, MinZoomSize, 32);//todo fixdata
            if (TargetBG)
            {
                this.TargetBG.transform.localScale = this.m_Target.transform.localScale / Mathf.Abs(newScale);
                this.TargetBG.sizeDelta = this.m_Target.sizeDelta * Mathf.Abs(newScale)+Vector2.one*10f;
            }
            this.m_Target.transform.localScale = newScale * Vector3.one;
        }
    }
    private void OnPan(MyGesture gesture, FingerCombination sender)
    {
        if (sender.Gesture.CenterDelta.magnitude > 0)
        {
            RectTransformUtility.ScreenPointToWorldPointInRectangle(m_Target as RectTransform, sender.Center, UniGameCameras.GetInstance().GetUICamera(), out var pos);
            this.m_Target.position = pos + panBeginPicPos;
        }
    }
    private void OnRotate(MyGesture gesture, FingerCombination sender)
    {
        var angle = -gesture.AngleDelta;
        if (Mathf.Abs(angle) > 0.01f)
        {
            this.m_Target.localEulerAngles= new Vector3(this.m_Target.localEulerAngles.x, this.m_Target.localEulerAngles.y, this.m_Target.localEulerAngles.z - angle);
        }
    }
    
    protected void OnDestroy()
    {
    }

    public void Dispose()
    {
    }
}
```

`PaintingTouch`

类继承自 `MonoBehaviour` 并实现了 `IDisposable` 接口，用于在 Unity 中处理触摸手势操作。该类依赖于 `Image` 组件，并包含多个字段和方法，用于处理缩放、平移、旋转等手势操作。

类中定义了几个公共字段，包括 `CanPinchPan` 和 `CanRotate`，用于指示是否允许缩放和平移以及是否允许旋转。`MinZoomSize` 用于设置最小缩放比例。`Target` 属性用于设置目标 `RectTransform`，并更新分辨率。`TargetBG` 用于存储背景的 `RectTransform`。类中还定义了几个事件，包括 `OnPinchDown`、`OnPinchUp`、`OnPinchOnDrag`、`OnPinchClick` 和 `OnGestureChange`，用于处理不同的手势操作。

在 `Awake` 方法中，尝试获取 `MulTouchHandler` 组件，如果未找到则添加该组件。然后，订阅 `OnFingerAdded` 和 `OnFingerRemoved` 事件，分别处理手势开始和手指抬起的操作。

`OnStartGesture` 方法根据触摸点的数量处理手势开始操作。如果触摸点为一个，则设置 `isClick` 为 `true` 并订阅 `OnChangePinchGesture` 事件。如果触摸点为两个，则设置 `isClick` 为 `false` 并订阅 `OnChangeGesture` 事件。然后，触发 `OnPinchDown` 事件。

`OnChangePinchGesture` 方法处理单指手势变化操作。如果触摸点数量不为一个，则返回。否则，设置 `beginPinch` 为 `true`。如果允许缩放和平移，则计算平移开始位置，并调用 `OnPan` 方法处理平移操作。最后，触发 `OnPinchOnDrag` 事件。

`GetTouchSize` 方法用于计算触摸点之间的距离，用于缩放操作。`OnChangeGesture` 方法处理双指手势变化操作，包括平移、缩放和旋转。如果未开始平移，则计算平移开始位置并设置 `beginPan` 为 `true`。如果未开始缩放，则计算缩放开始大小和比例，并设置 `beginZoom` 为 `true`。然后，调用 `OnZoom` 方法处理缩放操作。如果允许旋转，则调用 `OnRotate` 方法处理旋转操作。最后，触发 `OnGestureChange` 事件。

`OnFingerUp` 方法处理手指抬起操作。如果 `isClick` 为 `true`，则触发 `OnPinchClick` 事件并重置 `isClick`。如果触摸点数量为零，则重置 `beginPinch` 并触发 `OnPinchUp` 事件。如果触摸点数量不为一个，则重置 `beginPinchPan`。如果触摸点数量不为两个，则重置 `beginPan` 和 `beginZoom`。

`OnZoom` 方法根据触摸点之间的距离计算新的缩放比例，并应用到目标 `RectTransform`。如果存在背景，则同步更新背景的缩放和大小。`OnPan` 方法根据触摸点的位置计算新的平移位置，并应用到目标 `RectTransform`。`OnRotate` 方法根据手势的角度变化计算新的旋转角度，并应用到目标 `RectTransform`。

`OnDestroy` 方法在组件销毁时调用，默认实现为空。`Dispose` 方法用于释放资源，默认实现为空。通过这些方法，`PaintingTouch` 类提供了丰富的功能，用于处理触摸手势操作，包括缩放、平移和旋转等操作。