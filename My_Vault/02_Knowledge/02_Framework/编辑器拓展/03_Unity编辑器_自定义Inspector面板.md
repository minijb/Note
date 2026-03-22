---
title: Unity 自定义Inspector
date: 2026-03-16
tags:
  - unity
  - editor
  - inspector
type: framework
aliases:
  Inspector
description: Unity自定义Inspector面板
draft: false
---


# Unity编辑器 自定义Inspector面板

```c#
public class CustomEditorTest : MonoBehaviour 
{
    [Space(10)]
    public int     intValue;
    public bool    boolValue;
    public Vector2 v2;
    public float[] floatArray = new float[] {1.0f, 2.0f, 3.0f};
}

// 绘制方式1
[CanEditMultipleObjects, CustomEditor(typeof(CustomEditorTest))]
public class CustomEditorTestEditor : Editor
{
	private CustomEditorTest _target {get}
    public override void OnInspectorGUI()
    {
	    // 绘制原本的东西
	    // base.DrawDefaultInspector()
        // 自定义绘制Inspector
	    _taget.intValue = EditorGUILayout.IntField("IntValue", _target.intValue);
    }
}

// 绘制方式2

[CanEditMultipleObjects, CustomEditor(typeof(CustomEditorTest))]
public class CustomEditorTestEditor : Editor
{
	private SerializedProperty intValue;
    public void OnEnable()
    {
		intValue = serializedObject.FindProperty("intValue");
    }
    public override void OnInspectorGUI()
    {
	    serializedObject.Update();
	    EditorGUILayout.PropertyField(intValue);
    }
}


```


可以使用 layout 进行布局， 并使用label 进行提示

