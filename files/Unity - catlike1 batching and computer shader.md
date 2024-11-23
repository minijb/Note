---
tags:
  - unity
  - catlike
  - computer_shader
  - unity-batch
---
## unity Batching

1. Preference - core rendering Pipline - visibility - All Visible
2. URP - 右上角 - show addional Properties

3. 动态 batching ： URP 资产
4. URP : 同 上
5. GPU Instance : 在材质


## Computer Shader

### 外部脚本

1. 创建一个 计算 buffer

```c#
// GPU Computer Buffer
ComputeBuffer positionBuffer;

void OnEnable()
{
	// 无法热更新 --- 每次想用新的需要 new
	positionBuffer = new ComputeBuffer(resolution * resolution, 3*4); //  参数1 : obj 数量 ， 参数2 ： 每个 obj 的大小 -- float : 四字节
}

void OnDisable()
{
	positionBuffer.Release();
	positionBuffer = null; // 方便GC回收
}
```


2. 实例化 computer shader， 并指定索引

```c#
[SerializeField]
ComputeShader computeShader;

static readonly int
	positionsId = Shader.PropertyToID("_Positions"),
	resolutionId = Shader.PropertyToID("_Resolution"),
	stepId = Shader.PropertyToID("_Step"),
	timeId = Shader.PropertyToID("_Time");

```

3. Update 更新逻辑

```c#
// 设置值，并根据值得到position

void UpdateFunctionOnGPU () {
	float step = 2f / resolution;
	computeShader.SetInt(resolutionId, resolution);
	computeShader.SetFloat(stepId, step);
	computeShader.SetFloat(timeId, Time.time);

	// 注意 : 这里 不是进行 copy， 仅仅是 link buffer to kernal. 第一个参数是 kernal index 可以通过 findKernal 找到
	computeShader.SetBuffer(0, positionsId, positionsBuffer);


	// 分配 GPU 资源 这里 每块GPU : 8 * 8 , 需要多少块这种GPU块
	int groups = Mathf.CeilToInt(resolution / 8f);
	computeShader.Dispatch(0, groups, groups, 1);
}
```

4. 程序化生成cube

```c#
[SerializeField]
Material material;

[SerializeField]
Mesh mesh;

UpdateFunctionOnGPU();
var bounds = new Bounds(Vector3.zero, Vector3.one * (2f + 2f / resolution));
Graphics.DrawMeshInstancedProcedural(
	mesh, 0, material, bounds, positionsBuffer.count
);

```


Graphics.DrawMeshInstancedProcedural 参数：

1. mesh， sub_mesh index (用于一个mesh 含有多哥 组成部分), material, bounds 范围， 需要绘制的个数 count 
 
因为这种绘图方式不使用游戏对象 Unity 不知道在场景中哪里发生了绘图。我们必须通过提供一个边界框作为额外的参数来表明这一点。这是一个轴对齐的盒子，表示我们画的东西的空间边界。Unity 使用这个来确定是否可以跳过绘图，因为它最终会出现在摄像机的视野之外。这就是所谓的果实剔除。所以现在不是计算每个点的边界，而是同时计算整个图。这对于我们的图表来说是很好的，因为我们的想法是从整体上观察它。
### computer shader 本体

```hlsl
```