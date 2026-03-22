---
title: Unity 自定义窗口
date: 2026-03-16
tags:
  - unity
  - editor
  - window
type: framework
aliases:
  自定义窗口
description: Unity自定义EditorWindow窗口
draft: false
---


## 1. 窗口类型

1. ScriptableWizard（向导窗口）

- 单一目的的工具：设计用于执行特定的、一次性的任务
- 简化的工作流程：通常用于导入、设置、创建资源的向导
- 自动布局：内置了标准化的UI布局结构
- 预定义的按钮：通常有"Create"、"Apply"、"Cancel"等标准按钮

```c#
// 开启一个 Wizard windows
ScriptableWizard.DisplayWizard<xx>("title", "确定", "取消");

// 更新时调用

private void OnWizardUpdate()
{

}

private void OnWizardCreate()
private void OnWizardOtherButton()
protected override bool DrawWizardGUI()
```

2. EditorWindow（自定义编辑器窗口）

- 完全自定义：可以创建任意复杂度的编辑器界面
- 持久化状态：窗口可以保持打开，状态可以保存
- 灵活的UI布局：使用IMGUI或UI Elements自由绘制界面
- 多标签页支持：可以创建复杂的多页面工具

```c#
// 打开window
private static xxx window;
window = EditorWindow.GetWindow<xxx>("name");
window.show();

private void OnGUI()

```

2. PopupWindowContent --- 不常用

- **轻量级临时窗口**：用于显示临时的、非模态的UI元素
- **自动定位**：通常显示在触发它的控件附近
- **自动关闭**：点击窗口外部时自动关闭
- **无边框设计**：简洁的弹出式设计