---
tags:
  - Csharp
  - Event
  - Delegate
---
## 基本概念

Delegates : 简单来说就是函数的类型，可以同时添加多个函数，一起运行

如何向 Delegate 添加函数

```c#
public delegate void TestDelegate(); 
private TestDelegate testDelegateFunction;


testDelegateFunction = () => {xxxxx};
testDelegateFunction = delegate （）{Debug.Log("xxxx");}；


testDelegateFunction += ff;
testDelegateFunction -= ff;
```


Action : 内置 Delegate

```c#
private Action<int, float> testAction; //默认返回值为void
```

更加简洁

Func : 内置 Delegate

```c#
private Func<bool> testFunc; //返回 bool
private Func<int, bool> testFunc1; //函数：int , 返回 : bool
```


## Event

特殊的 Delegate ，利用 权限控制 实现了 发布 订阅模式。


1. 运行 Event `testEvent?.Invoke()`  只能在定义的类内使用
2. `+= , -=` 可以在任意类内使用


如何使用Event

```c#

//使用系统内置的delegate
public event EventHandler<OnSpacePressedArgs> OnSpacePressed;
public class OnSpacePressedArgs : EventArgs {
	public int count;
}

//使用 delegae 创建
public delegate void TestEventDelegate(float f);
public event TestEventDelegate OnFloatEvent;

public event Action<bool, int> OnActionEvent;

publiv UnityEvent OnUnityEvent;

private void Update()
{
	OnSpacePressed?.Invoke(this, new OnSpacePressedArgs {count = 100});
}

```


其他程序进行订阅 

```c#
xxx.OnSpacePressed += TestingEvent_OnSpacePressed;
xxx.OnSpacePressed -= TestingEvent_OnSpacePressed;


private void TestingEvent_OnSpacePressed(object sender, OnSpacePressedArgs e){
	Debug.Log(e);
}
```


#unityEvnet

可以手动添加对应文件内的函数 : [csdn](https://blog.csdn.net/qq_46044366/article/details/122806863)
