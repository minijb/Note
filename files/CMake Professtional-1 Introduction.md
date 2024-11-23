
**the stage of cmake**

![600](https://s2.loli.net/2024/05/09/aGVn9MEySwlg8hD.png)


**Generating Project Files** 

choose a project generator: Ninja, Unix Makefiles, MSYS Makefiles

```sh
mkdir build
cd build
cmake -G "Unix Makefiles" ../source

# use --help can display the variable
cmake -G -h
```

**building tool**

```sh
cmake --build /some/path/build --config Debug --target MyApp
```

--config 可以在多配置 选项中选择自定义选项进行配置， 如 :Visual Studio 15 2017, Xcode
--target 指定 build 的 目标

## 最小 project

```cmake
cmake_minimum_required(VERSION 3.2)
project(MyApp)
add_executable(myExe main.cpp)

```


**project command**

```cmake
project(projectName
  [VERSION major[.minor[.patch[.tweak]]]]
  [LANGUAGES languageName ...]
)
```

可以添加多个 add_executable 用于测试等

**executables**

```cmake
add_executable(targetName [WIN32] [MACOSX_BUNDLE]
  [EXCLUDE_FROM_ALL]
  source1 [source2 ...]
)
```

一些 keyword :

EXCLUDE_FROM_ALL  指定一些不需要 build 的project

**defining libraries**

the basic

```cmake
add_library(targetName [STATIC | SHARED | MODULE]
  [EXCLUDE_FROM_ALL]
  source1 [source2 ...]
)
```

和 add_executable 类似 

关键字: 

- STATIC : 静态库 windows: .lib, linux : .a
- SHARED : 动态库 windows: .dll, linux : .so
- MODULE : 和动态库类似但是动态加载. 

可以直接使用命令指定类型

```sh
cmake -DBUILD_SHARED_LIBS=YES /path/to/source
```

也可以写入 CMakeLists.txt

```cmake
set(BUILD_SHARED_LIBS YES)
```

## **Link Targets**

CMake 中一些和不同类型的链接

- PRIVATE : 当目标自身需要此链接库时使用
	- A 使用了 B 的库，其他和 A 链接的库，并不需要用到 B。
- PUBLIC : 当目标自身或其他目标链接了这个目标时使用
	- 并仅仅是 A 使用了 B， 他的 interface 也使用了 B
	- 意味着 如果没有B， 那么 A 无法使用。
	- 任何使用了 A 的库 都必须使用 B 才可以运行
	- example ： A 中定义的方法，其中至少有一个类型在 B 中定义或者实现。因此 使用 A 就必须使用 B。
- INTERFACE : 当目标自身不需要此链接库，但其他目标链接了这个目标时使用
	- 为了使用 A， 部分 B 就需要被使用。 
	- 和 PUBLIC 的区别是， A 本身不需要 B， 但是 A 的 interface 需要。
	- example : using a target to represent a header-only library’s dependencies

```cmake
target_link_libraries(targetName
  <PRIVATE|PUBLIC|INTERFACE> item1 [item2 ...]
  [<PRIVATE|PUBLIC|INTERFACE> item3 [item4 ...]]
  ...
)
```

使用这个命令来处理库和库之间的关系

```cmake
add_library(collector src1.cpp)
add_library(algo src2.cpp)
add_library(engine src3.cpp)
add_library(ui src4.cpp)
add_executable(myApp main.cpp)
target_link_libraries(collector
  PUBLIC ui
  PRIVATE algo engine
)
target_link_libraries(myApp PRIVATE collector)
```

ui PUBLIC 链接 collector, 因此 虽然 myApp 只链接 collector ， 但也链接这 ui。
algo and engine PRIVATE 链接 collector， 因此 myApp 并不直接链接他们。

这种方法可以解决循环依赖。


### 不指定 目标 链接

**指定 path to library file**

CMake may ask the linker to search for the library instead (e.g. replace /usr/lib/libfoo.so with -lfoo)

**Plain library name**

If just the name of the library is given with no path, the linker command will search for that library (e.g. foo becomes -lfoo or foo.lib, depending on the platform). This would be common for libraries provided by the system.

**Link Flag**

As a special case, items starting with a hyphen other than -l or -framework will be treated as flags to be added to the linker command. The CMake documentation warns that these should only be used for PRIVATE items, since they would be carried through to other targets if defined as PUBLIC or INTERFACE and this may not always be safe.

## 一些建议

- 目标名称不需要和项目名称相同。
- 命名不需要以 Lib 开头
- 除非有强烈理由，否则尽量避免在知道需要之前为库指定STATIC（静态）或SHARED（共享）关键字。这允许在选择静态库或动态库作为整个项目范围的策略时具有更大的灵活性。可以使用BUILD_SHARED_LIBS变量在一个地方更改默认设置
- 在使用 target_link_libraries()命令时 ， 推荐使用关键字。

