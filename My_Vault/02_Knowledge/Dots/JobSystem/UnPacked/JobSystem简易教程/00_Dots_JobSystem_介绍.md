---
title: JobSystem 介绍
date: 2026-03-16
tags:
  - unity
  - dots
  - job-system
type: framework
aliases:
  JobSystem介绍
description: Unity JobSystem介绍
draft: false
---


### Dots

JobSytem : 多线程系统
Burst ： Burst llvm 的后端编译器 --- 很多代码都可以编译，但是有限定
Entity Component System ： 实体组件系统


### ECS

Entity-Component-System 分离数据及行为，优化内存布局，提高缓存利用率

1. Entity ID: 不包含任何数据和逻辑 用来标记组件是否属于同一事物
2. Component ： 纯粹的数据，没有任何方法， 在unity中就是 实现 `IComponentData` 接口的 Struct
3. System ： 纯粹的逻辑， 不存储任何数据， 系统会持续遍历特定组件组合的所有 实体，并根据这些数据执行操作。
	1. MovementSystem ， 会遍历所有 PositionComponet 和 VelocityComponent 实体，并在每一帧根据速度跟新它们的位置

### JobSystem 

可以在 非 Dots 环境下使用

