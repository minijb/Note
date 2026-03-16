
## Library 类

使用一个类专门用来展示函数，但是不需要知道确切的算法公式。This is an example of specialization and separation of concerns. 

我们并不需要将此类作为一个组件或者实例化，因此我们使用 `static` 关键字并不继承 Monobehavior

```c#
using UnityEngine;
using static UnityEngine.Mathf;
public static class FunctionLibrary 
{
    public static float Wave(float x, float t)
    {
        return Sin(PI * (x + t));
    }

    public static float MutiWave(float x, float t)
    {
        float y = Sin(PI * (x + 0.5f * t));
        y += 0.5f * Sin(2f * PI * (x + t)); //尽量使用乘法而不是出发
        return y * (2f / 3f); // 1.5f无法使用小数表示，因此我们利用 2f/3f 得到一个最大精度的浮点是然后乘
    }
}
```

利用 `using` 关键字+ static 可以避免重复的类型书写，如 `UnityEngine.Mathf`

### 在编辑器内选择方法

让编辑器控制Graph使用不同的数学方法，

```c#
[SerializeField, Range(0, 1)]
int function;

if (function == 0)
{
	position.y = FunctionLibrary.Wave(position.x, time);
}
else
{
	position.y = FunctionLibrary.MutiWave(position.x, time);
}
```

此时编辑器就可以在运行的时候改变数学方法了。

## 波纹方法

```c#
public static float Ripple(float x, float t)
{
	float d = Abs(x);
	float y = Sin(PI * (4f * d - t));
	return y / (1f + 10f * d);
}
```


对应公式  

$$
y =\frac{\sin(\pi(4d-t))}{1+10d}
$$

其中 $1+10d$ 使得离中心越远幅度越小。

## 管理方法

### Delegates 委托

委托是一种特殊的类型，它定义了什么类型的方法可以引用。我们的数学函数方法没有标准的委托类型，但我们可以自己定义。因为它是一种类型，我们可以在它自己的文件中创建它，但是由于它是专门为我们库的方法创建的，我们将在FunctionLibrary类中定义它，使其成为内部或嵌套类型。

若要创建Wave函数的委托类型副本，请将其重命名为function并将其代码块替换为分号。这定义了一个没有实现的方法签名。然后，通过将static关键字替换为delegate，将其转换为委托类型。

```c#
public static class FunctionLibrary 
{
	public delegate float Function(float x, float t);
	
    public static Function GetFunction(int index)
    {
        if (index == 0)
        {
            return Wave;
        }
        else if (index == 1)
        {
            return MultiWave;
        }
        else
        {
            return Ripple;
        }
    }
}
```

现在我们可以引入一个GetFunction方法，该方法使用与循环中相同的if-else逻辑返回给定索引参数的Function，只是在每个块中我们返回适当的方法，而不是调用它。

```c#
void Update()
{
	FunctionLibrary.Function f = FunctionLibrary.GetFunction(function);
	float time = Time.time;
	for (int i = 0; i < points.Length; i++)
	{
		Transform point = points[i];
		Vector3 position = point.localPosition;
		position.y = f(position.x, time);
		point.localPosition = position;
	}
}
```

此时只需要添加一个委托就可以方便的使用不同方法。

## 委托数组

```c#

public delegate float Function(float x, float t);

private static Function[] functions =
{
	Wave, MultiWave, Ripple

};

public static Function GetFunction(int index)
{
	return functions[index];
}
```


### 使用 enum 进行优化

```c#
public delegate float Function(float x, float t);
public enum FunctionName
{
	Wave,
	MultiWave,
	Ripple
};

private static Function[] functions =
{
	Wave, MultiWave, Ripple
};

public static Function GetFunction(FunctionName name)
{
	return functions[(int)name];
}
```

同时实例化的 Graph 类中就可以使用 enum 建立一个下拉菜单

```c#
[SerializeField]
FunctionLibrary.FunctionName function;
```


## 添加维度

```c#
 public delegate float Function(float x, float z, float t);
```


同时我们需要注意的是在初始化点的时候我们要加入z轴的参数


```c#
points = new Transform[resolution * resolution];
for (int i = 0, x = 0, z = 0; i < points.Length; i++, x++)
{
	if (x == resolution) {
		x = 0;
		z += 1;
	}

	Transform point = points[i] = Instantiate(pointPrefab);
	point.SetParent(transform, false);
	position.x = (x + 0.5f) * step - 1f;
	position.z = (z + 0.5f) * step - 1f;
	point.localPosition = position;
	point.localScale = scale;
}
```


## 更好的视觉效果

`_GameObject / Align With View_ with selected`  可以切换到所选相机的视角。我们将方向光的Y轴角度从 -30 调整为 30

您可以通过转到quality项目设置并选择一个预配置的级别来选择默认渲染管道的视觉质量级别。默认下拉菜单控制独立应用默认使用的级别。

我们可以通过下面的阴影部分进一步调整阴影的性能和精度，将阴影距离减少到10，并将阴影级联设置为无级联。默认设置渲染四次阴影，这对我们来说是多余的。

**URP** : 在URP assert 中进行设置 Shadows / max Distance --> 10 。同时为了匹配校准URP，我们将勾选 Soft shadows 并在 Lighting/Main Light/Shadow Resolution --> 4096


![400](https://catlikecoding.com/unity/tutorials/basics/mathematical-surfaces/adding-another-dimension/shadow-settings-urp-inspector.png)

最后，你可能会注意到在播放模式下的视觉撕裂。可以通过游戏窗口工具栏左侧的第二个下拉菜单启用垂直同步(仅限游戏视图)来防止在游戏窗口中发生这种情况。启用后，新帧的呈现与显示刷新率同步。这只在没有场景窗口同时可见的情况下可靠地工作。VSync通过质量设置的其他部分配置为独立应用程序。

## 离开网格

### 三维方法

```c#
void Awake()
{
	float step = 2f / resolution;
	var scale = Vector3.one * step ;
	points = new Transform[resolution * resolution];

	for (int i = 0; i < points.Length; i++)
	{

		Transform point = points[i] = Instantiate(pointPrefab);
		point.SetParent(transform, false);
		point.localScale = scale;
	}

}


void Update()
{
	FunctionLibrary.Function f = FunctionLibrary.GetFunction(function);
	float time = Time.time;
	float step = 2f / resolution;


	float v = 0.5f * step - 1f;
	for (int i = 0, x = 0, z = 0; i < points.Length; i++, x++)
	{
		if (x == resolution)
		{
			x = 0;
			z += 1;
			v = (z + 0.5f) * step - 1f;
		}
		float u = (x + 0.5f) * step - 1f;
		points[i].localPosition = f(u, v, time);
	}
}

// ================================================
public static Vector3 Wave(float u, float v, float t)
{
	Vector3 p;
	p.x = u;
	p.y = Sin(PI * (u + v + t));
	p.z = v;
	return p;
}
public static Vector3 MultiWave(float u, float v, float t)
{
	Vector3 p;
	p.x = u;
	p.y = Sin(PI * (u + 0.5f * t));
	p.y += 0.5f * Sin(2f * PI * (v + t));
	p.y += Sin(PI * (u + v + 0.25f * t));
	p.y *= 1f / 2.5f;
	p.z = v;
	return p;
}

public static Vector3 Ripple(float u, float v, float t)
{
	float d = Sqrt(u * u + v * v);
	Vector3 p;
	p.x = u;
	p.y = Sin(PI * (4f * d - t));
	p.y /= 1f + 10f * d;
	p.z = v;
	return p;
}
```



