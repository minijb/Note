

## 1. 简单介绍

`[MenuItem("页签名/一级选项/二级选项/....")]`


可以在不同的窗口中添加页签！！  比如 Hierarchy, Project

- Hierarchy  --- `[MenuItem("GameObject/页签/一级选项/二级选项/....")]`

| 窗口                                                    | 前缀                                            |
| ----------------------------------------------------- | --------------------------------------------- |
| Hierarchy 的右键菜单添加物体，同时还有顶部菜单                          | GameObject                                    |
| Project                                               | Assets                                        |
| 菜单栏的Component菜单                                       | `[AddComponentMenu("一级选项/二级选项/....")]`        |
| 在Inspector为脚本右键添加菜单，如果需要在所有组件里面都有，只需要把脚本名改为Component。 | `[MenuItem("CONTEXT/脚本名/页签/一级选项/二级选项/....")]` |


**验证方法+优先级**


`[MenuItem("页签名/一级选项/二级选项/....", true,1000)]`

```csharp
public class MenuTest
{
    [MenuItem("Tools/Test1",false , 0)]
    static void Test1()
    {
        Debug.Log("Selection activeTransform " + Selection.activeTransform);
    }

    [MenuItem("Tools/Test1", true)]
    static bool ValidateTest1()
    {
        return Selection.activeTransform != null;
    }

    [MenuItem("Tools/Test2",false, 1)]
    static void Test2()
    {
        Debug.LogWarning("Test2");
    }
}
```


优先级默认为1000， 如果相差大于10， 则会出现分割线




## 2. 特性

为**组件**添加右键按钮菜单， 并通过 MenuCommand 获取上下文, 可以是自己的脚本。

```c#
[MenuItem("CONTEXT/Rigidbody/xxxx)]

using UnityEngine;
using UnityEditor;

public class Something : EditorWindow
{
    // Add menu item
    [MenuItem("CONTEXT/Rigidbody/Do Something")]
    static void DoSomething(MenuCommand command)
    {
        Rigidbody body = (Rigidbody)command.context;
        body.mass = 5;
        Debug.Log("Changed Rigidbody's Mass to " + body.mass + " from Context Menu...");
    }
}
```

|                                                                                       |                    |
| ------------------------------------------------------------------------------------- | ------------------ |
| [context](https://docs.unity.cn/cn/2023.2/ScriptReference/MenuCommand-context.html)   | 上下文是作为菜单命令目标的对象。   |
| [userData](https://docs.unity.cn/cn/2023.2/ScriptReference/MenuCommand-userData.html) | 用于将自定义信息传递给菜单项的整数。 |

## 3.添加快捷键

语法 路径后 + 空格 + 下划线 + 想要的按键

```csharp
[MenuItem("Unity编辑器拓展/Lesson1/TestFun %#&A")] //加入快捷键Ctrl+shift+alt+A
private static void TestFun()
{
    Debug.Log("TestFun");
}
```

组合键

下划线替换为

%表示ctrl

`#`表示shift

&表示alt

其他支持的按键：

LEFT、RIGHT：持类似#LEFT是左shift之类的按键

UP、DOWN、F1..F12、HOME、END、PGUP、PGDN



## 4. 选中物体

- Selection.activeGameObject 返回第一个选择的场景中的对象
- Selection.gameObjects 返回场景中选择的多个对象，包含预制体等
- Selection.objects 返回选择的多个对象


https://docs.unity.cn/cn/2023.2/ScriptReference/Selection.html


### 静态变量

|   |   |
|---|---|
|[activeContext](https://docs.unity.cn/cn/2023.2/ScriptReference/Selection-activeContext.html)|返回当前的上下文对象，与通过 SetActiveObjectWithContext 设置时相同。|
|[activeGameObject](https://docs.unity.cn/cn/2023.2/ScriptReference/Selection-activeGameObject.html)|返回处于活动状态的游戏对象。（显示在检视面板中的对象）。|
|[activeInstanceID](https://docs.unity.cn/cn/2023.2/ScriptReference/Selection-activeInstanceID.html)|返回实际对象选择的 instanceID。包括预制件、不可修改的对象。|
|[activeObject](https://docs.unity.cn/cn/2023.2/ScriptReference/Selection-activeObject.html)|返回实际对象选择。包括预制件、不可修改的对象。|
|[activeTransform](https://docs.unity.cn/cn/2023.2/ScriptReference/Selection-activeTransform.html)|返回处于活动状态的变换。（显示在检视面板中的变换）。|
|[assetGUIDs](https://docs.unity.cn/cn/2023.2/ScriptReference/Selection-assetGUIDs.html)|返回所选资源的 GUID。|
|[count](https://docs.unity.cn/cn/2023.2/ScriptReference/Selection-count.html)|Returns the number of objects in the Selection.|
|[gameObjects](https://docs.unity.cn/cn/2023.2/ScriptReference/Selection-gameObjects.html)|返回实际游戏对象选择。包括预制件、不可修改的对象。|
|[instanceIDs](https://docs.unity.cn/cn/2023.2/ScriptReference/Selection-instanceIDs.html)|来自场景的实际未过滤选择，以实例 ID 形式返回，而非 objects。|
|[objects](https://docs.unity.cn/cn/2023.2/ScriptReference/Selection-objects.html)|来自场景的实际未过滤选择。|
|[selectionChanged](https://docs.unity.cn/cn/2023.2/ScriptReference/Selection-selectionChanged.html)|当前活动/所选项发生更改时触发的委托回调。|
|[transforms](https://docs.unity.cn/cn/2023.2/ScriptReference/Selection-transforms.html)|返回顶级选择，不包括预制件。|

### 静态函数

|                                                                                                                         |                                    |
| ----------------------------------------------------------------------------------------------------------------------- | ---------------------------------- |
| [Contains](https://docs.unity.cn/cn/2023.2/ScriptReference/Selection.Contains.html)                                     | 返回某个对象是否包含在当前选择中。                  |
| [GetFiltered](https://docs.unity.cn/cn/2023.2/ScriptReference/Selection.GetFiltered.html)                               | 返回按类型和模式筛选的当前选择。                   |
| [GetTransforms](https://docs.unity.cn/cn/2023.2/ScriptReference/Selection.GetTransforms.html)                           | 允许使用 SelectionMode 位掩码对选择类型进行精细控制。 |
| [SetActiveObjectWithContext](https://docs.unity.cn/cn/2023.2/ScriptReference/Selection.SetActiveObjectWithContext.html) | 选择具有上下文的对象。                        |


## 5. 注意点

在使用 GameObject 也就是在 Hierarchy 窗口添加游戏对象的时候， 需要使用   [GameObjectUtility.SetParentAndAlign](https://docs.unity.cn/cn/2019.4/ScriptReference/GameObjectUtility.SetParentAndAlign.html) 从而保证正确的上下级关系， 同时需要使用 [Undo.RegisterCreatedObjectUndo](https://docs.unity.cn/cn/2019.4/ScriptReference/Undo.RegisterCreatedObjectUndo.html) 是的该操作可以撤销并将物体挂在到  [Selection.activeObject](https://docs.unity.cn/cn/2019.4/ScriptReference/Selection-activeObject.html) 设置到新创建的对象上


为了将“GameObject/”中的菜单项 传播到层级视图 Create 下拉菜单和层级视图上下文菜单，它必须与 其他游戏对象创建菜单项归为一组。这可以通过将其优先级 设为 10 来实现（请参阅以下示例）


```c#
    // Add a menu item to create custom GameObjects.
    // Priority 1 ensures it is grouped with the other menu items of the same kind
    // and propagated to the hierarchy dropdown and hierarchy context menus.
    [MenuItem("GameObject/MyCategory/Custom Game Object", false, 10)]
    static void CreateCustomGameObject(MenuCommand menuCommand)
    {
        // Create a custom game object
        GameObject go = new GameObject("Custom Game Object");
        // Ensure it gets reparented if this was a context click (otherwise does nothing)
        GameObjectUtility.SetParentAndAlign(go, menuCommand.context as GameObject);
        // Register the creation in the undo system
        Undo.RegisterCreatedObjectUndo(go, "Create " + go.name);
        Selection.activeObject = go;
    }
```

