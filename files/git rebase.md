---
tags:
  - git
---


变基简单来说就是将一个分支的提交记录复制到另一个上，以达到减少分支的目的，创造更加 **线性** 的提交历史

为了防止远程和本地的主干混乱，我们需要先使用 fetch 进行统一


```shell
git fetch {main_branch}
git checkout {feature_branch}
git rebase {main_branch} # 将自己的节点移动到 main 后面

#等价于
git rebase {main_branch} {feature_branch}
```

之后我们就可以切换 HEAD ，我们可以使用 fast-forward merge 也可以使用 no-ff创建一个新的 merge 节点

几个使用场景

```shell
# 在功能分支，将功能分支变基到主干分支上
git rebase {main_branch}
# 整理分支--缩小当前branch中的commit内容
git rebase -i {previous_commit}
```

##### --noto 

用于变基隔离较远的分支

![300](https://imgconvert.csdnimg.cn/aHR0cHM6Ly93czEuc2luYWltZy5jbi9sYXJnZS8wMDZWckpBSmd5MWc1azlpbXNoanRqMzBqMDBlcmRnNy5qcGc)

```shell
git rebase --onto master dev next
```

选中 在 next 但是 不在 dev 中的 commit 变基到 master 中。

![300](https://imgconvert.csdnimg.cn/aHR0cHM6Ly93czEuc2luYWltZy5jbi9sYXJnZS8wMDZWckpBSmd5MWc1azlzaG14OHRqMzBvYTA5eGdsdS5qcGc)

##### 可互动的rebase

常用于整理分支

```shell
git rebase -i {main_branch}
```