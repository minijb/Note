---
tags:
  - git
---
## delete or revert the commit


```shell
# soft 移动头节点， 同时将删除更改保存到暂存区，同时 工作区不变 --- non-destructive
git reset --soft HEAD~{num}/{hash} 
git reset --hard HEAD~{num}/{hash}  #回退，同时暂存区和工作区都会被重置和commit一样
git reset --mixed HEAD~{num}/{hash} #移动头节点， 保留工作目录，并清空暂存区


# 在可交互界面进行操作
git rebase -i HEAD~{num}/{hash} 
```

## commit --> working space

还原工作区内容 

```shell
git checkout {file_name}
git checkout HEAD~{num}/{hash} {filename}
git checkout {branch_name} {filename}
```

## 撤回 暂存区的内容

```shell
git restore --staged {filename} #撤回暂存区的文件，不影响工作区
git restore {filename} # 将工作区文件恢复到上次提交的状态
```

## revert

```shell
git revert {head}/{hash}
```

生成一个负修改，可以用于中和其他commit的修改。常用与恢复之前一个commit 的修改, **还有一种请款** 就是远程上有个错误，我们需要删除一个commit 的修改，我们不能删除一个节点，但是可以使用 revert 生成一个负节点


![k3inYfExP6SJ9uD.png](https://s2.loli.net/2024/03/20/k3inYfExP6SJ9uD.png)


