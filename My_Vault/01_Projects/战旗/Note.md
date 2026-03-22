---
title: 战旗 半身像Panel与UI组件
date: 2026-03-16
tags:
  - project
  - game
  - unity
  - ui
type: project
aliases:
  - 战旗Note
  - 半身像
description: 战旗项目半身像Panel开发笔记：WorldArchitecturePanel、OsDialogWorldNormalPanel、BattlePanel、FightInfoPanel组件结构及LoadUICompImage资源加载机制
draft: false
---

# 战旗 半身像Panel与UI组件

**半身像出现panel**
draft: false
---

# Note

**半身像出现panel**

1. WorldArchitecturePanel  --- UIComponent --- 需要进行重写
	- WorldArchitectureNpcSVItem --- refreshNameIcon --- setSpriteSync --- UIComponent 
2. OsDialogWorldNormalPanel --- `showLeft/Right/MidHero` --- LoadUICompImage  lua 调用 c#

> 使用 `CharInfo` -- excel `CharInfoTable`

```lua
---@class CharInfo
---@field public ID integer 序号
---@field public Name string 角色名称
---@field public Spine string Spine图像
---@field public SpineScale integer Spine比例调整
---@field public SpineOffsetX integer Spine偏移X轴
---@field public SpineOffsetY integer Spine偏移Y轴
---@field public Painting string 角色全身像
---@field public PaintingScale integer Painting比例调整
---@field public PaintingOffsetX integer Painting偏移X轴
---@field public PaintingOffsetY integer Painting偏移Y轴
---@field public CardHeadImage string 方头像（英雄列表和战斗用）
---@field public CardHeadFightImage string 对冲准备的眼神遮罩特写
---@field public Sound_CharSelect string[] Demo期用_音频选中时随机一个放一次会被打断
---@field public Sound_CharDead string Demo期用_音频死亡时放一次会被打断
{ name = 'CharInfoTable', file = 'charinfotable', mode = 'map', index = 'ID', value_type = 'CharInfo' },

```

3. BattlePanel
	- vs_info
		- vsContent
			- lt_head --- LoadUICompImage
			- `#mask`  --- rt_head -- 同上




4. FightInfoPanel
	- left/right_panel -- `#mask` --- left/right_head  --- LoadUICompImage


*****

LoadUICompImage --- 

本质来说就是  
- 找到一个 Image 组件
- 然后进行填充
- 调用 ImageManager 中的函数进行资源读取 
- ? 需不需要一个东西专门进行管理



### 这里有两种资源

1. prefab + control 资源 
2. 图片资源