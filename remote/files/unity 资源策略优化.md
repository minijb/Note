---
tags:
  - unity
---
## GC.MarkDependencies 

起因 : `Resources.UnloadUnusedAssets();`  过程中有大量未被使用的资源被释放导致性能下降

解决 : 使用 UnloadAsset 及时释放内存中没有使用的资源


