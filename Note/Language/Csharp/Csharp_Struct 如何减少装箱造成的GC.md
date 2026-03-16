
造成装箱和拆箱操作的原因是 --- struct 被当做 object 进行操作。
有以下情况造成装箱和拆箱操作：

1. 使用未重载的函数如 `ToString, GetType` 等
解决方案 ： 重载这些函数

2. 被当做Object参数传递
解决方案 : 继承Interface 接口，然后泛型方法如下 `void Test(T t) : where T : A`

3. 有的时候装箱拆箱不可避免，那么可以通过继承统一接口来提前
Struct A and B 继承 I 接口 那么 `Test(I i)` 拿到之后就会进行拆箱， 内部就不会再有装箱和拆箱操作了。

