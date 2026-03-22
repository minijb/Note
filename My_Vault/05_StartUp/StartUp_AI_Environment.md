---
title: AI 环境搭建
date: 2026-03-21
tags:
  - type/tutorial
  - tool/claude-code
  - tool/ccswitch
aliases:
  - AI环境搭建
description: 个人主力AI环境搭建教程，包含 Claude Code 和 CCSwitch 配置
draft: false
---

# AI 环境搭建

> **教程** — 一步步配置 AI 开发环境

## 前置要求
- Node.js 环境（通过 NVM 管理）
- 国内网络（需要代理）

## 工具清单

| 工具 | 用途 | 链接 |
|------|------|------|
| CCSwitch | 跨平台 AI API 切换 | [GitHub](https://github.com/farion1231/cc-switch/blob/main/README_ZH.md) |
| Claude Code | AI 编程助手 | [官方](https://claude.ai/code) |
| MiniMax | AI 模型提供商 | [官网](https://platform.minimax.com) |

## 步骤

### 第一步：安装 Claude Code CLI

```bash
# 安装 Node 环境（使用 NVM）
# 参考：[[StartUp_常用工具Tool_NVM]]

# 全局安装 Claude Code
npm install -g @anthropic-ai/claude-code
```

### 第二步：配置 CCSwitch

1. 下载安装 CCSwitch
2. 在设置中添加 Claude Code 栏位
3. 开启代理功能
4. 配置 AI API Key（推荐 MiniMax）

### 第三步：验证结果

```bash
# 检查 Claude Code 是否安装成功
claude --version

# 验证 CCSwitch 代理是否生效
ccswitch status
```

## 常见问题

| 问题 | 解决方案 |
|------|----------|
| 安装慢 | 使用淘宝镜像或代理 |
| 代理不生效 | 检查 CCSwitch 设置中的代理开关 |
| API Key 无效 | 确认 MiniMax 账号余额充足 |

## 相关资源

- [[StartUp_常用工具_NVM]] — NVM Node 版本管理
