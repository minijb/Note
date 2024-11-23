---
tags:
  - shader
---
## 光源

光与物体相交的结果 : **散射** **吸收**

散射: 不改变密度和颜色，只改变方向  --- 分为 反射，折射
吸收：改变密度和颜色，不改变方向

使用不同部分计算不同的散射方向: 
- **高光反射** 如何反射光线
- **漫反射** 折射，吸收，散射的表面

### 标准光照模型

分为四个部分:

- emissive : 自发光
- speccular ： 高光反射
- diffuse ： 漫反射
- ambient ： 环境光

### 环境光

- 全局变量

$$
c_{ambient} = g_{ambient}
$$

### 自发光

自己发光，但是不作为光源

$$
c_{emission} = m_{emission}
$$

### 漫反射

遵循 兰伯特定律。

$$
C_{diffuse} = (C_{light} \cdot m_{diffuse}) max(0, \hat{n} \cdot \hat{l})
$$

$m_{diffuse}$  为 漫反射颜色


### 高光反射

phong 模型

$$
c_{specular} = (c_{light} \cdot m_{specular}) max(0, \hat{v} \cdot \hat{r})^{M_{gloss}}
$$

$\hat{r}$ 为反射光线。

Blinn 模型使用半程向量，简化了方程

$$
\hat{h} = \frac {\hat{v} + \hat{l}}{\left |  \hat{v} + \hat{l}   \right |} 
$$

只需要计算 $\hat{h}$ 和 $\hat{n}$ 的夹角大小就可以了

### unity 中的环境光

window - render - lighting - environment 

shader 中 就可以 使用 `UNITY_LIGHTMODEL_AMBIENT`

```glsl
Shader "Book/C5/diffuse Shader"
{
    Properties
    {
        _Diffuse ("Diffuse", Color) = (1.0, 1.0, 1.0, 1.0)
    }
    SubShader
    {
     
        Pass{
            //  只有正确的定义 LightMode 才可以得到 Unity 的光照变量
            Tags {"LightMode"="ForwardBase"}

            CGPROGRAM

                #pragma vertex vert
                #pragma fragment frag
                #include "Lighting.cginc"

                struct a2v{
                    float4 vertex : POSITION; 
                    float3 normal : NORMAL; 
                };


                struct v2f{
                    float4 position : SV_POSITION;
                    float3 color : COLOR;
                };

                fixed4 _Diffuse;

                v2f vert(a2v v){

                    v2f o;
                    o.position = UnityObjectToClipPos(v.vertex);

                    fixed3 ambient = UNITY_LIGHTMODEL_AMBIENT;// 环境光照
                    

                    fixed3 worldNormal = normalize(mul(v.normal, (float3x3)unity_WorldToObject));
                    fixed3 worldLight = normalize(_WorldSpaceLightPos0.xyz);

                    fixed3 diffuse = _LightColor0.rgb * _Diffuse.rgb * saturate(dot(worldNormal, worldLight));

                    o.color = ambient + diffuse;
                    return o;
                }


                fixed4 frag(v2f i): SV_TARGET {

                    return fixed4(i.color, 1.0);
                }
            ENDCG
        }
    }
    FallBack "Diffuse"
}

```

平行光： `normalize(_WorldSpaceLightPos0.xyz)`

**注意：** 这个内置变量，需要定义合适的 LIGHT_MODE ，同时本节我们只有一个光源，如果有多个光源同时类型不一，我们就不能直接使用这个内置变量。


**逐片元**

```glsl
Shader "Book/C5/diffuse Shader"
{
    Properties
    {
        _Diffuse ("Diffuse", Color) = (1.0, 1.0, 1.0, 1.0)
    }
    SubShader
    {
     
        Pass{
            //  只有正确的定义 LightMode 才可以得到 Unity 的光照变量
            Tags {"LightMode"="ForwardBase"}

            CGPROGRAM

                #pragma vertex vert
                #pragma fragment frag
                #include "Lighting.cginc"

                struct a2v{
                    float4 vertex : POSITION; 
                    float3 normal : NORMAL; 
                };


                struct v2f{
                    float4 position : SV_POSITION;
                    float3 worldNormal : TEXCOORD0;
                };

                fixed4 _Diffuse;

                v2f vert(a2v v){

                    v2f o;
                    o.position = UnityObjectToClipPos(v.vertex);

                    o.worldNormal = normalize(mul(v.normal, (float3x3)unity_WorldToObject));

                    return o;
                }


                fixed4 frag(v2f i): SV_TARGET {

                    fixed3 ambient = UNITY_LIGHTMODEL_AMBIENT;// 环境光照
                    fixed3 worldLight = normalize(_WorldSpaceLightPos0.xyz);

                    fixed3 diffuse = _LightColor0.rgb * _Diffuse.rgb * saturate(dot(i.worldNormal, worldLight));

                    fixed3 color = ambient + diffuse;

                    return fixed4(color, 1.0);
                }
            ENDCG
        }
    }
    FallBack "Diffuse"
}

```

**saturate**

```c#
float saturate(float x)
{
     return max(0.0, min(1.0, x));

}
```
### 半兰伯特模型

$$
C_{diffuse} = (C_{light} \cdot m_{diffuse})(\alpha(\hat{n} \cdot \hat{l}) + \beta)
$$

区别就在 max 那边 $\alpha, \beta$ 都是 0.5

这样背面就不会是一整个同样的颜色

```glsl
fixed3 diffuse = _LightColor0.rgb * _Diffuse.rgb * (0.5 + 0.5* dot(i.worldNormal, worldLight));

```

![400](https://s2.loli.net/2024/06/07/LDipg36sdEnkB8W.png)


### 加入高光

使用  CG 提供的计算反射方向的函数 reflect(i,n) i为入射方向，n为法线

```hlsl
// Upgrade NOTE: replaced '_Object2World' with 'unity_ObjectToWorld'

Shader "Book/C5/Specular Shader"
{
    Properties
    {
        _Diffuse ("Diffuse", Color) = (1.0, 1.0, 1.0, 1.0)
        _Specular ("Specular", Color) = (1.0, 1.0, 1.0, 1.0)
        _Gloss ("Gloss", Range(8.0, 256)) = 20
    }
    SubShader
    {
     
        Pass{
            //  只有正确的定义 LightMode 才可以得到 Unity 的光照变量
            Tags {"LightMode"="ForwardBase"}

            CGPROGRAM

                #pragma vertex vert
                #pragma fragment frag
                #include "Lighting.cginc"

                struct a2v{
                    float4 vertex : POSITION; 
                    float3 normal : NORMAL; 
                };


                struct v2f{
                    float4 position : SV_POSITION;
                    float3 worldNormal : TEXCOORD0;
                    float3 worldPos: TEXCOORD1;
                };

                fixed4 _Diffuse;
                fixed4 _Specular;
                float _Gloss;

                v2f vert(a2v v){

                    v2f o;
                    o.position = UnityObjectToClipPos(v.vertex);

                    o.worldNormal = normalize(mul(v.normal, (float3x3)unity_WorldToObject));
                    o.worldPos = mul(unity_ObjectToWorld, v.vertex).xyz;

                    return o;
                }


                fixed4 frag(v2f i): SV_TARGET {

                    fixed3 ambient = UNITY_LIGHTMODEL_AMBIENT;// 环境光照
                    fixed3 worldLightDir = normalize(_WorldSpaceLightPos0.xyz);
                  
                    fixed3 diffuse = _LightColor0.rgb * _Diffuse.rgb * saturate(dot(i.worldNormal, worldLightDir));

                    fixed3 reflectDir = normalize(reflect(-worldLightDir, i.worldNormal));

                    fixed3 viewDir = normalize(_WorldSpaceCameraPos.xyz - i.worldPos);
                    fixed3 specular = _LightColor0.rgb * _Specular.rgb * pow(saturate(dot(reflectDir, viewDir)), _Gloss);

                    fixed3 color = ambient + diffuse + specular;

                    return fixed4(color, 1.0);
                }
            ENDCG
        }
    }
    FallBack "Diffuse"
}

```


**Blinn**

```glsl
fixed4 frag(v2f i): SV_TARGET {

	fixed3 ambient = UNITY_LIGHTMODEL_AMBIENT;// 环境光照
	fixed3 worldLightDir = normalize(_WorldSpaceLightPos0.xyz);
  
	fixed3 diffuse = _LightColor0.rgb * _Diffuse.rgb * saturate(dot(i.worldNormal, worldLightDir));

	fixed3 reflectDir = normalize(reflect(-worldLightDir, i.worldNormal));
	fixed3 viewDir = normalize(_WorldSpaceCameraPos.xyz - i.worldPos);
	fixed3 halfDir = normalize(worldLightDir+ viewDir); 

			
	fixed3 specular = _LightColor0.rgb * _Specular.rgb * pow(max(0, dot(i.worldNormal, halfDir)), _Gloss);

	fixed3 color = ambient + diffuse + specular;

	return fixed4(color, 1.0);
}
```


- `_WorldSpaceCameraPos` camera 空间位置
- `_WorldSpaceLightPos0` 光线方向

### unity 内置函数

- float3 WorldSpaceViewDir (float4 v)——输入一个**模型空间中的顶点位置**，返回**世界空间中从该点到摄像机的观察方向**。内部实现使用了UnityWorldSpaceViewDir函数
- float3 UnityWorldSpaceViewDir (float4 v)——输入一个**世界空间中的顶点位置**，**返回世界空间中该点到摄像机的观察方向**
- float3 ObjSpaceViewDir (float4 v)——输入一个**模型空间中的顶点位置**，**返回模型空间中从该点到摄像机的观察方向**
- float3 WorldSpaceLightDir (float4 v)——**仅可用于向前渲染**中。输入一个**模型空间中的顶点位置，返回世界中从该点到光源的光照方向**。内部实现使用了UnityWorldSpaceLightDir函数。没有被归一化
- float3 UnityWorldSpaceLightDir (float4 v)——仅用于向前渲染中。输入一个世界空间中的顶点位置，返回世界空间中从该点到光照方向。没有被归一化
- float3 ObjSpaceLightDir (float4 v)——仅用于向前渲染中。输入一个模型空间中的顶点位置，返回模型空间中从该点到光源的光照方向。没有被归一化
- float3 UnityObjectToWorldNormal (float3 norm)——把**法线方向从模型空间转换到世界空间中**
- float3 UnityObjectToWorlDir (float3 dir)——把**方向矢量从模型空间变换的世界空间**中
- float3 UnityWorldToObject (float3 dir)——把**方向矢量从世界空间变换到模型空间中**

需要注意，需要手动 归一化

为什么有些函数仅仅只能用于向前渲染：只有在向前渲染的时候 `_WorldSpaceLightPos0` 才会被正确表示

```glsl
fixed4 frag(v2f i): SV_TARGET {

	fixed3 ambient = UNITY_LIGHTMODEL_AMBIENT;// 环境光照
	fixed3 worldLightDir = normalize(UnityWorldSpaceLightDir(i.worldPos));
  
	fixed3 diffuse = _LightColor0.rgb * _Diffuse.rgb * saturate(dot(i.worldNormal, worldLightDir));

   
	fixed3 viewDir = normalize(UnityWorldSpaceViewDir(i.worldPos));
	fixed3 halfDir = normalize(worldLightDir + viewDir); 

			
	fixed3 specular = _LightColor0.rgb * _Specular.rgb * pow(max(0, dot(i.worldNormal, halfDir)), _Gloss);

	fixed3 color = ambient + diffuse + specular;

	return fixed4(color, 1.0);
}
```