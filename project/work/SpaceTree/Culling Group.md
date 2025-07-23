
如何使用 Culling Group 进行剔除

https://unitycoder.com/blog/2018/10/31/find-nearby-objects-using-cullinggroup/
https://www.bilibili.com/video/BV1eC6GYYEE4/?spm_id_from=333.1007.tianma.1-1-1.click&vd_source=8beb74be6b19124f110600d2ce0f3957

```c#
using UnityEngine;
using System.Collections;

public class CullingGroupExample : MonoBehaviour
{
    void Start()
    {
        // 创建一个CullingGroup，使用默认的相机作为参考点
        CullingGroup cullingGroup = new CullingGroup();

        // 设置CullingGroup的事件处理回调
        cullingGroup.onStateChanged += OnStateChanged;

        // 定义距离阈值，这些值将定义不同的距离带
        int[] bounds = {10, 20, 30};

        // 设置距离带
        cullingGroup.SetBoundingDistances(bounds);

        // 开始使用CullingGroup
        cullingGroup.SetBoundingSpheres(new Vector3[] { new Vector3(0, 0, 0) }, new float[] { 50f });



        // 激活CullingGroup
        cullingGroup.SetActive(true);
    }

    void OnStateChanged(CullingGroupEvent cullingGroupEvent)
    {
        // 检查事件类型
        switch (cullingGroupEvent.EventType)
        {
            case CullingGroupEvent.EventType.becameVisible:
                Debug.Log("物体变得可见: " + cullingGroupEvent.AffectedObject.name);
                break;
            case CullingGroupEvent.EventType.becameInvisible:
                Debug.Log("物体变得不可见: " + cullingGroupEvent.AffectedObject.name);
                break;
            case CullingGroupEvent.EventType.becameActive:
                Debug.Log("物体变得活跃: " + cullingGroupEvent.AffectedObject.name);
                break;
            case CullingGroupEvent.EventType.becameInactive:
                Debug.Log("物体变得不活跃: " + cullingGroupEvent.AffectedObject.name);
                break;
        }
    }

    void OnDestroy()
    {
        // 当对象销毁时，移除CullingGroup
        CullingGroup[] cullingGroups = FindObjectsOfType<CullingGroup>();
        foreach (CullingGroup cg in cullingGroups)
        {
            cg.RemoveObject(gameObject);
            cg.Dispose();
        }
    }
}
```

### CullingGroupEvent

`CullingGroupEvent` 是 Unity 中的一个结构体，它提供了有关 `CullingGroup` 中一个球体的当前和先前状态的信息 。这个结构体通常用于 `CullingGroup.onStateChanged` 事件的回调中，以便开发者能够在球体的可见性或距离状态发生变化时得到通知并执行相应的操作 。

以下是 `CullingGroupEvent` 结构体的成员及其作用 ：

1. **index**: 表示发生变化的球体的索引。
2. **wasVisible**: 在最近一次剔除通道之前，该球体是否可见。
3. **isVisible**: 在最近一次剔除通道之后，该球体是否可见。
4. **hasBecomeVisible**: 在最近一次剔除通道中，该球体是否从不可见变为可见。
5. **hasBecomeInvisible**: 在最近一次剔除通道中，该球体是否从可见变为不可见。
6. **previousDistance**: 在最近一次剔除通道之前，该球体的距离带索引。
7. **currentDistance**: 在最近一次剔除通道之后，该球体的当前距离带索引。

这些信息允许开发者了解球体相对于摄像机的可见性和距离变化，并据此做出响应。例如，当一个球体从不可见变为可见时，开发者可能会激活与该球体相关联的游戏对象，或者当球体进入特定的距离带时，调整其细节层次（LOD）。通过这种方式，`CullingGroupEvent` 提供了一种有效的方法来优化游戏性能，特别是在处理大量对象和复杂场景时 。


## 两个触发器   OnBecameVisible 与 OnBecameInvisible

当物体在/进入摄像机会调用一次，  当物体离开摄像机会调用一次