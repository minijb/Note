---
title: 三国杀 BattleTriggerComp 触发器管理
date: 2026-03-16
tags:
  - project
  - game
  - lua
  - trigger
type: project
aliases:
  - BattleTriggerComp
  - 触发器管理
description: 三国杀Battle中Trigger管理组件：triggers表管理、胜利/失败条件检查、触发器变量存储、LoadTrigger加载逻辑
draft: false
---

# 三国杀 BattleTriggerComp 触发器管理

Battle中用来管理 Trigger 的部分
draft: false
---

# project san BattleTriggerComp

Battle中用来管理 Trigger 的部分

使用到的变量及解释：

```lua
self.triggers = {}           -- 触发器实例表
self.VictoryConfCustom = {}   -- 自定义胜利条件ID列表
self.FailConfCustom = {}      -- 自定义失败条件ID列表
self.triggerVars = {}         -- 触发器变量存储
```

<font color="#0070c0">通常的胜利和失败条件</font>

```lua
local checkLostFuncs = {
    [CDataEnum.FailConditionType.TargetDie] = "CheckLostTargetDie",
	...
}

local checkWinFuncs = {
    [CDataEnum.VictoryConditionType.GeneralKill] = "CheckWinGeneralKill",
	...
}	
```

**添加Trigger**

```lua
---@param datas number[]
function BattleTriggerComp:LoadTrigger(datas)
    if nil == datas or #datas <= 0 then
        return
    end    
    local triggerTableData = self.dataMgr:GetDataTable("BattleEventTrigger")
    for i=1,#datas do
        local tID = datas[i]
        local triggerData = triggerTableData[tID]
        if nil ~= triggerData then
            local trigger = TriggerCreator(triggerData,self)
            trigger.onTrigger:AddObserver(self,self.onTrigger)
            trigger.onBeginTrigger:AddObserver(self,self.onBeginTrigger)
            trigger.onEndTrigger:AddObserver(self,self.onEndTrigger)
            self.triggers[triggerData.ID] = trigger
        else
            logError(string.format("tID:%d,not find in BattleEventTrigger",tID))
        end
    end
end
```

其他的都是普遍的通过 param的逻辑。