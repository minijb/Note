---
tags:
  - git
---
### 提交

基础操作

```shell
# 添加文件到暂存区
git add {file/*}

# 提交
git commit
git commit -m {message}
```

`git commit --amend` 重新提交, 简单来说就是部分文件忘记提交了或者写错了我们可以提交到暂存区，使用这个命令。这样暂存区的内容会被合并到之前提交的节点中。

### log

```shell
git log {branch/None}
git log {branch/None} --oneline