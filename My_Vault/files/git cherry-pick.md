---
tags:
  - git
---
choose a commit from one branch and apply it to another。

```shell
git cherry-pick {commit1} {commit2}
```

> 连续的提交 `A..B`  提交 A 必须早于提交 B 。 使用上面的命令，提交 A 将不会包含在 Cherry pick 中。如果要包含提交 A，可以使用下面的语法。 `git cherry-pick A^..B `

和 merge 以及 rebase 不同的是， merge 和并分支头，rebase需要整体变更分支，cherry-pick 可以选择 分支下任意的commit进行复制。

适用场景如下 ： 我们在功能分支上修改了一个bug，此时我们想要在主分支上做同样的修改，那么就可以适用 cherry-pick 将这个修改复制到主分支上。

![1Taz4HfiJ6MQCcw.png](https://s2.loli.net/2024/03/16/1Taz4HfiJ6MQCcw.png)

**冲突解决** : 在解决完冲突之后适用 `git cherry-pick --continue`