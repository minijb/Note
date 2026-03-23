---
title: Windows WSL2 配置指南
date: 2026-03-23
tags:
  - type/cheatsheet
  - tool/wsl2
  - tool/windows
aliases:
  - WSL2速查
  - WSL配置
description: Windows WSL2 子系统安装、迁移与配置常用命令速查
draft: false
---

# Windows WSL2 配置指南

> **速查表** — WSL2 安装、迁移与配置

## 快速导航
- [安装 Linux 子系统](#安装-linux-子系统)
- [迁移到非系统盘](#迁移到非系统盘)
- [配置内存限制](#配置内存限制)
- [代理配置](#代理配置)

---

## 安装 Linux 子系统

```powershell
# 安装 WSL（会自动启用虚拟平台）
wsl --install

# 查看可用的 Linux 发行版
wsl --list --online

# 安装指定版本（如 Ubuntu）
wsl --install Ubuntu

# 列出已安装的版本
wsl -l -v
```

> **提示**：首次安装需要重启电脑

---

## 迁移到非系统盘

避免 WSL 占用 C 盘空间，迁移到其他分区：

```powershell
# ① 关闭所有 WSL 实例
wsl --shutdown

# ② 导出当前发行版为 tar 文件
wsl --export Ubuntu D:\ubuntu.tar

# ③ 注销原发行版
wsl --unregister Ubuntu

# ④ 在目标盘创建目录
mkdir E:\WSL\Ubuntu

# ⑤ 导入到新位置
wsl --import Ubuntu E:\WSL\Ubuntu D:\ubuntu.tar

# ⑥ 删除临时文件
del D:\ubuntu.tar

# ⑦ 验证结果
wsl -l -v
```

---

## 配置内存限制

WSL2 默认会占用大量内存，可通过 `.wslconfig` 限制。

**步骤**：

1. 打开文件资源管理器，地址栏输入 `%USERPROFILE%` 回车
2. 新建文件 `.wslconfig`（注意开头有点）
3. 用记事本写入以下内容：

```text
[wsl2]
memory=8GB
processors=4
swap=2GB
localhostForwarding=true
```

| 参数 | 说明 | 建议值 |
|------|------|--------|
| `memory` | WSL 最大内存 | 总内存的 50% |
| `processors` | WSL 最大 CPU 核数 | 4 |
| `swap` | 交换空间大小 | 2GB |
| `localhostForwarding` | 允许 localhost 访问 | true |

> **内存分配建议**：8GB 电脑设 4GB，16GB 设 8GB，32GB 设 16GB

保存后执行 `wsl --shutdown` 重启生效。

---

## 代理配置

在 Ubuntu 终端中执行：

```bash
# 获取 Windows 主机的 IP（WSL 网关地址）
export WIN_IP=$(ip route show default | awk '{print $3}')

# 设置代理（替换为你的代理端口）
export http_proxy=http://$WIN_IP:7890
export https_proxy=http://$WIN_IP:7890
```

 **常用代理端口**：
 
| 软件                                      | HTTP 代理端口 |
| --------------------------------------- | --------- |
| Clash / Clash Verge / Clash for Windows | 7890      |
| V2RayN                                  | 10809     |
| Shadowsocks                             | 1080      |

### 永久生效（可选）

将以下内容添加到 `~/.bashrc` 或 `~/.zshrc`：

```bash
export WIN_IP=$(ip route show default | awk '{print $3}')
export http_proxy=http://$WIN_IP:7890
export https_proxy=http://$WIN_IP:7890
```

---

## 相关资源

- [WSL 官方文档](https://docs.microsoft.com/zh-cn/windows/wsl/)
- [WSL2 GitHub](https://github.com/microsoft/WSL2)