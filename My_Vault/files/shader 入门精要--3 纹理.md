---
tags:
  - shader
---
使用纹理 : 

```c#
   Properties{
    _Color ("Color Tint", Color) = (1,1,1,1)
    _MainTex ("Main Texture", 2D) = "White" {}
    _Specular ("Specular", Color) = (1,1,1,1)
    _Gloss ("Gloss", Range(8.0, 256)) = 20
   }
```

这里  "White"  是内置纹理

需要用到的变量

```shader
fixed4 _Color;
sampler2D _MainTex;
float4 _MainTex_ST;
fixed4 _Specular;
float _Gloss;
```

xxxx_ST 存储纹理的属性，可以得到纹理的缩放值，偏移值，

分别对应 : `_MainTex_ST.xy` , `_MainTex_ST.zw`

```shader
v2f vert(a2v v){

	v2f o;
	o.position = UnityObjectToClipPos(v.vertex);

	o.worldNormal = normalize (UnityObjectToWorldNormal(v.normal));
	o.worldPos = mul(unity_ObjectToWorld, v.vertex).xyz;
	// o.uv = v.texcoord.xy * _MainTex_ST.xy + _MainTex_ST.zw;
	o.uv = TRANSFORM_TEX(v.texcoord, _MainTex_ST);

	return o;
}
```

UV进行缩放再进行位移。

fragment

```shader
fixed4 frag(v2f i): SV_TARGET {

	fixed3 worldLightDir = normalize(UnityWorldSpaceLightDir(i.worldPos));
  
	fixed3 albedo = tex2D(_MainTex, i.uv).rgb * _Color.rgb;

	fixed3 ambient = UNITY_LIGHTMODEL_AMBIENT * albedo;
	fixed3 diffuse = _LightColor0.rgb *albedo  * saturate(dot(i.worldNormal, worldLightDir));
   
	fixed3 viewDir = normalize(UnityWorldSpaceViewDir(i.worldPos));
	fixed3 halfDir = normalize(worldLightDir + viewDir); 

			
	fixed3 specular = _LightColor0.rgb * _Specular.rgb * pow(max(0, dot(i.worldNormal, halfDir)), _Gloss);

	fixed3 color = ambient + specular + diffuse;

	return fixed4(color, 1.0);
}
```

步骤 : 
- `o.uv = TRANSFORM_TEX(v.texcoord, _MainTex_ST);` 自动得到 UV


- albedo : 纹理的颜色
- 利用纹理颜色得到 乘 原始漫反射 的颜色
- ambient 同理

> 高光不需要 ： 因为纯白色，没有原始的颜色。其他需要显示纹理颜色。

## 纹理属性

常用属性都在 texture 中， 同时修改 offset 和 Tilling 在纹理中。

可以为不同平台设置不同的最大纹理分辨率，以及 formate 格式、


## 凹凸映射

使用 切线空间的法线纹理。

 模型空间优势：

- 实现简单，计算简单
- 可以提供平滑的边界

切线空间

- 自由度高  --- 相对切线
- 可以进行 UV 动画
- 可以重用
- 可以压缩

计算过程

- 将光线和视角方向变换到切线空间下进行计算
- 将法线方向变换到世界空间进行计算

### 切线空间

需要的属性

```hlsl
   Properties{
    _Color ("Color Tint", Color) = (1,1,1,1)
    _MainTex ("Main Texture", 2D) = "White" {}
    _Specular ("Specular", Color) = (1,1,1,1)
    _Gloss ("Gloss", Range(8.0, 256)) = 20
    _BumpMap("Normal Map", 2D) = "Bump" {}
    _BumpScale("Bump Scale", Float) = 1.0
   }
```

`_BumpScale` 光线的影响程度

**a2v**

```glsl
struct a2v{
	float4 vertex : POSITION; 
	float3 normal : NORMAL; 
	float4 tangent : TANGENT;
	float4 texcoord : TEXCOORD0;
};
```

`TANGENT` 顶点的切线  --- float4 使用 w 确定 副切线的方向


```hlsl
v2f vert(a2v v){

	v2f o;
	o.pos = UnityObjectToClipPos(v.vertex);

	o.uv.xy = v.texcoord.xy * _MainTex_ST.xy + _MainTex_ST.zw;
	o.uv.zw = v.texcoord.xy * _BumpMap_ST.xy + _BumpMap_ST.zw;

	TANGENT_SPACE_ROTATION;

	o.lightDir = mul(rotation, ObjSpaceLightDir(v.vertex)).xyz;
	o.viewDir= mul(rotation, ObjSpaceViewDir(v.vertex)) .xyz;


	return o;
}


fixed4 frag(v2f i): SV_TARGET {
	fixed3 tangentLightDir = normalize(i.lightDir);
	fixed3 tangentViewDir = normalize(i.viewDir);
	
	// Get the texel in the normal map
	fixed4 packedNormal = tex2D(_BumpMap, i.uv.zw);
	fixed3 tangentNormal;
	// 将法向量映射回来
	// If the texture is not marked as "Normal map"
//				tangentNormal.xy = (packedNormal.xy * 2 - 1) * _BumpScale;
//				tangentNormal.z = sqrt(1.0 - saturate(dot(tangentNormal.xy, tangentNormal.xy)));
	
	// Or mark the texture as "Normal map", and use the built-in funciton
	tangentNormal = UnpackNormal(packedNormal);
	tangentNormal.xy *= _BumpScale;
	tangentNormal.z = sqrt(1.0 - saturate(dot(tangentNormal.xy, tangentNormal.xy)));
	
	fixed3 albedo = tex2D(_MainTex, i.uv).rgb * _Color.rgb;
	
	fixed3 ambient = UNITY_LIGHTMODEL_AMBIENT.xyz * albedo;
	
	fixed3 diffuse = _LightColor0.rgb * albedo * max(0, dot(tangentNormal, tangentLightDir));

	fixed3 halfDir = normalize(tangentLightDir + tangentViewDir);
	fixed3 specular = _LightColor0.rgb * _Specular.rgb * pow(max(0, dot(tangentNormal, halfDir)), _Gloss);
	
	return fixed4(ambient + diffuse + specular, 1.0);

}
```

**要点**

相等

```glsl
TANGENT_SPACE_ROTATION;

// Compute the binormal
float3 binormal = cross( normalize(v.normal), normalize(v.tangent.xyz) ) * v.tangent.w;
// Construct a matrix which transform vectors from object space to tangent space
float3x3 rotation = float3x3(v.tangent.xyz, binormal, v.normal);
```

乘 `v.tangent.w` 选择正确的 副切线方向！！！！

由于 法线为单位向量，因此我们可以直接通过 xy 得到 w

```glsl
tangentNormal = UnpackNormal(packedNormal);
tangentNormal.xy *= _BumpScale;
tangentNormal.z = sqrt(1.0 - saturate(dot(tangentNormal.xy, tangentNormal.xy)));
```

注意 ： unity 会根据不同的平台使用不同的 打包方式，因此推荐使用 `UnpackNormal` 而不是自己计算


```glsl
bump.xy *= _BumpScale;
bump.z = sqrt(1.0 - saturate(dot(bump.xy, bump.xy)));
```

z -- > 就是法线

如果 不需要偏移 则 xy = 0 ；那么自然 z 就是 1 。 那么就是普通的法线。
### 世界空间

```hlsl
struct a2v{
	float4 vertex : POSITION; 
	float3 normal : NORMAL; 
	float4 tangent : TANGENT;
	float4 texcoord : TEXCOORD0;
};


struct v2f{
	float4 pos : SV_POSITION;
	float4 uv : TEXCOORD0;
	float4 TtoW0 : TEXCOORD1;
	float4 TtoW1 : TEXCOORD2;
	float4 TtoW2 : TEXCOORD3;

};

v2f vert(a2v v){

	v2f o;
	o.pos = UnityObjectToClipPos(v.vertex);

	o.uv.xy = v.texcoord.xy * _MainTex_ST.xy + _MainTex_ST.zw;
	o.uv.zw = v.texcoord.xy * _BumpMap_ST.xy + _BumpMap_ST.zw;

	float3 worldPos = mul(unity_ObjectToWorld, v.vertex).xyz;  
	fixed3 worldNormal = UnityObjectToWorldNormal(v.normal);  
	fixed3 worldTangent = UnityObjectToWorldDir(v.tangent.xyz);  
	fixed3 worldBinormal = cross(worldNormal, worldTangent) * v.tangent.w; 



	o.TtoW0 = float4(worldTangent.x, worldBinormal.x, worldNormal.x, worldPos.x);
	o.TtoW1 = float4(worldTangent.y, worldBinormal.y, worldNormal.y, worldPos.y);
	o.TtoW2 = float4(worldTangent.z, worldBinormal.z, worldNormal.z, worldPos.z);



	return o;
}


fixed4 frag(v2f i): SV_TARGET {
	// Get the position in world space		
	float3 worldPos = float3(i.TtoW0.w, i.TtoW1.w, i.TtoW2.w);
	// Compute the light and view dir in world space
	fixed3 lightDir = normalize(UnityWorldSpaceLightDir(worldPos));
	fixed3 viewDir = normalize(UnityWorldSpaceViewDir(worldPos));
	
	// Get the normal in tangent space
	fixed3 bump = UnpackNormal(tex2D(_BumpMap, i.uv.zw));
	bump.xy *= _BumpScale;
	bump.z = sqrt(1.0 - saturate(dot(bump.xy, bump.xy)));
	// Transform the narmal from tangent space to world space
	bump = normalize(half3(dot(i.TtoW0.xyz, bump), dot(i.TtoW1.xyz, bump), dot(i.TtoW2.xyz, bump)));
	
	fixed3 albedo = tex2D(_MainTex, i.uv).rgb * _Color.rgb;
	
	fixed3 ambient = UNITY_LIGHTMODEL_AMBIENT.xyz * albedo;
	
	fixed3 diffuse = _LightColor0.rgb * albedo * max(0, dot(bump, lightDir));

	fixed3 halfDir = normalize(lightDir + viewDir);
	fixed3 specular = _LightColor0.rgb * _Specular.rgb * pow(max(0, dot(bump, halfDir)), _Gloss);
	
	return fixed4(ambient + diffuse + specular, 1.0);
}


```


`float4 TtoW0 : TEXCOORD1;`
`float4 TtoW1 : TEXCOORD2;`
`float4 TtoW2 : TEXCOORD3;`

这样来表示矩阵 ， 一个插值寄存器最多存储 float4

同时我们将 世界坐标放在最后一位

计算：

```hlsl
bump = normalize(half3(dot(i.TtoW0.xyz, bump), dot(i.TtoW1.xyz, bump), dot(i.TtoW2.xyz, bump)));
```

## 渐变纹理

```glsl
fixed4 frag(v2f i) : SV_Target {
	fixed3 worldNormal = normalize(i.worldNormal);
	fixed3 worldLightDir = normalize(UnityWorldSpaceLightDir(i.worldPos));
	
	fixed3 ambient = UNITY_LIGHTMODEL_AMBIENT.xyz;
	
	// Use the texture to sample the diffuse color !!!!!!!
	fixed halfLambert  = 0.5 * dot(worldNormal, worldLightDir) + 0.5;
	fixed3 diffuseColor = tex2D(_RampTex, fixed2(halfLambert, halfLambert)).rgb * _Color.rgb;
	
	fixed3 diffuse = _LightColor0.rgb * diffuseColor;
	
	fixed3 viewDir = normalize(UnityWorldSpaceViewDir(i.worldPos));
	fixed3 halfDir = normalize(worldLightDir + viewDir);
	fixed3 specular = _LightColor0.rgb * _Specular.rgb * pow(max(0, dot(worldNormal, halfDir)), _Gloss);
	
	return fixed4(ambient + diffuse + specular, 1.0);
}
```


`fixed halfLambert  = 0.5 * dot(worldNormal, worldLightDir) + 0.5;`

之前半兰伯特模型 ---- 得到的值 ---- 将原本  `[-1 - 1]` 转到 0-1 ，这部分使用 结合 法线贴图 --- 对于控制光影效果很好

## 遮罩纹理

将原本 三个通道的值 作为 mask，

```glsl
fixed4 frag(v2f i) : SV_Target {
	fixed3 tangentLightDir = normalize(i.lightDir);
	fixed3 tangentViewDir = normalize(i.viewDir);

	fixed3 tangentNormal = UnpackNormal(tex2D(_BumpMap, i.uv));
	tangentNormal.xy *= _BumpScale;
	tangentNormal.z = sqrt(1.0 - saturate(dot(tangentNormal.xy, tangentNormal.xy)));

	fixed3 albedo = tex2D(_MainTex, i.uv).rgb * _Color.rgb;
	
	fixed3 ambient = UNITY_LIGHTMODEL_AMBIENT.xyz * albedo;
	
	fixed3 diffuse = _LightColor0.rgb * albedo * max(0, dot(tangentNormal, tangentLightDir));
	
	fixed3 halfDir = normalize(tangentLightDir + tangentViewDir);
	// Get the mask value
	fixed specularMask = tex2D(_SpecularMask, i.uv).r * _SpecularScale;
	// Compute specular term with the specular mask
	fixed3 specular = _LightColor0.rgb * _Specular.rgb * pow(max(0, dot(tangentNormal, halfDir)), _Gloss) * specularMask;

	return fixed4(ambient + diffuse + specular, 1.0);
}
```

这里将 使用r 通道的值控制镜面反射的强度

