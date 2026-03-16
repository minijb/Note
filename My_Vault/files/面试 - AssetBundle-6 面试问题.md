---
tags:
  - 面试
---
## 面试相关

Asset 是什么： 如 texture, mesh, material 等 
GameObject ： 可以存在于游戏的实际场景中，也就是 asset 实例化后的对象 
AssetBundle： 资源管理插件，可以用于资源资源的压缩，传输等。

**打包策略** ： 
- 多个资源打成一个包， 此时的问题就是，加载一个包可能会加载多个资源，不利于热更新
- 打成多个包 ： 容易造成冗余，同时影响包的读取速度，同时不同包内可能存在重复


## 1 . 资源依赖

通过xml进行配置需要维护， 一般通过项目逻辑进行划分，减少依赖。

### 1.1 循环依赖

在打包过程中，使用 hashset 进行记录，通过 资源级别的检测，防止循环依赖

### 1.2 依赖丢失

需要把所有依赖的Bundle 先加载进来，否则会出现丢失。

### 1.3 压缩方式

Lz4 ： 快，分块进行加压，每次解压可以重用之前的内存，减少内存峰值。

**压缩分为两部分：** 索引+实际打包数据部分。

## 2. Resource

被打包进来的时候会被做成一个红黑树用作索引，**Resource 越大，红黑树越大， 同步不可以卸载，在游戏开始的时候就被加载到内存中，拖慢游戏启动的时间**

## 3. AssetBundle 卸载时机

```c#
AssetBundle.Unload(flase); // 释放 assetbundle 内存镜像， 不包含 load 穿甲拿到 asset 内存对象
AssetBundle.Unload(true); // 释放  内存镜像并销毁所有 load 创建的 asset 内存对象
```

推荐 true， 否则 内存垃圾越来越多。
使用 false， 容易出现资源重复加载

## 4. 资源的复制和引用

1. Instaniate 一个 prefab  是对 asset 的 clone + 引用结合的过程  
2. GameObject transform 是 clone 的。
3. 其他如 mesh ，texture ，material， shader 等是纯引用关系


![dLTUXZercWDaMbg.png](https://s2.loli.net/2024/08/14/dLTUXZercWDaMbg.png)


总结 ： 
- assetbundle 的可以从硬盘或者网络上加载到内存。
- load 过程就是将 对应的资源 解压， --- 使用 loadFromFile
- loadAsset 创建 asset 对象 `assetBundle.LoadAsset(name, type)`
- 使用 Instantiate 进行复制即引用
- **unload** ：
	- ture 将下层的全部卸载
	- false 只卸载 内存影响
- **unloadAsset** 只释放 asset
- **unloadUnusedAsset** 只释放内有引用的 asset



