---
title: ch unity Editor中button变色
date: 2026-03-16
tags:
  - resource
  - unity
type: editor
aliases:
  -
description: 1. 使用GUI.BackGround
draft: false
---

# ch unity Editor中button变色

1. 使用GUI.BackGround 

相当于状态机

```c#
Color bc = GUI.backgroundColor;
GUI.backgroundColor = Color.green;
GUIStyle btnStyle = new GUIStyle(GUI.skin.button)
{
	fixedWidth = thumbnailSize,
};
if (GUILayout.Button("刷新", btnStyle))
{
	ReflashImageInfos(this);
}
GUI.backgroundColor = bc;

```

2. 整体覆盖一个透明颜色

```c#
// 会这button

if (GUILayout.Button(content, btnStyle))
{
	selectedImageInfo = imageInfo;
}

if (selectedImageInfo_style == imageInfo)
{
	//获取上一次回执的 rect 
	Rect rect = GUILayoutUtility.GetLastRect();
	EditorGUI.DrawRect(rect, new Color(0, 0.15f, 0.62f, 0.3f));
}

```