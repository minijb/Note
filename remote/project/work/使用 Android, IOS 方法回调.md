
## Android

unity端调用方式有以下4种:
1、调用Android普通class的静态方法
`AndroidJavaObject helper = new AndroidJavaObject(“包名.类名”);`
helper.CallStatic(“方法名”, 参数1，参数2…);
example:

```c#
AndroidJavaObject helper = new AndroidJavaObject(“pers.study.android2unity.Helper”);
helper.CallStatic(“getMessageFormUnity”, “我是 unity”);
```

使用时，我们要确保，Android端有对应的包、类、方法，且参数一一对应。


2、调用Android普通class的非静态方法
`AndroidJavaObject helper = new AndroidJavaObject(“包名.类名”);`
helper.Call(“方法名”, 参数1，参数2…);
example:

```c#
AndroidJavaObject helper = new AndroidJavaObject(“pers.study.android2unity.Helper”);
helper.Call(“setAndroudForUntiyListener”, listener);
```

3、调用Android继承于unityplayerActivity的activity静态方法
下面两行是必写的，且参数“com.unity3d.player.UnityPlayer”，“currentActivity”是固定的，不能更改。用于获取UnityPlayer和当前Activity。

```c#
AndroidJavaClass jclass = new AndroidJavaClass(“com.unity3d.player.UnityPlayer”);
AndroidJavaObject jcontext = jclass.GetStatic(“currentActivity”);
//BridgeActivity是继承于unityplayerActivity的类
AndroidJavaClass loginObject = new AndroidJavaClass(“com.bridge.BridgeActivity”);
loginObject.CallStatic(“showToast”, jcontext)
```

4、调用Android继承于unityplayerActivity的activity非静态方法

```c#
//同上，下面两行必写
AndroidJavaClass jclass = new AndroidJavaClass(“com.unity3d.player.UnityPlayer”);
AndroidJavaObject jcontext = jclass.GetStatic(“currentActivity”);
//安卓端add方法有两个参数，且返回值为int类型
jcontext.Call(“add”, 15, 9)；
```


## IOS

```c#
#if UNITY_IOS/UNITY_IPHONE
[DLLImport("__Internal")]
private static entern void addApplePayObserver();
#endif
```