

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