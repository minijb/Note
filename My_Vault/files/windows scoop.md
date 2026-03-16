
## 安装

```shell
iwr -useb get.scoop.sh | iex
scoop update

# 代理
scoop config proxy 127.0.0.1:10809
```


- search——搜索仓库中是否有相应软件。
- install——安装软件。
- uninstall——卸载软件。
- update——更新软件。可通过`scoop update *`更新所有已安装软件，或通过`scoop update`更新所有软件仓库资料及Scoop自身而不更新软件。
- hold——锁定软件阻止其更新。
- info——查询软件简要信息。
- home——打开浏览器进入软件官网。

**添加仓库**

```sh
scoop bucket add {bucketname}
```


[main](https://link.zhihu.com/?target=https%3A//github.com/ScoopInstaller/Main) - Default bucket for the most common (mostly CLI) apps  
[extras](https://link.zhihu.com/?target=https%3A//github.com/ScoopInstaller/Extras) - Apps that don't fit the main bucket's [criteria](https://link.zhihu.com/?target=https%3A//github.com/ScoopInstaller/Scoop/wiki/Criteria-for-including-apps-in-the-main-bucket)  
[games](https://link.zhihu.com/?target=https%3A//github.com/Calinou/scoop-games) - Open source/freeware games and game-related tools  
[nerd-fonts](https://link.zhihu.com/?target=https%3A//github.com/matthewjberger/scoop-nerd-fonts) - Nerd Fonts  
[nirsoft](https://link.zhihu.com/?target=https%3A//github.com/kodybrown/scoop-nirsoft) - Almost all of the [250+](https://link.zhihu.com/?target=https%3A//rasa.github.io/scoop-directory/by-apps%23kodybrown_scoop-nirsoft) apps from [Nirsoft](https://link.zhihu.com/?target=https%3A//nirsoft.net/)  
[java](https://link.zhihu.com/?target=https%3A//github.com/ScoopInstaller/Java) - A collection of Java development kits (JDKs), Java runtime engines (JREs), Java's virtual machine debugging tools and Java based runtime engines.  
[nonportable](https://link.zhihu.com/?target=https%3A//github.com/TheRandomLabs/scoop-nonportable) - Non-portable apps (may require UAC)  
[php](https://link.zhihu.com/?target=https%3A//github.com/ScoopInstaller/PHP) - Installers for most versions of PHP  
[versions](https://link.zhihu.com/?target=https%3A//github.com/ScoopInstaller/Versions) - Alternative versions of apps found in other buckets


