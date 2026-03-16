#TODO
## 1. 命令行

```sh
# open code with current directory
code .

# open the current directory in the most recently used code window
code -r .

# create a new window
code -n

# change the language
code --locale=es

# open diff editor
code --diff <file1> <file2>

# open file at specific line and column <file:line[:character]>
code --goto package.json:10:5

# see help options
code --help

# disable all extensions
code --disable-extensions .

```


## 快速在错误之间跳转

Keyboard Shortcut: Ctrl+Shift+M

Quickly jump to errors and warnings in the project.

Cycle through errors with F8 or Shift+F8


## qick open

**Show Explorer view**
Keyboard Shortcut: Ctrl+Shift+E

**Quick Open**
Quickly search and open files.

Keyboard Shortcut: Ctrl+P


Ctrl+P  ？ ---> view commandsuggestions

### [Navigation history](https://code.visualstudio.com/docs/getstarted/tips-and-tricks?originUrl=%2Fdocs%2Fgetstarted%2Fintrovideos#_navigation-history)

Navigate entire history: Ctrl+Tab

Navigate back: Alt+Left

Navigate forward: Alt+Right

### [Multi cursor selection](https://code.visualstudio.com/docs/getstarted/tips-and-tricks?originUrl=%2Fdocs%2Fgetstarted%2Fintrovideos#_multi-cursor-selection)


alt + click

### [Column (box) selection](https://code.visualstudio.com/docs/getstarted/tips-and-tricks?originUrl=%2Fdocs%2Fgetstarted%2Fintrovideos#_column-box-selection)

You can select blocks of text by holding Shift+Alt (Shift+Option on macOS) while you drag your mouse. A separate cursor will be added to the end of each selected line.

### [Move line up and down](https://code.visualstudio.com/docs/getstarted/tips-and-tricks?originUrl=%2Fdocs%2Fgetstarted%2Fintrovideos#_move-line-up-and-down)

Keyboard Shortcut: Alt+Up or Alt+Down


### [Shrink / expand selection](https://code.visualstudio.com/docs/getstarted/tips-and-tricks?originUrl=%2Fdocs%2Fgetstarted%2Fintrovideos#_shrink-expand-selection)

Keyboard Shortcut: Shift+Alt+Left or Shift+Alt+Right

### [Go to Symbol in File](https://code.visualstudio.com/docs/getstarted/tips-and-tricks?originUrl=%2Fdocs%2Fgetstarted%2Fintrovideos#_go-to-symbol-in-file)

Keyboard Shortcut: Ctrl+Shift+O
You can group the symbols by kind by adding a colon, `@:`.

### [Go to Symbol in Workspace](https://code.visualstudio.com/docs/getstarted/tips-and-tricks?originUrl=%2Fdocs%2Fgetstarted%2Fintrovideos#_go-to-symbol-in-workspace)

Keyboard Shortcut: Ctrl+T

### [Go to Symbol in Workspace](https://code.visualstudio.com/docs/getstarted/tips-and-tricks?originUrl=%2Fdocs%2Fgetstarted%2Fintrovideos#_go-to-symbol-in-workspace)

Keyboard Shortcut: Ctrl+T  -->  `#`

### [Code folding](https://code.visualstudio.com/docs/getstarted/tips-and-tricks?originUrl=%2Fdocs%2Fgetstarted%2Fintrovideos#_code-folding)

Keyboard Shortcut: Ctrl+Shift+[, Ctrl+Shift+] and Ctrl+K Ctrl+L

### [Rename Symbol](https://code.visualstudio.com/docs/getstarted/tips-and-tricks?originUrl=%2Fdocs%2Fgetstarted%2Fintrovideos#_rename-symbol)

Select a symbol then type F2.

## [Snippets](https://code.visualstudio.com/docs/getstarted/tips-and-tricks?originUrl=%2Fdocs%2Fgetstarted%2Fintrovideos#_snippets)

### [Create custom snippets](https://code.visualstudio.com/docs/getstarted/tips-and-tricks?originUrl=%2Fdocs%2Fgetstarted%2Fintrovideos#_create-custom-snippets)

**File** > **Preferences** > **Configure Snippets**, select the language, and create a snippet.

JSON

```
"create component": {
    "prefix": "component",
    "body": [
        "class $1 extends React.Component {",
        "",
        "\trender() {",
        "\t\treturn ($2);",
        "\t}",
        "",
        "}"
    ]
},
```

See more details in [Creating your own Snippets](https://code.visualstudio.com/docs/editing/userdefinedsnippets).

### [Set VS Code as default merge tool](https://code.visualstudio.com/docs/getstarted/tips-and-tricks?originUrl=%2Fdocs%2Fgetstarted%2Fintrovideos#_set-vs-code-as-default-merge-tool)

Bash

```
git config --global merge.tool vscode
git config --global mergetool.vscode.cmd 'code --wait $MERGED'
```


### [Set VS Code as default diff tool](https://code.visualstudio.com/docs/getstarted/tips-and-tricks?originUrl=%2Fdocs%2Fgetstarted%2Fintrovideos#_set-vs-code-as-default-diff-tool)

Bash

```
git config --global diff.tool vscode
git config --global difftool.vscode.cmd 'code --wait --diff $LOCAL $REMOTE'
```


### Task

run task 快捷键

```json
{
  "key": "ctrl+h",
  "command": "workbench.action.tasks.runTask",
  "args": "Run tests"
}
```