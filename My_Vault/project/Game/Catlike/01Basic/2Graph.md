
## 预制件

将对象拖到 project 窗口创建预制件 prefeb。其中粗体表示当前对象 覆盖了 预制件的值。

![200](https://catlikecoding.com/unity/tutorials/basics/building-a-graph/creating-a-line-of-cubes/prefab-instance-inspector.png)


> 进入预制件设置的方法 ： 对象的右箭头， inspector 上方的open，双击assert中的预制件资源。

我们修改预制件，所有子集都会进行改变。例如，改变预制件的比例也会改变场景中立方体的比例。但是，每个实例使用自己的位置和旋转。此外，游戏对象实例可以被修改，这将覆盖预制件的值。请注意，预制和实例之间的关系在播放模式下被打破。

### 实例化

通过 `Object.Instantiate` 方法进行实例化。

> 继承链 MonoBehaviour -> Behaviour -> Component -> Object

实例化多个物体

```c#
[SerializeField]
private Transform pointPrefab;

void Awake()
{
	//初始化变量那个
	var position = Vector3.zero;
	var scale = Vector3.one / 5f;
	
	//循环
	for (int i = 0; i < 10; i++)
	{
		Transform point = Instantiate(pointPrefab);
		//确定x的位置
		position.x = (i + 0.5f) / 5f - 1f;
		point.localPosition = position;
		point.localScale = scale;
	}
}
```

切换 camera 的投影方法 ： main camera 对象中的 *Projection* 。天空盒也在附近。

### 对可实例化的变量进行限制

```c#
[SerializeField, Range(10,100)] 
private int reslution = 10;
```

### 设置实例化对象的父级

一旦实例化数量过多的话。unity窗口会被大量占据。我们可以将实例化的对象挂载到一个父对象上。其中需要一个 Transformer 类型的变量，**我们可以直接通过 `transformer` 变量得到当前类 --- 也就是 Graph 的 transformer 类型。**

```c#
Transform point = Instantiate(pointPrefab);
point.SetParent(transform, false);
```

当一个新的父对象被设置时，**Unity将尝试保持对象在其原始世界的位置、旋转和比例，此处我们并不需要。因此我们将第二个参数设置为 false**。此后所有实例化的对象都会出现在 `Graph` 对象的队列中。

## 为cube添加颜色

最简单方法：设置材质的颜色。但是如果cube的数量过多的话，需要的材质数量就多，因此我们需要一种独特的材质，根据位置改变颜色。此时我们需要做的就是制作自己的shader。我们创建一个标准表面shader。

> Unity提供了一个框架来快速生成执行默认照明计算的着色器，您可以通过调整某些值来影响它。这样的着色器被称为表面着色器。不幸的是，它们只适用于默认渲染管道。稍后我们将介绍通用渲染管道。

shader的语法独立，但是类似c#。

### unity shader 语法介绍

```shader
Shader "Graph/Point Surface" {
	
	SubShader {}
	
	FallBack "Diffuse"
}
```

一个 `Shader` 可以包含多个 `SubShader` , 同时subshader下面需要一个混合 `CG` 和 `HLSL` 的代码部分，需要卸载 `CGPROGRAM`  `ENDCG`  之间。

```shader
SubShader {
	CGPROGRAM
	ENDCG
}
```

我们首先需要一个编译标识符，并接指令

```
CGPROGRAM
#pragma surface ConfigureSurface Standard fullforwardshadows
#pragma target 3.0
struct Input {
	float3 worldPos;
};
void ConfigureSurface (Input input, inout SurfaceOutputStandard surface) {}

ENDCG
```

指示着色器编译器生成具有标准照明和完全支持阴影的表面着色器，ConfigureSurface引用了一个用于配置着色器的方法，我们必须创建这个方法。随后我们设置版本。

接下来我们定义输入的结构体用于输入到 `configuration` 方法中，必须为 `struct Input` 。其中 float3 相当于 vector3 结构。

随后我们定义 `ConfigureSurface` 方法。两个参数，一个是之前定义的 Input , 还有一个是 表面配置数据 `SurfaceOutputStandard`。**第二个参数必须有一个 inout 关键字**，表示同时作为输入以及方法输出的结果。


我们创建一个材料，然后在shader那一列，使用我们创建的shader。

```shader
void ConfigureSurface (Input input, inout SurfaceOutputStandard surface) {
	surface.Smoothness = 0.5;
}
```

这样就不完全哑光了。让smooth可配置：添加一个变量，并加入下划线 `_Smoothness` 。为了让配置选项出现在编辑器中，我们必须在顶端，subshader上方添加一个 `Properties` 代码块，这将为其提供Smoothness标签，将其公开为范围为0 - 1的滑块，并将其默认值设置为0.5。

```shader
Shader "Graph/Point Surface" {
	
	Properties {
		_Smoothness ("Smoothness", Range(0,1)) = 0.5
	}


	SubShader {
		CGPROGRAM
		#pragma surface ConfigureSurface Standard fullforwardshadows
		#pragma target 3.0

		struct Input {
			float3 worldPos;
		};

		float _Smoothness;


		void ConfigureSurface (Input input, inout SurfaceOutputStandard surface) {
			surface.Smoothness = _Smoothness;
		}
		ENDCG
	}
	
	FallBack "Diffuse"
```

直接使用位置代替色彩,由于我们的位置为 -1,1 此时负数没有颜色，因此哦我们需要，同时由于z为0，所以没有蓝色，我们只能更改 rg 两种颜色。

```shader
surface.Albedo.rg = input.worldPos.xy * 0.5 + 0.5;
```

## Universal Render Pipeline

除了默认的渲染管道，Unity还有通用和高清渲染管道，简称URP和HDRP。两种渲染管道都有不同的特性和限制。当前默认的渲染管道仍然可用，但其特性集被冻结。几年后，URP可能会成为默认的。让我们让我们的图也适用于URP。**在包管理添加URP。**

简单步骤，创建URP文件夹，创建rendering->URP pipeline 在设置->Graphics->Script able Render Pipeline Setting 中 设置为我们自己的URP

如果切换回原始的pipeline可以直接修改设置内的项。

此时材质中的shader还是默认的管线，因此此时的颜色是紫红色的。我们需要创建一个独立的shader给URP。由于URP比较难，最好的方法是使用Unity的着色器图形包来直观地设计着色器。URP依赖于这个包，所以它是和URP包一起自动安装的。

创建URP 的shader文件 _Assets / Create / Shader Graph/ _URP / Lit Shader Graph_ , 随后双击进入。

![shader](https://catlikecoding.com/unity/tutorials/basics/building-a-graph/coloring-the-graph/default-lit-shader-graph.png)

创建一个 float 变量并命名为 smoothness。点击可以看到当前变量的信息。

![280](https://catlikecoding.com/unity/tutorials/basics/building-a-graph/coloring-the-graph/smoothness-property-configured.png)

其中 Reference 为内部命名。我们设置默认值喜爱与0.5，并确保 `Exposed` 选项被勾选(用来确保材质获得当前的shader变量)。将变量拖下来，并连接到需要的值上。在 toolbar上点击 sace assert。并创建一个材质命名为 `Point URP`

### URP 添加颜色

右键创建Node，并搜索 postion ，默认是世界空间。随后添加add，multiplynode。

![600](https://catlikecoding.com/unity/tutorials/basics/building-a-graph/coloring-the-graph/compacted-shader-graph.png)

从这里开始，您可以使用默认呈现管道或urp。在从一个切换到另一个之后，你还必须改变点预制的材料，否则它将是洋红色的。如果你对从图形生成的着色器代码感到好奇，你可以通过图形检查器的视图生成着色器按钮获得它。

## 动画化图形

为了使图形有动画效果，我们必须随着时间的推移调整它的点。我们可以通过删除所有点并在每次更新时创建新点来做到这一点，但这是一种低效的方法。最好继续使用相同的点，在每次更新时调整它们的位置。为了使这成为可能，我们将使用一个字段来保持点的参考。向Transform类型的图形添加一个点字段。


```c#
public class Graph : MonoBehaviour
{
    [SerializeField] private Transform pointPrefab;
    [SerializeField, Range(10,100)] private int resolution = 10;


    private Transform[] points;
    void Awake()
    {
        float step = 2f / resolution;
        var position = Vector3.zero;
        var scale = Vector3.one * step ;

        points = new Transform[resolution];
        for (int i = 0; i < points.Length; i++)
        {
            Transform point = points[i] = Instantiate(pointPrefab);
            point.SetParent(transform, false);
            position.x = (i + 0.5f) *step - 1f;
            point.localPosition = position;
            point.localScale = scale;
        }

    }


    void Update() //每一帧都进行修改
    {
        for (int i = 0; i < points.Length; i++)
        {
            Transform point = points[i];
            Vector3 position = point.localPosition;
            position.y = position.x * position.x * position.x;
            point.localPosition = position;
        }
    }
}

```

### 动画化

此时我们的点还没有变动。我们需要让他们动起来。我们需要遵循 $f(x,t) = \sin(\pi (x + t))$

```c#
void Update()
{
	float time = Time.time;
	for (int i = 0; i < points.Length; i++)
	{
		Transform point = points[i];
		Vector3 position = point.localPosition;
		position.y = Mathf.Sin(Mathf.PI * (position.x + Time.time));
		point.localPosition = position;
	}
}
```


> Mathf , Time 为 unity 内置类。

### 夹紧颜色

正弦波的振幅是1，这意味着我们的点达到的最低和最高位置是-1和1。但是，由于这些点是具有一定大小的立方体，因此它们的扩展稍微超出了这个范围。因此，我们可以得到具有负或大于1的绿色分量的颜色。虽然这是不明显的，但让我们正确并夹紧颜色以确保它们保持在0 - 1范围内。我们可以通过饱和度函数传递生成的颜色来完成表面着色。这是一个特殊的函数，它将所有的分量都固定到0 1。这是一个常见的操作在着色器知道

我们可以通过饱和度函数传递生成的颜色来完成表面着色。这是一个特殊的函数，它将所有的分量都固定到0 1。这是一个常见的操作在着色器被称为饱和(Saturate)。在URP中找到node并修改。