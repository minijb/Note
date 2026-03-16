
## 1. 通过内置方法实现

```c#
private void OnDrawGizmos() // 绘制效果一直显示
private void OnDrawGizmosSelected() // 当选择时显示绘制
```


Gizmos.color 是全局静态变量，因此需用完之后需要赋值为原先的值

## 2. 通过特性实现

```c#
[DrawGizmo(GizmoType.Active | GizmoType.Selected)]
private static void MyCustomOnGrawGizomos(TargetExample target, GizmoType type){

}
```

需要将绘制的类放在 Editor 中， 使用特性的方法可以将业务逻辑和调试脚本分离


| GizmosType      | 描述                 |
| --------------- | ------------------ |
| Active          | 激活，则绘制             |
| SelectedOrChild | 被选择或者选择子物体， xxx    |
| NotSelected     |                    |
| Selected        |                    |
| Pickable        | 在编辑器中 gizmo 可以被点选择 |

## Gizmos 方法

```c#
Gizmos.DrawCube()
Gizmos.DrawWireCube() // 绘制立方体边框
Gizmos.DrawRay() // 绘制射线
Gizmos.DrawLine()
Gizmos.DrawIcon() // icon 素材需要放在 Gizmos 文件夹中
Gizmos.DrawFrustunm() // 绘制摄像机视锥体的范围
```