# 线性回归

特征$x_1,x_2,\cdots$，$x_1^{(i)}$表示第一类特征中的第i个

特征的参数$\theta_1,\theta2,\cdots$

拟合函数$h_\theta(x)=\theta_0+\theta_1x_1+\theta_2x_2+\cdots$

整合函数$h_\theta(x)=\sum_{i = 0}^n\theta_ix_i=\theta^Tx$可以使用形式表示



**误差**
$$
y^{(i)}=\theta^Tx^{(i)}+\varepsilon^{(i)}
$$
其中$\varepsilon$为误差，其中$\varepsilon^{(i)}$独立且具有相同分布，且符合均值为0的方差为$\theta^2$的高斯分布

高斯分布
$$
p(\epsilon^{(i)})={1 \over {\sqrt{2\pi}\sigma}}exp(-{{(\epsilon^{(i)})^2} \over {2\sigma^2}} )
$$


**似然函数**
$$
L(\theta) = \prod_{i=1}^mp(y^{(i)}|x^{{i}};\theta) = \prod_{i=1}^m{1 \over {\sqrt{2\pi}\sigma}}exp(-{{y^{(i)}-\theta^Tx^{(i)}} \over {2\sigma^2}} )
$$

### 目标推导

使用log就可以简化似然函数
$$
\sum_{i=1}^m\log{F(\theta)}= m\log{{1 \over {\sqrt{2\pi}\sigma}}}-{1 \over \sigma^2}\times{1 \over 2}\sum_{i=1}^m(y^{(i)}-\theta^Tx^{(i)})^2
$$
可以推到出最小二乘法
$$
J(\theta)={1 \over 2}\sum_{i=1}^m(y^{(i)}-\theta^Tx^{(i)})^2
$$

### 使用线性回归求解

目标函数$J(\theta)={1 \over 2}\sum_{i=1}^m(y^{(i)}-\theta^Tx^{(i)})^2={1 \over 2}(X\theta-y)^T(X\theta-y)$

求偏导$X^TX\theta-X^Ty=0$-->$\theta=(X^TX)^{-1}X^Ty$

但是经常不能通过这个方法求出值

**最常用的评估项$R^2$**:$1-{{\sum_{i-1}^m(\hat{y}_i-y_i)^2} \over {\sum_{i-1}^m(y_i-\tilde{y}_i)^2} }$

> 残差是实际观测值与模型估计值之间的差。比如，在回归分析中，得到回归方程为y=0.5+0.8x。若一个实际观测值为（2,3），则模型估计值为y=0.5+0.8×2=2.1，因此残差为3-2.1=0.9。从所有的实际观测值中代入回归方程可以得到所有的残差。这些残差的方差就是残差方差，描述了残差的差异程度。方差越小，说明模型估计值与实际数据吻合较好，反之较差。

$R^2$为1最好

## 1. 梯度下降（补充）

小批量梯度下降

$\theta_j = \theta_j - \alpha{1 \over 10}\sum_{k=i}^{i+9}(h_\theta(x^{(k)})-y^{(k)})x_j^{(k)}$

每集更新选择一小部分数据来计算，不需要用到所有数据来计算



**学习率**：开始较大，逐步减小

## 2. 模型的评估

#### **首先导入数据文件**

```python
import numpy as np
import os
import matplotlib.pyplot as plt
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['xtick.labelsize']=12
plt.rcParams['ytick.labelsize']=12
import warnings
warnings.filterwarnings('ignore')
np.random.seed(42)
from sklearn.datasets import  fetch_mldata
fetch_mldata('MNIST original',data_home='./datasets')
```

> 因为MNIST original包已经被弃用所以在https://github.com/amplab/datascience-sp14/raw/master/lab7/mldata/mnist-original.mat下载，然后船舰data_home中自动创建的mldata文件夹下放入下载的文件就可以自动加载

#### **交叉验证**

将数据集分为，训练集，验证集，测试集

验证集不同模型可以在训练集里随机选择

使用`sklearn.linear_model import SGDClassifier`进行梯度下降，

```py
# %%
import numpy as np
import os
import matplotlib.pyplot as plt
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['xtick.labelsize']=12
plt.rcParams['ytick.labelsize']=12
import warnings
warnings.filterwarnings('ignore')
np.random.seed(42)

# %%
from sklearn.datasets import  fetch_mldata

# %%
minist = fetch_mldata('MNIST original',data_home='./datasets')

# %%
X,y = minist["data"],minist["target"]
X.shape#(70000, 784)
y.shape#(70000,)
#这个数据集其实就是一个灰度图  图像为28*28*1=784个像素

# %%
#指定训练集和测试集
#其中X为特征，y为目标值
X_train,X_test = X[:60000],X[60000:]
y_train,y_test = y[:60000],y[60000:]

# %%
#洗牌操作
import numpy as np
shuffle_index = np.random.permutation(60000)
#Randomly permute a sequence, or return a permuted range.
#If x is a multi-dimensional array, it is only shuffled along its first index.
#得到一个随机的0-60000的数组
shuffle_index#array([30014, 20704, 39358, ..., 16650, 46800,  7085])
#把这些索引值回传到训练集中们 就是打乱数据集
#注意这里两个集合需要对应
X_train ,y_train = X_train[shuffle_index],y_train[shuffle_index]

# %%
#进行交叉验证,为了方便使用，进行二分类操作，
#选出数值为5的项
y_train_5 = (y_train==5)
y_test_5 = (y_test==5)

# %%
from sklearn.linear_model import SGDClassifier
sgd_clf = SGDClassifier(max_iter=5,random_state=42)#使用随机种子，确保每次结果一样
sgd_clf.fit(X_train,y_train_5)

# %%
#在官方文档中可以查看分类器可以使用的方法如predict来预测数据等
sgd_clf.predict([X[35000]])
#报错：期望一个二维的样本，但是给了一个一维的样本
#返回true  预测正确

# %%
y[32000]

# %%
#进行交叉验证
#可以自己选择数据集进行训练，也可以通过sklearn自带的功能来进行交叉验证
#



```

使用`sklearn.model_selection.cross_val_score`来进行

.cross_val_score(*estimator*, *X*, *y=None*, ***, *groups=None*, *scoring=None*, *cv=None*, *n_jobs=None*, *verbose=0*, *fit_params=None*, *pre_dispatch='2\*n_jobs'*, *error_score=nan*)

具体参数详见api文档

```python
# %%
#进行交叉验证
#可以自己选择数据集进行训练，也可以通过sklearn自带的功能来进行交叉验证
from sklearn.model_selection import  cross_val_score
#注意只需要传入训练集！！！不用自己进行分割
cross_val_score(sgd_clf,X_train,y_train,cv=3,scoring='accuracy')#cv为分割策略这里的3为将训练集切分为3份
#scirng 为评分方法
'''
array([0.85442911, 0.85284264, 0.83027454])
'''

# %%
#也可以自己手动操作
from sklearn.model_selection import  StratifiedKFold
from sklearn.base import  clone #可以克隆模型
skf = StratifiedKFold(n_splits=3,random_state=42)


# %%
for train_index , vary_index in skf.split(X_train,y_train):#通过split来获得训练集和验证集
    clone_clf = clone(sgd_clf)#克隆模型
    X_train_folds = X_train[train_index]
    y_train_folds =y_train[train_index]
    X_test_folds = X_train[vary_index]
    y_test_folds = y_train[vary_index]
    #铜鼓分类器来训练
    clone_clf.fit(X_train_folds,y_train_folds)
    y_pred = clone_clf.predict(X_test_folds)
    #预测准确率
    n_correct= sum(y_pred==y_test_folds)
    print(n_correct)
'''
16816
16979
17328
'''


```

#### 混淆矩阵

如1000个样本----990正常  10错误，如果我们全部预测为正常即预测1000true那么正确率为99%-------看起来正确率很高但是模型其实很差



混淆矩阵是除了ROC曲线和AUC之外的另一个判断分类好坏程度的方法。

TP(True Positive): 真实为0，预测也为0

FN(False Negative): 真实为0，预测为1

FP(False Positive): 真实为1，预测为0

TN(True Negative): 真实为1，预测也为1



简单的使用cross_val_predict预测

```python
# %%
from sklearn.model_selection import cross_val_predict
y_train_predict = cross_val_predict(sgd_clf,X_train,y_train_5,cv=3)
#(60000,)X：60000因为将训练集分为三分，进行了三次运算，三次验证集加起来为60000

# %%
import pandas as pd
y_train_predict

# %%
pd.Series(y_train_predict).value_counts()

```

使用混淆矩阵预测

在Classification metrics大类中

[`sklearn.metrics`](https://scikit-learn.org/stable/modules/classes.html#module-sklearn.metrics).confusion_matrix

```python
from sklearn.metrics import confusion_matrix
#通过之前的预测值获得混淆矩阵
confusion_matrix(y_train_5,y_train_predict)
'''
array([[53272,  1307],[ 1077,  4344]], dtype=int64)
'''
```

|      | 0               | 1               |
| ---- | --------------- | --------------- |
| 0    | true negatives  | false positives |
| 1    | flase negatives | true positives  |

- 53272个数据被正确的分到非5类
- 1307个数据被错误的分到5
- 1077个数据被错误的分到非5类
- 4344个数据被正确的分到5

precision精度---正确预测为正的占全部预测为正的比例
$$
precision = {TP \over TP+FP}
$$
recall召回率-----正确预测为正的占全部实际为正的比例
$$
recall = {TP \over TP+FN}
$$

> 精确率和召回率互相影响，理想状态下肯定追求两个都高，但是实际情况是两者相互“制约”：**追求精确率高，则召回率就低；追求召回率高，则通常会影响精确率**。我们当然希望预测的结果精确率越高越好，召回率越高越好， 但事实上这两者在某些情况下是矛盾的。这样就需要综合考虑它们，最常见的方法就是F-score。 也可以绘制出P-R曲线图，观察它们的分布情况。

sklearn 可以直接查看 进度和召回率

| [`metrics.precision_score`](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_score.html#sklearn.metrics.precision_score)(y_true, y_pred, *[, ...]) | Compute the precision. |
| ------------------------------------------------------------ | ---------------------- |
| [`metrics.recall_score`](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.recall_score.html#sklearn.metrics.recall_score)(y_true, y_pred, *[, ...]) | Compute the recall.    |

综合指标-------F-score
$$
F_1={2 \over {1 \over precision}+{1 \over recall}}={TP \over TP+ {FN+FP \over 2}}
$$

| [`metrics.f1_score`](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html#sklearn.metrics.f1_score)(y_true, y_pred, *[, ...]) | Compute the F1 score, also known as balanced F-score or F-measure. |
| ------------------------------------------------------------ | ------------------------------------------------------------ |

#### 阈值对结果的影响

算法会对预测得到一个得分值，之前的预测直接得到了结果，我们可以通过的得分值来判断结果

sklearn不能直接设置阈值，但是可以得到决策分数

`sklearn.linear_model.SGDClassifier.decision_function`通过这个函数得到预测的分数

```python
y_scores = sgd_clf.decision_function(X[35000:60000])
'''
array([  43349.73739616,  199462.44873406,  -95877.20355713, ...,
       -204517.36515234, -221946.26026495,  -88253.42407613])
'''
```

得到分数之后就可以通过阈值来判断对错

阈值小recall提高，precision降低

#### ROC曲线

sklearn.metrics.precision_recall_curve

```python
from sklearn.metrics import precision_recall_curve


# %%
y_scores=cross_val_predict(sgd_clf,X_train,y_train_5,cv=3,method='decision_function')
precision,recall,thresholds = precision_recall_curve(y_train_5,y_scores)
#精度，召回率，阈值
#可以通过plot打印出来

# %%
from matplotlib import pyplot as plt

# %%
def plot_pr_recall_threshold(precision,recall,thresholds):
    plt.plot(thresholds,precision[:-1],"b--",label="precision")
    plt.plot(thresholds,recall[:-1],"g-",label="recall")
    plt.xlabel("Threshold",fontsize=16)
    plt.legend(loc="upper left",fontsize=16)
    plt.xlim([0,1])
plt.figure(figsize=(8,4))
plot_pr_recall_threshold(precision,recall,thresholds)
plt.xlim([-700000,700000])
plt.show()

```

**ROC**

TPR--true postive rate(recall)

FPR--False postive rate

 ```python
 from sklearn.metrics import roc_curve
 fpr ,tpr,thresholds = roc_curve(y_train_5,y_scores)
 
 def plot_ROC(fpr,tpr,label=None):
     plt.plot(fpr,tpr,linewidth=2,label=label)
     plt.axis([0,1,0,1])
     plt.plot([0,1],[0,1],'k--')
     plt.xlabel("false positive rate")
     plt.ylabel("true positive rate")
 plt.figure(figsize=(8,6))
 plot_ROC(fpr,tpr)
 plt.show()
 ```

其中false positive rate 越小越好，true positive rate 越大越好

也就是越左上角越好，也就是说在1*1的数轴内，曲线的面积越大越好

但是roc曲线只适用于分类问题

可以通过roc_auc_score来判断roc的分数

```python
from sklearn.metrics import roc_auc_score
roc_auc_score(y_train_5,y_scores)#0.9624496555967155
```

## 代码实现

- 代码实现
- 梯度下降效果
- 对比不同的梯度下降策略
- 通过曲线分析
- 过拟合和欠拟合
- 正则化作用
- 提前停止策略

直接计算法实现线性变换

```python
# %%
import numpy as np
from matplotlib import  pyplot as plt
plt.rcParams['axes.labelsize']=14
plt.rcParams['xtick.labelsize']=12
plt.rcParams['ytick.labelsize']=12

# %%
#自制数据
X=2*np.random.rand(100,1)
y = 4+3*X + np.random.randn(100,1)

# %%
#查看数据
plt.plot(X,y,'b.')
plt.xlabel('X_1')
plt.ylabel('y')
plt.axis([0,2,0,15])#x，y轴的取值范围
plt.show()

# %%
X_b=np.c_[np.ones((100,1)),X]#c_  r_数据的拼接
#求Xt*X的逆
thrta_best=np.linalg.inv(X_b.T.dot(X_b)).dot(X_b.T).dot(y)

# %%
thrta_best

# %%
X_new = np.array([[0],[2]])
X_new = np.c_[np.ones((2,1)),X_new]
y_predict = X_new.dot(thrta_best)
y_predict
'''
array([[ 4.10721205],
[10.15670234]])
'''
#预测值差不多
plt.plot(X,y,'b.')
plt.plot(X_new[:,1],y_predict,'r--')
plt.axis([0,2,0,15])
plt.show()

#使用sklearn
from sklearn.linear_model import LinearRegression
Line_reg = LinearRegression()
Line_reg.fit(X,y)
print(Line_reg.coef_)
print(Line_reg.intercept_)
```

- 梯度下降步长不能太长也不能太短
- 全局最低和局部最低
- 标准化问题
- 数据预处理`sklearn.preprocessing`

### 批量梯度下降

在普通方法中，我们是直接对公式求偏导的方法来执行梯度下降，现在我们通过**矩阵**直接计算偏导可以更加快速的执行梯度下降
$$
{2 \over m}\sum_{i=1}^m(\theta^T*x^{(i)}-y^{(i)})x_j^{(i)}
$$

> https://www.bilibili.com/video/BV1xk4y1B7RQ?p=3
>
> 矩阵求导：
>
> - 输出分为两大类：标量函数（输出的是一个函数），向量函数（输出的是一个向量或矩阵）
>
> - 同理输入可以分为两大类
> - 那么矩阵求导可以分为4类
>
> 
>
> 矩阵的求导的本质：${dA\over dB}$矩阵A中的每一个元素对矩阵B中每一个元素的每一个元素求导
>
> 从求导个元素个数来看：元素个数为两者每个维度相乘
>
> 
>
> 求导方法：YX拉伸
>
> - 标量不变，向量拉伸
> - 前面横向拉，后面纵向拉
>
> 
>
> - 分子布局（Numerator Layout）：分子不变，分母转置
> - 分母布局（Denominator Layout）：分母不变，分子转置
>
> 例1：${df(x) \over dx}$$f(x)=f(x_1,x_2,...,x_n)$标量，x向量
> $$
> {df(x) \over dx}=\begin{bmatrix}
>     {\partial f(x) \over \partial x_1}\\
>      .\\
>     .\\
>     .
>   \end{bmatrix}
> $$
> 如果f(x)是向量，x为标量，那么结果就是横向的
>
> 例2：y为向量,x为向量
>
> 先吧y作为标量，x为向量那么就是先纵向拉伸，之后再横向拉伸
> $$
> {\partial y \over \partial x}=
> \begin{bmatrix}
>     {\partial y \over \partial x_1} \\
>     .\\
>     .\\
>     .\\
> \end{bmatrix}=
> \begin{bmatrix}
>     {\partial y_1 \over \partial x_1} & {\partial y_2 \over \partial x_1} & ...\\
>     .\\
>     .\\
>     .\\
> \end{bmatrix}
> $$
> 

手写

```python
# %%
eta=0.1
n_iterations=1000
m=100#样本个数
theta = np.random.randn(2,1)

# %%
for iteration in range(n_iterations):
    gradients = 2/m*X_b.T.dot(X_b.dot(theta)-y)
    theta = theta-eta*gradients

# %%
X_new_b.dot(theta)

```

### 不同学习率的影响

```python
theta_path_bgf = []
def plot_gradiant_descent(theta,eta,theta_path = None):
    m = len(X_b)
    plt.plot(X,y,'b.')
    n_iterations=1000
    for iteration in range(n_iterations):
        y_predict = X_new_b.dot(theta)
        plt.plot(X_new,y_predict,'r--')
        gradients = 2/m*X_b.T.dot(X_b.dot(theta)-y)
        theta = theta-eta*gradients
        if theta_path is not None:
            theta_path.append(theta)
    plt.xlabel('X_1')
    plt.axis([0,2,0,15])
    plt.title(f'eta={eta}')

# %%
theta = np.random.randn(2,1)
plt.figure(figsize=(10,4))
plt.subplot(131)
plot_gradiant_descent(theta,eta=0.02)
plt.subplot(132)
plot_gradiant_descent(theta,eta=0.1)
plt.subplot(133)
plot_gradiant_descent(theta,eta=0.5)
plt.show()

```

### 不同的梯度下降

#### 随机梯度下降

```python
theta_path_bgf = []
m = len(X_b)
n_epochs = 50 #衰减策略：在学习过程中先快后慢

t0 = 5
t1 = 50

theta = np.random.randn(2,1)
#在迭代的过程中动态的调整学习率
def learning_shcedule(t):
    return t0/(t1+t)
for epoch in range(n_epochs):#50次迭代，每次迭代所有样本的个数(m)
    for i in range(m):
        #只画前20
        if epoch < 10 and  i < 10:
            y_predict = X_new_b.dot(theta)
            plt.plot(X_new,y_predict,'r--')
        random_index = np.random.randint(m)
        xi = X_b[random_index:random_index+1]
        yi = y[random_index:random_index+1]
        gradients = 2*xi.T.dot(xi.dot(theta)-yi)
        eta=learning_shcedule(n_epochs*m+i)
        theta = theta -eta*gradients
        theta_path_bgf.append(theta)
plt.plot(X,y,'b.')  
plt.axis([0,2,0,15])
plt.show()
```

随机梯度下降损失函数是抖动的

#### Mini-Batch小批量梯度下降

每次只选取一小部分

```python
theta_path_mgd = []
n_iterations = 50
minibatch = 16

theta = np.random.randn(2,1)
m = len(X_b)
t=0
for epoch in range(n_epochs):#50次迭代，每次迭代所有样本的个数(m)
    #每次循环对数据进行重新洗牌，保证随机性
    shuffled_iundex = np.random.permutation(m)
    X_b_shuffled = X_b[shuffled_iundex]
    y_shuffled = y[shuffled_iundex]
    for i in range(0,m,minibatch):
        if epoch < 10 :
            y_predict = X_new_b.dot(theta)
            plt.plot(X_new,y_predict,'r--')
        t+=1
        xi = X_b_shuffled[i:i+minibatch]
        yi = y_shuffled[i:i+minibatch]
        gradients = 2/minibatch*xi.T.dot(xi.dot(theta)-yi)
        # print(gradients)
        #学习率逐步减小
        eta = learning_shcedule(t)
        theta = theta -eta*gradients
        theta_path_mgd.append(theta)
plt.plot(X,y,'b.')  
plt.axis([0,2,0,15])
plt.show()
    
```

#### 不同梯度下降比较

```python
theta_path_bgf=np.array(theta_path_bgf)
theta_path_mgd=np.array(theta_path_mgd)
theta_path_rgf=np.array(theta_path_rgf)
plt.figure(figsize=(15,7))
plt.plot(theta_path_bgf[:,0],theta_path_bgf[:,1],'r-s',linewidth=1,label='bgd')
plt.plot(theta_path_rgf[:,0],theta_path_rgf[:,1],'g-+',linewidth=1,label='rgd')
plt.plot(theta_path_mgd[:,0],theta_path_mgd[:,1],'b-o',linewidth=1,label='mgd')
plt.legend(loc='upper right')
plt.axis([3,3.89,3.05,3.8])
plt.show()
```

### 多项式回归

sklearn.preprocessing.PolynomialFeatures(*degree=2*, ***, *interaction_only=False*, *include_bias=True*, *order='C'*)

多项式变换

Generate polynomial and interaction features.

Generate a new feature matrix consisting of all polynomial combinations of the features with degree less than or equal to the specified degree. For example, if an input sample is two dimensional and of the form [a, b], the degree-2 polynomial features are [1, a, b, a^2, ab, b^2].

```python
# %%
import numpy as np
from matplotlib import  pyplot as plt
plt.rcParams['axes.labelsize']=14
plt.rcParams['xtick.labelsize']=12
plt.rcParams['ytick.labelsize']=12

# %%
#自制数据
X=2*np.random.rand(100,1)
y = 4+3*X + np.random.randn(100,1)

# %%
#查看数据
plt.plot(X,y,'b.')
plt.xlabel('X_1')
plt.ylabel('y')
plt.axis([0,2,0,15])#x，y轴的取值范围
plt.show()

# %%
X_b=np.c_[np.ones((100,1)),X]#c_  r_数据的拼接
#求Xt*X的逆
thrta_best=np.linalg.inv(X_b.T.dot(X_b)).dot(X_b.T).dot(y)

# %%
thrta_best

# %%
X_new = np.array([[0],[2]])
X_new_b = np.c_[np.ones((2,1)),X_new]
y_predict = X_new_b.dot(thrta_best)
y_predict
'''
array([[ 4.10721205],
[10.15670234]])
'''
#预测值差不多
plt.plot(X,y,'b.')
plt.plot(X_new_b[:,1],y_predict,'r--')
plt.axis([0,2,0,15])
plt.show()

# %%
#使用sklearn
from sklearn.linear_model import LinearRegression
Line_reg = LinearRegression()

# %%
Line_reg.fit(X,y)
print(Line_reg.coef_)#特征
print(Line_reg.intercept_)#标量

# %%
eta=0.1
n_iterations=1000
m=100#样本个数
theta = np.random.randn(2,1)

# %%
for iteration in range(n_iterations):
    gradients = 2/m*X_b.T.dot(X_b.dot(theta)-y)
    theta = theta-eta*gradients

# %%
theta

# %%
X_new_b.dot(theta)

# %%
theta_path_bgf = []
def plot_gradiant_descent(theta,eta,theta_path = None):
    m = len(X_b)
    plt.plot(X,y,'b.')
    n_iterations=1000
    for iteration in range(n_iterations):
        y_predict = X_new_b.dot(theta)
        plt.plot(X_new,y_predict,'r--')
        gradients = 2/m*X_b.T.dot(X_b.dot(theta)-y)
        theta = theta-eta*gradients
        if theta_path is not None:
            theta_path.append(theta)
    plt.xlabel('X_1')
    plt.axis([0,2,0,15])
    plt.title(f'eta={eta}')

# %%
theta = np.random.randn(2,1)
plt.figure(figsize=(10,4))
plt.subplot(131)
plot_gradiant_descent(theta,eta=0.02)
plt.subplot(132)
plot_gradiant_descent(theta,eta=0.1,theta_path=theta_path_bgf)
plt.subplot(133)
plot_gradiant_descent(theta,eta=0.5)
plt.show()

# %%
theta_path_rgf = []
m = len(X_b)
n_epochs = 50 #衰减策略：在学习过程中先快后慢

t0 = 5
t1 = 50

theta = np.random.randn(2,1)
#在迭代的过程中动态的调整学习率
def learning_shcedule(t):
    return t0/(t1+t)
for epoch in range(n_epochs):#50次迭代，每次迭代所有样本的个数(m)
    for i in range(m):
        #只画前20
        if epoch < 10 and  i < 10:
            y_predict = X_new_b.dot(theta)
            plt.plot(X_new,y_predict,'r--')
        random_index = np.random.randint(m)
        xi = X_b[random_index:random_index+1]
        yi = y[random_index:random_index+1]
        gradients = 2*xi.T.dot(xi.dot(theta)-yi)
        eta=learning_shcedule(n_epochs*m+i)
        theta = theta -eta*gradients
        theta_path_rgf.append(theta)
plt.plot(X,y,'b.')  
plt.axis([0,2,0,15])
plt.show()

# %%
theta_path_mgd = []
n_iterations = 50
minibatch = 16

theta = np.random.randn(2,1)
m = len(X_b)
t=0
for epoch in range(n_epochs):#50次迭代，每次迭代所有样本的个数(m)
    #每次循环对数据进行重新洗牌，保证随机性
    shuffled_iundex = np.random.permutation(m)
    X_b_shuffled = X_b[shuffled_iundex]
    y_shuffled = y[shuffled_iundex]
    for i in range(0,m,minibatch):
        if epoch < 10 :
            y_predict = X_new_b.dot(theta)
            plt.plot(X_new,y_predict,'r--')
        t+=1
        xi = X_b_shuffled[i:i+minibatch]
        yi = y_shuffled[i:i+minibatch]
        gradients = 2/minibatch*xi.T.dot(xi.dot(theta)-yi)
        # print(gradients)
        #学习率逐步减小
        eta = learning_shcedule(t)
        theta = theta -eta*gradients
        theta_path_mgd.append(theta)
plt.plot(X,y,'b.')  
plt.axis([0,2,0,15])
plt.show()
    

# %%
theta

# %%
theta_path_bgf=np.array(theta_path_bgf)
theta_path_mgd=np.array(theta_path_mgd)
theta_path_rgf=np.array(theta_path_rgf)
plt.figure(figsize=(15,7))
plt.plot(theta_path_bgf[:,0],theta_path_bgf[:,1],'r-s',linewidth=1,label='bgd')
plt.plot(theta_path_rgf[:,0],theta_path_rgf[:,1],'g-+',linewidth=1,label='rgd')
plt.plot(theta_path_mgd[:,0],theta_path_mgd[:,1],'b-o',linewidth=1,label='mgd')
plt.legend(loc='upper right')
plt.axis([3,3.89,3.05,3.8])
plt.show()

# %%
data_len = 100
#指定种子  确保每次随机一样
np.random.seed(42)
X = 6*np.random.rand(m,1)-3
y = 0.5*X**2+X+np.random.randn(m,1)
plt.plot(X,y,'b.')
plt.xlabel('X')
plt.ylabel('y')
plt.axis([-3,3,-3,9])
plt.show()

# %%
from sklearn.preprocessing import PolynomialFeatures
poly = PolynomialFeatures(2,include_bias=False)
X_ploy = poly.fit_transform(X)
X_ploy[0]

# %%
from sklearn.linear_model import LinearRegression
line_reg = LinearRegression()
line_reg.fit(X_ploy,y)
print(line_reg.coef_)
print(line_reg.intercept_)
#coef 0 ---x  1---x**2  intercept---常数项

# %%
plt.plot(X,y,'b.')
plt.xlabel('X')
plt.ylabel('y')
plt.axis([-3,3,-3,9])
X_lab = np.arange(-3,3,0.1).reshape(60,1)
#注意coef是一个矩阵
#也可以使用np.linespace(-3,3,100).reshape(100,1)
#-3，3中间分割100份
#y_lab = line_reg.intercept_+line_reg.coef_[:,0]*X_lab+line_reg.coef_[:,1]*X_lab**2
#这里也可以使用PolynomialFeatures来获得多项式的值
X_lab_poly = poly.transform(X_lab)
y_lab = line_reg.predict(X_lab_poly)
plt.plot(X_lab,y_lab,'r--')
plt.show()


```

### 模型复杂度

对比试验：使用高纬度的函数

- 得到数据
- 标准化
- 训练模型

使用`from sklearn.pipeline import Pipeline`来进行流水线流程

使用`from sklearn.preprocessing import StandardScaler`进行标准化

degree对模型的影响

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
plt.figure(figsize=(15,7))

for style,width,degree in (('g--+',1,50),('b--o',1,2),('r--*',1,1)):
    poly_feature = PolynomialFeatures(degree=degree,include_bias=False)
    std = StandardScaler()
    line_reg = LinearRegression()
    #执行流水化操作
    pipe_reg = Pipeline([
        ('poly_feature',poly_feature),
        ('standard',std),
        ('line_reg',line_reg)
    ])
    pipe_reg.fit(X,y)
    y_new_2=pipe_reg.predict(X_lab)
    plt.plot(X_lab,y_new_2,style,label=str(degree),linewidth=width)
plt.legend('upper right')
plt.plot(X,y,'b.')
plt.axis([-3,3,-5,10])
plt.show()
#如果degree 也就是函数的度数过高，会造成过拟合问题
```

**检查样本数量对模型的影响**

使用`from sklearn.metrics import mean_squared_error`误差军方来查看模型的好坏

- 通过`from sklearn.model_selection import train_test_split`来分割样本

```python
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
train_errors = []
test_errors=[]

def plot_learning_curves(model,X,y):
    X_train, X_test, y_train, y_test=train_test_split(X,y,test_size=0.2,random_state=100)
    train_errors,val_errors = [],[]
    for m in range(1,len(X_train)):
        model.fit(X_train[:m],y_train[:m])
        y_train_predict = model.predict(X_train[:m])
        y_test_predict = model.predict(X_test)
        train_errors.append(mean_squared_error(y_train[:m],y_train_predict[:m]))
        test_errors.append(mean_squared_error(y_test,y_test_predict))
    plt.plot(np.sqrt(train_errors),'r--+',linewidth = 2 ,label='train_error')
    plt.plot(np.sqrt(test_errors),'g--o',linewidth = 2 ,label='test_errors')
    
    
line_reg = LinearRegression()
plt.figure(figsize=(15,7))
plot_learning_curves(line_reg,X,y)
plt.axis([-1,80,0,4])
plt.legend()
plt.show()
```

### 正则化作用

degree过高时，验证损失函数和测试损失函数的图像

```python
pipe_reg = Pipeline([
        ('poly_feature',PolynomialFeatures(degree=10,include_bias=False)),
        ('line_reg',LinearRegression())
    ])
plot_learning_curves(pipe_reg,X,y)
plt.axis([-1,80,0,8])
plt.legend()
plt.show()
```

正则化就是解决过拟合问题

> 正则化是在经验风险项后面加上正则罚项，使得通过最小化经验风险求解模型参数转变为通过最小化结构风险求解模型参数，进而选择经验风险小并且简单的模型。

$$
J(\theta) = MSE(\theta)+\alpha{1 \over 2}\sum_{i=1}^n\theta_i^2
$$

设$x = [1,1,1,1]$,$\theta_1=[1,0,0,0]$,$\theta_2=[{1 \over 4},{1 \over 4},{1 \over 4},{1 \over 4}]$

两者的结果都是一样的

如果加上正则损失项

$J(\theta_1)=...+1^2+0=...+1$,$J(\theta_2)=...+{1 \over 4}^2*4=...+{1 \over 4}$

那么很明显$\theta_2$损失函数结果较小

### 岭回归和lasso

Linear least squares with l2 regularization.

Minimizes the objective function:
$$
||y - Xw||^2_2 + alpha * ||w||^2_2
$$
alpha控制正则化惩罚力度

> 个人理解：
>
> 因为数据样本中一直存在噪声，如果我们直接通过数据集训练的话，那些有噪声的特征就会被放大，从而导致过拟合
>
> 如果使用正则化过程中 $\theta_j=\theta_j(1-\beta{\alpha \over m})-\beta{1 \over m}\sum_{i=1}^m(h_\theta(x^{(i)})-y^{(i)})*x_j^{(i)}$
>
> 可见后半部分不变，前半部分乘一个小于1的函数，那么误差就会减小！！

lasso 就是一个绝对值！！！

```python
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
np.random.seed(42)
m=20
X = 3*np.random.rand(m,1)
y = 0.5*X+np.random.randn(m,1)/1.5+1
X_new = np.linspace(0,3,100).reshape(100,1)

def plot_model(model_class , ploynomial , alphas ,**model_kargs):
    for alpha,style in zip(alphas,('b--','g--','r:')) :
        model = model_class(alpha,**model_kargs)
        if ploynomial:
            model = Pipeline([
            ('poly_feature',PolynomialFeatures(degree=15,include_bias=False)),
            ('Standard',StandardScaler()),
            ('line_reg',model)
            ])
        model.fit(X,y)
        y_new_regul = model.predict(X_new)
        lw = 2 if alpha > 0 else 1
        plt.plot(X_new , y_new_regul,style,linewidth=lw,label=f'alpha ={alpha}')
    plt.plot(X,y,'b.')
    plt.legend()

# %%
plt.figure(figsize=(15,7))
plt.subplot(121)
plot_model(Lasso,ploynomial=True,alphas=(0,0.01,1))
plt.subplot(122)
plot_model(Ridge,ploynomial=True,alphas=(0,0.01,1))
plt.axis([0,3,0,10])
plt.show()

```

