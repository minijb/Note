# YOLOv4

主要改进：

- 主干特征提取网络的改进 `Darknet53->CSPDarknet53`
- 加强特征提取网络使用了SPP和PANet结构
- 使用了Mosaic数据增强
- LOSS方面进行了改进

主体结构

![image-20220630145454968](img/image-20220630145454968.png)

CSPDarkNet的主要功能为压缩宽高，提升特征图的数量

最终要的shape为`13*13*1024`

在PANet中进行多次上下采样并进行多次融合

YOLOhead----`75=3*25`

## 1. CSPDarknet 53

1. 使用了Mish激活函数而不是Leaky

$$
Mish = x *tanh(ln(1+e^x))
$$

2. 使用了CSPnet结构



Mish激活函数

```python
```

