

MeshRender 中可以存在多个 Material ， 但是 CanvasRender 一个 gameobject 中只能存在一个 Material 。 也就是说只能有一个 texture


## 1. 开启 Advanced -> Multiple CanvasRenders

会将每个 Material 单独作为一个 子物体 改在到当前的 Gameobject 中。

## 2. SkeletonGraphicCustomMaterials inspecter 界面替换

在 inspecter 界面控制 texture 的覆盖。

该组件的设计初衷里不包括用代码控制Material覆盖. 如果需要通过代码动态地设置SkeletonGraphic的material, 应直接通过 `SkeletonGraphic.CustomMaterialOverride` 来访问material覆盖数组, 或者通过 `SkeletonGraphic.CustomTextureOverride` 访问texture覆盖数组.

## 3. 使用代码替换 Material 或者 texture

1. [CustomMaterialOverride和CustomSlotMaterials](https://zh.esotericsoftware.com/spine-unity-rendering#CustomMaterialOverride%E5%92%8CCustomSlotMaterials)

```c#
if (originalMaterial == null)
   originalMaterial = skeletonAnimation.SkeletonDataAsset.atlasAssets[0].PrimaryMaterial;

skeletonAnimation.CustomMaterialOverride[originalMaterial] = newMaterial; // to enable the replacement.
skeletonAnimation.CustomMaterialOverride.Remove(originalMaterial); // to disable that replacement.
```

Graphic 中 CustomTextureOverride,CustomMaterialOverride 


2. MaterialPropertyBlocks

直接通过 `meshRender` 设置 material中的值

```c#
MaterialPropertyBlock mpb = new MaterialPropertyBlock();
mpb.SetColor("_FillColor", Color.red); // "_FillColor" is a named property on the used shader.
mpb.SetFloat("_FillPhase", 1.0f); // "_FillPhase" is another named property on the used shader.
GetComponent<MeshRenderer>().SetPropertyBlock(mpb);

// to deactivate the override again:
MaterialPropertyBlock mpb = this.cachedMaterialPropertyBlock; // assuming you had cached the MaterialPropertyBlock
mpb.Clear();
GetComponent<Renderer>().SetPropertyBlock(mpb);
```

- 使用Renderer.SetPropertyBlock设置不同的Material属性值会破坏渲染器合批(batching)操作. 当MaterialPropertyBlock的参数一致时 (例如tint颜色均置为绿色) 渲染器才会合批渲染.
- 每当你改变或添加了MaterialPropertyBlock的属性值时, 都需要调用 `SetPropertyBlock` 来设置参数. 但你可以把MaterialPropertyBlock保存在类成员中, 如此在改变某个属性值时就无需再实例化出一个新MaterialPropertyBlock了.
- **当需要经常更改某个属性时, 你可以使用静态方法 `Shader.PropertyToID(string)` 来缓存该属性ID(int值), 而无需每次都访问MaterialPropertyBlock中字符串重载过的setter.**

## 4. 简单聊聊换装

1. 使用skin --- 最简单但是需要美术配合
2. 自己手动添加 attachment --- 万能但是性能较差

以下两个需要预先将每个部位 分拆到不同的 atlas (自动生成对饮的material) 方便后期更换
3. 使用 CustomTextureOverride --- 需要原始图片大小一致
4. 使用 MaterialPropertyBlocks --- 同上  性能更好 但是没法在 Graphic 上使用(没有 meshrender)

