# Keras

- datasets
- layers
- losses
- metrics
- optimizers

## 1. metrics

新建meter

```python
acc_meter = tf.keras.metrics.Accuracy()
loss_meter = tf.keras.metrics.Mean()
```

添加数据,在迭代过程中持续的投喂数据

```python
loss_meter.updata_state(loss)
acc_meter.update_state(y,pred)
```

取出数据

```py
print(loss_meter.result().numpy())
print(acc_meter.result().numpy())
```

如果重新记录数据，需要清楚缓存

```python
loss_meter.reset_states()
acc_meter.reset_states()
```



## 3. 自定义网络

- `keras.Sequential`
- `keras.layers.Layer`
- `Keras.Model`

```python
model = Sequential([
    layers.Dense(256,activation=tf.nn.relu),# 784->256
    layers.Dense(128,activation=tf.nn.relu),
    layers.Dense(64,activation=tf.nn.relu),
    layers.Dense(32,activation=tf.nn.relu),
    layers.Dense(10),
])
model.build(input_shape=[None,28*28])
model.summary()
model.trainable_variables#直接查看可以进行求导的参数：也就是自己内部定义的参数w1...wn,b1...bn,按层划分
model.call()#等于model(x)，也就是调用__call__方法
```

我们只需要继承`keras.layers.Layer`,`keras.Model`就可以实现自己的层

Model:`compile,fit,evaluate,predict`

> srquential就是model的子类

```python
#自定义层
class MyDense(tf.keras.layers.Layer):
    def __init__(self,inp_dim,outp_dim):
        super(MyDense,self).__init__()
        #in:784  out:512
        self.kernel = self.add_variable('w',[inp_dim,outp_dim])
        self.bias = self.add_variable('b',[outp_dim])
        
    def call(self,inputs,training=None):
        out = input@ self.kernel+self.bias
        return out
    
#直接创造一个网络
class MyModel(tf.keras.Model):
    def __init__(self):
        super(MyModel,self).__init__()
        self.fc1 = MyDense(28*28,256)
        self.fc2 = MyDense(256,128)
        self.fc3 = MyDense(128,64)
        self.fc4 = MyDense(64,32)
        self.fc5 = MyDense(32,10)
        
    def call(self,input,training=None):
        x = self.fc1(input)
        x = tf.nn.relu(x)
        x = self.fc2(x)
        x = tf.nn.relu(x)
        x = self.fc3(x)
        x = tf.nn.relu(x)
        x = self.fc4(x)
        x = tf.nn.relu(x)
        x = self.fc5(x)
        return x
```

## 4. 模型的保存和加载！！

- `save/load weight`
- `save/load entire model`
- `saved_model`模型的保存格式`.ckpt`

```python
model.save_wights('./xxx/my_checkpoint')
model.load_weights('./xxx/my_checkpoint')
```

**保存参数**

```python
import  os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

import  tensorflow as tf
from    tensorflow.keras import datasets, layers, optimizers, Sequential, metrics


def preprocess(x, y):
    """
    x is a simple image, not a batch
    """
    x = tf.cast(x, dtype=tf.float32) / 255.
    x = tf.reshape(x, [28*28])
    y = tf.cast(y, dtype=tf.int32)
    y = tf.one_hot(y, depth=10)
    return x,y


batchsz = 128
(x, y), (x_val, y_val) = datasets.mnist.load_data()
print('datasets:', x.shape, y.shape, x.min(), x.max())



db = tf.data.Dataset.from_tensor_slices((x,y))
db = db.map(preprocess).shuffle(60000).batch(batchsz)
ds_val = tf.data.Dataset.from_tensor_slices((x_val, y_val))
ds_val = ds_val.map(preprocess).batch(batchsz) 

sample = next(iter(db))
print(sample[0].shape, sample[1].shape)


network = Sequential([layers.Dense(256, activation='relu'),
                    layers.Dense(128, activation='relu'),
                    layers.Dense(64, activation='relu'),
                    layers.Dense(32, activation='relu'),
                    layers.Dense(10)])
network.build(input_shape=(None, 28*28))
network.summary()




network.compile(optimizer=optimizers.Adam(lr=0.01),
		loss=tf.losses.CategoricalCrossentropy(from_logits=True),
		metrics=['accuracy']
	)

network.fit(db, epochs=3, validation_data=ds_val, validation_freq=2)

network.evaluate(ds_val)

network.save_weights('weights.ckpt')
print('saved weights.')
del network

network = Sequential([layers.Dense(256, activation='relu'),
                    layers.Dense(128, activation='relu'),
                    layers.Dense(64, activation='relu'),
                    layers.Dense(32, activation='relu'),
                    layers.Dense(10)])
network.compile(optimizer=optimizers.Adam(lr=0.01),
		loss=tf.losses.CategoricalCrossentropy(from_logits=True),
		metrics=['accuracy']
	)
network.load_weights('weights.ckpt')
print('loaded weights!')
network.evaluate(ds_val)
```

**保存整个模型**

```python
import  os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

import  tensorflow as tf
from    tensorflow.keras import datasets, layers, optimizers, Sequential, metrics


def preprocess(x, y):
    """
    x is a simple image, not a batch
    """
    x = tf.cast(x, dtype=tf.float32) / 255.
    x = tf.reshape(x, [28*28])
    y = tf.cast(y, dtype=tf.int32)
    y = tf.one_hot(y, depth=10)
    return x,y


batchsz = 128
(x, y), (x_val, y_val) = datasets.mnist.load_data()
print('datasets:', x.shape, y.shape, x.min(), x.max())



db = tf.data.Dataset.from_tensor_slices((x,y))
db = db.map(preprocess).shuffle(60000).batch(batchsz)
ds_val = tf.data.Dataset.from_tensor_slices((x_val, y_val))
ds_val = ds_val.map(preprocess).batch(batchsz) 

sample = next(iter(db))
print(sample[0].shape, sample[1].shape)


network = Sequential([layers.Dense(256, activation='relu'),
                    layers.Dense(128, activation='relu'),
                    layers.Dense(64, activation='relu'),
                    layers.Dense(32, activation='relu'),
                    layers.Dense(10)])
network.build(input_shape=(None, 28*28))
network.summary()




network.compile(optimizer=optimizers.Adam(lr=0.01),
		loss=tf.losses.CategoricalCrossentropy(from_logits=True),
		metrics=['accuracy']
	)

network.fit(db, epochs=3, validation_data=ds_val, validation_freq=2)

network.evaluate(ds_val)

network.save('model.h5')
print('saved total model.')
del network

print('loaded model from file.')
network = tf.keras.models.load_model('model.h5', compile=False)
network.compile(optimizer=optimizers.Adam(lr=0.01),
        loss=tf.losses.CategoricalCrossentropy(from_logits=True),
        metrics=['accuracy']
    )
x_val = tf.cast(x_val, dtype=tf.float32) / 255.
x_val = tf.reshape(x_val, [-1, 28*28])
y_val = tf.cast(y_val, dtype=tf.int32)
y_val = tf.one_hot(y_val, depth=10)
ds_val = tf.data.Dataset.from_tensor_slices((x_val, y_val)).batch(128)
network.evaluate(ds_val)
```

**工业环境下的部署**

```python
tf.saved_model.save(m,'/tmp/saved-model')

imported = tf.saved_model.load(path)
g = imported.signatures["serving_default"]
print(f(x=tf.ones([1,28,28,3])))
```

其他语言也可以通过这个来使用模型

## 5. 实战

```python
from cgi import test
from pickletools import optimize
import tensorflow as tf
from tensorflow import keras
import numpy as np


def preprocess(x, y):
    x = tf.cast(x, dtype=tf.float32)/255-1
    y = tf.cast(y, dtype=tf.int32)
    return x, y


batch_size = 128

# 数据处理
(x, y), (x_val, y_val) = keras.datasets.cifar10.load_data()
y = tf.squeeze(y)  # 删除值为1的元素
y_val = tf.squeeze(y_val)
# print(y.shape)#(50000, 1)
y = tf.one_hot(y, depth=10)
y_val = tf.one_hot(y_val, depth=10)

# 包装为数据库形式
train_db = tf.data.Dataset.from_tensor_slices((x, y))
train_db = train_db.map(preprocess).shuffle(10000).batch(batch_size)
test_db = tf.data.Dataset.from_tensor_slices((x_val, y_val))
test_db = test_db.map(preprocess).batch(batch_size)

# sample = next(iter(train_db))
# print(sample[0].shape)


class MyDense(keras.layers.Layer):

    def __init__(self, inp_dim, outp_dim):
        super(MyDense, self).__init__()
        self.kernel = self.add_weight('w', [inp_dim, outp_dim])
        self.bias = self.add_weight('b', [outp_dim])

    def call(self, inputs, training=None):
        out = inputs @ self.kernel+self.bias
        return out


class MyNetwork(keras.Model):
    def __init__(self):
        super(MyNetwork, self).__init__()
        self.fc1 = MyDense(32*32*3, 256)
        self.fc2 = MyDense(256, 256)
        self.fc3 = MyDense(256, 128)
        self.fc4 = MyDense(128, 64)
        self.fc5 = MyDense(64, 10)

    def call(self, input, training=None):
        """_summary_

        Args:
            input (_type_): [b,32,32,3]
        """
        x = tf.reshape(input, [-1, 32*32*3])

        x = self.fc1(x)
        x = tf.nn.relu(x)
        x = self.fc2(x)
        x = tf.nn.relu(x)
        x = self.fc3(x)
        x = tf.nn.relu(x)
        x = self.fc4(x)
        x = tf.nn.relu(x)
        x = self.fc5(x)
        return x


if __name__ == '__main__':
    network = MyNetwork()
    network.compile(optimizer = keras.optimizers.Adam(learning_rate = 0.001)
                    ,loss = tf.losses.CategoricalCrossentropy(from_logits=True),
                    metrics=['accuracy'])
    network.fit(train_db,epochs=3,validation_data = test_db,validation_freq =1)
    network.evaluate(test_db)
    network.save_weights('ckpt/weights.ckpt')
    
    del network
    network = MyNetwork()
    network.compile(optimizer = keras.optimizers.Adam(learning_rate = 0.001)
                    ,loss = tf.losses.CategoricalCrossentropy(from_logits=True),
                    metrics=['accuracy'])
    network.load_weights('ckpt/weights.ckpt').expect_partial()
    network.evaluate(test_db)
```

