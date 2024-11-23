
配合 unity 的剔出功能，根据距离进行自动剔除。


重要知识点 : 使用 CullingGroup 进行剔除.

如何设置 culling 的距离:  `public float[] FastCullingDistance = new float[] { 0f, 12.8f, 25.6f, 51.2f, 102.4f, 204.8f, 409.6f, 819.2f };`


根据当前用户设置的 Quality 得到剔除的阈值。


### 方法

- Init : 初始化管理器
- applyCullingData : 设置当前 剔除 group的值


**RefineChunckChange**  简易的八叉树节点控制

`public void RefineChunckChange(Vector3 cameraPos)`

1.  交换 tempRefineNodeSet 以及 refineSpaceNodesSet  :  refine 为 空,  temp 为 前一次 计算的结果
2.  position / NODE_WIDTH -->  在6个方向上尝试找到 SpaceNode
	1. 没有, 则创建 refineNode 并在 其中添加 renderer
	2. 有 , 则直接添加
3. 


将 tempRefineNodeSet 中的内容清空


