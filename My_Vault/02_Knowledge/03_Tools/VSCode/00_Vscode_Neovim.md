https://blog.zwyyy456.tech/zh/posts/setup/vscode-neovim/
https://github.com/mgua/mg-nvim-2025/blob/master/neovim-install-guide-windows.md
https://github.com/nvim-treesitter/nvim-treesitter/wiki/Windows-support
https://www.bilibili.com/video/BV1g4tXzXEwe/?spm_id_from=333.1007.tianma.6-1-19.click&vd_source=8beb74be6b19124f110600d2ce0f3957
## 1. Scoop + powershell安装并更新


[[Window_Scoop 安装、更新、使用]]
[[Window_Powershell_升级]]


## 2. 安装 neovim

- **Release:** `scoop install neovim`
- **Development (pre-release):**

```sh
scoop bucket add versions
scoop install neovim-nightly
```

### 3. 必备需求

- Neovim >= **0.9.0** (needs to be built with **LuaJIT**)
- Git >= **2.19.0** (for partial clones support)
- a [Nerd Font](https://www.nerdfonts.com/)(v3.0 or greater) **_(optional, but needed to display some icons)_**
- [lazygit](https://github.com/jesseduffield/lazygit) **_(optional)_**
- a **C** compiler for `nvim-treesitter`. See [here](https://github.com/nvim-treesitter/nvim-treesitter#requirements)
- **curl** for [blink.cmp](https://github.com/Saghen/blink.cmp) **(completion engine)**
- for [fzf-lua](https://github.com/ibhagwan/fzf-lua) **_(optional)_**
    - **fzf**: [fzf](https://github.com/junegunn/fzf) **(v0.25.1 or greater)**
    - **live grep**: [ripgrep](https://github.com/BurntSushi/ripgrep)
    - **find files**: [fd](https://github.com/sharkdp/fd)
- a terminal that support true color and _undercurl_:
    - [kitty](https://github.com/kovidgoyal/kitty) **_(Linux & Macos)_**
    - [wezterm](https://github.com/wez/wezterm) **_(Linux, Macos & Windows)_**
    - [alacritty](https://github.com/alacritty/alacritty) **_(Linux, Macos & Windows)_**
    - [iterm2](https://iterm2.com/) **_(Macos)_**


## 4. 安装 lazyvim

- Make a backup of your current Neovim files:
    
```sh
# requiredMove-Item $env:LOCALAPPDATA\nvim 
$env:LOCALAPPDATA\nvim.bak# optional but recommendedMove-Item 
$env:LOCALAPPDATA\nvim-data $env:LOCALAPPDATA\nvim-data.bak
```
    
- Clone the starter
    
```sh
git clone https://github.com/LazyVim/starter $env:LOCALAPPDATA\nvim
```
    
- Remove the `.git` folder, so you can add it to your own repo later
    
```sh
Remove-Item $env:LOCALAPPDATA\nvim\.git -Recurse -Force
```
    
- Start Neovim!
    
```sh
nvim
```

