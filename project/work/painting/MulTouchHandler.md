
```c#
public class MulTouchHandler : MonoBehaviour, IPointerDownHandler, IDragHandler, IPointerUpHandler
{
    public List<Finger> Fingers = new List<Finger>();
    public List<FingerCombination> FingerCombinations = new List<FingerCombination>();
    public bool NeedGesture;//手势开关
    public FingerCombination GetFingerCombination(params int[] fingerIndices)
    {
        var fc = FingerCombinations.Find(x => x.IDs.Count == fingerIndices.Length && fingerIndices.All(y => x.IDs.Contains(Fingers[y].ID)));
        if (fc != null) return fc;

        fc = new FingerCombination()
        {
            Fingers = fingerIndices.Select(x => Fingers[x]).ToList()
        };
        fc.IDs = fc.Fingers.Select(x => x.ID).ToList();
        fc.Data = Fingers.Select(x => x.Data).ToList();
        fc.PreviousData = Fingers.Select(x => x.Data).ToList();
        FingerCombinations.Add(fc);
        return fc;
    }

    public delegate void MultitouchEventHandler(int touchCount, MulTouchHandler sender);
    public event MultitouchEventHandler OnFingerAdded;
    public event MultitouchEventHandler OnFingerRemoved;
    public int TouchCount()
    {
        return Fingers.Count;
    }
    public void OnDrag(PointerEventData eventData)
    {
        var finger = Fingers.Find(x => x.ID == eventData.pointerId);
        var fcs = FingerCombinations.Where(x => x.IDs.Contains(eventData.pointerId));

        finger.PreviousData = finger.Data;
        finger.Data = eventData;

        foreach (var fc in fcs)
        {
            fc.PreviousData = fc.Data;
            fc.Data = fc.Fingers.Select(x => x.Data).ToList();
            fc.PreGesture = fc.Gesture;
            fc.Gesture = new MyGesture()
            {
                Center = fc.Center,
                Size = fc.Size,
                Angle = fc.Angle,
                SizeDelta = 1
            };
            if (fc.PreGesture != null)
            {
                fc.Gesture.PosDelta = fc.Size - fc.PreGesture.Size;
                fc.Gesture.CenterDelta = fc.Center - fc.PreGesture.Center;
                fc.Gesture.SizeDelta = fc.Size / fc.PreGesture.Size;

                var angle = fc.Angle - fc.PreGesture.Angle;
                fc.Gesture.AngleDelta = angle>180 ? (angle-360) : (angle < -180 ? angle + 360 : angle);

            }

            fc.Changed();
        }
    }
    public void OnPointerDown(PointerEventData eventData)
    {
        var finger = new Finger() { ID = eventData.pointerId, Data = eventData };
        Fingers.Add(finger);
         
        if (OnFingerAdded != null)
            OnFingerAdded(Fingers.Count, this);

    }
    public void OnPointerUp(PointerEventData eventData)
    {
        if (OnFingerRemoved != null)
            OnFingerRemoved(Fingers.Count- Fingers.Where(x => x.ID == eventData.pointerId).Count(), this);

        Fingers.RemoveAll(x => x.ID == eventData.pointerId);

        var fcs = FingerCombinations.Where(x => x.IDs.Contains(eventData.pointerId));
        foreach (var fc in fcs)
        {
            fc.Finished();
        }

        FingerCombinations.RemoveAll(x => x.IDs.Contains(eventData.pointerId));
    }
    public class Finger
    {
        public int ID;
        public PointerEventData Data;
        public PointerEventData PreviousData;
    }
    public class FingerCombination
    {
        public List<int> IDs = new List<int>();
        public List<Finger> Fingers;
        public List<PointerEventData> PreviousData;
        public List<PointerEventData> Data;

        public delegate void GestureEventHandler(MyGesture gesture, FingerCombination sender);
        public event GestureEventHandler OnChange;
        public delegate void GestureEndHandler(FingerCombination sender);
        public event GestureEndHandler OnFinish;

        public MyGesture Gesture;
        public MyGesture PreGesture;

        public Vector2 Center
        {
            get { return Data.Aggregate(Vector2.zero, (x, y) => x + y.position) / Data.Count; }
        }

        public float Size
        {
            get
            {
                if (Data.Count == 1) return 0;
                var magnitudeSum = 0f;
                for (int i = 1; i < Data.Count; i++)
                {
                    var dif = (Data[i].position - Data[0].position);
                    magnitudeSum += dif.magnitude;
                }
                return magnitudeSum / (Data.Count - 1);
            }
        }

        public float Angle
        {
            get
            {
                if (Data.Count == 1) return 0;
                var angleSum = 0f;
                for (int i = 1; i < Data.Count; i++)
                {
                    var dif = (Data[i].position - Data[0].position);
                    angleSum += Mathf.Atan2(dif.y, dif.x) * Mathf.Rad2Deg;
                }
                return angleSum / (Data.Count - 1);
            }
        }

        internal void Changed()
        {
            if (OnChange != null)
                OnChange.Invoke(Gesture, this);
        }

        internal void Finished()
        {
            if (OnFinish != null)
                OnFinish.Invoke(this);
        }
    }
    public class MyGesture
    {
        public Vector2 Center;
        public float Size;
        public float Angle;

        public float PosDelta;
        public Vector2 CenterDelta;
        public float SizeDelta;
        public float AngleDelta;
    }
    public PointerEventData GetFingerData(int index)
    {
        return Fingers[index].Data;
    }
    public int FingersCount()
    {
        return Fingers.Count;
    }

    public Vector2 Center
    {
        get { return Fingers.Aggregate(Vector2.zero, (x, y) => x + y.Data.position) / Fingers.Count; }
    }

    public float Size
    {
        get
        {
            if (Fingers.Count == 1) return 0;
            var magnitudeSum = 0f;
            for (int i = 1; i < Fingers.Count; i++)
            {
                var dif = (Fingers[i].Data.position - Fingers[0].Data.position);
                magnitudeSum += dif.magnitude;
            }
            return magnitudeSum / (Fingers.Count - 1);
        }
    }
}
```

`MulTouchHandler`

类继承自 `MonoBehaviour` 并实现了 `IPointerDownHandler`、`IDragHandler` 和 `IPointerUpHandler` 接口，用于在 Unity 中处理多点触控手势操作。该类包含多个字段和方法，用于管理手指触控数据、手势组合以及触控事件的处理。

类中定义了两个列表：`Fingers` 和 `FingerCombinations`，分别用于存储当前触控的手指数据和手势组合。`NeedGesture` 是一个布尔字段，用于指示是否需要处理手势。`GetFingerCombination` 方法用于获取指定手指索引的手势组合，如果不存在则创建新的手势组合并添加到 `FingerCombinations` 列表中。

类中定义了一个委托 `MultitouchEventHandler` 和两个事件 `OnFingerAdded` 和 `OnFingerRemoved`，用于处理手指添加和移除的事件。`TouchCount` 方法返回当前触控的手指数量。`OnDrag` 方法用于处理拖动事件，更新手指数据和手势组合的数据，并计算手势的变化量，然后触发手势变化事件。

`OnPointerDown` 方法用于处理手指按下事件，创建新的手指数据并添加到 `Fingers` 列表中，然后触发手指添加事件。`OnPointerUp` 方法用于处理手指抬起事件，触发手指移除事件并从 `Fingers` 列表中移除对应的手指数据，同时触发手势完成事件并从 `FingerCombinations` 列表中移除对应的手势组合。

类中还定义了三个内部类：`Finger`、`FingerCombination` 和 `MyGesture`。`Finger` 类用于存储手指的 ID 和触控数据。`FingerCombination` 类用于存储手势组合的数据，包括手指列表、触控数据、手势数据和手势变化事件。`MyGesture` 类用于存储手势的中心点、大小、角度以及变化量。

`FingerCombination` 类中定义了几个属性和方法，用于计算手势的中心点、大小和角度，并触发手势变化和完成事件。`Center` 属性返回手势的中心点，`Size` 属性返回手势的大小，`Angle` 属性返回手势的角度。`Changed` 方法用于触发手势变化事件，`Finished` 方法用于触发手势完成事件。

`MulTouchHandler` 类通过实现 `IPointerDownHandler`、`IDragHandler` 和 `IPointerUpHandler` 接口，处理触控事件并管理手指数据和手势组合。通过这些方法和事件，可以方便地在 Unity 中处理多点触控手势操作，包括拖动、缩放和旋转等操作。