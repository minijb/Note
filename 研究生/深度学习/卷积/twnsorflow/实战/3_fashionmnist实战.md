```python
# %%
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import datasets, layers, metrics, optimizers, Sequential


# %%
(x, y), (x_test, y_test) = datasets.fashion_mnist.load_data()
print(x.shape,x_test.shape)


# %%
def preprocess(x, y):
    x = tf.cast(x, dtype=tf.float32)/255
    y = tf.cast(y, dtype=tf.int32)
    return x, y

batch_size = 128

db = tf.data.Dataset.from_tensor_slices((x, y))
db = db.map(preprocess).shuffle(10000).batch(batch_size)

db_test = tf.data.Dataset.from_tensor_slices((x_test, y_test))
db_test = db_test.map(preprocess).batch(batch_size)
# print(next(iter(db))[0].shape)#(128, 28, 28)
print(x_test.shape,y_test.shape)
print(x.shape,y.shape)

# %%
model = Sequential([
    layers.Dense(256,activation=tf.nn.relu),# 784->256
    layers.Dense(128,activation=tf.nn.relu),
    layers.Dense(64,activation=tf.nn.relu),
    layers.Dense(32,activation=tf.nn.relu),
    layers.Dense(10),
])

# %%
#创建一个输入用来构建参数
model.build(input_shape=[None,28*28])
model.summary()

next(iter(db))[0].shape,next(iter(db_test))[0].shape

# %%
optimizer = optimizers.Adam(learning_rate=0.001)
for epoch in range(30):
    for step,(x,y) in enumerate(db):
        #x:[b,28,28]  y:[b]
        x = tf.reshape(x,[-1,28*28])
        with tf.GradientTape() as tape:
            #x:[b,784]==>[b,10]
            logits = model(x)
            y_onehot = tf.one_hot(y,depth=10)
            loss_mse = tf.reduce_mean(tf.losses.MSE(y_onehot,logits))
            loss_ce = tf.losses.categorical_crossentropy(y_onehot,logits,from_logits=True)
            loss_ce = tf.reduce_mean(loss_ce)
        #自动求导！！！！
        grads = tape.gradient(loss_ce,model.trainable_variables)
        optimizer.apply_gradients(zip(grads,model.trainable_variables))
        if step%100 == 0 :
            print(epoch,step,'loss:',float(loss_mse),float(loss_ce))
        
    total_correct = 0
    total_num = 0 
    for x,y in db_test:
        x = tf.reshape(x,[-1,28*28]) 
        logits = model(x)
        #logits =>prob
        prob = tf.nn.softmax(logits,axis=1)
        pred = tf.argmax(prob,axis=1)#[b,10]=>[b]
        pred = tf.cast(pred,tf.int32)
        # print(y.shape,pred.shape)
        correct = tf.equal(pred,y)#[b],true,false
        correct = tf.reduce_sum(tf.cast(correct,tf.int32))
        # print(correct)
        total_correct+=int(correct)
        total_num+=x.shape[0]
    acc = total_correct/total_num
    print('*'*20)
    print(epoch,total_correct,acc)
    print('*'*20)



```

