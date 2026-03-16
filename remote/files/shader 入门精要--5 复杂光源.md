---
tags:
  - shader
---
## shaderpath

shader path 决定 光照如何应用到 shader 

主要有两种：

- forward rendering path
- deferred rendering path

设置： project setting -> player -> other settings -> rendering path

使用多种类型

- 在不同的camera 中切换 rendering path

LightMode 类型


![VFBXNoiLzdTt6Cj.png](https://s2.loli.net/2024/06/28/VFBXNoiLzdTt6Cj.png)

### forward

原理：
每进行一次完整的前向渲染，我们需要渲染该对象的渲染图元，并计算两个缓冲区的信息：一个是颜色缓冲区，一个是深度缓冲区。我们利用深度缓冲来决定一个片元是否可见，如果可见就更新颜色缓冲区中的颜色值。
每个光源都需要一个pass，最后在帧缓冲内进行混合

unity 中的 forward

对于 **每个模型** 中的 **每个片元** 如果深度测试通过则计算光照

前向渲染路径有3种处理光照（即照亮物体）的方式：**逐顶点处理**、**逐像素处理**、**球谐函数**（Spherical Harmonics, SH）处理。

Unity使用的判断规则如下：

- 场景中最亮的平行光总是按逐像素处理的。
- 渲染模式被设置成Not Important的光源，会按逐顶点或者SH处理。
- 渲染模式被设置成Important的光源，会按逐像素处理。
- 如果根据以上规则得到的逐像素光源数量小于Quality Setting中的逐像素光源数量(Pixel Light Count)，会有更多的光源以逐像素的方式进行渲染。


两种不同的前线 pass

![6wifAbkzuolBN1K.png](https://s2.loli.net/2024/06/28/6wifAbkzuolBN1K.png)

说明 ：

- 除了 pass 标签外，还有 `#prama muti_compile_fwdbase/add` 保证生成不同的shader
- base pass 默认支持阴影， add pass 默认不支持 ---- 可以使用 `#prama multi_compile_fwdadd_fullshadows` 答题 `#prama multi_compile_fwdadd`
- 环境+自发光 都是在 base pass 计算，如果在 add 中计算会重复。
- 在 add 中开启了混合模式， 希望每个光照结果叠加。 否则会覆盖。
- 通常定义一个base pass（双面这种强制的除外） 以及一个 addtion pass 。base 执行一次， add会根据其他光的数目执行多次。

> base : 只计算一次，--- 计算环境光，自发光 以及 **最终重要的光**
> add ： 
#### 内置的光照变量和函数

![ruI5foN3LWvziaH.png](https://s2.loli.net/2024/06/28/ruI5foN3LWvziaH.png)


![RKHmMSijwqbBZzc.png](https://s2.loli.net/2024/06/28/RKHmMSijwqbBZzc.png)

### 延迟渲染

两个 pass  一个仅仅计算哪些片元可见并存储需要的参数， 第二个pass 进行计算

延迟渲染的缺点：

- 不支持真正的抗锯齿（anti-aliasing）功能。
- 不能处理半透明物体。
- 对显卡有一定要求。如果要使用延迟渲染的话，显卡必须支持MRT（Multiple Render Targets）、Shader Mode 3.0及以上、深度渲染纹理以及双面的模板缓冲。

G缓冲区

RT0 : RGB存储漫反射颜色，A没有
RT1 ：RGB存储高光反射颜色，A存储指数的部分
RT2 : RGB 用于存储法线，A没用
RT3 ：存储自发光+lightmap+反射探针
深度缓冲，模板缓冲


## 光源类型

1. 平行光
2. 点光线
3. 聚光灯

可访问类型： **位置，方向，颜色，强度，衰减**

shader

[[forward_render]]

**Bass pass**

```c
v2f vert(a2v v) {
	v2f o;
	o.pos = UnityObjectToClipPos(v.vertex);
	
	o.worldNormal = UnityObjectToWorldNormal(v.normal);
	
	o.worldPos = mul(unity_ObjectToWorld, v.vertex).xyz;
	
	return o;
}

fixed4 frag(v2f i) : SV_Target {
	fixed3 worldNormal = normalize(i.worldNormal);
	fixed3 worldLightDir = normalize(_WorldSpaceLightPos0.xyz);
	
	fixed3 ambient = UNITY_LIGHTMODEL_AMBIENT.xyz;
	
	fixed3 diffuse = _LightColor0.rgb * _Diffuse.rgb * max(0, dot(worldNormal, worldLightDir));

	fixed3 viewDir = normalize(_WorldSpaceCameraPos.xyz - i.worldPos.xyz);
	fixed3 halfDir = normalize(worldLightDir + viewDir);
	fixed3 specular = _LightColor0.rgb * _Specular.rgb * pow(max(0, dot(worldNormal, halfDir)), _Gloss);

	fixed atten = 1.0;
	
	return fixed4(ambient + (diffuse + specular) * atten, 1.0);
}	
```


> 一定是平型光，因此只需要知道 **方向** `_WorldSpaceLightPos0` ，颜色和强度就在 `_LightColor0`, 同时没有衰竭


**addition pass**

```c

Pass {
	// Pass for other pixel lights
	Tags { "LightMode"="ForwardAdd" }
	
	Blend One One  --------------- !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


v2f vert(a2v v) {
	v2f o;
	o.pos = UnityObjectToClipPos(v.vertex);
	
	o.worldNormal = UnityObjectToWorldNormal(v.normal);
	
	o.worldPos = mul(unity_ObjectToWorld, v.vertex).xyz;
	
	return o;
}

fixed4 frag(v2f i) : SV_Target {
	fixed3 worldNormal = normalize(i.worldNormal);
	#ifdef USING_DIRECTIONAL_LIGHT
		fixed3 worldLightDir = normalize(_WorldSpaceLightPos0.xyz);
	#else
		fixed3 worldLightDir = normalize(_WorldSpaceLightPos0.xyz - i.worldPos.xyz);
	#endif
	
	fixed3 diffuse = _LightColor0.rgb * _Diffuse.rgb * max(0, dot(worldNormal, worldLightDir));
	
	fixed3 viewDir = normalize(_WorldSpaceCameraPos.xyz - i.worldPos.xyz);
	fixed3 halfDir = normalize(worldLightDir + viewDir);
	fixed3 specular = _LightColor0.rgb * _Specular.rgb * pow(max(0, dot(worldNormal, halfDir)), _Gloss);
	
	#ifdef USING_DIRECTIONAL_LIGHT
		fixed atten = 1.0;
	#else
		#if defined (POINT)
			float3 lightCoord = mul(unity_WorldToLight, float4(i.worldPos, 1)).xyz;
			fixed atten = tex2D(_LightTexture0, dot(lightCoord, lightCoord).rr).UNITY_ATTEN_CHANNEL;
		#elif defined (SPOT)
			float4 lightCoord = mul(unity_WorldToLight, float4(i.worldPos, 1));
			fixed atten = (lightCoord.z > 0) * tex2D(_LightTexture0, lightCoord.xy / lightCoord.w + 0.5).w * tex2D(_LightTextureB0, dot(lightCoord, lightCoord).rr).UNITY_ATTEN_CHANNEL;
		#else
			fixed atten = 1.0;
		#endif
	#endif

	return fixed4((diffuse + specular) * atten, 1.0);
}
```

> 因为 会计算多个光源，因此开启混合 `Blend One One
> 1. 不计算环境光 和 自发光
> 2. 使用宏命令区分不同光的类型

计算衰竭的代码

```c
#if defined (POINT)
	float3 lightCoord = mul(unity_WorldToLight, float4(i.worldPos, 1)).xyz;
	fixed atten = tex2D(_LightTexture0, dot(lightCoord, lightCoord).rr).UNITY_ATTEN_CHANNEL;
#elif defined (SPOT)
	float4 lightCoord = mul(unity_WorldToLight, float4(i.worldPos, 1));
	fixed atten = (lightCoord.z > 0) * tex2D(_LightTexture0, lightCoord.xy / lightCoord.w + 0.5).w * tex2D(_LightTextureB0, dot(lightCoord, lightCoord).rr).UNITY_ATTEN_CHANNEL;
```

通过查找纹理得到衰竭 `tex2D(_LightTexture0, dot(lightCoord, lightCoord).rr).UNITY_ATTEN_CHANNEL`


最主要平行光 使用 base ，其他使用 根据 Auto num 使用 add。 修改 ： Edit -> project settings -> quality -> pixel light count. 

如何确定重要性：如果是 Auto 根据位置，强度等。可以自己设置render mode： important 或者 not important。

> 现在还没有 逐顶点和SH, 因此使用 not important 

### 光照衰减

使用纹理存储的弊端：

- 纹理大小会影响精度
- 不直观不方便

但是可以提高性能

**光照纹理**

使用 `_LightTexture0` 的纹理来计算光源衰竭。如果使用了 cookie 那么问纹理就是 `_LightTextureB0` 

确定改点在 光源空间的位置 
根据空间位置得到距离中心的距离，并根据这个距离来对纹理进行采样.
`UNITY_ATTEN_CHANNEL` 使用宏 来得到得到 衰竭值所在的分量(**就是哪个通道**)。

```c
float3 lightcoord = mul(_LightMatrix0, float4(i.worldPosition, 1)).xyz;
fixed atten = tex2D(_LightTexture0, dot(lightCoord, lightCoord).rr).UNITY_ATTEN_CHANNEL;
```

**使用公式计算**

```c
float distance = length(_WorldSpaceLightPos0.xyz - i.worldPosstion.xyz);
atten = 1.0 / distance;
```

## 阴影

实现 ： 将相机 放到 光源上， 此时 看不到的地方就是阴影

实现方法： 将相机放在光源上 ， 进行深度测试 (L) ，原本的深度值 (E) E > L -> 可见，但是处于阴影中

unity 中可用的设置：

1 ： 可渲染物体中 的 cast shadow 以及 receive shadow 

![400](https://s2.loli.net/2024/07/12/YRH6KJWA7hz2Gx8.png)
2. 在光源中设置阴影的属性

![KeycJRvqWPmraLT.png](https://s2.loli.net/2024/07/12/KeycJRvqWPmraLT.png)

默认的shadowshader

```c
	CGPROGRAM
	#pragma vertex vert
	#pragma fragment frag
	#pragma target 2.0
	#pragma multi_compile_shadowcaster
	#pragma multi_compile_instancing // allow instanced shadow pass for most of the shaders
	#include "UnityCG.cginc"

	struct v2f {
		V2F_SHADOW_CASTER;
	};

	v2f vert( appdata_base v )
	{
		v2f o;
		TRANSFER_SHADOW_CASTER_NORMALOFFSET(o)
		return o;
	}

	float4 frag( v2f i ) : SV_Target
	{
		SHADOW_CASTER_FRAGMENT(i)
	}
	ENDCG
```

如果只有一面投射阴影 ： 可以将物体的castshadow 设置为 two side.

### 让物体可以接受阴影

[[Shadow shader]]

在 v2f中添加一个变量 

```c
struct v2f {
	float4 pos : SV_POSITION;
	float3 worldNormal : TEXCOORD0;
	float3 worldPos : TEXCOORD1;
	SHADOW_COORDS(2)
};
```

声明一个用于阴影纹理采样的坐标， 添加插值寄存器的索引

在vert中使用宏 计算纹理坐标

```c
v2f vert(a2v v) {
	v2f o;
	o.pos = UnityObjectToClipPos(v.vertex);
	
	o.worldNormal = UnityObjectToWorldNormal(v.normal);

	o.worldPos = mul(unity_ObjectToWorld, v.vertex).xyz;
	
	// Pass shadow coordinates to pixel shader
	TRANSFER_SHADOW(o);
	
	return o;
}
```

在 frag 中 使用宏 计算阴影的值

```c
fixed4 frag(v2f i) : SV_Target {
	fixed3 worldNormal = normalize(i.worldNormal);
	fixed3 worldLightDir = normalize(_WorldSpaceLightPos0.xyz);
	
	fixed3 ambient = UNITY_LIGHTMODEL_AMBIENT.xyz;

	fixed3 diffuse = _LightColor0.rgb * _Diffuse.rgb * max(0, dot(worldNormal, worldLightDir));

	fixed3 viewDir = normalize(_WorldSpaceCameraPos.xyz - i.worldPos.xyz);
	fixed3 halfDir = normalize(worldLightDir + viewDir);
	fixed3 specular = _LightColor0.rgb * _Specular.rgb * pow(max(0, dot(worldNormal, halfDir)), _Gloss);

	fixed atten = 1.0;
	
	fixed shadow = SHADOW_ATTENUATION(i);
	
	return fixed4(ambient + (diffuse + specular) * atten * shadow, 1.0);
}
```

SHADOW_COORDS, TRANSFER_SHADOW, SHADOW_ATTENUATION 就是计算阴影的三剑客

**内部原理**

SHADOW_COORDS -- 声明 一个 `_ShadowCoord` 的阴影纹理坐标。

TRANSFER_SHADOW -- 根据平台不同而不同，简单来说就是将值从模型空间变换到光源空间。

SHADOW_ATTENUATION -- 采样纹理，得到颜色值。

> 注意： 如果使用宏，需要将变量设置为固定的名字如 v.vertex或a.pos, 

最后我们只需要将 shadow 和 颜色值相乘就可以了。

> 这里只改变了 base pass  ，add pass 差不多