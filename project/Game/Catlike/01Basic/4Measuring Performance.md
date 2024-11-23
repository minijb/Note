
## 分析unity

## Game window Statistics

右上角 status

CPU main thread took 31.7ms and the render thread took 29.2ms.

有30.003批，显然没有通过分批节省。这些是发送给GPU的绘制命令。我们的图包含10,000个点，所以看起来每个点都被渲染了三次。一次用于深度通道，一次用于单独列出的阴影施法者，一次用于渲染最终立方体，每个点。还有六个set-pass调用，这可以被认为是GPU被重新配置以不同的方式渲染，比如使用不同的材质。

如果使用URP则分析会稍微不同

虽然“批处理保存”报告没有批处理，但URP默认使用SRP批处理程序，但是统计面板不理解它。SRP批处理程序不会消除单个绘制命令，但可以使它们更有效。为了说明这一点，选择我们的URP资源，并在其检查器底部的Advanced部分禁用SRP Batcher。Make sure that _Dynamic Batching_ is disabled as well.

### Dynamic Batching

动态地将小网格组合成一个更大的网格，然后渲染。

> 开启 dynamic batching  --> Edit/preference/core rendering pipeline/visible ---> all visible
> 
> URP assert/rendering/dynamic batch


### GPU instancing

这使得使用单个绘制命令来告诉GPU绘制具有相同材质的一个网格的多个实例成为可能，提供一个变换矩阵数组和可选的其他实例数据。

## 帧调试器

灯光队员传统管线有较大影响，但是对于URP影响不大

## Profiler

Window/Analysis/Profiler

简单使用： 开启，点击需要的帧，可以选择查看的模式 -- timeline/Hierarchy

## profiling a build

It's thus much more useful to profile our app when it is running on its own.

File/Build settings --- 勾选 development build , autoconnect Profiler

点击右下角 进行build / build and run 

此时,unity的profiler窗口会自动运行并展示监测的性能。

还要记住，即使启用了“播放时清除”，探查器在附加到构建时也不会清除旧数据，因此，如果只运行应用程序几秒钟，请确保您正在查看相关帧。

## 展示帧率

## UI 面板

通过 TextMeshPro 包来创建UI面板，我们可以自己添加这个包。

> UI toolkit 也可以用来创建UI 但是需要额外的编辑器。

其中 Canves 的大小就和窗口大小一样。但是在 scene 窗口看起来会很大。 可以通过2d模式查看。我们创建的panel会自动创建在canves中,同时会自动创建 _EventSystem_ 对象--- 用来处理UI输入事件。在此项目中我们不会用到因此删除。

**canvers**

scaler component 用来管理UI的大小。默认设置假设一个恒定的像素大小。如果你使用的是高分辨率或视网膜显示器，那么你就必须增加比例因子，否则UI就会太小。你也可以尝试其他的比例模式。

[RectTransform](http://docs.unity3d.com/Documentation/ScriptReference/RectTransform.html) component，代替原本 transformer component。除了通常的位置、旋转和缩放之外，它还暴露了基于锚点的额外属性。锚控制对象相对于其父对象的相对位置和大小调整行为。

We'll put the frame rate counter panel at the top right of the window so set the panel's anchors to top right and the pivot XY to 1. Then set width to 38 and height to 70 and the position to zero. After that, set the color of the image component to black, keeping its alpha as it was.

如果这是您第一次创建TextMeshPro对象，将显示Import TMP Essentials弹出框。按照建议导入基本组件。这将创建一个TextMesh Pro资产文件夹，其中包含一些资产，我们不需要直接处理。

```c#
[SerializeField] private TextMeshProUGUI display;
```

简单来说就是对于自己的引用。

**Time.deltaTime**的问题：该值受时间刻度的限制，该时间刻度可用于慢动作、快进或完全停止时间。因此我们可以使用 `Time.unscaledDeltaTime` 进行替代。

`display.SetText` 的使用 --- 1) 直接输入字符串 2) 接收额外 float 变量替换 `{num1:num2}` 其中 num1 表示第n个float参数， num2为小数点后的位数

请注意，即使启用了VSync，最佳帧速率也可能超过显示器刷新率。同样，最差的帧速率不一定是显示器刷新率的倍数。这是可能的，因为我们没有测量显示帧之间的持续时间。我们正在测量Unity帧之间的持续时间，这是其更新循环的迭代。Unity的更新循环与显示器并不完全同步。当探查器显示下一帧的播放器循环在当前帧的渲染线程仍然繁忙时开始时，我们已经看到了这一点。渲染线程完成后，GPU仍有一些工作要做，在此之后，显示器刷新仍需要一些时间。因此，我们显示的FPS并不是真正的帧速率，而是Unity告诉我们的。理想情况下，这些都是一样的，但要做到这一点很复杂。有一篇关于Unity在这方面如何改进的博客文章，但这甚至不能说明整个故事。 可以看 [blogs](https://blogs.unity3d.com/2020/10/01/fixing-time-deltatime-in-unity-2020-2-for-smoother-gameplay-what-did-it-take/)


## Frame Durations

```c#
display.SetText(
	"MS\n{0:0}\n{1:0}\n{2:0}",
	1000f * bestDuration,
	1000f * duration / frames,
	1000f * worstDuration
);
```

## 遍历函数

由于手动切换会造成大幅波动，因此我们可以写一个函数遍历所有的方法或者通过用户输入决定方法

从现在开始，我们需要跟踪当前功能激活了多长时间，并在需要时切换到下一个功能。这将使我们的Update方法复杂化。它的当前代码只处理更新当前函数，因此让我们将其移动到一个单独的UpdateFunction方法中，并让Update调用它。这使我们的代码有条理。


```c#
[SerializeField]
FunctionLibrary.FunctionName function; //切换时间
```

##  Interpolating Functions  插值函数

更加平滑的切换不同的函数

额外需要切换的两个函数，progress 控制 morph 的速度

```c#
public static Vector3 Morph(
	float u, float v, float t, Function from, Function to, float progress
)
{
	return Vector3.LerpUnclamped(from(u, v, t), to(u, v, t), SmoothStep(0f, 1f, progress));
}
```

Lerp是线性插值的简写。它会在函数之间产生一个直接的等速过渡。我们可以在开始和结束的地方放慢进度，让它看起来更流畅一些。这是通过用Mathf调用替换原始进度来实现的


这是通过 调用 [Mathf](http://docs.unity3d.com/Documentation/ScriptReference/Mathf.html).Smoothstep来实现的。平滑步以0、1和进度作为参数。

使用LerpUnclamped使得不限制在0-1范围内。

