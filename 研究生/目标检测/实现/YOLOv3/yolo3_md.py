from collections import OrderedDict
import torch 
from torch import nn
from rich import print
from darknet import darkNet53

def conv2d(filter_in, filter_out, kernel_size):
    pad = (kernel_size - 1) // 2 if kernel_size else 0
    return nn.Sequential(OrderedDict([
        ("conv", nn.Conv2d(filter_in, filter_out, kernel_size=kernel_size, stride=1, padding=pad, bias=False)),
        ("bn", nn.BatchNorm2d(filter_out)),
        ("relu", nn.LeakyReLU(0.1)),
    ]))

def make_last_layers(filter_list,in_filter,out_filters):
        m = nn.ModuleList([
            conv2d(in_filter,filter_list[0],1),
            conv2d(filter_list[0],filter_list[1],3),
            conv2d(filter_list[1],filter_list[0],1),
            conv2d(filter_list[0],filter_list[1],3),
            conv2d(filter_list[1],filter_list[0],1),
            conv2d(filter_list[0],filter_list[1],3),
            #调整通道数
            nn.Conv2d(filter_list[1],out_filters,kernel_size=1,stride=1,padding=0,bias=True)
        ])
        
        return m

class YoloBody(nn.Module):
    def __init__(self,config):
        super(YoloBody,self).__init__()
        self.config = config 
        self.backbone = darkNet53()
        out_filters = self.backbone.layers_out_filters
        #就是每个grad cell的输出 : 3*25 原文为3*(5+80)
        final_out_filter0 = len(config['yolo']['anchor'][0]) * (5+config["yolo"]["classes"])
        self.last_layer0 = make_last_layers([512,1024],out_filters[-1],final_out_filter0)
        
        final_out_filter1 = len(config['yolo']['anchor'][1]) * (5+config["yolo"]["classes"])
        self.last_layer1_conv = conv2d(512,256,1)
        self.last_layer1_upSample = nn.Upsample(scale_factor=2,mode='nearest')
        self.last_layer1 = make_last_layers([256,512],out_filters[-2]+256,final_out_filter1)
        
        
        final_out_filter2 = len(config['yolo']['anchor'][2]) * (5+config["yolo"]["classes"])
        self.last_layer2_conv = conv2d(256,128,1)
        self.last_layer2_upSample = nn.Upsample(scale_factor=2,mode='nearest')
        self.last_layer2 = make_last_layers([128,256],out_filters[-3]+128,final_out_filter2)
    
    def forward(self,x):
        #该函数的作用是将卷积之后的结果分成两部分
        def _branch(last_layer,layer_in):
            for i ,e in enumerate(last_layer):
                layer_in = e(layer_in)
                if i == 4:
                    out_branch = layer_in
            return layer_in,out_branch
        # [52,52,256]  [26,26,512]  [13,13,1024]
        x2,x1,x0 = self.backbone(x)
        
        out0,out0_branch = _branch(self.last_layer0,x0)
        
        x1_in = self.last_layer1_conv(out0_branch)
        x1_in = self.last_layer1_upSample(x1_in)
        print(f"x1_in,x1",x1_in.shape,x1.shape)
        x1_in = torch.cat([x1_in,x1],1)
        out1,out1_branch= _branch(self.last_layer1,x1_in)
        print(f"after cat x1:",x1_in.shape,out1.shape)
        x2_in = self.last_layer2_conv(out1_branch)
        x2_in = self.last_layer2_upSample(x2_in)
        x2_in = torch.cat([x2_in,x2],1)
        out2,_ = _branch(self.last_layer2,x2_in)
        return out0,out1,out2
        
config = {
    'yolo' :{
        'anchor':[
            [0,1,2],
            [0,1,2],
            [0,1,2]],
        'classes' : 20
    }
    
} 
model = YoloBody(config)
x = torch.ones([1,3,416,416])
x1,x2,x3 = model(x)