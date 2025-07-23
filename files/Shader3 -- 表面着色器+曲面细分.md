
默认帮我们实现了光照

## 曲面细分


- 固定数量
- 基于变长
- 基于距离
- Phong


https://www.yuque.com/chengxuyuanchangfeng/idsf04/qh920r9xfa5rf5di

```c++
// 使用BlinnPhong光照模型，启用阴影，并添加顶点位移和细分着色。
#pragma surface surf BlinnPhong addshadow fullforwardshadows vertex:disp tessellate:tessFixed nolightmap
```


```c++
// 位移函数，对顶点位置进行调整。
void disp(inout appdata v)
{
	// 使用纹理采样lod方式获取位移贴图值，并乘以位移强度。
	float d = tex2Dlod(_DispTex, float4(v.texcoord.xy, 0, 0)).r * _Displacement;
	// 根据法线方向调整顶点位置，实现位移效果。
	v.vertex.xyz += v.normal * d;
}

// 定义细分级别变量，用于控制细分程度。
float _Tess;

// 固定细分级别函数，返回细分强度。
float4 tessFixed()
{
	return _Tess; // 由用户设置的_Tess值决定细分强度。
}


```



https://zhuanlan.zhihu.com/p/144400261  曲面细分

https://docs.unity3d.org.cn/6000.0/Documentation/Manual/SL-SurfaceShaderTessellation.html


## 制作水面

```c++
Properties
{
	_Color ("Color", Color) = (0,0,1,1) // 水体基础颜色
	_WaveHeight ("WaveHeight", float) = 1 // 波浪高度
	_WaveSpeed ("WaveSpeed", float) = 1 // 波浪速度
	_WaveGap ("WaveGap", float) = 1 // 波浪间隔
	_FoamTex ("FoamTex", 2D) = "white" {} // 泡沫纹理
	_NormalTex ("NormalTex", 2D) = "white" {} // 法线贴图
	_NormalScale ("NormalScale", float) = 1 // 法线强度
	_NormalSpeed ("NormalSpeed", float) = 1 // 法线贴图移动速度
}


// 顶点着色器函数
void vertexDataFunc(inout appdata_full v, out Input o)
{
	UNITY_INITIALIZE_OUTPUT(Input, o); // 初始化输出结构
	// 计算波浪高度，使用正弦函数模拟波浪效果
	fixed height = sin(_Time.y * _WaveSpeed + v.vertex.z * _WaveGap + v.vertex.x) * _WaveHeight;
	// 根据法线方向调整顶点位置，形成波浪效果
	v.vertex.xyz += v.normal * height;
}

```


https://www.yuque.com/chengxuyuanchangfeng/idsf04/grldtw06tlezapq8#578b06ca


```c++
float2 speed = _Time.x * float2(_WaveSpeed, _WaveSpeed) * _NormalSpeed;
```

- **_Time.x**：Unity 的内置变量，表示从游戏开始到现在的时间（以秒为单位）。
- **_WaveSpeed**：控制波浪速度的参数。
- **_NormalSpeed**：控制法线贴图移动速度的参数。
- **speed**：计算出的 UV 偏移量，用于动态移动法线贴图的采样位置。

 
 **采样法线贴图**

```
fixed3 bump1 = UnpackNormal(tex2D(_NormalTex, IN.uv_FoamTex.xy + speed)).rgb;
fixed3 bump2 = UnpackNormal(tex2D(_NormalTex, IN.uv_FoamTex.xy - speed)).rgb;
```

- **_NormalTex**：法线贴图，存储了切线空间中的法线信息。
- **IN.uv_FoamTex.xy**：泡沫纹理的 UV 坐标（这里被复用于法线贴图的采样）。
- **tex2D**：采样法线贴图，返回一个包含法线信息的四维向量。
- **UnpackNormal**：将法线贴图中的压缩数据解包为三维法线向量。

**含义**：

- 对法线贴图进行两次采样：

- `bump1`：UV 坐标向正方向偏移 (`+speed`)。
- `bump2`：UV 坐标向负方向偏移 (`-speed`)。

- 这种双向采样可以增强波浪的动态效果，使法线变化更加自然。

法线合并，并调整强度。


