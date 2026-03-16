
- [t1](https://www.youtube.com/watch?v=9RHGLZLUuwc&t=184s)
- [t2](https://www.youtube.com/watch?v=nF4X9BIUzx0&t=159s)

## Work on GPU

一个点需要16个 float ，呢么 40000个点据需要 2.44MiB 同时 URP会复制给GPU两次，一次是阴影一次是常规的集合形状。

因为我们只需要点的位置来显示它们，所以如果数据只存在于GPU端将是理想的。这将减少大量的数据传输。但是CPU不能再计算位置，GPU必须代替它。幸运的是，它非常适合这项任务。

在GPU上进行存储 --- `ComputeBuffer`

```c#
ComputeBuffer positionsBuffer;

void OnEnable()
{
	// amount of gameobj , 3 * float（4 字节）
	positionsBuffer = new ComputeBuffer(resolution * resolution, 3 * 4);
}
```

计算缓冲区包含任意的未类型化数据。我们必须通过第二个参数以字节为单位指定每个元素的确切大小。我们需要存储3D位置向量，它由三个浮点数组成，所以元素大小是3乘以4字节。因此，40,000个位置将需要0.48MB或大约0.46 mb的GPU内存。

这让我们获得了一个计算缓冲区，但这些对象不能在热重载中存活，这意味着如果我们在播放模式下更改代码，它将消失。因此我们使用 `OnEnable` 方法 而不是 Awake。这发生在它被唤醒之后，除非它被禁用，也发生在热重新加载完成之后。同时我们需要在 Obj disable 或者 销毁的时候抛弃 buffer 因此我们在 `OnDisable` 方法中销毁 buffer

```c#
void OnDisable()
1. {
	1. positionsBuffer.Release();
	positionsBuffer = null;
}
```


> Awake --> 游戏启动之前用于初始化任何变量和游戏状态,Awake函数是在所有objects实例化之后被调用的，因而可以安全地同其它objects通信或查询等.
> **Enable** --> 只有object是激活状态下才可被调用，在object可用之后被调用，这通常发生于MonoBehaviour实例被创建时，不能做协程
> **Start** --> 如果脚本实例是enabled的，则Start函数在第一帧更新之前被调用，在脚本实例生命周期中仅被调用一次。不论脚本enabled与否，Awake函数都会调用；假如初始化期间脚本disabled，则Start函数就不会与Awake函数在同一帧中被调用
> 
## Compute Shader

创建 Shader/Computer Shader

need main function, indicated via `#pragma kernal xxxx`

当GPU被要求计算shader function，他会将国祚分为不同的组，并然后安排它们独立并行地运行。每一组包含一堆线程用来执行相同的输入不同的操作。我们需要 **指定每组多少个线程**

```c#
// each group run only one single thread
[numthreads(1, 1, 1)]
void FunctionKernel (uint3 id: SV_DispatchThreadID) {}
```

<span style="background:#fff88f">GPU 在一个计算单元中 平行运行固定数量的 线程 -- warps 线程束</span>

如果一组 group 的线程小于 the size of warps ， 会造成部分线程空间，浪费时间。
如果超过，则GPU会用更多的warp。 默认64个线程是一个好的选择，因为他匹配amd GPU的warps内的线程数，对于NVidia来说是 32。

numtheads 从三个维度提供这些线程， `(64,1,1)` 提供了64个一维的线程， `(8,8,1)` 提供了相同数量但是二维的线程，由于每一个线程由三个无符号整数组成的向量标识，因此我们加入一个 `uint3 id` ,我们必须明确指出这个参数是用于线程标识符的。我们在参数名后面写一个冒号，后面跟着 `SV_DispatchThreadID` shader 语义关键字。

## UV 坐标系

如果我们知道图的步长，我们可以将线程标识符转换为UV坐标。为它添加一个名为Step的计算机着色器属性，就像我们在表面着色器中添加Smoothness一样。

```c#
float _Step;

[numthreads(8, 8, 1)]
void FunctionKernel (uint3 id: SV_DispatchThreadID) {}
```

随后我们创建以恶搞 `GetUV` 方法将线程标识符作为以恶搞参数并返回UV坐标系的值（float2）,在遍历这些点时，我们可以使用在Graph中应用的相同逻辑。取标识符的XY分量，加上0.5，乘以步长，然后减去1。

```c#
float _Step;

float2 GetUV (uint3 id) {
	return (id.xy + 0.5) * _Step - 1.0;
```

> UV坐标 ： 
> [uv1](https://www.bilibili.com/video/BV1GE411y7Af/?spm_id_from=333.337.search-card.all.click&vd_source=8beb74be6b19124f110600d2ce0f3957)
## 设置位置

为了存储一个位置，我们需要访问位置缓冲区。在HLSL中，一个计算buffer会被认为是 `structured buffer`。因为我们需要可读写版本的 -- `RWStructuredBuffer` 。同时我们需要指定数据的类型，即 `float3` .

```hlsl
RWStructuredBuffer<float3> _Positions;
uint _Resolution;
```

为了存储一个点的位置，我们需要分配一个基于 线程标识的 index。我们需要知道这个图形的分辨率。因此我们添加 uint 类型的 `_Resolution` .

然后创建一个SetPosition函数来设置一个位置，给出一个标识符和要设置的位置。对于索引，我们将使用标识符的X分量加上它的Y分量乘以图形分辨率.通过这种方式，我们将二维数据按顺序存储在一维数组中。

```c#
void SetPosition (uint3 id, float3 position) {
	if (id.x < _Resolution && id.y < _Resolution) {
		_Positions[id.x + id.y * _Resolution] = position;
	}
```

我们必须知道的一件事是，我们每组计算一个`8*8`个点的网格。如果图的分辨率不是8的倍数，那么我们最终会得到一行一列的组，这些组将计算出一些越界点。这些点的索引要么落在缓冲区之外，要么与有效的索引冲突，这将破坏我们的数据。

## wave 方法

添加 `_time` 属性使动画更生动。

```hlsl
float _Step, _Time;

[numthreads(8, 8, 1)]
void FunctionKernel (uint3 id: SV_DispatchThreadID) {
	float2 uv = GetUV(id);
	SetPosition(id, Wave(uv.x, uv.y, _Time));
}
```

随后复制wave方法并改变一下语法

```hlsl
#define PI 3.14159265358979323846

float3 Wave(float u, float v, float t)
{
    float3 p;
    p.x = u;
    p.y = sin(PI * (u + v + t));
    p.z = v;
    return p;
}
```

## dispatch a computer shader kernal

在 GPUGraph.cs 中实例化一个 ComputerShader 

```c#
[SerializeField]
ComputeShader computeShader;
```


我们需要设置计算着色器的一些属性。为此，我们需要知道Unity为它们使用的标识符。这些identify 按需声明，同时在引用程序运行期间不变，因此使用static，同时防止写入加入 `readonly`

```c#
	static readonly int
		positionsId = Shader.PropertyToID("_Positions"),
		resolutionId = Shader.PropertyToID("_Resolution"),
		stepId = Shader.PropertyToID("_Step"),
		timeId = Shader.PropertyToID("_Time");
```

> readonly对引用类型并不适用，因为它只强制不改变字段值本身。在这种情况下，对象数组本身仍然可以被修改。因此，它可以防止分配一个完全不同的数组，但不会阻止更改其元素。我更喜欢只对int这样的基本类型使用只读。

接下来，创建一个UpdateFunctionOnGPU方法来计算步长，并设置计算着色器的分辨率、步长和时间属性。这是通过对分辨率调用settint和对其他两个属性调用SetFloat来实现的，并将标识符和值作为参数。

我们需要设置 postions buffer， 这里不需要复制，只需要link。

```c#
void UpdateFunctionOnGPU()
{
	float step = 2f / resolution;
	computeShader.SetInt(resolutionId, resolution);
	computeShader.SetFloat(stepId, step);
	computeShader.SetFloat(timeId, Time.time);

	computeShader.SetBuffer(0, positionsId, positionsBuffer);
	int groups = Mathf.CeilToInt(resolution / 8f);
	computeShader.Dispatch(0, groups, groups, 1);
}

```

setBuffer的额外参数

- 第一个参数为 index of kernal funcion --- kernal function的可以有多个，buffer需要连接到具体的方法下。可以通过额外的方法找到方法ID `FindKernel`

最后我们使用 `dispatch` 方法 ， 参数:

- kernal index
- 运行的数量 -- 我们需要按照维度进行区分 ，如果全为1则只有第一组group会计算

因为我们使用 $8 \times 8$ 的组进行计算，那么我们就需要 $resolution / 8$ 

```c#
int groups = Mathf.CeilToInt(resolution / 8f);
computeShader.Dispatch(0, groups, groups, 1);
```

最后我们在 `Update` 函数中调用

## 进行绘制

因为 position 已经在 GPU 上了我们不需要cpu进行跟踪，相反，我们将指示GPU多次绘制具有特定材料的特定网格，通过单个命令。我们需要添加[Material](http://docs.unity3d.com/Documentation/ScriptReference/Material.html) and [Mesh](http://docs.unity3d.com/Documentation/ScriptReference/Mesh.html)。

```c#
	[SerializeField]
	Material material;

	[SerializeField]
	Mesh mesh;
```

使用 `Graphics.DrawMeshInstancedProcedural` 方法进行绘制。参数为 mesh，sub-mush, material.子网格索引适用于由多个部分组成的网格

> DrawMeshInstancedIndirect方法是有用的，当你不知道有多少实例绘制在CPU端，而不是通过缓冲区提供计算着色器的信息。

这种方法不适用 gameobj , unity 不知道场景中绘制的存在。我们必须通过提供一个边界框作为附加参数来表示这一点。这是一个与坐标轴对齐的方框，它表示我们要画的东西的空间边界。Unity使用它来决定是否可以跳过绘图，因为它最终在相机的视野之外。这就是所谓的截锥体剔除。不再是计算每个点的边界而是一次计算整个图的边界。这对我们的图来说很好，因为我们可以从整体上看它。

我们的图形位于原点，这些点应该保持在大小为2的立方体内。我们可以通过调用Vector3的bounds构造函数方法来为它创建一个边界值。0和Vector3。一个乘以两个作为参数。由于cube也存在大小因此我们需要加入分辨率

```c#
var bounds = new Bounds(Vector3.zero, Vector3.one * (2f + 2f / resolution));
Graphics.DrawMeshInstancedProcedural(mesh, 0, material, bounds，positionsBuffer.count);
```

我们必须提供给DrawMeshInstancedProcedural的最后一个参数是应该绘制多少实例。这应该与位置缓冲区中的元素数量相匹配，我们可以通过它的count属性来检索。

## 检索位置

我们首先建立一个shader，随后使用将 `#pragma target 4.5` 以支持计算shader

过程渲染类似于GPU实例化，但是需要额外的选项如 `instancing_options`, 这里我们需要 `procedural:ConfigureProcedural`

这表明表面着色器需要为每个顶点调用ConfigureProcedural函数。它是一个没有任何参数的空函数。将它添加到我们的着色器中。

默认情况下，这个函数只会在常规的抽取过程中被调用。为了在渲染阴影时也应用它，我们必须指出我们需要一个自定义阴影通道，通过在#pragma surface指令中添加addshadow。

```glsl
#pragma surface ConfigureSurface Standard fullforwardshadows addshadow
```

之后我们只需要添加同样的position_buffer就可以了.这里我们需要进行读取因此，类型为 
`StructuredBuffer `

```c#
#if defined(UNITY_PROCEDURAL_INSTANCING_ENABLED)
	StructuredBuffer<float3> _Positions;
#endif
```

但是，我们应该仅针对专门编制的用于程序图的着色器变体来执行此操作。当定义了Unity_procedural_instancing_enabled宏标签时，就是这种情况。我们可以通过编写 ` #if defined(UNITY_PROCEDURAL_INSTANCING_ENABLED)` 它的工作原理类似于c#中的条件块，除了在编译过程中包含或省略代码。最终代码中不存在分支。

We have to do the same for the code that we'll put inside the `ConfigureProcedural` function.

```c#
void ConfigureProcedural () {
	#if defined(UNITY_PROCEDURAL_INSTANCING_ENABLED)
		float3 position = _Positions[unity_InstanceID];
	#endif
}
```

现在我们可以通过使用当前正在绘制的实例的标识符索引位置缓冲区来检索该点的位置。我们可以通过unity InstanceID访问它的标识符，这是全局可访问的。

### 定义变换矩阵

一旦我们有了一个位置，下一步就是为这个点创建一个对象到世界的转换矩阵。为了使事情尽可能简单，我们将图形固定在世界原点，没有任何旋转和缩放。调整GPU图形游戏对象的Transform组件不会产生任何效果，因为我们不会使用它。我们使用一个变换矩阵

![a](https://catlikecoding.com/unity/tutorials/basics/compute-shaders/procedural-drawing/transformation-matrix.png)


变换矩阵用于将顶点从对象空间转换为世界空间。它通过unity ObjectToWorld全局提供。因为我们是按程序来画的这是一个单位矩阵，所以我们要替换它。最初将整个矩阵设为零。

我们可以通过float4(position, 1.0)为位置偏移构造一个列向量。We can set it as the fourth column by assigning it to `unity_ObjectToWorld._m03_m13_m23_m33`.

随后我们将对角线设置为 `_step`


```c#
unity_ObjectToWorld = 0.0;
unity_ObjectToWorld._m03_m13_m23_m33 = float4(position, 1.0);
unity_ObjectToWorld._m00_m11_m22 = _Step;
```

还有一个unity_worldtoObject矩阵，其中包含反向转换，用于转换正常向量。当应用不均匀变形时，需要正确地转换方向向量。但是由于这不适用于我们的图形，我们可以忽略它。不过，我们应该通过在Pragma的Intancing选项中添加假设尺度来告诉我们的着色器。

使用shader创建一个材质，并在运行的过程中绑定 position 和 step

```c#
material.SetBuffer(positionsId, positionsBuffer);
material.SetFloat(stepId, step);
```

### go to million

我们可以通过项目设置关闭异步着色器编译，但这只是我们的点表面GPU着色器的问题。幸运的是，我们可以通过添加 `#pragma editor_sync_compilation` 来告诉Unity对特定的着色器使用同步编译。这将迫使Unity在第一次使用着色器之前停止并立即编译着色器，从而避免虚拟着色器。

告诉Unity对特定的着色器使用同步编译，并增加实体的数量

## 使用 URP

我们可以将

```hlsl
#if defined(UNITY_PROCEDURAL_INSTANCING_ENABLED)
	StructuredBuffer<float3> _Positions;
#endif

float _Step;

void ConfigureProcedural () {
	#if defined(UNITY_PROCEDURAL_INSTANCING_ENABLED)
		float3 position = _Positions[unity_InstanceID];

		unity_ObjectToWorld = 0.0;
		unity_ObjectToWorld._m03_m13_m23_m33 = float4(position, 1.0);
		unity_ObjectToWorld._m00_m11_m22 = _Step;
	#endif
}
```

提取出来 作为一个 `.hlsl`  文件 并在 `Point surface GPU` 中 include

```c#
#include "PointGPU.hlsl"

struct Input {
	float3 worldPos;
};

float _Smoothness;

//#if defined(UNITY_PROCEDURAL_INSTANCING_ENABLED)
//	StructuredBuffer<float3> _Positions;
//#endif

//float _Step;

//void ConfigureProcedural () { … }

void ConfigureSurface (Input input, inout SurfaceOutputStandard surface) { … }
```

我们将使用 Custom Function node 并 include 一个 hlsl 文件。简单来说就是 node 从文件中引入一个方法。Although we don't need this functionality, the code won't be included unless we connect it to our graph。我们只需要引入一个格式正确的假函数就可以了

```hlsl
void ShaderGraphFunction_float (float3 In,out  float3 Out) {
	Out = In;
}

void ShaderGraphFunction_half (half3 In, out half3 Out) {
	Out = In;
}
```

注意这里的 `_float` 后缀是需要的因为他表示函数的精度。shader提供两种精度模式 `float/half` half 就是常规精度的一半。节点使用的精度可以显式选择或设置为继承，这是默认值。为了确保我们的图适用于两种精度模式，还添加了一个使用半精度的变体函数。

随后我们在 URP 中添加 custom function node 并在右边的菜单中绑定对应的name以及文件，添加一个输入输出，随后连接到 position 中。

*******

为了启用procedural rendering，我们需要 include `pragma instancing_options and #pragma editor_sync_compilation `

这需要直接注入到 生成的 shader 源文件中，同时不能被 include 在单个文件中，因此我们需要添加一个 custom function node ，和之前 type 代码一样，但是 type 为 string，此时Body的作用是方法的代码块，因此我们同样需要添加 inputs 和 outputs

## 改变分辨率

因为我们目前总是为缓冲区中的每个位置绘制一个点，降低了分辨率，而在播放模式下会固定一些点。这是因为计算着色器只更新适合图形的点。

不能调整计算缓冲区的大小。我们可以在每次分辨率改变时创建一个新的，但另一种更简单的方法是始终为最大分辨率分配一个缓冲区。这将使在游戏模式下改变分辨率变得毫不费力。

## 在 compute shader 中切换函数

使用宏 定义多个方法，让后通过index检索这些方法

```hlsl
#pragma kernel WaveKernel
#pragma kernel MultiWaveKernel
#pragma kernel RippleKernel
#pragma kernel SphereKernel
#pragma kernel TorusKernel

#define KERNEL_FUNCTION(function)\
[numthreads(8, 8, 1)]\
void function##Kernel (uint3 id: SV_DispatchThreadID) {\
	float2 uv = GetUV(id);\
	SetPosition(id, function(uv.x, uv.y, _Time));\
}


KERNEL_FUNCTION(Wave)
KERNEL_FUNCTION(MultiWave)
KERNEL_FUNCTION(Ripple)
KERNEL_FUNCTION(Sphere)
KERNEL_FUNCTION(Torus)
```

```c#
var kernelIndex = (int)function;//!!!!!!!!!!!!!!
computeShader.SetBuffer(kernelIndex, positionsId, positionsBuffer);
```

> 使用 get set方法动态的控制 functionCount 而不是写死到**GPUGraph**中，可以有效提高抽象程度。

