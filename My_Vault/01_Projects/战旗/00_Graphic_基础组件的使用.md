---
title: Unity Graphic 基础组件与 Mesh 重建
date: 2026-03-16
tags:
  - unity
  - ui
  - graphic
  - optimization
type: knowledge
aliases:
  - Graphic基础
  - Mesh重建
description: Unity Graphic组件注意事项：SetVerticesDirty触发Mesh重建，文字属性变化会导致Mesh重建，大量变动Text需注意性能
draft: false
---

# Unity Graphic 基础组件与 Mesh 重建

SetVerticesDirty --- 用于mesh 重建， 文字的以下属性进行变化都会进行Mesh重建，所以如果有大量需要经常变动的Text就要小心了。
draft: false
---

# Graphic    基础组件的使用

SetVerticesDirty --- 用于mesh 重建， 文字的以下属性进行变化都会进行Mesh重建，所以如果有大量需要经常变动的Text就要小心了。