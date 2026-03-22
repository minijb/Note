---
title: 战旗 嘴型动画 tips
date: 2026-03-16
tags:
  - project
  - game
  - animation
  - lipsync
type: project
aliases:
  嘴型tips
description: 战旗项目嘴型动画tips
draft: false
---


## 1. 捕获音频

1. Unity 自带的 : [OnAudioFilterRead](https://docs.unity.cn/cn/2019.4/ScriptReference/MonoBehaviour.OnAudioFilterRead.html)
	 只能捕获全局混合后声音
2. FMod 捕获：
	 可以捕获单独声道的声音


## 2. 声谱数据获取


Unity 提供的结构 ：  提供当前播放音频源的频谱数据块

AudioSource.GetSpectrumData ， [AudioSource.GetOutputData](https://docs.unity.cn/cn/current/ScriptReference/AudioSource.GetOutputData.html)、[AudioListener.GetSpectrumData](https://docs.unity.cn/cn/current/ScriptReference/AudioListener.GetSpectrumData.html)、[AudioListener.GetOutputData](https://docs.unity.cn/cn/current/ScriptReference/AudioListener.GetOutputData.html)。

提供当前播放音频源的频谱数据块。

将向 samples 参数指定的数组填充请求的数据。  
  
值的数量（提供的样本数组的长度）必须为 2 的幂数，即 128/256/512 等。最小值为 64，最大值为 8192。 使用 [window](https://docs.unity.cn/cn/current/ScriptReference/FFTWindow.html) 可减少频点/频带之间的泄漏。 注意，窗口类型越复杂，音质越好，但会降低速度。

**window** 为映射方法。

