---
tags:
  - 面试
  - shader
---
https://www.yuque.com/chengxuyuanchangfeng/idsf04/hrtq5eqarkgzcsb3


**几何着色器有意思的地方在于它可以把（一个或多个）顶点转变为完全不同的基本图形（primitive），从而生成比**

**原来多得多的顶点。**


```c++
[maxcertexcount(N)]
void ShaderName (PrimitiveType InputVertexType InputName[NumElements],
                inout StreamOutputObjectVertexType) OutputName){
    // 几何着色器具体实现
}
```


`[maxvertexcount(N)]`用来指定几何着色器单词调用所输出的顶点数量最大值。其中，N是几何着色器**单次调用**所输出的顶点数量最大值。几何着色器每次输出的顶点个数都可能不同，但是这个数量却不能超过之前定义的最大值。  
出于对性能方面的考虑，我们应当令maxvertexcount的值尽可能小。线管资料显示，GS每次输出的标量数量在1-20时，它将发挥出最佳的性能；而当27-40时，它的性能将下降到峰值性能的50%。

每次调用几何着色器所输出的标量个数为：maxvertexcount与输出顶点类型结构体中标量个数的乘积。例如，如果顶点结构体定义了`float3 pos : POSITION`与`float2 tex : COORD0`，即顶点元素中含有5个标量。假设此时将maxvertexcount设置为4，则几何着色器每次输出20个标量，以峰值性能执行。


### 输入输出

几何着色器的输入参数必须是一个定义有特定图元的顶点数组，点应输入一个顶点，线条列表/带应输入两个顶点，三角形列表/带应输入3个顶点，线及邻接图元为4个顶点，三角形及其邻接图元则为6个顶点。  
输入参数以图元类型作为前缀，用以描述输入到几何着色器的具体图元类型。并且注意，**输入图元类型必须对应输入装配阶段的图元拓扑类型**，否则会出现顶点不匹配的现象。该前缀可以是下列类型之一：

- `point`：输入图元拓扑类型为点列表
- `line`：输入图元拓扑类型为线列表或线条带
- `triangle`：输入的图元拓扑类型为三角形列表或三角形带
- `lineadj`：输入的图元拓扑类型为线条列表/带及其邻接图元
- `triangleadj`：输入的图元为三角形列表/带及其邻接图元

几何着色器的输出参数是标有`inout`修饰符的**流类型(stream type)** 。流类型存有一系列顶点，它们定义了几何着色器输出的几何图形。  
流类型的本质是一种模板类型(template type)，其模板参数用以指定输出顶点的具体类型。流类型有如下3种：

- `PointStream<OutputVertexType>`：一系列顶点所定义的点列表
- `LineStream<OutputVertexType>`：一系列顶点所定义的线条带
- `TriangleStream<OutputVertexType>`：一系列顶点所定义的三角形带

几何着色器输出的多个顶点会够成图元，图元的输出类型由流类型来指定。对于线条与三角形来说，几何着色器输出的对应图元拓扑类型必须是**线条带与三角形带**。而线条列表与三角形列表可以借助内置函数`RestarStrip`输出。

由于大多数模型图元拓扑类型都是三角形带，所以其实输入一般都是`triangle`。


### Append

`Append`函数用来将几何着色器的输出数据追加到一个现有的流中。

```
[maxcertexcount(N)]
void ShaderName (PrimitiveType InputVertexType InputName[NumElements],
                inout StreamOutputObjectVertexType) OutputName){
    // 几何着色器具体实现
    StreamOutputObjectVertexType gout;
    OutputName.Append(gout);
}
```

### RestartStrip

`RestartStrip`函数用来结束当前的基元条带，开始一个新的条带。如果当前的条带没有足够的顶点被追加出来以填满基元拓扑结构，那么末端的不完整基元将被丢弃。  
前面提到，几何着色器输出的图元拓扑类型只能是线条带或三角形带，但总有带状结构无法表示的情况(或者说过载了想不出来)，这时候就可以用`RestartStrip`来重置输出流，采用类似三角形列表的方式追加几个三角形。


```c++
[maxcertexcount(N)]
void ShaderName (PrimitiveType InputVertexType InputName[NumElements],
                inout StreamOutputObjectVertexType) OutputName){
    // 几何着色器具体实现
    StreamOutputObjectVertexType gout;
    OutputName.Append(gout);
    OutputName.RestartStrip();
    OutputName.Append(gout);
}
```


https://zhuanlan.zhihu.com/p/585436751


## point

```c++
#pragma geometry geom  // 使用名为geom的几何着色器

// 输入顶点结构体，包含顶点位置和纹理坐标
struct a2v
{
	float4 vertex : POSITION;  // 顶点位置
	float2 uv : TEXCOORD0;     // 顶点纹理坐标
};

// 顶点着色器到几何着色器之间的中间结构体
struct v2g
{
	float4 vertex : POSITION;  // 顶点位置
	float2 uv : TEXCOORD0;     // 顶点纹理坐标
};

// 从几何着色器到片段着色器之间的数据结构
struct g2f
{
	float4 vertex : SV_POSITION;  // 变换后的顶点位置
	float2 uv : TEXCOORD0;        // 纹理坐标
};

// 声明_MainTex纹理采样器和ST变换矩阵
sampler2D _MainTex;
float4 _MainTex_ST;

// 顶点着色器函数
v2g vert (a2v v)
{
	v2g o;
	o.vertex = v.vertex;  // 传递顶点位置
	o.uv = TRANSFORM_TEX(v.uv, _MainTex);  // 变换纹理坐标
	return o;
}

// 几何着色器函数
[maxvertexcount(1)]  // 每个几何着色器输出1个顶点
void geom(triangle v2g input[3], inout PointStream<g2f> outStream)
{
	// 计算输入的3个顶点的平均位置和纹理坐标
	float4 vertex = float4(0, 0, 0, 0);
	float2 uv = float2(0, 0);

	vertex = (input[0].vertex + input[1].vertex + input[2].vertex) / 3;  // 计算平均顶点位置
	uv = (input[0].uv + input[1].uv + input[2].uv) / 3;  // 计算平均纹理坐标

	// 输出到片段着色器的数据
	g2f o;
	o.vertex = UnityObjectToClipPos(vertex);  // 将顶点位置转换为裁剪空间
	o.uv = uv;  // 设置纹理坐标

	outStream.Append(o);  // 将输出数据加入到流中
}

// 片段着色器函数
fixed4 frag (g2f i) : SV_Target
{
	fixed4 col = tex2D(_MainTex, i.uv);  // 从_MainTex纹理中采样颜色
	return col;  // 返回采样的颜色
}
ENDCG

```


## 线


```c++
// 几何着色器函数
[maxvertexcount(6)] // 最大顶点输出数为6个（因为每条边输出2个顶点，总共3条边）
void geom(triangle v2g input[3], inout LineStream<g2f> outStream)
{
	// 遍历三角形的3个顶点
	for (int i = 0; i < 3; i++)
	{
		g2f o;

		// 处理当前顶点，将其转换为裁剪空间坐标并设置纹理坐标
		o.vertex = UnityObjectToClipPos(input[i].vertex); // 将顶点位置从对象空间转换到裁剪空间
		o.uv = input[i].uv; // 传递纹理坐标

		// 将当前顶点添加到输出流
		outStream.Append(o);

		// 计算当前顶点的下一个顶点（形成边）
		int next = (i + 1) % 3; // 使用环形索引来获得下一个顶点

		// 处理下一个顶点
		o.vertex = UnityObjectToClipPos(input[next].vertex); // 将下一个顶点的位置转换到裁剪空间
		o.uv = input[next].uv; // 传递下一个顶点的纹理坐标

		// 将下一个顶点添加到输出流
		outStream.Append(o);
	}
}

```