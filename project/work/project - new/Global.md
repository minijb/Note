
全局信息

```c#
public static UniAssetModule AssetModule;
public static UniDataModule DataModule;
public static UniRpcModule RpcModule;
public static UniAdsModule AdsModule;
public static UniNetworkSetting NetworkSetting;
public static int MainThreadID { get; protected set; }
public static UniPlay Play { get; protected set; }
public static UniGame Game => Play ? Play.Game : null;
public static UniUserMe UserMe = new UniUserMe();
[Sirenix.OdinInspector.ShowInInspector]
protected UniLaunchConfig launchConfig;

// 版本信息
```

