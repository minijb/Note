
## 1. 通过 .m / .mm 文件进行交互

放到 `Plugins/IOS` 目录下

## 2. 调用方法


```c#
[DllImport("__Internal")]
private static extern void IOSShowDialog(string title, string message, string confirmButtonString, string cancelButtonString
	SuccessCallBack successCallback, FailCallBack failCallback
);
[DllImport("__Internal")]
private static extern void IOSDoVibrate(long milliseconds);
[DllImport("__Internal")]
private static extern void IOSShowToast(string message);
```


## 3. 回调方法

1. `UnitySendMessage` 需要具体的 GameObject 并且必须 enable
2. 使用 AOT

```c++
// 申明回调函数
typedef void (*SuccessCallback)();
typedef void (*FailCallback)();
void IOSShowDialog(const char* title, const char* message, const char* confirmButtonString, const char* cancelButtonString, SuccessCallback successCallback, FailCallback failCallback);
```


```c#
private static delegate void SuccessCallback();
private static delegate void failCallback();

[MonoPInvokeCallback(typeof(SuccessCallback))]
private static void SuccessCallBack(){
}

[MonoPInvokeCallback(typeof(failCallback))]
private static void FailCallBack(){
}

[DllImport("__Internal")]
private static extern void IOSShowDialog(string title, string message, string confirmButtonString, string cancelButtonString
	SuccessCallBack successCallback, FailCallBack failCallback
);
```


## 3. IOS 部分的整体结构

```c++
extern "C"
{
    typedef void (*SuccessCallback)();
    typedef void (*FailCallback)();
    void IOSShowDialog(const char* title, const char* message, const char* confirmButtonString, const char* cancelButtonString, SuccessCallback successCallback, FailCallback failCallback);
    void IOSShowToast(const char* message);
    void IOSDoVibrat(long milisecond);
}

void IOSShowDialog(const char* title, const char* message, const char* confirmButtonString, const char* cancelButtonString, SuccessCallback successCallback, FailCallback failCallback)
```

