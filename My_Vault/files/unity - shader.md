---
tags:
  - unity
---
## 关键字 

**内置变量** https://docs.unity.cn/cn/2019.4/Manual/SL-UnityShaderVariables.html


应用 -> vertex

| 关键字       | 意义              |
| --------- | --------------- |
| POSITION  | object position |
| NORMAL    | 法线              |
| TEXCOORD0 | 纹理编号            |
| TANGENTG  | 切线              |
| COLOR     | 顶点颜色            |

vertex -> fragment

| SV_POSITION | ClipPosition |
| ----------- | ------------ |
| SV_TARGET   | 目标颜色         |
| COLOR0      |              |
| COLOR1      |              |
| TEXTURE0-7  |              |

## 函数

空间转换函数

- UnityObjectToClipPos

## 规范

1. a2v : application to vertex
2. v2f ： vertex to fragment

## 属性类型

1. Color , Vector : float/half/fixed4,
2. Range, Float : float half, fixed
3. 2D : sampler2D
4. Cube : samplerCube
5. 3D  : sampler3D


## 内置

### 1. 包

UnityCG.cginc : 包含常用使用的帮助函数，宏，结构体
UnityShaderVariables.cginc : Unity Shader 自动包含， 包含需要内置的全局变量
Lighting.cginc ： 包含内置的光照模型
HLSLSupport.cginc : 自动包含


### 2. 内置结构体

```c++

struct appdata_base {
    float4 vertex : POSITION;//顶点位置
    float3 normal : NORMAL;//发现
    float4 texcoord : TEXCOORD0;//纹理坐标
    UNITY_VERTEX_INPUT_INSTANCE_ID
};
 
struct appdata_tan {
    float4 vertex : POSITION;//顶点坐标位置
    float4 tangent : TANGENT;//切线
    float3 normal : NORMAL;//法线
    float4 texcoord : TEXCOORD0;//第一纹理坐标
    UNITY_VERTEX_INPUT_INSTANCE_ID
};
 
struct appdata_full {
    float4 vertex : POSITION;
    float4 tangent : TANGENT;
    float3 normal : NORMAL;
    float4 texcoord : TEXCOORD0;
    float4 texcoord1 : TEXCOORD1;//第二纹理坐标
    float4 texcoord2 : TEXCOORD2;//第三纹理坐标
    float4 texcoord3 : TEXCOORD3;//第四纹理坐标
    fixed4 color : COLOR;//顶点颜色
    UNITY_VERTEX_INPUT_INSTANCE_ID
}
```


### 3. 内置函数

| 函数名                                                | 描述                                                                                  |
| -------------------------------------------------- | ----------------------------------------------------------------------------------- |
| float3 WorldSpaceViewDir(float4 localPos )         | 输入一个模型顶点坐标，得到世界空间中从该点到摄像机的观察方向。（方向没单位化）---- **ViewDir**<br>                         |
| float3 ObjSpaceViewDir(float4 v )                  | 输入一个模型顶点坐标，得到模型空间中从该点到摄像机的观察方向。（方向没单位化）----- **ViewDir**                            |
| float3 WorldSpaceLightDir(float4 localPos )        | 输入一个模型顶点坐标，得到世界空间中从该点到光源（`_WorldSpaceLightPos0`）的光照方向。（方向没单位化） --- **LightDir**<br> |
| float3 ObjSpaceLightDir(float4 v )                 | 输入一个模型顶点坐标，得到模型空间中从该点到光源（`_WorldSpaceLightPos0`）的光照方向。（方向没单位化） --- **LightDir**     |
| float3 UnityObjectToWorldNormal(float3 norm )      | 将法线从模型空间转换到世界空间（方向已单位化） --- **NORMAL**<br>                                          |
| float3 UnityObjectToWorldDir(float3 dir )          | 把方向矢量从模型空间转换到世界空间（方向已单位化） --- **DIR**<br>                                           |
| float3 UnityWorldToObjectDir(float3 dir )          | 把方向矢量从世界空间转换到模型空间（方向已单位化） ---- **DIR**<br>                                          |
| float4 UnityWorldToClipPos(float3 pos )            | 把世界坐标空间中某一点pos变换到齐次裁剪空间  --- **Position**<br>                                       |
| float4 UnityViewToClipPos(float3 pos )             | 把观察坐标空间中某一点pos变换到齐次裁剪空间  --- **Position**<br>                                       |
| float3 UnityObjectToViewPos(float3 pos或float4 pos) | 模型局部空间坐标系中某一个点pos变换到观察空间坐标系  --- **Position**<br>                                   |
| float3 UnityWorldToViewPos(float3 pos )            | 把世界坐标系下的一个点pos变换到观察空间坐标系  --- **Position**<br>                                      |
|                                                    |                                                                                     |

https://blog.csdn.net/u012722551/article/details/103926660


## shader

### diffuse

顶点 diffuse 公式 ：

$$
c_{diffuse} = (c_{light} \cdot m_{diffuse}) max(0, \hat{n} \cdot  \hat{l})
$$

其中 $\hat{n}$ 为法线 $\hat{l}$ 为光源方向 --- 点乘 得到 $\cos \eta$  $m_{diffuse}$ 漫反射系数

![[diffuse.excalidraw]]


saturate ： 输出 0-1

利用顶点

```c++
	v2f vert(a2v v) {
		v2f o;
		// Transform the vertex from object space to projection space
		o.pos = UnityObjectToClipPos(v.vertex);
		
		// Get ambient term
		fixed3 ambient = UNITY_LIGHTMODEL_AMBIENT.xyz;
		
		// Transform the normal from object space to world space
		// fixed3 worldNormal = normalize(mul(v.normal, (float3x3)unity_WorldToObject));
		fixed3 worldNormal = normalize(UnityObjectToWorldNormal(v.normal));
		// Get the light direction in world space
		fixed3 worldLight = normalize(_WorldSpaceLightPos0.xyz);
		// Compute diffuse term
		fixed3 diffuse = _LightColor0.rgb * _Diffuse.rgb * saturate(dot(worldNormal, worldLight));
		
		o.color = ambient + diffuse;
		
		return o;
	}
	
	fixed4 frag(v2f i) : SV_Target {
		return fixed4(i.color, 1.0);
	}
```


利用片元

```c++

	struct a2v {
		float4 vertex : POSITION;
		float3 normal : NORMAL;
	};
	
	struct v2f {
		float4 pos : SV_POSITION;
		float3 worldNormal : TEXCOORD0;
	};
	
	v2f vert(a2v v) {
		v2f o;
		// Transform the vertex from object space to projection space
		o.pos = UnityObjectToClipPos(v.vertex);

		// Transform the normal from object space to world space
		o.worldNormal = UnityObjectToWorldNormal(v.normal);

		return o;
	}
	
	fixed4 frag(v2f i) : SV_Target {
		// Get ambient term
		fixed3 ambient = UNITY_LIGHTMODEL_AMBIENT.xyz;
		
		// Get the normal in world space
		fixed3 worldNormal = normalize(i.worldNormal);
		// Get the light direction in world space
		fixed3 worldLightDir = normalize(_WorldSpaceLightPos0.xyz);
		
		// Compute diffuse term
		fixed3 diffuse = _LightColor0.rgb * _Diffuse.rgb * saturate(dot(worldNormal, worldLightDir));
		
		fixed3 color = ambient + diffuse;
		
		return fixed4(color, 1.0);
	}
```


**半兰伯特**


$$
c_{diffuse} = (c_{light} \cdot m_{diffuse}) (0.5 \hat{n} \cdot  \hat{l} + 0.5)
$$


### 高光 specular 

![[specular.excalidraw]]


$$
c_{specular} = (c_{light} \cdot m_{specular}) max(0, \hat{n} \cdot \hat{h})^{m_{gloss}}
$$


$m_{gloss}$ 光泽度 ： 用来调整光斑的大小

$$
\hat{h} = \frac{\hat{v} + \hat{l}}{\left | \hat{v} + \hat{l} \right |}
$$
其中 $\hat{v}, \hat{l}$ 都是单位向量， 此时， $\hat{h}$ 就是中线。 此时只需要计算 法线 $\hat{n}$ 和 $\hat{h}$ 的夹角就可以确认位置。

```c#
fixed4 frag(v2f i) : SV_Target {
	// Get ambient term
	fixed3 ambient = UNITY_LIGHTMODEL_AMBIENT.xyz;
	
	fixed3 worldNormal = normalize(i.worldNormal);
	fixed3 worldLightDir = normalize(_WorldSpaceLightPos0.xyz);
	
	// Compute diffuse term
	fixed3 diffuse = _LightColor0.rgb * _Diffuse.rgb * max(0, dot(worldNormal, worldLightDir));
	
	// Get the view direction in world space
	fixed3 viewDir = normalize(_WorldSpaceCameraPos.xyz - i.worldPos.xyz);
	// Get the half direction in world space
	fixed3 halfDir = normalize(worldLightDir + viewDir);
	// Compute specular term
	fixed3 specular = _LightColor0.rgb * _Specular.rgb * pow(max(0, dot(worldNormal, halfDir)), _Gloss);
	
	return fixed4(ambient + diffuse + specular, 1.0);
}
```

`_WorldSpaceLightPos0`  方向光


**使用内置变量**

```c#
fixed4 frag(v2f i) : SV_Target {
	fixed3 ambient = UNITY_LIGHTMODEL_AMBIENT.xyz;
	
	fixed3 worldNormal = normalize(i.worldNormal);
	//  Use the build-in funtion to compute the light direction in world space
	// Remember to normalize the result
	fixed3 worldLightDir = normalize(UnityWorldSpaceLightDir(i.worldPos));
	
	fixed3 diffuse = _LightColor0.rgb * _Diffuse.rgb * max(0, dot(worldNormal, worldLightDir));
	
	// Use the build-in funtion to compute the view direction in world space
	// Remember to normalize the result
	fixed3 viewDir = normalize(UnityWorldSpaceViewDir(i.worldPos));
	fixed3 halfDir = normalize(worldLightDir + viewDir);
	fixed3 specular = _LightColor0.rgb * _Specular.rgb * pow(max(0, dot(worldNormal, halfDir)), _Gloss);
	
	return fixed4(ambient + diffuse + specular, 1.0);
}
```


## Texture

1. 在属性中添加一个纹理
2. 在CG中添加 两个变量

- `_MainTex_ST, _MainTex` --- ST为纹理的平移和缩放值


```c++

Properties {
	_Color ("Color Tint", Color) = (1, 1, 1, 1)
	_MainTex ("Main Tex", 2D) = "white" {}
	_Specular ("Specular", Color) = (1, 1, 1, 1)
	_Gloss ("Gloss", Range(8.0, 256)) = 20
}


fixed4 _Color;
sampler2D _MainTex;
float4 _MainTex_ST;
fixed4 _Specular;
float _Gloss;

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
	
	o.uv = v.texcoord.xy * _MainTex_ST.xy + _MainTex_ST.zw; // 得到UV坐标
	// Or just call the built-in function
//				o.uv = TRANSFORM_TEX(v.texcoord, _MainTex);
	
	return o;
}

fixed4 frag(v2f i) : SV_Target {
	fixed3 worldNormal = normalize(i.worldNormal);
	fixed3 worldLightDir = normalize(UnityWorldSpaceLightDir(i.worldPos));
	
	// Use the texture to sample the diffuse color ！！！！！！！！
	fixed3 albedo = tex2D(_MainTex, i.uv).rgb * _Color.rgb;
	
	fixed3 ambient = UNITY_LIGHTMODEL_AMBIENT.xyz * albedo;
	
	fixed3 diffuse = _LightColor0.rgb * albedo * max(0, dot(worldNormal, worldLightDir));
	
	fixed3 viewDir = normalize(UnityWorldSpaceViewDir(i.worldPos));
	fixed3 halfDir = normalize(worldLightDir + viewDir);
	fixed3 specular = _LightColor0.rgb * _Specular.rgb * pow(max(0, dot(worldNormal, halfDir)), _Gloss);
	
	return fixed4(ambient + diffuse + specular, 1.0);
}
			
```


**纹理属性**

1. Alpha from Grayscale ，字面意思
2. WrapMode 重复模式 ： reapeat ， clamp
3. Filter mode ： 纹理由于变换而产生拉伸时将采用哪种滤波模式， 消耗依次增大
4. MipMap ： 在Advanced 中开启
5. 最大纹理尺寸和纹理模式
	- 根据不同设备选择不同最大尺寸
	- 如果导入的纹理超过最大值， 会自动缩放最大分辨率。
	- formate 使用那种格式来存储纹理 
	- 尽量使用压缩格式

## 凹凸映射

**不同坐标空间的法线纹理**


**1. 模型空间**

直接定义纹理方向(模型空间)。

**2.  切线空间**

原点就是顶点， z轴： 法线， x轴是顶点的切线方向 $t$ , y轴 ： 副切线方向 $b$ 。

优势： 1. 自由度高 2. 可以进行 UV动画 3. 可以重用法线纹理 4. 可压缩