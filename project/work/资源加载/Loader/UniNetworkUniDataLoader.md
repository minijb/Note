
根据 mapID + version ， 从网络上得到网络节点。


**异步获取内容的方式**

```c#
await UniTaskPool.RunOnThreadPool(() =>  
{  
    file = GetUniNodeFile(dataFixer, parent, createFileOnFailed, checkEditCache);  
});
```

### GetUniNodeFile

1. 将 网络获得的信息进行解压缩 `UniNodeFile.Decompress(ReponseRawData, 0, ReponseRawData.Length, out var binData, out var _)`  --- 也就是 binData 
2. 根据解析的信息，获得file : `UniNodeFile`  --- [[UniNetworkUniDataLoader#GetUniNodeFile]]
3. 返回 file


