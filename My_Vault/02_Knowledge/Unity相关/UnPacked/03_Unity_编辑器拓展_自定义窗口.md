
## 1. 创建一个窗口类

```csharp
public class Lesson2 : EditorWindow
{
    [MenuItem("Unity编辑器拓展/Lesson2/显示自定义面板")]
    private static void ShowWindow()
    {
        Lesson2 win = EditorWindow.GetWindow<Lesson2>();
        win.titleContent = new GUIContent("我的窗口");
        win.Show();
    }
}
```


必须继承 EditorWindow

并且在该类的OnGUI函数中编写面板控件相关的逻辑


## 2. 显示窗口

`EditorWindow.GetWindow`

#TODO 