---
tags:
  - vscode
  - vim
---
## easymotion

- find char : `<leader><leader>s`
- find char forward/backwark : `<leader><leader> f/F`
- find word start/end `<leader><leader> w/b`
- find line `<leader><leader> j/k`
- find with / : `<leader><leader>/`

## vim-surround

- `cs{1}{2}`
- `ys{motion}{1}`
- `ds{1}`
- `S{1}` -- visual mode


## commentary

`gc / gC`

## vim-indent-object

根据缩进快速选中 常用于 if 语句以及python的缩进

`operator` -- 可以是 c,d,v .... 

| Command        | Description                                                                                          |     |
| -------------- | ---------------------------------------------------------------------------------------------------- | --- |
| `<operator>ii` | This indentation level                                                                               |     |
| `<operator>ai` | This indentation level and the line above (think `if` statements in Python)                          |     |
| `<operator>aI` | This indentation level, the line above, and the line after (think `if` statements in C/C++/Java/etc) |     |
## sneak

|                           |                                                                         |
| ------------------------- | ----------------------------------------------------------------------- |
| `s<char><char>`           | Move forward to the first occurrence of `<char><char>`                  |
| `S<char><char>`           | Move backward to the first occurrence of `<char><char>`                 |
| `<operator>z<char><char>` | Perform `<operator>` forward to the first occurrence of `<char><char>`  |
| `<operator>Z<char><char>` | Perform `<operator>` backward to the first occurrence of `<char><char>` |


注意 可以使用 `;:` 移动到下一个

## CamelCaseMotion

可以在驼峰内进行移动 --- 对应原本的 w

| Motion Command         | Description                                                                |
| ---------------------- | -------------------------------------------------------------------------- |
| `<leader>w`            | Move forward to the start of the next camelCase or snake_case word segment |
| `<leader>e`            | Move forward to the next end of a camelCase or snake_case word segment     |
| `<leader>b`            | Move back to the prior beginning of a camelCase or snake_case word segment |
| `<operator>i<leader>w` | Select/change/delete/etc. the current camelCase or snake_case word segment |