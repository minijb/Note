---
title: WSL 常用命令速览表
date: 2026-03-23
tags:
  - type/cheatsheet
  - tool/wsl2
  - tool/windows
aliases:
  - WSL速查
description: WSL (Windows Subsystem for Linux) 常用命令速查
draft: false
---

# WSL 常用命令速览表

> **速查表** — WSL 日常使用命令

## 安装与管理

| 命令 | 说明 |
|------|------|
| `wsl --install` | 安装 WSL（需管理员权限） |
| `wsl --list --online` | 查看可安装的 Linux 发行版 |
| `wsl --install <name>` | 安装指定发行版 |
| `wsl --list -v` | 列出已安装的发行版 |
| `wsl --update` | 更新 WSL 内核 |
| `wsl --shutdown` | 关闭所有 WSL 实例 |

## 实例操作

| 命令 | 说明 |
|------|------|
| `wsl -d <name>` | 启动指定发行版 |
| `wsl -t <name>` | 终止指定发行版 |
| `wsl --unregister <name>` | 注销并删除指定发行版 |
| `wsl -e bash -c "cmd"` | 不进入 shell 直接执行命令 |

## 导入与导出

| 命令 | 说明 |
|------|------|
| `wsl --export <name> <file>` | 导出发行版为 tar 文件 |
| `wsl --import <name> <path> <file>` | 从 tar 文件导入发行版 |

## WSL 内命令（进入子系统后）

```bash
# 查看 IP 地址
ip addr

# 查看系统信息
uname -a

# 查看磁盘使用
df -h

# 查看内存使用
free -h

# 在 Windows 中打开当前目录
explorer.exe .
```

## 常见问题

| 问题 | 解决方案 |
|------|----------|
| WSL 无法启动 | 以管理员身份运行 `wsl --shutdown` 后重试 |
| 内存占用过高 | 编辑 `%USERPROFILE%\.wslconfig` 限制内存 |
| 无法访问 localhost | 确保 `localhostForwarding=true` 在 .wslconfig 中 |
| 磁盘空间不足 | 使用 `wsl --export` 迁移到其他分区 |

---

## 相关资源

- [[StartUp_Windows_wsl2]] — WSL2 完整配置指南
- [WSL 官方文档](https://docs.microsoft.com/zh-cn/windows/wsl/)
