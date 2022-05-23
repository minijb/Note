# github 中ssh的使用

### 1. 检查是否含有ssh密钥

```shell
ls -al ~/.ssh
```

如果我们由了如下文件

- *id_rsa.pub*
- *id_ecdsa.pub*
- *id_ed25519.pub*

那么跳过第二步

### 2. 创建一个ssh密钥

```shell
ssh-keygen -t ed25519 -C "your_email@example.com"
#如果失败使用如下命令
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

如果想要设置密钥在选项中设置

windows的ssh文件存在`user/xxx/.ssh`,linux在`~/.ssh`

### 3. 向github中添加密钥

在设置中找到ssh，复制xxxx.pub文件中的文字

### 4. 测试ssh

```shell
ssh -T git@github.com
#选yes

#如下则成功
> Hi username! You've successfully authenticated, but GitHub does not
> provide shell access.
```

#### 5. 使用ssh来上传和拉取

```git
git remote add origin git@github.com:{name}/{repository_name}
```

## 2.代理

http/https协议

//设置代理(clone https://前缀的repo会走代理)

git config --global http.proxy 'http://127.0.0.1:1080'

git config --global https.proxy 'http://127.0.0.1:1080'

git config --global http.proxy 'socks5://127.0.0.1:1080'

git config --global https.proxy 'socks5://127.0.0.1:1080' 



删除
git config --global --unset http.proxy
git config --global --unset https.proxy
