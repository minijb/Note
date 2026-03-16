---
tags:
  - shader
---
# 透明效果

实现的两种方式 ：

- 透明度测试
- 透明度混合

渲染顺序：
1. 不透明物体
2. 透明物体按照先后 ， 后前 进行渲染

设置渲染队列

在 `SubShader` tag -- `Queue` 中进行设置

![1](https://img-blog.csdnimg.cn/direct/ab01968070f44850b43fd6512dfbfce3.png)

标签	说明
“Queue” = “Background”	值1000，此队列最先渲染。（一般用来渲染背景）
“Queue” = “Geometry”	值2000，通常是不透明物体。
“Queue” = “AlphaTest”	值2450，透贴，要么完全透明，要么完全不透明。
“Queue” = “Transparent”	值3000，常用于半透明对象，要混合的对象。
“Queue” = “Overlay”	值4000，最后渲染，用于叠加效果。

关闭深度测试  --- pass 中 `ZWrite Off`

### 透明度测试

一个偏远不满足条件 --- 则舍弃

使用 clip 进行透明度测试 

```c++
void clip(float4 x){
	if(any(x<0)) dicard;
}
```

```c++
Properties {
	_Color ("Color Tint", Color) = (1, 1, 1, 1)
	_MainTex ("Main Tex", 2D) = "white" {}
	_Cutoff ("Alpha Cutoff", Range(0, 1)) = 0.5 //用于clip的阈值
}
```

```c++
SubShader {
	Tags {"Queue"="AlphaTest" "IgnoreProjector"="True" "RenderType"="TransparentCutout"}
	Pass {
			Tags { "LightMode"="ForwardBase" }
```

- 确定渲染队列
- RenderType 将 shader  放入一个固定的组里 指名这个是使用深度测试的shader
- 取消投影器

```glsl
#pragma vertex vert
#pragma fragment frag

#include "Lighting.cginc"

fixed4 _Color;
sampler2D _MainTex;
float4 _MainTex_ST;
fixed _Cutoff;

struct a2v {
	float4 vertex : POSITION;
	float3 normal : NORMAL;
	float4 texcoord : TEXCOORD0;
};

struct v2f {
	float4 pos : SV_POSITION;
	float3 worldNormal : TEXCOORD0;
	float3 worldPos : TEXCOORD1;
	float2 uv : TEXCOORD2;
};

v2f vert(a2v v) {
	v2f o;
	o.pos = UnityObjectToClipPos(v.vertex);
	
	o.worldNormal = UnityObjectToWorldNormal(v.normal);
	
	o.worldPos = mul(unity_ObjectToWorld, v.vertex).xyz;
	
	o.uv = TRANSFORM_TEX(v.texcoord, _MainTex);
	
	return o;
}

fixed4 frag(v2f i) : SV_Target {
	fixed3 worldNormal = normalize(i.worldNormal);
	fixed3 worldLightDir = normalize(UnityWorldSpaceLightDir(i.worldPos));
	
	fixed4 texColor = tex2D(_MainTex, i.uv);
	
	// Alpha test
	clip (texColor.a - _Cutoff);
	// Equal to 
//				if ((texColor.a - _Cutoff) < 0.0) {
//					discard;
//				}
	
	fixed3 albedo = texColor.rgb * _Color.rgb;
	
	fixed3 ambient = UNITY_LIGHTMODEL_AMBIENT.xyz * albedo;
	
	fixed3 diffuse = _LightColor0.rgb * albedo * max(0, dot(worldNormal, worldLightDir));
	
	return fixed4(ambient + diffuse, 1.0);
}
```


### 透明混合

Blend：

Blend Off：关闭混合
Blend SrcFactor DstFactor：开启混合并设置混合因子。源颜色（该片元产生的颜色）会乘以SrcFactor，目标颜色（已经存在在缓冲区的颜色会乘以DstFactor），将两者相加然后再存入颜色缓冲。
Blend SrcFactor DstFactor, SrcFactorA DstFactorA：和上面几乎一样
BlendOp BlendOperation：并非简单混合，使用BlendOperation进行其他操作。


混合因子：

One：1

Zero：0

SrcColor：源颜色

SrcAlpha：源颜色透明度值

DstColor：目标颜色

DstAlpha：目标颜色透明度值

OneMinusSrcColor：1 - 源颜色

OneMinusSrcAlpha：1 - 源颜色透明度值

OneMinusDstColor：1 - 目标颜色

OneMinusDstAlpha1 - 目标颜色透明度值



$$
DST_{color} = SrcAlpha \times SrcColor + (1-SrcAlpha) \times DSTColor 
$$

```c++
Properties {
	_Color ("Color Tint", Color) = (1, 1, 1, 1)
	_MainTex ("Main Tex", 2D) = "white" {}
	_AlphaScale ("Alpha Scale", Range(0, 1)) = 1
}
SubShader {
	Tags {"Queue"="Transparent" "IgnoreProjector"="True" "RenderType"="Transparent"}
	
	Pass {
		Tags { "LightMode"="ForwardBase" }
	
		ZWrite Off
		Blend SrcAlpha OneMinusSrcAlpha
	.....
		fixed4 frag(v2f i) : SV_Target {
		fixed3 worldNormal = normalize(i.worldNormal);
		fixed3 worldLightDir = normalize(UnityWorldSpaceLightDir(i.worldPos));
		
		fixed4 texColor = tex2D(_MainTex, i.uv);
		
		fixed3 albedo = texColor.rgb * _Color.rgb;
		
		fixed3 ambient = UNITY_LIGHTMODEL_AMBIENT.xyz * albedo;
		
		fixed3 diffuse = _LightColor0.rgb * albedo * max(0, dot(worldNormal, worldLightDir));
		
		return fixed4(ambient + diffuse, texColor.a * _AlphaScale);
		}
	.....
```

修改一下渲染队列以及 rendertype

混合因子 SrcAlpha 目标颜色的混合因子  OneMinusSrcAlpha

透明通道使用 ` texColor.a * _AlphaScale`

### 开启深度写入的透明blend

使用两个 pass， 第一个开启深度写入但是不输出颜色，第二个 进行透明度混合

```c++
SubShader {
		Tags {"Queue"="Transparent" "IgnoreProjector"="True" "RenderType"="Transparent"}
		
		// Extra pass that renders to depth buffer only
		Pass {
			ZWrite On
			ColorMask 0
		}
		
		Pass {
			Tags { "LightMode"="ForwardBase" }
			
			ZWrite Off
			Blend SrcAlpha OneMinusSrcAlpha
			
			CGPROGRAM
			
			#pragma vertex vert
			#pragma fragment frag
			
			#include "Lighting.cginc"
			
			fixed4 _Color;
```

colorMask RGB | A | 0 --- 0 不输出任何颜色

可以提出被自身遮挡的片元

### shaderlab 中的混合命令

常见的混合类型

```c++
// 正常（Normal）,即透明度混合

Blend SrcAlpha OneMinusSrcAlpha

// 柔和相加(Soft Additive)

Blend OneMinusDstColor One

// 正片叠底（Multiply）,即相乘

Blend DstColor Zero

// 两倍相乘(2X Multiply)

Blend DstColor SrcColor

// 变暗(Darken)

BlendOp Min

Blend One One

// 变亮（Lighten）

BlendOp Max

Blend One One

// 滤色(Screen)

Blend OneMinusDstColor One

//等同于

Blend one OneMinusSrcColor

//线性减淡（LInear Dodge）

Blend One One
```

![wf1hO38YpIu5rSK.png](https://s2.loli.net/2024/06/28/wf1hO38YpIu5rSK.png)

### 双面渲染

Cull  Back|Front|OFF

因为 透明渲染 --- 需要关闭深度测试，这回使得渲染变得混乱

![s1DzCFxQJgijdXo.png](https://s2.loli.net/2024/06/28/s1DzCFxQJgijdXo.png)

思路： 分为两个 pass

第一个pass 只渲染背面 ， 第二个 pass  只渲染正面


```c++
		Tags {"Queue"="Transparent" "IgnoreProjector"="True" "RenderType"="Transparent"}
		
		// Extra pass that renders to depth buffer only
		Pass {
			Cull Front
			....
		}
		Pass {
			Cull Back
			....
		}
```

