---
title: ECS Entities
date: 2026-03-16
tags:
  - unity
  - dots
  - ecs
  - entities
type: framework
aliases:
  Entities
description: ECS Entities实体
draft: false
---


## 1. 是什么？

Entities是实体组件系统体系结构的三个主要元素之一。它们代表游戏或应用程序中的各个“事物”。`Entities既没有行为也没有数据；取而代之的是，它担任索引各种数据的职责。Systems提供行为，而Components存储数据。`


本质就是一个 ID。 没有类型的区分， 但是可以根据含有的 components 进行分组。EntityManager会持续跟踪监控entities上components的唯一组合。这种独特的组合称为`Archetype（原型）`。

可以根据EntityArchetype创建符合原型的entities， 也可以先创建 EntityArchetype 然后用它来创建 entities。

## 2. 创建 entities

使用EntityManager.CreateEntity函数创建一个实体。ECS在与EntityManager相同的world中创建entities。

您可以通过以下方式一个接一个的创建实体：

- 使用ComponentType对象数组创建一个包含多个component的entity。
- 使用一个EntityArchetype创建一个包含多个component的entity。
- 使用Instantiate复制现有entity，包括其当前数据。
- 创建一个没有components的entity，然后向其添加components。（您可以立即添加components，也可以在需要其他components时添加。）

您也`可以一次创建多个实体`：

- CreateEntity：使用具有相同archetype的新entities填充NativeArray。
- Instantiate：通过现有entities的副本，包括其当前数据来填充NativeArray。
- CreateChunk：显式创建由指定数量的并给定archetype的entities填充的chunks。

