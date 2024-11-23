---
tags:
  - protobuf
  - unity
---
- 确定 unity 使用的 api 版本 --- 一般都是 4.x
- 删除 protobuf 上的 targetFrameworks 中多余的版本

```c#
<TargetFrameworks>netstandard1.1;netstandard2.0;net45;net50</TargetFrameworks>
```

- 安装确实的 sdk 版本 
	- 使用 nuget 安装 Microsoft.NETFramework.ReferenceAssemblie.net45 -- Google.Protobuf
	- 注意：需要修改 global.json 中的版本
- 执行生成

