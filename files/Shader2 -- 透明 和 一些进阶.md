---
tags:
  - shader
---
https://www.yuque.com/chengxuyuanchangfeng/idsf04/mnlqqblkv279y5w2


这个面试精华里总提到，就是画家算法，一层又一层的覆盖上，被遮挡的部分其实就是所说的OverDraw了。那岂不是浪费性能嘛？是的，所以Unity把不透明的物体设置为，先渲染近处的，后渲染远的。但马上出来新的问题，后渲染远的，远的一刷上去就把近的覆盖了。肯定是不对的，所以这里有个概念**深度值Depth**.


**如何渲染透明**

但是我们不要忘了，还有个深度测试呢，写入了还是会覆盖，这个是发生在Blend之前的。所以依然有问题。那怎么办？

- 把B的深度测试关了，ZTest Off，这样B假如前面有个不透明的C，B会覆盖C的，所以这种方法不行。
- 把B设置深度测试总是通过，ZTest Always，一样和第一种的问题，也不行。
- **A通过深度测试之后，不写入深度缓存，那B就不知道前面还有个A，就会去写入B。所以B就会完全的绘制出来，A就会在混合阶段叠加上去。**


`Blend Off`：关闭混合（这是默认值）

`Blend SrcFactor DstFactor`：配置并启用混合。生成的颜色将乘以 **SrcFactor**。屏幕上的已有颜色乘以 **DstFactor**，然后将这两个值相加。

`Blend SrcFactor DstFactor, SrcFactorA DstFactorA`：同上，但使用不同系数来混合 Alpha 通道。

`BlendOp Op`：不将混合颜色相加，而是对它们执行不同的操作。

`BlendOp OpColor, OpAlpha`：同上，但是对颜色 (RGB) 通道和 Alpha (A) 通道使用不同的混合操作。

此外，您还可以设置上层渲染目标混合模式。当 使用多渲染目标 (MRT) 渲染时，上面的常规语法 将为所有渲染目标设置相同的混合模式。以下语法可以为各个渲染目标设置不同的混合模式，其中 `N` 是渲染目标索引（0 到 7）。此功能适用于大多数现代 API/GPU（DX11/12、GLCore、Metal 和 PS4）：

- `Blend N SrcFactor DstFactor`
- `Blend N SrcFactor DstFactor, SrcFactorA DstFactorA`
- `BlendOp N Op`
- `BlendOp N OpColor, OpAlpha`

`AlphaToMask On`：开启 alpha-to-coverage。使用 MSAA 时，alpha-to-coverage 会根据像素着色器结果 Alpha 值按比例修改多重采样覆盖率遮罩。这通常用于比常规 Alpha 测试更少锯齿的轮廓；对植被和其他经过 Alpha 测试的着色器非常有用。

Blend SrcAlpha OneMinusSrcAlpha // 传统透明度
Blend One OneMinusSrcAlpha // 预乘透明度
Blend One One // 加法
Blend OneMinusDstColor One // 软加法
Blend DstColor Zero // 乘法
Blend DstColor SrcColor // 2x 乘法


## 半透明

两个pass，一个渲染正面，一个渲染背面

第一个 pass 渲染背面， 第二个渲染正面

```c++
Cull Front
ZWrite Off
Blend SrcAlpha OneMinusSrcAlpha


Pass
{
	Cull Back
	ZWrite Off
	Blend SrcAlpha OneMinusSrcAlpha
```



## 模板测试

Unity官方文档定义如下：  
模板缓冲区可用作一般目的的每像素遮罩，以便保存或丢弃像素。 模板缓冲区通常是每像素 8 位整数。该值可以写入、递增或递减。后续绘制调用可以根据该值进行测试，以确定在运行像素着色器之前是否应丢弃像素。  
Unity Shader入门精要》大致解释如下：  
如果开启了模板测试，GPU会首先读取模板缓冲区中该片元位置的模板值，然后将该值和读取到的参考值进行比较，若没有通过测试，则该片元则会被舍弃。但是不管片元有没有通过测试，我们都可以根据模板测试结果来修改模板缓冲区。其中的比较函数和缓冲区操作都是可以由开发者指定的。

再直白点就是说：直接比大小，比不比得过你都可以修改模板缓冲区的值。

https://www.yuque.com/chengxuyuanchangfeng/idsf04/yumti7lrz5z2qbgm

```c++
Shader "Examples/CommandExample"
{
    SubShader
    {
         // 此处是定义子着色器的代码的其余部分。

        Pass
        {    
             // 此通道中的所有像素都会通过模板测试并将值 2 写入模板缓冲区
             // 如果要防止后续着色器绘制到渲染目标的此区域或将它们限制为仅渲染到此区域，则通常会执行此操作
             Stencil
             {
                 Ref 2
                 Comp Always
                 Pass Replace
             }            

             // 此处是定义通道的代码的其余部分。
        }
    }
}
```



## 法线和切线

法线贴图， 

**TBNj矩阵**https://www.yuque.com/chengxuyuanchangfeng/idsf04/ayktgb1gdbo9dcpa


1. **从法线贴图中解包法线信息**。
2. **根据切线和法线计算副切线**。
3. **通过切线空间（TBN矩阵）将法线贴图中的法线映射到对象空间或世界空间**。


## 玻璃折射

https://www.yuque.com/chengxuyuanchangfeng/idsf04/aef08h5mb3ypqgxm


float4 ComputeGrabScreenPos(float4 clipPos);

一个 pass


**需要法线贴图+法线贴图强度**。


|                                     |                                                                                                                                                             |
| ----------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `GrabPass { }`                      | 将帧缓冲区内容抓取到一个纹理中，使您可以在同一个子着色器中的后续通道中使用该纹理。  <br>  <br>使用 __GrabTexture_ 名称引用该纹理。  <br>  <br>当您使用此签名时，Unity 每次渲染包含此命令的批处理时都会抓取屏幕。这意味着 Unity 可以每帧多次抓取屏幕：每批次一次。 |
| `GrabPass { "ExampleTextureName" }` | 将帧缓冲区内容抓取到一个纹理中，使您可以在同一帧的后续通道中跨多个子着色器访问该纹理。  <br>  <br>使用给定名称引用该纹理。  <br>  <br>当您使用此签名时，Unity 会在渲染批处理的帧中第一次抓取屏幕，该批处理包含具有给定纹理名称的此命令。                         |
拿到当前屏幕的帧缓冲区内容，作为一个纹理。

需要记录原始位置，屏幕位置。


```c++
srcPos = ComputeGrabScreenPos(o.pos);  // 但是该函数返回的是齐次坐标下的屏幕坐标值
```

`ComputeGrabScreenPos` 的作用是将当前像素的屏幕空间位置转换为适合采样 `_GrabTexture` 的纹理坐标。它的输入通常是顶点着色器中计算出的裁剪空间坐标（`clipPos`），输出是一个四维向量（`float4`），表示屏幕空间坐标。


- **输入**：`clipPos` 是顶点在裁剪空间中的位置，通常通过 `UnityObjectToClipPos(v.vertex)` 计算得到。
- **输出**：返回一个四维向量，表示屏幕空间坐标，可以直接用于采样 `_GrabTexture`。

实现偏移。

`Normal.xy *   * _RefractoinTex_TexelSize.xy`  -- 通过实现对于屏幕图像进行法线方向上的扭曲和偏移实现折射效果 

`_RefractoinTex_TexelSize` 就是纹理的纹素大小--- Texel Size。 即 每个像素在UV坐标中的大小 


