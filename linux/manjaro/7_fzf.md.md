# FZF

快速的文件查找

官网

https://github.com/junegunn/fzf

https://github.com/junegunn/fzf.vim

## 1. 安装

```shell
sudo pacman -S fzf


# init.vim
Plug 'junegunn/fzf', { 'do': { -> fzf#install() } }

#如果想要查找具体的文件内容可以选择安装Ag或者Rg
#https://github.com/ggreer/the_silver_searcher

```

## 2. usage

| Command           | List                                                         |
| ----------------- | ------------------------------------------------------------ |
| `:Files [PATH]`   | Files (runs `$FZF_DEFAULT_COMMAND` if defined)               |
| `:GFiles [OPTS]`  | Git files (`git ls-files`)                                   |
| `:GFiles?`        | Git files (`git status`)                                     |
| `:Buffers`        | Open buffers                                                 |
| `:Colors`         | Color schemes                                                |
| `:Ag [PATTERN]`   | [ag](https://github.com/ggreer/the_silver_searcher) search result (`ALT-A` to select all, `ALT-D` to deselect all) |
| `:Rg [PATTERN]`   | [rg](https://github.com/BurntSushi/ripgrep) search result (`ALT-A` to select all, `ALT-D` to deselect all) |
| `:Lines [QUERY]`  | Lines in loaded buffers                                      |
| `:BLines [QUERY]` | Lines in the current buffer                                  |
| `:Tags [QUERY]`   | Tags in the project (`ctags -R`)                             |
| `:BTags [QUERY]`  | Tags in the current buffer                                   |
| `:Marks`          | Marks                                                        |
| `:Windows`        | Windows                                                      |
| `:Locate PATTERN` | `locate` command output                                      |
| `:History`        | `v:oldfiles` and open buffers                                |
| `:History:`       | Command history                                              |
| `:History/`       | Search history                                               |
| `:Snippets`       | Snippets ([UltiSnips](https://github.com/SirVer/ultisnips))  |
| `:Commits`        | Git commits (requires [fugitive.vim](https://github.com/tpope/vim-fugitive)) |
| `:BCommits`       | Git commits for the current buffer; visual-select lines to track changes in the range |
| `:Commands`       | Commands                                                     |
| `:Maps`           | Normal mode mappings                                         |
| `:Helptags`       | Help tags [1](https://github.com/junegunn/fzf.vim#helptags)  |
| `:Filetypes`      | File types                                                   |