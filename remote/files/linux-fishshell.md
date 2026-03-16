
## download

```sh
sudo apt-add-repository ppa:fish-shell/release-3  
sudo apt update  
sudo apt install fish
```

## Tutorial

https://www.cnblogs.com/Masquer/p/13920104.html#%E9%85%8D%E7%BD%AE%E7%8E%AF%E5%A2%83%E5%8F%98%E9%87%8F

### fish language

https://fishshell.com/docs/current/fish_for_bash_users.html#fish-for-bash-users
https://fishshell.com/docs/current/language.html#language


## settings

### 1. 将 fish 设置为默认shell

```sh
chsh -s /usr/bin/fish
```


### 2. 查看历史命令

`ctrl+r`

```shell
zhouhao@zhouhao ~> fish
search:
► fish                           ► ls                                            ► lazygit
► cd                             ► ssh -T git@github.com                         ► nvim .gitignore
► -> down/lazygit                ► cat id_ed25519.pub                            ► ll -a 1_pstree/
► for i in (ls)␤echo $i␤end      ► cd .ssh/
► for i in (ls)␤    echo $i␤end  ► ssh-keygen -t ed25519 -C "1414309848@qq.com"
Search again for more results
```

### 3. 采纳建议

-> 采纳建议，`alt+->` 采纳部分建议

### 4. 基本语法

Fish 的语法非常自然，一眼就能看懂。

🔽 `if`语句：

```shell
if grep fish /etc/shells
    echo Found fish
else if grep bash /etc/shells
    echo Found bash
else
    echo Got nothing
end
```

🔽`switch`语句

```shell
switch (uname)
case Linux
    echo Hi Tux!
case Darwin
    echo Hi Hexley!
case FreeBSD NetBSD DragonFly
    echo Hi Beastie!
case '*'
    echo Hi, stranger!
end
```

🔽`while`循环：

```shell
while true
    echo "Loop forever"
end
```

🔽`for`循环：

```shell
for file in *.txt
    cp $file $file.bak
end
```

#### 命令替代

```shell

# in bash shell:
[root@urmylucky ~]# echo `date`
Tue Nov 3 13:53:55 CST 2020

# in fish shell:
❯ echo (date)
Tue Nov  3 13:58:03 CST 2020

for i in (ls)
    echo $i
end
```

#### 函数

```shell
function ll
    ls -lhG $argv
end

function ls
    command ls -hG $argv
end
```

上面代码定义了一个`ll`函数。命令行执行这个函数以后，就可以用`ll`命令替代`ls -lhG`。其中，变量`$argv`表示函数的参数。

上面的代码重新定义`ls`命令。注意，函数体内的`ls`之前，要加上`command`，否则会因为无限循环而报错。


### 5. 环境变量

Fish 环境变量保存在两个地方：

1. ~/.config/fish/config.fish 用户环境变量
2. /etc/fish/config.fish 全局环境变量

```shell
vim ~/.config/fish/config.fish
#在最后一行加入(注意目录间用空格隔开)
set -x PATH /opt/demo/bin /home/guest/bin $PATH
#最后重新加载fish即可
```


### 6. alias

Fish中使用function来替代alias。定义的function存放于`~/.config/fish/functions`中，function名就是文件名，后缀为`.fish`，在fish启动的时候，所有位于functions文件夹里的以后缀`.fish`结尾的函数都会被自动加载。

config.fish文件中也可定义alias，等价于function。fish中的function不能在后台运行，即使加&也不能。


```shell
# After fish 3.0 can use -s in shell (recommend)
alias -s l "ls -lah"

# Define alias in shell
alias rmi "rm -i"

# Define alias in config file
alias rmi="rm -i"

# This is equivalent to entering the following function:
function rmi
    rm -i $argv
end

# Then, to save it across terminal sessions:
funcsave rmi
```

> 每个函数都必须带参数 $argv，这是shell传过来的参数。
> 最后一条命令创建文件`~/.config/fish/functions/rmi.fish`。

> 执行 bash 脚本 `bash -c SomeBashCommand`


### 7. 提示符

`fish_prompt` 函数用于定义命令行提示符（prompt）。

```shell
function fish_prompt
    set_color purple
    date "+%m/%d/%y"
    set_color FF0
    echo (pwd) '>'
    set_color normal

# result 
02/06/13 
/home/tutorial
```


## 配置

Fish 的配置文件是`~/.config/fish/config.fish`，每次 Fish 启动，就会自动加载这个文件。

我们可以在这个文件里面写入各种自定义函数，它们会被自动加载。比如，上面的`fish_prompt`函数就可以写在这个文件里面，这样每次启动 Fish，就会出现自定义的提示符。

Fish 还提供 Web 界面配置该文件。

Copy

`fish_config`

输入上面的命令以后，浏览器就会自动打开本机的 8000 端口，用户可以在网页上对 Fish 进行配置，比如选择提示符和配色主题