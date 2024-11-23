---
tags:
  - games101
---
## wsl 环境配置

### 必要的库

```shell
sudo apt install g++ gdb cmake
sudo apt install libopencv-dev libeigen3-dev
```

### opencv 头文件

```json
{
    "configurations": [
        {
            "name": "Linux",
            "includePath": [
                "${workspaceFolder}/**",
                "/usr/include/opencv4"
            ],
            "defines": [],
            "cStandard": "c17",
            "cppStandard": "gnu++17",
            "intelliSenseMode": "linux-gcc-x64"
        }
    ],
    "version": 4
}
```