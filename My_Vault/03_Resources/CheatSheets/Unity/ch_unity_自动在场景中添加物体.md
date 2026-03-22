---
title: ch unity 自动在场景中添加物体
date: 2026-03-16
tags:
  - resource
  - unity
type: knowledge
aliases:
  -
description: public class LogEditor
draft: false
---

# ch unity 自动在场景中添加物体

```c#
public class LogEditor
{
    [MenuItem("ZMLog/打开日志系统")]
    public static void LoadReport()
    {
        ScriptingDefineSymbols.AddScriptingDefineSymbol("OPEN_LOG");
        GameObject reportObj = GameObject.Find("Reporter");
        if (reportObj==null)
        {
            reportObj= GameObject.Instantiate(AssetDatabase.LoadAssetAtPath<GameObject>("Assets/Scripts/UnityDebuger/Unity-Logs-Viewer/Reporter.prefab"));
            reportObj.name = "Reporter";
            AssetDatabase.SaveAssets();
            EditorSceneManager.SaveScene(EditorSceneManager.GetActiveScene());
            AssetDatabase.Refresh();
            Debug.Log("Open Log Finish!");
        }
    }
    [MenuItem("ZMLog/关闭日志系统")]
    public static void CloseReport()
    {
        ScriptingDefineSymbols.RemoveScriptingDefineSymbol("OPEN_LOG");
        GameObject reportObj = GameObject.Find("Reporter");
        if (reportObj!=null)
        {
            GameObject.DestroyImmediate(reportObj);
            AssetDatabase.SaveAssets();
            EditorSceneManager.SaveScene(EditorSceneManager.GetActiveScene());
            AssetDatabase.Refresh();
            Debug.Log("Cloase Log Finish!");
        }
    }
}

```