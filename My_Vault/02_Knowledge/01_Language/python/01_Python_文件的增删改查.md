---
title: Python 文件操作
date: 2026-03-16
tags:
  - python
  - file
  - io
type: language
aliases:
  Python文件操作
description: Python文件增删改查操作
draft: false
---

title: Python 文件的增删改查
date: 2026-03-16
tags:
  - knowledge
  - python
type: language
aliases:
  -
description: 主要包含两个库文件 `shutil, os`
draft: false
---

# Python 文件的增删改查

主要包含两个库文件 `shutil, os`

- 复制 ： 
  - `shutil.copy(src, dest)` 复制文件
  - `shutil.copytree(src, dest)` 复制文件夹  
- 移动
  - `shutil.move(src, dest)`
- 删除
  - `os.unlink(dest)` 删除文件
  - `os.rmdir(dest)`
  - `os.rmtree(dest)`
- 创建文件夹
  - `os.makedirs(dest, exist_ok=True)` exist_ok : 是否递归的创建