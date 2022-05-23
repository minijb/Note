# Tmux

安装

```
sudo pacman -S tmux 
```

https://github.com/tmux-plugins/tpm

https://github.com/tmux-plugins/tmux-yank

https://github.com/wincent/clipper



配色

https://blog.csdn.net/ghostyusheng/article/details/88746182

```
### 1 .tmux.conf
set -g default-terminal "xterm-256color"
set-option -ga terminal-overrides ",xterm-256color:Tc"
 
### 2 init.vim
set termguicolors
if &term =~# '^screen'
    let &t_8f = "\<Esc>[38;2;%lu;%lu;%lum"
    let &t_8b = "\<Esc>[48;2;%lu;%lu;%lum"
endif
 
### 注意
注意这里有个坑，就是每次改完tmux的配置，一定要保证你的shell里面的tmux session!全部关闭!，重启tmux才能看到效果哦.
 
查看tmux session的命令:
 
tmux list-sessions
```

