
**GPU pipeline**

![700](https://s2.loli.net/2025/04/21/he1fA4FZP7n8rdo.png)



- A framebuffer is specified to use 
- Specify one or more textures as output (shading, depth, etc.) 
- Render (fragment shader specifies the content on each texture)

framebuffer -- 帧缓冲
一个渲染 --- 一个 pass
一个 framebuffer 可以绑定多个渲染目标

每一个 pass 的内容

- 指定 obj， camera， MVP 等
- 指定 framebuffer 以及 输入和输出的 纹理
- 指定 顶点和 片元着色器


## shader 初始化

- 创建shader
- 编译
- attach 到一个 program
- Link
- 使用


## Debug shader

- Nsight Graphics
- RenderDoc


![700](https://s2.loli.net/2025/04/21/8dQhpcZ7r35kmeC.png)


![700](https://s2.loli.net/2025/04/21/aFbGPBvNRfU2Owd.png)


