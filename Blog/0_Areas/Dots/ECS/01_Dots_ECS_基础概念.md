
## 1. 三大基础组成 E C S

**E** ： entites --> 实体  没有数据和逻辑，可以看作ID
**C** ： Component --> 组件 只含有数据
**S** ： System  --> 系统  只包含逻辑

![jpg](https://docs.unity3d.com/Packages/com.unity.entities@1.4/manual/images/entities-concepts.png)

## 2. 其他概念

**World** ： 世界， 实体的集合保存在 World 中， 通过 World 内部的 [`EntityManager`](https://docs.unity3d.com/Packages/com.unity.entities@1.4/api/Unity.Entities.EntityManager.html) 进行管理。
**Archetype** ： 原型， 具有相同唯一组件类型的组合的实体的唯一标识符
**Chunck**: 所有具有相同原型的实体和组件都存储在称为“块”的统一内存块中。每个块包含 16 KiB 的空间，其可存储的实体数量取决于该块原型中组件的数量和大小。系统会[`EntityManager`](https://docs.unity3d.com/Packages/com.unity.entities@1.4/api/Unity.Entities.EntityManager.html)根据需要创建和销毁块。

![200](http://www.benmutou.com/wp-content/uploads/2019/12/120519_0241_UnityECS52.png)

> 数据块内部包含一个数据， 分别对应每种组件类型和ID。 因此是紧密排布的