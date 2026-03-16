---
tags:
  - unity
---
## 安装

https://github.com/Cysharp/UniTask.git?path=src/UniTask/Assets/Plugins/UniTask

## 简介

- 使用Update
	- 依赖 monobehaviour
	- 引入更多的成员变量
- 协程
	- 小号打
	- 无法进行异常处理
	- 依赖 monobehaviour
- 使用 async task
	- 解决了对于 mono 的依赖
	- 使用进行 try catch
	- 问题
		- 使用多线程


UniTask 的优点 
- 继承 async 的优点
- 解决跨线程问题，默认使用主线程与 Unity 协同
- 使用值类型，无GC


## 1. 基础

```c#
async UniTask<string> DemoAsync()
{
    //----------------------------------- 1. 直接await 异步方法-----------------------------------
    var asset = await Resources.LoadAsync<TextAsset>("foo");
    var txt = (await UnityWebRequest.Get("https://...").SendWebRequest()).downloadHandler.text;
    await SceneManager.LoadSceneAsync("scene2");


	// -------------------------------- 异步操作 ----------------------------------
    // .WithCancellation enables Cancel, GetCancellationTokenOnDestroy synchornizes with lifetime of GameObject
    var asset2 = await Resources.LoadAsync<TextAsset>("bar").WithCancellation(this.GetCancellationTokenOnDestroy());

    // .ToUniTask accepts progress callback(and all options), Progress.Create is a lightweight alternative of IProgress<T>
    var asset3 = await Resources.LoadAsync<TextAsset>("baz").ToUniTask(Progress.Create<float>(x => Debug.Log(x)));


	// --------------------- 基础等待 -----------------------------------

    // 按帧等待
    await UniTask.DelayFrame(100); 

    // replacement of yield return new WaitForSeconds/WaitForSecondsRealtime
    await UniTask.Delay(TimeSpan.FromSeconds(10), ignoreTimeScale: false);
    
    // yield any playerloop timing(PreUpdate, Update, LateUpdate, etc...)
    await UniTask.Yield(PlayerLoopTiming.PreLateUpdate);

    // replacement of yield return null
    await UniTask.Yield();
    await UniTask.NextFrame();

    // replacement of WaitForEndOfFrame
#if UNITY_2023_1_OR_NEWER
    await UniTask.WaitForEndOfFrame();
#else
    // requires MonoBehaviour(CoroutineRunner))
    await UniTask.WaitForEndOfFrame(this); // this is MonoBehaviour
#endif

    // replacement of yield return new WaitForFixedUpdate(same as UniTask.Yield(PlayerLoopTiming.FixedUpdate))
    await UniTask.WaitForFixedUpdate();


	// ----------------------- waitUntil -----------------------------------

    // replacement of yield return WaitUntil
    await UniTask.WaitUntil(() => isActive == false);

    // special helper of WaitUntil
    await UniTask.WaitUntilValueChanged(this, x => x.isActive);



	// ------------------------- await 一个  IEnumerator coroutines / 一个标准的 task -----------------------------------
	// You can await IEnumerator coroutines
    await FooCoroutineEnumerator();

    // You can await a standard task
    await Task.Run(() => 100);


	// ------------------------  支持 线程池 ！！！ -----------------------------
    // Multithreading, run on ThreadPool under this code
    await UniTask.SwitchToThreadPool();

    /* work on ThreadPool */

    // return to MainThread(same as `ObserveOnMainThread` in UniRx)
    await UniTask.SwitchToMainThread();


	// -------------------------- 网络请求 -----------------------------------

    // get async webrequest
    async UniTask<string> GetTextAsync(UnityWebRequest req)
    {
        var op = await req.SendWebRequest();
        return op.downloadHandler.text;
    }

    var task1 = GetTextAsync(UnityWebRequest.Get("http://google.com"));
    var task2 = GetTextAsync(UnityWebRequest.Get("http://bing.com"));
    var task3 = GetTextAsync(UnityWebRequest.Get("http://yahoo.com"));



	// --------------------------------- whenAll  -----------------------------------

    // concurrent async-wait and get results easily by tuple syntax
    var (google, bing, yahoo) = await UniTask.WhenAll(task1, task2, task3);

    // shorthand of WhenAll, tuple can await directly
    var (google2, bing2, yahoo2) = await (task1, task2, task3);


	// ------------------------------- 返回 异步 value  -----------------------------------
    // return async-value.(or you can use `UniTask`(no result), `UniTaskVoid`(fire and forget)).
    return (asset as TextAsset)?.text ?? throw new InvalidOperationException("Asset not found");
}
```


## 2. 基础 UniTask 以及 AsyncOperation

UniTask 默认不适用多线程

You can await `AsyncOperation`, `ResourceRequest`, `AssetBundleRequest`, `AssetBundleCreateRequest`, `UnityWebRequestAsyncOperation`, `AsyncGPUReadbackRequest`, `IEnumerator` and others when `using Cysharp.Threading.Tasks;`.


extension method

```c#
* await asyncOperation;
* .WithCancellation(CancellationToken);
* .ToUniTask(IProgress, PlayerLoopTiming, CancellationToken);
```

`WithCancellation` 是简单版本的 UniTask。 全部return `UniTask` , 

> await 直接从 原生计时 PlayerLoop 返回， WithCancellation ToUniTask 再指定的 PlayerLoopTime 返回

> AssetBundleRequest 默认返回 asset ，如果想要返回 allAssets, 可以使用 `AwaitForAllAsset`


`UniTask` 类型可以使用 `UniTask.WhenAll`, `UniTask.WhenAny`. 返回值的类型 可以直接使用 放构造。


```c#
public async UniTaskVoid LoadManyAsync()
{
    // parallel load.
    var (a, b, c) = await UniTask.WhenAll(
        LoadAsSprite("foo"),
        LoadAsSprite("bar"),
        LoadAsSprite("baz"));
}

async UniTask<Sprite> LoadAsSprite(string path)
{
    var resource = await Resources.LoadAsync<Sprite>(path);
    return (resource as Sprite);
}
```


加入 一些回调函数， 可以使用 `UniTaskCompletionSource<T>` --- 轻量级别的 `TaskCompletionSource`

```c#
public UniTask<int> WrapByUniTaskCompletionSource()
{
    var utcs = new UniTaskCompletionSource<int>();

    // when complete, call utcs.TrySetResult();
    // when failed, call utcs.TrySetException();
    // when cancel, call utcs.TrySetCanceled();

    return utcs.Task; //return UniTask<int>
}
```


You can convert Task -> UniTask: `AsUniTask`, `UniTask` -> `UniTask<AsyncUnit>`: `AsAsyncUnitUniTask`, `UniTask<T>` -> `UniTask`: `AsUniTask`. `UniTask<T>` -> `UniTask`'s conversion cost is free.

**不应该出现的操作**

- Awaiting the instance multiple times.
- Calling AsTask multiple times.
- Using .Result or .GetAwaiter().GetResult() when the operation hasn't yet completed, or using them multiple times.
- Using more than one of these techniques to consume the instance.

如下

```c#
var task = UniTask.DelayFrame(10);
await task;
await task; // NG, throws Exception
```


## 3. 取消以及异常处理

https://github.com/Cysharp/UniTask?tab=readme-ov-file#cancellation-and-exception-handling

直接使用标准库的task  取消方法

```c#
var cts = new CancellationTokenSource();

cancelButton.onClick.AddListener(() =>
{
    cts.Cancel();
});

await UnityWebRequest.Get("http://google.co.jp").SendWebRequest().WithCancellation(cts.Token);

await UniTask.DelayFrame(1000, cancellationToken: cts.Token);
```

**两种创建方式** : CancellationToken can be created by `CancellationTokenSource` or MonoBehaviour's extension method `GetCancellationTokenOnDestroy`.

```c#
// this CancellationToken lifecycle is same as GameObject.
await UniTask.DelayFrame(1000, cancellationToken: this.GetCancellationTokenOnDestroy());
```

传递方式，直接使用参数进行传递，所有异步方法都推荐写一个这种参数。

CancellationToken表示async的生命周期。你可以保留你自己的生命周期，而不是默认的CancellationTokenOnDestroy。

```c#
public class MyBehaviour : MonoBehaviour
{
    CancellationTokenSource disableCancellation = new CancellationTokenSource();
    CancellationTokenSource destroyCancellation = new CancellationTokenSource();

    private void OnEnable()
    {
        if (disableCancellation != null)
        {
            disableCancellation.Dispose();
        }
        disableCancellation = new CancellationTokenSource();
    }

    private void OnDisable()
    {
        disableCancellation.Cancel();
    }

    private void OnDestroy()
    {
        destroyCancellation.Cancel();
        destroyCancellation.Dispose();
    }
}
```

当 cancellation 实行，所有的方法会抛出 `operationCalceledException` 。

如果没有处理异常最后会传播到 `UniTaskScheduler.UnobservedTaskException` 

手动取消抛出异常，取消异步任务

```c#
public async UniTask<int> FooAsync()
{
    await UniTask.Yield();
    throw new OperationCanceledException();
}
```

也可以忽视异常

```c#
public async UniTask<int> BarAsync()
{
    try
    {
        var x = await FooAsync();
        return x * 2;
    }
    catch (Exception ex) when (!(ex is OperationCanceledException)) // when (ex is not OperationCanceledException) at C# 9.0
    {
        return -1;
    }
}
```

一种更加轻量级的方法忽视异常, `UniTask.SuppressCancellationThrow`

```c#
var (isCanceled, _) = await UniTask.DelayFrame(10, cancellationToken: cts.Token).SuppressCancellationThrow();
if (isCanceled)
{
    // ...
}
```


提前判断并取消

Some features that use Unity's player loop, such as `UniTask.Yield` and `UniTask.Delay` etc, determines CancellationToken state on the player loop. This means it does not cancel immediately upon `CancellationToken` fired.

If you want to change this behaviour, the cancellation to be immediate, set the `cancelImmediately` flag as an argument.

```cs
await UniTask.Yield(cancellationToken, cancelImmediately: true);
```

注意:将cancelimmediate设置为true并检测立即取消的代价比默认行为高。这是因为它使用了CancellationToken.Register;它比在播放器循环上检查CancellationToken要重。