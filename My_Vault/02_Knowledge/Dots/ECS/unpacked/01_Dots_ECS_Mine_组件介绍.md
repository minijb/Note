---
title: ECS 组件介绍
date: 2026-03-16
tags:
  - unity
  - dots
  - ecs
  - component
type: framework
aliases:
  组件
description: ECS组件介绍
draft: false
---


## 1. Entity 实体

实体代表程序中独立存在的、拥有独立数据集的事物。
**本质** 就是个 ID， 将和具体物体关联起来。

实体集合存在于 `World` 中， `EntityManager` 管理所有的 Entity

常见方法

| **方法**            | **描述**            |
| ----------------- | ----------------- |
| `CreateEntity`    | 创建新实体。            |
| `Instantiate`     | 复制现有实体并从该副本创建新实体。 |
| `DestroyEntity`   | 摧毁一个现有的实体。        |
| `AddComponent`    | 将组件添加到现有实体。       |
| `RemoveComponent` | 从现有实体中删除组件。       |
| `GetComponent`    | 检索实体组件的值。         |
| `SetComponent`    | 覆盖实体组件的值。         |

## 2. Componet 组件

存储具体的数据

使用[`IComponentData`](https://docs.unity3d.com/Packages/com.unity.entities@1.4/api/Unity.Entities.IComponentData.html)没有方法的接口将结构体标记为组件类型。此组件类型只能包含非托管数据，并且可以包含方法，但最佳做法是将它们设置为纯数据。如果要创建托管组件，请将其定义为类


### 2.1 组件类型

| **Component**                                                                                                       | **描述**                                                                                                                                 |
| ------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| [Unmanaged components](https://docs.unity3d.com/Packages/com.unity.entities@1.4/manual/components-unmanaged.html)   | 最常见的组件类型，但只能存储某些类型的字段。                                                                                                                 |
| [Managed components](https://docs.unity3d.com/Packages/com.unity.entities@1.4/manual/components-managed.html)       | 可以存储任何字段类型的托管组件类型。                                                                                                                     |
| [Shared components](https://docs.unity3d.com/Packages/com.unity.entities@1.4/manual/components-shared.html)         | 根据实体的值将实体分组的组件。                                                                                                                        |
| [Cleanup components](https://docs.unity3d.com/Packages/com.unity.entities@1.4/manual/components-cleanup.html)       | 当你销毁一个包含清理组件的实体时，Unity 会移除所有非清理组件。这对于标记销毁时需要清理的实体非常有用。                                                                                 |
| [Tag components](https://docs.unity3d.com/Packages/com.unity.entities@1.4/manual/components-tag.html)               | 非托管组件，不存储任何数据，也不占用任何空间。您可以在[实体查询](https://docs.unity3d.com/Packages/com.unity.entities@1.4/manual/systems-entityquery-intro.html)过滤实体。 |
| [Buffer components](https://docs.unity3d.com/Packages/com.unity.entities@1.4/manual/components-buffer.html)         | 充当可调整大小数组的组件。                                                                                                                          |
| [Chunk components](https://docs.unity3d.com/Packages/com.unity.entities@1.4/manual/components-chunk.html)           | 存储与整个块（而不是单个实体）关联的值的组件。                                                                                                                |
| [Enableable components](https://docs.unity3d.com/Packages/com.unity.entities@1.4/manual/components-enableable.html) | 可以在运行时在实体上启用或禁用的组件，无需进行昂贵的结构更改。                                                                                                        |
| [Singleton components](https://docs.unity3d.com/Packages/com.unity.entities@1.4/manual/components-singleton.html)   | 在给定世界中仅有一个实例的组件。                                                                                                                       |

## 3. system 系统

系统提供将[组件](https://docs.unity3d.com/Packages/com.unity.entities@1.4/manual/concepts-components.html)数据从当前状态转换为下一个状态的逻辑。例如，系统**可能**会将所有移动实体的位置更新为其速度乘以自上次更新以来的时间间隔。


系统每帧在主线程上运行一次。系统被组织成系统组的层次结构，您可以使用这些层次结构来组织系统更新的顺序。

您可以在实体中创建非托管系统或托管系统。要定义托管系统，请创建一个继承自的类[`SystemBase`](https://docs.unity3d.com/Packages/com.unity.entities@1.4/api/Unity.Entities.SystemBase.html)。要定义非托管系统，请创建一个继承自 的结构体[`ISystem`](https://docs.unity3d.com/Packages/com.unity.entities@1.4/api/Unity.Entities.ISystem.html)。有关更多信息，请参阅[系统概述](https://docs.unity3d.com/Packages/com.unity.entities@1.4/manual/systems-intro.html)。和`ISystem`都有`SystemBase`三种方法可以覆盖：`OnUpdate`、`OnCreate`和`OnDestroy`。系统的`OnUpdate`方法每帧执行一次。

一个系统只能处理一个[世界](https://docs.unity3d.com/Packages/com.unity.entities@1.4/manual/concepts-worlds.html)中的实体，因此一个系统与一个特定的世界相关联。您可以使用该[`World`](https://docs.unity3d.com/Packages/com.unity.entities@1.4/api/Unity.Entities.ComponentSystemBase.World.html#Unity_Entities_ComponentSystemBase_World)属性返回系统所附加的世界。

默认情况下，自动引导过程会为每个系统和系统组创建一个实例。引导过程会创建一个包含三个系统组的默认环境：`InitializationSystemGroup`、`SimulationSystemGroup`和`PresentationSystemGroup`。默认情况下，系统实例会添加到`SimulationSystemGroup`。您可以使用`[UpdateInGroup]`属性覆盖此行为。

要禁用自动引导过程，请使用脚本定义`#UNITY_DISABLE_AUTOMATIC_SYSTEM_BOOTSTRAP`。


### 3.1 系统类型

您可以使用多种类型的系统：

- [`SystemBase`](https://docs.unity3d.com/Packages/com.unity.entities@1.4/manual/systems-systembase.html)：为托管系统提供基类。
- [`ISystem`](https://docs.unity3d.com/Packages/com.unity.entities@1.4/manual/systems-isystem.html)：为非托管系统提供接口。
- [`EntityCommandBufferSystem`](https://docs.unity3d.com/Packages/com.unity.entities@1.4/manual/systems-entity-command-buffers.html)：为其他系统提供实体命令缓冲区实例。这允许您将[结构更改](https://docs.unity3d.com/Packages/com.unity.entities@1.4/manual/concepts-structural-changes.html)组合在一起，以提高应用程序的性能。
- [`ComponentSystemGroup`](https://docs.unity3d.com/Packages/com.unity.entities@1.4/api/Unity.Entities.ComponentSystemGroup.html)：为系统提供嵌套的组织和更新顺序。

### 3.2系统组

系统组可以包含系统组和其他系统组作为其子组。系统组具有一个可重写的更新方法，其基本方法会按排序顺序更新该组的子组。


## 4. world 世界

为 entities 的集合 。 同时一个 entity 的id 在 world 中唯一， 同时含有一个 `EntityManager` 的 结构体， 用来创建，销毁，修改 entity。

一个 world 含有多个 system， 一个世界拥有一组[系统](https://docs.unity3d.com/Packages/com.unity.entities@1.4/manual/concepts-systems.html)，这些系统通常只访问同一个世界内的实体。此外，一个世界内具有相同组件类型的一组实体会存储在一个[原型](https://docs.unity3d.com/Packages/com.unity.entities@1.4/manual/concepts-archetypes.html)中，原型决定了程序中组件在内存中的组织方式。


### 4.1 初始化

默认情况下， 在进入游戏后，Unity会自动创建一个 World 并加入所有的 sysytem。

如果您希望手动将系统添加到默认世界，请创建一个实现[ICustom Bootstrap](https://docs.unity3d.com/Packages/com.unity.entities@1.4/api/Unity.Entities.ICustomBootstrap.html)接口的单个​​类。

如果您想要完全手动控制引导，请使用这些定义来禁用默认的世界创建：

- `#UNITY_DISABLE_AUTOMATIC_SYSTEM_BOOTSTRAP_RUNTIME_WORLD`：禁用默认运行时世界的生成。
- `#UNITY_DISABLE_AUTOMATIC_SYSTEM_BOOTSTRAP_EDITOR_WORLD`：禁用默认编辑器世界的生成。
- `#UNITY_DISABLE_AUTOMATIC_SYSTEM_BOOTSTRAP`：禁用两个默认世界的生成。

然后，您的代码将负责创建您的世界和系统，并将世界的更新插入到 Unity 可编写脚本的[Player Loop](https://docs.unity3d.com/ScriptReference/LowLevel.PlayerLoop.html)中。有关如何管理多个世界中的系统的更多信息，请参阅[管理多个世界中的系统](https://docs.unity3d.com/Packages/com.unity.entities@1.4/manual/systems-icustombootstrap.html)。

Unity 用于[`WorldFlags`](https://docs.unity3d.com/Packages/com.unity.entities@1.4/api/Unity.Entities.WorldFlags.html)在编辑器中创建专门的世界。



## 5. archetype 原型

原型是世界中所有具有相同唯一组件类型组合的实体的唯一标识符


For example, in the following diagram, all the entities in a world that have the components `Speed`, `Direction`, `Position`, and `Renderer` and no others share the archetype labelled `X`. All the entities that have component types `Speed`, `Direction`, and `Position` and no others share a different archetype labelled `Y`.

![image.png](https://s2.loli.net/2025/10/15/7oH9nAp3KIU2ifQ.png)
当你在实体中添加或移除组件类型时，世界会将[`EntityManager`](https://docs.unity3d.com/Packages/com.unity.entities@1.4/api/Unity.Entities.EntityManager.html)实体移动到相应的原型。例如，如果一个实体包含组件类型`Speed`、`Direction`和 ，`Position`而你移除了该`Speed`组件，世界会将实体移动到包含组件和 的`EntityManager`原型。如果不存在这样的原型，世界会创建它。`Direction``Position``EntityManager`

基于原型的实体组织方式意味着按组件类型查询实体非常高效。例如，如果您想查找所有包含组件类型 A 和 B 的实体，您可以找到所有包含这些组件类型的原型，这比扫描所有单个实体更高效。世界中现有的原型集合往往在程序生命周期的早期趋于稳定，因此您可以缓存查询以获得更快的性能。

原型只有在其世界被毁灭时才会被毁灭。

### 5.1 原型块

所有具有相同原型的实体和组件都存储在统一的内存块中，这些内存块称为“块”。每个块包含 16 KiB，其可存储的实体数量取决于块原型中组件的数量和大小。系统会[`EntityManager`](https://docs.unity3d.com/Packages/com.unity.entities@1.4/api/Unity.Entities.EntityManager.html)根据需要创建和销毁块。

每个块包含一个用于存储每种组件类型的数组，以及一个用于存储实体 ID 的附加数组。例如，在包含组件类型 A 和 B 的原型中，每个块包含三个数组：一个用于存储 A 组件值的数组，一个用于存储 B 组件值的数组，以及一个用于存储实体 ID 的数组。

块的数组是紧密排列的：块的第一个实体存储在这些数组的索引 0 处，块的第二个实体存储在索引 1 处，后续实体存储在连续的索引处。当新实体添加到块中时，它会存储在第一个可用的索引处。当实体从块中移除时（无论是因为被销毁还是被移动到其他原型），块的最后一个实体都会被移动以填补空缺。

当一个实体被添加到一个原型时，`EntityManager`如果原型的现有区块已满，则会创建一个新的区块。当最后一个实体从区块中移除时，则会`EntityManager`销毁该区块。

有关如何管理块内存的信息，请参阅[管理块分配](https://docs.unity3d.com/Packages/com.unity.entities@1.4/manual/performance-chunk-allocations.html)


## 6. 结构变化概念

导致 Unity 重新组织[内存块](https://docs.unity3d.com/Packages/com.unity.entities@1.4/manual/concepts-archetypes.html#archetype-chunks)或内存块内容的操作称为**结构性更改**。了解哪些操作属于结构性更改非常重要，因为它们可能占用大量资源，并且只能在主线程上执行，而不能在作业中执行。

以下操作被视为结构变化：

- 创建或销毁一个[实体](https://docs.unity3d.com/Packages/com.unity.entities@1.4/manual/concepts-entities.html)。
- 添加或删除[组件](https://docs.unity3d.com/Packages/com.unity.entities@1.4/manual/concepts-components.html)。
- 设置共享组件值。

您可以通过多种方式管理项目的结构变更。有关更多信息，请参阅[管理结构变更](https://docs.unity3d.com/Packages/com.unity.entities@1.4/manual/systems-manage-structural-changes.html)

**创建实体**

当您创建一个实体时，Unity 要么将该实体添加到现有的块中，要么如果没有可用于该实体[原型的](https://docs.unity3d.com/Packages/com.unity.entities@1.4/manual/concepts-archetypes.html)块，则创建一个新块并将实体添加到该块中。

**摧毁一个实体**

销毁实体时，Unity 会将该实体从其所在的块中移除。如果移除实体后在块中留下空隙，Unity 会移动块中的最后一个实体来填补该空隙。如果移除实体后块中留空，Unity 会释放该块。

**添加或删除组件**

当您在实体中添加或移除组件时，您会更改实体的原型。Unity 将每个实体存储在与实体原型匹配的块中。这意味着，如果您更改实体的原型，Unity 必须将该实体移动到另一个块。如果不存在合适的块，Unity 会创建一个新的块。如果移动操作导致前一个块出现空隙或空着，Unity 会移动块中的最后一个实体来填补空隙，或者释放该块。

**设置共享组件值**

当您设置实体[共享组件](https://docs.unity3d.com/Packages/com.unity.entities@1.4/manual/components-shared.html)的值时，Unity 会将该实体移动到与新共享组件值匹配的块。如果不存在合适的块，Unity 会创建一个新的。如果移动操作导致前一个块出现空隙或为空，Unity 会移动块中的最后一个实体以填补空隙，或者释放该块。

```ad-note
启动和禁用组件不算作结构性变化
```
### 6.1 同步点

您不能直接在 job 中进行结构更改，因为这可能会使已经安排的其他 job 无效，并创建同步点（sync point）。

同步点是程序执行过程中的一个点，它会在主线程上等待迄今为止已调度的所有作业完成。同步点会在一段时间内限制您使用作业系统中所有可用工作线程的能力。因此，您应该尽量避免同步点。

ECS 中数据的结构变化是导致同步点的主要原因。有关如何避免同步点的信息，请参阅[管理同步点](https://docs.unity3d.com/Packages/com.unity.entities@1.4/manual/performance-sync-points.html)。


## 7. 安全问题

1. Entities API 将数据存储在通常通过[作业系统](https://docs.unity3d.com/6000.0/Documentation/Manual/JobSystem.html)或主线程访问的块中。作业系统通常负责处理通过 NativeContainers 传入的所有数据的安全性，并使用符号标记数据是读取、写入还是两者兼而有之。但是，任何导致结构更改的 API 都可能导致这些数据在内存中移动，并使对该数据的任何引用失效。

2. 一般来说，所有结构更改都必须在主线程上使用世界的 进行`EntityManager`。此`ExclusiveEntityTransaction`功能允许您暂时将 置于`EntityManager`一种模式，其中单个工作线程（运行`IJob`）可以安全地对该世界的实体执行结构更改操作，从而使主线程可以自由地执行其他工作。

此功能的主要目的是允许辅助/流式世界安全地修改其实体并执行结构更改，而不会阻止主线程处理默认世界中的实体。它并非旨在作为`EntityManager`工作线程功能的完全通用接口。某些`EntityManager`操作在其实现中依赖于仅限主线程的功能，因此如果从作业代码中调用，将无法正常运行。官方仅支持直接公开的部分操作`ExclusiveEntityTransaction`。