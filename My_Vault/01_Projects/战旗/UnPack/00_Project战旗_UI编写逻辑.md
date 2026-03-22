---
title: 战旗 UI编写逻辑
date: 2026-03-16
tags:
  - project
  - game
  - unity
  - ui
type: project
aliases:
  战旗UI
description: 战旗项目UI编写逻辑
draft: false
---


## 绑定


两个对象 ：  
1. control  --- 具体的 gameobject
2. component --- 为lua提供所有的组件功能 如添加点击时间，设置文字

两个一一对应，**根据命名规则自动绑定** --- 生成 `bindGoObj.lua.txt` 的xlua 热更文件。 


## 具体逻辑

1. 位置 `Script/Lua/Client/UI/{PanelName}/{PanelName}.lua`
2. excel 导表 ： 从 GameData 中拿到信息即可
