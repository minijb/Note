
## 1. 自定义打包


包含的内容：
- C# 脚本
- 程序集
- 原生插件
- 模型、纹理、动画和音频剪辑以及其他资源。



## 2. 布局约定

```txt
<root>
  ├── package.json
  ├── README.md
  ├── CHANGELOG.md
  ├── LICENSE.md
  ├── Editor
  │   ├── Unity.[YourPackageName].Editor.asmdef
  │   └── EditorExample.cs
  ├── Runtime
  │   ├── Unity.[YourPackageName].asmdef
  │   └── RuntimeExample.cs
  ├── Tests
  │   ├── Editor
  │   │   ├── Unity.[YourPackageName].Editor.Tests.asmdef
  │   │   └── EditorExampleTest.cs
  │   └── Runtime
  │        ├── Unity.[YourPackageName].Tests.asmdef
  │        └── RuntimeExampleTest.cs
  └── Documentation~
       └── [YourPackageName].md
```


| **位置**           | **描述**                                                                                                                                                                |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `package.json`   | [包清单](https://docs.unity.cn/cn/2019.4/Manual/upm-manifestPkg.html)，定义了包的依赖项和其他元数据。                                                                                    |
| `README.md`      | 开发者包文档。通常来说，这是文档，可帮助那些想要修改包或想要在包主源代码仓库中推送更改的开发者。                                                                                                                      |
| `CHANGELOG.md`   | 对于包更改的描述，按照相反的时间顺序列示。最好使用标准格式，比如[保留变更日志 (Keep a Changelog)](http://keepachangelog.com/en/1.0.0/)。                                                                     |
| `LICENSE.md`     | 包含包许可证文本。通常，Package Manager 将从所选的 [SPDX 列表网站](https://spdx.org/licenses/)复制文本。                                                                                        |
| `Editor/`        | 特定于 Editor 平台的 Assets 文件夹。与 Assets 下的 Editor 文件夹不同，这只是一个约定，不会影响资源导入管线。请参阅[程序集定义和包](https://docs.unity.cn/cn/2019.4/Manual/cus-asmdef.html)以在此文件夹中正确配置特定于 Editor 的程序集。 |
| `Runtime/`       | 特定于运行时平台的 Assets 文件夹。这只是一个约定，不会影响资源导入管线。请参阅[程序集定义和包](https://docs.unity.cn/cn/2019.4/Manual/cus-asmdef.html)以在此文件夹中正确配置运行时程序集。                                        |
| `Tests/`         | 包测试文件夹。                                                                                                                                                               |
| `Tests/Editor/`  | 特定于 Editor 平台的测试文件夹。请参阅[程序集定义和包](https://docs.unity.cn/cn/2019.4/Manual/cus-asmdef.html)以在此文件夹中正确配置特定于 Editor 的测试程序集。                                                 |
| `Tests/Runtime/` | 特定于运行时平台的测试。请参阅[程序集定义和包](https://docs.unity.cn/cn/2019.4/Manual/cus-asmdef.html)以在此文件夹中正确配置运行时测试程序集。                                                                  |
| `Documentation~` | 可选文件夹，用于存储包文档。                                                                                                                                                        |

## 3. 清单  package.json

https://docs.unity.cn/cn/2019.4/Manual/upm-manifestPkg.html

简单例子

```c#
{
  "name": "com.unity.example",
  "version": "1.2.3",
  "displayName": "Package Example",
  "description": "This is an example package",
  "unity": "2019.1",
  "unityRelease": "0b5",
  "dependencies": {
    "com.unity.some-package": "1.0.0",
    "com.unity.other-package": "2.0.0"
 },
 "keywords": [
    "keyword1",
    "keyword2",
    "keyword3"
  ],
  "author": {
    "name": "Unity",
    "email": "unity@example.com",
    "url": "https://www.unity3d.com"
  }
}

```


```ad-note
title:打包命名注意
包的 name需要所有字母小写，否则会出现错误 
```