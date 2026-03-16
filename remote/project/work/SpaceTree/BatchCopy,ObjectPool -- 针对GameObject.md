
## BatchCopy

一个简易对象池。仅有对象存储+拿取+扩容的功能

### Init

创建父对象 go， 并在下面挂在一定数量的子物体

### Clone


复制一个 go 对象， 然后设置 hideFlags (不显示在 Inspector ). 然后将子武器全部提取出来， 然后删除复制的 go 对象


### ObjectPool

对象池。

利用 BatchCopy 实现的对象池