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

