
[[CMake#- 常用变量]]

## minie setting

```Cmake
cmake_minimum_required(VERSION 3.5.0)

project(
    xxx 
    VERSION 0.1.0 
    LANGUAGES C CXX
)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(${PROJECT_NAME} main.cpp)
```

## 基础

### 不同平台的配置文件

https://runebook.dev/cn/docs/cmake/command/configure_file

原理 : 将文件复制到另一个位置并修改其内容

`configre_file(input output)`

`#cmakedefine VAR ...`  会被替换为 `#define VAR ... 或者 /* #undef VAR */`

也可以直接使用  `#define xxx @xxx@` 
**example**

**foo.h.in**

```cpp
#cmakedefine FOO_ENABLE
#cmakedefine FOO_STRING "@FOO_STRING@"
```

**cmakeList**

```cmake
option(FOO_ENABLE "Enable Foo" ON)
if(FOO_ENABLE)
  set(FOO_STRING "foo")
endif()
configure_file(foo.h.in foo.h @ONLY)
```

**foo.h**

```cpp
#define FOO_ENABLE
#define FOO_STRING "foo"

// if undefine
/* #undef FOO_ENABLE */
/* #undef FOO_STRING */
```

新生成的文件可以使用 

```cmake
target_include_directories(<target> [SYSTEM] <INTERFACE|PUBLIC|PRIVATE> "${CMAKE_CURRENT_BINARY_DIR}")
```


**例子**

`#define` 类型的可以获取 cmake 的基本信息
`#cmakedefine` 可以让代码根据 cmake 中的 option ， 对应运行的代码 (可以根据不同情况添加不同的库， 并使用不同的函数)

```cmake
#cmakedefine USER_ADD
```

```cpp
#ifdef USER_ADD
xxx
#else
xxx
#endif
```

### compile_commands 生成编译json文件

代码跳转、补全等功能

1. `set(CMAKE_EXPORT_COMPILE_COMMANDS ON)`
2. 命令行中添加-DCMAKE_EXPORT_COMPILE_COMMANDS=on

### 添加子模块

```cmake
add_subdirectory (source_dir [binary_dir] [EXCLUDE_FROM_ALL])
```

### include 以及 库文件添加

https://cmake.org/cmake/help/latest/command/target_link_libraries.html
https://cmake.org/cmake/help/latest/command/target_include_directories.html

```cmake
target_link_libraries(<target>
                      <PRIVATE|PUBLIC|INTERFACE> <item>...
                     [<PRIVATE|PUBLIC|INTERFACE> <item>...]...)
                     
target_include_directories(<target> [SYSTEM] [AFTER|BEFORE]
  <INTERFACE|PUBLIC|PRIVATE> [items1...]
  [<INTERFACE|PUBLIC|PRIVATE> [items2...] ...])
```

> 这些命令和 inlcude_directories 以及 Link_libraryies 的区别就是 这两中是全局的， target_xx 可以用来准确对目标进行添加。
## 其他操作

### file 文件查找

https://runebook.dev/cn/docs/cmake/command/file

**主要功能包含** ： 1. reading  2. writing  3. filesystem 4. path conversion 5. Transfer 6. locking 7. Archiving

**常用：**

#### 1. GLOB

```cmake
file(GLOB <variable>
     [LIST_DIRECTORIES true|false] [RELATIVE <path>] [CONFIGURE_DEPENDS]
     [<globbing-expressions>...])
# 递归子目录
file(GLOB_RECURSE <variable> [FOLLOW_SYMLINKS]
     [LIST_DIRECTORIES true|false] [RELATIVE <path>] [CONFIGURE_DEPENDS]
     [<globbing-expressions>...])
```

globbing-expressions : 

```txt
*.cxx      - match all files with extension cxx
*.vt?      - match all files with extension vta,...,vtz
f[3-5].txt - match files f3.txt, f4.txt, f5.txt

// 递归
/dir/*.py  - match all python files in /dir and subdirectories
```

**例子**

| 命令                                                                   | 描述                                         |
| -------------------------------------------------------------------- | ------------------------------------------ |
| `file(GLOB VAR <pattern1> [<pattern2> ...])`                         | 将所有匹配模式 <pattern> 的文件赋值给变量 VAR。            |
| `file(GLOB VAR RELATIVE <path> <pattern1> [<pattern2> ...])`         | 与 GLOB 类似，但是返回的文件路径是相对于给定的 <path>。         |
| `file(GLOB_RECURSE VAR <pattern1> [<pattern2> ...])`                 | 递归地将所有匹配模式的文件赋值给变量 VAR。                    |
| `file(GLOB_RECURSE VAR RELATIVE <path> <pattern1> [<pattern2> ...])` | 与 GLOB_RECURSE 类似，但是返回的文件路径是相对于给定的 <path>。 |
### 文件复制

有两种方法： `configure_file`, `file`

```cmake
configure_file(example.txt ${CMAKE_CURRENT_BINARY_DIR}/example.txt COPYONLY)

file(COPY example.txt DESTINATION ${CMAKE_CURRENT_BINARY_DIR})
```


### private public interface

https://zhuanlan.zhihu.com/p/82244559

### option 开启 if 判断

```cmake
option(<variable> "<help_text>" [value])

if(<variable>)
elseif(<xxx>)
else()
endif()
```


### list 操作

https://cmake.org/cmake/help/latest/command/list.html




## - 常用变量

```cmake
CMAKE_SOURCE_DIR  ==  cmake 源文件所在目录
CMAKE_BINARY_DIR  ==  输出的二进制文件目录
```