---
tags:
  - git
---
## Merge types

- fast-forward (常用)  
- Non fast-forward
	- recursive(常用) /ort
	- octopus
	- ours
	- subtree

## 快速合并

两个分支一前一后，没有分叉，快速分支不会建立一个合并节点。

**合并更改但是不合并分支**

使用 `--squash` 将feature分支上所有更改复制到当前的暂存区 并使用提交。实现非合并或获取更改

```shell
#------------------- 合并更改 -------------------------
git merge --squash feature

Updating d160c4f..cb7113a
Fast-forward
Squash commit -- not updating HEAD
 feature/f1.txt | 0
 feature/f2.txt | 0
 2 files changed, 0 insertions(+), 0 deletions(-)
git: 'loh' is not a git command. See 'git --help'.

#------------------- commit -------------------------

git commit -m "merge feature"
[master 793e85d] merge feature
 2 files changed, 0 insertions(+), 0 deletions(-)
 create mode 100644 feature/f1.txt
 create mode 100644 feature/f2.txt

# log
commit 793e85deff025ea3ee55cf203afa2876f668142e (HEAD -> master)
Author: x
Date:   x

    merge feature

commit d160c4f0d6924df2ccd07f1107a462b41f0af039
Author: x
Date:   x

    “m2
```

![image.png](https://s2.loli.net/2022/12/18/vaQ8CH4AMoBwjck.png)

### 非快速合并

如果两个分支都有进行提交，此时需要创建一个合并节点。也是使用 

```shell
# 处于 main 分支
git merge --no-ff feature
```

![image.png](https://s2.loli.net/2022/12/18/MIsPv6QSikR8KUz.png)

此时同样可以使用 `--squash` 参数在不合并分支的前提下，在当前分支添加修改

```shell
git merge --squash  feature
```

![image.png](https://s2.loli.net/2022/12/18/WC5U2hjIPmBG8nz.png)
