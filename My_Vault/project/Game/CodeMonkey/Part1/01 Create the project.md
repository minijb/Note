
## create the project

- 创建 3D URP 模板的项目。
- 在 setting 中确认 使用了 URP。
- 在 settings/Quality 中 删除额外的 level --- 用来控制在不同设备上的材质质量
- 删除 settings 文件下除 highFidelity 以外的 URP 设置


## basic

选择 编辑器 --- visual studio/vscode --- Edit/preferences/External Tools

### code style

- constants : UpperCase -- `CONSTANTS`
- Properties/Events : PasecalCase -- `MyCodeStyle Instance`
- Fields : camelCase -- `memberVariable`
- Function : PasecalCase , Function params : camelCase -- `void Awake(int time)`

## Post processing

优化我们所见到的东西，一般是项目最后阶段做的事情。

删除原始的 profiler assert 

- Global Volume/Volume/Profile 删除默认的 资源，并创建一个新的
- 确保 Main Camera 中的 post process 是勾选的
- 确保 URP-render 资源文件中 post process 是勾选的

**色调映射 Tonemapping**

色调映射是将图像的 HDR 值重新映射到适合在屏幕上显示的范围内的过程。

**操作：** 勾选 mode 并选择 Neutral

**颜色调整 color adjustments**

[docs](https://docs.unity3d.com/cn/Packages/com.unity.render-pipelines.high-definition@7.4/manual/Post-Processing-Color-Adjustments.html)

Saturation -- 颜色强度 -- 20

**曝光 Bloom**

Threshold -- 0.95
Intensity -- 1

> [how to make unity Glow](https://www.youtube.com/watch?v=bkPe1hxOmbI)

**渐晕 (Vignette)** 

在摄影中，“渐晕”一词表示相对于中心朝图像边缘变暗和/或去饱和。在现实生活中，厚的或堆叠的滤镜、二次镜头和不正确的镜头遮光罩通常会产生此效果。您可以使用渐晕将焦点绘制到图像的中心。

Intensity -- 0.25
Smoothness -- 0.4

**Anti-aliasing 抗锯齿**

位置： main-camera - rendering /URP 资源文件 - Quality

**屏幕空间环境光遮蔽(SSAO) Screen space ambient occlusion**

位置：URP assert

作用：增加部分阴影的强度