# Tensorflow

## 1.变量

变量的定义

```python
w = tf.Variable([[0.5,1.0]])
```

值的格式：Tensor

```python
w = tf.Variable([[0.5,1.0]])
x = tf.Variable([[2.0],[1.0]])
#矩阵乘法
y = tf.matmul(w,x)
print(y)#值的格式：Tensor
#tf.Tensor([[2.]], shape=(1, 1), dtype=float32)
```

tensorflow创建的变量都是一个架构没有具体的值

如何赋值

注：2.0之后不适用session！！！！

找到一个新的教程，可以用来学习2.0

https://www.bilibili.com/video/BV1bv4y1P7nm?p=2

1. 定义一个session，把变量放入其中，才可以操作

>必须要使用global_variables_initializer的场合
>含有tf.Variable的环境下，因为tf中建立的变量是没有初始化的，也就是在debug时还不是一个tensor量，而是一个Variable变量类型
>
>可以不使用初始化的场合
>不含有tf.Variable、tf.get_Variable的环境下
>比如只有tf.random_normal或tf.constant等

## 1. GPU加速

1. 需要安装CUDA！！！否则不会GPU加速失败

教程https://blog.csdn.net/qq_38008528/article/details/118033428

下载地址：https://developer.nvidia.com/cuda-toolkit-archive

遇到问题：https://www.tensorflow.org/install/gpu

https://blog.csdn.net/m0_45447650/article/details/123704930

测试程序

```python
import tensorflow as tf
import timeit

with tf.device('/cpu:0'):
    cpu_a = tf.random.normal([10000,1000])
    cpu_b = tf.random.normal([1000,2000])
    print(cpu_a.device,cpu_b.device)
    
with tf.device('/gpu:0'):
    gpu_a = tf.random.normal([10000,1000])
    gpu_b = tf.random.normal([1000,2000])
    print(gpu_a.device,gpu_b.device)
    
def cpu_run():
    with tf.device('/cpu:0'):
        c=tf.matmul(cpu_a,cpu_b)
    return c

def gpu_run():
    with tf.device('/gpu:0'):
        c=tf.matmul(gpu_a,gpu_b)
    return c

#warm_up
cpu_time = timeit.timeit(cpu_run,number=10)
gpu_time = timeit.timeit(gpu_run,number=10)
print('warmup:',cpu_time,gpu_time)


cpu_time = timeit.timeit(cpu_run,number=100)
gpu_time = timeit.timeit(gpu_run,number=100)
print('run time:',cpu_time,gpu_time)
```

### 自动求导

$y = a^2*x+b*x+c$

```python
x = tf.constant(1.)
a = tf.constant(2.)
b = tf.constant(3.)
c = tf.constant(4.)

with tf.GradientTape() as tape:
    tape.watch([a,b,c])
    y = a**2*x + b*x+c
    
dy_da,dy_db,dy_dc = tape.gradient(y,[a,b,c])
print(dy_da,dy_db,dy_dc)
#tf.Tensor(4.0, shape=(), dtype=float32) tf.Tensor(1.0, shape=(), dtype=float32) tf.Tensor(1.0, shape=(), dtype=float32)
```

## 2.手写数字实战

```python
# %%
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers,optimizers,datasets

# %%
(x,y),(x_val,y_val)= datasets.mnist.load_data()
x = tf.convert_to_tensor(x,dtype=tf.float32)/255
y = tf.convert_to_tensor(y,dtype=tf.int32)
y = tf.one_hot(y,depth=10)
print(x.shape,y.shape)

# %%
train_datasets = tf.data.Dataset.from_tensor_slices((x,y))
train_datasets = train_datasets.batch(200)#一次加载200

model = keras.Sequential([
    layers.Dense(512,activation='relu'),
    layers.Dense(256,activation='relu'),
    layers.Dense(10)
])

optimizer = optimizers.SGD(learning_rate=0.001)

def train_epoch(epoch):
    for step,(x,y) in enumerate(train_datasets):
        with tf.GradientTape() as tape:
            x = tf.reshape(x,(-1,28*28))
            out = model(x)
            loss = tf.reduce_sum(tf.square(out-y))/x.shape[0]
        grads = tape.gradient(loss,model.trainable_variables)
        optimizer.apply_gradients(zip(grads,model.trainable_variables))
        if step%100==0:
            print(epoch,step,'loss',loss.numpy())

def train():
    for epoch in range(30):
        train_epoch(epoch)
        

# %%
train()

# %%




```

## 3. 数据类型

### Tensor

`list->np.array->tf.Tensor`

为了解决大数据的吞吐：储存同种类型：np.array

进一步支持GPU计算支持：tf.Tensor



scalar:1.1

vector:[1.1],[1.1,2.2]

matrix:[[1.1,2.2],[3.3,4.4]]



在tf中tensor就是这种所有的数据类型

**基本数据类型**

- int,float,double
- bool,string

创建常量

```python
tf.constant(1,shape=(),dtype=tf.double)
```

#### 常用api

- `a.device`查看使用的硬件

```python
with tf.device('/gpu:0'):
    a = tf.constant(1)
with tf.device('/cpu:0'):
    b = tf.constant(1)
print(a.device,b.device)
```

- 设备切换

```python
aa = a.cpu()
aa.device
bb =b.gpu()
```

> 注：如果a，b要进行运算的话，需要在同一种设备上

- tensor转化为numpy

```python
b.numpy()
a = np.arange(5)
aa = tf.convert_to_tensor(a)
```

- 查看形状,维数,类型,类型转换

```python
b.shape
b.ndim
tf.rank(x)
a.dtype
aa = tf.cast(a,dtype=xxxx)
```

- 判断是否为tensor

```python
tf.is_tensor(b)#return True False
```

#### Variable类型

tensor经过Variable之后就可以求导了

```python
a = tf.range(5)
b = tf.Variable(a)
b.trainable#True---需要进行求导
```

注：

- 转换之后本身还是tensor属性`tf.is_tensor(b)#True`
- `isinstance(b,tf.Tensor)#False`  `isinstance(b,tf.Variable)#True`所以可以用来区分有没有variable

- 直接得到数据`int\float(a)`



