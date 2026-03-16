---
tags:
  - git
---
tag 可以分为轻量标签与附注标签

**轻量标签**很像一个不会改变的分支——它只是某个特定提交的
**附注标签**是存储在 Git 数据库中的一个完整对象， 它们是可以被校验的，其中包含打标签者的名字、电子邮件地址、日期时间， 此外还有一个标签信息，并且可以使用 GNU Privacy Guard （GPG）签名并验证。 通常会建议创建附注标签，这样你可以拥有以上所有信息

```shell
# 列出标签
git tag

#删除标签
git tag -d {tag_name}
```

### 附注标签

```shell
git tag -a {tag_name} [hash] -m {message}
```

### 轻量标签

```shell
git tag {tag_name} [hash]
```

