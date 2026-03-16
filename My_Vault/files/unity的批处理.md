---
tags:
  - batch
  - unity
  - optimization
---

## 1. 批处理

将多个 `drawCall` 操作合并为一个，减少cpu和gpu之间的通信

### static batch

**概念**

- static object : 非移动的对象 --- 这些对象可以利用预计算信息减少资源的消耗
- 只有相同材质的的物体才会被合并到一起进行渲染

具体操作：

- 将静态物体合并为一个(或多个)大网格，这个(或这些)大网格以vertex buffers和index buffers的形式存储在GPU上；
- Unity按顺序绘制场景中的物体时[1]，如果两个物体的数据属于同一块buffer，且在vertex buffer和index buffer上连续，那么这两个物体仅产生1次DrawCall；
- 如果它们不连续，那么将产生2次DrawCall(specify different regions of this buffer)；但是由于它们属于同一块buffer，因此这2次DrawCall之间的GPU状态不发生改变，它们构成1次StaticBatch；虽然没有降低DrawCall次数，但是避免了重复的"buffer binding"——我对"buffer binding"的理解是：在shader开始执行前告诉shader这个是vertex buffer、这个是index buffer……
- **静态批处理不一定减少DrawCall，但是会让CPU在“设置渲染状态-提交Draw Call”上更高效；**


### dynamic batch

**动态批处理**，是为过去的低端设备设计的，只有当动态批处理产生的CPU开销小于DrawCall的开销，动态批处理才具有优化性能的效果。而在如今的电子设备上，动态批处理产生的CPU开销反而有可能大于DrawCall的开销，影响性能。因此你需要profile你的应用以确定是否需要动态批处理。

https://zhuanlan.zhihu.com/p/432223843


## SRP Batcher

URP 默认开启

原本，CPU每次提交DrawCall前都要【Set up Cbuffer - Upload Cbuffer】，但是在SRP Batcher里，所有材质球在显存里占有固定的CBuffer，如果材质球的内容不发生改变，CPU就不需要【SetUp-Upload】，从而降低了CPU渲染时间。——SRP batcher不会减少DrawCall，而是在DrawCall与DrawCall之间减少CPU的工作量。

适用场景 ：场景中有很多物体，很多不同的材质球（比如它们的颜色、贴图不同），但是这些材质球使用的是同一个shader（确切地说是Shader Variant）。

https://zhuanlan.zhihu.com/p/432223843

### GPU instancing

适用于大量重复的物体 --- 同一**Mesh**和同一**Material** 比如建筑物/树/草等重复出现的物体。

https://zhuanlan.zhihu.com/p/432223843


