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

## 2. 优化器

https://www.bilibili.com/video/BV1B7411L7Qt?p=14

待优化函数w，损失函数loass，学习率lr

1. 计算相关的梯度:$g_t={\sigma loss \over \sigma (w_t)}$
2. 计算t时刻异界动量$m_t$和二阶动量$V_t$
3. 计算t时刻下下降的梯度$\eta_t=lr*m_t/\sqrt{V_t}$
4. 计算t+1时刻的参数$w_t+1=w_t-\eta_t = w_t-lr*m_t/\sqrt{V_t}$

一阶动量：与梯度相关的函数

二阶动量：与蹄冻平方相关的函数



**常用的优化器**

**1. SGD**

$m_t=g_t$  $V_t=1$

$\eta_t = lr*g_t$

$w_{t+1}=w_t-\eta_t=w_t-lr*g_t$

**2.SGDM**

$m_t = \beta*m_{t-1}+(1-\beta)*g_t$   $V_t=1$

$\eta_t = lr*(\beta*m_{t-1}+(1-\beta)*g_t)$

$\beta$在0.9周围

```python
m_w,m_b = 0,0
beta = 0.9

m_w = beta*m_w+(1-beta)*grads[0]
m_b = beta*m_b+(1-beta)*grads[1]
w1.assgin_sub(lr*m_w)
b1.assgin_sub(lr*m_b)
```

**3.Adagrad**

$m_t=g_t$   $V_t=\sum_{\alpha=1}^tg_\alpha^t$

$\eta_t = lr*g_t/(\sqrt{\sum_{\alpha=1}^tg_\alpha^t})$

```python
m_w,m_b = 0,0


v_w += tf.square(grads[0])
v_b += tf.square(grads[1])
w1.assgin_sub(lr*grads[0]/tf.sqrt(v_w))
b1.assgin_sub(lr*grads[1]/tf.sqrt(v_b))
```

**3.RMSProp**

$m_t=g_t$   $V_t=\beta*V_{t-1}+(1-\beta)*g_t^2$

$\eta_t = lr*g_t/(\sqrt{\beta*V_{t-1}+(1-\beta)*g_t^2})$

```python
v_w,v_b = 0,0


v_w += beta*v_w+(1-beta)*tf.square(grads[0])
v_b += beta*v_b+(1-beta)*tf.square(grads[1])
w1.assgin_sub(lr*grads[0]/tf.sqrt(v_w))
b1.assgin_sub(lr*grads[1]/tf.sqrt(v_b))
```

**4.Adam**

$m_t=\beta_1*m_{t-1}+(1-\beta_1)*g_t$

$V_t=\beta_2*V_{t-1}+(1-\beta_2)*g_t^2$

在计算梯度的时候使用偏差

$\eta_t = lr*\hat{m_t}/\sqrt{\hat{V_t}}=lr*{m_t \over 1-\beta_1^t}/\sqrt{{V_t \over 1-\beta_2^t} }$

```python
m_w,m_b = 0,0
v_w,v_b = 0,0

beta1,beta2=0.9,0.999
m_w = beta1*m_w+(1-beta1)*grads[0]
m_b = beta1*m_b+(1-beta1)*grads[1]
v_w = beta2*v_w+(1-beta2)*tf.square(grads[0])
v_b = beta2*v_b+(1-beta2)*tf.square(grads[1])

m_w_col = m_w/(1-tf.pow(beta1,int(global_step)))
m_b_col = m_b/(1-tf.pow(beta1,int(global_step)))
v_w_col = v_w/(1-tf.pow(beta2,int(global_step)))
v_b_col = v_b/(1-tf.pow(beta2,int(global_step)))

w1.assgin_sub(lr*m_w_col/tf.sqrt(v_w_col))
b1.assgin_sub(lr*m_b_col/tf.sqrt(v_b_col))
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
```





