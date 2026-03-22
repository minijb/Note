---
title: 三国杀 Trigger 触发器系统设计
date: 2026-03-16
tags:
  - project
  - game
  - lua
  - trigger
  - event-driven
type: project
aliases:
  - Trigger系统
  - 触发器设计
description: 三国杀游戏Trigger触发器系统设计：TriggerBase骨架、观察者模式（onBegin/onEnd/onTrigger）、模板方法模式、参数控制、触发限制
draft: false
---

# 三国杀 Trigger 触发器系统设计

## TriggerBase ： 为触发器提供骨架

<font color="#0070c0">三个主要观察者： </font>
- `onBeginTrigger`
- `onEndTrigger`
- `onTrigger`

<font color="#0070c0">状态控制</font>
```lua
self.isCanTrigger    -- 是否可触发（初始激活状态）
self.isTrigger       -- 是否已触发
self.triggerCount    -- 总触发次数
self.triggerTurnCount -- 回合内触发次数
```

**<font color="#0070c0">参数控制</font>
有4个参数，每个参数的类型都不一致。可以覆盖大部分情况
```c#
---@field public Parameter1 integer 类型参数1
---@field public Parameter2 integer[] 类型参数2
---@field public Parameter3 TwoParam[] 类型参数3
---@field public Parameter4 integer 类型参数4
```

<font color="#0070c0">触发限制</font>
```c#
-- 双重限制：总次数 + 回合内次数
if self.triggerCount > self.info.TriggerCountMax then return end
if self.triggerTurnCount > self.info.TurnTriggerCountMax then return end
```

<font color="#0070c0">模板方法模式</font>
- `DoAction()` 作为主流程模板
- `RealRunAction()` 由子类实现具体逻辑
- `Check()` 方法为抽象方法，强制子类实现条件检测 

## TriggerAction

<font color="#0070c0">单一职责</font>
playPerform -- 负责播放动画
RunAction -- 负责动作分发


<font color="#0070c0">动作分发器模式</font>
```lua
function RunAction(battle,actionId,...)
    local data = battle.dataMgr:GetData("BattleEventAction",actionId)
    local actionType = data.ActionType
    
    if actionType == CDataEnum.BattleEventActionType.PlayPerform then
        -- 特殊动画处理
    else
        -- 通用动作处理
    end
end
```

> 注意： TriggerAction 的具体内容并没有在这里，使用多个单独的类，将逻辑隔离出来。


## TriggerCreator 工厂模式

明确上下文 ： battle+triggerType
TriggerM : 作为触发器类型的注册中心

<font color="#0070c0">封装创建流程</font>
```lua
local function CreateTrigger(triggerClass, battle, triggerId, info)
    local t = triggerClass(battle)  -- 实例化
    t.id = triggerId               -- 设置ID
    t.info = info                  -- 注入配置
    t:init()                       -- 初始化
    return t
end
```