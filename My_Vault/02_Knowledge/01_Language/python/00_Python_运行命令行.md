---
title: Python 运行命令行
date: 2026-03-16
tags:
  - python
  - cli
type: language
aliases:
  Python命令行
description: Python运行命令行相关知识
draft: false
---

title: Python 运行命令行
date: 2026-03-16
tags:
  - knowledge
  - python
type: language
aliases:
  -
description: This module allows you to spawn processes, connect to their
draft: false
---

# Python 运行命令行

## subprocess

This module allows you to spawn processes, connect to their  
input/output/error pipes, and obtain their return codes.

run(...): Runs a command, waits for it to complete, then returns a  
          CompletedProcess instance.  
Popen(...): A class for flexibly executing a command in a new proces  --- 更加底层

## subprocess.run 详解

`subprocess.run(args, *, stdin=None, input=None, stdout=None, stderr=None, capture_output=False, shell=False, cwd=None, timeout=None, check=False, encoding=None, errors=None, text=None, env=None, universal_newlines=None)`

- args : list -- 参数列表 `["ls", "-al"]`
- stdin, stdout, stderr : 值可以是 subprocess.PIPE/DEVNULL, 一个已经存在的文件描述符，一个开大的文件对象，none
- timeout ： 超时时间
- encoding ： 指定的字符串属性
- shell ： 是否使用系统的shell执行
- cwd ： 起始的目录文职



https://docs.pythonlang.cn/3/library/subprocess.html

```python
def run_svn_command(self, cmd: List[str]) -> str:
	"""执行SVN命令并返回输出"""
	try:
		full_cmd = ["svn"] + cmd
		result = subprocess.run(
			full_cmd,
			cwd=self.repo_path,
			capture_output=True,
			text=True,
			encoding='utf-8',
			errors='ignore'
		)
		
		if result.returncode != 0:
			print(f"SVN命令执行失败: {' '.join(full_cmd)}")
			print(f"错误信息: {result.stderr}")
			sys.exit(1)
			
		return result.stdout
	except FileNotFoundError:
		print("错误：未找到svn命令，请确保SVN客户端已安装并添加到系统PATH")
		sys.exit(1)
	except Exception as e:
		print(f"执行命令时出错: {e}")
		sys.exit(1)
```