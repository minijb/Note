---
title: 三国杀 TriggerAction 动作系统
date: 2026-03-16
tags:
  - project
  - game
  - lua
  - trigger
  - action
type: project
aliases:
  - TriggerAction
  - 动作系统
description: 三国杀TriggerAction动作系统：TriggerActionBase基类设计、17种动作类型（PlayPerform/SwitchAi/AddBuff等）、TriggerActionManager执行器
draft: false
---

# 三国杀 TriggerAction 动作系统

TriggerActionBase Trigger行为的基类

**定义**

```lua
---@class TriggerActionBase:Class
---@field public id number              -- 动作ID
---@field public actionType number      -- 动作类型枚举
---@field public data BattleEventAction -- 配置数据
---@field public battle Battle          -- 战斗实例引用
---@field public isCompleted boolean    -- 是否完成标记
---@field public P1 number              -- 参数1：数值型
---@field public P2 number[]            -- 参数2：数组型
---@field public P3 BEventAction3[]     -- 参数3：复杂结构数组
---@field public P4 number              -- 参数4：数值型
---@field public P5 string              -- 参数5：字符串型
local TriggerActionBase = class.Class("TriggerActionBase", nil, false)

```

两个抽象接口： Play， Stop 子类必须实现。

配合对象池做出了设计： `self.isCompleted = false` 

TriggerActionBase (基类)
    ├── PlayPerformAction      -- 播放表演
    ├── SwitchAiAction         -- 切换AI
    ├── SetVariableAction      -- 设置变量
    ├── AddBuffAction          -- 添加Buff
    ├── RemoveBuffAction       -- 移除Buff
    ├── GetItemAction          -- 获得物品
    ├── ReplaceAction          -- 替换单位
    ├── ResultSwitchAction     -- 结果切换
    ├── TargetActionValueAction-- 目标行动值
    ├── PlayEfMarkAction       -- 播放特效标记
    ├── GeneralUseBFSkillAction-- 将领使用战场技能
    ├── RemoveEfAction         -- 移除特效
    └── ChangeSidesAction      -- 切换阵营


## TriggerActionManager

立即执行的配置列表

```lua
local NeedRunNow ={
    [BEAT.PlayPerform]  = false,    -- 播放表演
    [BEAT.SwitchAi] = false,        -- 切换AI
    [BEAT.ActionStateSwitch] = true,-- 状态切换（立即执行）
    [BEAT.SetVariable] = true,      -- 设置变量（立即执行）
    [BEAT.AddVariable] = true,      -- 添加变量（立即执行）
    -- ... 共17种动作类型
}
```

<font color="#0070c0">动作执行</font>

```lua
function TriggerActionManager:DoAction(callback)
    -- 1. 检查队列是否为空
    -- 2. 设置回调和播放状态
    -- 3. 切换到ActionState状态
    -- 4. 取出第一个动作ID并执行
end

function TriggerActionManager:DoActionList(actList,callback)
```

```lua
function TriggerActionManager:DoActionInClient(id)
    -- 根据NeedRunNow配置决定执行方式
    -- true: 立即执行并存入actionQueue
    -- false: 存入actionIdQueue等待顺序执行
end

function TriggerActionManager:DoActionImmediate(id)
```




