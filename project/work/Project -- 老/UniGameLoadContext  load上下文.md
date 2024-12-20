
1. 加载上下文将加载过程分类，如资源初始化，资源加载，解析数据，下载数据，等等， 使用 enum 进行标注。 并使用一个 List 对每个类进行存储。 `UniGameStepLoadState[]` ， 长度为 enum (UniGameLoadStep) 的长度，刚好一一对应。 对应的值为 `UniGameStepLoadState` -- enum ： None, Waiting, Succ, Failed
2. stepsTime， 用于记录时间，长度和 `1` 对应
3. 游戏初始化的三个阶段 类型 `UniGameStepLoadState` ，主要用于防止初始资源重复初始化和加载 (只有在 None 的时候才会进行)： 
	 - AssetSystemState
	 - PreAssetLoadState
	 - GameAssetLoadState

常见流程：

`WaitxxxStep` :

```c#
await UniTask.WaitUntil( () => xxxx == true, token);
Steps[(int)UniGameLoadStep.enum] = UniGameStepLoadState.Succ;
```

`SetBeginStep(step)`

-  将 `Steps[]` 对应的状态设置为 Waiting
- 设置 StepsTime
-  UpdateLoadingUI

### 1. LoadPreAsset  async

主要加载各种配置

1.   await 前置操作 `WaitxxxStep`
2.  `SetBeginStep` 
3.   如果 LoadPreAsset 为 None 的时候才会进行加载 ！
	1.  将 PreAssetLoadState 设置为 waiting
	2.   await DataModule.LoadPreAsset()
		1. 加载 buildsetting --- 中的 scriptObject
		2.  将得到是数据放入 UniDataModule --- `AddScriptObject`  TODO
		3.  `GameBuildSettings, UniSetting, UniBoundsConfig, QualitySetting` 进行初始化 (这里利用了UniDataModule ) TODO
	3. 设置 Step 状态 --- 自动设置 UI_Loading
4.  如果 LoadPreAsset 不为 None 则等待直到成功后才进行下一个步骤
5. UniModuleManager  中所有模块执行 onLoadPreAsset 

### 2. LoadGameAsset async

加载item 资源，以及 excel 资源。

1.  await 前置操作 `WaitxxxStep`
2.  `SetBeginStep`
3.  异步加载资源 --- unitask.whenAll
	1.  DataModule.LoadGameAsset(),
	2.  UniLanguage.Initialize(),
	3.  AudioManager.Initialize(),
	4.  [[UniNodeLoadManager]].InitShapesPool()  !!!!
	5. 设置 Step 状态  --- 自动设置 UI_Loading
4.  如果 LoadPreAsset 不为 None 则等待直到成功后才进行下一个步骤