# loss和梯度和优化器

```python
import torch
from torch.nn import L1Loss

input = torch.tensor([1,2,3],dtype=torch.float32)
target = torch.tensor([1,2,5],dtype=torch.float32)

inputs = torch.reshape(input,(1,1,1,3))
targets = torch.reshape(target,(1,1,1,3))

loss = L1Loss(reduction='sum')
result = loss(inputs,targets)

print(result)
```

**注意 CrossEntropyLoss在两种框架内表示不同**

```python
x = torch.tensor([0.1,0.2,0.3])
y = torch.tensor([1])
x = torch.reshape(x,[1,3])
loss_cross = nn.CrossEntropyLoss()
result = loss_cross(x,y)
print(result)
```

## 1. 进行梯度

```python
from statistics import mode
from unittest import result
import torch 
from torchvision import datasets,transforms
from torch.utils.data import DataLoader
from rich import print
from torch  import conv3d, nn

datasets = datasets.CIFAR10("./pytorch/transform/dataset",train=True , transform=transforms.ToTensor())

dataloader = DataLoader(datasets , batch_size=64)

class test(nn.Module):
    """Some Information about test"""
    def __init__(self):
        super(test, self).__init__()
        self.conv1 = nn.Conv2d(in_channels=3 ,out_channels=32,kernel_size=5, padding=2)
        self.pool1 = nn.MaxPool2d(2)
        self.conv2 = nn.Conv2d(32,32,5,padding=2)
        self.pool2 = nn.MaxPool2d(2)
        self.conv3 = nn.Conv2d(32,64,5,padding=2)
        self.pool3 = nn.MaxPool2d(2)
        self.flatten = nn.Flatten()
        
        self.liner1 = nn.Linear(1024,64)
        self.liner2 = nn.Linear(64,10)
        
        self.model1 = nn.Sequential(
            nn.Conv2d(in_channels=3 ,out_channels=32,kernel_size=5, padding=2),
            nn.MaxPool2d(2),
            nn.Conv2d(32,32,5,padding=2),
            nn.MaxPool2d(2),
            nn.Conv2d(32,64,5,padding=2),
            nn.MaxPool2d(2),
            nn.Flatten(),
            nn.Linear(1024,64),
            nn.Linear(64,10)
        )
        
    def forward(self, x):
        x = self.model1(x)  
        return x
    
model = test()
loss_cross = nn.CrossEntropyLoss()

for step,(imgs,targets) in enumerate(dataloader):
    output = model(imgs)
    loss_result = loss_cross(output,targets) 
    print(loss_result)
    loss_result.backward()
    
```

## 2.优化器

`torch.optim`

```python
from statistics import mode
from unittest import result
import torch 
from torchvision import datasets,transforms
from torch.utils.data import DataLoader
from rich import print
from torch  import conv3d, nn

datasets = datasets.CIFAR10("./pytorch/transform/dataset",train=True , transform=transforms.ToTensor())

dataloader = DataLoader(datasets , batch_size=64)

class test(nn.Module):
    """Some Information about test"""
    def __init__(self):
        super(test, self).__init__()
        self.conv1 = nn.Conv2d(in_channels=3 ,out_channels=32,kernel_size=5, padding=2)
        self.pool1 = nn.MaxPool2d(2)
        self.conv2 = nn.Conv2d(32,32,5,padding=2)
        self.pool2 = nn.MaxPool2d(2)
        self.conv3 = nn.Conv2d(32,64,5,padding=2)
        self.pool3 = nn.MaxPool2d(2)
        self.flatten = nn.Flatten()
        
        self.liner1 = nn.Linear(1024,64)
        self.liner2 = nn.Linear(64,10)
        
        self.model1 = nn.Sequential(
            nn.Conv2d(in_channels=3 ,out_channels=32,kernel_size=5, padding=2),
            nn.MaxPool2d(2),
            nn.Conv2d(32,32,5,padding=2),
            nn.MaxPool2d(2),
            nn.Conv2d(32,64,5,padding=2),
            nn.MaxPool2d(2),
            nn.Flatten(),
            nn.Linear(1024,64),
            nn.Linear(64,10)
        )
        
    def forward(self, x):
        x = self.model1(x)  
        return x
    
model = test()
loss_cross = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(),lr=0.02)

for epch in range(20):
    for step,(imgs,targets) in enumerate(dataloader):
        optimizer.zero_grad()
        output = model(imgs)
        result_loss = loss_cross(output,targets) 
        print(result_loss)
        result_loss.backward()
        optimizer.step()
        # print('ok')
        
```

知识点

- 在初始化的时候将模型的参数放进去

- 每次使用之后都需要把梯度置零

- ```python
  model = test()
  loss_cross = nn.CrossEntropyLoss()
  optimizer = torch.optim.SGD(model.parameters(),lr=0.02)
  
  for epch in range(20):
      for step,(imgs,targets) in enumerate(dataloader):
          optimizer.zero_grad()
          output = model(imgs)
          result_loss = loss_cross(output,targets) 
          print(result_loss)
          result_loss.backward()
          optimizer.step()
  ```

