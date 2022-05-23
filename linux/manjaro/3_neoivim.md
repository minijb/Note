# neovim

### 1. 安装包管理器

```shell
sh -c 'curl -fLo "${XDG_DATA_HOME:-$HOME/.local/share}"/nvim/site/autoload/plug.vim --create-dirs \
       https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'
```

按照首页的

```vim
call plug#begin()

call plug#end()
```

在中间加入插件

插件网站https://vimawesome.com/

### 2. 第一个插件

https://github.com/mhinz/vim-startify

一个开始页面

```
Plug 'mhinz/vim-startify'
```

### 3. 主题

https://github.com/rafi/awesome-vim-colorschemes

这里我们选择了onedark.vim，官网https://github.com/joshdick/onedark.vim

- 配置正确的颜色！！！

在vim配置文件中加入以下代码

```vim
"配置正确的颜色
"需要注意的是tmux终端需要特别设置！！
if (empty($TMUX))
  if (has("nvim"))
    "For Neovim 0.1.3 and 0.1.4 < https://github.com/neovim/neovim/pull/2198 >
    let $NVIM_TUI_ENABLE_TRUE_COLOR=1
  endif
  "For Neovim > 0.1.5 and Vim > patch 7.4.1799 < https://github.com/vim/vim/commit/61be73bb0f965a895bfb064ea3e55476ac175162 >
  "Based on Vim patch 7.4.1770 (`guicolors` option) < https://github.com/vim/vim/commit/8a633e3427b47286869aa4b96f2bfc1fe65b25cd >
  " < https://github.com/neovim/neovim/wiki/Following-HEAD#20160511 >
  if (has("termguicolors"))
    set termguicolors
  endif
endif

#开启onedark
syntax on
colorscheme onedark
```

### 4. 侧边文件书以及小图标

官网

https://github.com/preservim/nerdtree

https://github.com/ryanoasis/vim-devicons

nerdtree安装

```
call plug#begin()
 	Plug 'preservim/nerdtree'
	Plug 'ryanoasis/vim-devicons'
	Plug 'tiagofumo/vim-nerdtree-syntax-highlight'
call plug#end()

"简单配置
"nerdtree
nnoremap <leader>g :NERDTreeToggle<CR>
nnoremap <leader>v :NERDTreeFind<CR>"跳转到目录树
```

### 5. 炫酷的airline

https://github.com/vim-airline/vim-airline

安装

```v
Plugin 'vim-airline/vim-airline'
Plugin 'vim-airline/vim-airline-themes'
```

airline有很多自己的插件和主题，具体看官网！！！

### 6. tab竖线

```vim
 " 缩进划线
 Plug 'yggdroot/indentline'
```

### 7. 模糊查询

https://github.com/ctrlpvim/ctrlp.vim

```vim
    Plug 'ctrlpvim/ctrlp.vim'
```

### 8 . 快速跳转

	"页面内快速跳转
	Plug 'easymotion/vim-easymotion'
	Plug 'haya14busa/incsearch-easymotion.vim'
	Plug 'haya14busa/incsearch.vim'

###  9. 类名查看

https://github.com/preservim/tagbar

```vim
Plug 'preservim/tagbar'
```

### 10 . 一些小工具

```vim
Plug 'jiangmiao/auto-pairs'
Plug 'tpope/vim-commentary'
```

### 11. 快捷键太多怕记不住

```vim
https://github.com/liuchengxu/vim-which-key#neovim
```

