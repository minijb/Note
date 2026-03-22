---
title: Unity 内存管理 加载过程和卸载策略
date: 2026-03-16
tags:
  - knowledge
  - unity
type: knowledge
aliases:
  -
description: https://baddogzz.github.io/2020/02/07/Unload-Resources/
draft: false
---

# Unity 内存管理 加载过程和卸载策略

https://baddogzz.github.io/2020/02/07/Unload-Resources/
https://zhuanlan.zhihu.com/p/1957212556377695584
https://blog.csdn.net/wu87990686/article/details/106862525
https://zhuanlan.zhihu.com/p/26972064669

https://blog.csdn.net/liweizhao/article/details/136761813 弱引用计数
[AssetBundle 介绍](https://aihailan.com/archives/4309)
https://zhuanlan.zhihu.com/p/496737920
https://zhuanlan.zhihu.com/p/1957212556377695584
https://gwb.tencent.com/community/detail/118994
https://zhuanlan.zhihu.com/p/660220029
https://gwb.tencent.com/community/detail/120369
https://caihua.tech/2017/07/16/2017-7-16-AssetBundle%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0%EF%BC%9A%E8%B5%84%E4%BA%A7%E3%80%81%E5%AF%B9%E8%B1%A1%E5%92%8C%E5%BA%8F%E5%88%97%E5%8C%96/
https://zhuanlan.zhihu.com/p/12227278636

https://blog.csdn.net/linxinfa/article/details/122390621

## 坑

Resources.UnloadAsset卸载，Sprite只会卸载Sprite组件，和Texture2D关联，不会卸载Texture2D图片，需要在调用Resources.UnloadUnusedAssets，才会卸载Texture2D图片。因此卸载Sprite后场景中引用了该Sprite的物体不受影响，只有再调用Resources.UnloadUnusedAssets后，图片信息才会丢失。
