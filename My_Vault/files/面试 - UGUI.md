---
tags:
  - 面试
---
尽管网格不同但是， 材质纹理字体相同的网格可以进行合并。


**当一个UI需要生成顶点数据的时候**

```c#
/// <summary>
/// Callback function when a UI element needs to generate vertices. Fills the vertex buffer data.
/// </summary>
/// <param name="vh">VertexHelper utility.</param>
/// <remarks>
/// Used by Text, UI.Image, and RawImage for example to generate vertices specific to their use case.
/// </remarks>
protected virtual void OnPopulateMesh(VertexHelper vh)
{
	var r = GetPixelAdjustedRect(); // 返回默认顶点数据
	var v = new Vector4(r.x, r.y, r.x + r.width, r.y + r.height);

	Color32 color32 = color;
	vh.Clear();
	vh.AddVert(new Vector3(v.x, v.y), color32, new Vector2(0f, 0f));
	vh.AddVert(new Vector3(v.x, v.w), color32, new Vector2(0f, 1f));
	vh.AddVert(new Vector3(v.z, v.w), color32, new Vector2(1f, 1f));
	vh.AddVert(new Vector3(v.z, v.y), color32, new Vector2(1f, 0f));

	vh.AddTriangle(0, 1, 2);
	vh.AddTriangle(2, 3, 0);
}


private void DoMeshGeneration()
{
	if (rectTransform != null && rectTransform.rect.width >= 0 && rectTransform.rect.height >= 0)
		OnPopulateMesh(s_VertexHelper); /// 默认顶点数据
	else
		s_VertexHelper.Clear(); // clear the vertex helper so invalid graphics dont draw.

	var components = ListPool<Component>.Get(); // 调用 所有组件中修改网格的部分！！！！
	GetComponents(typeof(IMeshModifier), components);

// 修改网格
	for (var i = 0; i < components.Count; i++)
		((IMeshModifier)components[i]).ModifyMesh(s_VertexHelper);

	ListPool<Component>.Release(components);

// 将数据填充到网格并穿个 CanvasRender
	s_VertexHelper.FillMesh(workerMesh);
	canvasRenderer.SetMesh(workerMesh); // 剔除透明度为0的像素
}

```

**Rebuild**

```c#
/// <summary>
/// Rebuilds the graphic geometry and its material on the PreRender cycle.
/// </summary>
/// <param name="update">The current step of the rendering CanvasUpdate cycle.</param>
/// <remarks>
/// See CanvasUpdateRegistry for more details on the canvas update cycle.
/// </remarks>
public virtual void Rebuild(CanvasUpdate update)
{
	if (canvasRenderer == null || canvasRenderer.cull)
		return;

	switch (update)
	{
		case CanvasUpdate.PreRender:
			if (m_VertsDirty) // 顶点数据变量 
			{
				UpdateGeometry(); // 生成网格 DoMeshGeneration
				m_VertsDirty = false;
			}
			if (m_MaterialDirty) // 材质变了
			{
				UpdateMaterial();
				m_MaterialDirty = false;
			}
			break;
	}
}
```


**CanvasUpdateRegistry**

```c#

/// <summary>
/// A place where CanvasElements can register themselves for rebuilding.
/// </summary>
public class CanvasUpdateRegistry
{
	private static CanvasUpdateRegistry s_Instance;

	private bool m_PerformingLayoutUpdate;
	private bool m_PerformingGraphicUpdate;

	// This list matches the CanvasUpdate enum above. Keep in sync
	private string[] m_CanvasUpdateProfilerStrings = new string[] { "CanvasUpdate.Prelayout", "CanvasUpdate.Layout", "CanvasUpdate.PostLayout", "CanvasUpdate.PreRender", "CanvasUpdate.LatePreRender" };
	private const string m_CullingUpdateProfilerString = "ClipperRegistry.Cull";

	private readonly IndexedSet<ICanvasElement> m_LayoutRebuildQueue = new IndexedSet<ICanvasElement>();
	private readonly IndexedSet<ICanvasElement> m_GraphicRebuildQueue = new IndexedSet<ICanvasElement>();

	protected CanvasUpdateRegistry()
	{
	Canvas.willRenderCanvases += PerformUpdate; // 执行 rebuild 方法
	}


// PerformUpdate 简单的流程 ： 1. 执行 rebuild ， 2. 清空队列

```


`Graphic` 继承 了 ICanvasElement ， 同时 ICanvasElement 需要实现 rebuild 类

注意 ： 只有发生变动的时候，才会将UI注册到两个队列，同时使用 PerformUpdate进行更新， 同时清空队列

因此我们需要关心 有哪些变化会被注册 `CanvasUpdateRegistry`

比如 ： Disable 的时候一定不会进入队列

```c#
protected override void OnDisable()
{
#if UNITY_EDITOR
	GraphicRebuildTracker.UnTrackGraphic(this);
#endif
	GraphicRegistry.DisableGraphicForCanvas(canvas, this);
	CanvasUpdateRegistry.DisableCanvasElementForRebuild(this); //！！！！！！！！！！！！！！！！！！！

	if (canvasRenderer != null)
		canvasRenderer.Clear();

	LayoutRebuilder.MarkLayoutForRebuild(rectTransform);

	base.OnDisable();
}
```

主要的注册场景 ： 

1. 更新顶点数据和材质参数
2. 层级关系变化
3. UI大小
4. CanvasRender 的 Cull 模式发生变化

## OverDraw

多次重回同一个像素造成的GPU开销， 主要元凶为半透明物体 --- 粒子+UI

1. 对于 AlPha 为0 的UI ，将Canvas Render 上的 CulTransparent Mesh 勾上， 保证 UI 时间相应同时不进行渲染
2. 减少Mash ，多使用rectMask2D


