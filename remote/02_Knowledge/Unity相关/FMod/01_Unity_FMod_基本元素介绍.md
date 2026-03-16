
## 1. Event 事件

FMod的所有音频效果都依赖于 Event.

程序的角度看，事件可以分为两种，功能性事件和音频类事件，  
功能性事件：它可以做到让某一类或者某一个音频暂停  
音频类事件：就是常规的播放声音

```cs
    private EventInstance eventInstance;  // 事件实例

    // 事件路径（请确保路径正确，大小写敏感）
    private string eventPath = "event:/MySoundEvent";

    void Start()
    {
        // 通过事件路径创建事件实例
        eventInstance = RuntimeManager.CreateInstance(eventPath);
        eventInstance.start();
        eventInstance.release();
    }
```

- 其中release()函数 标记 事件实例（EventInstance）为 可释放状态。事件实例一旦被标记为释放，当其进入“已停止”状态（FMOD_STUDIO_PLAYBACK_STOPPED）时，异步更新系统会自动销毁该实例。

```ad-note
- 一般来说 start 之后立即调用 release 进行释放。
- 如果希望多次调用，可以使用 step 进行停止，然后 start 。
- 调用 release 之后 仍然可以继续操作，但是如果已经完全停止， 可能返回无效句柄
```

## Bus 总线


- Bus 可以理解为相关音频或者功能事件的集合的总控，可以统一控制这个一组事件的各种参数，例如可以一次性调整某一类音效（如音乐或环境音）的音量，而不是单独修改每个事件的音量。

```cs
public class FMODBusHandler : MonoBehaviour
{
    public void ControlMusicBus(float volume, bool mute)
    {
        // 获取 Bus（确保路径正确）
        Bus musicBus = RuntimeManager.GetBus("bus:/Music");

        // 设置音量（范围 0.0 ~ 1.0）
        musicBus.setVolume(volume);

        // 设置静音状态
        musicBus.setMute(mute);
    }
}
```

**Master Bus作用**

- **Master Bus** 是 FMOD **音频信号流的最终出口**，所有音频最终都会经过 Master Bus 进行混音，并输出到音频设备（扬声器、耳机等）。
- Master Bus **控制整个游戏的主音量**，常用于 **全局音频管理**。
- **不能跳过 Master Bus**，FMOD 需要它来完成最终混音和输出。

信号流向

```text
[Music Bus] → [Master Bus] → [游戏音频输出]
[SFX Bus] →  
[Voice Bus] →  
[Reverb Return] →
```

📌 适用场景  
✅ 统一控制游戏的 全局音量  
✅ 处理 最终混音，如动态范围控制、音频压缩  
✅ 用于 全局静音、暂停音频（如游戏暂停时降低所有音量）


## Group Bus（分组总线）

- **Group Bus** 用于分类管理不同类型的音效，例如：
    - **Music Bus（音乐）**
    - **SFX Bus（音效）**
    - **Voice Bus（角色语音）**
- **Group Bus 允许单独调整某类音效的音量、混响、EQ**，而不会影响其他类别的音效。
- **多个事件（Event）可以输出到同一个 Group Bus**，然后再统一流向 Master Bus。

 **📌 信号流向**

```text
[事件: Background Music] → [Music Bus] → [Master Bus] → [游戏音频输出]
[事件: Footstep SFX] → [SFX Bus] →  
[事件: Character Voice] → [Voice Bus] →  
```

📌 适用场景  
✅ 调整某类音效的整体音量（如降低环境音，提高语音）  
✅ 在不同场景下动态改变某个类别的音效（如战斗时提高战斗音效，降低环境音）  
✅ 在 UI 设置中让玩家独立调节音乐、音效、语音的音量


## **3. Return Bus（返回总线）**

- Return Bus 是 FMOD 中用于 处理音频特效 的总线。**它的主要作用是接收来自多个音频源的信号，统一进行特效处理（如混响、低通滤波），然后再返回到主混音（Master Bus）。**
- **音效不会直接流入 Return Bus，而是由 Group Bus 发送部分音频信号（Send）到 Return Bus**，Return Bus 处理完毕后再返回 Master Bus。
- **多个 Group Bus 可以共享同一个 Return Bus，节省 CPU 计算量**（如多个角色语音共用一个混响）。

**📌 信号流向**

```text
[事件: 角色脚步声] → [SFX Bus] → [Reverb Return Bus] → [Master Bus] → [游戏音频输出]
[事件: 枪声] →
[事件: 环境音] →
```

📌 适用场景  
✅ 洞穴、教堂等场景混响（让所有声音共享一个 Reverb 计算）  
✅ 水下效果（低通滤波）（进入水中时声音变闷）  
✅ 提高性能，避免每个音效单独计算 DSP

Return Bus 允许多个声音 共享同一个混响或特效处理，而不是每个事件都独立计算混响。  
🎯 示例：游戏中的 洞穴、房间、大厅 等场景，需要有回声效果（Reverb）。如果每个声音单独处理混响，会占用大量 CPU 资源。Return Bus 可以 统一处理这些音效，提高性能。


## **Return Bus vs. Group Bus vs. Master Bus**

|**Bus 类型**|**作用**|**信号流向**|**适用场景**|
|---|---|---|---|
|**Master Bus**|负责最终音频输出，游戏所有音效都会经过此 Bus|Group Bus → Master Bus → 音频输出|调整游戏的整体音量、全局混音|
|**Group Bus**|组织和管理某一类音效（如音乐、SFX、语音）|事件 → Group Bus → Master Bus|音乐、音效、角色语音的分组管理|
|**Return Bus**|处理音频特效（如混响、低通滤波等）|事件 → Group Bus → Return Bus → Master Bus|洞穴混响、水下滤波、全局特效音处理|

✅ Master Bus 负责最终混音和游戏音频输出  
✅ Group Bus 主要用于分类管理不同类型的音效（如音乐、SFX、语音）  
✅ Return Bus 主要用于处理音频特效（如混响、低通滤波）

注意⚠️：Bus是串联连接时，**如果需要链路畅通，需要保持所有bus闭合**



## **FMOD 参数（Parameter）**

### **🔹 全局参数 vs. 事件参数（区别 & 适用场景）**

|**参数类型**|**作用范围**|**适用场景**|**代码调用方式**|
|---|---|---|---|
|**事件参数（Event Parameter）**|仅作用于 **特定事件实例**|**单个音效的动态变化**（如脚步音随地形变化）|`eventInstance.setParameterByName("参数名", 值);`|
|**全局参数（Global Parameter）**|作用于 **所有事件**，多个事件共享|**影响整个游戏的音效**（如天气、战斗状态、背景音乐情绪）|`RuntimeManager.StudioSystem.setParameterByName("参数名", 值);`|

---

### **🔹 基于参数动态调整音效（如脚步音随地形变化）**

- **事件参数** 可用于**改变同一音效的表现**（如脚步声在草地、木板、金属上的不同声音）。
- **全局参数** 可用于**改变整个游戏环境**（如雨天音效增强、战斗音乐变得紧张）。

```csharp
public class FMODParameterExample : MonoBehaviour
{
    public void SetFootstepSurface(float surfaceType)
    {
        EventInstance footstepInstance = RuntimeManager.CreateInstance("event:/Footstep");
        footstepInstance.setParameterByName("SurfaceType", surfaceType);
        footstepInstance.start();
        footstepInstance.release();
    }

    public void SetWeatherCondition(string weather)
    {
        EventInstance ambienceInstance = RuntimeManager.CreateInstance("event:/Ambience");
        ambienceInstance.setParameterByNameWithLabel("Weather", weather);
        ambienceInstance.start();
        ambienceInstance.release();
    }
}
```


## **FMOD 事件销毁回调（Callback）**

当 **事件实例被销毁（Destroyed）** 时，FMOD 会触发 `EVENT_CALLBACK_TYPE.DESTROYED` 回调。  
这个回调适用于：

- **在销毁前执行清理工作**
- **确保事件实例正确释放，防止内存泄漏**
- **记录日志，调试事件生命周期**

 **📌 代码示例：监听 FMOD 事件销毁**

```csharp
using FMOD;
using FMOD.Studio;
using FMODUnity;
using UnityEngine;
using System;
using System.Runtime.InteropServices;

public class FMODEventDestroyCallback : MonoBehaviour
{
    private EventInstance eventInstance;

    // FMOD 事件销毁回调
    [AOT.MonoPInvokeCallback(typeof(EVENT_CALLBACK))]
    private static RESULT EventCallback(EVENT_CALLBACK_TYPE type, IntPtr instancePtr, IntPtr parameters)
    {
        EventInstance eventInstance = new EventInstance(instancePtr);

        if (type == EVENT_CALLBACK_TYPE.DESTROYED)
        {
            eventInstance.getDescription(out EventDescription eventDesc);
            eventDesc.getPath(out string eventPath);
        }

        return RESULT.OK;
    }

    void Start()
    {
        // 创建事件实例
        eventInstance = RuntimeManager.CreateInstance("event:/MyEvent");

        // 绑定销毁回调
        eventInstance.setCallback(EventCallback, EVENT_CALLBACK_TYPE.DESTROYED);

        eventInstance.start();
        eventInstance.release();
    }
}
```

**注意事项**

- 事件销毁回调在音频线程执行，不能直接调用 Unity API
- eventPath在制作的过程中，如果有名称的变动，大小写不敏感


## 🔹 VCA（Voltage Controlled Amplifier）音量控制

VCA 是 FMOD 中的 "音量控制单元"，用于集中调节一组 Bus 的音量，类似于一组 Bus 的“总音量推子”。

- 可在 FMOD Studio 中将多个 Bus 分配给一个 VCA
- Unity 中可通过 `RuntimeManager.GetVCA("vca:/YourVCA")` 获取控制其音量

---
 📌 VCA 的特点

|特性|描述|
|---|---|
|控制作用对象|多个 Bus 的 **最终输出音量**|
|不支持 DSP 效果|无法挂载混响、低通、延迟等音频特效|
|无嵌套结构|不像 Bus 有父子层级结构|
|场景管理友好|常用于 UI 设置中的“音乐音量”、“语音音量”|
|性能开销极小|因为不参与信号处理，仅做音量乘法|

---
 📌 VCA 控制代码示例

```csharp
public class FMODVCAController : MonoBehaviour
{
    public void SetVCAVolume(float volume)
    {
        VCA vca = RuntimeManager.GetVCA("vca:/MusicVCA");
        vca.setVolume(volume);  // 范围 0.0 ~ 1.0
    }
}
```

 🔸 Bus vs VCA：功能与结构对比

|对比点|**Bus（总线）**|**VCA（音量控制器）**|
|---|---|---|
|控制内容|音频信号流、混音、DSP|音量控制，不处理音频信号流|
|DSP 支持|✅ 可添加混响、滤波等|❌ 不支持任何 DSP|
|层级结构|✅ 支持嵌套|❌ 无嵌套，所有 VCA 是平级|
|跨层控制能力|❌ 仅控制自身及子 Bus|✅ 可跨任意 Bus 层级控制|
|用途|路由、混响、暂停、效果分类管理|统一逻辑音量控制（如 UI、音乐、语音）|
|设置方式|在 Studio 中构建 Bus 树结构并指定|在 Studio 中手动将 Bus 指定到某个 VCA|

 ✅ VCA 的跨层控制能力

#### 什么是“跨层控制”？

FMOD 的 Bus 是树状结构（层级限制）：

```
Master Bus
├── Music
├── SFX
│   ├── UI
│   └── Environment
└── Dialogue
```

设置 `bus:/SFX` 的音量，只影响其自己与子 Bus。

#### VCA 如何打破层级限制？

你可以将多个不相关层级的 Bus，绑定到同一个 VCA：

- `vca:/UIVolume` 控制：
    - `bus:/SFX/UI`
    - `bus:/UI/Popup`

即便不在同一 Bus 分支下，VCA 依然能统一控制。

#### 示意结构：

```
Master Bus
├── Music
├── SFX
│   ├── UI
│   └── Gameplay
└── UI
    └── Popup
```

使用 VCA 实现统一 UI 音量滑块控制。
 ✅ 控制能力总结

|控制方式|受限于 Bus 层级|可跨层控制|
|---|---|---|
|**Bus**|✅ 是|❌ 否|
|**VCA**|❌ 否|✅ 是|

> ✅ VCA 是游戏中 UI 设置（音效、语音、背景音乐）音量滑块的首选方案。

## **FMOD Master Bank & Strings Bank 介绍**

### **🔹 1. Master Bank（主 Bank）**

- **Master Bank 是 FMOD 项目中的核心 Bank**，它**包含全局混音器（Global Mixer）**，用于管理整个项目的音频路由和音效输出。
- **所有事件实例（Event Instance）都依赖于 Master Bank**，即使事件本身的 `.bank` 文件已加载，**如果 Master Bank 没有加载，事件仍然无法播放**。

**📌 Master Bank 包含的内容**

|**组件**|**作用**|
|---|---|
|**Mixer（混音器）**|管理 Bus（总线），控制全局音量和效果|
|**Snapshots（快照）**|存储不同的混音状态，如战斗/探索模式|
|**Global Parameters（全局参数）**|控制整个游戏的音效，如环境音量、背景音乐强度|

 **📌 使用注意事项**

✅ **Master Bank 必须始终保持加载状态**，否则所有事件都会失效  
✅ **一般建议在游戏启动时加载 Master Bank**

**📌 代码示例：加载 Master Bank**

```csharp
using FMODUnity;
using UnityEngine;

public class FMODBankLoader : MonoBehaviour
{
    void Start()
    {
        RuntimeManager.LoadBank("Master");
        RuntimeManager.LoadBank("Master.strings"); // 需要加载字符串 Bank（见下方）
    }
}
```

### **🔹 2. Strings Bank（字符串 Bank）**

- **Strings Bank（字符串 Bank）存储了所有事件、Bus、参数的字符串路径到 GUID（全局唯一标识符）的映射**。
- FMOD **内部使用 GUID 访问事件**，但开发者通常用字符串路径（如 `"event:/Music/Background"`），Strings Bank 负责 **在运行时查找对应的 GUID**。

---

**📌 Strings Bank 的作用**

|**功能**|**描述**|
|---|---|
|**事件路径 → GUID 映射**|允许使用字符串访问事件，而不是手动维护 GUID|
|**Bus & Parameters 路径解析**|让 `RuntimeManager.GetBus("bus:/Music")` 正常工作|
|**减少 FMOD 内存占用**|仅存储字符串映射，不包含音频数据|

---

**📌 使用注意事项**

✅ **如果不加载 Strings Bank，使用字符串访问事件（如 `PlayOneShot("event:/Music/Theme")`）可能会失败**  
✅ **Strings Bank 仅包含映射信息，不包含音频数据，不会影响内存占用**

---

**📌 代码示例：从 GUID 获取事件**

```csharp
using FMOD.Studio;
using FMODUnity;
using UnityEngine;

public class FMODEventFromGUID : MonoBehaviour
{
    public string eventPath = "event:/SFX/Explosion";

    void Start()
    {
        // 通过字符串获取 GUID
        FMOD.GUID eventGUID;
        RuntimeManager.StudioSystem.lookupID(eventPath, out eventGUID);

        // 使用 GUID 创建事件
        EventInstance eventInstance;
        RuntimeManager.StudioSystem.createEventInstance(ref eventGUID, out eventInstance);

        eventInstance.start();
        eventInstance.release();
    }
}
```

### **🔹 3. 总结**

|**Bank 类型**|**作用**|**是否包含音频数据**|
|---|---|---|
|**Master Bank**|管理全局混音，包含 Bus、快照、参数|✅ 是|
|**Strings Bank**|事件路径与 GUID 映射|❌ 否|

📌 **Master Bank 负责全局音频混音，Strings Bank 让开发者可以用字符串访问事件。两者通常需要一起加载！🚀**


## **🔹 快照（Snapshot）及其机制**

**✅ 什么是快照（Snapshot）？**

- **快照（Snapshot）是 FMOD 提供的一种机制**，允许**在不同游戏状态下动态调整混音**。
- 它的作用类似于 **一组预设（Preset）**，可以同时修改 **多个 Bus（总线）的音量、效果参数、混响等**，并在运行时激活/停用。

**📌 快照的核心机制**

快照的机制类似于 **音频场景的切换**，可以在不同场景、游戏模式下调整音效。例如：

1. **进入战斗模式** → 提高战斗音效音量，降低环境音
2. **进入洞穴** → 增加混响，使声音更有空间感
3. **角色进入水下** → 启用低通滤波，让声音变得沉闷

### **🔹 快照的适用场景**

|**场景**|**作用**|
|---|---|
|**战斗模式切换**|提高战斗音效音量，降低环境音，增强紧张感|
|**室内/室外过渡**|进入洞穴时增加混响，进入房间时调整音量|
|**天气变化**|下雨时增加风声，降低背景音乐，调整环境氛围|
|**水下效果**|进入水下时应用低通滤波，让声音更闷，更符合现实感|
|**暂停游戏**|暂停时降低所有音效音量，营造静音或模糊的氛围|
|**角色受伤状态**|受伤时降低环境音，提高心跳或呼吸声，增强沉浸感|

**📌 快照的信号流向**

```text
[环境音 Bus] → [Master Bus] → [游戏音频输出]
[战斗音 Bus] → [Master Bus] 
[音乐 Bus] → [Master Bus]

(进入战斗) 快照 "BattleMode" → 提升 战斗音 Bus 音量, 降低环境音
(进入洞穴) 快照 "CaveReverb" → 增加混响, 降低高频
```

- 快照不会创建新 Bus，而是调整已有 Bus 的参数
- 多个快照可以同时生效，也可以互相过渡

```cs
public class FMODSnapshotController : MonoBehaviour
{
    private EventInstance snapshot;

    public void ActivateSnapshot()
    {
        snapshot = RuntimeManager.CreateInstance("snapshot:/BattleMode");
        snapshot.start();
    }

    public void DeactivateSnapshot()
    {
        snapshot.stop(FMOD.Studio.STOP_MODE.ALLOWFADEOUT);
    }
}
```

### **🔹 快照的总结**

|**功能**|**作用**|
|---|---|
|**快照（Snapshot）**|**用于动态调整多个 Bus 的参数，以适应不同的游戏状态**|
|**不会创建新 Bus**|**仅调整已有 Bus 的音量、混响、效果**|
|**支持多个快照**|**可同时生效，也可以互相过渡**|
|**适用场景**|**战斗模式、室内/室外过渡、天气变化、水下效果、暂停游戏、角色受伤状态等**|

📌 **快照可以极大增强游戏的沉浸感，合理使用可以让音效体验更加动态化，建议结合游戏场景需求进行优化！🚀**


## 🔹 什么是 UserData？

`UserData` 是 FMOD 提供的一种机制，允许你在播放某个事件时附带一段自定义数据（如字符串、结构体），并在 FMOD 回调中再次取回。

---

### 📌 示例代码

```csharp
// 设置 UserData
{
    string userData = "Hello User Data!";
    GCHandle handle = GCHandle.Alloc(userData);     // 告诉 GC：这个对象我要自己管理，别动它
    IntPtr pointer = GCHandle.ToIntPtr(handle);      // 转成原始 C 指针
    sound.setUserData(pointer);                      // 设置到 FMOD 事件实例
}

// 获取并释放 UserData
{
    IntPtr pointer;
    sound.getUserData(out pointer);                  // 获取 UserData 指针
    GCHandle handle = GCHandle.FromIntPtr(pointer);  // 还原托管对象句柄
    string userData = handle.Target as string;       // 获取实际对象
    Debug.Log(userData);
    handle.Free();                                   // 必须释放，防止内存泄漏
}
```

### 🧠 `GCHandle.Alloc()` 作用解释

- **将 C# 中的托管对象固定下来，防止 GC 垃圾回收或移动内存地址**
- 返回一个 `GCHandle` 结构，允许你通过 `ToIntPtr()` 获取指针形式传递到 FMOD

### ⚠️ 注意事项

|项目|描述|
|---|---|
|✅ 可传任意引用类型|如：`string`、`GameObject`、`class` 对象等|
|❌ 不建议传 struct|struct 会装箱成 object，可能导致访问麻烦|
|❗ 必须调用 `handle.Free()`|否则不会释放内存，可能导致内存泄漏|
|✅ 事件绑定唯一数据|每个 `EventInstance` 只能绑定一个 `UserData`|

### ✅ 总结一句话：

> `UserData` 通过 GCHandle 将托管对象转为原生指针绑定到 FMOD 事件中，常用于回调上下文、事件标记、性能分析等高级用途。

## 🔹 什么是延音点？

延音点（Sustain Point）是 FMOD 时间轴（Timeline）中的一个控制标记。  
当播放到延音点时，事件会暂停（或循环），直到程序调用 `keyOff()`，才会继续播放其后的内容。

它常用于控制音效中“等待触发继续”的逻辑，例如蓄力、等待操作、剧情推进等。

### 📌 常见使用场景

|场景|描述|
|---|---|
|蓄力技能音效|播放蓄力循环音，松手后播放释放音|
|UI 动画配音|等待动画完成后再播放收尾音|
|音乐演出结构控制|在剧情推进到某点后触发高潮音乐|

### 🔁 延音点 + Loop 区联合机制

FMOD 支持你将延音点设置在 loop 区末端：

```
[Intro] --> [Loop] 🔁 --> 🔷 延音点 --> [Release 结尾段]
```

当你调用 `keyOff()` 后，播放会跳出循环，从延音点继续播放 Release 段。

### 🧠 延音点播放逻辑

- 播放到延音点前：音频正常播放
- 播放到延音点：**暂停或循环**（取决于是否设置 loop）
- 调用 `eventInstance.keyOff()` 后：继续播放延音点之后的部分

### ✅ 示例代码（Unity）

```csharp
public class FMODSustainController : MonoBehaviour
{
    private EventInstance sustainEvent;

    public void StartChargingSound()
    {
        sustainEvent = RuntimeManager.CreateInstance("event:/Skill/Charge");
        sustainEvent.start();
        sustainEvent.release();
    }

    public void ReleaseChargeSound()
    {
        sustainEvent.keyOff(); // 触发延音点之后的播放
    }
}
```

### ⚠️ 延音点行为说明

|问题|说明|
|---|---|
|延音点不是播放起点|`keyOff()` 只让播放继续，并不会立刻跳到延音点|
|当前播放未到延音点|播放将继续走到延音点才跳出 loop|
|如果没设置 loop|播放将停在延音点，调用 `keyOff()` 后才继续|
|延音点后无内容|`keyOff()` 后播放可能立即结束|
|Loop+Sustain 必须正确位置|延音点必须在 loop 区间末尾才生效跳出行为|

### ❌ 延音点局限

如果你希望“释放技能时立刻播放释放音效”，延音点机制并不适合：

- 它不能立即跳出
- 只能等播放头自己走到 sustain 点

### ✅ 延音点适用总结

|控制目标|是否推荐使用延音点|
|---|---|
|精准释放动作同步|❌ 不推荐|
|渐进/节奏性过渡音效|✅ 推荐|
|音乐结构控制|✅ 推荐|
|剧情控制演出音效|✅ 推荐|

> 延音点适合需要“等待信号再继续”的长线音效控制，但如果需要毫秒级同步释放，推荐用独立事件实现控制。