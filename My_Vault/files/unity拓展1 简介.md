---
tags:
  - unity
---

### 两个需要了解的文件夹

**Editor文件夹** ： 随便放哪，可以有多个，放扩展器相关的文件，不会被打包到游戏内
**Editor Default Resources** ： 存放图片资源 通过 Resources.Load()
**Gizmos** ： - 该文件夹也需要放在Assets根目录下，可以用来存放Gizmos.DrawIcon()的图片资源


## 菜单栏扩展

### **MenuItem** 创建菜单栏按钮

- 第一个参数用来表示菜单的路径；
- 第二个参数用来判断是否是有效函数，是否需要显示；
- 第三个参数priority是优先级，用来表示菜单按钮的先后顺序，默认值为1000。一般菜单中的分栏，数值相差大于10。
- 注意需要是静态方法

**可控制的 menuitem**

```c#
// Validated menu item.
// Add a menu item named "Log Selected Transform Name" to MyMenu in the menu bar.
// We use a second function to validate the menu item
// so it will only be enabled if we have a transform selected.
[MenuItem("MyMenu/Log Selected Transform Name")]
static void LogSelectedTransformName()
{
	Debug.Log("Selected Transform is on " + Selection.activeTransform.gameObject.name + ".");
}

// Validate the menu item defined by the function above.
// The menu item will be disabled if this function returns false.
[MenuItem("MyMenu/Log Selected Transform Name", true)]
static bool ValidateLogSelectedTransformName() // 如果为false 则 不能选择
{
	// Return false if no transform is selected.
	return Selection.activeTransform != null;
}
```

**添加快捷键**

```c#
// Add a menu item named "Do Something with a Shortcut Key" to MyMenu in the menu bar
// and give it a shortcut (ctrl-g on Windows, cmd-g on macOS).
[MenuItem("MyMenu/Do Something with a Shortcut Key %g")]
static void DoSomethingWithAShortcutKey()
{
	Debug.Log("Doing something with a Shortcut Key...");
}
```

| 符号                 | 字符          |
| ------------------ | ----------- |
| %                  | Ctr/Command |
| #                  | Shift       |
| &                  | Alt         |
| LEFT/Right/UP/DOWN | 方向键         |
| F1-F2              | F功能键        |
| _g                 | 字母g         |

**给模块的菜单上添加控制**

在对应的模块上右键，可以看到一个新的按钮

```c#
// Add a menu item called "Double Mass" to a Rigidbody's context menu.
[MenuItem("CONTEXT/Rigidbody/Double Mass")]
static void DoubleMass(MenuCommand command)
{
	Rigidbody body = (Rigidbody)command.context;
	body.mass = body.mass * 2;
	Debug.Log("Doubled Rigidbody's Mass to " + body.mass + " from Context Menu.");
}
```

**MenuCommand**  ： 得到当前组件的上下文


**菜单分组**

默认快捷优先级为10，数值相差大于10就会分栏

```c#
// Add a menu item to create custom GameObjects.
// Priority 10 ensures it is grouped with the other menu items of the same kind
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

**当特定组件被加载的时候添加**

```c#
// Add a menu item called "Test" to the Scene view context menu when the 
// EditorToolContext "TestToolContext" is engaged. 
[MenuItem("CONTEXT/TestToolContext/Test")]
static void TestToolContextItem()
{
	Debug.Log("Testing Test Tool Context Menu Item");
}

// Add a menu item called "Test" to the Scene view context menu when the 
// EditorTool "TestTool" is engaged. 
[MenuItem("CONTEXT/TestTool/Test")]
static void TestToolItem()
{
	Debug.Log("Testing Test Tool Menu Item");
}
```


**ContextMenu、ContextMenuItem** 用于组件

前者针对组件本身， 后者针对组件的元素

```c#
[ContextMenuItem("Reset", "ResetBiography")]
[Multiline(8)]
[SerializeField] 
string playerBiography = "";

void ResetBiography()
{
	playerBiography = "";
}

/// Add a context menu named "Do Something" in the inspector
/// of the attached script.
[ContextMenu("Do Something")]
void DoSomething()
{
	Debug.Log("Perform operation");
}
```


## selection 用于选中的物体

- Selection.activeGameObject 返回第一个选择的场景中的对象
- Selection.gameObjects 返回场景中选择的多个对象，包含预制体等
- Selection.objects 返回选择的多个对象

```c#
//遍历选择的对象，并立刻销毁
foreach(object obj in Selection.objects)
{
    DestroyImmediate(obj);
}
```


https://docs.unity.cn/cn/2023.2/ScriptReference/Selection.html