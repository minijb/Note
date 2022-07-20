![image-20220718165456402](img/image-20220718165456402.png)

![image-20220718174131711](img/image-20220718174131711.png)

![image-20220718174723519](img/image-20220718174723519.png)

![image-20220718174848881](img/image-20220718174848881.png)

RNNt时刻的结构来自t时刻的输入和t-1时刻的结果

RNN的问题是网络越深很可能出现梯度爆炸，即某一个错误可能深度的影响全局

## LSTM

![image-20220718175113127](img/image-20220718175113127.png)

![1](https://img-blog.csdnimg.cn/20190317220617154.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FpYW45OQ==,size_16,color_FFFFFF,t_70)

- $f_t$遗忘门,

- $i_t$输入门，

- $o_t$输出门,

- $\hat{c_t}$临时(ceil state)
- $c_t$ceil state

![111](https://img-blog.csdnimg.cn/20190317220810201.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FpYW45OQ==,size_16,color_FFFFFF,t_70)![在这里插入图片描述](https://img-blog.csdnimg.cn/201903172208332.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FpYW45OQ==,size_16,color_FFFFFF,t_70)

https://blog.csdn.net/qian99/article/details/88628383 LSTM详细解析

- $h_t$输出

## 双向LSTM

![image-20220718180604763](img/image-20220718180604763.png)

![image-20220718200150548](img/image-20220718200150548.png)

![image-20220718200614572](img/image-20220718200614572.png)

我们得到发射分数就可以得到每个单词对应标签的最大可能性 

但是为什么使用CRF呢？

![image-20220718202913739](img/image-20220718202913739.png)

CRF可以对标签之间进行约束，以此来减少

![image-20220718203058382](img/image-20220718203058382.png)

![image-20220718203159810](img/image-20220718203159810.png)

转移分数是不同标签之间转移的分数以此来减少错误

![image-20220718203230788](img/image-20220718203230788.png)

最终得分等于转移分数加上发射分数

总的路径分数计算

![image-20220718204726851](img/image-20220718204726851.png)

## CRF损失函数以及维特比解码

![image-20220719092649897](img/image-20220719092649897.png)

### Viterbi算法（解码）

![image-20220719093254403](img/image-20220719093254403.png)

![image-20220719093708081](img/image-20220719093708081.png)

得到每种情况中分数最高的那一项

到了C项只需要再B项中（在之前的基础上）选择而不用关注A项是如何的，这样就大大减少了流程

最终解码的时间度

![image-20220719094319693](img/image-20220719094319693.png)

### CRF损失函数

![image-20220719094359271](img/image-20220719094359271.png)

$S_n$为转移分数+发射分数，$P_n$为路径，loss也就是真实路径比上总体路径的值，值越大越好

为了求最小值，使用$-log$

最后$log(e^{S_1}+e^{S_2}+e^{S_3}+...+e^{S_N})$也是使用到动态规划来进行计算

![image-20220719100034504](img/image-20220719100034504.png)

![image-20220719100057008](img/image-20220719100057008.png)

如何更新previous，之后带入到之前的previous矩阵进行计算得到新的scores



