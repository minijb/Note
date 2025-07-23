---
tags:
  - opengl
---

## glclear

清除某个buffer ： 如 colorBuffer，depthBuffer, stencllBuffer

`glClearColor` 设置一个颜色，当我们清除 color buffer 的时候见当前的 screen 设置为这个颜色

## 2D 图形

normalized device coordinates ： 标准化设备坐标， 用于表示当前screen 中的坐标： 中心为 (0,0) 范围： (-1,-1) - (1,1)

![600](https://learnopengl.com/img/getting-started/ndc.png)

## Opengl Object

**extensions** : opengl 支持扩展， 很多扩展是和硬件绑定的。

```c++
// query a extension
if(GL_ARB_extension_name)
{
    // Do cool new and modern stuff supported by hardware
}
else
{
    // Extension not supported: do it the old way
}
```

**opengl** 本质是一个状态机。其状态是和 `opengl context` 相关。当我们需要操作opengl 的时候，其实就是操作不同的状态，如 `bind_buffer` , mainipulate buffers and use current buffer to rendering。具体操作方法就是通过需要 state-using functions

**Objects** :

opengl 进行了许多抽象。 如 Object。

一个object表示 opengl 中状态子集合中的选项。

For example, we could have an object that represents the settings of the drawing window; we could then set its size, how many colors it supports and so on. One could visualize an object as a C-like struct:

```c
struct object_name {
    float  option1;
    int    option2;
    char[] name;
};
```

每当我们想要使用对象时，它通常看起来像这样(OpenGL 的上下文可视化为一个大结构) :

```c
// The State of OpenGL
struct OpenGL_Context {
  	...
  	object_name* object_Window_Target;
  	...  	
};

```

```c
// create object
unsigned int objectId = 0;
glGenObject(1, &objectId);
// bind/assign object to context
glBindObject(GL_WINDOW_TARGET, objectId);
// set options of object currently bound to GL_WINDOW_TARGET
glSetObjectOption(GL_WINDOW_TARGET, GL_OPTION_WINDOW_WIDTH,  800);
glSetObjectOption(GL_WINDOW_TARGET, GL_OPTION_WINDOW_HEIGHT, 600);
// set context target back to default
glBindObject(GL_WINDOW_TARGET, 0);
```




## Vertex Buffer Memory

希望 GPU 获得数据， 我们需要先设置一个 memory --- vertex buffer objects (VBO)

基本步骤

1. GenBuffer
2. BindBuffer -- GL_ARRAY_BUFFER
3. BufferData -- 填充数据

`glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);`

type, size, data point, mod

**mod**

- GL_STREAM_DRAW: the data is set only once and used by the GPU at most a few times.
- GL_STATIC_DRAW: the data is set only once and used many times.
- GL_DYNAMIC_DRAW: the data is changed a lot and used many times.

## Link vertex Attributes pointer

我们必须指定 OpenGL 在呈现之前如何解释顶点数据。

![xx](https://learnopengl.com/img/getting-started/vertex_attribute_pointer.png)

使用 glVertexAttribPointer 来指定 Attribute

```c++
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), (void*)0); 
glEnableVertexAttribArray(0);
```

glVertexAttribPointer 参数

-  vertex attribute we want to configure  --- `layout (location = 0)`
-  the size of vertex attribute  -- vec3 - 3
-  type of data
-  if want to be normalized
-  stride , 间隔， 3 times of float
-  offset of the begin

**注意** ： 每个顶点属性从一个VBO管理的内存中获得它的数据，而具体是从哪个VBO（程序中可以有多个VBO）获取则是通过在调用glVertexAttribPointer时绑定到GL_ARRAY_BUFFER的VBO决定的。由于在调用glVertexAttribPointer之前绑定的是先前定义的VBO对象，顶点属性`0`现在会链接到它的顶点数据。

**启用顶点属性** : `glEnableVertexAttribArray`



具体流程

```c++
// 0. 复制顶点数组到缓冲中供OpenGL使用
glBindBuffer(GL_ARRAY_BUFFER, VBO);
glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);
// 1. 设置顶点属性指针
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), (void*)0);
glEnableVertexAttribArray(0);
// 2. 当我们渲染一个物体时要使用着色器程序
glUseProgram(shaderProgram);
// 3. 绘制物体
someOpenGLFunctionThatDrawsOurTriangle();
```


### 更加方便的存储 attribute 和 VBO 之间的对应关系 --- Vertex Array Object

所有这些状态配置储存在一个对象中，并且可以通过绑定这个对象来恢复状态。
**简单来说就是存储了多个状态**

一个顶点数组对象会储存以下这些内容：

- `glEnableVertexAttribArray` 和 `glDisableVertexAttribArray` 的调用。
- 通过 `glVertexAttribPointer` 设置的顶点属性配置。
- 通过 `glVertexAttribPointer` 调用与顶点属性关联的顶点缓冲对象。

![xx](https://learnopengl-cn.github.io/img/01/04/vertex_array_objects.png)

**注意：这里的绑定和解绑的顺序是很重要的** https://blog.csdn.net/xiji333/article/details/114934590
https://zhuanlan.zhihu.com/p/612275858 (尤其是 EBO)

简单过程 

```c++
unsigned int VAO;
glGenVertexArrays(1, &VAO);
// ..:: 初始化代码（只运行一次 (除非你的物体频繁改变)） :: ..
// 1. 绑定VAO
glBindVertexArray(VAO);
// 2. 把顶点数组复制到缓冲中供OpenGL使用
glBindBuffer(GL_ARRAY_BUFFER, VBO);
glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);
// 3. 设置顶点属性指针
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), (void*)0);
glEnableVertexAttribArray(0);

[...]

// ..:: 绘制代码（渲染循环中） :: ..
// 4. 绘制物体
glUseProgram(shaderProgram);
glBindVertexArray(VAO);
someOpenGLFunctionThatDrawsOurTriangle();

glUseProgram(shaderProgram);
glBindVertexArray(VAO);
glDrawArrays(GL_TRIANGLES, 0, 3);
```

###  Element Buffer Object  元素缓冲对象

**一个 VAO 中可以有多个 VBO（保存的是 attribute），多个 EBO (保存的是实际数据)**

减少重复顶点

```c++
unsigned int indices[] = {
    // 注意索引从0开始! 
    // 此例的索引(0,1,2,3)就是顶点数组vertices的下标，
    // 这样可以由下标代表顶点组合成矩形

    0, 1, 3, // 第一个三角形
    1, 2, 3  // 第二个三角形
};

unsigned int EBO;
glGenBuffers(1, &EBO);

glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO);
glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(indices), indices, GL_STATIC_DRAW);


// draw
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO);
glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, 0);
```

注意， VAO 同时也可以绑定 EBO 

```c++
// ..:: 初始化代码 :: ..
// 1. 绑定顶点数组对象
glBindVertexArray(VAO);
// 2. 把我们的顶点数组复制到一个顶点缓冲中，供OpenGL使用
glBindBuffer(GL_ARRAY_BUFFER, VBO);
glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);
// 3. 复制我们的索引数组到一个索引缓冲中，供OpenGL使用
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO);
glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(indices), indices, GL_STATIC_DRAW);
// 4. 设定顶点属性指针
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), (void*)0);
glEnableVertexAttribArray(0);

[...]

// ..:: 绘制代码（渲染循环中） :: ..
glUseProgram(shaderProgram);
glBindVertexArray(VAO);
glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, 0);
glBindVertexArray(0);
```


**流程**

- bind VAO
- bind VBOs and attribute  (can unbind immediatly)
- bind EBOs
- unbind VAO
- unbind EBO

## 绑定和解绑顺序

绑定
VAO - VBO,EBO
解绑
VBO(单独), VAO - EBO

VAO 中存储的是 attribute pointer 数组，因此可以随时解绑 VBO
绑定的 EBO 是直接存储再VAO中的



## shader -- glsl

基础语法, 
vertex 输入 ： `in`
顶点类型 ： `vec3`
变量位置表示 `layout (location = 0)`

```glsl

#version 330 core
layout (location = 0) in vec3 aPos;

void main()
{
    gl_Position = vec4(aPos.x, aPos.y, aPos.z, 1.0);
}
```

输出使用 `gl_Position` 表示 类型 vec4 因此我们需要使用 1.0 进行填充

### 创建 Shader

**vertex shader**

1. 创建一个shader 

```c++
unsigned int vertexShader;
vertexShader = glCreateShader(GL_VERTEX_SHADER);s
```

2. 添加源代码并编译

```c++
glShaderSource(vertexShader, 1, &vertexShaderSource, NULL);
glCompileShader(vertexShader);
```

3. 检查编译是否发生错误

```c++
int  success;
char infoLog[512];
//  check if compile is success
glGetShaderiv(vertexShader, GL_COMPILE_STATUS, &success);

if(!success)
{
	// get the info
    glGetShaderInfoLog(vertexShader, 512, NULL, infoLog);
    std::cout << "ERROR::SHADER::VERTEX::COMPILATION_FAILED\n" << infoLog << std::endl;
}
```

**fragment shader**

```glsl

#version 330 core
out vec4 FragColor;

void main()
{
    FragColor = vec4(1.0f, 0.5f, 0.2f, 1.0f);
} 
```


使用 `out` 声明一个输出变量

### 生成一个 shader program

连接的过程就是将前一个的输入作为后一个的输出

```c++
// create a program
unsigned int shaderProgram;
shaderProgram = glCreateProgram();

// link
glAttachShader(shaderProgram, vertexShader);
glAttachShader(shaderProgram, fragmentShader);
glLinkProgram(shaderProgram);
```

和之前编译的过程一样， 可以使用  glGetShaderiv and glGetShaderInfoLog 来获取编译信息。

### 使用 一个 shader program

`glUseProgram(shaderProgram);`

Every shader and rendering call after glUseProgram will now use this program object (and thus the shaders).

### 注意 链接好之后就可以删除 shader 了

```c++
glDeleteShader(vertexShader);
glDeleteShader(fragmentShader);  
```



## Debug

[debug](https://learnopengl.com/In-Practice/Debugging)




