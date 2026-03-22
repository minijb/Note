---
title: Unity 编辑器全局设置
date: 2026-03-16
tags:
  - unity
  - editor
type: framework
aliases:
  编辑器全局
description: Unity编辑器全局配置
draft: false
---


## 1. 编辑器相关的文件夹

**Editor**
- 可以放在任何文件夹下，可以存在多个
- **不会打包**
**Editor Default Resources**
- Assets 根目录下，用来存放编辑器所需要的文件
- `EditorGUIUtility.Load()`
**Gizmos**
- Assets 根目录下，用来存放编辑器所需要的文件
- `Gizmos.DrawIcon()`

## 2. `[MenuItem]` 添加菜单栏按钮

`public MenuItem (string itemName, bool isValidateFunction, int priority);`

三个参数
1. 菜单路径
2. 是否是有效函数 --- 有效函数(判断当前是否符合使用条件)
3. priority 优先级，默认值为1000， 数值差大于10，会出现分栏

快捷键

| 符号                 | 按键          |
| ------------------ | ----------- |
| %                  | Ctr/Command |
| #                  | Shift       |
| &                  | Alt         |
| LEFT/RIGHT/UP/DOWN | 方向键         |
| F1-F2              | F功能键        |
| _g                 | 字母g         |

`[MenuItem("MyTools/test1 %_q")]` --- 快捷键为 Ctrl + Q

## 3. CONTEXT

**组件添加右键菜单选项** <font color="#0070c0">算是比较常用</font>

`[MenuItem("CONTEXT/Rigidbody/Init")]` --- 为 Rigidbody 添加右键菜单Init选项

## 4. MenuCommand

**获取当前操作组件的上下文**

```c#
[MenuItem("CONTEXT/PlayerHealth/Init")]
public static Init(MenuCommand cmd)
{
	// 这里获得了 对应的上下文对象
	PlayerHealth health = cmd.context as PlayerHealth;
}
```

## 5. ContextMenu 添加小齿轮菜单选项

`[ContextMenu("FunctionName")]`

## 6. ContextMenuItem 

给某个属性添加右键菜单选项

```c#
[ContextMenuItem("displayName", "HandleHealth")]
public float health;

pirvate void HandleHealth()
{
}
```

## 7. Selection 用于获得选择的物体

注意：有很多属性，用来处理多种情况
**常用**
- `activeGameObject` 返回第一个选择的**场景**中的对象
- `gameObjects
- ` 返回场景中选择的多个对象，包含预制体等
- `objects` 返回选择的多个对象
