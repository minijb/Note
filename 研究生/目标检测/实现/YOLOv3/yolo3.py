from torch import nn
import torch
from rich import print
from darknet import darkNet53


class YOLOv3(nn.Module):
    def __init__(self, anchor_masks, classes_num):
        """ YOLOv3
        Args:
            anchor_masks (list): the anchors shape from kmeans
            classes_num (int): the number of classes 
        """
        super(YOLOv3, self).__init__()
        self.backbone = darkNet53()
        # ----------------------------------
        # convolutional set
        # 五部分: (kernel_size) 1,3,1,3,1
        # ----------------------------------

        # ===========================#
        # conv1
        # ===========================#
        self.convolutionalSet0 = self._createConvoltionalSet(1024, 512, 1024)
        # get 13,13,weneed
        self.branch_out0 = self._createBranchOut(
            512, 1024, len(anchor_masks[0])*(classes_num+5))
        self.branch_down0 = self._createBranchDown(512, 216)

        # ===========================#
        # conv2
        # ===========================#\
        # 注因为经过cat合并输入为(26,26,728)我们在这一部分需要转换为(26,26,216)
        self.convolutionalSet1 = self._createConvoltionalSet(512, 256, 728)
        self.branch_out1 = self._createBranchOut(
            256, 512, len(anchor_masks[1])*(classes_num+5))
        self.branch_down1 = self._createBranchDown(256, 128)

        # ===========================#
        # conv3
        # ===========================#
        self.convolutionalSet2 = self._createConvoltionalSet(256, 128, 384)
        self.branch_out2 = self._createBranchOut(
            128, 256, len(anchor_masks[2])*(classes_num+5))

    def forward(self, x):
        """_summary_

        Returns:
            out0: [13,13,need]

        """
        # out2 : [52,52,256]  out1: [ 26,26,512]  out0:[13,13,1024]
        out2, out1, out0 = self.backbone(x)

        out0 = self.convolutionalSet0(out0)
        out0_out = self.branch_out0(out0)  # [13,13,need]
        out0_down = self.branch_down0(out0)  # [26,26,216]
        out1 = torch.cat([out0_down, out1], 1)  # [26,26,728]

        out1 =self.convolutionalSet1(out1)
        out1_out = self.branch_out1(out1)
        out1_down = self.branch_down1(out1)
        out2 = torch.cat([out1_down,out2],1)
        
        out2 = self.convolutionalSet2(out2)
        out2_out = self.branch_out2(out2)
        
        
        return out0_out,out1_out,out2_out

    def conv2d(self, channel_in, channel_out, kernel_size):
        pad = (kernel_size - 1) // 2 if kernel_size else 0
        return [
            nn.Conv2d(channel_in, channel_out, kernel_size=kernel_size,
                      stride=1, padding=pad, bias=False),
            nn.BatchNorm2d(channel_out),
            nn.LeakyReLU(0.1)
        ]

    def _createConvoltionalSet(self, channel_0, channel_1, in_channel):
        """ convoltionalSet
        Args:
            channel_0 (): inner list channel 0
            channel_1 ():  inner list channel 1
            in_channel (): input_cha
        """
        model_list = self._add_Sequential(self.conv2d(in_channel, channel_1, 1),
                                          self.conv2d(channel_1, channel_0, 3),
                                          self.conv2d(channel_0, channel_1, 1),
                                          self.conv2d(channel_1, channel_0, 3),
                                          self.conv2d(channel_0, channel_1, 1))
        # 这里需要将元素解包，因为的值要么是一个个单独的model或者，OrderedDict([])
        return nn.Sequential(*model_list)

    def _createBranchOut(self, channel_in, channel_out, channel_need):
        model_list = self._add_Sequential(
            self.conv2d(channel_in, channel_out, 3),
            nn.Conv2d(channel_out, channel_need, kernel_size=1,
                      padding=0, stride=1, bias=True)
        )
        return nn.Sequential(*model_list)

    def _createBranchDown(self, channel_in, channel_out):
        model_list = self._add_Sequential(
            self.conv2d(channel_in, channel_out, 1),
            nn.Upsample(scale_factor=2, mode='nearest')
        )
        return nn.Sequential(*model_list)

    # 因为Sequential里面不能添加Sequential，因此我们将conv2d里的元素组合为一个list
    def _add_Sequential(self, *args):
        model_list = []
        for i in args:
            if type(i) == list:
                model_list.extend(i)
            else:
                model_list.append(i)
        return model_list


model = YOLOv3([[1, 2, 3], [1, 2, 3], [1, 2, 3]], 20)
x = torch.ones([1, 3, 416, 416])
out0,out1,out2 = model(x)
print(out0.shape,out1.shape,out2.shape)
