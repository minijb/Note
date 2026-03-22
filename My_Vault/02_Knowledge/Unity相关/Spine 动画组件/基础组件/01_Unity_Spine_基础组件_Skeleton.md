---
title: Unity Spine Skeleton Animation
date: 2026-03-16
tags:
  - unity
  - spine
  - animation
type: framework
aliases:
  Spine Animation
description: Unity Spine基础组件SkeletonAnimation
draft: false
---


## 1. 基础介绍

- 将 Spine skeleton 附加到 GameObject 上， 并执行播放动画和响应动画事件等。
- 引用 skeleton data, 得到骨骼层次和槽位信息等。


使用脚本创建
```c#
// instantiating a SkeletonAnimation GameObject from a SkeletonDataAsset
SkeletonAnimation instance = SkeletonAnimation.NewSkeletonAnimationGameObject(skeletonDataAsset);

// instantiating a SkeletonGraphic GameObject from a SkeletonDataAsset
SkeletonGraphic instance
   = SkeletonGraphic.NewSkeletonGraphicGameObject(skeletonDataAsset, transform, skeletonGraphicMaterial);
   
// instantiation from exported assets without prior import
// 1. Create the AtlasAsset (needs atlas text asset and textures, and materials/shader);
// 2. Create SkeletonDataAsset (needs json or binary asset file, and an AtlasAsset)
SpineAtlasAsset runtimeAtlasAsset
   = SpineAtlasAsset.CreateRuntimeInstance(atlasTxt, textures, materialPropertySource, true);
SkeletonDataAsset runtimeSkeletonDataAsset
   = SkeletonDataAsset.CreateRuntimeInstance(skeletonJson, runtimeAtlasAsset, true);
// 3. Create SkeletonAnimation (needs a valid SkeletonDataAsset)
SkeletonAnimation instance = SkeletonAnimation.NewSkeletonAnimationGameObject(runtimeSkeletonDataAsset);
```


## 2. 生命周期

![jpg](https://zh.esotericsoftware.com/img/spine-runtimes-guide/spine-unity/spine-unity-skeletonanimation-updates.png)

对应的回调函数

- `SkeletonAnimation.BeforeApply` 在应用该帧动画之前触发该事件. **当你想在动画应用到skeleton上之前改变skeleton状态时**, 可以使用该回调.
- `SkeletonAnimation.UpdateLocal` **在该帧动画更新完成并应用于skeleton的局部值之后触发该事件. 如果你需要读取或修改骨骼的局部值, 请使用该回调**.
- `SkeletonAnimation.UpdateComplete` 在Skeleton中所有骨骼的世界值计算完成后触发该事件. 在该事件之后, Update阶段的SkeletonAnimation不再有其他操作. **如果你只需要读取骨骼的世界值, 请使用该回调**. 如果其他代码在SkeletonAnimation的Update之后修改了这些值, 这时读取到的世界值仍可能会变化.
- `SkeletonAnimation.UpdateWorld` 在计算了Skeleton中所有骨骼的世界值后触发该事件. 若在代码中订阅了该事件, **运行时则将再次调用 `skeleton.UpdateWorldTransform`**. 如果你的skeleton复杂或正在执行其他计算, 该行为将显得非必要甚至有些浪费. **如果需要根据骨骼的世界值来修改骨骼的局部值, 请使用该回调. 该回调在Unity代码中实现自定义约束时会很有帮助**.

SkeletonRenderer Update回调

- `OnRebuild` 在skeleton成功初始化后触发.
- `OnMeshAndMaterialsUpdated` 会在更新完网格和所有material后, 于 `LateUpdate()` 结束时触发.

<font color="#00b050">修改 skeleton 状态 </font>

- 若要在 _应用动画_ 之前执行代码, 请在 `Update` 中调用代码, 并将执行顺序设置 _在 SkeletonAnimation 之前_.
- 若要在 _应用动画_ 后到生成skeleton网格前这段时间内执行代码, 同样请在 `Update` 中调用代码, 但应将执行顺序设置 _在 SkeletonAnimation 之后_. 也可以在 `LateUpdate` 中调用, 并将执行顺序设置 _在 SkeletonAnimation 之前_.

```c#
// At execution order -1, this component executes before SkeletonAnimation and SkeletonRenderer.
[DefaultExecutionOrder(-1)]
public class SetupPoseComponent : MonoBehaviour {
   ...

   void Update() {
      // This call lets the skeleton start from setup-pose each frame before applying animations.
      // SetupPoseComponent.Update needs to be called before SkeletonAnimation.Update, which is ensured
      // by [DefaultExecutionOrder(-1)] above.
      skeleton.SetToSetupPose();
   }
}
```

同样可以进行手动更新

在进行某些修改后, 可能需要立即将动画重新应用到skeleton上, 或者基于修改后的skeleton重新生成skeleton网格. 相较于 [通用运行时](https://esotericsoftware.com/spine-runtime-skeletons), `SkeletonAnimation` 组件的方法可以实现单次调用便完成一致更新. 下例中, `skeleton.UpdateWorldTransform()` 就是在 `Update(deltaTime)` 和 `ApplyAnimation()` 中调用的.

- **`Update(deltaTime)`** 更新了整个skeleton. Skeleton网格维持不变.  
    `SkeletonAnimation.Update(deltaTime)` 则更新了底层的 `AnimationState`, 然后在这一帧根据skeleton物理约束推进Transform运动, 并将动画应用于skeleton, 最后更新所有骨骼的世界变换(transform). 当你需要在不推进时间的情况下进行更新整个skeleton, 或者你想按照自定义的delta time来推进更新时, 是有必要的手动维护更新步调的.

```c#
// After setting bones and slots to setup pose, perform a full skeleton update without advancing time. 
skeleton.SetToSetupPose();
skeletonAnimation.Update(0);

// Setting only slots to setup pose usually (except for when active skin bones change)
// does not require bone world transform updates, so AnimationState.Apply(skeleton) is sufficient.
skeleton.SetSlotsToSetupPose();
skeletonAnimation.AnimationState.Apply(skeleton)
```

- **`ApplyAnimation()`** 将动画重新应用到了skeleton上.  
    `SkeletonAnimation.ApplyAnimation()` 也会将动画重新应用到skeleton上, 但它不会更新底层的 `AnimationState` 或将变换运动传递给物理约束.

```c#
// If your script modifies skeleton properties in LateUpdate() and script execution order
// of the script executes after SkeletonAnimation.

   SkeletonAnimation skeletonAnimation;
   Spine.AnimationState animationState;
   Spine.Skeleton skeleton;

void LateUpdate () {
   skeleton.SetToSetupPose(); // perform some skeleton modifications
   skeletonAnimation.Update(0);
   skeletonAnimation.LateUpdateMesh(); // otherwise SkeletonAnimation.LateUpdate would be called next frame
   }
```
