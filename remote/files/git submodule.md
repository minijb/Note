---
tags:
  - git
---
## 添加一个submodule

```sh
git submodule add {url} {path}
```

## submodule 提交更新

- 直接在子文件夹中进行提交

## submodule 拉取更新

- 子文件夹 ： `git pull`
- 在主目录中 : `git submodule update --remote [submodule文件夹相对路径]`
	- 没有路径则更新所有的 submodule
	- 当我们更新子项目后，相当于是把主项目记录的 submodule 的 commit id 给更新了，需要提交下主项目的变更。
- 在主目录执行 `git submodule update [submodule文件夹相对路径]` -- 根据 submodule 中的id进行更新
	- 注意，这个方法会使 submodule 的分支处于主项目里指定的 commit id。可能并不是拉 submodule 的 master 最新代码。
	- 所以，这种方法仅适用于，当主仓库里记录的 submodule 的 commit id 已经是最新的（可能被其他同事提交过）。或者你期望 submodule 跟主仓库记录的保持一致时，也可以使用该方法。


## clone 包含 submodule 的仓库

1. 按需 
	1. `git clone {main}`
	2. `git submodule init {path}`
	3. `git submodule update {path}`
	- 合并2，3 `git submodule update --init [submodule的文件夹的相对路径]`
2. 全部更新
	1. `git clone {main}`
	2. `git submodule init`
	3. `git submodule update`
3. 一步
	- `git clone --recurse-submodules [主项目Git仓库地址]`