
回调点

![jpg](https://zh.esotericsoftware.com/img/spine-runtimes-guide/spine-unity/callbackchart.png)

`Spine.AnimationState` 和 `TrackEntry` 将触发以下事件:

- **Start** 当动画开始播放时触发,
    - 当调用`SetAnimation`时立刻触发.
    - 它也可以在一个队列中的动画开始播放时触发.
- **End** 当动画从轨道中被移除(或中断)时触发,
    - 当当前动画快要播放完成时你调用`SetAnimation`中断了它, 该事件将被触发.
    - 当使用`ClearTrack`或者`ClearTracks`清除了轨道时, 该事件也会被触发.
    - 在混合(mix)/淡入淡出(crossfade)期间，在mix完成后End事件将被触发.
    - 当注册到`AnimationState`时, **永远不要**在`End`事件处理中调用`SetAnimation`, 它会引发无限递归. 请看下面的警告. 可以注册一个`TrackEntry.End`来替代.
    - 注意, 默认情况下, 非循环动画的TrackEntries不再在动画的持续时间内停止. 相反, 会继续无限期地保持最后一帧, 直到你移除它或用其他动画取代它. 如果你想让你的`TrackEntry`达到其动画持续时长(duration)时清空轨道, 请将[`TrackEntry.TrackEnd`](https://zh.esotericsoftware.com/spine-api-reference#TrackEntry-trackEnd)设置为动画持续时长.
- **Dispose** 当AnimationState释放一个(在其生命周期结束时的)TrackEntry时, 会对TrackEntry触发.
    - 像spine-libgdx和spine-csharp这样的运行时会把TrackEntry对象缓存，以减小非必要的GC压力。这在Unity中尤为重要，因为Unity的GC实现有较为老旧低效.
    - 当TrackEntries被释放后，一定要记得移除对它们的所有引用，因为它们可能稍后就会被写入多余数据或触发意外事件.
    - Dispose事件会在End事件后立即触发.
- **Interrupt** 当设置了新的动画且当前有一个动画还在播放时触发.
    - 当一个动画开始mixing/crossfading到另一个动画时触发.
- **Complete** 当动画完成时触发,
    - 当一个非循环的动画播放完毕时触发，无论是否存在下一个在排队的动画.
    - 在循环动画每次循环结束后，也会触发.
- **Event** _任何_用户自定义事件被监听到时触发.
    - 这些事件点在Spine编辑器的动画中设置的。它们显示围为紫色的关键帧。在树状视图中也可以看到一个紫色的icon.
    - 为了区分不同的事件，你需要检查`Spine.Event e`的`Name`参数。(或者`Data`引用).
    - 当你想要按照动画节点去播放声音时它会非常有用，比如播放脚步声。它也可以根据Spine动画去同步或者通知非Spine系统，比如Unity的粒子系统或者产生单独的特效，甚至是诸如对齐发射子弹的时刻这样的游戏逻辑(如果你真的想这么做的话).
    - 每个TrackEntry都有一个`EventThreshold`属性. 它定义了在淡入淡出的哪些时间点上不触发用户事件. 更多信息请参见[**混合过程中的事件**](https://zh.esotericsoftware.com/spine-unity-events#%E6%B7%B7%E5%90%88%E8%BF%87%E7%A8%8B%E4%B8%AD%E7%9A%84%E4%BA%8B%E4%BB%B6).

在一个动画播放完成后，另一个队列中的动画即将开始播放的时候，事件触发的顺序为: `Complete`, `End`, `Start`.


## 1. 对比: AnimationState和TrackEntry事件

AnimationState和一个TrackEntry对象都会触发上文列出的Spine动画事件.

订阅AnimationState本身的事件, 会返回所有在其上播放的动画的回调.

相反，当订阅TrackEntry事件时，你将只订阅播放动画的那个具体实例。在这一TrackEntry结束后就被释放掉，不会产生任何新的事件.

TrackEntry事件会在对应的AnimationState事件之前触发.

## 2. 混合过程中的事件

![jpg](https://zh.esotericsoftware.com/img/spine-runtimes-guide/spine-unity/callbackchart-mix.png)
## 3. 例子 

```c#
// Sample written for for Spine 3.7
using UnityEngine;
using Spine;
using Spine.Unity;

// Add this to the same GameObject as your SkeletonAnimation
public class MySpineEventHandler : MonoBehaviour {

   // The [SpineEvent] attribute makes the inspector for this MonoBehaviour
   // draw the field as a dropdown list of existing event names in your SkeletonData.
   [SpineEvent] public string footstepEventName = "footstep"; 

   void Start () {
      var skeletonAnimation = GetComponent<SkeletonAnimation>();
      if (skeletonAnimation == null) return;

      // This is how you subscribe via a declared method.
      // The method needs the correct signature.
      skeletonAnimation.AnimationState.Event += HandleEvent;

      skeletonAnimation.AnimationState.Start += delegate (TrackEntry trackEntry) {
         // You can also use an anonymous delegate.
         Debug.Log(string.Format("track {0} started a new animation.", trackEntry.TrackIndex));
      };

      skeletonAnimation.AnimationState.End += delegate {
         // ... or choose to ignore its parameters.
         Debug.Log("An animation ended!");
      };
   }

   void HandleEvent (TrackEntry trackEntry, Spine.Event e) {
      // Play some sound if the event named "footstep" fired.
      if (e.Data.Name == footstepEventName) {
         Debug.Log("Play a footstep sound!");
      }
   }
}
```


**含有声音事件**


```c#
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace Spine.Unity.Examples {
   public class HandleEventWithAudioExample : MonoBehaviour {

      public SkeletonAnimation skeletonAnimation;
      [SpineEvent(dataField: "skeletonAnimation", fallbackToTextField: true)]
      public string eventName;

      [Space]
      public AudioSource audioSource;
      public AudioClip audioClip;
      public float basePitch = 1f;
      public float randomPitchOffset = 0.1f;

      [Space]
      public bool logDebugMessage = false;

      Spine.EventData eventData;

      void OnValidate () {
         if (skeletonAnimation == null) GetComponent<SkeletonAnimation>();
         if (audioSource == null) GetComponent<AudioSource>();
      }

      void Start () {
         if (audioSource == null) return;
         if (skeletonAnimation == null) return;
         skeletonAnimation.Initialize(false);
         if (!skeletonAnimation.valid) return;

         eventData = skeletonAnimation.Skeleton.Data.FindEvent(eventName);
         skeletonAnimation.AnimationState.Event += HandleAnimationStateEvent;
      }

      private void HandleAnimationStateEvent (TrackEntry trackEntry, Event e) {
         if (logDebugMessage) Debug.Log("Event fired! " + e.Data.Name);
         //bool eventMatch = string.Equals(e.Data.Name, eventName, System.StringComparison.Ordinal); // Testing recommendation: String compare.
         bool eventMatch = (eventData == e.Data); // Performance recommendation: Match cached reference instead of string.
         if (eventMatch) {
            Play();
         }
      }

      public void Play () {
         audioSource.pitch = basePitch + Random.Range(-randomPitchOffset, randomPitchOffset);
         audioSource.clip = audioClip;
         audioSource.Play();
      }
   }

}
```

