---
tags:
  - git
---
### 环境初始化

```shell
# 创建git仓库
git init 

# 环境初始化
git config --global user.name {name}
git config --global user.email {email}
```

### 设置代理

```shell
#http || https
git config --global http.proxy 127.0.0.1:7890
git config --global https.proxy 127.0.0.1:7890

#sock5代理
git config --global http.proxy socks5 127.0.0.1:7891
git config --global https.proxy socks5 127.0.0.1:7891

#查看
git config --global --get http.proxy
git config --global --get https.proxy

#取消
git config --global --unset http.proxy
git config --global --unset https.proxy
```

### ssh连接

github ssh settings : [webcite](https://github.com/settings/keys)

配置过程

```shell
# generation a new ssh key
ssh-keygen -t ed25519 -C "your_email@example.com"
```

复制 `xxx.pub` 公钥文件的内容到 github setting 页面 保存 ssh key。

## test

```shell
ssh -T git@github.com
```