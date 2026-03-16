
1. Material Property Block --- 原本相同的材质才可以进行合批(Color 不一样就会生成材质)， 使用 Material Property Block 可以不生成相似的材质。‘

https://blog.csdn.net/liweizhao/article/details/81937590

2. 使用 Constant Buffer 进行优化， 将不怎么变动的数据  直接放到 GPU 内。



### Constant Buffer

每帧更新，且每次更新提交的数据都是整个constant buffer。基于此需要合理安排什么变量纳入其中。
常量的概念只是在单帧内保持不变，整个游戏运行过程中是允许修改这些buffer的


https://www.cnblogs.com/lanyelinxiang/p/16792845.html

https://zhuanlan.zhihu.com/p/35830868