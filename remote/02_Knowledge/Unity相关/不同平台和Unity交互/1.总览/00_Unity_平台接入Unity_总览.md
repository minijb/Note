
## 1. Android 接入 Unity

1. 使用AndroidJavaClass调用JNI访问系统方法，无法直接使用Android资源
2. 将 Java 代码作为插件导入 Unity (Jar/AAR)  可以接入任意Java库，很灵活。

## 2.UnityPlayerActivity

核心父类， https://blog.csdn.net/qq_33060405/article/details/147198174

UnityPlayerActivity 是 Unity 在 Android 平台上的主要活动类，它在 Unity 导出到 Android 工程时自动生成。这个类负责启动 Unity 引擎、管理游戏的生命周期以及处理与 Android 系统的交互。以下是对 UnityPlayerActivity 的详细解析，包括其功能、生命周期管理和与 Unity 引擎的交互。

可以使用自定义 UnityPlayerActivity 以此来让 Unity 和 Unity 进行交互。

## 3. 如何自定义UnityPlayerActivity

1. 需要一个unity的类库 unity.class

- 可以 build 那个界面将，export porject 打勾 -- 导出android studio 项目
- 也可以自己到编辑器界面寻找


## 4. c# 和 Java 之间的交互方式

C#调用Java有两种方式：

一是使用AndroidJavaClass/AndroidJavaObject

二是使用AndroidJNI/AndroidJNIHelper

Java调用C#有两种方式：

一是使用UnitySendMessage

二是使用AndroidJavaProxy
