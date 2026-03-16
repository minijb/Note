---
tags:
  - shader
---
**速查表**

https://www.yuque.com/chengxuyuanchangfeng/idsf04/vgcpvc45krzkbe9d


## 基础结构

Properties 属性 -- 可以在外部添加修改的值。

- 数字
- 颜色/矢量
- 纹理


着色器中的每个属性均通过 **name** 引用（在 Unity 中，着色器属性名称通常以下划线开头）。属性在材质检视面板中将显示为 **display name**。每个属性都在等号后给出默认值：

- 对于 _Range_ 和 _Float_ 属性，默认值仅仅是单个数字，例如“13.37”。
- 对于 _Color_ 和 _Vector_ 属性，默认值是括在圆括号中的四个数字，例如“(1,0.5,0.2,1)”。
- 对于 2D 纹理，默认值为空字符串或内置默认纹理之一：“white”（RGBA：1,1,1,1）、“black”（RGBA：0,0,0,0）、“gray”（RGBA：0.5,0.5,0.5,0.5）、“bump”（RGBA：0.5,0.5,1,0.5）或“red”（RGBA：1,0,0,0）。
- 对于非 2D 纹理（立方体、3D 或 2D 数组），默认值为空字符串。如果材质未指定立方体贴图/3D/数组纹理，则使用灰色（RGBA：0.5,0.5,0.5,0.5）。

## subShader

Unity 中的每个着色器都包含一个子着色器列表。当 Unity 必须显示网格时，它将找到要使用的着色器，并选择在用户的显卡上运行的第一个子着色器。

```shader
Subshader { [Tags] [CommonState] Passdef [Passdef ...]}
```

subShader 可以写多个，自动选择合适的
Pass 代码块将使游戏对象的几何体被渲染一次。 --- 也就是说可以有多个pass

**常见 Tags**：

- Rendering Order - Queue tag
- RenderType tag

RenderType标签将着色器分类为若干预定义组，例如是一个不透明的着色器，或alpha测试的着色器等。被用于着色器替换，或者在某些情况下用于生成相机的深度纹理。

|                           |                                         |
| ------------------------- | --------------------------------------- |
| 类型                        | 描述                                      |
| **Opaque**                | 用于大多数着色器（法线着色器、自发光着色器、反射着色器以及地形的着色器）。   |
| **Transparent**           | 用于半透明着色器（透明着色器、粒子着色器、字体着色器、地形额外通道的着色器）。 |
| **TransparentCutout**     | 蒙皮透明着色器（Transparent Cutout，两个通道的植被着色器）。 |
| **Background**            | 天空盒着色器。                                 |
| **Overlay**               | 光晕着色器、闪光着色器。                            |
| **TreeOpaque**            | 地形引擎中的树皮。                               |
| **TreeTransparentCutout** | 地形引擎中的树叶。                               |
| **TreeBillboard**         | 地形引擎中的广告牌树。                             |
| **Grass**                 | 地形引擎中的草。                                |
| **GrassBillboard**        | 地形引擎何中的广告牌草。                            |
### LOD

着色器的LOD(Level ofdetail)是用在整个shader或者SubShader中。当LOD的值小于设定值时，相应的shader不会工作。

默认情况下，允许的 LOD 级别可以是无限的。也就是说，可以使用硬件所支持的所有的着色器。然而，在某些情况下即使硬件可以支持它们，你可能也要放弃着色器的详细信息。例如，一些廉价的图形卡可能支持所有功能，但使用这些功能的速度太慢了。所以，你可能就不想在这些卡上使用视差法线映射了。

着色器的细节层次既可以针对单个着色器进行设定（使用Shader.maximumLOD），也可以针对所有着色器进行全局设定（使用Shader.globalMaximumLOD）。

在你的自定义着色器中，使用LOD命令来为每个子着色器来设定LOD值。

Unity中内建的着色器的LOD设置参数如下：

- VertexLit kind of shaders = 100
- Decal, Reflective VertexLit = 150
- Diffuse = 200
- Diffuse Detail, Reflective Bumped Unlit, Reflective Bumped VertexLit = 250
- Bumped, Specular = 300
- Bumped Specular = 400
- Parallax = 500
- Parallax Specular = 600

> SubShader Tags:
> 1. Render Order 
> 2. RenderType  主要就两个 Opaque不透明 ， Transparent 透明
> 3. LOD ： LOD Level


## Pass

**tags**: 

Cull Back | Front | Off
ZTest (Less | Greater | LEqual | GEqual | Equal | NotEqual | Always)
ZWrite On | Off


ZTest：深度测试，开启后测试结果决定片元是否被舍弃，可配置  
ZWrite：深度写入，开启后决定片元的深度值是否写入深度缓冲，可配置

ZTest可设置的测试规则：

- ZTest Less：深度小于当前缓存则通过
- ZTest Greater：深度大于当前缓存则通过
- ZTest LEqual：深度小于等于当前缓存则通过
- ZTest GEqual：深度大于等于当前缓存则通过
- ZTest Equal：深度等于当前缓存则通过
- ZTest NotEqual：深度不等于当前缓存则通过
- ZTest Always：不论如何都通过

ZTest Off等同于ZTest Always，关闭深度测试等于完全通过。

从流程图中可以看出：

- 在开启ZTest下，没有通过测试的片元部分是直接被舍弃，通过测试的片元被保留下来
- 在关闭ZTest下，不存在片元被舍弃的情况，也就是说，关闭深度测试，整个片元是被保留下来的
- 在ZWrite开启状态下，只有保留下来片元深度值才能被写入深度缓冲

1.深度测试通过，深度写入开启：写入深度缓冲区，写入颜色缓冲区  
2.深度测试通过，深度写入关闭：不写深度缓冲区，写入颜色缓冲区  
3.深度测试失败，深度写入开启：不写深度缓冲区，不写颜色缓冲区  
4.深度测试失败，深度写入关闭：不写深度缓冲区，不写颜色缓冲区


Offset 

设置 Z 缓冲区深度偏移，z-fighting：就是2个z值一样，放在同一个平面下的多边形，因为他们的z值极其接近，所以会出现交替显示，闪烁的现象，所以为了不让它继续闪下去，我们可以通过 Offset 来分出它们之间的先后顺序

Blend

Blend sourceBlendMode destBlendMode
Blend sourceBlendMode destBlendMode, alphaSourceBlendMode alphaDestBlendMode
BlendOp colorOp
BlendOp colorOp, alphaOp
AlphaToMask On | Off

第一个 one 代表源颜色  
第二个 one 代表目标颜色

**混合因子**

One：源或目标的完整值  
Zero：0  
SrcColor：源的颜色值  
SrcAlpha：源的Alpha值  
DstColor：目标的颜色值  
DstAlpha：目标的Alpha值  
OneMinusSrcColor：1-源颜色得到的值  
OneMinusSrcAlpha：1-源Alpha得到的值  
OneMinusDstColor：1-目标颜色得到的值  
OneMinusDstAlpha：1-目标Alpha得到的值

**常见混合类型 (Blend Type)**

Blend SrcAlpha OneMinusSrcAlpha // 传统透明度

Blend One OneMinusSrcAlpha // 预乘透明度

Blend One One // 加法

Blend OneMinusDstColor One // 软加法

Blend DstColor Zero // 乘法

Blend DstColor SrcColor // 2x 乘法




ColorMask 

RGB | A | 0 | R、G、B、A 的任意组合ColorMask

ColorMask命令可以设置颜色的写入通道，可以选择哪些通道写入，也就是会阻止GPU将一些通道写入到RenderTarget当中。

默认情况下，GPU会写入所有的通道RGBA，但有时候实现一些效果的时候，我们不需要4个通道，比如我们可以在渲染阴影贴图时关闭所有的颜色通道，因为只需要深度图。还有一种常用的场景就是完全禁用颜色写入，以便我们可以在一个缓冲区中填充数据而无需写入其他缓冲区，例如在不写入渲染目标的情况下填充模板缓冲区。

https://www.yuque.com/chengxuyuanchangfeng/idsf04/nsa4mkxfnz20e163#colormask


`#pragma vertex name` --- 用于命名

`#include"UnityCG.cginc"`  --- 代码复用


## 顶点着色器

```c++
struct appdata
{
    float4 vertex : POSITION;  // 顶点位置
    float2 uv : TEXCOORD0;     // 顶点的纹理坐标
};
```



POSITION : 标识
SV_POSITION : 裁剪坐标

基础类型 float，half，fixed ，int，
复合类型 ： `float3/4s` ,矩阵类型以类似的方式构建；例如 `float4x4` 是一个 4x4 变换矩阵。请注意，某些平台仅支持方形矩阵
纹理 ： 

```c++
sampler2D _MainTex;
samplerCUBE _Cubemap;
```

对于移动平台，这些将转换为“低精度采样器”，即预期纹理应具有低精度数据。如果您知道纹理包含 HDR 颜色，则可能需要使用半精度采样器：

```c++
sampler2D_half _MainTex;
samplerCUBE_half _Cubemap;
```

纹理包含完整浮点精度数据

```c++
sampler2D_float _MainTex;
samplerCUBE_float _Cubemap;
```

### 从程序传给顶点函数

其他常见的字段

POSITION：顶点坐标（模型空间下）
NORMAL：法线向量（模型空间下）
TANGENT：切线向量（模型空间下）
TEXCOORD0~n：[纹理坐标](https://so.csdn.net/so/search?q=%E7%BA%B9%E7%90%86%E5%9D%90%E6%A0%87&spm=1001.2101.3001.7020)（第几套uv的意思）
[COLOR](https://so.csdn.net/so/search?q=COLOR&spm=1001.2101.3001.7020)：顶点颜色


```c++
struct appdata
	{
		float4 vertex : POSITION;		//顶点
		float4 tangent : TANGENT;		//切线
		float3 normal : NORMAL;			//法线
		float4 texcoord : TEXCOORD0;	        //UV1
		float4 texcoord1 : TEXCOORD1;	        //UV2
		float4 texcoord2 : TEXCOORD2;	        //UV3
		float4 texcoord3 : TEXCOORD3;	        //UV4
		fixed4 color : COLOR;			//顶点色
	};
```


### 片元输入

```c++
struct v2f
{
    float2 uv : TEXCOORD0;      // 传递给片段着色器的纹理坐标
    UNITY_FOG_COORDS(1)         // Unity的雾效坐标
    float4 vertex : SV_POSITION;  // 传递给片段着色器的裁剪空间位置
};
```

创建一个v2f的结构体
第一行创建一个叫uv的float2的变量，从TEXCOORD0取的信息
第二行就是一个默认的宏了，表示使用TEXCOORD1存一下雾效有关的坐标
第三行唯一的不一样就是这个SV_前缀了，啥意思呢？就是传递转换到裁剪空间的位置，SV的意思就是System Value的缩写了。


## 片元着色器


`SV_Target` 用来标识 **片段着色器**（fragment shader）输出的颜色值或数据，这些数据最终会被存储到帧缓冲（Frame Buffer）中或者进一步用于屏幕渲染。

tex2D就是在纹理上取颜色，颜色咋取的？就是每一个uv值对应上取到的。
第二行是一个宏，根据雾效坐标去调整下颜色
然后返回最终的颜色。

```C++
fixed4 frag (v2f i) : SV_Target
{
    // 使用纹理坐标采样纹理颜色
    fixed4 col = tex2D(_MainTex, i.uv);
    // 应用雾效
    UNITY_APPLY_FOG(i.fogCoord, col);  // 根据雾效坐标调整颜色
    return col;  // 返回最终颜色
}
```

alpha 只有在混合模式的时候才有效。

## 纹理

```c++
sampler2D _MainTex;  // 定义纹理采样器
float4 _MainTex_ST;  // 纹理的平移、缩放和旋转参数
```

sampler2D就是2D的纹理采样器，就是说上面这个图里的信息在这个里面就能取得到。

`_MainTex_S`T是什么呢?
`_MainTex_ST`的含义是纹理的偏移/缩放值。`_MainTex_ST.xy`存储缩放值，`_MainTex_ST.zw`存储偏移值。


Tiling是平铺，就是_MainTex_ST.xy的缩放值
Offset是偏移，就是_MainTex_ST.zw存储偏移值
默认都是1,1和0,0。这样有个好处就是UV在0-1之间，也不偏移。假如真的改了会咋样，Unity默认是重复覆盖上去。


## UV扰动

- **第一面板**：基础纹理的UV坐标（规则网格）。
- **第二面板**：灰度扭曲纹理叠加的效果。
- **第三面板**：动态滚动的UV网格变化（箭头表示方向）。
- **第四面板**：最终效果，显示应用扭曲后主纹理的波浪形和弯曲。

**如何扰动 ： 使用噪声进行扰动。**

```glsl
Tags {
	"Queue"="Transparent" // 设置渲染队列为透明队列，表示该对象会在不透明对象之后渲染，数值越大越后渲染
	"RenderType"="Transparent" // 设置渲染类型为透明类型
}
```

**需要的属性**

```c++
Properties
{
	_MainTex ("Main Texture", 2D) = "white" {} // 主纹理
	_DistortTex("Distortion Texture", 2D) = "white" {} // 扭曲纹理
   _DistortAmount("Distortion Amount", Range(0,2)) = 0.5 // 扭曲强度
   _DistortTexXSpeed("Scroll speed X", Range(-50,50)) = 5 // 扭曲纹理在X方向上的滚动速度
   _DistortTexYSpeed("Scroll speed Y", Range(-50,50)) = 5 // 扭曲纹理在Y方向上的滚动速度
	[HideInInspector] _RandomSeed("_MaxYUV", Range(0, 10000)) = 0.0 // 隐藏在Inspector中，随机种子值
}
```

需要的数据类型 

```c++
#pragma multi_compile_fog

#include "UnityCG.cginc" // 引入Unity常用的着色器函数库
struct appdata
{
	float4 vertex : POSITION; // 顶点位置
	float2 uv : TEXCOORD0; // UV坐标
};

struct v2f
{
	float2 uv : TEXCOORD0; // UV坐标 ---- 原始 uv 坐标
	UNITY_FOG_COORDS(1) // 雾效的插值数据
	float4 vertex : SV_POSITION; // 转换到裁剪空间的顶点位置
	half2 uvDistTex : TEXCOORD3; // 用于扭曲纹理的UV坐标 --- 扭曲的 uv 坐标
};

sampler2D _MainTex; // 主纹理采样器
float4 _MainTex_ST; // 主纹理的缩放和偏移
sampler2D _DistortTex; // 扭曲纹理采样器
half4 _DistortTex_ST; // 扭曲纹理的缩放和偏移
half _DistortTexXSpeed, _DistortTexYSpeed, _DistortAmount; // 扭曲相关的参数
UNITY_DEFINE_INSTANCED_PROP(float, _RandomSeed) // 定义实例化属性，随机种子
```



顶点着色器 

```c++
v2f vert (appdata v)
{
	v2f o;
	o.vertex = UnityObjectToClipPos(v.vertex); // 将顶点从本地空间转换到裁剪空间
	o.uv = TRANSFORM_TEX(v.uv, _MainTex); // 对UV进行缩放和偏移变换
	UNITY_TRANSFER_FOG(o,o.vertex); // 传递雾效相关数据
	o.uvDistTex = TRANSFORM_TEX(v.uv, _DistortTex); // 对扭曲纹理的UV进行变换 ----- 对噪声图进行采样 --- 进行扰动
	return o;
}
```


> 雾坐标 ： https://blog.csdn.net/liu_if_else/article/details/73743706


片段着色器

```c++
// 片段着色器
fixed4 frag (v2f i) : SV_Target
{
	half randomSeed = UNITY_ACCESS_INSTANCED_PROP(Props, _RandomSeed); // 获取随机种子值
	UNITY_APPLY_FOG(i.fogCoord, col); // 应用雾效
	
	// 根据时间和随机种子值滚动扭曲纹理的UV
	i.uvDistTex.x += ((_Time.x + randomSeed) * _DistortTexXSpeed) % 1;
	i.uvDistTex.y += ((_Time.x + randomSeed) * _DistortTexYSpeed) % 1;
	
	// 计算扭曲的强度，并对主纹理的UV坐标进行扰动
	half distortAmnt = (tex2D(_DistortTex, i.uvDistTex).r - 0.5) * 0.2 * _DistortAmount; // 只取 r
	i.uv.x += distortAmnt;
	i.uv.y += distortAmnt;
	
	fixed4 col = tex2D(_MainTex, i.uv); // 采样主纹理颜色
	return col; // 输出最终颜色
}
```


|                 |        |                                                    |
| --------------- | ------ | -------------------------------------------------- |
| _Time           | float4 | t 是自该场景加载开始所经过的时间，4个分量分别是 (t/20, t, t*2, t*3)      |
| _SinTime        | float4 | t 是时间的正弦值，4个分量分别是 (t/8, t/4, t/2, t)               |
| _CosTime        | float4 | t 是时间的余弦值，4个分量分别是 (t/8, t/4, t/2, t)               |
| unity_DeltaTime | float4 | dt 是时间增量，4个分量的值分别是(dt, 1/dt, smoothDt, 1/smoothDt) |
https://www.yuque.com/chengxuyuanchangfeng/idsf04/iw29twwcqgi0im3h


## 火焰效果  --- 描边燃烧

```c++
Shader "Chapter1/chapter1_4" // 定义着色器名称为“Chapter1/chapter1_4”
{
    Properties
    {
        _MainTex ("Texture", 2D) = "white" {}  // 主纹理，默认为白色纹理
        _Color("Main Color", Color) = (1,1,1,1) // 主颜色，默认为白色

        _OutlineTex("Outline Texture", 2D) = "white" {} // 轮廓纹理，默认为白色纹理
        _OutlineTexXSpeed("Texture scroll speed X", Range(-50,50)) = 10 // 轮廓纹理在X轴上的滚动速度
        _OutlineTexYSpeed("Texture scroll speed Y", Range(-50,50)) = 0 // 轮廓纹理在Y轴上的滚动速度
        [HideInInspector] _RandomSeed("_MaxYUV", Range(0, 10000)) = 0.0 // 随机种子，影响轮廓随机效果
        
        [Space] // 空格，用于分隔属性
        _OutlineDistortTex("Outline Distortion Texture", 2D) = "white" {} // 轮廓失真纹理，默认为白色纹理
        _OutlineDistortAmount("Outline Distortion Amount", Range(0,2)) = 0.5 // 轮廓失真强度
        _OutlineDistortTexXSpeed("Distortion scroll speed X", Range(-50,50)) = 5 // 失真纹理在X轴的滚动速度
        _OutlineDistortTexYSpeed("Distortion scroll speed Y", Range(-50,50)) = 5 // 失真纹理在Y轴的滚动速度
        
        [Space] // 空格，用于分隔属性
        _OutlineColor("Outline Base Color", Color) = (1,1,1,1) // 轮廓的基本颜色，默认为白色
        _OutlineAlpha("Outline Base Alpha",  Range(0,1)) = 1 // 轮廓透明度，默认为1（完全不透明）
        _OutlineGlow("Outline Base Glow", Range(1,100)) = 1.5 // 轮廓发光强度
        _OutlineWidth("Outline Base Width", Range(0,0.2)) = 0.004 // 轮廓宽度
        _OutlinePixelWidth("Outline Base Pixel Width", Int) = 1 // 轮廓像素宽度，控制轮廓的精细度
    }
    SubShader
    {
        Tags {
            "Queue"="Transparent" // 设置渲染队列为透明队列，表示该对象会在不透明对象后渲染
            "RenderType"="Transparent" // 设置渲染类型为透明类型
        }

        Blend SrcAlpha OneMinusSrcAlpha // 设置混合模式，基于源Alpha进行混合
        LOD 100 // 设定Shader的细节层次为100

        Pass
        {
            CGPROGRAM
            #pragma vertex vert // 使用顶点着色器
            #pragma fragment frag // 使用片段着色器
            // 使雾效工作
            #pragma multi_compile_fog // 启用多种雾效编译选项

            #include "UnityCG.cginc" // 引入Unity的通用着色器代码库

            // 定义输入结构体，用于接收顶点数据
            struct appdata
            {
                float4 vertex : POSITION; // 顶点位置
                float2 uv : TEXCOORD0; // 顶点纹理坐标
                half4 color : COLOR; // 顶点颜色
            };

            // 定义输出结构体，传递数据到片段着色器
            struct v2f
            {
                float2 uv : TEXCOORD0; // 顶点的纹理坐标
                half4 color : COLOR; // 顶点颜色
                half2 uvOutTex : TEXCOORD1; // 用于轮廓纹理的纹理坐标
                half2 uvOutDistTex : TEXCOORD2; // 用于轮廓失真纹理的纹理坐标
                float4 vertex : SV_POSITION; // 顶点位置（裁剪空间）
            };

            // 声明所有纹理采样器和参数
            sampler2D _MainTex; // 主纹理
            float4 _MainTex_ST, _MainTex_TexelSize, _Color; // 主纹理的变换和颜色值

            sampler2D _OutlineTex; // 轮廓纹理
            half4 _OutlineTex_ST; // 轮廓纹理的变换
            half _OutlineTexXSpeed, _OutlineTexYSpeed; // 轮廓纹理滚动速度

            half4 _OutlineColor; // 轮廓的基本颜色
            half _OutlineAlpha, _OutlineGlow, _OutlineWidth; // 轮廓透明度、发光强度、宽度
            int _OutlinePixelWidth; // 轮廓的像素宽度

            sampler2D _OutlineDistortTex; // 轮廓失真纹理
            half4 _OutlineDistortTex_ST; // 轮廓失真纹理的变换
            half _OutlineDistortTexXSpeed, _OutlineDistortTexYSpeed, _OutlineDistortAmount; // 失真纹理的滚动速度和强度
            
            UNITY_DEFINE_INSTANCED_PROP(float, _RandomSeed) // 随机种子，用于每个物体实例化

            // 顶点着色器
            v2f vert (appdata v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex); // 将顶点坐标转换到裁剪空间
                o.uv = TRANSFORM_TEX(v.uv, _MainTex); // 将纹理坐标从模型空间转换到UV空间
                o.color = v.color; // 将顶点颜色传递给片段着色器
                o.uvOutTex = TRANSFORM_TEX(v.uv, _OutlineTex); // 轮廓纹理的坐标变换
                o.uvOutDistTex = TRANSFORM_TEX(v.uv, _OutlineDistortTex); // 轮廓失真纹理的坐标变换
                return o;
            }

            // 片段着色器
            fixed4 frag (v2f i) : SV_Target
            {
                half4 col = tex2D(_MainTex, i.uv); // 获取主纹理的颜色
                half originalAlpha = col.a; // 记录主纹理的Alpha值

                half randomSeed = UNITY_ACCESS_INSTANCED_PROP(Props, _RandomSeed); // 获取随机种子值

                // 处理轮廓失真
                i.uvOutDistTex.x += ((_Time.x + randomSeed) * _OutlineDistortTexXSpeed) % 1; // 轮廓失真纹理X轴滚动
                i.uvOutDistTex.y += ((_Time.x + randomSeed) * _OutlineDistortTexYSpeed) % 1; // 轮廓失真纹理Y轴滚动
                half outDistortAmnt = (tex2D(_OutlineDistortTex, i.uvOutDistTex).r - 0.5) * 0.2 * _OutlineDistortAmount; // 获取失真强度
                half2 destUv = half2(_OutlineWidth * _MainTex_TexelSize.x * 200, _OutlineWidth * _MainTex_TexelSize.y * 200); // 计算失真偏移
                destUv.x += outDistortAmnt; // 应用X轴失真
                destUv.y += outDistortAmnt; // 应用Y轴失真

                // 采样主纹理的四个方向的透明度值，来检测轮廓区域
                half spriteLeft = tex2D(_MainTex, i.uv + half2(destUv.x, 0)).a;
                half spriteRight = tex2D(_MainTex, i.uv - half2(destUv.x, 0)).a;
                half spriteBottom = tex2D(_MainTex, i.uv + half2(0, destUv.y)).a;
                half spriteTop = tex2D(_MainTex, i.uv - half2(0, destUv.y)).a;
                half result = spriteLeft + spriteRight + spriteBottom + spriteTop; // 计算轮廓效果的强度

                result = step(0.05, saturate(result)); // 通过saturate和step函数生成轮廓区域

                result *= (1 - originalAlpha) * _OutlineAlpha; // 根据主纹理透明度调整轮廓透明度

                // 轮廓纹理滚动
                i.uvOutTex.x += ((_Time.x + randomSeed) * _OutlineTexXSpeed) % 1; // 轮廓纹理X轴滚动
                i.uvOutTex.y += ((_Time.x + randomSeed) * _OutlineTexYSpeed) % 1; // 轮廓纹理Y轴滚动
                half4 tempOutColor = tex2D(_OutlineTex, i.uvOutTex); // 获取轮廓纹理的颜色
                tempOutColor *= _OutlineColor; // 应用轮廓颜色
                _OutlineColor = tempOutColor;
                half4 outline = _OutlineColor * i.color.a; // 轮廓颜色，按顶点颜色加权
                outline.rgb *= _OutlineGlow; // 应用轮廓发光效果
                outline.a = result; // 轮廓的透明度为轮廓强度

                col = lerp(col, outline, result); // 将主纹理与轮廓纹理混合
                col *= _Color; // 应用主颜色

                return col; // 返回最终的颜色结果
            }
            ENDCG
        }
    }
}
```


额外输入的属性

```c++



[Space] // 空格，用于分隔属性
_OutlineDistortTex("Outline Distortion Texture", 2D) = "white" {} // 轮廓失真纹理，默认为白色纹理
_OutlineDistortAmount("Outline Distortion Amount", Range(0,2)) = 0.5 // 轮廓失真强度
_OutlineDistortTexXSpeed("Distortion scroll speed X", Range(-50,50)) = 5 // 失真纹理在X轴的滚动速度
_OutlineDistortTexYSpeed("Distortion scroll speed Y", Range(-50,50)) = 5 // 失真纹理在Y轴的滚动速度


// 轮廓的基本属性
_OutlineColor("Outline Base Color", Color) = (1,1,1,1) // 轮廓的基本颜色，默认为白色
_OutlineAlpha("Outline Base Alpha",  Range(0,1)) = 1 // 轮廓透明度，默认为1（完全不透明）
_OutlineGlow("Outline Base Glow", Range(1,100)) = 1.5 // 轮廓发光强度
_OutlineWidth("Outline Base Width", Range(0,0.2)) = 0.004 // 轮廓宽度
_OutlinePixelWidth("Outline Base Pixel Width", Int) = 1 // 轮廓像素宽度，控制轮廓的精细度
```


主要部分

```c++
// 处理轮廓失真
i.uvOutDistTex.x += ((_Time.x + randomSeed) * _OutlineDistortTexXSpeed) % 1; // 轮廓失真纹理X轴滚动
i.uvOutDistTex.y += ((_Time.x + randomSeed) * _OutlineDistortTexYSpeed) % 1; // 轮廓失真纹理Y轴滚动
half outDistortAmnt = (tex2D(_OutlineDistortTex, i.uvOutDistTex).r - 0.5) * 0.2 * _OutlineDistortAmount; // 获取失真强度
half2 destUv = half2(_OutlineWidth * _MainTex_TexelSize.x * 200, _OutlineWidth * _MainTex_TexelSize.y * 200); // 计算失真偏移
destUv.x += outDistortAmnt; // 应用X轴失真
destUv.y += outDistortAmnt; // 应用Y轴失真

// 采样主纹理的四个方向的透明度值，来检测轮廓区域
half spriteLeft = tex2D(_MainTex, i.uv + half2(destUv.x, 0)).a;
half spriteRight = tex2D(_MainTex, i.uv - half2(destUv.x, 0)).a;
half spriteBottom = tex2D(_MainTex, i.uv + half2(0, destUv.y)).a;
half spriteTop = tex2D(_MainTex, i.uv - half2(0, destUv.y)).a;
half result = spriteLeft + spriteRight + spriteBottom + spriteTop; // 计算轮廓效果的强度

result = step(0.05, saturate(result)); // 通过saturate和step函数生成轮廓区域

result *= (1 - originalAlpha) * _OutlineAlpha; // 根据主纹理透明度调整轮廓透明度

// 轮廓纹理滚动
i.uvOutTex.x += ((_Time.x + randomSeed) * _OutlineTexXSpeed) % 1; // 轮廓纹理X轴滚动
i.uvOutTex.y += ((_Time.x + randomSeed) * _OutlineTexYSpeed) % 1; // 轮廓纹理Y轴滚动
half4 tempOutColor = tex2D(_OutlineTex, i.uvOutTex); // 获取轮廓纹理的颜色
tempOutColor *= _OutlineColor; // 应用轮廓颜色
_OutlineColor = tempOutColor;
half4 outline = _OutlineColor * i.color.a; // 轮廓颜色，按顶点颜色加权
outline.rgb *= _OutlineGlow; // 应用轮廓发光效果
outline.a = result; // 轮廓的透明度为轮廓强度

col = lerp(col, outline, result); // 将主纹理与轮廓纹理混合
col *= _Color; // 应用主颜色

return col; // 返回最终的颜色结果
```


`_MainTex_TexelSize` --- 宽高大小的倒数。

## 水平线如何做？


世界坐标 0,0,0 和  自身的世界坐标做比较。 --- yoffset

`smoothstep(edge_low, edge_up, x)`函数:

- `[edge_low, edge_up]`是指定的一个差值范围
- `x`是任意实数
- 函数结果是:

- `if x < edge_low; return 0`.
- `if x > edge_up; return 1`.
- 如果`x`处于`edge_low`和`edge_up`之间, 则返回`x`在`[0, 1]`范围内的映射值

- 比如指定范围是`[0, 10]`, `x=5`, 我们我们将其映射到`[0, 1]`之后, 对应的映射值为`0.5`
- 比如指定范围是`[0, 100]`, `x=5`, 我们我们将其映射到`[0, 1]`之后, 对应的映射值为`0.05`


## 关照模型

### 兰伯特

由于顶点数目往往远小于像素数目，因此逐顶点光照的计算量要小，效率较高。

需要法线。

```c++
// 定义输出结构体，传递数据到片段着色器
struct v2f
{
	// uv：纹理坐标
	float2 uv : TEXCOORD0;
	// vertex：变换后的顶点位置（裁剪空间位置）
	float4 vertex : SV_POSITION;
	// color：计算得到的漫反射光照颜色
	fixed3 color : COLOR;
};

// 定义 uniform 变量，用于存储外部传入的数据
uniform sampler2D _MainTex; // 纹理采样器
uniform float4 _MainTex_ST; // 纹理的平移和缩放参数

// 顶点着色器：负责处理顶点数据并进行必要的变换
v2f vert(appdata v)
{
	v2f o;
	// 将物体空间的顶点转换为裁剪空间的顶点
	o.vertex = UnityObjectToClipPos(v.vertex);
	// 变换纹理坐标
	o.uv = TRANSFORM_TEX(v.uv, _MainTex);

	// 计算世界空间的法线：将物体空间法线转换为世界空间
	fixed3 worldNormal = normalize(UnityObjectToWorldNormal(v.normal));
	// 计算世界空间的光照方向：获取光源方向并标准化
	fixed3 worldLight = normalize(_WorldSpaceLightPos0.xyz);

	// 计算漫反射光照强度（Dot product）：计算法线与光源方向的点积并应用光源的颜色
	fixed3 diffuse = _LightColor0.rgb * saturate(dot(worldNormal, worldLight));

	// 将计算的漫反射颜色传递给输出
	o.color = diffuse;

	// 返回处理后的数据
	return o;
}

// 片段着色器：负责计算每个像素的颜色
fixed4 frag(v2f i) : SV_Target
{
	// 采样纹理颜色
	fixed4 color = tex2D(_MainTex, i.uv);
	// 将纹理颜色与漫反射光照强度相乘，得到最终的颜色
	color.rgb = color.rgb * i.color;
	// 返回最终颜色
	return color;
}
```


### 半兰伯特

$$
Cdiffuse = (Clight*Mdiffuse)*((0, N•L) * 0.5 + 0.5)
$$

只有完全背光面（$N•L=-1$）时**Cdiffuse** 才会为0

`fixed3 diffuse = _LightColor0.rgb * (dot(worldNormal, worldLight) * 0.5 + 0.5);`

### Phong  Blinn-Phong

`C = C_ambient + C_diffuse + C_specular`


![700](https://s2.loli.net/2025/02/27/EIpr1DzMyahiXT9.png)


**blinn-Phong**

- **公式**：`C_specular = (C_light * M_specular)max(0,n * h)^ M_gloss;`

- C_lightr入射光颜色和强度。
- M_specular材质的高光反射系数。
- n是法线。
- h半程向量，就是i和v的半程。
- M_gloss可控制高光反射面积的大小。当 M_gloss的值越大，反射面积则越小。

- 注意上面是用的n和h做的计算，不是原来v了。


![700](https://s2.loli.net/2025/02/27/Idw6fZ2i9yHqaUV.png)

## 前向渲染，延迟渲染

https://www.yuque.com/chengxuyuanchangfeng/idsf04/ro7l5vdbu2oe9ypu

Forward渲染是每一个光源都计算一次的，Deferred是所有的光源仅仅计算一次，在多光源场景下效率更高。

在前向渲染中，影响每个对象的一些最亮的光源以完全逐像素光照模式渲染。然后，最多 4 个点光源采用每顶点计算方式。其他光源以球谐函数 (SH) 计算，这种计算方式会快得多，但仅得到近似值。光源是否为每像素光源根据以下原则而定：

- Render Mode 设置为 **Not Important** 的光源始终为每顶点或 SH 光源。
- 最亮的方向光始终为每像素光源。
- Render Mode 设置为 **Important** 的光源始终为每像素光源。


请注意，光源组会重叠；例如，最后一个每像素光源混合到每顶点光照模式，因此当对象和光源移动时，“光射量”(light popping) 较少。


#### 划重点：

就上图的官方例子里说明了，最亮用逐像素渲染，剩下最多4个用逐顶点，然后是更快的SH球谐渲染。这个SH后面再说，只需要知道消耗很少的CPU，几乎不消耗GPU，并且呢增加SH灯光的数量不会影响性能消耗。

#### 那怎么判断一个灯光是不是逐像素渲染呢？

- 渲染模式是Not Important的总是按照逐顶点或者SH方式渲染
- 按设置为Important的灯光就总是逐像素渲染了
- 最亮的（显然最亮的视觉影响比较大嘛）平行光也总是逐像素的
- 如果少于设置的Pixel Light数量，那剩下的也是逐像素渲染


### 延迟渲染又是什么？

字面意思就是推迟处理渲染的方式，优势就是有N多的实时灯光依然能保持比较流畅的帧率。主要原理就是：**灯光Pass是基于G-Buffer屏幕空间缓存和深度信息计算的光照**。那光照在屏幕空间计算，就可以避免计算那些没通过深度测试的片段，从而减少了浪费。所有灯光都是逐像素的，听起来是非常的棒，**但有一个致命的缺点就是不支持抗锯齿，也不能处理半透明。**

所以就得酌情使用了，既然是不受灯光数量影响，就主要受像素数影响，就是被光找到的物体数影响。

并且只能在MRT（多重渲染目标）、Shader Model3.0以上，且支持深度渲染贴图的显卡上才能运行


## 阴影

需要两个 pass 

一个 pass 用来渲染主要光源的投影， 额外的 处理逐像素光的投影。

> 先做主光源和阴影 ， 然后再这个基础上添加其他光源的颜色

```c++
Tags{"LightMode" = "ForwardBase"}
#pragma multi_compile_fwdbase // 多重编译，支持不同光照模型


// 定义顶点到片段的数据结构
struct v2f
{
	float4 pos : SV_POSITION;   // 裁剪空间的顶点位置
	float3 normal : TEXCOORD0; // 法线，用于光照计算
	float4 vertex : TEXCOORD1; // 模型空间的顶点位置
	SHADOW_COORDS(2)           // 使用Unity预定义宏存储阴影坐标 !!!!!!!！！！！！！！！！！！！-------------
	// 2 --- textcoord0 后面的编号
}

// 顶点着色器
v2f vert (appdata_base v)
{
	v2f o;
	o.pos = UnityObjectToClipPos(v.vertex); // 转换顶点到裁剪空间
	o.normal = v.normal;                   // 传递法线信息
	o.vertex = v.vertex;                   // 传递顶点位置
	TRANSFER_SHADOW(o)                     // 计算阴影坐标并存储 ！！！！！！！！！！！！-------------
	return o;
}
// 片段着色器
fixed4 frag (v2f i) : SV_Target
{
	// 计算法线方向
	float3 n = UnityObjectToWorldNormal(i.normal);
	n = normalize(n);

	// 计算世界空间中的光源方向
	float3 l = WorldSpaceLightDir(i.vertex);
	l = normalize(l);

	// 将顶点从模型空间转换到世界空间
	float4 worldPos = mul(unity_ObjectToWorld, i.vertex);

	// Lambert光照模型：计算法线与光线夹角的点积
	fixed ndotl = saturate(dot(n, l));
	fixed4 color = _LightColor0 * _MainColor * ndotl;

	// 叠加4个点光源的光照 ！！！！！！！！！！！！--------------
	color.rgb += Shade4PointLights(
		unity_4LightPosX0, unity_4LightPosY0, unity_4LightPosZ0, // 点光源位置
		unity_LightColor[0].rgb, unity_LightColor[1].rgb, 
		unity_LightColor[2].rgb, unity_LightColor[3].rgb,       // 点光源颜色
		unity_4LightAtten0, worldPos.rgb, n                     // 衰减和位置
	) * _MainColor;

	// 叠加环境光照
	color += unity_AmbientSky;

	// 使用Unity宏计算阴影衰减系数
	UNITY_LIGHT_ATTENUATION(shadowmask, i, worldPos.rgb) //！！！！！！！！！！！！-------------

	// 将阴影系数与颜色相乘，应用阴影效果
	color.rgb *= shadowmask;

	return color; // 返回最终颜色
}



// pass 2 ------------------------------------------------------------------
Pass
	{
		// 标签定义，此Pass用于附加光源，模式为"ForwardAdd"
		Tags{"LightMode" = "ForwardAdd"}

		// 混合模式：相加混合 !!!!!!=======================================
		Blend One One

		CGPROGRAM
		#pragma vertex vert
		#pragma fragment frag
		#pragma multi_compile_fwdadd_fullshadows // 支持多重编译，包含完整阴影
		#include "UnityCG.cginc"
		#include "Lighting.cginc"
		#include "AutoLight.cginc"

		// 定义顶点到片段的数据结构，与基础Pass一致
		struct v2f
		{
			float4 pos : SV_POSITION;
			float3 normal : TEXCOORD0;
			float4 vertex : TEXCOORD1;
			SHADOW_COORDS(2)
		};

		fixed4 _MainColor;

		// 顶点着色器
		v2f vert (appdata_base v)
		{
			v2f o;
			o.pos = UnityObjectToClipPos(v.vertex);
			o.normal = v.normal;
			o.vertex = v.vertex;
			TRANSFER_SHADOW(o)
			return o;
		}

		// 片段着色器
		fixed4 frag (v2f i) : SV_Target
		{
			// 计算法线和光照方向
			float3 n = UnityObjectToWorldNormal(i.normal);
			n = normalize(n);
			float3 l = WorldSpaceLightDir(i.vertex);
			l = normalize(l);

			// 转换顶点到世界空间
			float4 worldPos = mul(unity_ObjectToWorld, i.vertex);

			// Lambert光照计算
			fixed ndotl = saturate(dot(n, l));
			fixed4 color = _LightColor0 * _MainColor * ndotl;

			// 叠加点光源的光照
			color.rgb += Shade4PointLights(
				unity_4LightPosX0, unity_4LightPosY0, unity_4LightPosZ0,
				unity_LightColor[0].rgb, unity_LightColor[1].rgb,
				unity_LightColor[2].rgb, unity_LightColor[3].rgb,
				unity_4LightAtten0, worldPos.rgb, n
			) * _MainColor;

			// 使用阴影宏计算阴影系数
			UNITY_LIGHT_ATTENUATION(shadowmask, i, worldPos.rgb)

			// 应用阴影到颜色
			color.rgb *= shadowmask;

			return color; // 返回最终颜色
		}
		ENDCG
	}
}
```