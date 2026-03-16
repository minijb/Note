---
tags:
  - git
---
将当前的**工作区和暂存区**的修改暂存起来，同时将工作区变得干净，方便 从远程进行 fetch，或者 暂存当前想法同时修改一个bug。

注意在使用多个 stash的时候会出现冲突。

常用命令:

```shell
# 进行 stash
git stash
git stash -m {name of stash}

# 展示 stash 
git stash list 
git stash show

# 取出 satsh
git stash pop #取出栈底
git stash pop --index {num}
git stash brach {branch_name} {index} #将 stash 取出后存入到新建的分支上

# 抛弃
git stash drop [id] #没有id 则会默认删除最新的
git stash clear
```

## 处理冲突

如何避免？

- 将冲突之前分配到一个新的分支上

处理冲突?

- 修改冲突文件
- `git add .`
- **推荐** : `git commit -m {something to do}`
- `git satsh drop 1`  由于冲突不会自动删除 stash 内的条目，需要手动删除。


