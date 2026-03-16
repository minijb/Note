
```sh
iwr -useb get.scoop.sh | iex

# optional 更换 Scoop 的更新目录
$env:SCOOP='D:\Applications\Scoop'
[Environment]::SetEnvironmentVariable('SCOOP', $env:SCOOP, 'User')
```


## 常用参数


- search——搜索仓库中是否有相应软件。
- install——安装软件。
- uninstall——卸载软件。
- update——更新软件。可通过`scoop update *`更新所有已安装软件，或通过`scoop update`更新所有软件仓库资料及Scoop自身而不更新软件。
- hold——锁定软件阻止其更新。
- info——查询软件简要信息。
- home——打开浏览器进入软件官网。

```sh
C:\Users\skeathy>scoop help
Usage: scoop <command> [<args>]

Some useful commands are:

alias       Manage scoop aliases
bucket      Manage Scoop buckets
cache       Show or clear the download cache
cat         Show content of specified manifest.
checkup     Check for potential problems
cleanup     Cleanup apps by removing old versions
config      Get or set configuration values
create      Create a custom app manifest
depends     List dependencies for an app
export      Exports (an importable) list of installed apps
help        Show help for a command
hold        Hold an app to disable updates
home        Opens the app homepage
info        Display information about an app
install     Install apps
list        List installed apps
prefix      Returns the path to the specified app
reset       Reset an app to resolve conflicts
search      Search available apps
status      Show status and check for new app versions
unhold      Unhold an app to enable updates
uninstall   Uninstall an app
update      Update apps, or Scoop itself
virustotal  Look for app's hash on virustotal.com
which       Locate a shim/executable (similar to 'which' on Linux)

```


## 常用的软件仓库

添加仓库

```sh
scoop bucket add bucketname (+ url可选)
```

**常用的仓库**

[main](https://link.zhihu.com/?target=https%3A//github.com/ScoopInstaller/Main) - Default bucket for the most common (mostly CLI) apps  
[extras](https://link.zhihu.com/?target=https%3A//github.com/ScoopInstaller/Extras) - Apps that don't fit the main bucket's [criteria](https://link.zhihu.com/?target=https%3A//github.com/ScoopInstaller/Scoop/wiki/Criteria-for-including-apps-in-the-main-bucket)  
[games](https://link.zhihu.com/?target=https%3A//github.com/Calinou/scoop-games) - Open source/freeware games and game-related tools  
[nerd-fonts](https://link.zhihu.com/?target=https%3A//github.com/matthewjberger/scoop-nerd-fonts) - Nerd Fonts  
[nirsoft](https://link.zhihu.com/?target=https%3A//github.com/kodybrown/scoop-nirsoft) - Almost all of the [250+](https://link.zhihu.com/?target=https%3A//rasa.github.io/scoop-directory/by-apps%23kodybrown_scoop-nirsoft) apps from [Nirsoft](https://link.zhihu.com/?target=https%3A//nirsoft.net/)  
[java](https://link.zhihu.com/?target=https%3A//github.com/ScoopInstaller/Java) - A collection of Java development kits (JDKs), Java runtime engines (JREs), Java's virtual machine debugging tools and Java based runtime engines.  
[nonportable](https://link.zhihu.com/?target=https%3A//github.com/TheRandomLabs/scoop-nonportable) - Non-portable apps (may require UAC)  
[php](https://link.zhihu.com/?target=https%3A//github.com/ScoopInstaller/PHP) - Installers for most versions of PHP  
[versions](https://link.zhihu.com/?target=https%3A//github.com/ScoopInstaller/Versions) - Alternative versions of apps found in other buckets