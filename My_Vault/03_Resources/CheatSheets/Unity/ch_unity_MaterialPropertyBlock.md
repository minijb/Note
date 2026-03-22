---
title: ch unity MaterialPropertyBlock
date: 2026-03-16
tags:
  - resource
  - unity
type: knowledge
aliases:
  -
description: 直接使用 `render.material.SetColor()` 会生成大量的材质对象，提升内存的占用，并且还会打断物体的合批操作，在少量物体时可以用这种方法。
draft: false
---

# ch unity MaterialPropertyBlock

直接使用 `render.material.SetColor()` 会生成大量的材质对象，提升内存的占用，并且还会打断物体的合批操作，在少量物体时可以用这种方法。