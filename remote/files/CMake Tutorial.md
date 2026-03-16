## step 1

**the minal project**

```cmake
cmake_minimum_required(VERSION 3.10)
project(Tutorial)
add_executable(Tutorial tutorial.cxx)
```

**specifying c++ standard**

```cmake
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)
```

**project version**

```cmake
project(Tutorial VERSION 1.0)
# the config file
configure_file(TutorialConfig.h.in TutorialConfig.h)
target_include_directories(Tutorial PUBLIC
                           "${PROJECT_BINARY_DIR}"
                           )

```

the definiation

```cpp
#define Tutorial_VERSION_MAJOR @Tutorial_VERSION_MAJOR@
#define Tutorial_VERSION_MINOR @Tutorial_VERSION_MINOR@
```

## step 2 add library


different level of cmake

```cmake
# MathFunctions/CMakeLists.txt
add_library(MathFunctions MathFunctions.cxx mysqrt.cxx)

# main
add_subdirectory(MathFunctions)
target_link_libraries(Tutorial PUBLIC MathFunctions) # link
target_include_directories(Tutorial PUBLIC
                          "${PROJECT_BINARY_DIR}"
                          "${PROJECT_SOURCE_DIR}/MathFunctions"
                          )
```

**add option** 通常和 宏定义一起使用

```cmake
# MathFunctions/CMakeLists.txt
add_library(MathFunctions MathFunctions.cxx )
# define a cache variable and set it on
option(USE_MYMATH "Use tutorial provided math implementation" ON)

# use if
if (USE_MYMATH)
	target_compile_definitions(MathFunctions PRIVATE "USE_MYMATH")
	add_library(SqrtLibrary STATIC
			  mysqrt.cxx
			  )
			  
	target_link_libraries(MathFunctions PRIVATE SqrtLibrary) 
endif()
```

> 我们将自己的 mysqrt.cxx 作为一个库， 如果 有 USE_MYMATH 我们会将其作为一个库添加到 MathFunctions， 在外部 Tutorial 中，只需要知道链接 MathFunctions 就可以了，不需要具体的实现细节。

the cxx file

```cpp
#include <cmath>
#ifdef USE_MYMATH
#  include "mysqrt.h"
#endif

#ifdef USE_MYMATH
  return detail::mysqrt(x);
#else
  return std::sqrt(x);
#endif
```

## step3 add usage required lib

任何想要使用 `MathFunctions` 的 都需要 inlucde 当前文件，但是 `MathFunctions` 不需要。因此我们使用 `INTERFACE`

 Remember `INTERFACE` means things that consumers require but the producer doesn't.

```cmake
target_include_directories(MathFunctions
                           INTERFACE ${CMAKE_CURRENT_SOURCE_DIR}
                           )
```

此时 main 中 我们就可以移除 add_include 文件。 main 中只需要使用 [`target_link_libraries()`](https://cmake.org/cmake/help/latest/command/target_link_libraries.html#command:target_link_libraries "target_link_libraries") 链接目标哭的名字。


**为库添加特性**

创建一个 INTERFACE 的库 --- 一个虚拟库。然后给这个接口库设置了一个编译特性cxx_std_11。那么只要依赖找个虚拟库的对象，在编译时都会使用到cxx_std_11找个特征。

```cmake
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)

add_library(tutorial_compiler_flags INTERFACE)
target_compile_features(tutorial_compiler_flags INTERFACE cxx_std_11)
```

此时 在不同的库 就可以通过引入这个库来添加 c++ 11 的特性

```cmake
target_link_libraries(Tutorial PUBLIC MathFunctions tutorial_compiler_flags)
target_link_libraries(SqrtLibrary PUBLIC tutorial_compiler_flags)
target_link_libraries(MathFunctions PUBLIC tutorial_compiler_flags)
```

当然也可以直接，设置，上面的好处是可以同时设置多个。

```cmake
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)

target_compile_features(Tutorial INTERFACE cxx_std_11)
```


## step4 : add generator expression

```cmake
# 当编译单元的语言与language匹配且CMake编译器id和compiler_ids中任意匹配则为1，否则为0
set(gcc_like_cxx "$<COMPILE_LANG_AND_ID:CXX,ARMClang,AppleClang,Clang,GNU,LCC>")
# 当使用c++和msvc编译器时mscv_cxx变量值为1
set(msvc_cxx "$<COMPILE_LANG_AND_ID:CXX,MSVC>")
```

cmake构建分为config和build阶段，生成器表达式的值在build阶段才得到。生成器表达式可用于根据某些条件设置某些变量和编译选项。

```cmake
$<condition:true_string>
$<IF:condition,true_string,false_string>
```

当condition为真则返回true_string字符串，否则返回空字符串

```cmake
target_compile_options(tutorial_compiler_flags INTERFACE
  "$<${gcc_like_cxx}:-Wall;-Wextra;-Wshadow;-Wformat=2;-Wunused>"
  "$<${msvc_cxx}:-W3>"
)
```

可以嵌套

```cmake
$<${msvc_cxx}:$<BUILD_INTERFACE:-W3>>
```

https://www.bilibili.com/video/BV1Tw411s7Pk/?spm_id_from=333.788&vd_source=8beb74be6b19124f110600d2ce0f3957