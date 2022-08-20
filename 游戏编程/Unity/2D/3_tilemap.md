## Tilemap的碰撞

 在tilemap中添加tilemap专用的collider 2D：为所有的tilemap添加碰撞

- 有些tilemap不希望有边界:将对应的tile的default collider设置为None

- ruletile同理

### 优化

因为瓦片的碰撞可能存在微小的缝隙可以使用CompositeColider 2D来创建一个大的碰撞体

同时勾选上tilemap colider 2D 中used by composite

## 可收集对象的交互

### 添加生命

```c#
public int maxhealth = 5;
private int currentHealthy;
    

private void changeHealth(int amount)
{
    //限定生命值的范围
    currentHealthy = Mathf.Clamp(currentHealthy + amount, 0, maxhealth);
    Debug.Log("当前生命:"+currentHealthy);
}
```

这里Mathf就是一个工具类

