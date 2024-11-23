---
tags:
  - shader
---
## Shader 基础结构

```glsl
Shader "Custom/shader"
{
    Properties
    {
		 _Color ("Color", Color) = (1,1,1,1)
    }
    SubShader
    {
       Pass {
       }
    }
    SubShader
    {
       
    }

    FallBack "Diffuse"
}

```

**Properties** :  连接材质和shader

结构 : `Nmae ("displayName", PropertyType) = DefaultType`

**SubShader** : 轻量级成员

选择一个适合平台的 subshader。

结构: 一系列pass， 以及 tag 和 状态

```hlsl
    SubShader
    {
	    // selectable
	    [tag]
		[RenderSetup]
		
       Pass {
       }
    }
```

rendersetup :  渲染选项，如深度测试，混合模式，剔除模式的呢。

tag ： 告诉 shader 怎样或者何时渲染对象

- Queue : 渲染队列
- RenderType ： 着色器分类
- DisableBatch
- ForceNoShaderCasting
- IgnoreProjector ： 常用于半透明物体
-  ....

**Pass** 

```glsl
Pass {
	[Name]
	[Tags]
	[RenderType]
	// other code
}
```

RenderType : 同上
Tags ： 功能同上，但是选项不同

> 特殊的pass：
> UsePass 使用其他Shader 的Pass
> GrabPass 过去屏幕结果并存储在纹理中。

**FallBack** ： 所有的SubShader都不行的后路

## 基础

关闭 skybox ： window -> rendering -> lighting 

```glsl
// Upgrade NOTE: replaced 'mul(UNITY_MATRIX_MVP,*)' with 'UnityObjectToClipPos(*)'

Shader "Book/C5/Simple Shader"
{
    Properties
    {

    }
    SubShader
    {
     
        Pass{
            CGPROGRAM

                #pragma vertex vert
                #pragma fragment frag

                float4 vert(float4 v : POSITION) : SV_POSITION{
                    return UnityObjectToClipPos (v);
                }


                fixed4 frag(): SV_TARGET {
                    return fixed4(1.0, 1.0,1.0,1.0);
                }
            ENDCG
        }
    }
    FallBack "Diffuse"
}

```

POSITION, SV_POSITION, SV_TARGET 都是关键字

使用结构体实现多个参数的输入

```glsl
struct a2v{
	float4 ver : POSITION; // 模型空间的坐标
	float3 normal : NORMAL; // 法线
	float4 texcoord : TEXCOORD0; //纹理坐标
};

float4 vert(a2v v) : SV_POSITION{
	return UnityObjectToClipPos(v.ver);
}

```

**顶点和片元着色之间的通信**

```glsl
#pragma vertex vert
#pragma fragment frag

struct a2v{
	float4 ver : POSITION; // 模型空间的坐标
	float3 normal : NORMAL; // 法线
	float4 texcoord : TEXCOORD0; //纹理坐标
};

struct v2f{
	float4 pos : SV_POSITION;
	float3 color : COLOR0;
};

v2f vert(a2v v){

	v2f o;
	o.pos = UnityObjectToClipPos(v.ver);
	o.color = v.normal * 0.5 + fixed3(0.5, 0.5, 0.5);
	return o;
}



fixed4 frag(v2f i): SV_TARGET {
	return fixed4(i.color, 1.0);
}
```

**利用属性**

在 Properties 中进行设置，

```glsl
Properties
{
	_Color ("Color Tint", Color) = (1.0, 1.0, 1.0, 1.0)
}

Pass{
 CGPROGRAM

	 #pragma vertex vert
	 #pragma fragment frag

	 struct a2v{
		 float4 ver : POSITION; // 模型空间的坐标
		 float3 normal : NORMAL; // 法线
		 float4 texcoord : TEXCOORD0; //纹理坐标
	 };


	 struct v2f{
		 float4 pos : SV_POSITION;
		 float3 color : COLOR0;
	 };


	 fixed4 _Color;

	 v2f vert(a2v v){

		 v2f o;
		 o.pos = UnityObjectToClipPos(v.ver);
		 o.color = v.normal * 0.5 + fixed3(0.5, 0.5, 0.5);
		 return o;
	 }


	 fixed4 frag(v2f i): SV_TARGET {

		 fixed3 c = i.color;
		 c *= _Color.rgb;
		 return fixed4(c, 1.0);
	 }
 ENDCG
}
```

Pass 中也需要一个和 Property 中一样名称的变量。

| ShaderLab属性类型 | CG变量类型              |
| ------------- | ------------------- |
| Color,Vector  | float4,half4,fixed4 |
| Range,Float   | float,half,fixed    |
| 2D            | sampler2D           |
| Cube          | samplerCube         |
| 3D            | sampler3D           |

| 类型    | 精度                                        |
| ----- | ----------------------------------------- |
| float | 最高精度的浮点值，通常使用32位来存储                       |
| half  | 中等精度的浮点值，通常使用16位来存储，精度范围是-600 000~+60 000 |
| fixed | 最低精度的浮点值，通常使用11位来存储，精度范围-2.0~+2.0         |


## 内置文件和变量

```glsl
#include "xxx.xx"
```

常用文件

- `UnityCG.cginc` 常用帮助函数，宏，结构体
- `UnityShaderVarables.cginc` 自动包含，有很多内置的全局变量。
- `Lighting.cginc` 内置光照模型，如果使用 surface shader 会被自动包含
- `HLSLSupport.cginc` 很多用于跨平台的宏和定义

`UnityCG.cginc` 内常用的结构体

**顶点着色器输入**
- appdata_base :  顶点位置，顶点法线，第一组纹理坐标
- appdata_tan : 顶点位置，顶点切线，顶点法线，第一组纹理坐标
- appdata_full : 顶点位置，顶点切线，顶点法线，四组纹理坐标
- appdata_img : 顶点位置，第一组纹理坐标

**顶点输出**

- v2f_img : 裁剪空间位置，纹理坐标

**常用函数**

WorldSpaceVireDir
ObjSpaceVireDir
WorldSpaceLightDir
ObjSpaceVireDir

UnityObjectToWorldNormal
UnityObjectToWorldDir
UnityWorldToObjectDir

## 语义

赋给shader输入输出的字符串，表达了这里的参数的含义。让shader 知道从哪里读取数据，并把数据输出到哪里。

SV_xxx 系统数值语义，在渲染管线中有意义。


## 调试

frame debugger

RenderDoc