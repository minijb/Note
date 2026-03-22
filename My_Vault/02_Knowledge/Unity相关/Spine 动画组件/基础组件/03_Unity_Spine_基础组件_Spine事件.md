---
title: Unity Spine 事件
date: 2026-03-16
tags:
  - unity
  - spine
  - event
type: framework
aliases:
  Spine事件
description: Unity Spine动画组件事件处理
draft: false
---


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

