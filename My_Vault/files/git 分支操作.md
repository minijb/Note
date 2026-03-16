---
tags:
  - git
---

### 分支

```shell
# 查看 
git branch

# 创建
git branch {name}
git switch {name} #切换分支
git checkout -b {name} #创建并切换到分支
git switch -c {name} #同上

# 删除
git branch -d {name}

# merge
git merge {name} #将另一条分支和自己合并 ， 注意结果为自己的分支名
