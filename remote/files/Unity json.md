---
tags:
  - unity
---
## unity 中 对于 json 的解析

```c#
JsonUtility.ToJson(o);
JsonUtility.FromJson<ColorProto>(args[1])
```


## .Net

```c#
JsonSerializer.Serialize<ColorProto>(proto as ColorProto)
JsonSerializer.Deserialize<ReadyProto>(args[1])
```