
UIPathDic ： UI 路由 --- 生成路径 ： `dic<UIName, string>`
UIFactory ： 工厂 --- enum ,   `Func<UIBase>`
UIPool : 缓存池
FirstUI ： enum --- 第一个 UI

一些常用的小组件 ： dialog ， MessagePop，gameloading

```c#
private static GameObject toastParent;  
public static UIGizmosManager GizmosMgr = new UIGizmosManager();
private Transform uiParent;
private Transform hudCanvas;
GameObject Toast;

```
