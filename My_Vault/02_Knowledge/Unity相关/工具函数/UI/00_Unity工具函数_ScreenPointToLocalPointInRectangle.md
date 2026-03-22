---
title: Unity工具函数 ScreenPointToLocalPointInRectangle
date: 2026-03-16
tags:
  - knowledge
  - unity
type: ui
aliases:
  -
description: `public static bool ScreenPointToLocalPointInRectangle (RectTransform rect, Vector2 screenPoint, Cam...
draft: false
---

# Unity工具函数 ScreenPointToLocalPointInRectangle

`public static bool ScreenPointToLocalPointInRectangle (RectTransform rect, Vector2 screenPoint, Camera cam, out Vector2 localPoint);`

屏幕中的一个点 --- ScreenPoint
相对于 rect 的位置
对于设置为 Screen Space - Overlay 模式的 Canvas 中的 RectTransform，cam 参数应为 null。


常用于检测点击是否在 UI 上。


![[ScreenPointToLocalPointInRectangle.excalidraw]]

计算两个UI 的相对位置

```c#
public Vector2 CalculateUIRelativePos(RectTransform targetRect, RectTransform arrowRect)
{
	// 坐标转换
	Vector2 pos = RectTransformUtility.WorldToScreenPoint(camera, targetRect.position);
	RectTransformUtility.ScreenPointToLocalPointInRectangle(arrowRect, pos, camera, out Vector2 localPoint);
	return localPoint;
}
```