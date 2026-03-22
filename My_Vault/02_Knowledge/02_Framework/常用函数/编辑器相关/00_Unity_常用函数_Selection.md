---
title: Unity Selection 选中对象
date: 2026-03-16
tags:
  - unity
  - editor
  - selection
type: framework
aliases:
  Selection
description: Unity编辑器 Selection类获取选中对象
draft: false
---


## Selection 用于返回在编辑器中选中的物体

count 返回选中的个数， `activeContext/GameObject/InstanceID/Object/Transform` 返回处于活动转台的物体, `assetGUIDs` 返回**选中资源**的GUID，`transforms,objects,gameObjects,instancesID` 则是未过滤的选择。 `selectionChanged` 选择改变时的回调

```c#
static void CheckDirectoryDependencies()
{
    // 获取选中的文件夹
    string[] selectedGUIDs = Selection.assetGUIDs;
    if (selectedGUIDs.Length == 0) return;

    StringBuilder report = new StringBuilder();
    report.AppendLine("=== 目录依赖检查报告 ===");

    foreach (string guid in selectedGUIDs)
    {
        string path = AssetDatabase.GUIDToAssetPath(guid);

        // 检查是否是文件夹
        if (!AssetDatabase.IsValidFolder(path))
        {
            Debug.LogWarning($"{path} 不是文件夹，跳过");
            continue;
        }

        AnalyzeSingleDirectory(path, report);
    }
}
```