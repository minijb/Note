
可以直接修改物体本身， 存储了对于 skeleton data资源的引用---其中又引用了数个atlas资源

## 1. 设置attachment

```c#
bool success = skeletonAnimation.Skeleton.SetAttachment("slotName", "attachmentName");

// using properties
[SpineSlot] public string slotProperty = "slotName";
[SpineAttachment] public string attachmentProperty = "attachmentName";
...
bool success = skeletonAnimation.Skeleton.SetAttachment(slotProperty, attachmentProperty);
```


**Setup Pose** : 重置为

```c#
skeleton.SetToSetupPose();
skeleton.SetBonesToSetupPose();
skeleton.SetSlotsToSetupPose();
```

**跟换皮肤**

```c#
bool success = skeletonAnimation.Skeleton.SetSkin("skinName");
skeletonAnimation.Skeleton.SetSlotsToSetupPose(); // see note below

// using properties
[SpineSkin] public string skinProperty = "skinName";
...
bool success = skeletonAnimation.Skeleton.SetSkin(skinProperty);
skeletonAnimation.Skeleton.SetSlotsToSetupPose(); // see note below
```


组合皮肤

```c#
var skeleton = skeletonAnimation.Skeleton;
var skeletonData = skeleton.Data;
var mixAndMatchSkin = new Skin("custom-girl");
mixAndMatchSkin.AddSkin(skeletonData.FindSkin("skin-base"));
mixAndMatchSkin.AddSkin(skeletonData.FindSkin("nose/short"));
mixAndMatchSkin.AddSkin(skeletonData.FindSkin("eyelids/girly"));
mixAndMatchSkin.AddSkin(skeletonData.FindSkin("eyes/violet"));
mixAndMatchSkin.AddSkin(skeletonData.FindSkin("hair/brown"));
mixAndMatchSkin.AddSkin(skeletonData.FindSkin("clothes/hoodie-orange"));
mixAndMatchSkin.AddSkin(skeletonData.FindSkin("legs/pants-jeans"));
mixAndMatchSkin.AddSkin(skeletonData.FindSkin("accessories/bag"));
mixAndMatchSkin.AddSkin(skeletonData.FindSkin("accessories/hat-red-yellow"));
skeleton.SetSkin(mixAndMatchSkin);
skeleton.SetSlotsToSetupPose();
skeletonAnimation.AnimationState.Apply(skeletonAnimation.Skeleton); // skeletonMecanim.Update() for SkeletonMecanim
```


[运行时重打包](https://zh.esotericsoftware.com/spine-unity-main-components#%E8%BF%90%E8%A1%8C%E6%97%B6%E9%87%8D%E6%89%93%E5%8C%85)

当组合皮肤时会不可避免地会使用到到多种material, 这将导致额外绘制调用. 此时可使用 `Skin.GetRepackedSkin()` 方法, 将不同皮肤中使用到的texture区域合并为单页texture.

```c#
using Spine.Unity.AttachmentTools;

// Create a repacked skin.
Skin repackedSkin = collectedSkin.GetRepackedSkin("Repacked skin", skeletonAnimation.SkeletonDataAsset.atlasAssets[0].PrimaryMaterial, out runtimeMaterial, out runtimeAtlas);
collectedSkin.Clear();

// Use the repacked skin.
skeletonAnimation.Skeleton.Skin = repackedSkin;
skeletonAnimation.Skeleton.SetSlotsToSetupPose();
skeletonAnimation.AnimationState.Apply(skeletonAnimation.Skeleton); // skeletonMecanim.Update() for SkeletonMecanim

// You can optionally clear the cache after multiple repack operations.
AtlasUtilities.ClearCache();
```


## 2. 懒加载 atlas texture

因为所有的 atlas texture 均通过 SkeletonDataAsset 间接引用， 因此会一起加载。

使用对应的 UPM 包
