---
tags:
  - opengl
---
```glsl
#version version_number
in type in_variable_name;
in type in_variable_name;

out type out_variable_name;

uniform type uniform_name;

void main()
{
  // 处理输入并进行一些图形操作
  ...
  // 输出处理过的结果到输出变量
  out_variable_name = weird_stuff_we_processed;
}
```

输入的变量为顶点属性， 至少保证有16个

**基本属性**

`int`、`float`、`double`、`uint`和`bool`

**向量**

| 类型      | 含义                      |
| ------- | ----------------------- |
| `vecn`  | 包含`n`个float分量的默认向量      |
| `bvecn` | 包含`n`个bool分量的向量         |
| `ivecn` | 包含`n`个int分量的向量          |
| `uvecn` | 包含`n`个unsigned int分量的向量 |
| `dvecn` | 包含`n`个double分量的向量       |
直接获取变量 `.xyzw / .rgba`


GLSL定义了`in`和`out`关键字专门来实现这个目的。每个着色器使用这两个关键字设定输入和输出，只要一个输出变量与下一个着色器阶段的输入匹配，它就会传递下去。但在顶点和片段着色器中会有点不同。使用 location 指定直接接受的变量。

### 全局 uniform

uniform是全局的(Global)。全局意味着uniform变量必须在每个着色器程序对象中都是独一无二的，而且它可以被着色器程序的任意着色器在任意阶段访问。第二，无论你把uniform值设置成什么，uniform会一直保存它们的数据，直到它们被重置或更新。


```glsl
#version 330 core
out vec4 FragColor;

uniform vec4 ourColor; // 在OpenGL程序代码中设定这个变量

void main()
{
    FragColor = ourColor;
}
```

```c++
float timeValue = glfwGetTime();
float greenValue = (sin(timeValue) / 2.0f) + 0.5f;
int vertexColorLocation = glGetUniformLocation(shaderProgram, "ourColor");
glUseProgram(shaderProgram);
glUniform4f(vertexColorLocation, 0.0f, greenValue, 0.0f, 1.0f);
```

| 后缀   | 含义                      |
| ---- | ----------------------- |
| `f`  | 函数需要一个float作为它的值        |
| `i`  | 函数需要一个int作为它的值          |
| `ui` | 函数需要一个unsigned int作为它的值 |
| `3f` | 函数需要3个float作为它的值        |
| `fv` | 函数需要一个float向量/数组作为它的值   |
