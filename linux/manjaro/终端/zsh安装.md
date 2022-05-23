### zsh安装

安装oh-my-zsh之前应该先安装zsh

在ubuntu中可以使用

```shell
sudo apt-get update
sudo apt-get install zsh
```

### oh-my-zsh安装

on-my-zsh 的官网https://ohmyz.sh/#install

**安装**

```shell
#二选一
sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

sh -c "$(wget https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh -O -)"
```

执行安装脚本会提示更换默认shell为zsh，选择Y

安装提示信息

```shell
Initialized empty Git repository in /home/pi/.oh-my-zsh/.git/
remote: Enumerating objects: 1293, done.
remote: Counting objects: 100% (1293/1293), done.
remote: Compressing objects: 100% (1249/1249), done.
remote: Total 1293 (delta 25), reused 1047 (delta 24), pack-reused 0
Receiving objects: 100% (1293/1293), 1.07 MiB | 1.22 MiB/s, done.
Resolving deltas: 100% (25/25), done.
From https://github.com/ohmyzsh/ohmyzsh
 * [new branch]      master     -> origin/master
Branch 'master' set up to track remote branch 'master' from 'origin'.
Already on 'master'
```

![image.png](https://s2.loli.net/2022/02/06/hr6NvUCSxLXusPK.png)

安装完成

### 美化及配置

![image.png](https://s2.loli.net/2022/02/06/GYpA97DLFPwJodz.png)

#### 主题设置

点击进入themes

*This section uses new, uniform screenshots. To see the previous section, go to [Themes (legacy)](https://github.com/ohmyzsh/ohmyzsh/wiki/Themes-(legacy)).*

All the current themes can be found in the `themes/` directory in the Oh My Zsh distribution. [See list here.](https://github.com/robbyrussell/oh-my-zsh/tree/master/themes/)

In order to enable a theme, set `ZSH_THEME` to the name of the theme in your `~/.zshrc`, before sourcing Oh My Zsh; for example: `ZSH_THEME=robbyrussell` If you do not want any theme enabled, just set `ZSH_THEME` to blank: `ZSH_THEME=""`

Here is a collection of screenshots and descriptions of themes that have been contributed to Oh My Zsh. There are some missing from this page. If you want to add or edit descriptions, see the [format description](https://github.com/ohmyzsh/ohmyzsh/wiki/Themes#theme-description-format) at the bottom of this page.

按照要求替换.zshrc中的文件

#### 插件配置

插件可以说是zsh的精髓

点击官网的plugin可以看到插件列表https://github.com/ohmyzsh/ohmyzsh/wiki/Plugins

#### 常用插件

- zsh-autosuggestions
- zsh-syntax-highlighting
- autojump
- wd
- colored-man-pages

#### 输入法

https://www.bilibili.com/video/BV1A4411a7tK?spm_id_from=333.1007.top_right_bar_window_history.content.click







