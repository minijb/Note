---
title: 通过  camera 实现物体的预览
date: 2026-03-16
tags:
  - untagged
type: knowledge
aliases:
  -
description: https://www.cnblogs.com/Jimm/p/5951362.html
draft: false
---

# 通过  camera 实现物体的预览

https://www.cnblogs.com/Jimm/p/5951362.html


有两种模式 ：

- 一种是使用 renderTexture + Material(Unit/Textre)
- 还有一种是手动编写， OnPostRender。获得 texture ReadPixel(从相机中读取数据到cpu)