## new project

创建页面后，我们来到默认的layout，我们可以自定义我们的layout。

### Package

unity的功能是模块化的，除了核心模块外，我们可以下载并添加额外的包。

```ad-tip
title:  位置
位置： windows -> package manager
```


### 色彩空间

将unity默认的色彩空间从gamma变为linear

### 样本场景

切换资源窗口的显示方式 : 单双列

基础样本场景包含两个组件：main camera + directional light , 位置 : hierarchy window

**不显示实体** : 点击实体左侧的眼睛图标

## 建立一个简单的钟表

创建一个空的对象。手动控制工具的快捷键 `q,w,e,r,t` 

### 创建钟表的表面

添加 _Cylinder_ 圆柱体。

组件介绍

- `mesh filter` 其中包含对内置圆柱网格的引用。
- `Mesh Render` 确保对象被渲染，同时还决定对象使用的材质。

![250](https://s2.loli.net/2024/02/13/5Bs1Ec4mVqMWGdJ.png)

- `Capsule Collider` 用于3D物理系统，代表一个圆柱含有一个胶囊刚体(unity没有默认的圆柱刚体)。如果我们希望为钟表建立刚体的话，可以选择 `mesh Collider` ，使用右上角三点删除刚体

我们将圆柱体改名为 face ，此时层级结构如下。

![ZhfEy9S5PLzNCHx.png](https://s2.loli.net/2024/02/13/ZhfEy9S5PLzNCHx.png)

此时 face 时 clock 的子对象，子对象服从于它们的父对象的转换。这意味着当Clock改变位置时，Face也会改变。就好像他们是一个单一的实体。旋转和缩放也是如此。此时对于一个复杂对象可以整体的移动物体。

### 创建钟的外围

建立钟表指示器，创建立方体。同时改变外围指示的材质。

建立 cube 实体。创建了一个 **材质** ， 修改 _Albedo_ <font color="#548dd4">反射率</font>以修改材质的颜色。随后再 `mesh Render` 组件中的 _Materials_ 选项，以修改指示物的颜色。根据角度进行旋转和位移

## 创建钟的指针

同理创建一个方形对象，由于指针不是中心对称的，但它的旋转按照中心自身旋转，和实际情况不符。因此我们创建一个空的pivot对象包裹它，这个对象的中心位置再 `0.0.0` 此时旋转 pivot 子对象会环绕 pivot 的中心进行旋转。

## 添加动画

### 控制指针

现在我们定义了一个字段表示 指针的 transformer 属性 

```c#
Transform hoursPivot;
```

由于这个变量默认时 private 的，但是class并不知道 unity 场景，变量不能直接绑定实际的物体对象。我们可以将变量描述为 serializable 可序列化。这意味着当Unity保存场景时，它应该包含在场景数据中，这是通过将所有数据按顺序序列化并将其写入文件来实现的。

```c#
 [SerializeField]
    Transform hoursPivot;
```

> 我们可以将变量设置为 public ，但是只有其他变量需要访问该字段的时候才推荐使用public，这样更加方便维护。

![TFxpWRg93UKeHw8.png](https://s2.loli.net/2024/02/14/TFxpWRg93UKeHw8.png)


此时我们就可以在 unity 编辑器中进行绑定。使用同样方法配置剩下两个指针。

我们添加一个 `Awake` 的函数，Unity将在组件被唤醒时调用该方法。

我们首先初始化角度，将欧拉角转变为三元数。

```c#
void Awake()
{
	hoursPivot.localRotation = Quaternion.Euler(0, 0, -30);
}

```

> localRotation属性表示Transform组件单独描述的旋转，因此它是相对于其父组件的旋转。这是你在它的检查器中看到的旋转。相反，`rotation`属性表示世界空间中的最终旋转，考虑到整个对象层次结构。如果我们将时钟作为一个整体旋转，设置该属性会产生奇怪的结果，因为当属性补偿时钟的旋转时，手臂会忽略这一点。

### 获得当前时间

`Datatime.Now` 得到系统时间, 随后我们分配指针的角度。注意可以使用var代替声明.

```c#
DateTime time = DateTime.Now;
_hoursPivot.localRotation = Quaternion.Euler(0, 0, HoursToDegrees * time.Hour);
_minutePivot.localRotation = Quaternion.Euler(0, 0, minutesToDegrees * time.Minute);
_secondPivot.localRotation = Quaternion.Euler(0, 0, secondsToDegrees * time.Second);
```

此时我们将使用 Update 函数，在每一帧变更指针的角度。

```c#
void Update()
{
	var time = DateTime.Now;
	_hoursPivot.localRotation =
		Quaternion.Euler(0f, 0f, HoursToDegrees * time.Hour);
	_minutePivot.localRotation =
		Quaternion.Euler(0f, 0f, minutesToDegrees * time.Minute);
	_secondPivot.localRotation =
		Quaternion.Euler(0f, 0f, secondsToDegrees * time.Second);
}
```

### 连续旋转

现在转动动画时跳跃的。我们需要将每次转动变得更加连贯。由于DateTime不提供小数数据，但是提供了一个 `timeSpan` 的值包含我们需要的格式的数据。需要注意的是的类型为 double ，我们需要将他转换为 float。

```c#
void Update()
{
	TimeSpan time = DateTime.Now.TimeOfDay;
	hoursPivot.localRotation =
		Quaternion.Euler(0f, 0f, HoursToDegrees * (float)time.TotalHours);
	minutePivot.localRotation =
		Quaternion.Euler(0f, 0f, minutesToDegrees * (float)time.TotalMinutes);
	secondPivot.localRotation =
		Quaternion.Euler(0f, 0f, secondsToDegrees * (float)time.TotalSeconds);
    }
```

