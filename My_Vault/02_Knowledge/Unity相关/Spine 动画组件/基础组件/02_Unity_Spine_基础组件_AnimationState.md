---
title: Unity Spine AnimationState
date: 2026-03-16
tags:
  - unity
  - spine
  - animationstate
type: framework
aliases:
  AnimationState
description: Unity Spine基础组件AnimationState
draft: false
---


## 1. 设置动画

```c#
TrackEntry entry = skeletonAnimation.AnimationState.SetAnimation(trackIndex, "walk", true);

// using properties
[SpineAnimation] public string animationProperty = "walk";
...
TrackEntry entry = skeletonAnimation.AnimationState.SetAnimation(trackIndex, animationProperty, true);

// using AnimationReferenceAsset
public AnimationReferenceAsset animationReferenceAsset; // assign a generated AnimationReferenceAsset to this property
...
TrackEntry entry = skeletonAnimation.AnimationState.SetAnimation(trackIndex, animationReferenceAsset, true);
```


## 2. 队列动画

要将动画加入队列, 需要提供轨道索引、动画名称、是否循环播放该动画, 以及该动画在轨道上开始播放的延迟时间(以秒为单位).

```c#
TrackEntry entry = skeletonAnimation.AnimationState.AddAnimation(trackIndex, "run", true, 2);
```


## 3. 清除动画

如果轨道当前没有动画但已设置了动画时, 运行时会立即开始播放动画. 清空轨道后将不再应用轨道动画, Skeleton将保持清空动画时的姿势. 如[通用运行时指南](https://zh.esotericsoftware.com/spine-applying-animations/#%E7%A9%BA%E5%8A%A8%E7%94%BB)所述, _empty_动画就是用来mix-in(淡入)或mix-out(淡出)到另一个动画的. Skeleton动画组件提供了设置空动画、队列空动画、清空某条或全部轨道的方法. 这些方法的用法与上文中队列动画的方法和参数相似.

```c#
TrackEntry entry = skeletonAnimation.AnimationState.SetEmptyAnimation(trackIndex, mixDuration);
entry = skeletonAnimation.AnimationState.AddEmptyAnimation(trackIndex, mixDuration, delay);
skeletonAnimation.AnimationState.ClearTrack(trackIndex);
skeletonAnimation.AnimationState.ClearTracks();
```

## 4. [轨道条目](https://zh.esotericsoftware.com/spine-unity-main-components#%E8%BD%A8%E9%81%93%E6%9D%A1%E7%9B%AE)

AnimationState的所有方法都会返回一个 [TrackEntry](https://zh.esotericsoftware.com/spine-api-reference#TrackEntry) (轨道条目)对象, 它可以进一步定制如何回放某段动画, 也能自定义轨道条目中某个事件的委托. 详见下文中的 _处理AnimationState事件_ 一节.

> **请注意:** 运行时从底层的AnimationState中删除了轨道条目所对应的动画后, 这些方法返回的轨道条目便会失效. Unity的垃圾收集器会自动释放它们. 在接收到轨道条目的销毁事件(dispose event)后, 就不应再存储或访问这个轨道条目了.


```c#
TrackEntry entry = ...
entry.EventThreshold = 2;
float trackEnd = entry.TrackEnd;
```


## 5. 处理AnimationState事件

动画播放已开始(started事件) .
动画播放中断(interrupted事件), 例如清空了一条轨道或设置了一段新动画.
无中断地完成了动画播放(completed事件) , 如果是循环动画, 该事件可能会多次出现.
动画播放停止(ended事件) .
已销毁动画及其的 TrackEntry (disposed事件) .
用户定义事件触发(event事件).


```c#
SkeletonAnimation skeletonAnimation;
Spine.AnimationState animationState;

void Awake () {
   skeletonAnimation = GetComponent<SkeletonAnimation>();
   animationState = skeletonAnimation.AnimationState;

   // registering for events raised by any animation
   animationState.Start += OnSpineAnimationStart;
   animationState.Interrupt += OnSpineAnimationInterrupt;
   animationState.End += OnSpineAnimationEnd;
   animationState.Dispose += OnSpineAnimationDispose;
   animationState.Complete += OnSpineAnimationComplete;

   animationState.Event += OnUserDefinedEvent;

   // registering for events raised by a single animation track entry
   Spine.TrackEntry trackEntry = animationState.SetAnimation(trackIndex, "walk", true);
   trackEntry.Start += OnSpineAnimationStart;
   trackEntry.Interrupt += OnSpineAnimationInterrupt;
   trackEntry.End += OnSpineAnimationEnd;
   trackEntry.Dispose += OnSpineAnimationDispose;
   trackEntry.Complete += OnSpineAnimationComplete;
   trackEntry.Event += OnUserDefinedEvent;
}

public void OnSpineAnimationStart(TrackEntry trackEntry) {
   // Add your implementation code here to react to start events
}
public void OnSpineAnimationInterrupt(TrackEntry trackEntry) {
   // Add your implementation code here to react to interrupt events
}
public void OnSpineAnimationEnd(TrackEntry trackEntry) {
   // Add your implementation code here to react to end events
}
public void OnSpineAnimationDispose(TrackEntry trackEntry) {
   // Add your implementation code here to react to dispose events
}
public void OnSpineAnimationComplete(TrackEntry trackEntry) {
   // Add your implementation code here to react to complete events
}


string targetEventName = "targetEvent";
string targetEventNameInFolder = "eventFolderName/targetEvent";

public void OnUserDefinedEvent(Spine.TrackEntry trackEntry, Spine.Event e) {

   if (e.Data.Name == targetEventName) {
      // Add your implementation code here to react to user defined event
   }
}

// you can cache event data to save the string comparison
Spine.EventData targetEventData;
void Start () {
   targetEventData = skeletonAnimation.Skeleton.Data.FindEvent(targetEventName);
}
public void OnUserDefinedEvent(Spine.TrackEntry trackEntry, Spine.Event e) {

   if (e.Data == targetEventData) {
      // Add your implementation code here to react to user defined event
   }
}
```


[在回调中更改AnimationState或游戏状态](https://zh.esotericsoftware.com/spine-unity-main-components#%E5%9C%A8%E5%9B%9E%E8%B0%83%E4%B8%AD%E6%9B%B4%E6%94%B9AnimationState%E6%88%96%E6%B8%B8%E6%88%8F%E7%8A%B6%E6%80%81) -- 修改animationState的时机
[Coroutine中的Yield指令](https://zh.esotericsoftware.com/spine-unity-main-components#Coroutine%E4%B8%AD%E7%9A%84Yield%E6%8C%87%E4%BB%A4) --- 异步等待调用时间


