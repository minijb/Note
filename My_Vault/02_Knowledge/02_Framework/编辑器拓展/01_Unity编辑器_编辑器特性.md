---
title: Unity 编辑器特性
date: 2026-03-16
tags:
  - unity
  - editor
  - attribute
type: framework
aliases:
  编辑器特性
description: Unity编辑器特性Attributes
draft: false
---


## 1. 属性特性

- `[Range(0,100)]`  限制数值范围
- `[Multline(3)]`  字符串多行显示
- `[TextArea(2,4)]`  文本输入框 --- 最小最大行数，超过最大可以滑动
- `[SerializeField]`  序列化字段
- `[NonSerializeField]` 不序列化，并在Inspector上隐藏
- `[HideInInspector]` 
- `[FormerlySerizalizedAs("Value")]`  当变量名发生改变时，可以保存原来的Value的值
- `[ContextMenu("xx")]`
- `[ContextMenuItem("xx", "xxx")]`  
- `[Header("Value")]`  
- `[Space(10)]`  间隔，数值越大，间隔越大
- `[ToolTip("xxx")]`  提示
- `[ColorUsage(true)]`  显示颜色面板

## 2. 方法特性

- `[DrawGizmo]` 用于Gizmo渲染，讲逻辑与调试代码分析
- `[MenuItem]` 添加菜单项
- `[DLLImport]` DllImport特性适用于方法，告诉运行时的程序：该方法位于指定的DLL的非托管代码中。（DllImporter是在DLL为非托管代码时才会使用的），在Unity3D中引用外部DLL的一个主要目的是方便集成一些外部插件，以便调用现有的外部动态库链接。

## 3. 常用的类的特性

- `[Serializable]` 序列化一个类，作为自述信显示在 Inspect
- `[RequireComponent(typeof(xxx))]` 必须挂在某个组件
- `[DisallowMultipleComponent]` 不允许挂在多个类/起子类
- `[ExecuteInEditMode]` 允许脚本在编辑器未运行情况下运行
- `[CanEditMultipleObjects]` 允许当选择多个刮油该脚本对象时，统一修改至
- `[AddComponentMenu]`可以在菜单栏Component内添加组件按钮
- `[CustomEditor]` 要自定义剪辑器就要添加这个特性
- `[CustomPropertyDrawer]` 用于回执自定义 propertyDrawer 的特性
- `[SelectionBase]` 现在在闯劲中使用概述性的对象，不会无选中子物体

可以同时减价多个特性使用都好隔开 `[SerializeField, Range(0,5)]`

