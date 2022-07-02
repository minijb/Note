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
class Mish(nn.Module):
    def __init__(self, **kwargs):
        super(Mish, self).__init__(**kwargs)
    def foward(self, x):
        return x*torch.tanh(F.softplus(x))
#也可以直接使用
torch.nn.function.mish()
```

基础的残差块

```python
# ===========================#
# 主干部分的卷积快
# ===========================#
class BasicConv(nn.Module):
    def __init__(self,in_channels,out_channels,kernel_size,strides=1) -> None:
        super(BasicConv,self).__init__()
        self.conv = nn.Conv2d(in_channels,out_channels,kernel_size,strides)
        self.bn = nn.BatchNorm2d(out_channels)
        self.activation = Mish()
    def forward(self,x):
        x = self.conv(x)
        x = self.bn(x)
        x = self.activation(x)
        return x
        
# ===========================#
# 主干部分残差块
# ===========================#

class ResBlock(nn.Module):
    #nn.Identity()就是输入什么就输出什么的占位模块
    def __init__(self,channels,hidden_channels=None,residual_activation=nn.Identity()):
        super(ResBlock,self).__init__()
        if hidden_channels is None:
            hidden_channels = channels
        self.block = nn.Sequential(
            BasicConv(channels,hidden_channels,1),
            BasicConv(hidden_channels,channels,3)
        )
        
    def forward(self,x):
        return x + self.block(x)
```

CSPNet的结构

![11](https://img-blog.csdnimg.cn/20200509113651540.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NDc5MTk2NA==,size_16,color_FFFFFF,t_70#pic_center)

**主干部分继续进行原来的残差块的堆叠**；
**另一部分则像一个残差边一样，经过少量处理直接连接到最后。**

具体过程

- 进行下采样
- 分为p1,p2

p1:

- 1*1卷积调整通道数

p2:

- 1*1卷积调整通道数
- 进行多次卷积

最后进行cat堆叠

注：下采样和cat都会使用卷积快

```python
# ===========================#
# 主干的模块
# ===========================#

'''
注意点：第一次之后一层卷积且图的储存不修改
输入：输入的通道数，输出的通道数，part2需要卷积的次数，是否是第一层（第一层的特征曾shape不变化）
'''
class ResBlock_body(nn.Module):
    def __init__(self,in_channels,out_channels,num_blocks,first=False) -> None:
        super(ResBlock_body,self).__init__()
        
        #卷积下采样
        self.downSample_conv = BasicConv(in_channels,out_channels,3,2)
        
        if first:
            #第一层只需要改变通道数不需要改变shape
            self.branch_conv0 = BasicConv(out_channels,out_channels,1)
            self.branch_conv1 = BasicConv(out_channels,out_channels,1)
            self.blcoks_conv = nn.Sequential(
                ResBlock(channels=out_channels,hidden_channels=out_channels//2),
                BasicConv(out_channels, out_channels, 1)
            )
            #注：这里进行了因为进行了堆叠所以需要*2
            self.concat_conv = BasicConv(out_channels*2, out_channels, 1)
        else:
            self.branch_conv0 = BasicConv(out_channels,out_channels//2,1)
            self.branch_conv1 = BasicConv(out_channels,out_channels//2,1)
            self.blcoks_conv = nn.Sequential(
                 *[ResBlock(out_channels//2) for _ in range(num_blocks)],
                BasicConv(out_channels//2, out_channels//2, 1)
            )
            self.concat_conv = BasicConv(out_channels, out_channels, 1)
            
    def forward(self,x):
        x = self.downSample_conv(x)
        
        x0 = self.branch_conv0(x)
        x1 = self.branch_conv1(x)
        x1= self.blcoks_conv(x1)
        x = torch.cat([x1,x0],dim=1)
        x = self.concat_conv(x)
        return x
    
text = torch.ones(1,32,416,416)
model = ResBlock_body(32,64,1,True)
print(model(text).shape)
```

主干网络：

只需要构建第一个卷积层个各个模块就可以了，最终由三个输出

```python
'''
输入每个模块需要卷积的次数就可以了
'''
class CSPDarkNet(nn.Module):
    def __init__(self, layers):
        super(CSPDarkNet, self).__init__()
        self.inplanes = 32
        self.conv1 = BasicConv(3, self.inplanes, kernel_size=3, strides=1)
        self.feature_channels = [64, 128, 256, 512, 1024]

        self.stages = nn.ModuleList([
            ResBlock_body(self.inplanes, self.feature_channels[0], layers[0], first=True),
            ResBlock_body(self.feature_channels[0], self.feature_channels[1], layers[1], first=False),
            ResBlock_body(self.feature_channels[1], self.feature_channels[2], layers[2], first=False),
            ResBlock_body(self.feature_channels[2], self.feature_channels[3], layers[3], first=False),
            ResBlock_body(self.feature_channels[3], self.feature_channels[4], layers[4], first=False)
        ])

        self.num_features = 1


    def forward(self, x):
        x = self.conv1(x)

        x = self.stages[0](x)
        x = self.stages[1](x)
        out3 = self.stages[2](x)
        out4 = self.stages[3](out3)
        out5 = self.stages[4](out4)

        return out3, out4, out5

def darknet53(**kwargs):
    model = CSPDarkNet([1, 2, 8, 8, 4])
    return model
```

