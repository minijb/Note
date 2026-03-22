---
title: 三国杀 Battle 战斗系统架构
date: 2026-03-16
tags:
  - project
  - game
  - lua
  - architecture
type: project
aliases:
  - Battle系统
  - 战斗架构
description: 三国杀游戏Battle战斗系统架构：组合优于继承、单一职责、多层级状态机、阵营管理、多随机数设计、实体管理
draft: false
---

# 三国杀 Battle 战斗系统架构

## Battle -- 总文件

- **组合优于继承**：通过 `class.AddComponents` 将14个功能组件组合到Battle类中，Battle.lua 就是用来协调各个系统的
- **单一职责**：每个组件负责特定领域（地图、触发器、回合、Buff、战斗等）
- **松耦合**：组件间通过事件系统通信，避免直接依赖

<font color="#0070c0">多层级状态管理</font>

```lua
-- 主状态机管理战斗流程
self.mainStateMgr:AddState("StateNone", ...)
self.mainStateMgr:AddState("ArrangeState", ...)  -- 布阵阶段
self.mainStateMgr:AddState("FieldState", ...)     -- 战场阶段  
self.mainStateMgr:AddState("FightState", ...)    -- 战斗阶段
```

<font color="#0070c0">阵营管理</font>
```lua
-- 5种阵营类型支持复杂战斗场景
self.teams:set(Enum.Team.None, BattleTeam(Enum.Team.None, self))    -- 无阵营，旁观
self.teams:set(Enum.Team.Self, BattleTeam(Enum.Team.Self, self))    -- 我方
self.teams:set(Enum.Team.Friend, BattleTeam(Enum.Team.Friend, self)) -- 友方
self.teams:set(Enum.Team.Enemy, BattleTeam(Enum.Team.Enemy, self))  -- 敌方
self.teams:set(Enum.Team.Hide, BattleTeam(Enum.Team.Hide, self))     -- 隐藏
```

### 核心功能

<font color="#0070c0">多随机数设计</font>
```lua
-- 4种独立的随机数生成器，避免随机污染
self.battleRandom = Random("battleRandom", self, true)      -- 战斗逻辑随机
self.aiRandom = Random("aiRandom", self, true)              -- AI决策随机  
self.autoBattleRandom = Random("autoBattleRandom", self, false) -- 托管随机
```

<font color="#0070c0">实体管理</font>
```lua
-- 多层级的实体查找机制
function Battle:GetEntityById(id)           -- 全局查找
function Battle:GetEntityByTeamTypeAndId(teamType, id, containDestroy)  -- 按队伍查找
function Battle:GetHeroByConfigID(teamType, configId)  -- 按配置ID查找
```

