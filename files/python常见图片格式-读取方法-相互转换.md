---
tags:
  - PIL
  - pytorch
  - opencv
  - image
---
### PIL

**读取** `image = Image.open({path})`

格式 `h,w`
### Tensor

**读取**

```python
image = Image.open(image_name).convert('RGB')
image = transforms.ToTensor()(image)
```

格式 ： `3, height , width`

数据类型 ： `float32` ---- tensor

颜色通道顺序 ： RGB

## Opencv

**读取** `cv2.imread({path})`

格式 ： `height width 3`

数据类型 ： `uint8`  --- numpy.ndarry


## 转换

### tensor -- cv

```python
max_val=tensor_img.max()
tesor_img=tensor_img*255/max_val

cv_img = tensor_img.permute(1,2,0).numpy() # 类型转换 并修改通道
cv_img = np.uint8(cv_img)

cv_img=cv2.cvtColor(cv_img,cv2.COLOR_RGB2BGR) # 转换颜色通道
```

### tensor -- PIL

```python
from torchvision import transforms

img_PIL = transforms.ToPILImage([mode])(img_tensor)
img_tensor = transforms.PILToTenso()(img_PIL)  # 不进行 scale

img_tensor = transforms.ToTensor()(img_PIL) # 默认进行 scale
```

[mode](https://pytorch.org/vision/main/generated/torchvision.transforms.ToPILImage.html#torchvision.transforms.ToPILImage) 的解释

### PIL -- opencv

```python
img_PIL = Image.open("../datasets/MVTec/bottle/train/good/000.png")
img_cv2 = cv2.imread("../datasets/MVTec/bottle/train/good/000.png")


img_PIL = transforms.PILToTensor()(img_PIL).numpy() #转为 numpy
img_cv2 = img_cv2.transpose(2,0,1)
```


