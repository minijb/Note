# YOLOv3

总体思路

https://blog.csdn.net/weixin_44791964/article/details/105310627

![请添加图片描述](https://img-blog.csdnimg.cn/ac5ff41080e946a8b858df6783422c65.jpg?x-oss-process=image/watermark,type_ZHJvaWRzYW5zZmFsbGJhY2s,shadow_50,text_Q1NETiBAQnViYmxpaWlpbmc=,size_20,color_FFFFFF,t_70,g_se,x_16)

特征提取架构

- 输入图片`batch 416  416 3`
- 输出图片有三种
  - `52 52 256`
  - `26 26 512`
  - `13 13 1024`
- `[13,13,1024]==>[13,13,75]`   `75 = 3 *(20+5)`

注：原文中种类数为80，这个可以酌情修改！！

- 每种输出的特征图会进行上采样并向上堆叠

![img](https://upload-images.jianshu.io/upload_images/16006821-59dd6b77da823e7f.png?imageMogr2/auto-orient/strip|imageView2/2/w/1200/format/webp)

## 1. 网络的架构

**残差网络**

![image-20220621145704500](img/image-20220621145704500.png)

结构如图，作用：让这一层的交过不会更差，只会更好

![new](img/1.png)

