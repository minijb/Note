
用于初始化插件

## 1. preInit

非 editor 模式

1. 对于 NetWork (Mirror) 进行初始化
2. 使用自定义的 fixupdate 处理参数 如下 （需要自己添加到 player loop 中）

```c#
static void OnEnginePreFixedUpdate()  
{  
    if(CanFixedUpdate)  
    {        engineEarlyUpdateTime = System.DateTime.Now;  
    }
}  
static void OnEngineLateFixedUpdate()  
{  
    CanFixedUpdate = false;  
    var usedTime = (float)(System.DateTime.Now - engineEarlyUpdateTime).TotalSeconds;  
    if(usedTime<fixedTimeStep||usedTime>maxFixedTimeStep)  
    {        CanFixedUpdate=true;  
    }
}
```

### Initialize

添加一下 component

1.  Mirror 模块
2.  UniCharacters
3.  UniInteractManager  交互管理模块
4.  UniSwitchManager  服务器和客户端 时间交互通道/事件池
5.  UniUGVAvatarAnimationModule  动作管理
6.  UGCScriptExecuteService 代码执行 ？ 是不是自适应代码那个
7.  UniMissileManager  子弹管理？
8.  UniRankModule 排行管理 

根据 世界类型 在 UniScene 中 添加对应的 UnixxxScene.

[[UniScence|UniScene -> PreInitialize]] -- 进行预处理

