
```cmake
set(varName value... [PARENT_SCOPE])
```

cmake 中 所有的值都是 string， 如果同时添加多个值，会自动添加 ;

```cmake
set(myVar a b c) # myVar = "a;b;c"
set(myVar a;b;c) # myVar = "a;b;c"
set(myVar "a b c") # myVar = "a b c"
set(myVar a b;c) # myVar = "a;b;c"
set(myVar a "b c") # myVar = "a;b c"
```

同理变量也可以用在任何 string 或者 需要值的地方

```cmake
set(foo ab) # foo = "ab"
set(bar ${foo}cd) # bar = "abcd"
set(baz ${foo} cd) # baz = "ab;cd"
set(myVar ba) # myVar = "ba"
set(big "${${myVar}r}ef") # big = "${bar}ef" = "abcdef"
set(${foo} xyz) # ab = "xyz"
set(bar ${notSetVar}) # bar = ""
```

同理 string 也可以包含 "

```cmake
set(myVar "goes here")
set(multiLine "First line ${myVar}
Second line with a \"quoted\" word")
```

lua形式的字符串，可以在之间添加 = ，数量不限，但是前后的数量需要一致。

```cmake
# Simple multi-line content with bracket syntax,
# no = needed between the square bracket markers
set(multiLine [[
First line
Second line
]])
# Bracket syntax prevents unwanted substitution
set(shellScript [=[
#!/bin/bash
[[ -n "${USER}" ]] && echo "Have USER"
]=])
# Equivalent code without bracket syntax
set(shellScript
"#!/bin/bash
[[ -n \"\${USER}\" ]] && echo \"Have USER\"
")
```

unset a variable

```cmake
set(myVar)
unset(myVar)
```

### environment variable

```cmake
set(ENV{PATH} "$ENV{PATH}:/opt/myDir")
```

仅仅在运行的时候有用，一旦结束就会恢复。

### Cache Variables

存储在 CMakeCache.txt, 一旦设置除非手动修改不会变更。

```cmake
set(varName value... CACHE type "docstring" [FORCE])
```

The type must be one of the following: --- 用来辅助GUI设置

- BOOL 
- FILEPATH
- PATH
- STRING
- INTTERNAL ：用户无法使用该变量。内部缓存变量有时用于持久记录项目的内部信息，如缓存密集查询或计算的结果。密集查询或计算的结果。GUI 工具不会显示内部变量。

设置 boolean 变量 可以使用 option

```cmake
# 等同
option(optVar helpString [initialValue])
set(optVar initialValue CACHE BOOL helpString)
```

