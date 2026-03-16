---
tags:
  - git
---


## 主分支 master

正式版本

- 对于科研 ： 可以是最好的指标

## 开发分支 develop

可以是 预发布，或者 开发的分支

推荐使用 `--no-ff` 添加合并节点


## 临时分支

- 功能 feature
- 预发布 release
- 修改bug fixbug

临时添加使用完之后需要删除

> 部分功能暂时无法实现
> - 暂时搁置
> - merge 到 develop, 但是在下一个 commit 删除 (使用rebase)

## release

需要打一些tag

## git flow

https://danielkummer.github.io/git-flow-cheatsheet/index.zh_CN.html

```shell
git flow init

# 添加/完成 feature
git flow feature start {name}
git flow feature finish {name}
git flow feature publish {name} #将特性发送给到远端
git flow feature pull origin {name}
git flow feature track {name} #跟踪特性

# release 同理 注意 finish 的时候归并到 master 和 develop 并在 master 上打标签
git flow release start {版本号}
# hotfix 同理 
```