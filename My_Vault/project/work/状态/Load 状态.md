---
title: Load 状态
date: 2026-03-16
tags:
  - untagged
type: knowledge
aliases:
  -
description: public enum UniGameLoadStep:int
draft: false
---

# Load 状态

```c#
public enum UniGameLoadStep:int
{
	//
	// MainInitBegin,
	// //插件初始化
	// PluginInit,
	//资源系统初始化
	InitAddressables,
	//初始资源初始化
	InitPreAsset,
	//游戏内资源加载
	InitGameAsset,
	//游戏初始化
	GameInitBeing,
	//下载作品数据
	LoadWork=GameInitBeing,
	//解析作品数据
	ParseWork,
	//启动游戏服务
	StartGameServer,
	//启动游戏服务
	StartGameClient,
	
	CreateGameNetPlayer,
	//请求房间信息
	EnterGameScene,
	//连接游戏服务
	ConnectGame,
	//加载作品场景
	LoadWorkScene,
	//加载游戏预设场景
	LoadGameScene,
	//加载相机系统
	LoadGameCameras,
	//加载用户界面
	LoadGameUI,
	//UserStore
	//LoadUserStore,
	//请求用户信息
	QueryPlayerInfo,
	//请求用户背包
	//QueryPlayerBag,
	//QuerySystemConfig,
	//初始化游戏内模块
	//InitGameModules,
	Count,
	None = Count
}

```