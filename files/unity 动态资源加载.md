---
tags:
  - unity
---
**常见资源类型**

GameObject（游戏对象）
Shader（着色器）
Mesh（网格）
Material（材质）
Texture/Sprite（贴图/精灵）

**内存镜像**

任何游戏资源或对象一旦加载，都会占用设备的一部分内存区域，这个内存区域就是资源或对象的内存镜像，如果内存镜像过多达到设备的极限，游戏必然会发生性能问题

**引用和复制**

可以说是Unity的“黑科技”之一，但也可以说是资源加载和释放的一个坑点。

- 引用：指对原资源仅仅是引用关系，不再重新复制一份内存镜像，但引用的关键在于，如果原资源被删除会导致引用关系损坏，使得引用的对象发生资源丢失错误。
- 复制：复制原资源的内存镜像，从而产生两个不同的内存区域，如果被复制的资源被释放，不会影响复制的资源。

  ![700](https://i-blog.csdnimg.cn/blog_migrate/bfa36b5f201cd88d9a9ae33b226830a8.jpeg)


1. 加载 assetbundle 会生成内存镜像 -- 紫色
2. 使用 load 会加载绿色部分的资源 ！！！
3. Instaniate 一个 gameobject 会复制一个新的内存区域。

想要完整的销毁一个 gameobject 1. 销毁 gameobject 2. 销毁 asset 3. 销毁 assetbundle

**AssetBundle加载策略**：
1. AssetBundle 只Load一次
2. Asset 只 加载一次 (反复加载也没事)

**AssetBundle 资源释放**

实例化的GameObject ： Destory

**加载的资源prefab** ： 因为是内存镜像，对象可以用Object.Destroy释放，Sprite等资源可以用Reources.UnloadAsset。**但Texture类的资源就比较麻烦，只能通过Resources.UnloadUnusedAssets方法才能比较有效的释放，但条件比较苛刻，prefab的父（bundle）和子（obj）都要已经被释放的情况下，加上本身引用清空，然后使用UnloadUnusedAssets才有效。**

bundle ： AssetBundle.Unload。**参数为false的时候**，仅仅把资源包内存释放，但保留任何已经加载的资源和实例化对象，这些资源和对象的释放有待后续代码完成。**参数为true的时候**，是一次比较彻底的内存释放，资源包和所有被加载出的资源都会被释放，当然实例化的obj不会被释放，但引用关系会被破坏，所以在使用这种方式前必须提前销毁所有实例化对象。


> 当Destory一个GameObject或者其他实例时，只是释放实例中那些Clone出来的Assets，而并不会释放那些引用的Assets，因为Destroy不知道是否有其他人在引用这些Assets。等到场景中没有任何物体引用到这些Assets之后，它们就会成为UnusedAssets，此时可以通过Resources.UnloadUnusedAssets来进行释放。AssetBundle.Unload(false)不行，因为它只会释放文件的内存镜像，不会释放资源；AssetBunde.Unload(true)也不行，因为它是暴力的释放，可能有其他对象在引用其中的Assets，暴力释放可能导致程序错误。
> 
> 系统在加载新场景时，所有的内存对象都会被自动销毁，这包括了Resources.Load加载的Assets, 静态绑定的Assets，AssetBundle.Load加载的资源和Instantiate实例化的对象。但是AssetBundle.Load本身的文件内存镜像（用于创建各种Asset）不会被自动销毁，这个必须使用AssetBundle.Unload(false)来进行主动销毁。推荐的做法是在加载完资源后立马调用AssetBunble.Unload(false)销毁文件内存镜像

https://blog.csdn.net/u013774978/article/details/129847761 可以看看案例分析
