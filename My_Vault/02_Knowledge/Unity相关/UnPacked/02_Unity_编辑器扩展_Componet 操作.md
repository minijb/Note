---
title: Unity Component 操作
date: 2026-03-16
tags:
  - unity
  - editor
  - component
type: framework
aliases:
  Component
description: Unity编辑器Component组件操作
draft: false
---


### 1. 给某组件添加右边小齿轮菜单选项

**`[ContextMenu(string buttonName)]`**

```c#
[ContextMenu("TestFunc")]
public void TestFunction()
{
	Debug.Log("Test");
}

```


### 2. 给某属性添加右键菜单选项

**`[ContextMenuItem(string buttonName, string functionName)]`**

```c#
[ContextMenuItem("ChangeNum", "ChangeNumFunc")]
public int testNum;
private void ChangeNumFunc()
{
    testNum = 2;
}

```